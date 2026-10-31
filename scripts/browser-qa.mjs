import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { runRelease09QA } from './release09-browser-checks.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const chromeBinary = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const expectedBookCount = catalogue.books.length;
const expectedCoverMotifs = catalogue.books.map(book => book.cover.motif).sort();
const requestedBooks = process.argv.find(arg => arg.startsWith('--books='))?.slice(8).split(',') || [];
const books = requestedBooks.length ? requestedBooks : catalogue.books.map(book => book.file);
const releaseBooks = requestedBooks.length ? books : ['four-thousand-weeks.html', 'mindfulness.html', 'a-guide-to-the-good-life.html', 'the-body-keeps-the-score.html', 'amphibian-man.html', 'selfie.html'];
if (books.some(file => !catalogue.books.some(book => book.file === file))) throw new Error('QA reader must be registered');
// Each phase owns a fresh browser/profile and finishes within Chrome's 30s limit.
// Reader layout, focus, desktop rail and iOS coverage stay independent of discovery.
const phases = ['discovery', 'readers-320', 'readers-900', 'readers-960', 'focus', 'ios', 'safe-area', 'repaired', 'release-interactions', 'release-reader-interactions', 'release-consent', 'release-closures', 'release-card', 'offline'];
const phase = process.argv.find(arg => arg.startsWith('--phase='))?.slice(8);
const requestedOrigin = process.argv.find(arg => arg.startsWith('--origin='))?.slice(9);
const outputDir = process.env.BOOK_LIBRARY_QA_DIR || fs.mkdtempSync(path.join(os.tmpdir(), 'book-library-discovery-qa-'));
if (path.resolve(outputDir) === root || path.resolve(outputDir).startsWith(root + path.sep)) throw new Error('QA artifacts must stay outside the repository');
fs.mkdirSync(outputDir, { recursive: true });
if (!phase) {
  for (const nextPhase of phases) {
    const run = spawnSync(process.execPath, [fileURLToPath(import.meta.url), `--phase=${nextPhase}`, ...process.argv.filter(arg => arg.startsWith('--books=') || arg.startsWith('--origin='))], {
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
if (![...phases, 'release-state', 'release-cards', 'release-quotations', 'release-migration', 'release-tail', 'release09-guards', 'release09-metadata', 'release09-corrections', 'release09-tail'].includes(phase)) throw new Error(`Unknown QA phase: ${phase}`);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'book-tiktok-chrome-'));
let summary = {};
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
    const rows = spawnSync('ps', ['-axo', 'pid=,ppid='], {encoding:'utf8'}).stdout.trim().split('\n').map(row=>row.trim().split(/\s+/).map(Number));
    const owned = new Set([chrome.pid]);
    for (let pass=0;pass<12;pass++) for (const [pid,ppid] of rows) if (owned.has(ppid)) owned.add(pid);
    try { process.kill(-chrome.pid, 'SIGKILL'); } catch (_) {}
    for (const pid of [...owned].reverse()) { try { process.kill(pid,'SIGKILL'); } catch (_) {} }
  }
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 80 });
}

process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });
process.on('SIGTERM', () => { cleanup(); process.exit(143); });

const fixtureOrigin = requestedOrigin || 'https://book-library.test';
const debugPort = await freePort();

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
const consentDialogs = [];
let consentDecision = false;
let testingFileStandalone = false;
const standaloneManifestDiagnostics = [];
socket.addEventListener('message', event => {
  const message = JSON.parse(String(event.data));
  if (message.id && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolve(message.result || {});
  } else if (message.method === 'Page.javascriptDialogOpening' && ['release-interactions', 'release-consent', 'release-closures', 'release-tail'].includes(phase)) {
    consentDialogs.push({ type: message.params.type, message: message.params.message, accepted: consentDecision });
    command('Page.handleJavaScriptDialog', { accept: consentDecision }).catch(error => runtimeErrors.push(error.message));
  } else if (message.method === 'Fetch.requestPaused') {
    const { requestId, request } = message.params;
    const url = new URL(request.url);
    if (requestedOrigin && url.origin === fixtureOrigin) { command('Fetch.continueRequest', { requestId }); return; }
    if (!requestedOrigin && url.origin === fixtureOrigin && url.pathname !== '/sw.js') {
      const filename = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname).slice(1);
      const file = path.resolve(root, filename);
      if (file.startsWith(root + path.sep) && fs.existsSync(file) && fs.statSync(file).isFile()) {
        const mime = file.endsWith('.html') ? 'text/html; charset=utf-8' : file.endsWith('.json') || file.endsWith('.webmanifest') ? 'application/json' : file.endsWith('.png') ? 'image/png' : 'application/octet-stream';
        command('Fetch.fulfillRequest', { requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: mime }], body: fs.readFileSync(file).toString('base64') }); return;
      }
    }
    command('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' });
  } else if (message.method === 'Runtime.exceptionThrown') {
    runtimeErrors.push(message.params.exceptionDetails?.text || 'Runtime exception');
  } else if (message.method === 'Log.entryAdded' && message.params.entry.level === 'error') {
    const entry = message.params.entry;
    if (testingFileStandalone && (/Access to manifest at 'file:/.test(entry.text) || /\/manifest\.webmanifest$/.test(entry.url || ''))) {
      standaloneManifestDiagnostics.push({ text: entry.text, url: entry.url });
    } else runtimeErrors.push(entry.text);
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
  await command('Page.navigate', { url: `${fixtureOrigin}/${pathname}` });
  await waitFor(async () => evaluate(`window.__bookQaLeaving !== ${JSON.stringify(previousDocument)} && document.readyState === 'complete' && (${condition})`), `load ${pathname}`);
}

function assert(value, message) {
  if (!value) throw new Error(message);
}

await command('Page.enable');
await command('Runtime.enable');
await command('Log.enable');
await command('Network.enable');
await command('Fetch.enable', { patterns: [{ urlPattern: 'http*' }] });
if (!requestedOrigin) await command('Page.addScriptToEvaluateOnNewDocument', { source: "Object.defineProperty(navigator, 'serviceWorker', { value: { register: () => Promise.resolve({}), ready: Promise.resolve({}) } });" });
await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });

