import fs from 'node:fs';
import {createHash} from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';
import { spawn } from 'node:child_process';
import { pathToFileURL,fileURLToPath } from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const phase=process.argv[2]||'320';
const widths={320:568,390:844,1024:768,1440:900};
const width=Number(phase)||390,height=widths[width]||844;
const out=path.join(dir,'qa');fs.mkdirSync(out,{recursive:true});
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'lost-world-depth-v2-'));
const key='book-tiktok.the-lost-world.depth-v2.';
let chrome,ws,cleaned=false,seq=0;const pending=new Map(),errors=[],remote=[];
function cleanup(){if(cleaned)return;cleaned=true;try{ws?.close()}catch{}if(chrome?.pid)try{process.kill(-chrome.pid,'SIGKILL')}catch{}fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:60});}
process.on('exit',cleanup);process.on('SIGINT',()=>{cleanup();process.exit(130)});process.on('SIGTERM',()=>{cleanup();process.exit(143)});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const portProbe=net.createServer();await new Promise(r=>portProbe.listen(0,'127.0.0.1',r));const port=portProbe.address().port;await new Promise(r=>portProbe.close(r));
chrome=spawn('/usr/bin/timeout',['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows','--no-first-run','--no-default-browser-check','--allow-file-access-from-files',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,'about:blank'],{detached:true,stdio:'ignore'});
let report={phase,width,height,timeoutSeconds:30,contentServerStarted:false,inputHashes:Object.fromEntries(['the-lost-world.html','story-data.json'].map(n=>[n,createHash('sha256').update(fs.readFileSync(path.join(dir,n))).digest('hex')]))};
try{
 let target;for(let i=0;i<100&&!target;i++){try{target=(await(await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(x=>x.type==='page')}catch{}if(!target)await pause(40)}if(!target)throw Error('Chrome did not start');
 ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.requestWillBeSent'&&/^https?:/.test(m.params.request.url))remote.push(m.params.request.url)};
 const cmd=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error(method+' timeout'))},20000);pending.set(id,{resolve:v=>{clearTimeout(timer);resolve(v)},reject:e=>{clearTimeout(timer);reject(e)}});ws.send(JSON.stringify({id,method,params}));});
 const ev=async expression=>{report.lastEvaluate=expression.slice(0,240);const r=await cmd('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value};
 const assert=(v,label)=>{if(!v)throw Error(label)};
 const load=async()=>{
  await cmd('Page.navigate',{url:pathToFileURL(path.join(dir,'the-lost-world.html')).href});
  for(let i=0;i<100;i++){if(await ev(`document.readyState==='complete'&&!!document.querySelector('[data-start]')&&!!window.BookSettings`))break;await pause(35)}
  await ev(`document.fonts.ready.then(()=>true)`);
 };
 await cmd('Page.enable');await cmd('Runtime.enable');await cmd('Network.enable');
 await cmd('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:-1,uploadThroughput:-1});
 await cmd('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<600});
 await cmd('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 await load();await cmd('Page.bringToFront');
 const defaults=await ev(`({language:document.documentElement.lang,theme:document.documentElement.dataset.theme,font:BookSettings.get().readingFont,mode:document.querySelector('[data-mode].is-active')?.dataset.mode})`);
 assert(defaults.language==='ru'&&defaults.theme==='dark'&&defaults.font==='sans'&&defaults.mode==='essential','defaults');report.defaults=defaults;
 const data=JSON.parse(fs.readFileSync(path.join(dir,'story-data.json'),'utf8'));
 const click=async id=>ev(`document.querySelector('#contentsList [data-go-to="${id}"]').click()`);
 const enter=async()=>ev(`document.querySelector('#dialogModePicker [data-mode="deep"]').click();if(document.getElementById('deepConsentDialog').open)document.getElementById('confirmDeep').click()`);
 if(phase==='consent'){
  report.cancel=await ev(`(()=>{document.querySelector('[data-mode="deep"]').click();const r={open:deepConsentDialog.open,cancelFocused:document.activeElement.id==='cancelDeep',stillEssential:document.querySelector('#dialogModePicker .is-active').dataset.mode==='essential'};cancelDeep.click();return r})()`);assert(Object.values(report.cancel).every(Boolean),'cancel');
  report.downgrades=[];
  for(const lang of ['ru','en'])for(const lower of ['essential','core']){
   await ev(`if(document.documentElement.lang!=='${lang}')languageButton.click()`);await enter();await click('hand');
   const r=await ev(`(()=>{document.querySelector('#dialogModePicker [data-mode="${lower}"]').click();const before=story.textContent,b=document.querySelector('[data-start="continue"]'),generic=/спойлер|spoiler/i.test(b?.textContent||'');b.click();const r={generic,open:deepConsentDialog.open,unchanged:story.textContent===before,modeUnchanged:document.querySelector('#dialogModePicker .is-active').dataset.mode==='${lower}'};cancelDeep.click();b.click();confirmDeep.click();r.destination=story.querySelector('h1').textContent===JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s=>s.id==='hand').copy.${lang}.title;document.querySelector('#dialogModePicker [data-mode="${lower}"]').click();document.querySelector('#dialogModePicker [data-mode="deep"]').click();r.pickerAsks=deepConsentDialog.open;cancelDeep.click();return r})()`);
   report.downgrades.push({lang,lower,...r});assert(Object.values(r).every(Boolean),'actual downgrade '+JSON.stringify(r));
  }
  // A real downgrade at a scene shared with Core also revokes consent.
  await enter();await click('iguanodons');
  report.sharedSceneDowngrade=await ev(`(()=>{document.querySelector('#dialogModePicker [data-mode="core"]').click();const preserved=localStorage.getItem('${key}lastScreen')==='iguanodons';document.querySelector('#dialogModePicker [data-mode="deep"]').click();const asks=deepConsentDialog.open;cancelDeep.click();return{preserved,asks}})()`);assert(Object.values(report.sharedSceneDowngrade).every(Boolean),'shared scene downgrade');
  report.reloads=[];
  for(const lang of ['ru','en'])for(const lower of ['essential','core','deep']){
   await ev(`localStorage.setItem('${key}language','${lang}');localStorage.setItem('${key}mode','${lower}');localStorage.setItem('${key}lastScreen','potts')`);await load();
   const r=await ev(`(()=>{const b=document.querySelector('[data-start="continue"]'),before=story.textContent,r={generic:/спойлер|spoiler/i.test(b.textContent),safe:!contentsList.textContent.includes('At the door')&&!contentsList.textContent.includes('У двери'),mode:document.querySelector('#dialogModePicker .is-active').dataset.mode};b.click();r.open=deepConsentDialog.open;r.unchanged=before===story.textContent;confirmDeep.click();r.destination=localStorage.getItem('${key}lastScreen')==='potts';return r})()`);
   report.reloads.push({lang,savedMode:lower,...r});assert(r.generic&&r.safe&&r.open&&r.unchanged&&r.destination&&r.mode===(lower==='deep'?'essential':lower),'fresh reload');
  }
  report.lifecycle=await ev(`(()=>{window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}));window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}));const safe=document.querySelector('#dialogModePicker .is-active').dataset.mode==='essential';document.querySelector('[data-start="continue"]').click();const asks=deepConsentDialog.open;cancelDeep.click();return{safe,asks,scope:'pagehide/pageshow BFCache lifecycle events dispatched in Chrome; not a physical Safari cache test'}})()`);assert(report.lifecycle.safe&&report.lifecycle.asks,'BFCache lifecycle');
  await click('final');await ev(`document.querySelector('[data-open-deep]').click()`);assert(await ev(`deepConsentDialog.open`),'final asks');
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await pause(80);assert(await ev(`!deepConsentDialog.open`),'Escape consent');
  await ev(`document.querySelector('[data-open-deep]').click();confirmDeep.click()`);assert(await ev(`localStorage.getItem('${key}lastScreen')==='deep-warning'`),'explicit target');
  await click('shotgun');
  report.interactions=await ev(`(()=>{const r={};languageButton.click();r.languageId=localStorage.getItem('${key}lastScreen')==='shotgun';const el=story.querySelector('.slide-scroll');el.scrollTop=70;const top=el.scrollTop;BookSettings.set('theme','light');BookSettings.set('readingFont','serif');r.settingsId=localStorage.getItem('${key}lastScreen')==='shotgun';r.settingsScroll=el===story.querySelector('.slide-scroll')&&el.scrollTop===top;document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}));r.focusOn=document.documentElement.dataset.focusMode==='true';nextButton.click();r.focusPaging=document.documentElement.dataset.focusMode==='true';document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));r.focusOff=!document.documentElement.hasAttribute('data-focus-mode');document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));r.keyboard=localStorage.getItem('${key}lastScreen')==='shotgun';story.dispatchEvent(new PointerEvent('pointerdown',{pointerId:9,clientX:260,clientY:220,bubbles:true}));story.dispatchEvent(new PointerEvent('pointerup',{pointerId:9,clientX:100,clientY:220,bubbles:true}));r.swipe=localStorage.getItem('${key}lastScreen')==='asphalt';return r})()`);assert(Object.values(report.interactions).every(Boolean),'interactions '+JSON.stringify(report.interactions));
  await ev(`themeButton.click()`);assert(await ev(`bookSettingsDialog.open`),'settings modal');
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  report.settingsFocusContained=await ev(`bookSettingsDialog.contains(document.activeElement)`);assert(report.settingsFocusContained,'settings Tab');
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});await pause(80);
  report.settingsFocusReturned=await ev(`!bookSettingsDialog.open&&document.activeElement.id==='themeButton'`);assert(report.settingsFocusReturned,'settings focus return');
  await ev(`sourcesButton.click()`);assert(await ev(`sourcesDialog.open`),'sources');await ev(`sourcesDialog.close();contentsButton.click()`);assert(await ev(`contentsDialog.open`),'contents');await ev(`contentsDialog.close()`);
  await click('final');await ev(`nextButton.click()`);assert(await ev(`!localStorage.getItem('${key}lastScreen')`),'restart clears');
  await ev(`localStorage.setItem('${key}lastScreen','invalid-old-id')`);await load();await ev(`document.querySelector('[data-start="begin"]').click()`);report.invalidIdStarts=await ev(`localStorage.getItem('${key}lastScreen')==='money'`);assert(report.invalidIdStarts,'invalid saved ID');
  report.globalPreferencesAfterReload=await ev(`({theme:BookSettings.get().theme,font:BookSettings.get().readingFont,storage:JSON.parse(localStorage.getItem('bookLibrary.preferences.v1'))})`);assert(report.globalPreferencesAfterReload.theme==='light'&&report.globalPreferencesAfterReload.font==='serif','global preferences survive reload');
  report.consentKeys=await ev(`Object.keys(localStorage).filter(k=>/consent/i.test(k))`);assert(!report.consentKeys.length,'no stored consent');
  report.oldNamespaceUntouched=await ev(`Object.keys(localStorage).filter(k=>k.startsWith('book-tiktok.the-lost-world.')&&!k.startsWith('${key}')).length===0`);assert(report.oldNamespaceUntouched,'old progress untouched');
 }else{
  report.cases=[];
  for(const lang of ['ru','en'])for(const theme of ['light','dark'])for(const font of ['sans','serif']){
   await ev(`if(document.documentElement.lang!=='${lang}')languageButton.click();BookSettings.set('theme','${theme}');BookSettings.set('readingFont','${font}')`);await enter();await ev(`document.fonts.ready.then(()=>true)`);
   for(const id of ['cover','chalk-arrows','night-pride','empty-camp','capture-shot','bark','potts','final']){
    await click(id);
    const r=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),s=d.screens.find(s=>s.id==='${id}'),sc=story.querySelector('.slide-scroll'),norm=x=>x.replace(/\\s+/g,' ').trim(),tmp=document.createElement('div');tmp.innerHTML=s.copy.${lang}.body;sc.scrollTop=sc.scrollHeight;return{title:story.querySelector('h1').textContent===s.copy.${lang}.title,body:norm(story.textContent).includes(norm(tmp.textContent)),noOverflow:document.documentElement.scrollWidth<=innerWidth+1&&sc.scrollWidth<=sc.clientWidth+1,bottom:sc.scrollHeight-sc.clientHeight-sc.scrollTop<2,noAcademicChrome:!story.querySelector('.source-label')}})()`);
    report.cases.push({lang,theme,font,id,...r});assert(Object.values(r).every(Boolean),'layout '+JSON.stringify(report.cases.at(-1)));
   }
   if((lang==='ru'&&theme==='light'&&font==='serif')||(lang==='en'&&theme==='dark'&&font==='sans')){
    await click('shotgun');await ev(`document.fonts.ready.then(()=>true)`);await ev(`new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);await pause(160);const shot=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,`${phase}-${lang}-${theme}-${font}.png`),Buffer.from(shot.data,'base64'));
   }
  }
  report.header=await ev(`(()=>{const bar=document.querySelector('.topbar'),a=bar.getBoundingClientRect(),bs=[...bar.querySelectorAll('a,button')].filter(b=>!b.hidden&&getComputedStyle(b).display!=='none');return{controls:bs.length,oneRow:Math.max(...bs.map(b=>b.getBoundingClientRect().top))-Math.min(...bs.map(b=>b.getBoundingClientRect().top))<2,inside:bs.every(b=>{const r=b.getBoundingClientRect();return r.left>=a.left-1&&r.right<=a.right+1&&r.top>=a.top-1&&r.bottom<=a.bottom+1}),iconLabels:bs.every(b=>b.querySelector('[data-reader-icon]')&&!b.textContent.trim()&&b.getAttribute('aria-label')),rail:getComputedStyle(desktopRail).display!=='none'}})()`);assert(report.header.oneRow&&report.header.inside&&report.header.iconLabels&&report.header.rail===(width>=900),'header');
  await cmd('DOM.enable');await cmd('CSS.enable');report.fonts=[];
  for(const lang of ['ru','en'])for(const font of ['sans','serif']){
   await ev(`if(document.documentElement.lang!=='${lang}')languageButton.click();BookSettings.set('readingFont','${font}')`);await click('shotgun');await ev(`document.fonts.ready.then(()=>true)`);
   const root=await cmd('DOM.getDocument',{depth:0}),node=await cmd('DOM.querySelector',{nodeId:root.root.nodeId,selector:'#story .slide-scroll > p:not(.kicker)'}),actual=await cmd('CSS.getPlatformFontsForNode',{nodeId:node.nodeId});
   report.fonts.push({lang,font,actual:actual.fonts});assert(actual.fonts.some(x=>x.isCustomFont&&x.glyphCount>0&&(font==='sans'?/Geist/.test(x.familyName):lang==='ru'?/Source Serif/.test(x.familyName):/Geist Serif/.test(x.familyName))),'font');
  }
  await click('shotgun');
  report.denseScroll=await ev(`(()=>{const el=story.querySelector('.slide-scroll'),p=el.querySelector('p:last-child'),t=p.lastChild;el.scrollTop=el.scrollHeight;const range=document.createRange();range.setStart(t,t.textContent.length-1);range.setEnd(t,t.textContent.length);const r=range.getBoundingClientRect(),b=el.getBoundingClientRect();return{scrollTop:el.scrollTop,clientHeight:el.clientHeight,scrollHeight:el.scrollHeight,lastCharacterVisible:r.top>=b.top-1&&r.bottom<=b.bottom+1}})()`);assert(report.denseScroll.lastCharacterVisible,'dense scroll end');
  if(width===390){
   report.routes=[];
   for(const lang of ['ru','en'])for(const [mode,level]of Object.entries({essential:1,core:2,deep:3})){
    const r=await ev(`(()=>{if(document.documentElement.lang!=='${lang}')languageButton.click();document.querySelector('#dialogModePicker [data-mode="${mode}"]').click();if(deepConsentDialog.open)confirmDeep.click();const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),ss=d.screens.filter(s=>s.level<=${level}),ids=[...contentsList.querySelectorAll('[data-go-to]')].map(b=>b.dataset.goTo),bad=[];if(ids.join('|')!==ss.map(s=>s.id).join('|'))bad.push('route');for(const s of ss){contentsList.querySelector('[data-go-to="'+s.id+'"]').click();if(story.querySelector('h1')?.textContent!==s.copy.${lang}.title)bad.push(s.id);const sc=story.querySelector('.slide-scroll');if(sc.scrollWidth>sc.clientWidth+1)bad.push(s.id+':overflow')}const maps=sourcesList.querySelector('details')?.querySelectorAll('li');if(maps?.length!==ss.filter(s=>s.evidenceLocator).length)bad.push('map');if('${mode}'!=='deep'){const t=contentsList.textContent+sourcesList.textContent;for(const s of d.screens.filter(s=>s.level===3))if(t.includes(s.copy.${lang}.title))bad.push(s.id+':leak')}return{mode:'${mode}',lang:'${lang}',count:ss.length,bad}})()`);
    report.routes.push(r);assert(!r.bad.length,'route '+JSON.stringify(r));
   }
  }
  await ev(`BookSettings.set('theme','light');BookSettings.set('readingFont','serif');if(document.documentElement.lang!=='ru')languageButton.click()`);await click('cover');await ev(`document.querySelector('.slide-scroll').scrollTop=0`);
  await ev(`new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);await pause(160);const shot=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,`${phase}-cover.png`),Buffer.from(shot.data,'base64'));
 }
 assert(!errors.length&&!remote.length,'runtime/network '+JSON.stringify({errors,remote}));report.runtimeErrors=errors;report.remoteRequests=remote;report.status='completed';
}catch(e){report.status='failed';report.error=e.stack;process.exitCode=1;}
finally{cleanup();await pause(120);let alive=false;try{process.kill(-chrome.pid,0);alive=true}catch{}report.profileRemoved=!fs.existsSync(profile);report.ownedProcessGroupAliveAfterCleanup=alive;fs.writeFileSync(path.join(out,`browser-${phase}.json`),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({phase,status:report.status,cases:report.cases?.length,error:report.error,profileRemoved:report.profileRemoved,ownedProcessGroupAliveAfterCleanup:alive}));}
