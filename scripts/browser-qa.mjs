import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const chromeBinary = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const expectedBookCount = catalogue.books.length;
const expectedCoverMotifs = catalogue.books.map(book => book.cover.motif).sort();
const books = catalogue.books.map(book => book.file);
// Each phase owns a fresh browser/profile and finishes within Chrome's 30s limit.
// Reader layout, focus, desktop rail and iOS coverage stay independent of discovery.
const phases = ['discovery', 'readers-320', 'readers-900', 'readers-960', 'focus', 'ios'];
const phase = process.argv.find(arg => arg.startsWith('--phase='))?.slice(8);
const outputDir = process.env.BOOK_LIBRARY_QA_DIR || fs.mkdtempSync(path.join(os.tmpdir(), 'book-library-discovery-qa-'));
if (path.resolve(outputDir) === root || path.resolve(outputDir).startsWith(root + path.sep)) throw new Error('QA artifacts must stay outside the repository');
fs.mkdirSync(outputDir, { recursive: true });
if (!phase) {
  for (const nextPhase of phases) {
    const run = spawnSync(process.execPath, [fileURLToPath(import.meta.url), `--phase=${nextPhase}`], {
      cwd: root, encoding: 'utf8', timeout: 45000,
      env: { ...process.env, BOOK_LIBRARY_QA_DIR: outputDir }
    });
    process.stdout.write(run.stdout || '');
    process.stderr.write(run.stderr || '');
    if (run.status !== 0) process.exit(run.status || 1);
  }
  console.log(`Browser QA passed. Reports and screenshots: ${outputDir}`);
  process.exit(0);
}
if (!phases.includes(phase)) throw new Error(`Unknown QA phase: ${phase}`);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'book-tiktok-chrome-'));
let summary = {};
let server;
let chrome;
let socket;
let cleaned = false;

function freePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', reject);
    probe.listen(0, '127.0.0.1', () => {
      const { port } = probe.address();
      probe.close(() => resolve(port));
    });
  });
}

function delay(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

async function waitFor(fn, label, timeout = 7000) {
  const started = Date.now();
  let lastError;
  while (Date.now() - started < timeout) {
    try {
      const result = await fn();
      if (result) return result;
    } catch (error) { lastError = error; }
    await delay(75);
  }
  throw new Error(`${label} timed out${lastError ? `: ${lastError.message}` : ''}`);
}

function cleanup() {
  if (cleaned) return;
  cleaned = true;
  if (socket && socket.readyState <= 1) socket.close();
  if (chrome && chrome.pid) {
    // This detached process group belongs only to this phase/profile. Do not
    // leave helpers running or let a closing browser recreate its profile.
    try { process.kill(-chrome.pid, 'SIGKILL'); } catch (_) {}
  }
  if (server && server.pid) {
    try { server.kill('SIGTERM'); } catch (_) {}
  }
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 80 });
}

process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });
process.on('SIGTERM', () => { cleanup(); process.exit(143); });

const httpPort = await freePort();
const debugPort = await freePort();
server = spawn('python3', ['-m', 'http.server', String(httpPort), '--bind', '127.0.0.1', '--directory', root], {
  stdio: 'ignore'
});

chrome = spawn('/usr/bin/timeout', [
  '30', chromeBinary, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--user-data-dir=${profile}`, `--remote-debugging-port=${debugPort}`, '--window-size=390,844', 'about:blank'
], { stdio: 'ignore', detached: true });

await waitFor(async () => {
  const response = await fetch(`http://127.0.0.1:${debugPort}/json/list`);
  if (!response.ok) return false;
  const targets = await response.json();
  return targets.find(target => target.type === 'page' && target.webSocketDebuggerUrl);
}, 'Chrome DevTools target').then(target => {
  socket = new WebSocket(target.webSocketDebuggerUrl);
});

await new Promise((resolve, reject) => {
  socket.addEventListener('open', resolve, { once: true });
  socket.addEventListener('error', reject, { once: true });
});

let commandId = 0;
const pending = new Map();
const runtimeErrors = [];
socket.addEventListener('message', event => {
  const message = JSON.parse(String(event.data));
  if (message.id && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolve(message.result || {});
  } else if (message.method === 'Runtime.exceptionThrown') {
    runtimeErrors.push(message.params.exceptionDetails?.text || 'Runtime exception');
  } else if (message.method === 'Log.entryAdded' && message.params.entry.level === 'error') {
    runtimeErrors.push(message.params.entry.text);
  }
});
socket.addEventListener('close', () => {
  for (const request of pending.values()) {
    clearTimeout(request.timer);
    request.reject(new Error(`Chrome closed during ${phase}`));
  }
  pending.clear();
});

