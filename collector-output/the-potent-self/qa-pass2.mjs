import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

// No server, preview tab, HTTP polling or shared Chrome. CDP uses owned pipes.
const root = path.dirname(fileURLToPath(import.meta.url));
const file = path.join(root, 'the-potent-self.html');
const data = JSON.parse(fs.readFileSync(path.join(root, 'story-data.json')));
const html = fs.readFileSync(file, 'utf8');
const embedded = JSON.parse(html.match(/<script id="book-tiktok-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.deepEqual(embedded.screens, data.screens, 'effective HTML corpus differs from authoring JSON');
assert.deepEqual(embedded.sources, data.sources, 'effective source ledger differs');
assert.deepEqual(embedded.targetModes, data.targetModes);
const phase = process.argv[2] || '320';
const widths = { '320': [320, 568], '390': [390, 844], '1024': [1024, 768], '1440': [1440, 900], interactions: [390, 844], ios: [320, 568] };
assert.ok(widths[phase]);
const out = process.env.POTENT_SELF_QA_DIR;
assert.ok(out && !path.resolve(out).startsWith(root), 'screenshots/logs require an external directory');
fs.mkdirSync(out, { recursive: true });
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'potent-self-pass2-chrome-'));
const chrome = spawn('/usr/bin/timeout', ['30', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-background-networking',
  `--user-data-dir=${profile}`, '--remote-debugging-pipe', 'about:blank'],
{ stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe'], detached: true });
let cleaned = false;
function cleanup() {
  if (cleaned) return;
  cleaned = true;
  try { process.kill(-chrome.pid, 'SIGKILL'); } catch {}
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 80 });
}
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });
process.on('SIGTERM', () => { cleanup(); process.exit(143); });
let seq = 0, buffer = '';
const pending = new Map(), events = new Map(), errors = [], network = [];
chrome.stdio[4].on('data', bytes => {
  buffer += bytes.toString();
  for (;;) {
    const n = buffer.indexOf('\0');
    if (n < 0) break;
    const raw = buffer.slice(0, n); buffer = buffer.slice(n + 1);
    if (!raw) continue;
    const m = JSON.parse(raw);
    if (m.id && pending.has(m.id)) {
      const p = pending.get(m.id); pending.delete(m.id); clearTimeout(p.timer);
      if (m.error) p.reject(new Error(JSON.stringify(m.error))); else p.resolve(m.result || {});
    } else if (m.method) {
      if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails);
      if (m.method === 'Network.requestWillBeSent' && /^https?:/.test(m.params.request.url)) network.push(m.params.request.url);
      const p = events.get(`${m.sessionId || ''}:${m.method}`);
      if (p) { events.delete(`${m.sessionId || ''}:${m.method}`); clearTimeout(p.timer); p.resolve(m.params); }
    }
  }
});
chrome.on('exit', code => {
  for (const p of pending.values()) { clearTimeout(p.timer); p.reject(new Error(`Chrome exited ${code}`)); }
  pending.clear();
});
function cmd(method, params = {}, sessionId) {
  const id = ++seq;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`${method} timed out`)); }, 6500);
    pending.set(id, { resolve, reject, timer });
    chrome.stdio[3].write(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }) + '\0');
  });
}
function event(method, sessionId) {
  return new Promise((resolve, reject) => {
    const key = `${sessionId}:${method}`;
    const timer = setTimeout(() => { events.delete(key); reject(new Error(`${method} did not arrive`)); }, 6500);
    events.set(key, { resolve, reject, timer });
  });
}

