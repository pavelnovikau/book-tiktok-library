import { spawn } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const chromeBinary = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const catalogue = JSON.parse(fs.readFileSync(path.join(root, 'books.json'), 'utf8'));
const expectedBookCount = catalogue.books.length;
const expectedShelfCount = new Set(catalogue.books.map(book => book.section)).size;
const books = catalogue.books.map(book => book.file);
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'book-tiktok-chrome-'));
let server;
let chrome;
let socket;

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
  if (socket && socket.readyState <= 1) socket.close();
  if (chrome && chrome.pid) {
    try { process.kill(-chrome.pid, 'SIGTERM'); } catch (_) {}
  }
  if (server && server.pid) {
    try { server.kill('SIGTERM'); } catch (_) {}
  }
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch (_) {}
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

function command(method, params = {}) {
  const id = ++commandId;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(expression) {
  const result = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'Evaluation failed');
  return result.result?.value;
}

async function navigate(pathname, condition) {
  await command('Page.navigate', { url: `http://127.0.0.1:${httpPort}/${pathname}` });
  await waitFor(async () => evaluate(`document.readyState === 'complete' && (${condition})`), `load ${pathname}`);
}

function assert(value, message) {
  if (!value) throw new Error(message);
}

await command('Page.enable');
await command('Runtime.enable');
await command('Log.enable');
await command('Network.enable');
await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });

await navigate('', `document.querySelectorAll('.book').length === ${expectedBookCount}`);
const indexPhone = await evaluate(`(() => ({
  books: document.querySelectorAll('.book').length,
  shelves: document.querySelectorAll('.shelf').length,
  stats: [bookStat.textContent, screenStat.textContent, sectionStat.textContent],
  overflow: document.documentElement.scrollWidth - innerWidth,
  manifest: document.querySelector('link[rel="manifest"]')?.getAttribute('href'),
  primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim(),
  flexoki: document.querySelector('.flexoki-credit')?.href
}))()`);
assert(indexPhone.books === expectedBookCount, `phone index: expected ${expectedBookCount} books`);
assert(indexPhone.shelves === expectedShelfCount, `phone index: expected ${expectedShelfCount} populated section shelves`);
assert(indexPhone.overflow <= 1, `phone index overflow: ${indexPhone.overflow}px`);
assert(indexPhone.manifest === './manifest.webmanifest', 'phone index: manifest link missing');
assert(indexPhone.primary === '#2f968d', `phone index: unexpected dark action color ${indexPhone.primary}`);
assert(indexPhone.flexoki === 'https://stephango.com/flexoki', 'phone index: official Flexoki credit missing');
await evaluate(`languageButton.click(); themeButton.click();`);
const toggled = await evaluate(`({
  lang: document.documentElement.lang,
  theme: document.documentElement.dataset.theme,
  primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim()
})`);
assert(toggled.lang === 'en' && toggled.theme === 'light' && toggled.primary === '#1c6c66', 'language/theme controls or quiet action color did not update state');
await evaluate(`searchInput.value = 'Theory'; searchInput.dispatchEvent(new Event('input', { bubbles: true }));`);
await waitFor(async () => (await evaluate(`document.querySelectorAll('.book').length`)) === 1, 'catalogue search');
await evaluate(`navigator.serviceWorker.ready.then(() => true)`);

await command('Emulation.setDeviceMetricsOverride', { width: 320, height: 568, deviceScaleFactor: 2, mobile: true });
for (const book of books) {
  await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
  const compact = await evaluate(`(() => {
    const controls = [...document.querySelectorAll('.app-header .topbar a, .app-header .topbar button, .topbar a, .topbar button')]
      .filter(node => getComputedStyle(node).display !== 'none');
    return {
      controls: controls.length,
      inside: controls.every(node => { const rect = node.getBoundingClientRect(); return rect.left >= -1 && rect.right <= innerWidth + 1; }),
      overflow: document.documentElement.scrollWidth - innerWidth,
      primary: getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim(),
      onPrimary: getComputedStyle(document.documentElement).getPropertyValue('--color-on-primary').trim()
    };
  })()`);
  assert(compact.inside, `${book}: topbar control escaped the 320px viewport`);
  assert(compact.overflow <= 1, `${book}: 320px overflow: ${compact.overflow}px`);
  assert(compact.primary === '#2f968d' && compact.onPrimary === '#100f0f', `${book}: quiet dark action colors were not applied`);
}

await command('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
for (const book of books) {
  await navigate(book, "document.getElementById('story') && document.getElementById('story').children.length > 0");
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

assert(runtimeErrors.length === 0, `browser errors: ${runtimeErrors.join(' | ')}`);
console.log(JSON.stringify({
  index: indexPhone,
  readers: books.length,
  phone: '320x568 and 390x844',
  desktop: '1440x900',
  focusMode: 'passed',
  iosInstallGuide: 'browser and standalone modes passed',
  runtimeErrors: runtimeErrors.length
}, null, 2));

cleanup();
process.exit(0);
