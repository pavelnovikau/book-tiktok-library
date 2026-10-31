// Book-local QA, using the maintained library QA's CDP/profile cleanup pattern.
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath, pathToFileURL } from 'node:url';

const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const evidence = '/Users/pn/smartcat/_private/book-tiktok-evidence/meditations-20261031/browser-qa';
fs.mkdirSync(evidence, { recursive: true });
const phase = process.argv[2] || 'traverse';
if (!['traverse', 'interactions'].includes(phase)) throw Error('Unknown phase');
const profile = execFileSync('/usr/bin/mktemp', ['-d', path.join(os.tmpdir(), 'meditations-chrome-XXXXXX')], { encoding: 'utf8' }).trim();
const binary = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let chrome, socket, cleaned = false;
const pending = new Map();
let seq = 0;
const errors = [], requests = [];
const report = { phase, file: path.join(dir, 'meditations.html'), offline: true, checks: [], runtimeErrors: errors, externalRequests: requests, screenshots: [] };
report.htmlSha256 = createHash('sha256').update(fs.readFileSync(report.file)).digest('hex');
const pause = ms => new Promise(r => setTimeout(r, ms));
function cleanup() {
  if (cleaned) return;
  cleaned = true;
  if (socket?.readyState <= 1) socket.close();
  if (chrome?.pid) { try { process.kill(-chrome.pid, 'SIGKILL'); } catch {} }
  fs.rmSync(profile, { recursive: true, force: true, maxRetries: 8, retryDelay: 60 });
}
process.on('exit', cleanup);
process.on('SIGINT', () => { cleanup(); process.exit(130); });
process.on('SIGTERM', () => { cleanup(); process.exit(143); });
async function freePort() {
  return new Promise(resolve => {
    const server = net.createServer();
    server.listen(0, '127.0.0.1', () => { const port = server.address().port; server.close(() => resolve(port)); });
  });
}
function command(method, params = {}) {
  const id = ++seq;
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => { pending.delete(id); reject(Error(`${method} timeout`)); }, 5000);
    pending.set(id, { resolve: r => { clearTimeout(timer); resolve(r); }, reject });
    socket.send(JSON.stringify({ id, method, params }));
  });
}
async function evaluate(expression) {
  const r = await command('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result?.value;
}
function assert(value, label) { if (!value) throw Error(label); report.checks.push(label); }
async function ready() {
  for (let i = 0; i < 50; i++) {
    if (await evaluate("document.readyState === 'complete' && Boolean(document.querySelector('#story h1'))")) return;
    await pause(30);
  }
  throw Error('Reader load timeout');
}
async function screenshot(name) {
  await evaluate('Promise.all(document.getAnimations().map(animation => animation.finished.catch(() => {})))');
  const r = await command('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  const filename = path.join(evidence, name + '.png');
  fs.writeFileSync(filename, Buffer.from(r.data, 'base64'));
  report.screenshots.push(filename);
}
async function viewport(width, height) {
  await command('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width < 900 });
}
async function go(id) { await evaluate(`document.querySelector('#contentsList [data-go-to="${id}"]').click()`); }
async function mode(value) { await evaluate(`document.querySelector('#dialogModePicker [data-mode="${value}"]').click()`); }
async function language(lang) { await evaluate(`if(document.documentElement.lang !== '${lang}') languageButton.click()`); }
async function theme(value) { await evaluate(`if(document.documentElement.dataset.theme !== '${value}') themeButton.click()`); }

try {
  const port = await freePort();
  chrome = spawn('/usr/bin/timeout', ['30', binary, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--disable-background-networking', `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`, 'about:blank'], { stdio: 'ignore', detached: true });
  let target;
  for (let i = 0; i < 80 && !target; i++) {
    try { target = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t => t.type === 'page'); } catch {}
    if (!target) await pause(40);
  }
  if (!target) throw Error('No owned Chrome target');
  socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => { socket.addEventListener('open', resolve, { once: true }); socket.addEventListener('error', reject, { once: true }); });
  socket.addEventListener('message', event => {
    const message = JSON.parse(String(event.data));
    if (message.id && pending.has(message.id)) {
      const request = pending.get(message.id); pending.delete(message.id);
      if (message.error) request.reject(Error(message.error.message)); else request.resolve(message.result || {});
    }
    if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails?.exception?.description || message.params.exceptionDetails?.text);
    if (message.method === 'Network.requestWillBeSent' && /^https?:/.test(message.params.request.url)) requests.push(message.params.request.url);
  });
  await command('Page.enable'); await command('Runtime.enable'); await command('Network.enable');
  await command('Network.emulateNetworkConditions', { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
  await viewport(390, 844);
  await command('Page.navigate', { url: pathToFileURL(report.file).href }); await ready();
  await evaluate('document.fonts.ready.then(() => true)');
  const defaults = await evaluate(`({lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,mode:document.querySelector('[data-mode].is-active')?.dataset.mode,fonts:document.fonts.check('16px Geist') && document.fonts.check('16px "Geist Mono"'),image:[...document.images].every(i=>i.complete&&i.naturalWidth>0),sourceDisplay:getComputedStyle(document.querySelector('#sourcesDialog')).display})`);
  assert(defaults.lang === 'ru' && defaults.theme === 'dark' && defaults.mode === 'essential', 'fresh RU/dark/Essential defaults');
  assert(defaults.fonts && defaults.image, 'embedded Geist fonts and title leaf decode offline');

  if (phase === 'traverse') {
    await screenshot('390-ru-dark-fresh-cover');
    report.layouts = [];
    for (const [width, height] of [[320,568], [390,844], [1024,768], [1440,900]]) {
      await viewport(width, height);
      for (const lang of ['ru','en']) {
        await language(lang);
        for (const color of ['dark','light']) {
          await theme(color);
          const result = await evaluate(`(() => {
            const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent), levels={essential:1,core:2,deep:3}, visits=[], bad=[];
            for(const m of ['essential','core','deep']) {
              document.querySelector('#dialogModePicker [data-mode="'+m+'"]').click();
              const expected=d.screens.filter(s=>s.level<=levels[m]);
              if(expected.length!==d.targetModes[m])bad.push('mode count '+m);
              for(const s of expected) {
                document.querySelector('#contentsList [data-go-to="'+s.id+'"]').click();
                const title=document.querySelector('#story h1').textContent;
                if(title!==s.copy[document.documentElement.lang].title)bad.push('title '+s.id);
                const slide=document.querySelector('.slide-scroll');
                if(document.documentElement.scrollWidth>innerWidth+1||slide.scrollWidth>slide.clientWidth+1)bad.push('overflow '+s.id);
                if(s.type!=='cover' && counter.textContent!==(expected.indexOf(s)+1)+' / '+expected.length)bad.push('counter '+s.id);
                const quote=document.querySelector('[data-quote-id]');
                if(s.quotation && !quote?.textContent.includes(s.quotation.text[document.documentElement.lang]))bad.push('quotation '+s.id);
                if(document.querySelector('#story .source-label') && getComputedStyle(document.querySelector('#story .source-label')).display!=='none')bad.push('research footer '+s.id);
                slide.scrollTop=slide.scrollHeight;
                const tail=slide.querySelector('.cover-actions button:last-child') || [...slide.children].reverse().find(x=>getComputedStyle(x).display!=='none');
                if(tail.getBoundingClientRect().bottom>slide.getBoundingClientRect().bottom+1)bad.push('unreachable scroll tail '+s.id);
                slide.scrollTop=0;
                visits.push({mode:m,id:s.id});
              }
            }
            return {visits:visits.length,unique:new Set(visits.map(x=>x.id)).size,bad};
          })()`);
          assert(result.bad.length === 0 && result.visits === 87 && result.unique === 39, `${width} ${lang} ${color}: all 87 nested positions / 39 screens, exact titles/counts/quotes, zero horizontal overflow`);
          const header = await evaluate(`new Promise(resolve=>requestAnimationFrame(()=>{
            const cs=[...document.querySelectorAll('.topbar a,.topbar button')].filter(x=>!x.hidden&&x.getBoundingClientRect().width>0),rs=cs.map(x=>x.getBoundingClientRect());
            const rail=document.querySelector('#desktopRail'), active=document.querySelector('#desktopContentsList .is-active');
            resolve({oneRow:Math.max(...rs.map(r=>r.top))-Math.min(...rs.map(r=>r.top))<2,inside:rs.every(r=>r.left>=0&&r.right<=innerWidth),icons:cs.every(x=>x.querySelector('svg')&&x.getAttribute('aria-label')&&x.textContent.trim()===''),rail:getComputedStyle(rail).display!=='none',active:active?.getAttribute('aria-current')==='page'});
          }))`);
          assert(header.oneRow && header.inside && header.icons, `${width} ${lang} ${color}: one compact accessible icon-only header row`);
          if (width >= 1024) assert(header.rail && header.active, `${width} ${lang} ${color}: desktop rail active item synchronized`);
          report.layouts.push({width,height,lang,theme:color,...result,header});
        }
      }
    }
    report.totalScreenVisits = report.layouts.reduce((n,x)=>n+x.visits,0);
    await viewport(390,844); await language('ru'); await theme('dark'); await mode('deep');
    await go('cover'); await screenshot('390-ru-dark-cover');
    await go('waking'); await screenshot('390-ru-dark-waking');
    await go('anger-nine'); await screenshot('390-ru-dark-dense');
    await viewport(320,568); await language('en'); await theme('light'); await go('judgment'); await screenshot('320-en-light-quotation');
    await go('final'); await screenshot('320-en-light-final');
    await viewport(1440,900); await screenshot('1440-en-light-final-rail');
  } else {
    await mode('deep'); await go('judgment');
    const initialCounter = await evaluate('counter.textContent');
    await language('en'); await theme('light');
    assert(await evaluate(`counter.textContent===${JSON.stringify(initialCounter)} && localStorage.getItem('book-tiktok.meditations.lastScreen')==='judgment'`), 'language and theme preserve stable screen and depth');
    await evaluate('sourcesButton.click()');
    assert(await evaluate("sourcesDialog.open && sourcesList.children.length===3 && methodNote.textContent.includes('13 of 14') && methodNote.textContent.includes('XII.35')"), 'Sources dialog includes exact edition scope, translator concordance and MIT limitation');
    await evaluate("document.querySelector('[data-close-dialog=\"sourcesDialog\"]').click()");
    await evaluate('contentsButton.click()');
    assert(await evaluate('contentsDialog.open && contentsList.children.length===39'), 'Contents dialog shows exact Deep corpus');
    await evaluate("document.querySelector('#contentsList [data-go-to=\"caesar\"]').click()");
    assert(await evaluate("!contentsDialog.open && document.querySelector('#story h1').textContent==='A warning to an emperor'"), 'chapter button navigation closes dialog and preserves target');
    await evaluate('document.activeElement?.blur()');
    await command('Input.dispatchKeyEvent', {type:'keyDown',key:'ArrowRight',code:'ArrowRight'});
    assert(await evaluate("document.querySelector('#story h1').textContent==='Gladly changing his mind'"), 'keyboard advances by correct stable screen');
    await evaluate('nextButton.click()');
    assert(await evaluate("document.querySelector('#story h1').textContent==='The bee and the swarm'"), 'Next button advances');
    await evaluate('previousButton.click()');
    assert(await evaluate("document.querySelector('#story h1').textContent==='Gladly changing his mind'"), 'Back button reverses');
    await evaluate("story.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:280,clientY:240,pointerId:7}));story.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:100,clientY:245,pointerId:7}))");
    assert(await evaluate("document.querySelector('#story h1').textContent==='The bee and the swarm'"), 'horizontal pointer swipe advances');
    await evaluate("story.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,clientX:160,clientY:400,pointerId:8}));story.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,clientX:162,clientY:120,pointerId:8}))");
    assert(await evaluate("document.querySelector('#story h1').textContent==='The bee and the swarm'"), 'vertical pointer gesture does not change page');
    const tap = await evaluate("(()=>{const r=document.querySelector('#story p:not(.kicker)').getBoundingClientRect();return {x:r.left+20,y:r.top+8}})()");
    await command('Input.dispatchMouseEvent',{type:'mousePressed',...tap,button:'left',clickCount:1});
    await command('Input.dispatchMouseEvent',{type:'mouseReleased',...tap,button:'left',clickCount:1});
    assert(await evaluate("document.documentElement.dataset.focusMode==='true'"), 'tap on non-interactive reading text enables focus');
    await command('Input.dispatchMouseEvent',{type:'mousePressed',...tap,button:'left',clickCount:1});
    await command('Input.dispatchMouseEvent',{type:'mouseReleased',...tap,button:'left',clickCount:1});
    assert(await evaluate("document.documentElement.dataset.focusMode!=='true'"), 'second reading-text tap restores chrome');
    await evaluate('document.activeElement?.blur()');
    await command('Input.dispatchKeyEvent', {type:'keyDown',key:'f',code:'KeyF'});
    assert(await evaluate("document.documentElement.dataset.focusMode==='true' && getComputedStyle(document.querySelector('.app-header')).display==='none' && nextButton.getBoundingClientRect().width>0"), 'focus mode hides header and retains Next');
    await evaluate('nextButton.click()');
    assert(await evaluate("document.documentElement.dataset.focusMode==='true'"), 'paging preserves focus');
    await command('Input.dispatchKeyEvent', {type:'keyDown',key:'Escape',code:'Escape'});
    assert(await evaluate("document.documentElement.dataset.focusMode!=='true' && getComputedStyle(document.querySelector('.app-header')).display!=='none'"), 'Escape restores normal reading');
    await mode('deep'); await go('anger-nine');
    await command('Page.reload'); await ready();
    assert(await evaluate("document.querySelector('[data-start=\"continue\"]')?.textContent.includes('Before passing judgment')"), 'reload offers saved stable-screen continuation');
    await evaluate("document.querySelector('[data-start=\"continue\"]').click()");
    assert(await evaluate("document.querySelector('#story h1').textContent==='Before passing judgment'"), 'Continue restores saved screen');
    await command('Page.reload'); await ready(); await evaluate("document.querySelector('[data-start=\"begin\"]').click()");
    assert(await evaluate("document.querySelector('#story h1').textContent==='First, what he owes'"), 'Start over begins at first reading screen');
    await mode('deep'); await go('anger-nine'); await evaluate("localStorage.setItem('book-tiktok.meditations.mode','essential')");
    await command('Page.reload'); await ready(); await evaluate("document.querySelector('[data-start=\"continue\"]').click()");
    assert(await evaluate("document.querySelector('#story h1').textContent==='Before passing judgment' && localStorage.getItem('book-tiktok.meditations.mode')==='deep'"), 'saved hidden Deep screen raises depth correctly (no fiction spoiler policy applies)');
    await go('final'); await evaluate('nextButton.click()');
    assert(await evaluate("Boolean(document.querySelector('[data-start=\"begin\"]')) && !localStorage.getItem('book-tiktok.meditations.lastScreen')"), 'final Restart clears saved position');
    await viewport(320,568); await language('ru');
    await command('Emulation.setSafeAreaInsetsOverride',{insets:{top:47,bottom:34,left:0,right:0}});
    const safe = await evaluate(`new Promise(resolve=>requestAnimationFrame(()=>{const cs=[...document.querySelectorAll('.topbar a,.topbar button')].filter(x=>!x.hidden&&x.getBoundingClientRect().width>0);resolve(cs.every(x=>{const r=x.getBoundingClientRect();return r.top>=47&&r.left>=0&&r.right<=innerWidth}));}))`);
    assert(safe, '320px compact header stays below emulated 47px iOS status safe area');
    await screenshot('320-ru-safe-area-cover');
    await command('Emulation.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'});
    await command('Page.reload'); await ready(); await pause(550);
    const install = await evaluate("({trigger:!document.querySelector('#bookLibraryInstallTrigger')?.hidden,dialog:document.querySelector('.book-library-install-dialog')?.open})");
    assert(install.trigger && install.dialog, 'emulated iPhone Safari offers install guide in the same row');
    await evaluate("document.querySelector('.book-library-install-dialog').close()");
    await evaluate("document.querySelector('#bookLibraryInstallTrigger').click()");
    assert(await evaluate("document.querySelector('.book-library-install-dialog').open"), 'install guide remains available manually');
    await evaluate("document.querySelector('.book-library-install-dialog').close()");
    await command('Page.addScriptToEvaluateOnNewDocument',{source:"Object.defineProperty(navigator,'standalone',{get:()=>true});"});
    await command('Page.reload'); await ready(); await pause(500);
    assert(await evaluate("document.querySelector('#bookLibraryInstallTrigger').hidden && !document.querySelector('.book-library-install-dialog').open"), 'emulated standalone hides install guide and trigger');
  }
  assert(errors.length === 0, 'zero runtime exceptions');
  assert(requests.length === 0, 'zero external runtime network requests while offline');
  report.status = 'worker-local-checks-passed';
} catch (error) {
  report.status = 'failed'; report.failure = String(error.stack || error); process.exitCode = 1;
} finally {
  cleanup();
  report.ownedProfileRemoved = !fs.existsSync(profile);
  fs.writeFileSync(path.join(dir, 'qa', `browser-${phase}.json`), JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({phase,status:report.status,checks:report.checks.length,visits:report.totalScreenVisits,errors,requests,profileRemoved:report.ownedProfileRemoved,failure:report.failure},null,2));
}
