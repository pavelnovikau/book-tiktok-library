import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const dir = path.dirname(fileURLToPath(import.meta.url));
const phase = process.argv[2] || '390';
const sizes = { '320': [320,568], '390': [390,844], '1024': [1024,768], '1440': [1440,900], interactions: [390,844], ios: [320,568], visual: [320,568] };
if (!sizes[phase]) throw new Error('Unknown phase');
const output = path.join(dir, 'qa');
fs.mkdirSync(output, {recursive:true});
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'solaris-qa-chrome-'));
let chrome, ws, cleaned = false;
function cleanup() {
  if (cleaned) return;
  cleaned = true;
  try { ws?.close(); } catch {}
  try { process.kill(-chrome.pid, 'SIGKILL'); } catch {}
  fs.rmSync(profile, {recursive:true,force:true,maxRetries:5,retryDelay:60});
}
process.on('exit', cleanup);
for (const sig of ['SIGINT','SIGTERM']) process.on(sig, () => {cleanup();process.exit(1);});
const port = await new Promise(resolve => {
  const n = net.createServer(); n.listen(0,'127.0.0.1', () => {const p=n.address().port;n.close(()=>resolve(p));});
});
const [width,height] = sizes[phase];
chrome = spawn('/opt/homebrew/bin/timeout', ['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,
  `--remote-debugging-port=${port}`,`--window-size=${width},${height}`,'about:blank'], {stdio:'ignore',detached:true});