function command(method, params = {}) {
  const id = ++commandId;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`${method} timed out during ${phase}`)); }, 7000);
    pending.set(id, { resolve: result => { clearTimeout(timer); resolve(result); }, reject: error => { clearTimeout(timer); reject(error); }, timer });
    socket.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(expression) {
  const result = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'Evaluation failed');
  return result.result?.value;
}

async function navigate(pathname, condition) {
  const previousDocument = `${Date.now()}-${Math.random()}`;
  await evaluate(`window.__bookQaLeaving = ${JSON.stringify(previousDocument)}`);
  await command('Page.navigate', { url: `http://127.0.0.1:${httpPort}/${pathname}` });
  await waitFor(async () => evaluate(`window.__bookQaLeaving !== ${JSON.stringify(previousDocument)} && document.readyState === 'complete' && (${condition})`), `load ${pathname}`);
}

function assert(value, message) {
  if (!value) throw new Error(message);
}

await command('Page.enable');
await command('Runtime.enable');
await command('Log.enable');
await command('Network.enable');
await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });

if (phase === 'discovery') {
  await navigate('', `document.querySelectorAll('.book').length === ${expectedBookCount}`);
  await evaluate('document.fonts.ready.then(() => true)');
  const initial = await evaluate(`({
    books: document.querySelectorAll('.book').length,
    stats: [bookStat.textContent, screenStat.textContent, topicStat.textContent],
    manifest: document.querySelector('link[rel="manifest"]')?.getAttribute('href'),
    flexoki: document.querySelector('.flexoki-credit')?.href,
    coverBackgrounds: [...document.querySelectorAll('.cover')].map(node => getComputedStyle(node).backgroundColor),
    covers: [...document.querySelectorAll('.cover[data-cover-motif]')].map(node => ({
      motif: node.dataset.coverMotif, svg: Boolean(node.querySelector('.cover__art svg')),
      width: node.getBoundingClientRect().width, height: node.getBoundingClientRect().height
    }))
  })`);
  assert(initial.manifest === './manifest.webmanifest', 'homepage: manifest link missing');
  assert(initial.flexoki === 'https://stephango.com/flexoki', 'homepage: official Flexoki credit missing');
  assert(initial.covers.length === expectedBookCount && initial.covers.every(cover => cover.svg && cover.width > 0 && cover.height > 0), 'homepage: a semantic cover is missing or collapsed');
  assert(JSON.stringify(initial.covers.map(cover => cover.motif).sort()) === JSON.stringify(expectedCoverMotifs), 'homepage: rendered cover motifs differ from books.json');
  assert(new Set(initial.covers.map(cover => cover.motif)).size === expectedBookCount, 'homepage: cover motifs are not unique');
  assert(Number(initial.stats[0].match(/[0-9]+/)[0]) === expectedBookCount, 'homepage: total book count is wrong');
  assert(Number(initial.stats[1].match(/[0-9]+/)[0]) === catalogue.books.reduce((sum, book) => sum + book.screenCount, 0), 'homepage: total screen count is wrong');
  const allSlugs = catalogue.books.map(book => book.slug);
  const checkVisible = async (expected, label) => {
    const actual = await evaluate(`({
      slugs: [...document.querySelectorAll('.book')].map(node => node.dataset.book),
      count: Number(filterSummary.textContent.match(/[0-9]+/)[0]),
      statusHidden: libraryStatus.hidden
    })`);
    assert(new Set(actual.slugs).size === actual.slugs.length, `${label}: duplicate books`);
    assert(JSON.stringify(actual.slugs.sort()) === JSON.stringify([...expected].sort()), `${label}: unexpected books: ${actual.slugs.join(', ')}`);
    assert(actual.count === expected.length && actual.statusHidden === (expected.length > 0), `${label}: result count/empty state mismatch`);
  };
  const setQuery = query => evaluate(`searchInput.value = ${JSON.stringify(query)}; searchInput.dispatchEvent(new Event('input', { bubbles: true }));`);
  const setTopic = topic => evaluate(`topicFilter.value = ${JSON.stringify(topic)}; topicFilter.dispatchEvent(new Event('change', { bubbles: true }));`);
  const setType = type => evaluate(`document.querySelector('[data-type="${type}"]').click()`);
  const reset = () => evaluate('resetFilters.click()');
  const screenshots = [];
  const viewportChecks = [];
  for (const width of [320, 390, 900, 960, 1440]) {
    await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : width < 900 ? 844 : 900, deviceScaleFactor: 1, mobile: width < 900 });
    for (const language of ['ru', 'en']) {
      if (await evaluate('document.documentElement.lang') !== language) await evaluate('languageButton.click()');
      for (const theme of ['dark', 'light']) {
        if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('themeButton.click()');
        const layout = await evaluate(`(() => {
          const controls = [...document.querySelectorAll('#typeFilter button, #topicFilter, #searchInput')];
          return {
            overflow: document.documentElement.scrollWidth - innerWidth,
            firstBookTop: document.querySelector('.book').getBoundingClientRect().top,
            controlsInside: controls.every(node => { const rect = node.getBoundingClientRect(); return rect.left >= -1 && rect.right <= innerWidth + 1 && rect.height >= 44; }),
            language: document.documentElement.lang, theme: document.documentElement.dataset.theme,
            themeAction: themeButton.textContent, themeAria: themeButton.getAttribute('aria-label'),
            primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim(),
            types: [...document.querySelectorAll('#typeFilter [data-type]')].map(node => node.dataset.type),
            aria: document.querySelector('.discovery').getAttribute('aria-label'),
            topicAria: topicFilter.getAttribute('aria-label'),
            administrative: /Сыну|For my son|Без подборки|No collection|14[+]/.test(document.body.innerText)
          };
        })()`);
        assert(layout.overflow <= 1, `${width}/${language}/${theme}: homepage overflow ${layout.overflow}px`);
        assert(layout.controlsInside && layout.types.join(',') === 'all,fiction,nonfiction', `${width}/${language}/${theme}: discovery controls clipped/missing`);
        assert(layout.language === language && layout.theme === theme, 'homepage: language/theme did not change');
        const expectedThemeAction = language === 'ru' ? (theme === 'dark' ? 'Светлая' : 'Тёмная') : (theme === 'dark' ? 'Light' : 'Dark');
        assert(layout.themeAction === expectedThemeAction && layout.themeAria === expectedThemeAction, 'homepage: theme button does not describe its next action');
        assert(layout.primary === (theme === 'dark' ? '#2f968d' : '#1c6c66'), 'homepage: quiet action tokens changed');
        assert(layout.aria === (language === 'ru' ? 'Поиск и фильтры' : 'Search and filters') && layout.topicAria === (language === 'ru' ? 'Жанр или тема' : 'Genre or subject'), 'homepage: discovery aria labels not localized');
        assert(!layout.administrative, 'homepage: audience/admin choices leaked into discovery');
        if (width < 900) assert(layout.firstBookTop <= 410, `${width}/${language}: books arrive too late (${layout.firstBookTop}px)`);
        await checkVisible(allSlugs, `${width}/${language}/${theme} all books`);
        viewportChecks.push({ width, language, theme, firstBookTop: layout.firstBookTop, overflow: layout.overflow });
        if ((width === 320 && language === 'ru' && theme === 'dark') ||
            (width === 390 && language === 'en' && theme === 'light') ||
            (width === 900 && language === 'en' && theme === 'dark') ||
            (width === 960 && language === 'ru' && theme === 'light') ||
            (width === 1440 && ((language === 'ru' && theme === 'dark') || (language === 'en' && theme === 'light')))) {
          const filename = path.join(outputDir, `home-${width}-${language}-${theme}.png`);
          const capture = await command('Page.captureScreenshot', { format: 'png' });
          fs.writeFileSync(filename, Buffer.from(capture.data, 'base64')); screenshots.push(filename);
        }
      }
    }
  }
  const lightBackgrounds = await evaluate('[...document.querySelectorAll(".cover")].map(node => getComputedStyle(node).backgroundColor)');
  assert(lightBackgrounds.every((background, index) => background !== initial.coverBackgrounds[index]), 'homepage: semantic cover tones did not switch themes');

  // Check type/facet counts and overlapping membership in both languages/themes.
  const discoveryModes = [['ru', 'dark'], ['ru', 'light'], ['en', 'dark'], ['en', 'light']];
  let facetCases = 0;
  for (const [language, theme] of discoveryModes) {
    if (await evaluate('document.documentElement.lang') !== language) await evaluate('languageButton.click()');
    if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('themeButton.click()');
    for (const type of ['all', 'fiction', 'nonfiction']) {
      await reset(); await setType(type);
      const typeBooks = catalogue.books.filter(book => type === 'all' || book.workTypes.includes(type));
      await checkVisible(typeBooks.map(book => book.slug), `type=${type}`);
      const options = await evaluate('[...topicFilter.options].map(node => ({ id: node.value, count: Number(node.textContent.match(/ · ([0-9]+)$/)[1]) }))');
      const facets = catalogue.discovery.genres.concat(catalogue.discovery.subjects);
      for (const option of options) {
        const expected = typeBooks.filter(book => option.id === 'all' || book.genres.includes(option.id) || book.subjects.includes(option.id));
        assert(option.count === expected.length, `${type}/${option.id}: wrong facet count`);
        if (option.id !== 'all') assert(expected.length > 0, `${type}: an unused topic is displayed`);
        facetCases += 1;
        await setTopic(option.id);
        await checkVisible(expected.map(book => book.slug), `${type}/${option.id}`);
      }
      const expectedIds = ['all', ...facets.filter(facet => typeBooks.some(book => book.genres.includes(facet.id) || book.subjects.includes(facet.id))).map(facet => facet.id)];
      assert(JSON.stringify(options.map(option => option.id).sort()) === JSON.stringify(expectedIds.sort()), `${type}: missing/unused genre or subject options`);
    }
  }
  const searches = [
    ['фантастика', catalogue.books.filter(book => book.genres.includes('science-fiction')).map(book => book.slug)],
    ['science fiction', catalogue.books.filter(book => book.genres.includes('science-fiction')).map(book => book.slug)],
    ['стоицизм', ['a-guide-to-the-good-life']], ['стоики', ['a-guide-to-the-good-life']],
    ['stoic', ['a-guide-to-the-good-life']], ['sci-fi', catalogue.books.filter(book => book.genres.includes('science-fiction')).map(book => book.slug)],
    ['Сапольски', catalogue.books.filter(book => book.collections.includes('sapolsky')).map(book => book.slug)],
    ['Sapolsky', catalogue.books.filter(book => book.collections.includes('sapolsky')).map(book => book.slug)],
    ['Толкин', ['the-hobbit']], ['Tolkien', ['the-hobbit']],
    ['Дети капитана Гранта', ['children-of-captain-grant']], ['The Children of Captain Grant', ['children-of-captain-grant']],
    ['все решено', ['determined']], ['Принятие решений', catalogue.books.filter(book => book.tags.includes('decision-making')).map(book => book.slug)],
    ['ИИ', ['hermes-nous', 'akselerando']], ['Сунь цзы', ['the-art-of-war']],
    ['Философия и смысл', catalogue.books.filter(book => book.subjects.includes('philosophy-meaning')).map(book => book.slug)],
    ['Psychology and relationships', catalogue.books.filter(book => book.subjects.includes('psychology-relationships')).map(book => book.slug)],
    ...['white-fang', 'i-robot', 'the-two-captains', 'the-wee-free-men', 'the-hitchhikers-guide-to-the-galaxy']
      .flatMap(slug => {
        const book = catalogue.books.find(book => book.slug === slug);
        return book ? [[book.title.ru, [slug]], [book.title.en, [slug]]] : [];
      }),
    ['not-a-real-book-947', []]
  ];
  for (const [language, theme] of discoveryModes) {
    if (await evaluate('document.documentElement.lang') !== language) await evaluate('languageButton.click()');
    if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('themeButton.click()');
    for (const [query, expected] of searches) {
      await reset(); await setQuery(query); await checkVisible(expected, `${language} search ${query}`);
      const counts = await evaluate('[...document.querySelectorAll("#typeFilter button")].map(node => Number(node.querySelector(".filter-button__count").textContent))');
      const expectedBooks = catalogue.books.filter(book => expected.includes(book.slug));
      assert(JSON.stringify(counts) === JSON.stringify([expectedBooks.length, ...['fiction','nonfiction'].map(type => expectedBooks.filter(book => book.workTypes.includes(type)).length)]), `${query}: type counts ignore query`);
    }
  }
  await reset(); await setType('fiction'); await setTopic('adventure'); await setQuery('фантастика');
  await checkVisible(catalogue.books.filter(book => book.workTypes.includes('fiction') && book.genres.includes('adventure') && book.genres.includes('science-fiction')).map(book => book.slug), 'composed type + genre + bilingual topic query');
  const scienceFictionCount = catalogue.books.filter(book => book.workTypes.includes('fiction') && book.genres.includes('science-fiction')).length;
  assert(await evaluate(`[...topicFilter.options].find(node => node.value === "science-fiction").textContent.endsWith(" · ${scienceFictionCount}")`), 'genre counts must respect type/query, not the active genre');
  await waitFor(() => evaluate('new URL(location.href).searchParams.get("type") === "fiction" && new URL(location.href).searchParams.get("topic") === "adventure" && new URL(location.href).searchParams.get("q") === "фантастика"'), 'composed filters update URL');
  await setType('nonfiction'); await checkVisible([], 'incompatible visible type/genre combination');
  assert(await evaluate('topicFilter.value === "adventure" && topicFilter.selectedOptions[0].textContent.endsWith(" · 0")'), 'active zero-count genre became invisible');
  await reset(); await checkVisible(allSlugs, 'clear all after empty results');
  await waitFor(() => evaluate('!new URL(location.href).search'), 'clear all clears URL');
  assert(await evaluate('searchInput.value === "" && topicFilter.value === "all" && !new URL(location.href).search && document.activeElement === searchInput'), 'clear all did not clear URL/focus/controls');

  // Real keyboard activation; rerenders must preserve focus on native controls.
  await evaluate('document.querySelector("[data-type=fiction]").focus()');
  await command('Input.dispatchKeyEvent', { type: 'keyDown', key: ' ', code: 'Space', windowsVirtualKeyCode: 32 });
  await command('Input.dispatchKeyEvent', { type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32 });
  assert(await evaluate('document.activeElement.dataset.type === "fiction" && document.activeElement.getAttribute("aria-pressed") === "true"'), 'Space activation lost type-button focus');
  await evaluate('topicFilter.focus()');
  await command('Input.dispatchKeyEvent', { type: 'keyDown', key: 's', code: 'KeyS', text: 's', windowsVirtualKeyCode: 83 });
  await command('Input.dispatchKeyEvent', { type: 'keyUp', key: 's', code: 'KeyS', windowsVirtualKeyCode: 83 });
  const keyboardTopic = await evaluate('({ focused: document.activeElement.id, value: topicFilter.value, selected: topicFilter.selectedOptions[0]?.textContent })');
  assert(keyboardTopic.focused === 'topicFilter' && keyboardTopic.value !== 'all', `native genre/subject selector cannot be changed with the keyboard: ${JSON.stringify(keyboardTopic)}`);

  // Old links have explicit, visible replacements; no legacy/audience filter survives.
  for (const [kind, mappings] of [['section', catalogue.discovery.legacySections], ['collection', catalogue.discovery.legacyCollections]]) {
    for (const [id, mapping] of Object.entries(mappings)) {
      await navigate(`?${kind}=${id}`, 'document.getElementById("books").getAttribute("aria-busy") === "false"');
      const expected = catalogue.books.filter(book =>
        (!mapping.type || book.workTypes.includes(mapping.type)) &&
        (!mapping.topic || book.genres.includes(mapping.topic) || book.subjects.includes(mapping.topic)) &&
        (!mapping.query || Object.values(book.author).join(' ').toLowerCase().includes(mapping.query.toLowerCase()))
      ).map(book => book.slug);
      await checkVisible(expected, `legacy ${kind}=${id}`);
      assert(await evaluate(`!new URL(location.href).searchParams.has(${JSON.stringify(kind)}) && !discoveryNotice.hidden && topicFilter.value === ${JSON.stringify(mapping.topic || 'all')} && searchInput.value === ${JSON.stringify(mapping.query || '')} && document.querySelector('[data-type="${mapping.type || 'all'}"]').getAttribute('aria-pressed') === 'true'`), `legacy ${id}: mapping is invisible or URL not canonical`);
    }
  }
  await navigate('?type=missing&topic=missing&q=', 'document.getElementById("books").getAttribute("aria-busy") === "false"');
  await checkVisible(allSlugs, 'invalid URL filters');
  assert(await evaluate('!discoveryNotice.hidden && topicFilter.value === "all"'), 'invalid filters were not explained');

  await reset(); await setType('nonfiction'); await setTopic('philosophy-meaning'); await setQuery('стоицизм');
  if (await evaluate('document.documentElement.lang') !== 'en') await evaluate('languageButton.click()');
  if (await evaluate('document.documentElement.dataset.theme') !== 'light') await evaluate('themeButton.click()');
  await navigate('?type=nonfiction&topic=philosophy-meaning&q=стоицизм', 'document.getElementById("books").getAttribute("aria-busy") === "false"');
  await checkVisible(['a-guide-to-the-good-life'], 'URL filter + language/theme persistence');
  assert(await evaluate('document.documentElement.lang === "en" && document.documentElement.dataset.theme === "light" && searchInput.value === "стоицизм"'), 'language/theme or query changed on navigation');
  const saveScreenshot = async name => {
    const filename = path.join(outputDir, name + '.png');
    const capture = await command('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(filename, Buffer.from(capture.data, 'base64')); screenshots.push(filename);
  };
  await saveScreenshot('home-1440-philosophy-en-light');
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await reset(); await evaluate('languageButton.click(); themeButton.click()');
  await setType('fiction'); await setTopic('fantasy');
  await checkVisible(catalogue.books.filter(book => book.workTypes.includes('fiction') && book.genres.includes('fantasy')).map(book => book.slug), 'phone fantasy');
  await saveScreenshot('home-390-fiction-fantasy-ru-dark');
  await command('Emulation.setDeviceMetricsOverride', { width: 320, height: 568, deviceScaleFactor: 1, mobile: true });
  await evaluate('themeButton.click()'); await setQuery('not-a-real-book-947');
  await checkVisible([], 'phone empty state');
  assert(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1 && !resetFilters.disabled'), 'phone empty state overflow or missing reset');
  await saveScreenshot('home-320-empty-ru-light');
  await reset();
  await setQuery('all');
  await waitFor(() => evaluate('new URL(location.href).searchParams.get("q") === "all"'), 'literal query all is preserved');

  // A visit to the catalogue must preserve progress for both reader implementations.
  for (const reader of [
    { file: 'essentialism.html', progress: 'book-tiktok.essentialism.lastScreen' },
    { file: 'theory-of-constraints.html', progress: 'tocbook.lastSlide' }
  ]) {
    await navigate(reader.file, 'document.getElementById("story")?.children.length > 0');
    await evaluate(`document.querySelector('[data-start], [data-action="start"]').click(); document.querySelector('#nextButton, #btn-next').click()`);
    const remembered = await evaluate(`localStorage.getItem(${JSON.stringify(reader.progress)})`);
    assert(remembered, `${reader.file}: progress did not save`);
    await navigate('', 'document.getElementById("books")?.getAttribute("aria-busy") === "false"');
    await evaluate('languageButton.click(); themeButton.click()');
    assert(await evaluate(`localStorage.getItem(${JSON.stringify(reader.progress)}) === ${JSON.stringify(remembered)}`), `${reader.file}: homepage changed reading progress`);
    await navigate(reader.file, 'document.getElementById("story")?.children.length > 0');
    assert(await evaluate(`localStorage.getItem(${JSON.stringify(reader.progress)}) === ${JSON.stringify(remembered)} && document.querySelector('[data-start], [data-action="start"]').textContent.includes('Продолжить')`), `${reader.file}: progress did not survive return to reader`);
    await evaluate(`document.querySelector('[data-start], [data-action="start"]').click()`);
    assert(await evaluate(`localStorage.getItem(${JSON.stringify(reader.progress)}) === ${JSON.stringify(remembered)}`), `${reader.file}: Continue did not resume the saved screen`);
  }
  // Exercise the additive schema-2 fallback with an in-memory response, never
  // by rewriting the shared manifest or any book/collector file.
  const schema2 = JSON.parse(JSON.stringify(catalogue));
  delete schema2.discovery;
  for (const book of schema2.books) for (const key of ['workTypes', 'genres', 'subjects', 'workTypeLabel']) delete book[key];
  const fallbackScript = await command('Page.addScriptToEvaluateOnNewDocument', {
    source: `(() => { const fetchOriginal = window.fetch.bind(window); window.fetch = function (resource, options) { return resource === './books.json' ? Promise.resolve(new Response(${JSON.stringify(JSON.stringify(schema2))}, { headers: { 'Content-Type': 'application/json' } })) : fetchOriginal(resource, options); }; })();`
  });
  await navigate('', 'document.getElementById("books")?.getAttribute("aria-busy") === "false"');
  await checkVisible(allSlugs, 'unextended schema-2 catalogue');
  await setType('fiction');
  await checkVisible(catalogue.books.filter(book => book.section === 'fiction-adventure').map(book => book.slug), 'schema-2 fallback fiction');
  await command('Page.removeScriptToEvaluateOnNewDocument', { identifier: fallbackScript.identifier });
  await evaluate('navigator.serviceWorker.ready.then(() => true)');
  summary = { books: expectedBookCount, viewportChecks, facetCases, searches: searches.length * discoveryModes.length, readerProgress: 'both reader implementations preserved', schema2Compatibility: 'passed', legacyLinks: Object.keys(catalogue.discovery.legacySections).length + Object.keys(catalogue.discovery.legacyCollections).length, screenshots };

}

if (phase.startsWith('readers-')) {
  const width = Number(phase.slice(8));
  await command('Emulation.setDeviceMetricsOverride', { width, height: 768, deviceScaleFactor: 1, mobile: width < 900 });
  for (const book of books) {
    await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
    const compact = await evaluate(`(() => {
      const controls = [...document.querySelectorAll('.app-header .topbar a, .app-header .topbar button, .topbar a, .topbar button')]
        .filter(node => getComputedStyle(node).display !== 'none');
      return {
        iconsOnly: controls.every(node => node.textContent.trim() === '' && node.querySelector('svg[data-reader-icon]') && node.getAttribute('aria-label') && node.title),
        language: document.documentElement.lang,
        coverInside: [...document.querySelectorAll('.cover-layout .cover-copy, .cover-layout .cover-visual')].every(node => {
          const pane = document.getElementById('story').getBoundingClientRect();
          const rect = node.getBoundingClientRect();
          return rect.left >= pane.left - 1 && rect.right <= pane.right + 1;
        }),
        controls: controls.length,
        inside: controls.every(node => { const rect = node.getBoundingClientRect(); return rect.left >= -1 && rect.right <= innerWidth + 1; }),
        overflow: document.documentElement.scrollWidth - innerWidth,
        primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim(),
        onPrimary: getComputedStyle(document.documentElement).getPropertyValue('--color-on-primary').trim()
      };
    })()`);
    assert(compact.iconsOnly, `${book}: header controls must be accessible icons without text`);
    assert(compact.coverInside, `${book}: cover clipped inside the ${width}px reader pane`);
    assert(compact.inside, `${book}: topbar control escaped the ${width}px viewport`);
    assert(compact.overflow <= 1, `${book}: ${width}px overflow: ${compact.overflow}px`);
    assert(compact.primary === '#2f968d' && compact.onPrimary === '#100f0f', `${book}: quiet dark action colors were not applied`);
  }
  summary = { readers: books.length, width: Number(phase.slice(8)), headerAndCoverLayout: 'passed' };
}


if (phase === 'focus') {
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  for (const book of books) {
    await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
    const chapterControl = await evaluate(`(() => {
      const button = document.querySelector('#contentsButton, #btn-contents');
      button.focus();
      return button.id;
    })()`);
    await command('Input.dispatchKeyEvent', { type: 'keyDown', key: ' ', code: 'Space', windowsVirtualKeyCode: 32 });
    await command('Input.dispatchKeyEvent', { type: 'keyUp', key: ' ', code: 'Space', windowsVirtualKeyCode: 32 });
    assert(await evaluate(`Boolean(document.querySelector('dialog[open]'))`), `${book}: Space did not activate ${chapterControl}`);
    await evaluate(`document.querySelectorAll('dialog[open]').forEach(dialog => dialog.close()); document.activeElement.blur()`);
    await evaluate(`(() => {
      const start = document.querySelector('[data-start], [data-action="start"]');
      if (start) start.click();
      return true;
    })()`);
    await delay(60);
    await evaluate(`(() => {
      const story = document.getElementById('story');
      story.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 71, pointerType: 'touch', clientX: 120, clientY: 220 }));
      story.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, pointerId: 71, pointerType: 'touch', clientX: 120, clientY: 220 }));
    })()`);
    const focused = await evaluate(`(() => {
      const header = document.querySelector('.app-header, .topbar');
      const previous = document.querySelector('#previousButton, #btn-back');
      const next = document.querySelector('#nextButton, #btn-next');
      const rect = next.getBoundingClientRect();
      return {
        active: document.documentElement.dataset.focusMode === 'true',
        header: header ? getComputedStyle(header).display : 'none',
        previous: previous ? getComputedStyle(previous).display : 'none',
        next: getComputedStyle(next).display,
        nextInside: rect.right <= innerWidth + 1 && rect.bottom <= innerHeight + 1,
        overflow: document.documentElement.scrollWidth - innerWidth
      };
    })()`);
    assert(focused.active, `${book}: focus mode did not activate`);
    assert(focused.header === 'none', `${book}: header remained visible in focus mode`);
    assert(focused.previous === 'none', `${book}: previous control remained visible in focus mode`);
    assert(focused.next !== 'none' && focused.nextInside, `${book}: Next is not visible inside the viewport`);
    assert(focused.overflow <= 1, `${book}: phone overflow in focus mode: ${focused.overflow}px`);
    await evaluate(`(() => {
      const story = document.getElementById('story');
      story.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: 72, pointerType: 'touch', clientX: 120, clientY: 220 }));
      story.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, pointerId: 72, pointerType: 'touch', clientX: 120, clientY: 220 }));
    })()`);
    assert(!(await evaluate(`document.documentElement.dataset.focusMode === 'true'`)), `${book}: second tap did not exit focus mode`);
  }

  summary = { readers: books.length, focusModeAndKeyboard: 'passed' };
}


if (phase === 'ios') {
  await command('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await navigate('theory-of-constraints.html', "document.getElementById('story') && document.getElementById('story').children.length > 0");
  const desktopRail = await evaluate(`getComputedStyle(document.getElementById('desktopRail')).display`);
  assert(desktopRail !== 'none', 'desktop reader rail is not visible');
  await evaluate(`document.documentElement.setAttribute('data-focus-mode', 'true')`);
  const desktopFocus = await evaluate(`(() => ({
    rail: getComputedStyle(document.getElementById('desktopRail')).display,
    shellWidth: document.getElementById('appShell').getBoundingClientRect().width,
    overflow: document.documentElement.scrollWidth - innerWidth
  }))()`);
  assert(desktopFocus.rail === 'none', 'desktop rail remained visible in focus mode');
  assert(desktopFocus.shellWidth <= 901, `desktop focus measure is too wide: ${desktopFocus.shellWidth}px`);
  assert(desktopFocus.overflow <= 1, `desktop focus overflow: ${desktopFocus.overflow}px`);

  await evaluate(`localStorage.removeItem('bookLibrary.installGuide.seen.v2')`);
  await command('Network.setUserAgentOverride', {
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1'
  });
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 3, mobile: true });
  await navigate('essentialism.html?ios-install-qa=1', "document.getElementById('story') && document.getElementById('story').children.length > 0");
  await waitFor(async () => evaluate(`document.getElementById('bookLibraryInstallDialog')?.open === true`), 'iOS install guide');
  const iosInstall = await evaluate(`(() => {
    const trigger = document.getElementById('bookLibraryInstallTrigger');
    const dialog = document.getElementById('bookLibraryInstallDialog');
    return {
      installable: document.documentElement.dataset.bookInstallable === 'true',
      trigger: getComputedStyle(trigger).display,
      dialog: dialog.open,
      title: document.getElementById('bookLibraryInstallTitle').textContent,
      telegram: dialog.textContent.includes('Telegram'),
      overflow: document.documentElement.scrollWidth - innerWidth
    };
  })()`);
  assert(iosInstall.installable, 'iOS browser mode was not detected');
  assert(iosInstall.trigger !== 'none', 'iOS install trigger is hidden in browser mode');
  assert(iosInstall.dialog, 'iOS install guide did not auto-open');
  assert(iosInstall.title === 'Уберите строку Safari' && iosInstall.telegram, 'iOS install guide copy is incomplete');
  assert(iosInstall.overflow <= 1, `iOS install guide overflow: ${iosInstall.overflow}px`);
  await evaluate(`bookLibraryInstallClose.click()`);
  assert(await evaluate(`!bookLibraryInstallDialog.open && localStorage.getItem('bookLibrary.installGuide.seen.v2') === 'true'`), 'iOS install guide did not close or remember dismissal');
  await command('Emulation.setDeviceMetricsOverride', { width: 320, height: 568, deviceScaleFactor: 2, mobile: true });
  const iosHeader = await evaluate(`(() => {
    const controls = [...document.querySelectorAll('.topbar a, .topbar button')];
    const language = document.getElementById('languageButton').getBoundingClientRect();
    return {
      oneRow: controls.every(node => Math.abs(node.getBoundingClientRect().top - language.top) <= 1),
      reachable: controls.every(node => {
        const rect = node.getBoundingClientRect();
        const hit = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
        return rect.left >= -1 && rect.right <= innerWidth + 1 && hit && (hit === node || node.contains(hit));
      }),
      position: getComputedStyle(bookLibraryInstallTrigger).position,
      language: { x: language.x + language.width / 2, y: language.y + language.height / 2 }
    };
  })()`);
  assert(iosHeader.reachable && iosHeader.oneRow && iosHeader.position === 'static', 'iOS header must remain one reachable 320px icon row');
  const languageBeforeClick = await evaluate(`document.documentElement.lang`);
  for (let activation = 0; activation < 2; activation += 1) {
    await command('Input.dispatchMouseEvent', { type: 'mousePressed', ...iosHeader.language, button: 'left', clickCount: 1 });
    await command('Input.dispatchMouseEvent', { type: 'mouseReleased', ...iosHeader.language, button: 'left', clickCount: 1 });
    assert(await evaluate(`document.documentElement.lang`) === (activation === 0 ? (languageBeforeClick === 'ru' ? 'en' : 'ru') : languageBeforeClick), 'iOS guide intercepted the Language click');
  }
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 3, mobile: true });
  await evaluate(`document.documentElement.lang = 'en'; bookLibraryInstallTrigger.click()`);
  assert(await evaluate(`bookLibraryInstallDialog.open && bookLibraryInstallTitle.textContent === 'Remove the Safari bar'`), 'iOS install guide did not localize to English');
  await evaluate(`bookLibraryInstallClose.click(); document.documentElement.setAttribute('data-focus-mode', 'true')`);
  assert(await evaluate(`getComputedStyle(bookLibraryInstallTrigger).display === 'none'`), 'install trigger remained visible in focus mode');

  await command('Page.addScriptToEvaluateOnNewDocument', {
    source: "Object.defineProperty(navigator, 'standalone', { configurable: true, get: function () { return true; } });"
  });
  await navigate('essentialism.html?standalone-qa=1', "document.getElementById('story') && document.getElementById('story').children.length > 0");
  await delay(550);
  const standaloneInstall = await evaluate(`(() => ({
    installable: document.documentElement.dataset.bookInstallable === 'true',
    trigger: getComputedStyle(document.getElementById('bookLibraryInstallTrigger')).display,
    dialog: document.getElementById('bookLibraryInstallDialog').open
  }))()`);
  assert(!standaloneInstall.installable, 'standalone reader was marked installable');
  assert(standaloneInstall.trigger === 'none', 'install trigger remained visible in standalone mode');
  assert(!standaloneInstall.dialog, 'install guide opened in standalone mode');

  summary = { desktopFocusAndRail: 'passed', iosInstallGuide: 'browser and standalone modes passed', physicalIPhone: false };
}

assert(runtimeErrors.length === 0, `browser errors: ${runtimeErrors.join(' | ')}`);
const report = { phase, ...summary, runtimeErrors: runtimeErrors.length };
fs.writeFileSync(path.join(outputDir, `${phase}.json`), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));

cleanup();
process.exit(0);
