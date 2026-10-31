import fs from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import {spawn,spawnSync} from 'node:child_process';
export async function chromeSession(run) {
 const profile=spawnSync('mktemp',['-d',path.join(os.tmpdir(),'flowers-chrome-sol.XXXXXX')],{encoding:'utf8'}).stdout.trim();
 if(!profile) throw Error('mktemp failed');
 const port=await new Promise(resolve=>{const s=net.createServer();s.listen(0,'127.0.0.1',()=>{let p=s.address().port;s.close(()=>resolve(p));});});
 let chrome,socket,id=0; const pending=new Map(),errors=[],requests=[];
 function cleanup(){if(socket&&socket.readyState<2)socket.close(); if(chrome?.pid){try{process.kill(-chrome.pid,'SIGKILL')}catch{}}fs.rmSync(profile,{recursive:true,force:true,maxRetries:8,retryDelay:100});}
 process.once('exit',cleanup);process.once('SIGTERM',()=>{cleanup();process.exit(143)});process.once('SIGINT',()=>{cleanup();process.exit(130)});
 const command=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;const timer=setTimeout(()=>{pending.delete(n);reject(Error(method+' timeout'))},5000);pending.set(n,{resolve:r=>{clearTimeout(timer);resolve(r)},reject});socket.send(JSON.stringify({id:n,method,params}));});
 const evaluate=async expression=>{const r=await command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;};
 const until=async (fn,label)=>{for(let n=0;n<85;n++){try{const r=await fn();if(r)return r}catch{}await new Promise(r=>setTimeout(r,75));}throw Error(label+' timeout')};
 try{
  chrome=spawn('/usr/bin/timeout',['30','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--disable-background-networking',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,'about:blank'],{detached:true,stdio:'ignore'});
  const target=await until(async()=>{const r=await fetch(`http://127.0.0.1:${port}/json/list`);return (await r.json()).find(t=>t.type==='page'&&t.webSocketDebuggerUrl)},'CDP');
  socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
  socket.addEventListener('message',e=>{const m=JSON.parse(String(e.data));if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result||{});}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);else if(m.method==='Network.requestWillBeSent')requests.push(m.params.request.url);});
  await command('Page.enable');await command('Runtime.enable');await command('Network.enable');
  await run({command,evaluate,until,errors,requests,profile});
 }finally{cleanup();process.removeListener('exit',cleanup)}
}