const delay = ms => new Promise(r=>setTimeout(r,ms));
let target;
for (let n=0;n<100;n++) {
  try {target=(await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t=>t.type==='page');}catch{}
  if (target) break; await delay(50);
}
if (!target) throw new Error('Owned Chrome did not start');
ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
let seq=0;const pending=new Map();const errors=[],requests=[];
ws.addEventListener('message',event=>{
  const m=JSON.parse(String(event.data));
  if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);}
  if(m.method==='Runtime.exceptionThrown') errors.push(m.params.exceptionDetails);
  if(m.method==='Runtime.consoleAPICalled'&&m.params.type==='error') errors.push(m.params);
  if(m.method==='Network.requestWillBeSent'&&/^https?:/.test(m.params.request.url)) requests.push(m.params.request.url);
});
function cdp(method,params={}){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(new Error('CDP timeout '+method));},4000);pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
async function shot(name){await delay(400);const r=await cdp('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(output,name+'.png'),Buffer.from(r.data,'base64'));}
const url=pathToFileURL(path.join(dir,'solaris.html')).href;
await cdp('Page.enable');await cdp('Runtime.enable');await cdp('Network.enable');
await cdp('Network.setBlockedURLs',{urls:['http://*','https://*']});
await cdp('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
await cdp('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<500});
async function load(){await cdp('Page.navigate',{url});for(let i=0;i<100;i++){if(await evaluate("!!document.querySelector('#story h1') && !!window.BookSettings").catch(()=>false))break;await delay(20);}await evaluate('document.fonts.ready.then(()=>true)');}
await load();
await evaluate("localStorage.clear();sessionStorage.clear();true");
await load();
const defaults=await evaluate(`({lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont,mode:document.querySelector('[data-mode][aria-pressed="true"]').dataset.mode,home:document.querySelector('#libraryButton').getAttribute('href')})`);
if(defaults.lang!=='ru'||defaults.theme!=='dark'||defaults.mode!=='essential'||defaults.home!=='./')throw new Error('Bad defaults '+JSON.stringify(defaults));
let result={phase,width,height,url,offline:true,defaults,checks:[],visits:0};
if (/^\d+$/.test(phase)) {
  result.matrix = await evaluate(`(async()=>{
    const data=JSON.parse(document.querySelector('#book-tiktok-data').textContent);
    const failures=[];let visits=0,scrollable=0,dialogs=0;
    const assert=(x,message)=>{if(!x)failures.push(message);};
    const click=s=>{const el=document.querySelector(s);if(!el)throw Error('missing '+s);el.click();};
    const active=()=>document.querySelector('#desktopContentsList .is-active')?.dataset.goTo;
    const plain=x=>{const d=document.createElement('div');d.innerHTML=x;return d.textContent;};
    const css=document.createElement('style');css.textContent='*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}';document.head.append(css);
    const within=(r,b)=>r.left>=b.left-1&&r.right<=b.right+1;
    for(const font of ['sans','serif'])for(const theme of ['dark','light'])for(const language of ['ru','en'])for(const mode of ['essential','core','deep']){
      document.querySelectorAll('dialog[open]').forEach(d=>d.close());
      if(document.documentElement.lang!==language)click('#languageButton');
      BookSettings.set('readingFont',font);BookSettings.set('theme',theme);
      await document.fonts.ready;
      click('[data-mode="'+mode+'"]');
      if(document.querySelector('#solarisSpoilerDialog').open){
        const d=document.querySelector('#solarisSpoilerDialog'),r=d.getBoundingClientRect();
        assert(r.left>=-1&&r.right<=innerWidth+1,'consent dialog width');
        for(const el of d.querySelectorAll('h2,p,button'))assert(within(el.getBoundingClientRect(),r),'consent child overflow');
        d.scrollTop=d.scrollHeight;
        assert(d.querySelector('.dialog-footer').getBoundingClientRect().bottom<=r.bottom+2,'consent footer clipped');
        click('#solarisSpoilerAccept');
      }
      click('[data-go-to="cover"]');
      const list=data.screens.filter(s=>s.level<=({essential:1,core:2,deep:3}[mode]));
      const context=[font,theme,language,mode].join('/');
      assert(list.length===data.targetModes[mode],context+' count');
      assert(document.querySelectorAll('#contentsList [data-go-to]').length===list.length,context+' contents count');
      assert(JSON.stringify([...document.querySelectorAll('#contentsList [data-go-to]')].map(e=>e.dataset.goTo))===JSON.stringify(list.map(s=>s.id)),context+' contents ids');
      if(mode!=='deep')assert(![...document.querySelectorAll('#contentsList [data-go-to]')].some(el=>data.screens.find(s=>s.id===el.dataset.goTo).level===3),context+' late contents leak');
      for(let index=0;index<list.length;index++){
        const s=list[index],copy=s.copy[language],label=context+'/'+s.id;
        assert(active()===s.id,label+' active');
        assert(document.querySelector('#story h1').textContent===copy.title,label+' title');
        assert(document.querySelector('#counter').textContent===(index+1)+' / '+list.length,label+' counter');
        assert(document.querySelector('#story').textContent.includes(plain(copy.body)),label+' body');
        assert(!document.querySelector('#story .source-label'),label+' narrative chrome');
        assert(document.documentElement.scrollWidth<=innerWidth+1,label+' document overflow');
        const sc=document.querySelector('#story .slide-scroll'),r=sc.getBoundingClientRect();
        assert(sc.scrollWidth<=sc.clientWidth+1,label+' scroller overflow');
        for(const el of sc.querySelectorAll('p,h1,.cover-copy,.cover-actions,.cover-visual'))assert(within(el.getBoundingClientRect(),r),label+' child overflow');
        sc.scrollTop=sc.scrollHeight;
        assert(Math.abs(sc.scrollTop-Math.max(0,sc.scrollHeight-sc.clientHeight))<2,label+' scroll bottom');
        if(sc.scrollHeight>sc.clientHeight+1)scrollable++;
        const end=sc.lastElementChild;
        assert(end.getBoundingClientRect().bottom<=r.bottom+2,label+' bottom clipped');
        if(s.type==='cover'){
          const pic=sc.querySelector('img');assert(pic?.complete&&pic.naturalWidth>0,label+' cover decode');
          const parent=sc.querySelector('.cover-copy').getBoundingClientRect();
          for(const el of sc.querySelector('.cover-copy').children)assert(within(el.getBoundingClientRect(),parent),label+' cover copy width');
        }
        if(innerWidth>=900)assert(getComputedStyle(document.querySelector('#desktopRail')).display!=='none',label+' desktop rail');
        visits++;
        if(index<list.length-1){if(index===0)click('[data-go-to="'+list[1].id+'"]');else click('#nextButton');}
      }
      for(const [button,id] of [['#sourcesButton','sourcesDialog'],['#contentsButton','contentsDialog']]){
        click(button);const d=document.getElementById(id);d.scrollTop=0;const b=d.getBoundingClientRect();
        assert(d.open&&b.left>=-1&&b.right<=innerWidth+1,context+'/'+id+' dialog width');
        const sc=d.querySelector('.dialog-body');if(sc)sc.scrollTop=sc.scrollHeight;
        if(id==='sourcesDialog')assert(d.querySelectorAll('#sourcesList li').length===data.sources.length,context+' source count');
        d.close();dialogs++;
      }
    }
    return {visits,scrollable,dialogs,failures,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})),sources:data.sources.length};
  })()`);
  result.visits=result.matrix.visits;
  if(result.matrix.failures.length)throw new Error(JSON.stringify(result.matrix.failures.slice(0,12)));
  if(phase==='320'||phase==='1440'){
    await evaluate(`document.querySelectorAll('dialog[open]').forEach(d=>d.close());document.querySelector('[data-go-to="cover"]').click();true`);
    await shot('cover-'+phase);
    await evaluate(`document.querySelector('[data-go-to="reported-final-will"]').click();true`);
    await shot('letter-'+phase);
  }
} else if(phase==='interactions') {
  const evalCheck=async(name,code)=>{const value=await evaluate(code);if(!value)throw new Error(name+' '+JSON.stringify(await evaluate("({dialog:document.querySelector('#solarisSpoilerDialog').open,count:document.querySelectorAll('#contentsList [data-go-to]').length,focus:document.activeElement?.id})")));result.checks.push(name);console.log('PASS '+name);};
  const click=async(selector)=>evaluate(`document.querySelector(${JSON.stringify(selector)}).click();true`);
  const key=async(key,code=key)=>{const vk=({Escape:27,ArrowRight:39,ArrowLeft:37,' ':32,f:70})[key]||0;await cdp('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:vk,nativeVirtualKeyCode:vk});await cdp('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:vk,nativeVirtualKeyCode:vk});await delay(40);};
  await click('[data-mode="deep"]');
  await evalCheck('Deep selection waits; no late contents',`document.querySelector('#solarisSpoilerDialog').open&&document.querySelectorAll('#contentsList [data-go-to]').length===10`);
  await key('Escape');
  await evalCheck('Escape cancels without entering Deep',`!document.querySelector('#solarisSpoilerDialog').open&&document.querySelectorAll('#contentsList [data-go-to]').length===10`);
  await click('[data-mode="deep"]');await click('#solarisSpoilerAccept');
  await evalCheck('Explicit consent opens Deep contents',`document.querySelectorAll('#contentsList [data-go-to]').length===32`);
  await click('[data-go-to="oxygen-attempt"]');
  await click('#languageButton');
  await evalCheck('Language preserves late stable ID',`document.documentElement.lang==='en'&&document.querySelector('#desktopContentsList .is-active').dataset.goTo==='oxygen-attempt'`);
  await click('#themeButton');
  await evaluate(`document.querySelector('input[name="book-theme"][value="light"]').click();document.querySelector('input[name="book-font"][value="serif"]').click();true`);
  await evalCheck('Settings UI preserves ID and discloses Cyrillic fallback',`document.querySelector('#bookSettingsDialog').open&&document.querySelector('#desktopContentsList .is-active').dataset.goTo==='oxygen-attempt'&&document.documentElement.dataset.theme==='light'&&document.querySelector('#bookSettingsFontNote').textContent.includes('Source Serif 4')`);
  await click('#bookSettingsClose');
  await load();
  await evalCheck('Reload revokes Deep and uses generic safe resume',`document.querySelectorAll('#contentsList [data-go-to]').length===10&&document.querySelector('[data-start="continue"]').textContent==='Continue Deep — ending spoilers'&&!document.querySelector('#story').textContent.includes('Hissing in the dark')`);
  await evaluate(`document.querySelector('#story .slide-scroll').scrollTop=10000;true`);await shot('resume-safe');
  await click('#languageButton');
  await evalCheck('Russian saved Deep label is generic',`document.querySelector('[data-start="continue"]').textContent==='Продолжить Deep — спойлеры финала'&&!document.querySelector('#story').textContent.includes('Шипение в темноте')`);
  await click('[data-start="continue"]');
  await evalCheck('Russian consent is localized',`document.querySelector('#solarisSpoilerDialog').open&&document.querySelector('#solarisSpoilerTitle').textContent==='Открыть сюжет и финал?'`);
  await click('#solarisSpoilerCancel');await click('#languageButton');
  await click('[data-start="continue"]');
  await evalCheck('Deep resume requires new consent',`document.querySelector('#solarisSpoilerDialog').open&&document.querySelector('#desktopContentsList .is-active').dataset.goTo==='cover'`);
  await click('#solarisSpoilerCancel');await click('[data-start="continue"]');await click('#solarisSpoilerAccept');
  await evalCheck('Accepted resume returns to same ID',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='oxygen-attempt'`);
  await click('[data-mode="core"]');await click('[data-mode="deep"]');
  await evalCheck('Leaving Deep revokes consent',`document.querySelector('#solarisSpoilerDialog').open`);
  await click('#solarisSpoilerCancel');
  await evaluate(`const trigger=document.createElement('button');trigger.dataset.goTo='reported-final-will';document.querySelector('#desktopContentsList').append(trigger);true`);
  // Exercise the same hidden-ID pathway through a remembered ID, rather than an unbound synthetic node.
  await evaluate(`localStorage.setItem('book-tiktok.solaris.lastScreen','reported-final-will');true`);await load();
  await click('[data-start="continue"]');await click('#solarisSpoilerAccept');
  await evalCheck('Saved hidden level-3 ID raises depth after consent',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='reported-final-will'&&document.querySelectorAll('#contentsList [data-go-to]').length===32`);
  await evaluate(`window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}));true`);
  await evalCheck('BFCache restore revokes consent and hides late titles',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='cover'&&document.querySelectorAll('#contentsList [data-go-to]').length===10`);
  await evaluate(`localStorage.setItem('book-tiktok.solaris.lastScreen','obsolete-id');true`);await load();
  await evalCheck('Removed legacy ID falls back safely',`!document.querySelector('[data-start="continue"]')&&document.querySelector('[data-start="begin"]')`);
  await click('[data-start="begin"]');
  await evaluate(`document.activeElement?.blur();true`);await key('ArrowRight');
  await evalCheck('Native ArrowRight advances',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='broken-welcome'`);
  await key(' ','Space');
  await evalCheck('Native Space advances',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='solaristics-library'`);
  await click('#nextButton');await key('f','KeyF');
  await evalCheck('Focus after Next hides header and preserves Next',`document.documentElement.getAttribute('data-focus-mode')==='true'&&getComputedStyle(document.querySelector('#nextButton')).display!=='none'`);
  await key('Escape');
  await evalCheck('Escape restores reading chrome',`!document.documentElement.hasAttribute('data-focus-mode')`);
  const before=await evaluate(`document.querySelector('#desktopContentsList .is-active').dataset.goTo`);
  await cdp('Page.bringToFront');await shot('gesture-before');
  await cdp('Input.dispatchMouseEvent',{type:'mousePressed',x:290,y:300,button:'left',buttons:1,clickCount:1});
  await cdp('Input.dispatchMouseEvent',{type:'mouseMoved',x:110,y:303,button:'left',buttons:1});
  await cdp('Input.dispatchMouseEvent',{type:'mouseReleased',x:110,y:303,button:'left',buttons:0,clickCount:1});await delay(80);
  const after=await evaluate(`document.querySelector('#desktopContentsList .is-active').dataset.goTo`);
  if(before===after)throw new Error('Native pointer drag did not advance');result.checks.push('Native horizontal pointer drag');
  await evalCheck('Vertical pointer gesture does not page or toggle focus',`(()=>{
    const before=document.querySelector('#desktopContentsList .is-active').dataset.goTo;
    const story=document.querySelector('#story');
    story.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true,pointerId:99,pointerType:'touch',clientX:150,clientY:350}));
    story.dispatchEvent(new PointerEvent('pointerup',{bubbles:true,pointerId:99,pointerType:'touch',clientX:153,clientY:170}));
    return before===document.querySelector('#desktopContentsList .is-active').dataset.goTo&&!document.documentElement.hasAttribute('data-focus-mode');
  })()`);
  await cdp('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:1});
  await shot('touch-before');
  const touchBefore=await evaluate(`document.querySelector('#desktopContentsList .is-active').dataset.goTo`);
  await cdp('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:290,y:300}]});
  await cdp('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:110,y:303}]});
  await cdp('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await delay(80);
  const touchAfter=await evaluate(`document.querySelector('#desktopContentsList .is-active').dataset.goTo`);
  if(touchBefore===touchAfter)throw new Error('Native horizontal touch did not advance');
  result.checks.push('Native horizontal touch swipe after compositor frame');
  await evaluate('window.getSelection().removeAllRanges();true');
  for(const expected of [true,false]){
    await shot('tap-before');
    const point=await evaluate(`(()=>{const r=document.querySelector('#story .slide-scroll > p:not(.kicker)').getBoundingClientRect();return {x:r.x+12,y:r.y+12};})()`);
    await cdp('Input.dispatchMouseEvent',{type:'mousePressed',...point,button:'left',buttons:1,clickCount:1});
    await cdp('Input.dispatchMouseEvent',{type:'mouseReleased',...point,button:'left',buttons:0,clickCount:1});
    await evalCheck('Native text tap focus '+expected,`(document.documentElement.getAttribute('data-focus-mode')==='true')===${expected}`);
  }

  await click('[data-go-to="final"]');await click('#nextButton');
  await evalCheck('Restart clears saved position',`document.querySelector('#desktopContentsList .is-active').dataset.goTo==='cover'&&!localStorage.getItem('book-tiktok.solaris.lastScreen')`);
  await evalCheck('Consent never persisted',`!Object.keys(localStorage).some(k=>/consent|spoiler/i.test(k))`);
  await shot('restart-cover');
} else if(phase==='visual'){
  await evaluate(`const css=document.createElement('style');css.textContent='*,*::before,*::after{animation:none!important;transition:none!important}';document.head.append(css);document.querySelector('[data-mode="deep"]').click();true`);
  await shot('consent-ru-dark-320');
  await evaluate(`document.querySelector('#solarisSpoilerAccept').click();document.querySelector('[data-go-to="oxygen-attempt"]').click();true`);await shot('oxygen-ru-dark-320');
  await evaluate(`document.querySelector('[data-go-to="cruel-expectation"]').click();true`);await shot('ending-ru-dark-320');
  await evaluate(`document.querySelector('[data-go-to="final"]').click();true`);await shot('final-ru-dark-320');
  result.checks.push('Representative dark RU prose, ending, shared final and consent captured for visual inspection');
} else {
  await cdp('Network.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1'});
  for(const [w,h] of [[320,568],[390,844]]){
    await cdp('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:true});
    await evaluate('sessionStorage.clear();true');await load();await delay(100);
    for(const language of ['ru','en']){
    await evaluate(`document.querySelectorAll('dialog[open]').forEach(d=>d.close());if(document.documentElement.lang!==${JSON.stringify(language)})document.querySelector('#languageButton').click();document.querySelector('#bookLibraryInstallTrigger').click();true`);
    const details=await evaluate(`(()=>{
      const d=document.querySelector('#bookLibraryInstallDialog');
      if(!d.open)document.querySelector('#bookLibraryInstallTrigger').click();
      const r=d.getBoundingClientRect(),title=document.querySelector('#bookLibraryInstallTitle').getBoundingClientRect();
      const buttons=[...document.querySelectorAll('.topbar a,.topbar button')].map(x=>({id:x.id,x:x.getBoundingClientRect().x,y:x.getBoundingClientRect().y,right:x.getBoundingClientRect().right}));
      const text=d.textContent;return {language:document.documentElement.lang,title:document.querySelector('#bookLibraryInstallTitle').textContent,open:d.open,scrollTop:d.scrollTop,titleTop:title.top,top:r.top,right:r.right,buttons,hasRoute:/Safari/.test(text)};
    })()`);
    if(!details.open||details.right>w+1||!details.hasRoute||details.titleTop<details.top||details.buttons.length!==6||details.buttons.some(b=>b.right>w+1||b.y!==details.buttons[0].y))throw new Error('iOS guide geometry '+JSON.stringify(details));
    result.checks.push({viewport:[w,h],guide:details});await shot('ios-'+w+(language==='en'?'-en':''));
    await evaluate(`document.querySelector('#bookLibraryInstallDialog').close();true`);
    }
  }
  await cdp('Page.addScriptToEvaluateOnNewDocument',{source:"Object.defineProperty(navigator,'standalone',{get:()=>true});"});
  await load();
  const standalone=await evaluate(`document.querySelector('#bookLibraryInstallTrigger').hidden&&!document.querySelector('#bookLibraryInstallDialog').open`);
  if(!standalone)throw new Error('Standalone guide visible');result.checks.push('Emulated standalone hides guide');
}
result.errors=errors;result.externalRuntimeRequests=requests;result.chromeProfileRemovedAfterRun=profile;
if(errors.length||requests.length)throw new Error('Runtime/network '+JSON.stringify({errors,requests}));
fs.writeFileSync(path.join(output,phase+'.json'),JSON.stringify(result,null,2)+'\n');
cleanup();
if(fs.existsSync(profile))throw new Error('Chrome profile survived cleanup');
console.log(JSON.stringify({phase,visits:result.visits,checks:result.checks.length,errors:errors.length,requests:requests.length,cleaned:true}));
