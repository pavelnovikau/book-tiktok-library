// Book-local supplement: prove global Settings survive a real file:// reload.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';
import {spawn,execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';

const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const slug='why-zebras-dont-get-ulcers';
const profile=execFileSync('/usr/bin/mktemp',['-d',path.join(os.tmpdir(),'zebras-prefs-XXXXXX')],{encoding:'utf8'}).trim();
const port=await new Promise(resolve=>{const s=net.createServer();s.listen(0,'127.0.0.1',()=>{const p=s.address().port;s.close(()=>resolve(p))})});
const hash=name=>createHash('sha256').update(fs.readFileSync(path.join(dir,name))).digest('hex');
const report={scope:'Same standalone file, real reload; synthetic storage event separately identified. No cross-file or physical Safari claim.',inputHashes:Object.fromEntries(['story-data.json',slug+'.html','qa/preference-check.mjs'].map(f=>[f,hash(f)])),checks:[]};
let chrome,socket,counter=0,cleaned=false,failure;
const pending=new Map(),errors=[],requests=[];
const ownPids=()=>execFileSync('/bin/ps',['-axo','pid=,command='],{encoding:'utf8'}).split('\n').filter(l=>l.includes('--user-data-dir='+profile)).map(l=>Number(l.trim().split(/\s/)[0])).filter(Boolean);
function cleanup(){if(cleaned)return;cleaned=true;try{socket?.close()}catch{}for(const p of pending.values())clearTimeout(p.timer);try{if(chrome?.pid)process.kill(-chrome.pid,'SIGKILL')}catch{}for(const pid of ownPids())try{process.kill(pid,'SIGKILL')}catch{}fs.rmSync(profile,{recursive:true,force:true,maxRetries:6,retryDelay:80});report.cleanup={profileRemoved:!fs.existsSync(profile),remainingOwnedPids:ownPids(),timeoutSeconds:30,isolatedProcessGroup:true}}
process.on('exit',cleanup);process.on('SIGINT',()=>{cleanup();process.exit(130)});process.on('SIGTERM',()=>{cleanup();process.exit(143)});
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const assert=(v,m)=>{if(!v)throw Error(m);report.checks.push(m)};
try{
 chrome=spawn('/usr/bin/timeout',['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,'about:blank'],{stdio:'ignore',detached:true});
 let target;for(let i=0;i<60;i++){try{target=(await(await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(t=>t.type==='page');if(target)break}catch{}await pause(60)}assert(target,'isolated Chrome target');
 socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{socket.addEventListener('open',r,{once:true});socket.addEventListener('error',j,{once:true})});
 socket.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);if(p){clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result)}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.requestWillBeSent')requests.push(m.params.request.url)});
 function c(method,params={}){const id=++counter;return new Promise((resolve,reject)=>{const timer=setTimeout(()=>{pending.delete(id);reject(Error(method+' timeout'))},6500);pending.set(id,{resolve,reject,timer});socket.send(JSON.stringify({id,method,params}))})}
 async function ev(expression){const r=await c('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.exception?.description||r.exceptionDetails.text);return r.result?.value}
 await c('Page.enable');await c('Runtime.enable');await c('Network.enable');await c('Emulation.setDeviceMetricsOverride',{width:320,height:568,deviceScaleFactor:1,mobile:true});
 await c('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
 await c('Page.navigate',{url:pathToFileURL(path.join(dir,slug+'.html')).href});
 async function ready(previousOrigin){for(let i=0;i<70;i++){if(await ev("document.readyState==='complete'&&!!document.querySelector('#story h1')&&!!window.BookSettings"+(previousOrigin===undefined?'':'&&performance.timeOrigin!=='+JSON.stringify(previousOrigin))))return;await pause(40)}throw Error('reader readiness')}
 await ready();
 report.changed=await ev(`(async()=>{
 const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent),p='book-tiktok.'+d.slug+'.depth-v2.';
 document.querySelector('[data-mode="deep"]').click();document.querySelector('#desktopContentsList [data-go-to="unit-027"]').click();document.querySelector('#languageButton').click();
 const sc=document.querySelector('.slide-scroll');sc.scrollTop=30;const before={id:localStorage.getItem(p+'lastScreen'),mode:localStorage.getItem(p+'mode'),scroll:sc.scrollTop};
 document.querySelector('#themeButton').click();document.querySelector('input[name="book-theme"][value="light"]').click();document.querySelector('input[name="book-font"][value="serif"]').click();document.querySelector('#bookSettingsClose').click();await document.fonts.ready;await new Promise(r=>requestAnimationFrame(r));
 return{before,after:{id:localStorage.getItem(p+'lastScreen'),mode:localStorage.getItem(p+'mode'),scroll:sc.scrollTop},global:JSON.parse(localStorage.getItem('bookLibrary.preferences.v1')),lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont};})()`);
 assert(report.changed.global.version===1&&report.changed.global.theme==='light'&&report.changed.global.readingFont==='serif','global v1 preferences saved by Settings');
 assert(JSON.stringify(report.changed.before)===JSON.stringify(report.changed.after),'Settings preserve exact ID, depth and reading scroll');
 const previousOrigin=await ev('performance.timeOrigin');await c('Page.reload');await ready(previousOrigin);report.realDocumentReload=true;
 report.reloaded=await ev(`(()=>{const d=JSON.parse(document.querySelector('#book-tiktok-data').textContent),p='book-tiktok.'+d.slug+'.depth-v2.',b=document.querySelector('[data-start="continue"]');const before={lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont,mode:localStorage.getItem(p+'mode'),id:localStorage.getItem(p+'lastScreen'),continueOffered:!!b};if(b)b.click();return {before,title:document.querySelector('#story h1').textContent,id:localStorage.getItem(p+'lastScreen'),theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont};})()`);
 assert(report.reloaded.before.lang==='en'&&report.reloaded.before.theme==='light'&&report.reloaded.before.font==='serif','real reload restores EN, global light and Serif');
 assert(report.reloaded.before.mode==='deep'&&report.reloaded.before.id==='unit-027'&&report.reloaded.before.continueOffered&&report.reloaded.id==='unit-027'&&report.reloaded.title==='The nurse goes on vacation','real reload and Continue preserve expanded-book position');
 report.syntheticStorageEvent=await ev(`(()=>{const value=JSON.stringify({version:1,theme:'dark',readingFont:'sans'});localStorage.setItem('bookLibrary.preferences.v1',value);dispatchEvent(new StorageEvent('storage',{key:'bookLibrary.preferences.v1',newValue:value}));return{theme:document.documentElement.dataset.theme,font:document.documentElement.dataset.readingFont,title:document.querySelector('#story h1').textContent};})()`);
 assert(report.syntheticStorageEvent.theme==='dark'&&report.syntheticStorageEvent.font==='sans'&&report.syntheticStorageEvent.title==='The nurse goes on vacation','synthetic global storage event refreshes Settings without paging');
 assert(errors.length===0,'zero runtime exceptions');assert(!requests.some(u=>/^https?:/.test(u)),'zero remote runtime requests');report.errors=errors;report.remoteRuntimeRequests=requests.filter(u=>/^https?:/.test(u));report.status='local-checks-completed';
}catch(e){failure=e;report.status='local-check-failed';report.error=e.stack;report.errors=errors;}
finally{cleanup()}
fs.writeFileSync(path.join(dir,'qa','preference-state.json'),JSON.stringify(report,null,2)+'\n');
if(!report.cleanup.profileRemoved||report.cleanup.remainingOwnedPids.length)throw Error('cleanup');
if(failure)throw failure;
console.log(JSON.stringify({status:report.status,checks:report.checks.length,cleanup:report.cleanup}));
