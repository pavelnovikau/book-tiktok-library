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
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'white-fang-depth-v2-'));
const key='book-tiktok.white-fang.depth-v2.';
let chrome,ws,cleaned=false,seq=0;const pending=new Map(),errors=[],remote=[];
function cleanup(){if(cleaned)return;cleaned=true;try{ws?.close()}catch{}if(chrome?.pid)try{process.kill(-chrome.pid,'SIGKILL')}catch{}fs.rmSync(profile,{recursive:true,force:true,maxRetries:5,retryDelay:60});}
process.on('exit',cleanup);process.on('SIGINT',()=>{cleanup();process.exit(130)});process.on('SIGTERM',()=>{cleanup();process.exit(143)});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const portProbe=net.createServer();await new Promise(r=>portProbe.listen(0,'127.0.0.1',r));const port=portProbe.address().port;await new Promise(r=>portProbe.close(r));
chrome=spawn('/usr/bin/timeout',['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows','--no-first-run','--no-default-browser-check','--allow-file-access-from-files',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,'about:blank'],{detached:true,stdio:'ignore'});
let report={phase,width,height,timeoutSeconds:30,contentServerStarted:false,inputHashes:Object.fromEntries(['white-fang.html','story-data.json'].map(n=>[n,createHash('sha256').update(fs.readFileSync(path.join(dir,n))).digest('hex')]))};
try{
 let target;for(let i=0;i<100&&!target;i++){try{target=(await(await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(x=>x.type==='page')}catch{}if(!target)await pause(40)}if(!target)throw Error('Chrome did not start');
 ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.requestWillBeSent'&&/^https?:/.test(m.params.request.url))remote.push(m.params.request.url)};
 const cmd=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error(method+' timeout'))},20000);pending.set(id,{resolve:v=>{clearTimeout(timer);resolve(v)},reject:e=>{clearTimeout(timer);reject(e)}});ws.send(JSON.stringify({id,method,params}));});
 const ev=async expression=>{report.lastEvaluate=expression.slice(0,240);const r=await cmd('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value};
 const assert=(v,label)=>{if(!v)throw Error(label)};
 const load=async()=>{
  await cmd('Page.navigate',{url:pathToFileURL(path.join(dir,'white-fang.html')).href});
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
 if(phase==='controls'){
  await cmd('Emulation.setDeviceMetricsOverride',{width:320,height:568,deviceScaleFactor:1,mobile:true});
  await ev(`document.documentElement.style.setProperty('--reader-safe-top','30px');document.documentElement.style.setProperty('--reader-safe-right','12px');document.documentElement.style.setProperty('--reader-safe-left','12px');document.querySelector('[data-start="begin"]').click()`);
  await pause(80);report.safeArea=await ev(`(()=>{const bs=[...document.querySelector('.topbar').querySelectorAll('button,a')].filter(x=>!x.hidden&&getComputedStyle(x).display!=='none'),rs=bs.map(b=>b.getBoundingClientRect());return{bounds:rs.map(r=>({x:r.x,y:r.y,w:r.width,h:r.height})),rootScroll:scrollY,safe:getComputedStyle(document.documentElement).getPropertyValue('--reader-safe-top'),padding:getComputedStyle(document.querySelector('.app-header')).paddingTop,count:bs.length,belowInset:rs.every(r=>r.top>=30),inside:rs.every(r=>r.left>=12&&r.right<=innerWidth-12),oneRow:Math.max(...rs.map(r=>r.top))-Math.min(...rs.map(r=>r.top))<2}})()`);
  assert(report.safeArea.count===5&&report.safeArea.belowInset&&report.safeArea.inside&&report.safeArea.oneRow,'safe-area icon row');
  await ev(`document.getElementById('themeButton').click()`);report.tabFocus=[];
  for(let i=0;i<12;i++){
   await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9,nativeVirtualKeyCode:9});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9,nativeVirtualKeyCode:9});
   const r=await ev(`({id:document.activeElement.id,inside:!!document.activeElement.closest('#bookSettingsDialog')})`);report.tabFocus.push(r);assert(r.inside,'Settings native Tab escaped');
  }
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});await pause(60);
  await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await pause(80);report.focusReturned=await ev(`!document.getElementById('bookSettingsDialog').open&&document.activeElement.id==='themeButton'`);assert(report.focusReturned,'Settings focus return');
  await ev(`document.activeElement.blur()`);report.pageKeys=[];
  for(const [key,code,num,id] of [['PageDown','PageDown',34,'i-1-p2'],[' ','Space',32,'i-1-p3'],['PageUp','PageUp',33,'i-1-p2']]){
   await cmd('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:num,nativeVirtualKeyCode:num});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:num,nativeVirtualKeyCode:num});
   const actual=await ev(`localStorage.getItem('book-tiktok.white-fang.depth-v2.lastScreen')`);report.pageKeys.push({key,id,actual});assert(actual===id,'page key '+JSON.stringify(report.pageKeys.at(-1)));
  }
  await cmd('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await ev(`document.documentElement.style.removeProperty('--reader-safe-top');document.querySelector('#dialogModePicker [data-mode="deep"]').click();document.getElementById('confirmDeep').click();document.querySelector('#contentsList [data-go-to="v-5-p6"]').click()`);await pause(600);
  await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});report.rail=await ev(`(()=>{const rail=document.getElementById('desktopContentsList'),a=rail.querySelector('[aria-current="page"]'),r=a.getBoundingClientRect(),b=rail.getBoundingClientRect();return{bounds:{activeTop:r.top,activeBottom:r.bottom,railTop:b.top,railBottom:b.bottom,scrollTop:rail.scrollTop},active:a.dataset.goTo==='v-5-p6',visible:r.top>=b.top-1&&r.bottom<=b.bottom+1,scrollable:rail.scrollHeight>rail.clientHeight}})()`);assert(report.rail.active&&report.rail.visible&&report.rail.scrollable,'desktop rail sync');
 }else if(phase==='tails'){
  report.rows=[];
  await ev(`document.querySelector('#dialogModePicker [data-mode="deep"]').click();document.getElementById('confirmDeep').click()`);
  for(const [w,h] of Object.entries(widths)){
   await cmd('Emulation.setDeviceMetricsOverride',{width:Number(w),height:h,deviceScaleFactor:1,mobile:Number(w)<600});
   for(const lang of ['ru','en'])for(const theme of ['dark','light'])for(const font of ['sans','serif']){
    await ev(`if(document.documentElement.lang!=='${lang}')document.getElementById('languageButton').click();BookSettings.set('theme','${theme}');BookSettings.set('readingFont','${font}')`);
    await ev(`document.fonts.ready.then(()=>true)`);
    const r=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),bad=[];let n=0;for(const s of d.screens.filter(x=>x.narrative)){document.querySelector('#contentsList [data-go-to="'+s.id+'"]').click();const el=document.querySelector('#story .slide-scroll'),p=el.querySelector('p:last-child'),t=p.lastChild;el.scrollTop=el.scrollHeight;const rng=document.createRange();rng.setStart(t,t.textContent.length-1);rng.setEnd(t,t.textContent.length);const r=rng.getBoundingClientRect(),b=el.getBoundingClientRect();if(r.top<b.top-1||r.bottom>b.bottom+1)bad.push(s.id+':last-character');n++;}return{n,bad}})()`);
    report.rows.push({width:w,lang,theme,font,...r});assert(!r.bad.length,'tail '+JSON.stringify(report.rows.at(-1)));
   }
  }
  report.lastCharactersVerified=report.rows.reduce((n,r)=>n+r.n,0);
 }else if(phase==='entries'){
  report.coverPicker=await ev(`(()=>{const b=document.querySelector('#story [data-mode="deep"]'),before=document.getElementById('story').textContent;b.click();const r={open:document.getElementById('deepConsentDialog').open,unchanged:document.getElementById('story').textContent===before};document.getElementById('cancelDeep').click();return r})()`);assert(Object.values(report.coverPicker).every(Boolean),'cover picker');
  report.staleContents=[];
  for(const list of ['contentsList','desktopContentsList'])for(const lower of ['essential','core']){
   const r=await ev(`(()=>{document.querySelector('#dialogModePicker [data-mode="deep"]').click();if(document.getElementById('deepConsentDialog').open)document.getElementById('confirmDeep').click();const stale=document.querySelector('#${list} [data-go-to="v-5-p6"]');document.querySelector('#contentsList [data-go-to="v-5-p3"]').click();document.querySelector('#dialogModePicker [data-mode="${lower}"]').click();const before=document.getElementById('story').textContent;stale.click();const r={open:document.getElementById('deepConsentDialog').open,unchanged:document.getElementById('story').textContent===before,noTitle:!document.getElementById('sourcesList').textContent.includes('Тёплый язык')};document.getElementById('cancelDeep').click();return r})()`);
   report.staleContents.push({list,lower,...r});assert(Object.values(r).every(Boolean),'stale hidden title');
  }
  await ev(`localStorage.clear();localStorage.setItem('book-tiktok.white-fang.mode','deep');localStorage.setItem('book-tiktok.white-fang.language','en');localStorage.setItem('book-tiktok.white-fang.lastScreen','quiet-last-image');localStorage.setItem('book-tiktok.white-fang.consent','true');localStorage.setItem('bookLibrary.preferences.v1',JSON.stringify({version:1,theme:'light',readingFont:'serif'}))`);await load();
  report.legacyIsolation=await ev(`({ru:document.documentElement.lang==='ru',essential:document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode==='essential',cover:!!document.querySelector('[data-start="begin"]'),noContinue:!document.querySelector('[data-start="continue"]'),globalTheme:document.documentElement.dataset.theme==='light',globalFont:BookSettings.get().readingFont==='serif',oldProgressUntouched:localStorage.getItem('book-tiktok.white-fang.lastScreen')==='quiet-last-image'})`);assert(Object.values(report.legacyIsolation).every(Boolean),'old progress/global preferences');
  await ev(`document.querySelector('[data-start="begin"]').click();document.getElementById('nextButton').click()`);
  const saved=await ev(`localStorage.getItem('${key}lastScreen')`);await load();
  report.safeResume=await ev(`(()=>{document.querySelector('[data-start="continue"]').click();return localStorage.getItem('${key}lastScreen')==='${saved}'&&!document.getElementById('deepConsentDialog').open})()`);assert(report.safeResume,'safe position reload');
  await ev(`document.querySelector('#dialogModePicker [data-mode="deep"]').click();document.getElementById('confirmDeep').click();document.querySelector('#contentsList [data-go-to="v-5-p6"]').click()`);await load();
  report.acceptedThenReload=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),text=document.getElementById('story').textContent+document.getElementById('contentsList').textContent+document.getElementById('sourcesList').textContent;const safe=d.screens.filter(s=>s.level===3).every(s=>!text.includes(s.copy.ru.title));document.querySelector('[data-start="continue"]').click();return{safe,open:document.getElementById('deepConsentDialog').open,essential:document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode==='essential'}})()`);assert(Object.values(report.acceptedThenReload).every(Boolean),'consent survives reload');
  const pic=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,'entries-consent.png'),Buffer.from(pic.data,'base64'));
  await ev(`document.getElementById('cancelDeep').click()`);
  report.touchAndFocus=await ev(`(()=>{const r={},s=document.getElementById('story');document.querySelector('#contentsList [data-go-to="i-1-p1"]').click();const key='${key}lastScreen';s.dispatchEvent(new PointerEvent('pointerdown',{pointerId:9,clientX:180,clientY:200,bubbles:true}));s.dispatchEvent(new PointerEvent('pointerup',{pointerId:9,clientX:175,clientY:420,bubbles:true}));r.verticalDoesNotPage=localStorage.getItem(key)==='i-1-p1';document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}));r.headerHidden=getComputedStyle(document.querySelector('.app-header')).display==='none';r.railHidden=getComputedStyle(document.getElementById('desktopRail')).display==='none';r.backHidden=getComputedStyle(document.getElementById('previousButton')).display==='none';r.nextVisible=getComputedStyle(document.getElementById('nextButton')).display!=='none';document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));r.restored=getComputedStyle(document.querySelector('.app-header')).display!=='none';return r})()`);assert(Object.values(report.touchAndFocus).every(Boolean),'vertical gesture/focus');

 }else if(phase==='ios'){
  await cmd('Network.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1'});
  await load();await pause(550);
  report.installBrowser=await ev(`({open:document.getElementById('bookLibraryInstallDialog').open,trigger:!document.getElementById('bookLibraryInstallTrigger').hidden,text:document.getElementById('bookLibraryInstallDialog').textContent})`);
  assert(report.installBrowser.open&&report.installBrowser.trigger&&report.installBrowser.text.includes('Поделиться')&&report.installBrowser.text.includes('На экран Домой'),'iOS install guide');
  await ev(`document.getElementById('bookLibraryInstallClose').click();document.getElementById('languageButton').click();document.getElementById('bookLibraryInstallTrigger').click()`);
  report.installEnglish=await ev(`document.getElementById('bookLibraryInstallDialog').textContent.includes('Add to Home Screen')`);assert(report.installEnglish,'localized guide');
  await ev(`document.getElementById('bookLibraryInstallClose').click();document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}))`);
  report.installFocusHidden=await ev(`getComputedStyle(document.getElementById('bookLibraryInstallTrigger')).display==='none'`);assert(report.installFocusHidden,'focus guide hidden');
  await ev(`document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))`);
  report.iosHeader=await ev(`(()=>{const bar=document.querySelector('.topbar'),a=bar.getBoundingClientRect(),bs=[...bar.querySelectorAll('a,button')].filter(x=>!x.hidden&&getComputedStyle(x).display!=='none');return{count:bs.length,allInside:bs.every(b=>{const r=b.getBoundingClientRect();return r.left>=a.left-1&&r.right<=a.right+1&&r.top>=a.top-1&&r.bottom<=a.bottom+1}),oneRow:Math.max(...bs.map(b=>b.getBoundingClientRect().top))-Math.min(...bs.map(b=>b.getBoundingClientRect().top))<2}})()`);assert(report.iosHeader.count===6&&report.iosHeader.allInside&&report.iosHeader.oneRow,'iOS header');
  await cmd('Page.addScriptToEvaluateOnNewDocument',{source:"Object.defineProperty(navigator,'standalone',{get:()=>true})"});await load();await pause(100);
  report.standalone=await ev(`({guideClosed:!document.getElementById('bookLibraryInstallDialog').open,triggerHidden:document.getElementById('bookLibraryInstallTrigger').hidden})`);assert(report.standalone.guideClosed&&report.standalone.triggerHidden,'standalone guide hidden');
  report.scope='Chrome user-agent/standalone emulation; no physical iPhone, Safari or PWA certification';
 }else if(phase!=='consent'){
  const rows=[];
  for(const lang of ['ru','en'])for(const theme of ['dark','light'])for(const font of ['sans','serif']){
   await ev(`if(document.documentElement.lang!=='${lang}')document.getElementById('languageButton').click();BookSettings.set('theme','${theme}');BookSettings.set('readingFont','${font}')`);
   await ev(`document.fonts.ready.then(()=>true)`);
   for(const mode of ['essential','core','deep']){
    const row=await ev(`(()=>{document.querySelector('#dialogModePicker [data-mode="${mode}"]').click();if(document.getElementById('deepConsentDialog').open)document.getElementById('confirmDeep').click();const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),expected=d.screens.filter(s=>s.level<=${{essential:1,core:2,deep:3}[mode]}),bad=[];const ids=[...document.querySelectorAll('#contentsList [data-go-to]')].map(b=>b.dataset.goTo);if(ids.join('|')!==expected.map(s=>s.id).join('|'))bad.push('route-ids');const norm=x=>x.replace(/\\s+/g,' ').trim();for(const s of expected){document.querySelector('#contentsList [data-go-to="'+s.id+'"]').click();const copy=s.copy.${lang},story=document.getElementById('story');if(story.querySelector('h1')?.textContent!==copy.title)bad.push(s.id+':title');const tmp=document.createElement('div');tmp.innerHTML=copy.body;if(!norm(story.textContent).includes(norm(tmp.textContent)))bad.push(s.id+':body');const expectedParagraphs=[...tmp.querySelectorAll('p')].map(x=>norm(x.textContent));const host=s.type==='cover'?story.querySelector('.cover-copy'):story.querySelector('.slide-scroll');const actualParagraphs=[...host.querySelectorAll(':scope > p:not(.kicker):not(.cover-subtitle)')].filter(x=>!x.querySelector('button')).map(x=>norm(x.textContent));if(JSON.stringify(actualParagraphs)!==JSON.stringify(expectedParagraphs))bad.push(s.id+':paragraph-parity');const scroll=story.querySelector('.slide-scroll');if(document.documentElement.scrollWidth>innerWidth+1||scroll.scrollWidth>scroll.clientWidth+1)bad.push(s.id+':horizontal-overflow');scroll.scrollTop=scroll.scrollHeight;if(scroll.scrollHeight-scroll.clientHeight-scroll.scrollTop>2)bad.push(s.id+':tail-scroll');if(story.querySelector('.source-label'))bad.push(s.id+':academic-chrome');const sourceMap=document.querySelector('#sourcesList details');const maps=sourceMap?.querySelectorAll('li');if(maps?.length!==expected.filter(x=>x.evidenceLocator).length)bad.push(s.id+':source-map-count');}if('${mode}'!=='deep'){const texts=document.getElementById('contentsList').textContent+document.getElementById('sourcesList').textContent;for(const s of d.screens.filter(x=>x.level===3))if(texts.includes(s.copy.${lang}.title))bad.push(s.id+':hidden-title-leak');}return{screens:expected.length,bad}})()`);
    rows.push({lang,theme,font,mode,...row});assert(!row.bad.length,'matrix '+JSON.stringify(rows.at(-1)));
   }
  }
  report.rows=rows;report.renderedInstances=rows.reduce((n,r)=>n+r.screens,0);
  report.layout=await ev(`(()=>{const bar=document.querySelector('.topbar'),area=bar.getBoundingClientRect(),buttons=[...bar.querySelectorAll('a,button')].filter(x=>!x.hidden&&getComputedStyle(x).display!=='none'),bad=[];for(const b of buttons){const r=b.getBoundingClientRect();if(r.left<area.left-1||r.right>area.right+1||r.top<area.top-1||r.bottom>area.bottom+1)bad.push(b.id+':bounds');if(!b.querySelector('[data-reader-icon]')||b.textContent.trim())bad.push(b.id+':not-icon');if(!b.getAttribute('aria-label'))bad.push(b.id+':label');}const ys=buttons.map(b=>b.getBoundingClientRect().top);if(Math.max(...ys)-Math.min(...ys)>2)bad.push('multiple-rows');return{controls:buttons.length,bad,railVisible:getComputedStyle(document.getElementById('desktopRail')).display!=='none'}})()`);
  assert(!report.layout.bad.length&&report.layout.railVisible===(width>=900),'header/rail '+JSON.stringify(report.layout));
  const fonts=[];await cmd('DOM.enable');await cmd('CSS.enable');
  for(const lang of ['ru','en'])for(const font of ['sans','serif']){
   await ev(`if(document.documentElement.lang!=='${lang}')document.getElementById('languageButton').click();BookSettings.set('readingFont','${font}');document.querySelector('#contentsList [data-go-to="i-1-p1"]').click()`);
   await ev(`document.fonts.ready.then(()=>true)`);
   const root=await cmd('DOM.getDocument',{depth:0});const node=await cmd('DOM.querySelector',{nodeId:root.root.nodeId,selector:'#story .slide-scroll > p:not(.kicker)'});
   const actual=await cmd('CSS.getPlatformFontsForNode',{nodeId:node.nodeId});fonts.push({lang,font,actual:actual.fonts});
   assert(actual.fonts.some(x=>x.isCustomFont&&x.glyphCount>0&&(font==='sans'?/Geist/.test(x.familyName):lang==='ru'?/Source Serif/.test(x.familyName):/Geist Serif/.test(x.familyName))),'actual paragraph font '+JSON.stringify(fonts.at(-1)));
  }
  report.platformFonts=fonts;
  await ev(`document.getElementById('themeButton').click()`);
  report.settings=await ev(`({open:document.getElementById('bookSettingsDialog').open,note:document.getElementById('bookSettingsFontNote').textContent})`);
  assert(report.settings.open&&report.settings.note.includes('Source Serif 4'),'honest settings note');
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});
  await ev(`new Promise(resolve=>setTimeout(resolve,60))`);
  report.settings.escapeClosed=await ev(`!document.getElementById('bookSettingsDialog').open`);
  assert(report.settings.escapeClosed,'Settings Escape did not close');
  await ev(`document.getElementById('sourcesButton').click()`);assert(await ev(`document.getElementById('sourcesDialog').open`),'sources modal');await ev(`document.getElementById('sourcesDialog').close()`);
  await ev(`BookSettings.set('theme','dark');BookSettings.set('readingFont','sans');if(document.documentElement.lang!=='en')document.getElementById('languageButton').click();document.querySelector('#contentsList [data-go-to="v-5-p1"]').click()`);
  await ev(`document.fonts.ready.then(()=>true)`);
  report.denseScroll=await ev(`(()=>{const el=document.querySelector('#story .slide-scroll'),p=el.querySelector('p:last-child'),t=p.lastChild;el.scrollTop=el.scrollHeight;const range=document.createRange();range.setStart(t,t.textContent.length-1);range.setEnd(t,t.textContent.length);const r=range.getBoundingClientRect(),b=el.getBoundingClientRect();return{scrollTop:el.scrollTop,scrollHeight:el.scrollHeight,clientHeight:el.clientHeight,lastCharacterVisible:r.top>=b.top-1&&r.bottom<=b.bottom+1}})()`);
  assert(report.denseScroll.lastCharacterVisible,'last character unreachable '+JSON.stringify(report.denseScroll));
  const shot=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,`${phase}-dense-en.png`),Buffer.from(shot.data,'base64'));
  await ev(`if(document.documentElement.lang!=='ru')document.getElementById('languageButton').click();document.querySelector('#contentsList [data-go-to="iv-6-p2"]').click();BookSettings.set('readingFont','serif');BookSettings.set('theme','light')`);
  await ev(`document.fonts.ready.then(()=>true)`);
  const shot2=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,`${phase}-scene-ru-serif.png`),Buffer.from(shot2.data,'base64'));
  await ev(`document.querySelector('#contentsList [data-go-to="cover"]').click()`);await ev(`Promise.resolve(true)`);
  const shot3=await cmd('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(out,`${phase}-cover-ru.png`),Buffer.from(shot3.data,'base64'));
 }else{
  report.pickerCancel=await ev(`(()=>{document.querySelector('#dialogModePicker [data-mode="deep"]').click();const open=document.getElementById('deepConsentDialog').open,mode=document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode,cancelFocused=document.activeElement.id==='cancelDeep';document.getElementById('cancelDeep').click();return{open,mode,cancelFocused}})()`);
  assert(report.pickerCancel.open&&report.pickerCancel.mode==='essential'&&report.pickerCancel.cancelFocused,'cancel baseline');
  const resume=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),late=d.screens.filter(s=>s.level===3),bad=[];let paths=0;for(const lang of ['ru','en']){if(document.documentElement.lang!==lang)document.getElementById('languageButton').click();for(const mode of ['essential','core'])for(const s of late){window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}));document.querySelector('#dialogModePicker [data-mode="'+mode+'"]').click();localStorage.setItem('${key}lastScreen',s.id);document.querySelector('#contentsList [data-go-to="cover"]').click();const b=document.querySelector('[data-start="continue"]');if(!/спойлер|spoiler/i.test(b?.textContent||''))bad.push(s.id+':label');if(document.getElementById('contentsList').textContent.includes(s.copy[lang].title))bad.push(s.id+':contents');const before=document.getElementById('story').textContent;b.click();if(!document.getElementById('deepConsentDialog').open)bad.push(s.id+':no-fresh-consent');if(document.getElementById('story').textContent!==before)bad.push(s.id+':content-before-consent');document.getElementById('cancelDeep').click();if(document.getElementById('story').textContent!==before)bad.push(s.id+':cancel-changed');b.click();document.getElementById('confirmDeep').click();if(document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode!=='deep')bad.push(s.id+':raise');if(document.getElementById('story').querySelector('h1')?.textContent!==s.copy[lang].title)bad.push(s.id+':wrong-target');paths++;}}return{paths,bad,scope:'BFCache pageshow emulation for every level-3 ID, both languages and lower modes'}})()`);
  report.savedDeep=resume;assert(!resume.bad.length,'saved paths '+JSON.stringify(resume));
  report.actualDowngrade=[];
  for(const lang of ['ru','en'])for(const lower of ['essential','core']){
   const r=await ev(`(()=>{
    if(document.documentElement.lang!=='${lang}')document.getElementById('languageButton').click();
    document.querySelector('#dialogModePicker [data-mode="deep"]').click();
    if(document.getElementById('deepConsentDialog').open)document.getElementById('confirmDeep').click();
    document.querySelector('#contentsList [data-go-to="v-5-p3"]').click();
    document.querySelector('#dialogModePicker [data-mode="${lower}"]').click();
    const before=document.getElementById('story').textContent;
    document.querySelector('[data-start="continue"]').click();
    const resumeOpen=document.getElementById('deepConsentDialog').open;
    const modeUnchanged=document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode==='${lower}';
    const storyUnchanged=document.getElementById('story').textContent===before;
    document.getElementById('cancelDeep').click();
    document.querySelector('#dialogModePicker [data-mode="deep"]').click();
    const pickerOpen=document.getElementById('deepConsentDialog').open;
    document.getElementById('cancelDeep').click();
    return {resumeOpen,modeUnchanged,storyUnchanged,pickerOpen};
   })()`);
   report.actualDowngrade.push({lang,lower,...r});assert(Object.values(r).every(Boolean),'fresh warning after actual downgrade '+JSON.stringify(r));
  }
  report.realReloads=[];
  for(const lang of ['ru','en'])for(const mode of ['essential','core']){
   await ev(`localStorage.setItem('${key}language','${lang}');localStorage.setItem('${key}mode','${mode}');localStorage.setItem('${key}lastScreen','v-5-p3');`);await load();
   const r=await ev(`(()=>{const b=document.querySelector('[data-start="continue"]'),generic=/спойлер|spoiler/i.test(b.textContent),safe=!document.getElementById('story').textContent.includes('Джима Холла с детства')&&!document.getElementById('story').textContent.includes('Jim Hall had been');b.click();return{generic,safe,open:document.getElementById('deepConsentDialog').open,mode:document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode}})()`);
   report.realReloads.push({lang,mode,...r});assert(r.generic&&r.safe&&r.open&&r.mode===mode,'reload guard');await ev(`document.getElementById('confirmDeep').click()`);
  }
  // A saved Deep mode itself must never populate the rail with ending titles.
  await ev(`localStorage.setItem('${key}mode','deep');localStorage.setItem('${key}lastScreen','v-5-p6')`);await load();
  report.savedModeReset=await ev(`({mode:document.querySelector('#dialogModePicker [data-mode].is-active').dataset.mode,noTitle:!document.getElementById('contentsList').textContent.includes('A warm tongue')&&!document.getElementById('contentsList').textContent.includes('Тёплый язык')})`);
  assert(report.savedModeReset.mode==='essential'&&report.savedModeReset.noTitle,'saved Deep mode leak');
  // An explicit local entry on the lower-depth final must ask, not silently enter.
  await ev(`document.querySelector('#contentsList [data-go-to="final"]').click();document.querySelector('[data-open-deep]').click()`);
  report.explicitEntry=await ev(`document.getElementById('deepConsentDialog').open`);assert(report.explicitEntry,'explicit entry');
  await cmd('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});await cmd('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});
  await ev(`new Promise(resolve=>setTimeout(resolve,60))`);
  report.consentEscapeClosed=await ev(`!document.getElementById('deepConsentDialog').open`);assert(report.consentEscapeClosed,'Consent Escape did not close');
  await ev(`document.querySelector('[data-open-deep]').click();document.getElementById('confirmDeep').click()`);
  assert(await ev(`document.getElementById('story').querySelector('h1').textContent===JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s=>s.id==='deep-warning').copy[document.documentElement.lang].title`),'explicit entry target');
  report.interactions=await ev(`(()=>{const r={},k='${key}lastScreen';document.querySelector('#contentsList [data-go-to="iv-6-p2"]').click();document.getElementById('languageButton').click();r.languageKeepsId=localStorage.getItem(k)==='iv-6-p2';const el=document.querySelector('.slide-scroll');el.scrollTop=60;const old=el.scrollTop;BookSettings.set('theme','light');BookSettings.set('readingFont','serif');r.settingsKeepId=localStorage.getItem(k)==='iv-6-p2';r.settingsKeepScroll=el===document.querySelector('.slide-scroll')&&el.scrollTop===old;document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}));r.focusOn=document.documentElement.dataset.focusMode==='true';document.getElementById('nextButton').click();r.focusPaging=document.documentElement.dataset.focusMode==='true';document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));r.focusOff=!document.documentElement.hasAttribute('data-focus-mode');document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));r.keyboardBack=localStorage.getItem(k)==='iv-6-p2';const story=document.getElementById('story');story.dispatchEvent(new PointerEvent('pointerdown',{pointerId:5,clientX:240,clientY:220,bubbles:true}));story.dispatchEvent(new PointerEvent('pointerup',{pointerId:5,clientX:100,clientY:220,bubbles:true}));r.syntheticSwipe=localStorage.getItem(k)==='iv-6-p3';document.querySelector('#contentsList [data-go-to="final"]').click();document.getElementById('nextButton').click();r.restartClears=!localStorage.getItem(k);return r})()`);
  assert(Object.values(report.interactions).every(Boolean),'interactions '+JSON.stringify(report.interactions));
  await ev(`localStorage.setItem('${key}lastScreen','invalid-old-id');document.querySelector('#contentsList [data-go-to="cover"]').click();`);
  // Invalid IDs are omitted from the resume label; begin still advances safely.
  await ev(`document.querySelector('[data-start="begin"]').click()`);report.invalidIdStarts=await ev(`document.getElementById('story').querySelector('h1').textContent.length>0`);
  report.persistedConsentKeys=await ev(`[...Array(localStorage.length)].map((_,i)=>localStorage.key(i)).filter(k=>/consent/i.test(k))`);assert(!report.persistedConsentKeys.length,'persistent consent');
 }
 assert(!errors.length&&!remote.length,'runtime/network '+JSON.stringify({errors,remote}));
 report.runtimeErrors=errors;report.remoteRequests=remote;report.status='completed';
}catch(e){report.status='failed';report.error=e.stack;throw e;}
finally{cleanup();report.profileRemoved=!fs.existsSync(profile);report.processGroupTerminated=true;fs.writeFileSync(path.join(out,`browser-${phase}.json`),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({phase,status:report.status,renderedInstances:report.renderedInstances,savedPaths:report.savedDeep?.paths,error:report.error,profileRemoved:report.profileRemoved}));}
