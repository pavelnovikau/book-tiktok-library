import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

const base = path.dirname(fileURLToPath(import.meta.url));
const [widthArg = '320', heightArg = '568', kind = 'matrix'] = process.argv.slice(2);
const width = Number(widthArg), height = Number(heightArg);
const qa = path.join(base, 'qa');
fs.mkdirSync(qa, { recursive: true });
const data = JSON.parse(fs.readFileSync(path.join(base, 'story-data.json'), 'utf8'));
const profile = execFileSync('mktemp', ['-d', path.join(os.tmpdir(), 'nvc-chrome-XXXXXX')], { encoding: 'utf8' }).trim();
const chrome = spawn('/usr/bin/timeout', [
  '30', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '--headless=new', '--no-first-run', '--no-default-browser-check',
  '--disable-background-networking', '--disable-component-update',
  '--disable-features=MediaRouter', '--remote-debugging-port=0',
  `--user-data-dir=${profile}`, 'about:blank'
], { stdio: 'ignore', detached: true });
let ws, sequence = 0, cleaned = false;
const pending = new Map(), errors = [], requests = [];
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
function assert(value, message) { if (!value) throw new Error(message); }
function cleanup() {
  if (cleaned) return;
  cleaned = true;
  try { ws?.close(); } catch {}
  try { process.kill(-chrome.pid, 'SIGKILL'); } catch {}
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 50 });
}
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });
process.on('SIGTERM', () => { cleanup(); process.exit(143); });
function send(method, params = {}) {
  const id = ++sequence;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`${method} timed out`)); }, 6000);
    pending.set(id, { resolve: result => { clearTimeout(timer); resolve(result); }, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}
async function ev(expression) {
  const result = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) throw new Error(JSON.stringify(result.exceptionDetails));
  return result.result.value;
}
async function loaded() {
  for (let i = 0; i < 120; i++) {
    if (await ev('document.readyState === "complete" && !!document.querySelector("#story h1")')) return;
    await delay(25);
  }
  throw new Error('Reader did not load');
}
async function screenshot(name) {
  const result = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  fs.writeFileSync(path.join(qa, `${width}-${name}.png`), Buffer.from(result.data, 'base64'));
}
const hash = name => createHash('sha256').update(fs.readFileSync(path.join(base, name))).digest('hex');
const report = { viewport: [width, height], kind, errors, requests, modes: [], interactions: [], standaloneFile: true,
  testedHashes: { authoring: hash('story-data.json'), html: hash('nonviolent-communication.html') } };