if (phase.startsWith('release09-')) summary = await runRelease09QA({ phase, books: releaseBooks, navigate, evaluate, command, assert, catalogue, outputDir });

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
        if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
        const layout = await evaluate(`(() => {
          const controls = [...document.querySelectorAll('#typeFilter button, #topicFilter, #searchInput')];
          return {
            typeWidths: [...document.querySelectorAll('#typeFilter button')].map(node => node.getBoundingClientRect().width),
            labelsInside: [...document.querySelectorAll('#typeFilter button')].every(node => node.scrollWidth <= node.clientWidth + 1),
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
        assert(Math.max(...layout.typeWidths) - Math.min(...layout.typeWidths) <= 1 && layout.labelsInside, `${width}/${language}/${theme}: type tabs unequal or labels overflowing`);
        assert(layout.overflow <= 1, `${width}/${language}/${theme}: homepage overflow ${layout.overflow}px`);
        assert(layout.controlsInside && layout.types.join(',') === 'all,fiction,nonfiction', `${width}/${language}/${theme}: discovery controls clipped/missing`);
        assert(layout.language === language && layout.theme === theme, 'homepage: language/theme did not change');
        const expectedSettingsLabel = language === 'ru' ? 'Настройки' : 'Settings';
        assert(layout.themeAction.trim() === '' && layout.themeAria === expectedSettingsLabel, 'homepage: icon must open localized Settings');
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
    if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
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
    ...['стоицизм', 'стоики', 'stoic'].map(query => [query, catalogue.books.filter(book => book.tags.includes('stoicism')).map(book => book.slug)]),
    ['sci-fi', catalogue.books.filter(book => book.genres.includes('science-fiction')).map(book => book.slug)],
    ['Сапольски', catalogue.books.filter(book => book.collections.includes('sapolsky')).map(book => book.slug)],
    ['Sapolsky', catalogue.books.filter(book => book.collections.includes('sapolsky')).map(book => book.slug)],
    ['Толкин', ['the-hobbit']], ['Tolkien', ['the-hobbit']],
    ['Дети капитана Гранта', ['children-of-captain-grant']], ['The Children of Captain Grant', ['children-of-captain-grant']],
    ['все решено', ['determined']], ['Принятие решений', catalogue.books.filter(book => book.tags.includes('decision-making')).map(book => book.slug)],
    ['ИИ', ['hermes-nous', 'akselerando']], ['Сунь цзы', ['the-art-of-war']],
    ['Философия и смысл', catalogue.books.filter(book => book.subjects.includes('philosophy-meaning')).map(book => book.slug)],
    ['Psychology and relationships', catalogue.books.filter(book => book.subjects.includes('psychology-relationships')).map(book => book.slug)],
    ...['white-fang', 'i-robot', 'the-two-captains', 'the-wee-free-men', 'the-hitchhikers-guide-to-the-galaxy', 'amphibian-man', 'monday-begins-on-saturday', 'meditations', 'the-left-hand-of-darkness', 'atomic-habits', 'huberman-protocols', 'hermes-nous', 'thinking-fast-and-slow', 'thinking-in-systems', 'project-hail-mary', 'the-giver', 'governing-the-commons', 'the-structure-of-scientific-revolutions', 'seeing-like-a-state', 'determined', 'theory-of-constraints', '1873', 'a-wizard-of-earthsea'].concat(releaseBooks.map(file=>file.slice(0,-5)))
      .flatMap(slug => {
        const book = catalogue.books.find(book => book.slug === slug);
        return book ? [[book.title.ru, [slug]], [book.title.en, [slug]]] : [];
      }),
    ['not-a-real-book-947', []]
  ];
  for (const [language, theme] of discoveryModes) {
    if (await evaluate('document.documentElement.lang') !== language) await evaluate('languageButton.click()');
    if (await evaluate('document.documentElement.dataset.theme') !== theme) await evaluate('BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
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
  if (await evaluate('document.documentElement.dataset.theme') !== 'light') await evaluate('BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
  await navigate('?type=nonfiction&topic=philosophy-meaning&q=стоицизм', 'document.getElementById("books").getAttribute("aria-busy") === "false"');
  await checkVisible(catalogue.books.filter(book => book.workTypes.includes('nonfiction') && book.subjects.includes('philosophy-meaning') && book.tags.includes('stoicism')).map(book => book.slug), 'URL filter + language/theme persistence');
  assert(await evaluate('document.documentElement.lang === "en" && document.documentElement.dataset.theme === "light" && searchInput.value === "стоицизм"'), 'language/theme or query changed on navigation');
  const saveScreenshot = async name => {
    const filename = path.join(outputDir, name + '.png');
    const capture = await command('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(filename, Buffer.from(capture.data, 'base64')); screenshots.push(filename);
  };
  await saveScreenshot('home-1440-philosophy-en-light');
  await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: true });
  await reset(); await evaluate('languageButton.click(); BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
  await setType('fiction'); await setTopic('fantasy');
  await checkVisible(catalogue.books.filter(book => book.workTypes.includes('fiction') && book.genres.includes('fantasy')).map(book => book.slug), 'phone fantasy');
  await saveScreenshot('home-390-fiction-fantasy-ru-dark');
  await command('Emulation.setDeviceMetricsOverride', { width: 320, height: 568, deviceScaleFactor: 1, mobile: true });
  await evaluate('BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")'); await setQuery('not-a-real-book-947');
  await checkVisible([], 'phone empty state');
  assert(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1 && !resetFilters.disabled'), 'phone empty state overflow or missing reset');
  await saveScreenshot('home-320-empty-ru-light');
  await reset();
  await setQuery('all');
  await waitFor(() => evaluate('new URL(location.href).searchParams.get("q") === "all"'), 'literal query all is preserved');

  // A catalogue visit preserves progress using the reader's actual storage runtime.
  for (const reader of [
    { file: 'essentialism.html', progress: 'book-tiktok.essentialism.lastScreen' },
    { file: 'theory-of-constraints.html', progress: 'tocbook.lastSlide' }
  ]) {
    await navigate(reader.file, 'document.getElementById("story")?.children.length > 0');
    await evaluate(`document.querySelector('[data-start], [data-action="start"]').click(); document.querySelector('#nextButton, #btn-next').click()`);
    reader.progress = await evaluate(`document.getElementById('book-tiktok-data') ? 'book-tiktok.'+JSON.parse(document.getElementById('book-tiktok-data').textContent).slug+'.lastScreen' : ${JSON.stringify(reader.progress)}`);
    const remembered = await evaluate(`localStorage.getItem(${JSON.stringify(reader.progress)})`);
    assert(remembered, `${reader.file}: progress did not save`);
    await navigate('', 'document.getElementById("books")?.getAttribute("aria-busy") === "false"');
    await evaluate('languageButton.click(); BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark")');
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
  const desktopBook = requestedBooks.length ? books[0] : 'theory-of-constraints.html';
  const installBook = requestedBooks.length ? books[0] : 'essentialism.html';
  await command('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await navigate(desktopBook, "document.getElementById('story') && document.getElementById('story').children.length > 0");
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
  await navigate(installBook + '?ios-install-qa=1', "document.getElementById('story') && document.getElementById('story').children.length > 0");
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
  await navigate(installBook + '?standalone-qa=1', "document.getElementById('story') && document.getElementById('story').children.length > 0");
  await delay(550);
  const standaloneInstall = await evaluate(`(() => ({
    installable: document.documentElement.dataset.bookInstallable === 'true',
    trigger: getComputedStyle(document.getElementById('bookLibraryInstallTrigger')).display,
    dialog: document.getElementById('bookLibraryInstallDialog').open
  }))()`);
  assert(!standaloneInstall.installable, 'standalone reader was marked installable');
  assert(standaloneInstall.trigger === 'none', 'install trigger remained visible in standalone mode');
  assert(!standaloneInstall.dialog, 'install guide opened in standalone mode');

  summary = { desktopBook, installBook, desktopFocusAndRail: 'passed', iosInstallGuide: 'browser and standalone modes passed', physicalIPhone: false };
}

if (phase === 'repaired') {
  const revised = requestedBooks.length ? books : ['the-art-of-war.html', 'essentialism.html', 'skin-in-the-game.html'];
  let rendered = 0;
  const checks = [];
  for (const book of revised) {
    const slug = book.slice(0, -5);
    await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
    await evaluate(`localStorage.setItem('book-tiktok.${slug}.lastScreen', 'removed-old-screen'); localStorage.setItem('book-tiktok.${slug}.mode', 'deep')`);
    await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
    assert(await evaluate(`!document.querySelector('[data-start="continue"]') && document.querySelector('.cover-layout')`), `${book}: stale saved ID did not safely fall back to cover`);
    // This phase measures rendering. Native ending consent is separately exercised below.
    await evaluate('window.confirm = () => true');
    await evaluate(`document.fonts.ready.then(() => true)`);
    for (const width of [320, 390, 1024, 1440]) {
      await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : width < 900 ? 844 : 900, deviceScaleFactor: 1, mobile: width < 900 });
      const result = await evaluate(`(async () => {
        const style = document.createElement('style'); style.textContent = '.story-slide { animation: none !important; }'; document.head.append(style);
        const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
        const failures = []; let count = 0;
        for (const language of ['ru', 'en']) {
          if (document.documentElement.lang !== language) languageButton.click();
          for (const theme of ['dark', 'light']) {
            if (document.documentElement.dataset.theme !== theme) BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark");
            for (const [mode, level] of [['essential', 1], ['core', 2], ['deep', 3]]) {
              document.querySelector('[data-mode="' + mode + '"]').click();
              document.querySelector('#accelerandoSpoilerDialog [data-spoiler-accept], #spoilerDialog[open] [data-spoiler-accept], #spoilerDialog[open] #spoilerAccept, #endingDialog[open] #endingAccept')?.click();
              await Promise.resolve();
              const visible = data.screens.filter(s => s.level <= level);
              const contents = [...document.querySelectorAll('#contentsList [data-go-to]')];
              if (progressTrack.children.length !== data.targetModes[mode]) failures.push(mode + ' reading-route count');
              if (contents.length !== visible.length && contents.length !== data.screens.length) failures.push(mode + ' contents count');
              // Some book-local runtimes list locked placeholders for deeper screens.
              for (const button of contents) {
                const target = data.screens.find(s => s.id === button.dataset.goTo);
                // Custom readers may name non-spoiler Core chapters at Essential.
                // Ending titles must remain masked until the Deep route opens.
                if (target.level === 3 && level < 3 && button.textContent.includes(target.copy[language].title)) failures.push(target.id + ' hidden ending title');
              }
              for (const screen of visible) {
                document.querySelector('#contentsList [data-go-to="' + screen.id + '"]').click();
                await Promise.resolve();
                const scroller = document.querySelector('.slide-scroll');
                if (document.querySelector('#story h1').textContent !== screen.copy[language].title) failures.push(screen.id + ' title');
                if (screen.type !== 'cover') {
                  scroller.scrollTop = scroller.scrollHeight;
                  const tail = [...scroller.querySelectorAll(':scope > p')].filter(node => getComputedStyle(node).display !== 'none').at(-1);
                  if (tail && tail.getBoundingClientRect().bottom > scroller.getBoundingClientRect().bottom + 1) failures.push(screen.id + ' last line unreachable');
                }
                if (scroller.scrollWidth > scroller.clientWidth + 1 || document.documentElement.scrollWidth > innerWidth + 1) failures.push(screen.id + ' overflow');
                count++;
              }
            }
            sourcesButton.click(); if (!sourcesDialog.open || !sourcesList.textContent.trim() || !methodNote.textContent.trim()) failures.push('global sources'); sourcesDialog.close();
          }
        }
        // A retained saved ID resumes the corresponding rewritten screen.
        const remembered = data.screens[1]; localStorage.setItem('book-tiktok.' + data.slug + '.lastScreen', remembered.id);
        document.querySelector('#contentsList [data-go-to="cover"]').click();
        document.querySelector('[data-start="continue"]').click();
        await Promise.resolve();
        if (document.querySelector('#story h1').textContent !== remembered.copy[document.documentElement.lang].title) failures.push('retained resume');
        style.remove(); return { count, failures, counts: data.targetModes };
      })()`);
      assert(!result.failures.length, `${book}/${width}: ${result.failures.join(', ')}`);
      rendered += result.count; checks.push({ book, width, ...result });
      const capture = await command('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(path.join(outputDir, `${slug}-${width}.png`), Buffer.from(capture.data, 'base64'));
    }
  }
  for (const presentation of ['narrative', 'explanatory']) {
    const example = JSON.parse(fs.readFileSync(path.join(root, 'skills/book-tiktok/assets/story-data.example.json'), 'utf8'));
    example.contentMode = presentation; example.slug = 'qa-' + presentation;
    const dataPath = path.join(outputDir, presentation + '.json'); const htmlPath = path.join(outputDir, presentation + '.html');
    fs.writeFileSync(dataPath, JSON.stringify(example));
    const build = spawnSync(process.execPath, [path.join(root, 'skills/book-tiktok/scripts/build_story.mjs'), dataPath, '--out', htmlPath], { encoding: 'utf8' });
    assert(build.status === 0, build.stderr);
    await command('Page.navigate', { url: 'file://' + htmlPath });
    await waitFor(() => evaluate(`location.protocol === 'file:' && document.querySelector('[data-start]')`), 'presentation fixture');
    const result = await evaluate(`(() => { document.querySelector('[data-start]').click(); sourcesButton.click(); return { labels: document.querySelectorAll('.source-label').length, sources: sourcesDialog.open && sourcesList.textContent.trim().length > 0, mapped: JSON.parse(document.getElementById('book-tiktok-data').textContent).screens[1].sources.length > 0 }; })()`);
    assert(result.sources && result.mapped && result.labels === (presentation === 'narrative' ? 0 : 1), `${presentation}: source presentation regression`);
  }
  summary = { readers: revised, rendered, checks, sourcePresentation: 'narrative/explanatory fixtures passed; embedded maps and global Sources preserved', savedProgress: 'removed and retained IDs passed' };
}

if (phase === 'release-interactions' || phase === 'release-reader-interactions') {
  const checks = [];
  for (const book of releaseBooks) {
    await navigate(book, "document.querySelector('[data-start]')");
    const result = await evaluate(`(() => {
      const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
      const first = data.screens.find(s => s.type !== 'cover' && s.level === 1);
      document.querySelector('[data-start]').click();
      const title = document.querySelector('#story h1').textContent;
      languageButton.click();
      if (document.querySelector('#story h1').textContent !== first.copy.en.title) throw Error('language lost position');
      BookSettings.set("theme", document.documentElement.dataset.theme === "dark" ? "light" : "dark");
      if (document.querySelector('#story h1').textContent !== first.copy.en.title) throw Error('theme lost position');
      sourcesButton.click();
      const sources = sourcesDialog.open && sourcesList.querySelectorAll('a').length === data.sources.length && methodNote.textContent === data.methodNote.en;
      sourcesDialog.close();
      const labels = document.querySelectorAll('.source-label').length;
      const pointer = (id, x, y, x2, y2) => {
        story.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, pointerId: id, pointerType: 'touch', clientX: x, clientY: y }));
        story.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, pointerId: id, pointerType: 'touch', clientX: x2, clientY: y2 }));
      };
      pointer(81, 180, 250, 180, 370);
      const verticalPreserved = document.querySelector('#story h1').textContent === first.copy.en.title && document.documentElement.dataset.focusMode !== 'true';
      pointer(82, 270, 250, 90, 250);
      const swipeAdvanced = document.querySelector('#story h1').textContent !== first.copy.en.title && document.documentElement.dataset.focusMode !== 'true';
      return { title, sources, labels, narrative: data.contentMode === 'narrative', saved: localStorage.getItem('book-tiktok.' + data.slug + '.lastScreen') === data.screens.filter(s => s.level === 1)[2].id, verticalPreserved, swipeAdvanced, home: libraryButton.getAttribute('href') };
    })()`);
    assert(result.sources && result.saved && result.home === './', `${book}: Sources/progress/Home failed`);
    assert(result.verticalPreserved && result.swipeAdvanced, `${book}: swipe/vertical motion violated reading/focus contract`);
    assert(result.labels === (result.narrative ? 0 : 1), `${book}: narrative footer suppression failed`);
    checks.push({ book, ...result });
  }
  if (phase === 'release-reader-interactions') summary = { checks, sourcesProgressSwipe: 'passed for each accepted reader' };
  else {
  const book = 'amphibian-man.html';
  for (const language of ['ru', 'en']) {
    await navigate(book, "document.querySelector('[data-start]')");
    await evaluate(`localStorage.setItem('book-tiktok.amphibian-man.language', '${language}'); localStorage.setItem('book-tiktok.amphibian-man.mode', 'deep'); localStorage.setItem('book-tiktok.amphibian-man.lastScreen', 'farewell')`);
    await navigate(book, "document.querySelector('[data-start=continue]')");
    assert(await evaluate(`(() => {
      const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
      const late = data.screens.filter(s => s.level === 3);
      const text = document.body.innerText;
      return document.querySelector('[data-mode=essential][aria-pressed=true]') && (document.querySelector('[data-start=continue]').textContent.includes('Deep') || data.slug === 'a-wizard-of-earthsea') && late.every(s => !text.includes(s.copy['${language}'].title));
    })()`), `${language}: saved Deep leaked before consent`);
    consentDecision = false;
    await evaluate("document.querySelector('[data-start=continue]').click()");
    assert(await evaluate("Boolean(document.querySelector('.cover-layout')) && !document.querySelector('#contentsList [data-go-to=farewell]')"), `${language}: cancelled saved Deep still opened ending`);
    consentDecision = true;
    await evaluate("document.querySelector('[data-start=continue]').click()");
    assert(await evaluate(`document.querySelector('#story h1').textContent === JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s => s.id === 'farewell').copy['${language}'].title && document.querySelectorAll('.source-label').length === 0`), `${language}: accepted saved Deep did not resume`);
    await navigate(book, "document.querySelector('[data-start=continue]')");
    assert(await evaluate("!document.querySelector('#contentsList [data-go-to=farewell]')"), `${language}: reload retained ending consent`);
    consentDecision = false;
    await evaluate("document.querySelector('[data-mode=deep]').click()");
    assert(await evaluate("!document.querySelector('#contentsList [data-go-to=farewell]')"), `${language}: cancelled Deep picker exposed ending`);
    consentDecision = true;
    await evaluate("document.querySelector('[data-mode=deep]').click(); document.querySelector('#contentsList [data-go-to=final]').click(); nextButton.click()");
    assert(await evaluate("!localStorage.getItem('book-tiktok.amphibian-man.lastScreen') && Boolean(document.querySelector('[data-start=begin]'))"), `${language}: restart retained saved ending`);
  }
  assert(consentDialogs.length === 8 && consentDialogs.every(d => d.type === 'confirm' && /спойлер|spoiler/i.test(d.message)), 'missing localized native consent dialogs');
  await navigate('?type=fiction&topic=science-fiction&q=Беляев', "document.querySelectorAll('.book').length === 1");
  const newCard = await evaluate(`(() => {
    const card = document.querySelector('[data-book=amphibian-man]');
    return { present: Boolean(card), motif: card?.querySelector('[data-cover-motif]')?.dataset.coverMotif, artwork: Boolean(card?.querySelector('.cover__art svg')), stats: [bookStat.textContent, screenStat.textContent], noAgeShelf: !/14[+]|Сыну|For my son/.test(document.body.innerText) };
  })()`);
  assert(newCard.present && newCard.motif === 'sea-air' && newCard.artwork && newCard.noAgeShelf, 'new narrative card/discovery regression');
  for (const width of [320, 1440]) {
    await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : 900, deviceScaleFactor: 1, mobile: width < 900 });
    const capture = await command('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, `amphibian-card-${width}.png`), Buffer.from(capture.data, 'base64'));
  }
  summary = { checks, savedDeepConsent: consentDialogs, reloadRequiresConsent: true, restartClearsProgress: true, newCard };
  }
}

if (phase === 'release-card') {
  const book = catalogue.books.find(book => book.slug === 'monday-begins-on-saturday');
  const checks = [];
  assert(book.audience === 'general' && book.spoilerPolicy === 'full-plot-in-deep' && book.collections.length === 0, 'Monday discovery metadata');
  for (const width of [320, 390, 1440]) {
    await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : width === 390 ? 844 : 900, deviceScaleFactor: 1, mobile: width < 900 });
    await navigate('?type=fiction&topic=fantasy&q=Стругацкие', "document.querySelectorAll('.book').length === 1");
    const result = await evaluate(`(() => {
      const card = document.querySelector('[data-book=monday-begins-on-saturday]');
      return { title: card.textContent.includes(${JSON.stringify(book.title.ru)}), author: card.textContent.includes(${JSON.stringify(book.author.ru)}),
        motif: card.querySelector('[data-cover-motif]').dataset.coverMotif, artwork: Boolean(card.querySelector('.cover__art svg path.art-bold')),
        stats: [bookStat.textContent, screenStat.textContent], overflow: document.documentElement.scrollWidth > innerWidth + 1,
        noAgeShelf: !/14[+]|Сыну|For my son/.test(document.body.innerText) };
    })()`);
    assert(result.title && result.author && result.motif === 'enchanted-lab' && result.artwork && !result.overflow && result.noAgeShelf, `Monday card ${width}: ${JSON.stringify(result)}`);
    checks.push({ width, ...result });
    const capture = await command('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(outputDir, `monday-card-${width}.png`), Buffer.from(capture.data, 'base64'));
  }
  summary = { checks, controlledDiscovery: 'fiction/fantasy/Strugatsky', uniqueCoverMotif: 'enchanted-lab' };
}

if (phase === 'release-consent') {
  const checks = [];
  const modalDecisions = [];
  async function decide(accept) {
    const modal = await evaluate(`(() => {
      const dialog = document.querySelector('#accelerandoSpoilerDialog[open], #spoilerDialog[open], #endingDialog[open]');
      if (!dialog) return null;
      const selected = dialog.querySelector(${JSON.stringify(accept ? '[data-spoiler-accept], #spoilerAccept, #endingAccept' : '[data-spoiler-cancel], #spoilerCancel, #endingCancel')});
      if (!selected) throw Error('Missing book-local consent control');
      const result = { id: dialog.id, accepted: ${accept}, title: dialog.querySelector('h2').textContent };
      selected.click(); return result;
    })()`);
    if (modal) modalDecisions.push(modal);
    await evaluate('Promise.resolve(true)');
  }
  for (const book of releaseBooks) {
    const expected = JSON.parse(fs.readFileSync(path.join(root, book), 'utf8').match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
    if (expected.spoilerPolicy !== 'full-plot-in-deep') continue;
    const slug = expected.slug;
    const late = expected.screens.find(screen => screen.level === 3);
    for (const language of ['ru', 'en']) {
      await navigate(book, "document.querySelector('[data-start]')");
      await evaluate(`localStorage.setItem('book-tiktok.${slug}.language', '${language}'); localStorage.setItem('book-tiktok.${slug}.mode', 'deep'); localStorage.setItem('book-tiktok.${slug}.lastScreen', '${late.id}')`);
      await navigate(book, "document.querySelector('[data-start=continue]')");
      assert(await evaluate(`(() => {
        const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
        return document.querySelector('[data-mode=essential][aria-pressed=true]') && (document.querySelector('[data-start=continue]').textContent.includes('Deep') || data.slug === 'a-wizard-of-earthsea') &&
          data.screens.filter(s => s.level === 3).every(s => !document.body.innerText.includes(s.copy['${language}'].title));
      })()`), `${book}/${language}: stored Deep exposed late titles or bypassed Essential`);
      consentDecision = false;
      await evaluate("document.querySelector('[data-start=continue]').click()");
      await decide(false);
      assert(await evaluate("Boolean(document.querySelector('.cover-layout')) && !document.querySelector('[data-mode=deep][aria-pressed=true]')"), `${book}/${language}: cancel resumed ending`);
      consentDecision = true;
      await evaluate("document.querySelector('[data-start=continue]').click()");
      await decide(true);
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(late.copy[language].title)}`), `${book}/${language}: accepted resume lost target`);
      await navigate(book, "document.querySelector('[data-start=continue]')");
      assert(await evaluate("Boolean(document.querySelector('[data-mode=essential][aria-pressed=true]'))"), `${book}/${language}: consent survived reload`);
      consentDecision = false;
      await evaluate("document.querySelector('[data-mode=deep]').click()");
      await decide(false);
      assert(await evaluate("!document.querySelector('[data-mode=deep][aria-pressed=true]')"), `${book}/${language}: cancel Deep picker opened ending`);
      consentDecision = true;
      await evaluate("document.querySelector('[data-mode=deep]').click()");
      await decide(true);
      assert(await evaluate("Boolean(document.querySelector('[data-mode=deep][aria-pressed=true]'))"), `${book}/${language}: accepted Deep picker stayed closed`);
      await evaluate("document.querySelector('#contentsList [data-go-to=final]').click()");
      await evaluate("nextButton.click()");
      assert(await evaluate(`!localStorage.getItem('book-tiktok.${slug}.lastScreen') && Boolean(document.querySelector('[data-start=begin]'))`), `${book}/${language}: restart retained ending`);
      checks.push({ book, language, savedDeepHidden: true, cancelledAndAcceptedResume: true, reloadRequiresConsent: true, cancelledAndAcceptedDeepPicker: true, restartClearsProgress: true });
    }
  }
  assert(checks.length > 0, 'No spoiler readers exercised');
  assert(consentDialogs.length + modalDecisions.length === checks.length * 4, 'Consent action did not show the actual native or custom dialog');
  summary = { checks, nativeDialogs: consentDialogs, customDialogs: modalDecisions, physicalIPhone: false };
}

