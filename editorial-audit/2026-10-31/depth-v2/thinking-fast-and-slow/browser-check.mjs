import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import {createHash} from 'node:crypto';
import {spawn,execFileSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url)),width=Number(process.argv[2]||320),height={320:568,390:844,1024:768,1440:900}[width];
if(!height)throw Error('Unsupported viewport');
const ios=process.argv.includes('--ios'),prefix=ios?'ios-':'';
const data=JSON.parse(fs.readFileSync(path.join(dir,'story-data.json'),'utf8'));
const profile=execFileSync('/usr/bin/mktemp',['-d',path.join(os.tmpdir(),'kahneman-depth-v2-XXXXXX')],{encoding:'utf8'}).trim();
const port=await new Promise(resolve=>{const s=net.createServer();s.listen(0,'127.0.0.1',()=>{const p=s.address().port;s.close(()=>resolve(p))})});
let chrome,socket,cleaned=false,counter=0,report={width,height,offline:true},failure;
report.inputHashes=Object.fromEntries(['story-data.json','thinking-fast-and-slow.html','browser-check.mjs'].map(name=>[name,createHash('sha256').update(fs.readFileSync(path.join(dir,name))).digest('hex')]));
const pending=new Map(),errors=[],requests=[];
function ownPids(){return execFileSync('/bin/ps',['-axo','pid=,command='],{encoding:'utf8'}).split('\n').filter(l=>l.includes('--user-data-dir='+profile)).map(l=>Number(l.trim().split(/\s/)[0])).filter(Boolean)}
function cleanup(){if(cleaned)return report.cleanup;cleaned=true;try{socket?.close()}catch{}for(const p of pending.values())clearTimeout(p.timer);try{if(chrome?.pid)process.kill(-chrome.pid,'SIGKILL')}catch{}for(const pid of ownPids()){try{process.kill(pid,'SIGKILL')}catch{}}fs.rmSync(profile,{recursive:true,force:true,maxRetries:6,retryDelay:80});return report.cleanup={profileRemoved:!fs.existsSync(profile),remainingOwnedPids:ownPids(),timeoutSeconds:30,isolatedProcessGroup:true};}
process.on('exit',cleanup);process.on('SIGINT',()=>{cleanup();process.exit(130)});process.on('SIGTERM',()=>{cleanup();process.exit(143)});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const assert=(v,m)=>{if(!v)throw Error(m)};
try{
 chrome=spawn('/usr/bin/timeout',['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore',detached:true});
 let target;for(let i=0;i<60;i++){try{target=(await(await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t=>t.type==='page');if(target)break}catch{}await pause(60)}assert(target,'Chrome target');
 socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{socket.addEventListener('open',r,{once:true});socket.addEventListener('error',j,{once:true})});
 socket.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(p){clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result)}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.requestWillBeSent')requests.push(m.params.request.url)});
 function c(method,params={}){const id=++counter;return new Promise((resolve,reject)=>{const timer=setTimeout(()=>{pending.delete(id);reject(Error(method+' timeout'))},6500);pending.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params}))})}
 async function ev(expression){const r=await c('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result?.value}
 await c('Page.enable');await c('Runtime.enable');await c('Network.enable');await c('DOM.enable');await c('CSS.enable');
 await c('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
 await c('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<900});
 if(ios){
 await c('Network.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1',platform:'iPhone'});
 const protocol=await(await fetch(`http://127.0.0.1:${port}/json/protocol`)).json();const command=protocol.domains.find(d=>d.domain==='Emulation').commands.find(x=>/setSafeAreaInsets/.test(x.name));
 if(command){await c('Emulation.'+command.name,{insets:{top:44,bottom:34,left:0,right:0}});report.safeArea={method:command.name,top:44,bottom:34};}else report.safeArea={unsupported:true};
 }
 await c('Page.navigate',{url:pathToFileURL(path.join(dir,data.slug+'.html')).href});
 for(let i=0;i<70;i++){if(await ev("document.readyState==='complete'&&!!document.querySelector('#story h1')&&!!window.BookSettings"))break;await pause(40)}
 if(ios){await pause(750);report.iosGuide=await ev(`(()=>{const d=document.querySelector('#bookLibraryInstallDialog');const ok=d.open&&d.textContent.includes('На экран Домой');if(!ok)throw Error('iPhone guide');document.querySelector('#bookLibraryInstallClose').click();return {autoOpened:true,localized:true,closed:!d.open}})()`);}
 await ev(`(async()=>{await Promise.all([...document.fonts].map(f=>f.load()));await document.fonts.ready;const s=document.createElement('style');s.textContent='*,*::before,*::after{animation:none!important;transition:none!important}';document.head.append(s)})()`);
 report.initial=await ev(`({language:document.documentElement.lang,theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont,mode:localStorage.getItem('book-tiktok.thinking-fast-and-slow.mode'),counts:JSON.parse(document.querySelector('#book-tiktok-data').textContent).targetModes,visible:document.querySelectorAll('.progress-segment').length,fonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))})`);
 assert(report.initial.language==='ru'&&report.initial.theme==='dark'&&report.initial.font==='sans'&&report.initial.visible===data.targetModes.essential,'fresh RU/dark/Sans/Essential');
 assert(report.initial.fonts.every(f=>f.status==='loaded'),'embedded font faces loaded');
 report.traversal=await ev(`(async()=>{
 const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent),failures=[],routes=[];let views=0;const a=(v,m)=>{if(!v)failures.push(m)};
 const micro=()=>Promise.resolve();
 for(const lang of ['ru','en']){if(document.documentElement.lang!==lang)document.querySelector('#languageButton').click();await micro();
 for(const theme of ['dark','light']){BookSettings.set('theme',theme);
 for(const font of ['sans','serif']){BookSettings.set('readingFont',font);await document.fonts.ready;
 for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
 document.querySelector('[data-mode="'+mode+'"]').click();document.querySelector('#desktopContentsList [data-go-to="cover"]').click();await micro();const list=d.screens.filter(s=>s.level<=level);a(document.querySelectorAll('.progress-segment').length===d.targetModes[mode],mode+' count');const seen=[];
 for(const s of list){const item=document.querySelector('#desktopContentsList [data-go-to="'+s.id+'"]');a(!!item,'contents item '+s.id);item.click();await micro();const h=document.querySelector('#story h1'),el=document.querySelector('.slide-scroll');a(h.textContent===s.copy[lang].title,'title '+lang+'/'+s.id);const tmp=document.createElement('div');tmp.innerHTML=s.copy[lang].body;const actual=document.querySelector('#story').textContent.replace(/\\s+/g,' ');a([...tmp.querySelectorAll('p')].every(p=>actual.includes(p.textContent.replace(/\\s+/g,' '))),'body '+lang+'/'+s.id);a(document.documentElement.scrollWidth<=innerWidth+1,'document overflow '+s.id);a(el.scrollWidth<=el.clientWidth+1,'slide overflow '+s.id);a(h.getBoundingClientRect().left>=-1&&h.getBoundingClientRect().right<=innerWidth+1,'heading bounds '+s.id);el.scrollTop=el.scrollHeight;const ps=[...el.querySelectorAll('p')].filter(p=>!p.classList.contains('kicker')&&!p.classList.contains('source-label'));const last=ps.at(-1);if(last)a(last.getBoundingClientRect().bottom<=el.getBoundingClientRect().bottom+1,'body tail '+s.id);el.scrollTop=0;seen.push(s.id);views++;}
 routes.push({lang,theme,font,mode,count:seen.length,orderedIds:seen});
 }}}}
 return{failures,routes,views};})()`);
 assert(report.traversal.failures.length===0,JSON.stringify(report.traversal.failures.slice(0,12)));
 report.interaction=await ev(`(async()=>{
 const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent),checks=[],a=(v,m)=>{if(!v)throw Error(m);checks.push(m)};const frame=()=>new Promise(r=>requestAnimationFrame(r));const key=k=>document.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true}));const go=id=>document.querySelector('#desktopContentsList [data-go-to="'+id+'"]').click();
 if(document.documentElement.lang!=='ru')document.querySelector('#languageButton').click();document.querySelector('[data-mode="deep"]').click();go('same-outcomes-new-frame');await frame();
 const saved=localStorage.getItem('book-tiktok.'+d.slug+'.lastScreen'),count=document.querySelector('#counter').textContent;document.querySelector('#languageButton').click();await frame();a(localStorage.getItem('book-tiktok.'+d.slug+'.lastScreen')===saved,'language preserves stable ID');a(document.querySelector('#counter').textContent===count,'language preserves position/depth');
 const scroll=document.querySelector('.slide-scroll');scroll.scrollTop=Math.min(35,scroll.scrollHeight-scroll.clientHeight);const top=scroll.scrollTop;const beforeTheme=document.documentElement.dataset.theme;document.querySelector('#themeButton').click();a(document.querySelector('#bookSettingsDialog').open,'gear opens Settings');a(document.documentElement.dataset.theme===beforeTheme,'opening Settings does not toggle theme');document.querySelector('input[name="book-theme"][value="dark"]').click();document.querySelector('input[name="book-font"][value="serif"]').click();await frame();await frame();a(document.documentElement.dataset.theme==='dark'&&document.documentElement.dataset.readingFont==='serif','Settings radio controls');a(localStorage.getItem('book-tiktok.'+d.slug+'.lastScreen')===saved&&document.querySelector('#counter').textContent===count,'Settings preserves book state');a(Math.abs(scroll.scrollTop-top)<=1,'Settings preserves reading scroll');a(document.querySelector('#bookSettingsFontNote').textContent.includes('Source Serif 4'),'localized honest Serif fallback note');document.querySelector('#bookSettingsClose').click();a(!document.querySelector('#bookSettingsDialog').open,'Settings closes');
 document.querySelector('#sourcesButton').click();a(document.querySelector('#sourcesDialog').open,'Sources opens');a(document.querySelectorAll('#sourcesList li').length===5,'all source roles globally accessible');document.querySelector('#sourcesDialog').close();document.querySelector('#contentsButton').click();a(document.querySelector('#contentsDialog').open,'Contents opens');document.querySelector('#contentsDialog').close();
 key('f');a(document.documentElement.hasAttribute('data-focus-mode'),'keyboard focus on');a(getComputedStyle(document.querySelector('.app-header')).display==='none','focus hides header');a(getComputedStyle(document.querySelector('#nextButton')).display!=='none','focus keeps Next');const focusTitle=document.querySelector('#story h1').textContent;document.querySelector('#nextButton').click();a(document.documentElement.hasAttribute('data-focus-mode')&&document.querySelector('#story h1').textContent!==focusTitle,'focus persists while paging');key('Escape');a(!document.documentElement.hasAttribute('data-focus-mode'),'Escape exits focus');
 go('the-question');const t=document.querySelector('#story h1').textContent;key('ArrowRight');a(document.querySelector('#story h1').textContent!==t,'keyboard next');document.querySelector('#previousButton').click();a(document.querySelector('#story h1').textContent===t,'Previous button');
 const story=document.querySelector('#story');story.dispatchEvent(new PointerEvent('pointerdown',{pointerId:7,clientX:220,clientY:200,bubbles:true}));story.dispatchEvent(new PointerEvent('pointerup',{pointerId:7,clientX:65,clientY:200,bubbles:true}));a(document.querySelector('#story h1').textContent!==t,'horizontal pointer swipe advances');const swiped=document.querySelector('#story h1').textContent;story.dispatchEvent(new PointerEvent('pointerdown',{pointerId:8,clientX:100,clientY:250,bubbles:true}));story.dispatchEvent(new PointerEvent('pointerup',{pointerId:8,clientX:103,clientY:90,bubbles:true}));a(document.querySelector('#story h1').textContent===swiped&&!document.documentElement.hasAttribute('data-focus-mode'),'vertical gesture neither pages nor focuses');
 go('final');document.querySelector('#nextButton').click();a(document.querySelector('#story h1').textContent===d.title[document.documentElement.lang]&&!localStorage.getItem('book-tiktok.'+d.slug+'.lastScreen'),'final restart clears saved screen');
 await frame();const controls=[...document.querySelectorAll('.topbar button,.topbar a')].filter(n=>!n.hidden&&getComputedStyle(n).display!=='none');const rs=controls.map(n=>n.getBoundingClientRect());a(Math.max(...rs.map(r=>r.top))-Math.min(...rs.map(r=>r.top))<2,'compact one-row header');a(rs.every(r=>r.left>=0&&r.right<=innerWidth+1),'header controls within viewport');a(controls.every(n=>n.querySelector('svg')&&n.title&&n.getAttribute('aria-label')&&!n.textContent.trim()),'labeled icon-only header');a(document.querySelector('#libraryButton').getAttribute('href')==='./','home href');a(innerWidth<900||getComputedStyle(document.querySelector('.desktop-rail')).display!=='none','desktop rail visible');
 document.querySelector('[data-mode="deep"]').click();go('bayesian-update');await frame();a(document.querySelector('#desktopContentsList .is-active').dataset.goTo==='bayesian-update','rail follows stable ID');return checks;})()`);
 // Inspect actual custom fonts used to draw reading paragraphs, not just CSS names.
 if(ios){
 report.iosGuide.header=await ev(`(()=>{const a=[...document.querySelectorAll('.topbar button,.topbar a')].filter(n=>!n.hidden&&getComputedStyle(n).display!=='none'),r=a.map(n=>n.getBoundingClientRect());return {count:a.length,minTop:Math.min(...r.map(x=>x.top)),maxRight:Math.max(...r.map(x=>x.right)),oneRow:Math.max(...r.map(x=>x.top))-Math.min(...r.map(x=>x.top))<2}})()`);
 assert(report.iosGuide.header.oneRow&&report.iosGuide.header.maxRight<=width+1,'iPhone header geometry');if(report.safeArea.top)assert(report.iosGuide.header.minTop>=44,'header below emulated safe area');
 const beforeTouch=await ev(`document.querySelector('#story h1').textContent`);
 await c('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:width-50,y:300,id:1}]});await c('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:55,y:301,id:1}]});await c('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await pause(50);
 assert(await ev(`document.querySelector('#story h1').textContent`)!==beforeTouch,'CDP mobile touch swipe');report.iosGuide.cdpTouchSwipe=true;await ev(`document.querySelector('#desktopContentsList [data-go-to="bayesian-update"]').click()`);
 }
 report.platformFonts=[];
 for(const lang of ['ru','en'])for(const font of ['sans','serif']){
  await ev(`(async()=>{if(document.documentElement.lang!==${JSON.stringify(lang)})document.querySelector('#languageButton').click();BookSettings.set('readingFont',${JSON.stringify(font)});await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r));})()`);
  const doc=await c('DOM.getDocument');const node=await c('DOM.querySelector',{nodeId:doc.root.nodeId,selector:'#story .slide-scroll p:not(.kicker):not(.source-label)'});const used=await c('CSS.getPlatformFontsForNode',{nodeId:node.nodeId});report.platformFonts.push({lang,font,fonts:used.fonts});
  const wanted=font==='sans'?'Geist':lang==='ru'?'Source Serif 4':'Geist Serif';assert(used.fonts.some(f=>f.familyName===wanted&&f.isCustomFont&&f.glyphCount>0),'actual font '+lang+'/'+font+' '+JSON.stringify(used));
 }
 // Reload in saved EN/Deep state, then verify both Continue and Start over.
 await c('Page.reload');await pause(160);
 report.savedState=await ev(`(async()=>{const a=(v,m)=>{if(!v)throw Error(m)};a(document.documentElement.lang==='en','saved language');a(document.querySelectorAll('.progress-segment').length===97,'saved Deep');a(document.querySelector('[data-start="continue"]'),'Continue offered');document.querySelector('[data-start="continue"]').click();a(localStorage.getItem('book-tiktok.thinking-fast-and-slow.lastScreen')==='bayesian-update','saved screen retained');a(document.querySelector('#story h1').textContent==='Combining two kinds of information','Continue resumes');return {language:'en',mode:'deep',screen:'bayesian-update',continue:true}})()`);
 await c('Page.reload');await pause(100);await ev(`document.querySelector('[data-start="begin"]').click()`);assert(await ev(`document.querySelector('#story h1').textContent==='An error familiar to researchers'`),'Start over begins mode');report.savedState.startOver=true;
 // Screenshots are local QA only; no preview tools and no content server.
 for(const [label,id,lang,theme,font] of [['cover','cover','ru','dark','sans'],['dense','a-complete-looking-story','ru','light','serif'],['quantitative','same-outcomes-new-frame','en','dark','sans'],['final','final','ru','dark','sans']]){
  await ev(`(async()=>{if(document.documentElement.lang!==${JSON.stringify(lang)})document.querySelector('#languageButton').click();BookSettings.set('theme',${JSON.stringify(theme)});BookSettings.set('readingFont',${JSON.stringify(font)});document.querySelector('#desktopContentsList [data-go-to="${id}"]').click();await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r))})()`);
  await pause(350);
  fs.writeFileSync(path.join(dir,'qa',`${prefix}${width}-${label}.png`),Buffer.from((await c('Page.captureScreenshot',{format:'png'})).data,'base64'));
 }
 if(ios){
 await ev(`(()=>{if(document.documentElement.lang!=='en')document.querySelector('#languageButton').click();document.querySelector('#bookLibraryInstallTrigger').click();const d=document.querySelector('#bookLibraryInstallDialog');if(!d.open||!d.textContent.includes('Home Screen'))throw Error('EN install guide');document.querySelector('#bookLibraryInstallClose').click()})()`);report.iosGuide.englishManual=true;
 await c('Page.addScriptToEvaluateOnNewDocument',{source:"Object.defineProperty(navigator,'standalone',{get:()=>true,configurable:true})"});await c('Page.reload');await pause(150);report.iosGuide.standalone=await ev(`(()=>{const t=document.querySelector('#bookLibraryInstallTrigger'),d=document.querySelector('#bookLibraryInstallDialog');return !d.open&&(t.hidden||getComputedStyle(t).display==='none')})()`);assert(report.iosGuide.standalone,'standalone hides guide and trigger');
 }
 assert(errors.length===0,'runtime errors');assert(!requests.some(u=>/^https?:/.test(u)),'remote runtime requests');report.errors=errors;report.remoteRuntimeRequests=requests.filter(u=>/^https?:/.test(u));report.status='local-checks-completed';
}catch(e){failure=e;report.status='local-check-failed';report.error=e.stack;report.errors=errors;}
finally{cleanup();}
fs.writeFileSync(path.join(dir,'qa',`browser-${prefix}${width}.json`),JSON.stringify(report,null,2)+'\n');
assert(report.cleanup.profileRemoved&&report.cleanup.remainingOwnedPids.length===0,'cleanup');
if(failure)throw failure;
console.log(JSON.stringify({width,status:report.status,views:report.traversal.views,interactionChecks:report.interaction.length,cleanup:report.cleanup}));