try {
  let port;
  for (let i = 0; i < 150; i++) {
    try { port = fs.readFileSync(path.join(profile, 'DevToolsActivePort'), 'utf8').split('\n')[0]; break; } catch {}
    await delay(40);
  }
  assert(port, 'Chrome startup');
  const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  ws = new WebSocket(targets.find(target => target.type === 'page').webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  ws.onmessage = event => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const task = pending.get(message.id);
      pending.delete(message.id);
      message.error ? task.reject(new Error(JSON.stringify(message.error))) : task.resolve(message.result);
    } else if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails);
    else if (message.method === 'Log.entryAdded' && message.params.entry.level === 'error') errors.push(message.params.entry);
    else if (message.method === 'Network.requestWillBeSent' && /^https?:/.test(message.params.request.url)) requests.push(message.params.request.url);
  };
  await send('Page.enable');
  await send('Runtime.enable');
  await send('Log.enable');
  await send('Network.enable');
  await send('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  if (kind === 'ios') {
    await send('Emulation.setUserAgentOverride', {
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
      platform: 'iPhone'
    });
  }
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 900 });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Page.navigate', { url: pathToFileURL(path.join(base, 'nonviolent-communication.html')).href });
  await loaded();
  await ev(`Object.keys(localStorage).filter(k => k.startsWith('book-tiktok.nonviolent-communication.')).forEach(k => localStorage.removeItem(k)); location.reload(); true`);
  await delay(120);
  await loaded();
  report.defaults = await ev(`({language:document.documentElement.lang,theme:document.documentElement.dataset.theme,count:document.querySelector('#counter').textContent,focus:document.documentElement.dataset.focusMode})`);
  assert(report.defaults.language === 'ru' && report.defaults.theme === 'dark' && report.defaults.count === '1 / 16', 'RU/dark/Essential defaults');
  const embedded = await ev(`JSON.parse(document.querySelector('#book-tiktok-data').textContent)`);
  assert(JSON.stringify(embedded.screens) === JSON.stringify(data.screens), 'Embedded/canonical screen mismatch');
  report.embeddedPairsCompared = embedded.screens.length;
  await ev('document.fonts.ready.then(() => true)');
  report.fonts = await ev('[...document.fonts].map(font=>({family:font.family,status:font.status}))');
  assert(report.fonts.length >= 2 && report.fonts.every(font => font.status === 'loaded'), 'Embedded fonts');
  if (kind === 'matrix') {
    for (const language of ['ru', 'en']) {
      if (await ev('document.documentElement.lang') !== language) await ev('languageButton.click()');
      for (const theme of ['dark', 'light']) {
        if (await ev('document.documentElement.dataset.theme') !== theme) await ev('themeButton.click()');
        await delay(220);
        await screenshot(`${language}-${theme}-cover`);
        for (const [mode, expected] of Object.entries(data.targetModes)) {
          const result = await ev(`(async()=>{
            document.querySelector('[data-mode="${mode}"]').click();
            const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent);
            const list=d.screens.filter(s=>s.level<=({essential:1,core:2,deep:3})['${mode}']);
            const r={language:'${language}',theme:'${theme}',mode:'${mode}',visited:0,failures:[],scrolling:[]};
            for(let i=0;i<list.length;i++){
              if(i)nextButton.click();
              await new Promise(requestAnimationFrame);
              const s=list[i], sc=document.querySelector('.slide-scroll');
              if(document.querySelector('#story h1').textContent!==s.copy['${language}'].title)r.failures.push([s.id,'title']);
              if(!sc.innerHTML.includes(s.copy['${language}'].body))r.failures.push([s.id,'body']);
              if(counter.textContent!==((i+1)+' / '+list.length))r.failures.push([s.id,'counter']);
              if(document.documentElement.scrollWidth>innerWidth+1||sc.scrollWidth>sc.clientWidth+1)r.failures.push([s.id,'overflow']);
              if(s.type!=='cover'&&getComputedStyle(document.querySelector('.source-label')).display!=='none')r.failures.push([s.id,'sources-outside-dialog']);
              const controls=[libraryButton,contentsButton,languageButton,sourcesButton,themeButton];
              const rects=controls.map(n=>n.getBoundingClientRect());
              if(rects.some(r=>r.left<0||r.right>innerWidth+1)||Math.max(...rects.map(r=>r.top))-Math.min(...rects.map(r=>r.top))>1)r.failures.push([s.id,'header-layout']);
              if(controls.some(n=>n.textContent.trim()||!n.querySelector('svg')||!n.getAttribute('aria-label')))r.failures.push([s.id,'icon-controls']);
              if(sc.scrollHeight>sc.clientHeight+2){sc.scrollTop=sc.scrollHeight;if(sc.scrollTop<1)r.failures.push([s.id,'scroll']);r.scrolling.push(s.id);sc.scrollTop=0;}
              if(innerWidth>=900){
                const rail=document.querySelector('.desktop-rail'),active=rail.querySelector('[aria-current="page"]');
                if(getComputedStyle(rail).display==='none'||active?.dataset.goTo!==s.id)r.failures.push([s.id,'rail']);
                const ar=active.getBoundingClientRect(), rr=document.querySelector('.desktop-contents').getBoundingClientRect();
                if(ar.top<rr.top-1||ar.bottom>rr.bottom+1)r.failures.push([s.id,'active-rail-outside']);
              }
              r.visited++;
            }
            nextButton.click();return r;
          })()`);
          report.modes.push(result);
          assert(result.visited === expected && !result.failures.length, JSON.stringify(result));
        }
        await ev(`(()=>{contentsButton.click(); const b=contentsList.querySelector('[data-go-to]');b.dataset.goTo='principal-meeting';b.click();return true})()`);
        await screenshot(`${language}-${theme}-principal`);
        await ev(`(()=>{contentsButton.click(); const b=contentsList.querySelector('[data-go-to]');b.dataset.goTo='cover';b.click();return true})()`);
      }
    }
  } else if (kind === 'ios') {
    await delay(550);
    assert(await ev('bookLibraryInstallDialog.open && !bookLibraryInstallTrigger.hidden'), 'iOS automatic guide');
    await ev('bookLibraryInstallClose.click(); languageButton.click()');
    await delay(60);
    await ev('bookLibraryInstallTrigger.click()');
    assert(await ev('bookLibraryInstallDialog.open && bookLibraryInstallDialog.textContent.includes("Add to Home Screen")'), 'iOS English guide');
    await screenshot('ios-en-guide');
    await ev('bookLibraryInstallClose.click()');
    const row = await ev(`(()=>{
      const nodes=[libraryButton,contentsButton,languageButton,sourcesButton,themeButton,bookLibraryInstallTrigger];
      const r=nodes.map(n=>n.getBoundingClientRect());
      return {count:nodes.length,inside:r.every(x=>x.left>=0&&x.right<=innerWidth+1),oneRow:Math.max(...r.map(x=>x.top))-Math.min(...r.map(x=>x.top))<=1,icons:nodes.every(n=>n.querySelector('svg')&&!n.textContent.trim())};
    })()`);
    assert(row.inside && row.oneRow && row.icons, 'Six-control iOS row '+JSON.stringify(row));
    await ev(`document.documentElement.style.setProperty('--reader-safe-top','47px')`);
    await delay(80);
    assert(await ev('libraryButton.getBoundingClientRect().top >= 47'), 'iOS safe area');
    await screenshot('ios-safe-area');
    await send('Page.addScriptToEvaluateOnNewDocument', { source: 'Object.defineProperty(navigator, "standalone", {get:()=>true});' });
    await send('Page.reload'); await delay(550); await loaded();
    assert(await ev('!bookLibraryInstallDialog.open && bookLibraryInstallTrigger.hidden'), 'Standalone guide hidden');
    report.ios = { automaticGuide: true, englishGuide: true, header: row, safeArea47: true, standaloneGuideHidden: true, realDevice: false };
  } else {
    report.interactions = await ev(`(async()=>{
      const checks=[],ok=(x,m)=>{if(!x)throw Error(m);checks.push(m)};
      const key=k=>document.body.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true}));
      document.querySelector('[data-start]').click();
      const first=document.querySelector('#story h1').textContent;
      key('ArrowRight');ok(counter.textContent.startsWith('3 /'),'ArrowRight');
      key('ArrowLeft');ok(document.querySelector('#story h1').textContent===first,'ArrowLeft');
      key('PageDown');key('PageUp');ok(document.querySelector('#story h1').textContent===first,'page keys');
      key(' ');ok(counter.textContent.startsWith('3 /'),'Space');
      const before=counter.textContent;languageButton.click();themeButton.click();languageButton.click();themeButton.click();ok(counter.textContent===before,'language/theme position');
      sourcesButton.click();ok(sourcesDialog.open&&sourcesList.children.length===11,'Sources dialog and 11 sources');
      ok(methodNote.textContent.includes('не по полному EPUB'),'honest scope in dialog');
      document.querySelector('[data-close-dialog="sourcesDialog"]').click();ok(!sourcesDialog.open,'Sources close');
      contentsButton.click();ok(contentsDialog.open,'Contents open');
      const b=contentsList.querySelector('[data-go-to]');b.dataset.goTo='one-delay-different-feelings';b.click();
      ok(counter.textContent.endsWith('/ 30'),'hidden target raises depth');
      key('f');ok(document.documentElement.dataset.focusMode==='true','F focus');
      ok(getComputedStyle(document.querySelector('.app-header')).display==='none','focus hides header');
      ok(getComputedStyle(document.querySelector('.desktop-rail')).display==='none','focus hides rail');
      ok(getComputedStyle(nextButton).display!=='none','focus keeps Next');
      nextButton.click();ok(document.documentElement.dataset.focusMode==='true','focus persists');key('Escape');ok(!document.documentElement.dataset.focusMode,'Escape restores');
      const el=document.querySelector('#story'),pointer=(t,x,y)=>el.dispatchEvent(new PointerEvent(t,{pointerId:11,clientX:x,clientY:y,bubbles:true,button:0}));
      pointer('pointerdown',120,190);pointer('pointerup',120,190);ok(document.documentElement.dataset.focusMode==='true','tap focus');
      pointer('pointerdown',120,190);pointer('pointerup',120,190);ok(!document.documentElement.dataset.focusMode,'tap restore');
      const pos=counter.textContent;pointer('pointerdown',150,190);pointer('pointerup',150,290);ok(counter.textContent===pos&&!document.documentElement.dataset.focusMode,'vertical gesture exclusion');
      pointer('pointerdown',220,190);pointer('pointerup',100,194);ok(counter.textContent!==pos&&!document.documentElement.dataset.focusMode,'horizontal swipe');
      return checks;
    })()`);
    const saved = await ev(`localStorage.getItem('book-tiktok.nonviolent-communication.lastScreen')`);
    await send('Page.reload'); await delay(100); await loaded();
    assert(await ev(`!!document.querySelector('[data-start="continue"]')`), 'Continue button');
    await ev(`document.querySelector('[data-start="continue"]').click()`);
    assert(await ev(`document.querySelector('.desktop-rail [aria-current="page"]').dataset.goTo`) === saved, 'Saved progress');
    await send('Page.reload'); await delay(100); await loaded();
    await ev(`document.querySelector('[data-start="begin"]').click()`);
    assert(await ev(`counter.textContent.startsWith('2 /')`), 'Start over');
    report.interactions.push('saved progress / Continue / Start over');
    await ev(`(()=>{contentsButton.click();const b=contentsList.querySelector('[data-go-to]');b.dataset.goTo='final';b.click();return true})()`);
    await screenshot('final');
    await ev('nextButton.click()');
    assert(await ev(`!!document.querySelector('.cover-layout')`), 'Final restart');
    report.interactions.push('final restart');
    // Emulated safe-area placement without changing the actual source file.
    await ev(`document.documentElement.style.setProperty('--reader-safe-top','47px'); true`);
    await delay(80);
    const safe = await ev(`({top:libraryButton.getBoundingClientRect().top,padding:getComputedStyle(document.querySelector('.app-header')).paddingTop,safe:getComputedStyle(document.documentElement).getPropertyValue('--reader-safe-top'),controls:[libraryButton,contentsButton,languageButton,sourcesButton,themeButton].every(n=>n.getBoundingClientRect().right<=innerWidth+1)})`);
    assert(safe.top >= 47 && safe.controls, 'Safe area '+JSON.stringify(safe));
    report.safeArea = safe;
    report.realIPhonePwaTest = false;
  }
  assert(!errors.length, `Runtime errors: ${JSON.stringify(errors)}`);
  assert(!requests.length, `External runtime requests: ${JSON.stringify(requests)}`);
  report.cleanup = 'Unique mktemp profile; timeout 30; owned process group terminated and profile deleted in finally';
  fs.writeFileSync(path.join(qa, `${kind}-${width}.json`), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ viewport: report.viewport, kind, visited: report.modes.reduce((sum,m)=>sum+m.visited,0), interactions: report.interactions.length, errors: errors.length, externalRequests: requests.length }));
} finally {
  try { if (ws?.readyState === 1) await Promise.race([send('Browser.close'), delay(250)]); } catch {}
  cleanup();
}
