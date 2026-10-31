// No content server: CDP fulfills same-origin fixture requests from this checkout.
// Every phase owns a mkdtemp profile and a timeout-30 Chrome process tree.
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const requestedBooks = process.argv.find(a=>a.startsWith('--books='))?.slice(8).split(',');
const qaBooks = requestedBooks ? requestedBooks.map(file=>{const b=catalogue.books.find(b=>b.file===file);if(!b)throw Error('Unregistered QA reader '+file);return b;}) : catalogue.books;
const phases = [...Array.from({ length: Math.ceil(qaBooks.length / 4) }, (_, n) => `layout-${n}`), 'persistence', 'migration', 'review-regressions', 'consent', 'hitchhiker', 'mobile', ...Array.from({ length: Math.ceil(qaBooks.length / 8) }, (_, n) => `offline-${n}`)];
const phase = process.argv.find(a => a.startsWith('--phase='))?.slice(8);
const requestedOrigin = process.argv.find(a => a.startsWith('--origin='))?.slice(9);
const output = process.env.BOOK_SETTINGS_QA_DIR || fs.mkdtempSync(path.join(os.tmpdir(), 'book-settings-qa-'));
if (path.resolve(output).startsWith(root + path.sep)) throw Error('Keep QA artifacts outside the repository');
fs.mkdirSync(output, { recursive: true });
if (!phase) {
  for (const next of phases) {
    const run = spawnSync(process.execPath, [fileURLToPath(import.meta.url), `--phase=${next}`, ...process.argv.filter(a => a.startsWith('--origin=') || a.startsWith('--books='))], { cwd: root, encoding: 'utf8', timeout: 40000, env: { ...process.env, BOOK_SETTINGS_QA_DIR: output } });
    process.stdout.write(run.stdout || ''); process.stderr.write(run.stderr || '');
    if (run.status !== 0) process.exit(run.status || 1);
  }
  console.log(`Settings QA passed. Reports and screenshots: ${output}`);
  process.exit(0);
}
if (!phases.includes(phase)) throw Error(`Unknown phase ${phase}`);
const origin = requestedOrigin || 'https://book-library.test';
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'book-settings-chrome-'));
const binary = process.env.CHROME_BINARY || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let chrome, socket, cleaned = false, id = 0, consentDecision = false;
const pending = new Map(), errors = [], remoteRequests = [], nativeDialogs = [];
const report = { phase, origin: requestedOrigin || 'owned-local-CDP-fixtures', checks: [], fonts: [] };
const assert = (condition, label) => { if (!condition) throw Error(label); };
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function until(fn, label) {
  const end = Date.now() + 6000;
  while (Date.now() < end) { if (await fn()) return; await delay(35); }
  throw Error(`Timed out: ${label}`);
}
function cleanup() {
  if (cleaned) return; cleaned = true;
  if (socket?.readyState <= 1) socket.close();
  if (chrome?.pid) {
    // Collect owned descendants before terminating their parent, then the group.
    const rows = spawnSync('ps', ['-axo', 'pid=,ppid='], { encoding: 'utf8' }).stdout.trim().split('\n').map(l => l.trim().split(/\s+/).map(Number));
    const owned = new Set([chrome.pid]);
    for (let pass = 0; pass < 12; pass++) for (const [pid, ppid] of rows) if (owned.has(ppid)) owned.add(pid);
    try { process.kill(-chrome.pid, 'SIGKILL'); } catch (_) {}
    for (const pid of [...owned].reverse()) { try { process.kill(pid, 'SIGKILL'); } catch (_) {} }
  }
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 80 });
}
process.on('exit', cleanup);
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => { cleanup(); process.exit(1); });
function command(method, params = {}) {
  const next = ++id;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(next); reject(Error(`${method} timed out`)); }, 6000);
    pending.set(next, { resolve: result => { clearTimeout(timer); resolve(result); }, reject: error => { clearTimeout(timer); reject(error); } });
    socket.send(JSON.stringify({ id: next, method, params }));
  });
}
async function evaluate(expression) {
  const r = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result?.value;
}
async function navigate(file = '', fileScheme = false) {
  await evaluate('window.__settingsLeaving = true');
  await command('Page.navigate', { url: fileScheme ? `file://${path.join(root, file)}` : `${origin}/${file}` });
  await until(() => evaluate("!window.__settingsLeaving && document.readyState === 'complete' && Boolean(window.BookSettings?.open) && (document.getElementById('story')?.children.length > 0 || document.querySelectorAll('.book').length > 0)"), `load ${file}`);
  await evaluate('document.fonts.ready.then(() => true)');
}
async function width(w) { await command('Emulation.setDeviceMetricsOverride', { width: w, height: w === 320 ? 568 : w < 900 ? 844 : 900, deviceScaleFactor: 1, mobile: w < 900 }); }
async function screenshot(name) { const r = await command('Page.captureScreenshot', { format: 'png' }); fs.writeFileSync(path.join(output, `${name}.png`), Buffer.from(r.data, 'base64')); }
async function press(key, code, vk) {
  await command('Input.dispatchKeyEvent', { type: 'keyDown', key, code, windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk, ...(key === 'Enter' ? { text: '\r', unmodifiedText: '\r' } : {}) });
  await command('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk });
}
async function renderedFonts(selector) {
  const doc = await command('DOM.getDocument');
  const { nodeId } = await command('DOM.querySelector', { nodeId: doc.root.nodeId, selector });
  assert(nodeId, `Missing font specimen ${selector}`);
  const { fonts } = await command('CSS.getPlatformFontsForNode', { nodeId });
  return fonts;
}
const start = "(document.querySelector('[data-start=continue], [data-action=resume]') || document.querySelector('[data-start], [data-action=start]'))?.click()";
const language = "document.querySelector('#languageButton, #btn-lang')";
const theme = "document.querySelector('#themeButton, #btn-theme')";
try {
  chrome = spawn('/usr/bin/timeout', ['--foreground', '30', binary, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`, '--remote-debugging-port=0', 'about:blank'], { stdio: 'ignore', detached: true });
  const portFile = path.join(profile, 'DevToolsActivePort');
  await until(() => fs.existsSync(portFile) && /^[1-9]\d*\n/.test(fs.readFileSync(portFile, 'utf8')), 'Chrome startup');
  const port = fs.readFileSync(portFile, 'utf8').split('\n')[0];
  const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  socket = new WebSocket(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
  socket.addEventListener('message', event => {
    const m = JSON.parse(event.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.reject(Error(m.error.message)) : p.resolve(m.result || {}); }
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
    if (m.method === 'Page.javascriptDialogOpening') {
      nativeDialogs.push({ message: m.params.message, accepted: consentDecision });
      command('Page.handleJavaScriptDialog', { accept: consentDecision }).catch(e => errors.push(e.message));
    }
    if (m.method === 'Fetch.requestPaused') {
      const { requestId, request } = m.params;
      const url = new URL(request.url);
      if (requestedOrigin && url.origin === origin) {
        command('Fetch.continueRequest', { requestId }).catch(e => errors.push(e.message));
        return;
      }
      if (url.origin === origin && url.pathname !== '/sw.js') {
        const filename = decodeURIComponent(url.pathname === '/' ? '/index.html' : url.pathname).slice(1);
        const file = path.resolve(root, filename);
        if (file.startsWith(root + path.sep) && fs.existsSync(file) && fs.statSync(file).isFile()) {
          const mime = file.endsWith('.html') ? 'text/html; charset=utf-8' : file.endsWith('.json') || file.endsWith('.webmanifest') ? 'application/json' : file.endsWith('.png') ? 'image/png' : 'application/octet-stream';
          command('Fetch.fulfillRequest', { requestId, responseCode: 200, responseHeaders: [{ name: 'Content-Type', value: mime }], body: fs.readFileSync(file).toString('base64') }).catch(e => errors.push(e.message));
          return;
        }
      }
      if (url.origin !== origin && /^https?:/.test(url.protocol)) remoteRequests.push(request.url);
      command('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' }).catch(e => errors.push(e.message));
    }
  });
  socket.addEventListener('close', () => { for (const p of pending.values()) p.reject(Error('Owned Chrome closed')); pending.clear(); });
  for (const method of ['Page.enable', 'Runtime.enable', 'DOM.enable', 'CSS.enable', 'Network.enable']) await command(method);
  await command('Fetch.enable', { patterns: [{ urlPattern: 'http*' }] });
  // Fixtures exercise pages, not a service-worker install. Offline file phases
  // exercise portable readers separately; no physical iOS/PWA claim is made.
  await command('Page.addScriptToEvaluateOnNewDocument', { source: "Object.defineProperty(navigator, 'serviceWorker', { value: { register: () => Promise.resolve({}) } });" });
  await width(320);

  if (phase.startsWith('layout-')) {
    const books = qaBooks.slice(Number(phase.slice(7)) * 4, Number(phase.slice(7)) * 4 + 4);
    for (const book of books) {
      await navigate(book.file);
      await evaluate(start);
      for (const w of [320, 390, 900, 1440]) {
        await width(w);
        const result = await evaluate(`(async () => {
          const failures = []; let cases = 0;
          for (const lang of ['ru', 'en']) for (const theme of ['dark', 'light']) for (const font of ['sans', 'serif']) {
            if (document.documentElement.lang !== lang) ${language}.click();
            BookSettings.set('theme', theme); BookSettings.set('readingFont', font);
            await document.fonts.ready; await new Promise(requestAnimationFrame);
            const controls = [...document.querySelectorAll('.topbar a, .topbar button')].filter(n => n.getBoundingClientRect().height > 0);
            const rects = controls.map(n => n.getBoundingClientRect());
            if (rects.some(r => r.left < -1 || r.right > innerWidth + 1 || Math.abs(r.top - rects[0].top) > 1 || r.width > 37 || r.height > 37)) failures.push(lang + '/' + theme + '/' + font + ': header geometry');
            if (controls.some(n => n.textContent.trim() || !n.querySelector('svg') || !n.getAttribute('aria-label') || !n.title)) failures.push('header semantics');
            if (!${theme}.querySelector('[data-reader-icon=settings]')) failures.push('gear');
            if (document.documentElement.scrollWidth > innerWidth + 1) failures.push('horizontal overflow');
            cases++;
          }
          return { cases, failures };
        })()`);
        assert(!result.failures.length, `${book.file}/${w}: ${result.failures}`);
        report.checks.push({ file: book.file, width: w, ...result });
      }
      // Actual text nodes, including Ё/ё, inspected through Chrome's rendered
      // platform-font API, rather than trusting a CSS stack or fonts.check().
      for (const font of ['sans', 'serif']) {
        await evaluate(`BookSettings.set('readingFont', '${font}'); document.getElementById('story').insertAdjacentHTML('beforeend', '<p id="qaRu">Съешь ещё этих мягких французских булок Ёё</p><p id="qaEn">Read the book</p>'); document.fonts.ready.then(() => true)`);
        for (const [selector, expected] of [['#qaRu', font === 'serif' ? 'Source Serif 4' : 'Geist'], ['#qaEn', font === 'serif' ? 'Geist Serif' : 'Geist']]) {
          const fonts = await renderedFonts(selector);
          assert(fonts.some(f => f.isCustomFont && f.familyName === expected && f.glyphCount > 0), `${book.file}/${font}/${selector}: ${JSON.stringify(fonts)}`);
          report.fonts.push({ file: book.file, choice: font, selector, fonts });
        }
        await evaluate("document.getElementById('qaRu').remove(); document.getElementById('qaEn').remove()");
        for (const lang of ['ru', 'en']) {
          await evaluate(`if(document.documentElement.lang!=='${lang}') ${language}.click(); document.fonts.ready.then(()=>true)`);
          await evaluate(`(() => { const p=[...document.querySelectorAll('#story p:not(.kicker):not(.source-label):not(.cover-author)')].find(n=>!n.closest('button,figcaption') && /${lang==='ru'?'[А-Яа-яЁё]{3}':'[A-Za-z]{3}'}/.test(n.textContent)); if(!p) throw Error('No actual reading paragraph'); p.dataset.qaReading='true'; })()`);
          const fonts = await renderedFonts('[data-qa-reading]');
          const expected = font==='sans' ? 'Geist' : lang==='ru' ? 'Source Serif 4' : 'Geist Serif';
          assert(fonts.some(f=>f.isCustomFont && f.familyName===expected && f.glyphCount>0), `${book.file}/${font}/${lang}: actual text font ${JSON.stringify(fonts)}`);
          report.fonts.push({file:book.file,choice:font,language:lang,actualReadingText:true,fonts});
          await evaluate("document.querySelector('[data-qa-reading]').removeAttribute('data-qa-reading')");
        }

      }
    }
  }

  if (phase === 'review-regressions') {
    await navigate('essentialism.html');
    const coldFaces = await evaluate("[...document.fonts].filter(f => /Serif/.test(f.family)).map(f => ({family:f.family,status:f.status}))");
    assert(coldFaces.length === 2 && coldFaces.every(f => f.status === 'unloaded'), 'R2 requires unused, undecoded Serif faces');
    await evaluate(start);
    await evaluate("document.getElementById('contentsButton').click(); document.querySelector('#contentsList [data-go-to=\"three-part-cycle\"]').click()");
    const before = await evaluate(`(() => {
      const scroller = document.querySelector('.slide-scroll');
      window.__reviewScroller = scroller; window.__reviewSlide = document.querySelector('.story-slide');
      scroller.scrollTop = 40;
      return {top:scroller.scrollTop,max:scroller.scrollHeight-scroller.clientHeight,paragraphTop:scroller.querySelector('p').getBoundingClientRect().top};
    })()`);
    assert(before.top === 40 && before.max >= 40, 'R2 requires a genuinely scrolled reading screen');
    await evaluate("document.querySelector('#themeButton').click(); document.querySelector('input[name=book-font][value=serif]').click()");
    await until(() => evaluate("document.documentElement.dataset.readingFont==='serif' && document.fonts.status==='loaded'"), 'cold Serif layout');
    await evaluate('new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve(true))))');
    const after = await evaluate(`(() => {
      const scroller = document.querySelector('.slide-scroll');
      return {top:scroller.scrollTop,max:scroller.scrollHeight-scroller.clientHeight,paragraphTop:scroller.querySelector('p').getBoundingClientRect().top,sameScroller:scroller===window.__reviewScroller,sameSlide:document.querySelector('.story-slide')===window.__reviewSlide};
    })()`);
    assert(after.sameScroller && after.sameSlide, 'R2 keeps the active slide and scroller');
    assert(Math.abs(after.top - before.top) < 1, `R2 scroll moved ${before.top} -> ${after.top}`);
    assert(Math.abs(after.paragraphTop - before.paragraphTop) < 1, 'R2 preserves the paragraph viewport position');
    report.checks.push({case:'cold Serif with nonzero scroll',coldFaces,before,after});
    await press('Escape', 'Escape', 27);
    assert(await evaluate("BookSettings.set('readingFont','sans'); document.documentElement.dataset.readingFont==='sans'"), 'Cached Sans applies synchronously');
    assert(await evaluate("BookSettings.set('readingFont','serif'); document.documentElement.dataset.readingFont==='serif'"), 'Cached Serif applies synchronously');

    for (const reviewedBook of ['1873.html','theory-of-constraints.html','hermes-nous.html']) {
      await navigate(reviewedBook);
      await evaluate(start);
      await press('ArrowRight', 'ArrowRight', 39);
      for (const lang of ['ru', 'en']) {
        if (await evaluate(`document.documentElement.lang !== '${lang}'`)) await evaluate(`${language}.click()`);
        await evaluate("window.__reviewReaderSlide=document.getElementById('story').firstElementChild; window.__reviewReaderKey=document.getElementById('book-tiktok-data') ? 'book-tiktok.'+JSON.parse(document.getElementById('book-tiktok-data').textContent).slug+'.lastScreen' : 'bookHermesNous.lastSlide'; window.__reviewReaderId=localStorage.getItem(window.__reviewReaderKey); if(!window.__reviewReaderId) throw Error('Reader must have real saved progress')");
        await evaluate(`${theme}.click(); document.querySelector('input[name=book-theme][value=light]').click(); document.querySelector('input[name=book-theme][value=light]').focus()`);
        await press('ArrowRight', 'ArrowRight', 39);
        const result = await evaluate(`({dark:document.querySelector('input[name=book-theme][value=dark]').checked,theme:document.documentElement.dataset.theme,dialogOpen:document.getElementById('bookSettingsDialog').open,sameSlide:window.__reviewReaderSlide===document.getElementById('story').firstElementChild,sameSavedId:window.__reviewReaderId===localStorage.getItem(window.__reviewReaderKey)})`);
        assert(result.dark && result.theme === 'dark' && result.dialogOpen && result.sameSlide && result.sameSavedId, `R1/${lang}: ${JSON.stringify(result)}`);
        report.checks.push({case:'native radio ArrowRight',file:reviewedBook,lang,...result});
        await evaluate("document.querySelector('input[name=book-theme][value=dark]').focus()");
        await press('ArrowLeft', 'ArrowLeft', 37);
        assert(await evaluate("document.querySelector('input[name=book-theme][value=light]').checked && document.documentElement.dataset.theme==='light'"), 'R1 native theme ArrowLeft wrap');
        await evaluate("document.querySelector('input[name=book-font][value=sans]').click(); document.querySelector('input[name=book-font][value=sans]').focus()");
        await press('ArrowLeft', 'ArrowLeft', 37);
        await until(() => evaluate("document.documentElement.dataset.readingFont==='serif'"), 'R1 native font ArrowLeft wrap');
        assert(await evaluate("document.querySelector('input[name=book-font][value=serif]').checked && window.__reviewReaderSlide===document.getElementById('story').firstElementChild && window.__reviewReaderId===localStorage.getItem(window.__reviewReaderKey)"), 'R1 font ArrowLeft changed reading state');
        await press('ArrowRight', 'ArrowRight', 39);
        assert(await evaluate("document.querySelector('input[name=book-font][value=sans]').checked && document.documentElement.dataset.readingFont==='sans' && window.__reviewReaderSlide===document.getElementById('story').firstElementChild && window.__reviewReaderId===localStorage.getItem(window.__reviewReaderKey)"), 'R1 font ArrowRight changed reading state');
        report.checks.push({case:'both radio groups native Left/Right wrap',file:reviewedBook,lang,sameSlide:true,sameSavedId:true});
        await press('Escape', 'Escape', 27);
      }
    }
    await evaluate("BookSettings.set('readingFont','sans'); BookSettings.set('readingFont','serif'); BookSettings.set('readingFont','sans')");
    await until(() => evaluate("document.documentElement.dataset.readingFont==='sans'"), 'latest rapid font choice');
    assert(await evaluate("BookSettings.get().readingFont==='sans' && JSON.parse(localStorage.getItem('bookLibrary.preferences.v1')).readingFont==='sans'"), 'Latest rapid choice matches stored preference');
    report.checks.push({case:'rapid font changes retain the last choice'});
  }

  if (phase === 'persistence') {
    await navigate();
    assert(await evaluate("document.documentElement.lang === 'ru' && BookSettings.get().theme === 'dark' && BookSettings.get().readingFont === 'sans'"), 'new default');
    const homeCheck = await evaluate(`(() => {
      const stats = [...document.querySelectorAll('.stat strong')].map(n => n.textContent);
      ${theme}.focus(); ${theme}.click();
      return { stats, open: bookSettingsDialog.open, heading: document.activeElement.id, theme: document.documentElement.dataset.theme, note: bookSettingsFontNote.textContent };
    })()`);
    assert(homeCheck.open && homeCheck.heading === 'bookSettingsTitle' && homeCheck.theme === 'dark' && homeCheck.note.includes('Source Serif 4'), 'homepage modal/old-toggle suppression');
    await evaluate("document.querySelector('[name=book-theme][value=light]').click(); document.querySelector('[name=book-font][value=serif]').click()");
    await screenshot('home-320-settings-ru-light-serif');
    await press('Escape', 'Escape', 27);
    assert(await evaluate("!bookSettingsDialog.open && document.activeElement.id === 'themeButton'"), 'Escape/focus return');
    const all = await evaluate("({ stats: [bookStat.textContent, screenStat.textContent], tabs: [...document.querySelectorAll('#typeFilter button')].map(n=>n.getBoundingClientRect().width) })");
    assert(Number(all.stats[0].match(/\d+/)[0]) === catalogue.books.length && Number(all.stats[1].match(/\d+/)[0]) === catalogue.books.reduce((n,b)=>n+b.screenCount,0), 'statistics strip');
    assert(Math.max(...all.tabs) - Math.min(...all.tabs) <= 1, 'equal tabs');
    const saved = [];
    for (const book of [catalogue.books.find(b=>b.slug==='essentialism'), catalogue.books.find(b=>b.file==='1873.html'), catalogue.books.find(b=>b.file==='theory-of-constraints.html'), catalogue.books.find(b=>b.file==='hermes-nous.html')]) {
      await navigate(book.file);
      assert(await evaluate("BookSettings.get().theme === 'light' && BookSettings.get().readingFont === 'serif' && document.documentElement.dataset.theme === 'light'"), `${book.file}: global preferences`);
      await evaluate(`${start}; document.querySelector('#nextButton, #btn-next').click()`);
      const before = await evaluate("({title:document.querySelector('#story h1').textContent,storage:{...localStorage},html:story.innerHTML})");
      await evaluate(`${theme}.click(); document.querySelector('[name=book-theme][value=dark]').click(); document.querySelector('[name=book-font][value=sans]').click(); bookSettingsClose.click()`);
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(before.title)} && story.innerHTML === ${JSON.stringify(before.html)}`), `${book.file}: settings rerendered current screen`);
      const unchanged = await evaluate(`Object.entries(${JSON.stringify(before.storage)}).filter(([key])=> /mode|lastScreen|lastSlide|language|focus/i.test(key)).every(([key,value])=>localStorage.getItem(key)===value)`);
      assert(unchanged, `${book.file}: mode/position/language storage changed`);
      saved.push({ file: book.file, title: before.title });
      await evaluate(`${language}.click(); document.querySelector('#nextButton, #btn-next').click()`);
      assert(await evaluate("document.documentElement.dataset.theme==='dark' && document.documentElement.dataset.readingFont==='sans'"), `${book.file}: render reverted theme/font`);
      await evaluate(`document.querySelector('#previousButton, #btn-back').click(); ${language}.click()`);
      await navigate(book.file);
      assert(await evaluate("BookSettings.get().theme === 'dark' && BookSettings.get().readingFont === 'sans'"), `${book.file}: reload theme/font`);
      await evaluate(start);
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(before.title)}`), `${book.file}: reading resume`);
      await evaluate("BookSettings.set('theme','light'); BookSettings.set('readingFont','serif')");
    }
    await navigate();
    assert(await evaluate("BookSettings.get().theme === 'light' && BookSettings.get().readingFont === 'serif'"), 'book B -> home persistence');
    report.checks.push({ homeCheck, all, saved });
    // Native Tab stays trapped; Enter selects/activates without paging.
    await evaluate(`${theme}.focus(); ${theme}.click()`);
    for (let n=0;n<8;n++) {
      await press('Tab', 'Tab', 9);
      assert(await evaluate("bookSettingsDialog.contains(document.activeElement)"), 'native focus trap');
    }
    await press('Escape', 'Escape', 27);
    await evaluate("languageButton.click(); themeButton.click()");
    assert(await evaluate("bookSettingsTitle.textContent === 'Settings' && document.querySelector('input[value=light]').checked && bookSettingsFontNote.textContent.includes('Russian')"), 'EN settings localization/selected states');
    await screenshot('home-320-settings-en-light-serif');
    const uiFonts = await renderedFonts('#bookSettingsFontNote');
    assert(uiFonts.every(f=>f.isCustomFont && f.familyName==='Geist'), 'Settings UI must remain real Sans in Serif mode');
    report.fonts.push({choice:'serif',settingsUI:true,fonts:uiFonts});
    await press('Tab','Tab',9);
    await press('ArrowRight','ArrowRight',39);
    assert(await evaluate("document.querySelector('[name=book-theme][value=dark]').checked && BookSettings.get().theme==='dark'"), 'native radio keyboard selection');
    await press('Escape','Escape',27);
    await until(()=>evaluate("document.activeElement.id==='themeButton' && !bookSettingsDialog.open"), 'Escape returns to gear');
    await press('Enter','Enter',13);
    assert(await evaluate("bookSettingsDialog.open && BookSettings.get().theme==='dark'"), 'Enter opens gear without toggling: '+JSON.stringify(await evaluate("({open:bookSettingsDialog.open, theme:BookSettings.get().theme, active:document.activeElement.id})")));
    await press('Escape','Escape',27);

  }

  if (phase === 'migration') {
    await navigate();
    for (const file of ['essentialism.html','1873.html','theory-of-constraints.html','hermes-nous.html']) {
      const modern = fs.readFileSync(path.join(root,file),'utf8').includes('id="book-tiktok-data"');
      const key = modern ? 'book-tiktok.'+file.slice(0,-5)+'.theme' : ({'1873.html':'book1873.theme','theory-of-constraints.html':'tocbook.theme','hermes-nous.html':'bookHermesNous.theme'})[file];
      await evaluate(`localStorage.clear(); localStorage.setItem('${key}', 'light')`);
      await navigate(file);
      assert(await evaluate("BookSettings.get().theme === 'light' && BookSettings.get().readingFont === 'sans'"), `${file}: migrate local theme`);
      await evaluate(`localStorage.setItem('${key}','dark'); BookSettings.set('readingFont','serif')`);
      await navigate(file);
      assert(await evaluate("document.documentElement.dataset.theme === 'light' && BookSettings.get().readingFont === 'serif'"), `${file}: global wins over stale local theme`);
      report.checks.push({file, migration:'pass', precedence:'pass'});
    }
    await evaluate("localStorage.setItem('bookLibrary.preferences.v1', '{broken')");
    await navigate('hermes-nous.html');
    assert(await evaluate("BookSettings.get().version===1 && BookSettings.get().readingFont==='sans'"), 'invalid global fallback');
    await command('Page.addScriptToEvaluateOnNewDocument', { source: "Storage.prototype.getItem = Storage.prototype.setItem = function () { throw new DOMException('blocked', 'SecurityError'); };" });
    await navigate('1873.html');
    await evaluate("BookSettings.set('theme','light'); BookSettings.set('readingFont','serif'); themeButton.click()");
    assert(await evaluate("bookSettingsDialog.open && document.documentElement.dataset.theme==='light' && document.documentElement.dataset.readingFont==='serif'"), 'storage-disabled session usability');
  }

  if (phase === 'consent' || phase === 'hitchhiker') {
    const books = catalogue.books.filter(b=>b.spoilerPolicy === 'full-plot-in-deep').filter(b=>(b.slug==='the-hitchhikers-guide-to-the-galaxy') === (phase==='hitchhiker'));
    const guarded = books.filter(book => /spoilerDialog|accelerandoSpoilerDialog|(?:window\.)?confirm\s*\(/.test(fs.readFileSync(path.join(root, book.file), 'utf8')));
    report.unchangedLegacyLimits = books.filter(b=>!guarded.includes(b)).map(b=>({file:b.file,limit:'Existing runtime has no explicit saved-Deep consent guard; Settings preserves it without changing reading policy.'}));
    for (const book of guarded) for (const lang of ['ru','en']) {
      await navigate(book.file);
      const data = await evaluate("JSON.parse(document.getElementById('book-tiktok-data').textContent)");
      const late = data.screens.filter(s=>s.level===3 && !s.final).at(-1);
      assert(late, `${book.file}: no late screen`);
      await evaluate(`sessionStorage.removeItem('book-tiktok.${book.slug}.spoilerConsent'); localStorage.setItem('book-tiktok.${book.slug}.mode','deep'); localStorage.setItem('book-tiktok.${book.slug}.lastScreen', ${JSON.stringify(late.id)}); localStorage.setItem('book-tiktok.${book.slug}.language','${lang}')`);
      await navigate(book.file);
      const checkSafe = async () => assert(await evaluate(`Boolean(document.querySelector('.cover-layout')) && !document.body.innerText.includes(${JSON.stringify(late.copy[lang].title)})`), `${book.file}/${lang}: ending visible before consent`);
      await checkSafe();
      await evaluate(`${theme}.click(); document.querySelector('[name=book-font][value=serif]').click(); bookSettingsClose.click()`);
      await checkSafe();
      consentDecision = false;
      await evaluate("document.querySelector('[data-start=continue]').click()");
      const custom = await evaluate("Boolean(document.querySelector('#spoilerDialog[open], #accelerandoSpoilerDialog[open]'))");
      if (custom) await evaluate("document.querySelector('#spoilerDialog[open] #spoilerCancel, #spoilerDialog[open] [data-spoiler-cancel], #accelerandoSpoilerDialog[open] [data-spoiler-cancel]').click()");
      if (phase === 'hitchhiker') assert(custom, 'Hitchhiker custom consent missing');
      await checkSafe();
      consentDecision = true;
      await evaluate("document.querySelector('[data-start=continue]').click()");
      if (custom) await evaluate("document.querySelector('#spoilerDialog[open] #spoilerAccept, #spoilerDialog[open] [data-spoiler-accept], #accelerandoSpoilerDialog[open] [data-spoiler-accept]').click(); new Promise(resolve=>setTimeout(resolve,0))");
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(late.copy[lang].title)}`), `${book.file}/${lang}: accepted Deep resume`);
      await evaluate(`${theme}.click(); document.querySelector('[name=book-theme][value=light]').click(); bookSettingsClose.click()`);
      assert(await evaluate(`document.querySelector('#story h1').textContent === ${JSON.stringify(late.copy[lang].title)}`), 'Settings lost consented screen');
      const sessionConsent = await evaluate(`sessionStorage.getItem('book-tiktok.${book.slug}.spoilerConsent')`);
      await navigate(book.file);
      if (Number(sessionConsent) < 3) await checkSafe();
      report.checks.push({file:book.file,lang,savedDeep:'cancel/accept/reload/settings pass',reloadPolicy: Number(sessionConsent)>=3 ? 'book-local session consent preserved' : 'asks again',lateId:late.id});
    }
    report.nativeDialogs = nativeDialogs;
  }

  if (phase === 'mobile') {
    await command('Network.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1' });
    await command('Emulation.setSafeAreaInsetsOverride', { insets: { top: 59, bottom: 34, left: 0, right: 0 } });
    for (const file of ['', 'essentialism.html', '1873.html', 'theory-of-constraints.html', 'hermes-nous.html']) {
      await navigate(file);
      await delay(500); // Only this short wait observes the existing install timer.
      await evaluate("document.querySelector('dialog[open]')?.close()");
      const install = file ? 'bookLibraryInstallTrigger' : 'installButton';
      await evaluate(`document.getElementById('${install}').click()`);
      const shown = await evaluate(`(() => {
        const d = document.querySelector('dialog[open]'), h = d.querySelector('h2');
        return {scroll:d.scrollTop, headingFocused:document.activeElement===h, headingVisible:h.getBoundingClientRect().top>=d.getBoundingClientRect().top, firstTop:Math.min(...[...document.querySelectorAll('.topbar button,.topbar a')].map(n=>n.getBoundingClientRect()).filter(r=>r.height>0).map(r=>r.top))};
      })()`);
      assert(shown.scroll===0 && shown.headingFocused && shown.headingVisible && shown.firstTop>=59, `${file}: install heading/safe inset ${JSON.stringify(shown)}`);
      await screenshot(`${file || 'home'}-320-ios-install`);
      await press('Escape','Escape',27);
      await evaluate(`${theme}.click()`);
      assert(await evaluate("bookSettingsDialog.getBoundingClientRect().top>=59 && bookSettingsDialog.getBoundingClientRect().bottom<=innerHeight-34"), `${file}: settings safe area`);
      await press('Escape','Escape',27);
      if (file) {
        await evaluate(`${start}; const p=document.querySelector('#story p:not(.kicker)'); p.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:3,pointerType:'touch',clientX:120,clientY:220}));p.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:3,pointerType:'touch',clientX:120,clientY:220}));`);
        assert(await evaluate("document.documentElement.dataset.focusMode==='true' && document.querySelector('#nextButton,#btn-next').getBoundingClientRect().height>0 && document.querySelector('.topbar').getBoundingClientRect().height===0"), `${file}: focus mode`);
        await navigate(file);
        assert(await evaluate("document.documentElement.dataset.focusMode==='true'"), `${file}: focus reload`);
        await press('Escape','Escape',27);
      }
      report.checks.push({file,...shown});
    }
    await command('Page.addScriptToEvaluateOnNewDocument', { source: "Object.defineProperty(navigator, 'standalone', { get:()=>true });" });
    await navigate('essentialism.html');
    assert(await evaluate("bookLibraryInstallTrigger.hidden && document.querySelector('.topbar').getBoundingClientRect().top>=59"), 'standalone install hidden / row inset');
  }

  if (phase.startsWith('offline-')) {
    const n = Number(phase.slice(8));
    await command('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
    for (const book of qaBooks.slice(n*8,n*8+8)) {
      await navigate(book.file, true);
      await evaluate(start);
      for (const font of ['sans','serif']) {
        await evaluate(`BookSettings.set('readingFont','${font}'); BookSettings.set('theme','light'); Promise.all([document.fonts.load('16px Geist'), document.fonts.load('16px \"Geist Serif\"'), document.fonts.load('16px \"Source Serif 4\"'), ...[...document.images].map(i=>i.decode())]).then(()=>true)`);
        assert(await evaluate("document.fonts.check('16px Geist') && document.fonts.check('16px \"Geist Serif\"') && document.fonts.check('16px \"Source Serif 4\"') && [...document.images].every(i=>i.complete && i.naturalWidth>0)"), `${book.file}: standalone fonts/images`);
      }
      await evaluate("document.querySelector('#sourcesButton,#btn-sources').click()");
      assert(await evaluate("Boolean(document.querySelector('dialog[open] a[href]'))"), `${book.file}: offline sources`);
      report.checks.push({file:book.file,offline:true});
    }
  }
  assert(!errors.length, `Runtime errors: ${errors.join('\n')}`);
  assert(!remoteRequests.length, `Remote runtime requests: ${remoteRequests.join(', ')}`);
  report.runtimeErrors = errors; report.remoteRequests = remoteRequests; report.status = 'pass';
  fs.writeFileSync(path.join(output, `${phase}.json`), JSON.stringify(report, null, 2));
  console.log(`${phase}: pass (${report.checks.length} checks, ${report.fonts.length} rendered-font records) ${output}`);
} catch (error) {
  report.status='fail'; report.error=error.stack; report.runtimeErrors=errors;
  fs.writeFileSync(path.join(output, `${phase}.json`), JSON.stringify(report,null,2));
  console.error(error); process.exitCode=1;
} finally { cleanup(); }