if (phase === 'release-tail') {
  const checks = [];
  consentDecision = true;
  for (const book of releaseBooks) {
    const data = JSON.parse(fs.readFileSync(path.join(root, book), 'utf8').match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
    const longest = data.screens.filter(s=>s.type!=='cover'&&!s.final).sort((a,b)=>b.copy.ru.body.length-a.copy.ru.body.length)[0];
    for (const [language, theme, width] of [['ru','dark',320],['en','light',320],['ru','light',390],['en','dark',1440]]) {
      await command('Emulation.setDeviceMetricsOverride', {width,height:width===320?568:width===390?844:900,deviceScaleFactor:1,mobile:width<900});
      await navigate(book, "document.querySelector('[data-start]')");
      await evaluate(`if(document.documentElement.lang!=='${language}')languageButton.click(); BookSettings.set('theme','${theme}'); document.querySelector('[data-mode=deep]').click(); document.querySelector('#spoilerDialog[open] [data-spoiler-accept], #spoilerDialog[open] #spoilerAccept, #endingDialog[open] #endingAccept')?.click()`);
      await evaluate(`document.querySelector('#contentsList [data-go-to="${longest.id}"]').click()`);
      for (const font of ['sans','serif']) {
        await evaluate(`BookSettings.set('readingFont','${font}'); document.fonts.ready.then(()=>true)`);
        await waitFor(()=>evaluate(`document.documentElement.dataset.readingFont==='${font}'`),'reading font');
        await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
        const result=await evaluate(`(() => {
          const scroll=document.querySelector('.slide-scroll');scroll.scrollTop=scroll.scrollHeight;
          const tail=[...scroll.querySelectorAll('p,li,blockquote')].filter(n=>getComputedStyle(n).display!=='none').at(-1);
          return {overflow:scroll.scrollWidth>scroll.clientWidth+1||document.documentElement.scrollWidth>innerWidth+1,tailReachable:tail.getBoundingClientRect().bottom<=scroll.getBoundingClientRect().bottom+1,sameScreen:document.querySelector('#story h1').textContent===${JSON.stringify(longest.copy[language].title)}};
        })()`);
        assert(!result.overflow&&result.tailReachable&&result.sameScreen,`${book}/${language}/${font}: dense text tail ${JSON.stringify(result)}`);
        checks.push({book,language,font,width,id:longest.id,...result});
      }
      if(width===320){const shot=await command('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(outputDir,book.slice(0,-5)+'-dense-320.png'),Buffer.from(shot.data,'base64'));}
    }
  }
  summary={checks,scope:'Longest actual reading screen in each accepted book, RU/EN320, RU390, EN1440, both fonts; corrected screens have a separate exact-copy phase.'};
}

if (phase === 'release-closures') {
  const release = process.argv.find(arg => arg.startsWith('--release='))?.slice(10) || '03';
  if (!/^\d{2}$/.test(release)) throw new Error('Expected a two-digit editorial release');
  const receipt = JSON.parse(fs.readFileSync(path.join(root, `editorial-audit/2026-10-31/publisher-findings/release-${release}.json`), 'utf8'));
  const checks = [];
  consentDecision = true;
  for (const candidate of receipt.acceptedCandidates.filter(candidate => candidate.checkedScreens && releaseBooks.includes(candidate.slug + '.html'))) {
    const book = candidate.slug + '.html';
    for (const [language, theme, width] of [['ru', 'dark', 320], ['en', 'light', 1440]]) {
      await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : 900, deviceScaleFactor: 1, mobile: width < 900 });
      await navigate(book, "document.querySelector('[data-start]')");
      await evaluate(`if (document.documentElement.lang !== '${language}') languageButton.click(); BookSettings.set('theme', '${theme}'); document.querySelector('[data-mode=deep]').click(); document.querySelector('#accelerandoSpoilerDialog [data-spoiler-accept], #spoilerDialog[open] [data-spoiler-accept], #spoilerDialog[open] #spoilerAccept, #endingDialog[open] #endingAccept')?.click();`);
      await evaluate('Promise.resolve(true)');
      for (const id of candidate.checkedScreens) {
        await evaluate(`document.querySelector('#contentsList [data-go-to="${id}"]').click()`);
        const result = await evaluate(`(() => {
          const data = JSON.parse(document.getElementById('book-tiktok-data').textContent); const screen = data.screens.find(s => s.id === '${id}');
          const expected = document.createElement('template'); expected.innerHTML = screen.copy['${language}'].body;
          const scroll = document.querySelector('.slide-scroll');
          scroll.scrollTop = scroll.scrollHeight;
          const tail = [...scroll.querySelectorAll('p')].filter(node => getComputedStyle(node).display !== 'none').at(-1);
          return { title: document.querySelector('#story h1').textContent === screen.copy['${language}'].title,
            body: scroll.textContent.includes(expected.content.textContent), overflow: scroll.scrollWidth > scroll.clientWidth + 1 || document.documentElement.scrollWidth > innerWidth + 1,
            lastLineReachable: tail && tail.getBoundingClientRect().bottom <= scroll.getBoundingClientRect().bottom + 1,
            sourceMap: screen.sources.length > 0 || screen.id === 'final' || screen.type === 'cover' };
        })()`);
        assert(result.title && result.body && !result.overflow && result.sourceMap && result.lastLineReachable, `${book}/${language}/${id}: changed-copy integration failed: ${JSON.stringify(result)}`);
        checks.push({ book, language, theme, width, id, ...result });
      }
    }
  }
  summary = { checks, changedCopyIntegration: 'exact current title/body displayed', literaryScope: 'Source closure is separately recorded; this phase tests rendered corrected copy.' };
}

if (phase === 'release-migration') {
  const checks = [];
  for (const book of releaseBooks) {
    const slug = book.slice(0, -5);
    await navigate(book, "document.querySelector('[data-start]')");
    for (const removedId of ['cover', 'not-a-current-screen', ...(slug === 'the-hobbit' ? ['a-voice-nearby', 'a-contract'] : [])]) {
      await evaluate(`Object.keys(localStorage).filter(key => key.startsWith('book-tiktok.${slug}.')).forEach(key => localStorage.removeItem(key)); localStorage.setItem('book-tiktok.${slug}.lastScreen','${removedId}'); localStorage.setItem('book-tiktok.${slug}.mode','core'); localStorage.setItem('book-tiktok.${slug}.language','en')`);
      await navigate(book, "document.querySelector('[data-start]')");
      assert(await evaluate(`!localStorage.getItem('book-tiktok.${slug}.lastScreen') && !document.querySelector('[data-start=continue]') && Boolean(document.querySelector('.cover-layout')) && Boolean(document.querySelector('[data-mode=essential][aria-pressed=true]')) && document.documentElement.lang==='en'`), `${book}: invalid/cover saved ID survived: ${removedId}`);
      checks.push({book,removedId,safeEssentialCover:true,languagePreserved:true});
    }
    if (slug === 'the-hobbit') {
      for (const validId of ['a-good-morning','e-gollum']) {
        await evaluate(`localStorage.setItem('book-tiktok.${slug}.lastScreen','${validId}'); localStorage.setItem('book-tiktok.${slug}.mode','deep'); sessionStorage.setItem('book-tiktok.${slug}.spoilerConsent','3')`);
        await navigate(book, "document.querySelector('[data-start=continue]')");
        assert(await evaluate(`!sessionStorage.getItem('book-tiktok.${slug}.spoilerConsent') && Boolean(document.querySelector('[data-mode=essential][aria-pressed=true]'))`), 'Hobbit: old session approval survived');
        await evaluate("document.querySelector('[data-start=continue]').click(); document.querySelector('#spoilerDialog[open] #spoilerAccept')?.click()");
        assert(await evaluate(`document.querySelector('#story h1').textContent===JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s=>s.id==='${validId}').copy.en.title`), 'Hobbit: retained old ID did not resume');
        checks.push({book,validId,resumed:true,staleSessionConsentCleared:true});
      }
    }
  }
  const migrations = [
    { book:'1873.html', old:'book1873', valid:'bimetallism', removed:'thesis', marker:'legacyMigration07' },
    { book:'theory-of-constraints.html', old:'tocbook', valid:'inherent-simplicity', removed:'herbie', marker:'legacyMigration07' },
    { book:'hermes-nous.html', old:'bookHermesNous', valid:'gateway', removed:'console', marker:'legacyMigration06' }
  ].filter(entry => releaseBooks.includes(entry.book));
  for (const m of migrations) for (const language of ['ru','en']) {
    const slug=m.book.slice(0,-5), prefix='book-tiktok.'+slug+'.';
    for (const [oldMode, newMode] of [['short','essential'],['core','core'],['deep','deep'],['full','deep']]) {
      await evaluate(`localStorage.clear(); localStorage.setItem('${m.old}.language','${language}'); localStorage.setItem('${m.old}.theme','light'); localStorage.setItem('${m.old}.mode','${oldMode}'); localStorage.setItem('${m.old}.lastSlide','${m.valid}')`);
      await navigate(m.book, "document.querySelector('[data-start=continue]')");
      assert(await evaluate(`document.documentElement.lang==='${language}' && document.documentElement.dataset.theme==='light' && localStorage.getItem('${prefix}lastScreen')==='${m.valid}' && localStorage.getItem('${prefix}${m.marker}')==='done' && localStorage.getItem('${prefix}mode')==='${newMode}'`), `${m.book}/${language}/${oldMode}: migration`);
      await evaluate("document.querySelector('[data-start=continue]').click()");
      assert(await evaluate(`document.querySelector('#story h1').textContent===JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s=>s.id==='${m.valid}').copy['${language}'].title`), `${m.book}: valid ID resumption`);
      await evaluate("document.querySelector('#contentsList [data-go-to=final]').click(); nextButton.click()");
      await navigate(m.book, "document.querySelector('[data-start=begin]')");
      assert(await evaluate(`!localStorage.getItem('${prefix}lastScreen') && !document.querySelector('[data-start=continue]') && localStorage.getItem('${m.old}.lastSlide')==='${m.valid}'`), `${m.book}: restart resurrected old progress`);
      checks.push({book:m.book,language,oldMode,newMode,valid:m.valid,restartSafe:true,legacyKeysPreserved:true});
    }
    for(const oldId of [m.removed,'cover']) {
      await evaluate(`localStorage.clear(); localStorage.setItem('${m.old}.language','${language}'); localStorage.setItem('${m.old}.mode','deep'); localStorage.setItem('${m.old}.lastSlide','${oldId}')`);
      await navigate(m.book, "document.querySelector('[data-start=begin]')");
      assert(await evaluate(`Boolean(document.querySelector('[data-mode=essential][aria-pressed=true]')) && !localStorage.getItem('${prefix}lastScreen') && !document.querySelector('[data-start=continue]')`), `${m.book}: removed/cover legacy ID`);
      checks.push({book:m.book,language,oldId,safeEssentialCover:true});
    }
    await evaluate(`localStorage.clear(); localStorage.setItem('${m.old}.language','ru'); localStorage.setItem('${m.old}.theme','light'); localStorage.setItem('${m.old}.lastSlide','${m.valid}'); localStorage.setItem('${prefix}language','en'); localStorage.setItem('${prefix}theme','dark'); localStorage.setItem('${prefix}lastScreen','final')`);
    await navigate(m.book, "document.querySelector('[data-start=continue]')");
    assert(await evaluate(`document.documentElement.lang==='en' && document.documentElement.dataset.theme==='dark' && localStorage.getItem('${prefix}lastScreen')==='final'`), `${m.book}: modern values must win`);
  }
  summary = {checks,physicalIPhone:false};
}

if (phase === 'release-state') {
  const checks = [];
  for (const book of releaseBooks) {
    const slug = book.slice(0, -5);
    for (const language of ['ru', 'en']) {
      await navigate(book, "document.querySelector('[data-start]')");
      await evaluate(`Object.keys(localStorage).filter(key => key.startsWith('book-tiktok.${slug}.')).forEach(key => localStorage.removeItem(key)); localStorage.setItem('book-tiktok.${slug}.language', '${language}')`);
      await navigate(book, "document.querySelector('[data-start]')");
      assert(await evaluate("Boolean(document.querySelector('[data-mode=essential][aria-pressed=true]')) && Boolean(document.querySelector('.cover-layout'))"), `${book}/${language}: fresh reader is not Essential/cover`);
      const stable = await evaluate(`(() => { const data = JSON.parse(document.getElementById('book-tiktok-data').textContent); const screen = data.screens.find(s => s.level === 2); localStorage.setItem('book-tiktok.${slug}.lastScreen', screen.id); return { id: screen.id, title: screen.copy['${language}'].title }; })()`);
      await navigate(book, "document.querySelector('[data-start=continue]')");
      await evaluate("document.querySelector('[data-start=continue]').click(); document.querySelector('#spoilerDialog[open] [data-spoiler-accept], #spoilerDialog[open] #spoilerAccept, #endingDialog[open] #endingAccept')?.click()");
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(stable.title)}`), `${book}/${language}: Core stable saved ID was not restored`);
      await evaluate("sourcesButton.click()");
      assert(await evaluate(`sourcesDialog.open && methodNote.textContent === JSON.parse(document.getElementById('book-tiktok-data').textContent).methodNote['${language}']`), `${book}/${language}: source scope changed`);
      await evaluate("sourcesDialog.close(); document.querySelector('#contentsList [data-go-to=final]').click(); nextButton.click()");
      assert(await evaluate(`!localStorage.getItem('book-tiktok.${slug}.lastScreen') && Boolean(document.querySelector('[data-start=begin]'))`), `${book}/${language}: final restart retained saved progress`);
      const custom = await evaluate("Boolean(document.querySelector('#spoilerDialog, #endingDialog'))");
      if (custom) {
        await evaluate("document.querySelector('[data-mode=deep]').click()");
        assert(await evaluate(`Boolean(document.querySelector('#spoilerDialog[open], #endingDialog[open]'))`), `${book}/${language}: custom consent missing`);
        await command('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
        await command('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
        assert(await evaluate("!Boolean(document.querySelector('#spoilerDialog[open], #endingDialog[open]')) && !document.querySelector('[data-mode=deep][aria-pressed=true]') && Boolean(document.querySelector('.cover-layout'))"), `${book}/${language}: Escape opened an ending`);
        await evaluate("document.querySelector('[data-mode=deep]').click(); document.querySelector('#spoilerDialog[open] [data-spoiler-accept], #spoilerDialog[open] #spoilerAccept, #endingDialog[open] #endingAccept').click(); document.querySelector('[data-mode=core]').click(); document.querySelector('[data-mode=deep]').click()");
        if (book === 'a-wizard-of-earthsea.html') {
          // Preserve its existing document-local depth consent; reload still revokes it.
          assert(await evaluate("Boolean(document.querySelector('[data-mode=deep][aria-pressed=true]'))"), 'Earthsea existing session consent');
        } else {
          assert(await evaluate("Boolean(document.querySelector('#spoilerDialog[open], #endingDialog[open]')) && !document.querySelector('[data-mode=deep][aria-pressed=true]')"), `${book}/${language}: lowering depth retained consent`);
          await evaluate("document.querySelector('#spoilerDialog[open] [data-spoiler-cancel], #spoilerDialog[open] #spoilerCancel, #endingDialog[open] #endingCancel').click()");
        }
      }
      checks.push({ book, language, freshEssential: true, savedCoreId: stable.id, finalRestart: true, sourceScope: true, customEscapeAndDowngrade: custom ? (book === 'a-wizard-of-earthsea.html' ? 'Escape passed; existing same-document depth consent preserved; reload separately verified' : 'passed') : 'not applicable' });
    }
  }
  summary = { checks, physicalIPhone: false };
}

if (phase === 'release-cards') {
  const checks = [];
  for (const width of [320, 1440]) {
    await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : 900, deviceScaleFactor: 1, mobile: width < 900 });
    await navigate('', `document.querySelectorAll('.book').length === ${expectedBookCount}`);
    for (const language of ['ru', 'en']) {
      await evaluate(`if (document.documentElement.lang !== '${language}') languageButton.click()`);
      for (const book of releaseBooks) {
        const expected = catalogue.books.find(item => item.file === book);
        const result = await evaluate(`(() => { const card = document.querySelector('[data-book="${expected.slug}"]'); return { title: card.textContent.includes(${JSON.stringify(expected.title[language])}), author: card.textContent.includes(${JSON.stringify(expected.author[language])}), description: card.textContent.includes(${JSON.stringify(expected.description[language])}), motif: card.querySelector('[data-cover-motif]').dataset.coverMotif, artwork: card.querySelectorAll('.cover__art svg path').length, href: card.getAttribute('href') || card.querySelector('a')?.getAttribute('href'), overflow: card.scrollWidth > card.clientWidth + 1 }; })()`);
        assert(result.title && result.author && result.description && result.motif === expected.cover.motif && result.artwork > 0 && !result.overflow && result.href === './' + book, `${book}/${language}/${width}: card integration failed: ${JSON.stringify(result)}`);
        checks.push({ book, language, width, ...result });
      }
    }
    const capture = await command('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
    fs.writeFileSync(path.join(outputDir, `release-cards-${width}.png`), Buffer.from(capture.data, 'base64'));
  }
  summary = { checks, catalogueBooks: expectedBookCount, catalogueScreens: catalogue.books.reduce((n, book) => n + book.screenCount, 0) };
}

if (phase === 'release-quotations') {
  await command('Emulation.setDeviceMetricsOverride', { width: 320, height: 568, deviceScaleFactor: 1, mobile: true });
  await navigate('meditations.html', "document.querySelector('[data-start]')");
  const checks = await evaluate(`(async () => {
    const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
    const style = document.createElement('style'); style.textContent = '.story-slide { animation: none !important; }'; document.head.append(style);
    await document.fonts.ready;
    const results = [];
    for (const language of ['ru', 'en']) {
      if (document.documentElement.lang !== language) languageButton.click();
      document.querySelector('#contentsList [data-go-to=cover]').click();
      const cover = document.querySelector('#story img');
      if (!cover || !cover.complete || !cover.naturalWidth || !cover.src.startsWith('data:image/png;base64,')) throw Error('Archival cover is not embedded/decoded');
      for (const theme of ['dark', 'light']) {
        if (document.documentElement.dataset.theme !== theme) themeButton.click();
        document.querySelector('[data-mode=deep]').click();
        for (const screen of data.screens.filter(screen => screen.quotation)) {
          document.querySelector('#contentsList [data-go-to="' + screen.id + '"]').click();
          const scroll = document.querySelector('.slide-scroll');
          const quote = screen.quotation;
          if (!scroll.textContent.includes(quote.text[language]) || !scroll.textContent.includes(quote.translators[language]) || !scroll.textContent.includes(quote.locator)) throw Error(screen.id + ': quotation/translator/location changed');
          scroll.scrollTop = scroll.scrollHeight;
          const tail = [...scroll.querySelectorAll(':scope > p')].filter(node => getComputedStyle(node).display !== 'none').at(-1);
          if (tail.getBoundingClientRect().bottom > scroll.getBoundingClientRect().bottom + 1) throw Error(screen.id + ': quotation tail unreachable');
          if (screen.id === 'final' && !scroll.textContent.includes('XII.35')) throw Error('Rogovin concordance missing');
          results.push({ id: screen.id, language, theme, exactQuotation: true, translatorAndLocator: true, lastLineReachable: true });
        }
      }
    }
    style.remove(); return results;
  })()`);
  assert(checks.length === 56, 'All14 quotation pairs in both themes must be rendered');
  summary = { checks, archivalCoverEmbedded: true, scope: 'Rendered fidelity to independently accepted quotation objects; no new primary translation audit.' };
}

if (phase === 'offline') {
  const offlineBooks = [];
  // A real hosted origin can exercise its worker. Local fixtures make no SW claim.
  if (requestedOrigin) {
  await navigate('', `document.querySelectorAll('.book').length === ${expectedBookCount}`);
  await evaluate('navigator.serviceWorker.ready.then(() => true)');
  await waitFor(() => evaluate('Boolean(navigator.serviceWorker.controller)'), 'service worker control');
  for (const book of releaseBooks) {
    await navigate(book, "document.querySelector('[data-start]')");
    await waitFor(() => evaluate(`caches.open('book-tiktok-library-v3-live-catalogue').then(cache => cache.match(new URL('${book}', location.href)).then(Boolean))`), `cached ${book}`);
  }
  await command('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  await navigate('', `document.querySelectorAll('.book').length === ${expectedBookCount}`);
  for (const book of releaseBooks) {
    await navigate(book, "document.querySelector('[data-start]')");
    const data = await evaluate("JSON.parse(document.getElementById('book-tiktok-data').textContent)");
    assert(data.slug + '.html' === book, `${book}: offline navigation fell back to homepage`);
    await evaluate("document.querySelector('[data-start=begin], [data-start]').click(); sourcesButton.click()");
    assert(await evaluate("sourcesDialog.open && sourcesList.textContent.trim().length > 0 && document.fonts.check('16px Geist')"), `${book}: offline Sources/font failed`);
    offlineBooks.push(book);
  }
  }
  await command('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  // Portable HTML also works without an HTTP origin or a service worker.
  testingFileStandalone = true;
  for (const book of releaseBooks) {
    await command('Page.navigate', { url: 'file://' + path.join(root, book) });
    await waitFor(() => evaluate("location.protocol === 'file:' && document.querySelector('[data-start]')"), `standalone ${book}`);
    assert(await evaluate("document.images.length === 0 || [...document.images].every(image => image.complete && image.naturalWidth > 0)"), `${book}: embedded image failed offline`);
  }
  summary = { catalogue: expectedBookCount, pwaOffline: requestedOrigin ? offlineBooks : 'not-exercised-with-local-fixtures', fileStandaloneOffline: releaseBooks, standaloneManifestDiagnostics,
    limitation: 'Chrome blocks optional PWA manifest loading under file://; embedded reading remains usable. No physical iPhone/PWA claim.' };
}

if (phase === 'safe-area') {
  await command('Network.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1' });
  await command('Page.addScriptToEvaluateOnNewDocument', { source: "Object.defineProperty(navigator, 'standalone', { configurable: true, get: () => true });" });
  // Override the engine's environment insets, rather than just changing header
  // padding: this exercises the production env() path in normal and focus modes.
  await command('Emulation.setSafeAreaInsetsOverride', { insets: { top: 59, bottom: 34, left: 0, right: 0 } });
  const checks = [];
  for (const width of [320, 390]) {
    await command('Emulation.setDeviceMetricsOverride', { width, height: width === 320 ? 568 : 844, deviceScaleFactor: 1, mobile: true });
    for (const book of books) {
      await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
      await evaluate(`document.documentElement.removeAttribute('data-focus-mode'); document.querySelector('[data-start], [data-action="start"]')?.click()`);
      const geometry = () => evaluate(`(() => {
        const nodes = [...document.querySelectorAll('.topbar a, .topbar button')].filter(n => n.getBoundingClientRect().height > 0);
        const boxes = nodes.map(n => n.getBoundingClientRect());
        const next = document.querySelector('#nextButton, #btn-next').getBoundingClientRect();
        const header = document.querySelector('.app-header, header.topbar').getBoundingClientRect();
        return {
          top: Math.min(...boxes.map(r => r.top)),
          oneRow: Math.max(...boxes.map(r => r.top)) - Math.min(...boxes.map(r => r.top)) <= 1,
          reachable: nodes.every(n => { const r = n.getBoundingClientRect(); const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2); return r.left >= 0 && r.right <= innerWidth + 1 && hit && n.contains(hit); }),
          iconsOnly: nodes.every(n => !n.textContent.trim() && n.querySelector('svg[data-reader-icon]') && n.getAttribute('aria-label')),
          nextBottom: next.bottom, headerTop: header.top, scrollY,
          installHidden: getComputedStyle(document.getElementById('bookLibraryInstallTrigger')).display === 'none',
          focus: document.documentElement.dataset.focusMode === 'true',
          previousHidden: getComputedStyle(document.querySelector('#previousButton, #btn-back')).display === 'none',
          counterHidden: getComputedStyle(document.querySelector('#counter, .nav-position, .counter')).display === 'none'
        };
      })()`);
      const normal = await geometry();
      assert(normal.top >= 59 && normal.oneRow && normal.reachable && normal.iconsOnly, `${book}/${width}: icon row is under status area, split or unreachable: ${JSON.stringify(normal)}`);
      assert(normal.installHidden && normal.nextBottom <= (width === 320 ? 568 : 844) - 34 + 1, `${book}/${width}: standalone/safe bottom geometry failed`);
      await evaluate(`document.querySelectorAll('.slide-scroll, .scroll').forEach(n => n.scrollTop = n.scrollHeight); window.scrollTo(0, 9999)`);
      const scrolled = await geometry();
      assert(scrolled.top === normal.top && scrolled.reachable && scrolled.headerTop === normal.headerTop, `${book}/${width}: reading scroll displaced header`);
      await evaluate(`document.documentElement.setAttribute('data-focus-mode', 'true')`);
      const focus = await geometry();
      assert(focus.previousHidden && focus.counterHidden && focus.nextBottom <= (width === 320 ? 568 : 844) - 34 + 1, `${book}/${width}: focus geometry failed`);
      await evaluate(`document.documentElement.removeAttribute('data-focus-mode')`);
      const restored = await geometry();
      assert(restored.top === normal.top && restored.reachable, `${book}/${width}: focus exit lost header`);
      checks.push({ book, width, normal, scrolled, restored, focus });
      if (book === 'the-lost-world.html') {
        const capture = await command('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(outputDir, `safe-area-${width}.png`), Buffer.from(capture.data, 'base64'));
      }
    }
  }
  summary = { readers: books.length, safeArea: 'engine env() override top=59 bottom=34', checks, physicalIPhone: false };
}

assert(runtimeErrors.length === 0, `browser errors: ${runtimeErrors.join(' | ')}`);
const report = { phase, origin: requestedOrigin || 'owned-local-CDP-fixtures', ...summary, runtimeErrors: runtimeErrors.length };
fs.writeFileSync(path.join(outputDir, `${phase}.json`), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ phase, books: books.length, runtimeErrors: runtimeErrors.length, report: path.join(outputDir, `${phase}.json`) }));

cleanup();
process.exit(0);
