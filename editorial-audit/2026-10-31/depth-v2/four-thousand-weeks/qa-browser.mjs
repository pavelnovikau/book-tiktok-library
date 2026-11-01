import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import os from 'node:os';
import {spawn} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const phase=process.argv[2]||'cold';
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'four-thousand-weeks-qa-'));
const chrome=spawn('/opt/homebrew/bin/timeout',['--foreground','30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--disable-background-networking','--disable-component-update','--disable-sync','--metrics-recording-only','--disable-extensions','--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank'],{detached:true,stdio:['ignore','ignore','pipe']});
let socket,stderr='',seq=0;const pending=new Map(),events=[];chrome.stderr.on('data',x=>stderr+=x);
const delay=ms=>new Promise(r=>setTimeout(r,ms));
function command(method,params={}) {return new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});}
async function ev(expression){const r=await command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
async function click(selector){return ev(`document.querySelector(${JSON.stringify(selector)}).click()`);}
const result={inputHtmlSha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'four-thousand-weeks.html'))).digest('hex'),phase,startedAt:new Date().toISOString(),checks:[],failures:[],runtimeErrors:[],remoteRequests:[],profile};
function check(name,ok,detail){result.checks.push({name,pass:!!ok,detail});if(!ok)result.failures.push({name,detail});}
try{
 let port;for(let i=0;i<100;i++){try{port=fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').split('\n')[0];break;}catch{}await delay(50);}if(!port)throw Error('No CDP port '+stderr.slice(-500));
 const targets=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();socket=new WebSocket(targets.find(x=>x.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{socket.onopen=r;socket.onerror=j;});socket.onmessage=({data})=>{const x=JSON.parse(data);if(x.id){const p=pending.get(x.id);pending.delete(x.id);if(x.error)p.reject(Error(JSON.stringify(x.error)));else p.resolve(x.result);}else{events.push(x);if(x.method==='Runtime.exceptionThrown')result.runtimeErrors.push(x.params.exceptionDetails);if(x.method==='Network.requestWillBeSent'&&/^https?:/.test(x.params.request.url))result.remoteRequests.push(x.params.request.url);}};
 await command('Runtime.enable');await command('Page.enable');await command('Network.enable');await command('Network.setBlockedURLs',{urls:['http://*','https://*']});await command('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 const url=pathToFileURL(path.join(root,'four-thousand-weeks.html')).href;
 async function load(){await command('Page.navigate',{url});for(let i=0;i<100;i++){try{if(await ev(`document.querySelector('[data-start]') && !!window.BookSettings`))break;}catch{}await delay(30);}await ev('document.fonts.ready.then(()=>true)');}
 async function screenshot(name){const r=await command('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(root,name),Buffer.from(r.data,'base64'));}
 const width=Number(phase)||320,height=width===320?568:width===390?844:width===1024?768:900;
 await command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<500});if(phase==='ios')await command('Emulation.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1',platform:'iPhone'});await load();
 if(phase==='cold'){
  check('fresh default RU dark Essential Sans',await ev(`document.documentElement.lang==='ru' && document.documentElement.dataset.theme==='dark' && document.documentElement.dataset.readingFont==='sans' && document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true'`));
  // The first switch to Serif occurs at a genuine, measured nonzero scroll.
  await click('[data-start]');await ev(`document.querySelector('.slide-scroll').scrollTop=120`);
  const before=await ev(`({top:document.querySelector('.slide-scroll').scrollTop,id:localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen'),fontFaces:[...document.fonts].map(x=>[x.family,x.status])})`);
  check('cold Serif starts at real nonzero scroll',before.top>0,before);
  await click('#themeButton');await click('input[name="book-font"][value="serif"]');
  for(let i=0;i<60;i++){if(await ev(`document.documentElement.dataset.readingFont==='serif'`))break;await delay(20);}
  await click('#bookSettingsClose');
  const after=await ev(`({top:document.querySelector('.slide-scroll').scrollTop,id:localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen'),font:document.documentElement.dataset.readingFont})`);
  check('first cold Serif preserves scroll and passage',after.font==='serif'&&Math.abs(after.top-before.top)<1&&after.id===before.id,{before,after});
  await screenshot('qa-cold-serif-320.png');
  await command('DOM.enable');await command('CSS.enable');const doc=await command('DOM.getDocument');const node=await command('DOM.querySelector',{nodeId:doc.root.nodeId,selector:'#story .slide-scroll > p:not(.kicker):not(.source-label)'});result.actualRussianParagraphFonts=await command('CSS.getPlatformFontsForNode',{nodeId:node.nodeId});
  check('Cyrillic actual Serif fallback',result.actualRussianParagraphFonts.fonts.some(x=>/Source Serif 4/.test(x.familyName)),result.actualRussianParagraphFonts);
  await click('#themeButton');const position=after.id;await ev(`document.querySelector('input[name="book-font"][value="serif"]').focus()`);
  await command('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowLeft',code:'ArrowLeft',windowsVirtualKeyCode:37});await command('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowLeft',code:'ArrowLeft',windowsVirtualKeyCode:37});await delay(50);
  check('Settings arrow keys select radio without paging',await ev(`document.querySelector('input[name="book-font"][value="sans"]').checked && localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen')===${JSON.stringify(position)}`));
  await ev(`document.querySelector('input[name="book-theme"][value="dark"]').focus()`);await command('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});await command('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});
  check('Settings theme ArrowRight',await ev(`document.documentElement.dataset.theme==='light' && document.querySelector('input[name="book-theme"][value="light"]').checked`));
  await command('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await command('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await delay(30);
  check('Escape and focus return',await ev(`!document.querySelector('#bookSettingsDialog').open && document.activeElement.id==='themeButton'`));
  await ev(`BookSettings.set('readingFont','serif')`);await click('#languageButton');await delay(60);const docEn=await command('DOM.getDocument');const nodeEn=await command('DOM.querySelector',{nodeId:docEn.root.nodeId,selector:'#story .slide-scroll > p:not(.kicker):not(.source-label)'});result.actualEnglishParagraphFonts=await command('CSS.getPlatformFontsForNode',{nodeId:nodeEn.nodeId});check('Latin actual Geist Serif',result.actualEnglishParagraphFonts.fonts.some(x=>/Geist Serif/.test(x.familyName)),result.actualEnglishParagraphFonts);
 } else if(phase==='ios'){
  await delay(500);check('emulated iOS guide automatically opens',await ev(`document.querySelector('#bookLibraryInstallDialog').open && !document.querySelector('#bookLibraryInstallTrigger').hidden`));await click('#bookLibraryInstallClose');await click('#languageButton');await click('#bookLibraryInstallTrigger');check('guide localizes and contains actual add-home path',await ev(`document.querySelector('#bookLibraryInstallDialog').textContent.includes('Add to Home Screen') && document.querySelector('#bookLibraryInstallDialog').textContent.includes('cannot hide')`));await click('#bookLibraryInstallClose');
  await ev(`document.documentElement.style.setProperty('--reader-safe-top','44px')`);await delay(40);
  const header=await ev(`Array.from(document.querySelectorAll('.topbar a,.topbar button')).filter(n=>!n.hidden).map(n=>({id:n.id,rect:n.getBoundingClientRect().toJSON(),svg:!!n.querySelector('svg')}))`);check('emulated nonzero safe inset, six icon controls in one reachable row',header.length===6&&header.every(n=>n.svg&&n.rect.top>=44&&n.rect.right<=320)&&Math.max(...header.map(n=>n.rect.top))-Math.min(...header.map(n=>n.rect.top))<2,header);
  await click('[data-start]');await ev(`document.activeElement.blur();document.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}))`);check('focus hides iOS install trigger',await ev(`getComputedStyle(document.querySelector('#bookLibraryInstallTrigger')).display==='none'`));await ev(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))`);
  await command('Page.addScriptToEvaluateOnNewDocument',{source:`Object.defineProperty(navigator,'standalone',{get:()=>true})`});await load();await delay(500);check('emulated standalone suppresses guide and trigger',await ev(`!document.querySelector('#bookLibraryInstallDialog').open && document.querySelector('#bookLibraryInstallTrigger').hidden`));
 } else if(phase==='interaction'){
  await ev(`localStorage.clear();localStorage.setItem('book-tiktok.four-thousand-weeks.lastScreen','doing-nothing');localStorage.setItem('book-tiktok.four-thousand-weeks.mode','deep');localStorage.setItem('book-tiktok.four-thousand-weeks.language','en');localStorage.setItem('book-tiktok.four-thousand-weeks.theme','light')`);await load();
  check('actual legacy old id cannot resume or change depth/language',await ev(`document.documentElement.lang==='ru' && document.querySelector('[data-start]').dataset.start==='begin' && document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true' && localStorage.getItem('book-tiktok.four-thousand-weeks.lastScreen')==='doing-nothing'`));
  await click('[data-mode="deep"]');await click('[data-start="begin"]');await click('#contentsButton');await click('#contentsList [data-go-to="part-09-passage-01"]');
  check('genuine deeper position saved',await ev(`localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen')==='part-09-passage-01'`));
  await load();check('reload retains explicit chosen Deep',await ev(`document.querySelector('[data-mode="deep"]').getAttribute('aria-pressed')==='true' && document.querySelector('[data-start="continue"]')`));
  await click('[data-mode="essential"]');check('lower depth Continue visibly names Deep target',await ev(`document.querySelector('[data-start="continue"]').textContent.includes('Глубоко') && document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true'`));
  await load();check('real lower-depth reload stays Essential with named deeper Continue',await ev(`document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true' && document.querySelector('[data-start="continue"]').textContent.includes('Глубоко')`));
  await click('#languageButton');check('EN deeper Continue names Deep',await ev(`document.querySelector('[data-start="continue"]').textContent.includes('Continue in Deep')`));await click('[data-start="continue"]');
  check('Continue enters named deeper route and saved passage',await ev(`document.querySelector('#story h1').textContent==='Shinzen Young’s account' && localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.mode')==='deep' && !document.querySelector('dialog[open]')`));
  await click('#languageButton');check('language switch preserves current passage',await ev(`document.querySelector('#story h1').textContent==='Рассказ Шинзена Янга'`));
  await click('#sourcesButton');check('Sources method opens and declares RU edition',await ev(`document.querySelector('#sourcesDialog').open && document.querySelector('#sourcesList').textContent.includes('2023')`));await ev(`document.querySelector('#sourcesDialog').close()`);
  await ev(`document.activeElement.blur();document.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}))`);
  check('focus hides header rail/back but retains Next',await ev(`document.documentElement.dataset.focusMode==='true' && getComputedStyle(document.querySelector('#nextButton')).display!=='none' && getComputedStyle(document.querySelector('#previousButton')).display==='none'`));
  await click('#nextButton');check('focus persists while paging',await ev(`document.documentElement.dataset.focusMode==='true'`));await ev(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))`);
  check('Escape restores normal chrome',await ev(`document.documentElement.dataset.focusMode!=='true'`));
  await click('#contentsButton');await click('#contentsList [data-go-to="part-19-passage-03"]');check('final has restart',await ev(`document.querySelector('#nextButton').textContent==='Сначала'`));await click('#nextButton');check('restart clears current progress only',await ev(`!localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen') && localStorage.getItem('book-tiktok.four-thousand-weeks.lastScreen')==='doing-nothing'`));
  await screenshot('qa-cover-320.png');
  await click('[data-start="begin"]');await ev(`document.activeElement.blur();document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))`);check('reader ArrowRight',await ev(`localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen')==='part-01-passage-02'`));
  await ev(`{const s=document.querySelector('#story');s.dispatchEvent(new PointerEvent('pointerdown',{pointerId:1,clientX:270,clientY:200,bubbles:true}));s.dispatchEvent(new PointerEvent('pointerup',{pointerId:1,clientX:80,clientY:205,bubbles:true}));}`);check('horizontal swipe advances',await ev(`localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen')==='part-01-passage-03'`));
  await ev(`{const s=document.querySelector('#story');s.dispatchEvent(new PointerEvent('pointerdown',{pointerId:2,clientX:150,clientY:300,bubbles:true}));s.dispatchEvent(new PointerEvent('pointerup',{pointerId:2,clientX:152,clientY:100,bubbles:true}));}`);check('vertical gesture does not page',await ev(`localStorage.getItem('book-tiktok.four-thousand-weeks.depth-v2.lastScreen')==='part-01-passage-03'`));
  await command('Input.dispatchMouseEvent',{type:'mousePressed',x:120,y:230,button:'left',clickCount:1});await command('Input.dispatchMouseEvent',{type:'mouseReleased',x:120,y:230,button:'left',clickCount:1});check('real CDP pointer text tap enters focus',await ev(`document.documentElement.dataset.focusMode==='true'`));
  await command('Input.dispatchMouseEvent',{type:'mousePressed',x:120,y:230,button:'left',clickCount:1});await command('Input.dispatchMouseEvent',{type:'mouseReleased',x:120,y:230,button:'left',clickCount:1});check('second real pointer tap restores chrome',await ev(`document.documentElement.dataset.focusMode!=='true'`));
 } else {
  const matrix=await ev(`(async()=>{
    const data=JSON.parse(document.querySelector('#book-tiktok-data').textContent),errors=[],cases=[];let visits=0;
    await Promise.all(['Geist','Geist Serif','Source Serif 4'].map(f=>document.fonts.load('400 16px "'+f+'"','AaЁёЯя')));
    for(const theme of ['dark','light'])for(const font of ['sans','serif'])for(const lang of ['ru','en']){
      BookSettings.set('theme',theme);BookSettings.set('readingFont',font);await document.fonts.ready;
      if(document.documentElement.lang!==lang)document.querySelector('#languageButton').click();
      for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
        document.querySelector('[data-mode="'+mode+'"]').click();
        document.querySelector('#contentsList [data-go-to="cover"]').click();
        const screens=data.screens.filter(s=>s.level<=level);
        for(let i=0;i<screens.length;i++){
          const item=screens[i],h=document.querySelector('#story h1'),scroll=document.querySelector('.slide-scroll');visits++;
          if(!h||h.textContent!==item.copy[lang].title)errors.push({kind:'title',id:item.id,lang,mode});
          if(document.querySelector('#counter').textContent!==(i+1)+' / '+screens.length)errors.push({kind:'counter',id:item.id});
          if(document.documentElement.scrollWidth>innerWidth||scroll.scrollWidth>scroll.clientWidth+1)errors.push({kind:'horizontal',id:item.id,theme,font,lang,mode,width:innerWidth});
          if(item.type!=='cover'){
            const p=[...scroll.querySelectorAll(':scope > p')].filter(p=>!p.matches('.kicker,.source-label'));
            if(p.length!==1||p[0].innerHTML!==new DOMParser().parseFromString(item.copy[lang].body,'text/html').body.querySelector('p').innerHTML)errors.push({kind:'body-parity',id:item.id,lang});
            scroll.scrollTop=scroll.scrollHeight;
            const n=p[0].firstChild,r=document.createRange();r.setStart(n,Math.max(0,n.length-12));r.setEnd(n,n.length);const b=r.getBoundingClientRect(),sb=scroll.getBoundingClientRect();
            if(b.bottom>sb.bottom+1)errors.push({kind:'last-line',id:item.id,bottom:b.bottom,edge:sb.bottom});
          }
          document.querySelector('#nextButton').click();
        }
        cases.push({theme,font,lang,mode,screens:screens.length});
      }
    }
    const controls=[...document.querySelectorAll('.topbar .topbar-group > a, .topbar .topbar-group > button')].map(x=>({id:x.id,rect:x.getBoundingClientRect().toJSON()}));
    return {visits,cases,errors,controls,viewport:[innerWidth,innerHeight],fontStatus:[...document.fonts].map(f=>[f.family,f.status]),railVisible:getComputedStyle(document.querySelector('.desktop-rail')).display!=='none'};
  })()`);
  result.matrix=matrix;check('all RU/EN rendered passages, all depths/themes/fonts, parity/overflow/last-line',matrix.errors.length===0,matrix.errors.slice(0,20));
  if(width>=900)check('desktop rail visible',matrix.railVisible);else check('phone rail hidden',!matrix.railVisible);
  const header=await ev(`Array.from(document.querySelectorAll('.topbar a,.topbar button')).filter(n=>!n.hidden).map(n=>({id:n.id,svg:!!n.querySelector('svg'),label:n.getAttribute('aria-label'),rect:n.getBoundingClientRect().toJSON()}))`);check('icon-only accessible header fits one row',header.every(n=>n.svg&&n.label&&n.rect.left>=0&&n.rect.right<=width&&n.rect.top>=0)&&Math.max(...header.map(n=>n.rect.top))-Math.min(...header.map(n=>n.rect.top))<2,header);
  // Native settings and representative typography screenshot in each viewport.
  await ev(`BookSettings.set('theme','dark');BookSettings.set('readingFont','serif');document.querySelector('[data-mode="deep"]').click();document.querySelector('#contentsList [data-go-to="part-18-passage-01"]').click()`);await delay(80);await screenshot(`qa-dense-${width}.png`);
 }
 check('zero page runtime errors',result.runtimeErrors.length===0,result.runtimeErrors);
 check('zero remote runtime requests',result.remoteRequests.length===0,result.remoteRequests);
}catch(e){result.failures.push({exception:e.stack});}
finally{
 try{socket?.close();}catch{}try{process.kill(-chrome.pid,'SIGTERM');}catch{}await delay(150);try{process.kill(-chrome.pid,'SIGKILL');}catch{}await delay(100);let ownedGroupAlive=false;try{process.kill(-chrome.pid,0);ownedGroupAlive=true;}catch{}fs.rmSync(profile,{recursive:true,force:true});result.profileRemoved=!fs.existsSync(profile);result.ownedGroupTerminated=!ownedGroupAlive;if(ownedGroupAlive)result.failures.push({name:'owned group remains alive'});result.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(root,`qa-browser-${phase}.json`),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({phase,checks:result.checks.length,visits:result.matrix?.visits,failures:result.failures,profileRemoved:result.profileRemoved}));if(result.failures.length)process.exitCode=1;
}