try {
  const { targetId } = await cmd('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cmd('Target.attachToTarget', { targetId, flatten: true });
  const c = (method, params) => cmd(method, params, sessionId);
  const ev = async expression => {
    const r = await c('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
    return r.result?.value;
  };
  await c('Page.enable'); await c('Runtime.enable'); await c('Network.enable');
  await c('Network.setBlockedURLs', { urls: ['http://*', 'https://*'] });
  await c('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  const [width, height] = widths[phase];
  await c('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 600 });
  if (phase === 'ios') {
    await c('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1' });
  }
  let loaded = event('Page.loadEventFired', sessionId);
  await c('Page.navigate', { url: pathToFileURL(file).href }); await loaded;
  await ev('document.fonts.ready.then(() => Promise.all([...document.images].map(x => x.decode()))).then(() => true)');
  const defaults = await ev(`({lang:document.documentElement.lang, theme:document.documentElement.dataset.theme,
    count:document.getElementById('progressTrack').children.length,
    mode:document.querySelector('.mode-button.is-active').dataset.mode,
    home:document.getElementById('libraryButton').getAttribute('href'),
    font:BookSettings.get().readingFont})`);
  assert.deepEqual(defaults, { lang: 'ru', theme: 'dark', count: data.targetModes.essential, mode: 'essential', home: './', font: 'sans' });
  const report = { phase, viewport: [width, height], defaults, fileOffline: true, corpusEquality: true, screenshots: [], network, errors };
  async function screenshot(name) {
    await ev('document.fonts.ready.then(() => Promise.allSettled(document.getAnimations().map(a => a.finished))).then(() => Promise.all([...document.images].map(x => x.decode())))');
    const { data: png } = await c('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    const dest = path.join(out, `${phase}-${name}.png`); fs.writeFileSync(dest, Buffer.from(png, 'base64')); report.screenshots.push(dest);
  }
  if (phase === 'ios') {
    // Await the existing guide's open event, rather than polling or assuming a timeout passed.
    await ev(`(async()=>{
      if(!bookLibraryInstallDialog.open) await new Promise(resolve=>{
        const observer=new MutationObserver(()=>{if(bookLibraryInstallDialog.open){observer.disconnect();resolve()}});
        observer.observe(bookLibraryInstallDialog,{attributes:true,attributeFilter:['open']});
      }); return true;
    })()`);
    assert.equal(await ev('bookLibraryInstallDialog.open && !bookLibraryInstallTrigger.hidden'), true);
    assert.equal(await ev('bookLibraryInstallDialog.innerText.includes("На экран Домой")'), true);
    await ev('bookLibraryInstallClose.click(); languageButton.click(); bookLibraryInstallTrigger.click()');
    assert.equal(await ev('bookLibraryInstallDialog.innerText.includes("Add to Home Screen")'), true);
    await ev('bookLibraryInstallClose.click();document.documentElement.style.setProperty("--reader-safe-top","47px")');
    const geometry = await ev(`(()=>{const controls=[...document.querySelectorAll('.topbar a,.topbar button')].filter(x=>getComputedStyle(x).display!=='none');const rects=controls.map(x=>x.getBoundingClientRect());return {count:rects.length,row:rects.every(r=>Math.abs(r.top-rects[0].top)<2),inside:rects.every(r=>r.left>=0&&r.right<=320&&r.top>=47)}})()`);
    assert.deepEqual(geometry, { count: 6, row: true, inside: true });
    await screenshot('six-icons-safe-inset');
    await ev('document.querySelector("[data-start]").click()');
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'f', code: 'KeyF' });
    assert.equal(await ev('getComputedStyle(bookLibraryInstallTrigger).display'), 'none');
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape' });
    await c('Page.addScriptToEvaluateOnNewDocument', { source: 'Object.defineProperty(navigator,"standalone",{get:()=>true});' });
    loaded=event('Page.loadEventFired',sessionId); await c('Page.reload'); await loaded;
    assert.equal(await ev('bookLibraryInstallTrigger.hidden && !bookLibraryInstallDialog.open && !document.documentElement.hasAttribute("data-book-installable")'),true);
    report.ios={guide:'RU/EN open and close; existing delayed auto-open observed',safeInset:geometry,focusHidesGuide:true,standaloneHidesGuide:true,scope:'Chrome emulation, not physical Safari'};
  } else if (phase !== 'interactions') {
    await ev(`Promise.all([document.fonts.load('400 16px "Geist Serif"','Aa'),document.fonts.load('400 16px "Source Serif 4"','Ёя')]).then(()=>true)`);
    await screenshot('cover-ru-dark');
    const traversed = await ev(`(() => {
      const data = JSON.parse(document.getElementById('book-tiktok-data').textContent);
      const failures = [], cases = [];
      const check = (value, label) => { if (!value) failures.push(label); };
      const visible = el => el && getComputedStyle(el).display !== 'none' && el.getBoundingClientRect().height > 0;
      for (const font of ['sans','serif']) {
      BookSettings.set('readingFont',font);
      for (const theme of ['dark','light']) {
        BookSettings.set('theme', theme);
        for (const lang of ['ru','en']) {
          if (document.documentElement.lang !== lang) document.getElementById('languageButton').click();
          for (const [mode,level] of [['essential',1],['core',2],['deep',3]]) {
            document.querySelector('[data-mode="'+mode+'"]').click();
            const list = data.screens.filter(x => x.level <= level);
            check(list.length === data.targetModes[mode], mode+' count');
            for (let i=0;i<list.length;i++) {
              const s=list[i], label=font+'/'+theme+'/'+lang+'/'+mode+'/'+s.id;
              document.querySelector('#contentsList [data-go-to="'+s.id+'"]').click();
              check(document.querySelector('#story h1')?.textContent===s.copy[lang].title,label+' title');
              check(document.getElementById('counter').textContent===(i+1)+' / '+list.length,label+' counter');
              check(document.getElementById('progressTrack').children.length===list.length,label+' segments');
              check(document.querySelectorAll('.progress-segment.is-current').length===1,label+' current');
              check(document.querySelector('#contentsList .is-active')?.dataset.goTo===s.id,label+' chapter');
              check(document.documentElement.scrollWidth<=innerWidth+1,label+' document overflow');
              const sc=document.querySelector('#story .slide-scroll'), rect=sc.getBoundingClientRect();
              check(sc.scrollWidth<=sc.clientWidth+1,label+' body overflow');
              sc.scrollTop=sc.scrollHeight;
              if (s.type!=='cover') {
                const ps=[...sc.querySelectorAll(':scope > p:not(.kicker):not(.source-label)')];
                const p=ps.at(-1), text=p?.lastChild;
                if (text?.nodeType===3) {
                  const r=document.createRange(); r.setStart(text,Math.max(0,text.length-1));r.setEnd(text,text.length);
                  const tail=r.getBoundingClientRect();
                  check(tail.bottom<=rect.bottom+2 && tail.top>=rect.top-2,label+' body tail unreachable');
                } else failures.push(label+' no body tail');
                check(sc.innerText.includes(s.copy[lang].body.replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').slice(-25)),label+' body missing');
              }
              const header=document.querySelector('.topbar');
              const controls=[...header.querySelectorAll('button,a')].filter(visible);
              const rs=controls.map(x=>x.getBoundingClientRect());
              check(rs.every(r=>r.left>=-1 && r.right<=innerWidth+1),label+' header clipped');
              check(rs.every(r=>Math.abs(r.top-rs[0].top)<2),label+' header not one row');
              check(controls.every(x=>x.getAttribute('aria-label') && x.title),label+' header labels');
              if (innerWidth>=900) check(visible(document.querySelector('.desktop-rail')),label+' rail absent');
              cases.push(label);
              sc.scrollTop=0;
            }
          }
        }
      }
      }
      return {cases:cases.length, failures, exactCounts:data.targetModes};
    })()`);
    assert.deepEqual(traversed.failures, [], JSON.stringify(traversed.failures.slice(0, 12)));
    report.traversal = traversed;
    await ev(`document.querySelector('#contentsList [data-go-to="head-to-sitting"]').click(); BookSettings.set('theme','dark'); if(document.documentElement.lang!=='ru')languageButton.click()`);
    await screenshot('procedure-ru-dark');
    await ev(`BookSettings.set('theme','light'); languageButton.click()`); await screenshot('procedure-en-light');
    await ev(`document.querySelector('#contentsList [data-go-to="final"]').click()`); await screenshot('final-en-light');
    await ev('nextButton.click()');
    assert.equal(await ev('Boolean(document.querySelector("[data-start]"))'), true, 'final restart did not return cover');
  } else {
    await ev('document.querySelector("[data-start]").click()');
    const first = await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")');
    assert.equal(first, 'capacity-and-use');
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'ArrowRight', code: 'ArrowRight' });
    assert.equal(await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")'), 'divided-action');
    await c('Input.dispatchKeyEvent', { type: 'keyUp', key: 'ArrowRight', code: 'ArrowRight' });
    await ev('sourcesButton.click()');
    assert.equal(await ev('sourcesDialog.open && sourcesList.querySelectorAll("a").length===5 && methodNote.textContent.includes("53–66")'), true);
    await ev('sourcesDialog.close(); themeButton.click()');
    assert.equal(await ev('bookSettingsDialog.open && Boolean(document.querySelector("#themeButton svg"))'), true, 'gear/settings missing');
    await ev('document.querySelector("input[name=book-theme][value=light]").click(); document.querySelector("input[name=book-font][value=serif]").click();bookSettingsClose.click()');
    await ev('document.fonts.ready');
    assert.equal(await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")'), 'divided-action', 'settings moved screen');
    assert.equal(await ev('document.documentElement.dataset.theme'), 'light');
    assert.equal(await ev('BookSettings.get().readingFont'), 'serif');
    assert.equal(await ev('getComputedStyle(document.querySelector("#story p:not(.kicker)")).fontSynthesis'), 'none');
    await c('DOM.enable'); await c('CSS.enable');
    async function platformFonts() {
      const { root: doc } = await c('DOM.getDocument');
      const { nodeId } = await c('DOM.querySelector', { nodeId: doc.nodeId, selector: '#story .slide-scroll > p:not(.kicker):not(.source-label)' });
      return (await c('CSS.getPlatformFontsForNode', { nodeId })).fonts;
    }
    report.serifRU = await platformFonts();
    assert.ok(report.serifRU.some(f => /Source Serif/i.test(f.familyName) && f.isCustomFont));
    await ev('languageButton.click()'); await ev('document.fonts.ready');
    report.serifEN = await platformFonts();
    assert.ok(report.serifEN.some(f => /Geist Serif/i.test(f.familyName) && f.isCustomFont));
    assert.equal(await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")'), 'divided-action', 'language moved screen');
    await ev('BookSettings.set("readingFont","sans")'); await ev('document.fonts.ready');
    report.sansEN = await platformFonts();
    assert.ok(report.sansEN.some(f => /Geist/i.test(f.familyName) && f.isCustomFont));
    await ev('contentsButton.click(); document.querySelector("#dialogModePicker [data-mode=deep]").click(); document.querySelector("#contentsList [data-go-to=transfer-example]").click()');
    assert.equal(await ev('contentsDialog.open'), false);
    assert.equal(await ev('counter.textContent'), `${data.screens.findIndex(s => s.id === 'transfer-example') + 1} / ${data.targetModes.deep}`);
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'f', code: 'KeyF' });
    assert.equal(await ev('document.documentElement.dataset.focusMode'), 'true');
    assert.equal(await ev('getComputedStyle(document.querySelector(".app-header")).display'), 'none');
    await ev('nextButton.click()');
    assert.equal(await ev('document.documentElement.dataset.focusMode'), 'true', 'paging lost focus mode');
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape' });
    assert.equal(await ev('document.documentElement.hasAttribute("data-focus-mode")'), false);
    // Pointer input drives both real listeners; vertical movement must be ignored.
    const point = await ev('(()=>{const r=document.querySelector("#story h1").getBoundingClientRect();return {x:r.x+15,y:r.y+15}})()');
    await c('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 });
    await c('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 });
    assert.equal(await ev('document.documentElement.dataset.focusMode'), 'true', 'tap did not enter focus');
    await c('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape' });
    const before = await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")');
    await ev('(()=>{const s=document.getElementById("story");s.dispatchEvent(new PointerEvent("pointerdown",{bubbles:true,clientX:160,clientY:220}));s.dispatchEvent(new PointerEvent("pointerup",{bubbles:true,clientX:162,clientY:350}));})()');
    assert.equal(await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")'), before);
    assert.equal(await ev('document.documentElement.hasAttribute("data-focus-mode")'), false, 'vertical movement became focus tap');
    await ev('(()=>{const s=document.getElementById("story");s.dispatchEvent(new PointerEvent("pointerdown",{bubbles:true,clientX:300,clientY:300}));s.dispatchEvent(new PointerEvent("pointerup",{bubbles:true,clientX:100,clientY:302}));})()');
    assert.notEqual(await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")'), before, 'horizontal swipe ignored');
    const saved = await ev('localStorage.getItem("book-tiktok.the-potent-self.lastScreen")');
    loaded = event('Page.loadEventFired', sessionId); await c('Page.reload'); await loaded;
    await ev('document.fonts.ready');
    assert.equal(await ev('document.documentElement.lang'), 'en');
    assert.equal(await ev('document.querySelector(".mode-button.is-active").dataset.mode'), 'deep');
    assert.equal(await ev('document.querySelector("[data-start]").dataset.start'), 'continue');
    await ev('document.querySelector("[data-start=continue]").click()');
    assert.equal(await ev('document.querySelector("#contentsList .is-active").dataset.goTo'), saved);
    // Simulate a saved hidden depth with a shallower mode; Continue raises mode by ID.
    await ev('localStorage.setItem("book-tiktok.the-potent-self.lastScreen","transfer-example");localStorage.setItem("book-tiktok.the-potent-self.mode","essential")');
    loaded = event('Page.loadEventFired', sessionId); await c('Page.reload'); await loaded;
    await ev('document.querySelector("[data-start=continue]").click()');
    assert.equal(await ev('document.querySelector("#contentsList .is-active").dataset.goTo'), 'transfer-example');
    assert.equal(await ev('counter.textContent.endsWith("/ 21")'), true, 'hidden saved screen did not raise depth');
    loaded = event('Page.loadEventFired', sessionId); await c('Page.reload'); await loaded;
    await ev('document.querySelector("[data-start=begin]").click()');
    assert.equal(await ev('document.querySelector("#contentsList .is-active").dataset.goTo'), 'capacity-and-use');
    await c('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    await ev('document.querySelector("#desktopContentsList [data-go-to=final]").click()');
    await ev('new Promise(resolve => requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
    assert.equal(await ev('(()=>{const a=document.querySelector("#desktopContentsList .is-active").getBoundingClientRect();const r=document.querySelector("#desktopContentsList").getBoundingClientRect();return a.top>=r.top-1&&a.bottom<=r.bottom+1})()'), true, 'active desktop chapter not visible');
    report.interactions = ['buttons','keyboard','Sources','Settings gear','actual custom font usage RU/EN','language/position','theme/position','focus tap/key/escape/paging','vertical gesture ignored','horizontal gesture','saved Continue','saved hidden-depth ID raises mode','Start over','desktop rail synchronization'];
    await screenshot('desktop-final');
  }
  assert.deepEqual(network, [], 'reader attempted runtime HTTP/HTTPS');
  assert.deepEqual(errors, [], 'runtime exceptions');
  const reportPath = path.join(out, `${phase}.json`);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ phase, traversal: report.traversal?.cases, checks: report.interactions, reportPath, runtimeErrors: errors.length, runtimeNetworkRequests: network.length }));
} finally { cleanup(); }
