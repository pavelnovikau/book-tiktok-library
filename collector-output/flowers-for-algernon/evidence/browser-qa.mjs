import fs from 'node:fs';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import {chromeSession} from './chrome-session.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));const file=path.resolve(here,'../flowers-for-algernon.html'), url=pathToFileURL(file).href;
const phase=process.argv[2]||'320';
const sizes={'320':[320,568],'390':[390,844],'1024':[1024,768],'1440':[1440,900],behavior:[390,844],ios:[320,568]};
const [width,height]=sizes[phase]||[];if(!width)throw Error('unknown phase');
const expected=JSON.parse(fs.readFileSync(path.resolve(here,'../story-data.json'),'utf8'));
let result={phase,width,height,checks:[],visits:0};
const assert=(v,m)=>{if(!v)throw Error(m);result.checks.push(m)};
await chromeSession(async({command,evaluate,until,errors,requests,profile})=>{
 await command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width<900});
 if(phase==='ios'){
  await command('Network.setUserAgentOverride',{userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1'});
 }
 await command('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:-1,uploadThroughput:-1});
 const load=async()=>{await command('Page.navigate',{url});await until(()=>evaluate('document.readyState === "complete" && Boolean(document.querySelector("#story h1"))'),'file render');await evaluate('document.fonts.ready.then(()=>true)');};
 await load();
 const initial=await evaluate(`({lang:document.documentElement.lang,theme:document.documentElement.dataset.theme,essential:document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed'),home:document.getElementById('libraryButton').getAttribute('href'),narrative:document.documentElement.dataset.contentMode,data:JSON.parse(document.getElementById('book-tiktok-data').textContent)})`);
 assert(initial.lang==='ru'&&initial.theme==='dark'&&initial.essential==='true','fresh RU/dark/Essential');
 assert(initial.home==='./','home control links to ./');assert(initial.narrative==='narrative','narrative presentation');
 assert(JSON.stringify(initial.data.screens)===JSON.stringify(expected.screens),'effective embedded corpus equals canonical 34 RU/EN pairs');
 assert(JSON.stringify(initial.data.sources)===JSON.stringify(expected.sources),'embedded source map equals canonical');
 const shot=async name=>{await new Promise(r=>setTimeout(r,220));const r=await command('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(path.join(here,name+'.png'),Buffer.from(r.data,'base64'));};
 if(['320','1440'].includes(phase))await shot('cover-'+phase+'-ru-dark');
 if(/^\d+$/.test(phase)){
  const traversal=await evaluate(`(async()=>{
   const data=JSON.parse(document.getElementById('book-tiktok-data').textContent), failures=[],metrics=[];let visits=0;
   const test=(ok,msg)=>{if(!ok)failures.push(msg)};
   for(const language of ['ru','en']){
    if(document.documentElement.lang!==language)document.getElementById('languageButton').click();
    for(const theme of ['dark','light']){
     if(document.documentElement.dataset.theme!==theme)document.getElementById('themeButton').click();
     for(const [mode,level] of [['essential',1],['core',2],['deep',3]]){
      document.getElementById('contentsButton').click();
      document.querySelector('#dialogModePicker [data-mode="'+mode+'"]').click();
      if(document.getElementById('spoilerDialog').open)document.querySelector('[data-ending-accept]').click();
      if(document.getElementById('contentsDialog').open)document.getElementById('contentsDialog').close();
      const screens=data.screens.filter(s=>s.level<=level);
      test(screens.length===data.targetModes[mode],'exact '+mode+' total');
      test(document.querySelectorAll('#contentsList [data-go-to]').length===screens.length,'contents '+mode+' total');
      for(const [i,s] of screens.entries()){
       document.querySelector('#contentsList [data-go-to="'+s.id+'"]').click();
       visits++;
       const title=document.querySelector('#story h1'), sc=document.querySelector('#story .slide-scroll');
       test(title.textContent===s.copy[language].title,mode+'/'+language+'/'+s.id+' title');
       test(document.getElementById('counter').textContent===(i+1)+' / '+screens.length,mode+'/'+language+'/'+s.id+' counter');
       test(document.documentElement.scrollWidth<=innerWidth+1,mode+'/'+language+'/'+s.id+' page overflow');
       test(sc.scrollWidth<=sc.clientWidth+1,mode+'/'+language+'/'+s.id+' text overflow');
       test(!document.querySelector('#story .source-label'),s.id+' hides inline provenance');
      }
      metrics.push({mode,language,theme,count:screens.length});
     }
    }
   }
   await new Promise(resolve=>requestAnimationFrame(resolve));
   const controls=[...document.querySelectorAll('.topbar a,.topbar button')].filter(n=>n.getBoundingClientRect().width&&getComputedStyle(n).display!=='none').map(n=>{const b=n.getBoundingClientRect();return {id:n.id,x:b.x,y:b.y,width:b.width,height:b.height,label:n.getAttribute('aria-label'),text:n.textContent.trim(),icon:!!n.querySelector('svg')}});
   test(controls.every(c=>c.label&&c.icon&&!c.text),'icon-only localized header');
   test(controls.every(c=>c.x>=-1&&c.x+c.width<=innerWidth+1),'header fits');
   test(Math.max(...controls.map(c=>c.y))-Math.min(...controls.map(c=>c.y))<=2,'single header row');
   const rail=document.querySelector('.chapter-rail')||document.getElementById('desktopContentsList')?.parentElement;
   if(innerWidth>=900)test(rail&&getComputedStyle(rail).display!=='none','desktop rail visible');
   return {failures,visits,metrics,controls,fonts:document.fonts.status};
  })()`);
  assert(!traversal.failures.length,'all bilingual/theme/mode traversals and layout checks: '+JSON.stringify(traversal.failures));
  result.visits=traversal.visits;result.traversal=traversal;
  assert(traversal.fonts==='loaded','embedded fonts load while offline');
  await evaluate(`document.querySelector('#contentsList [data-go-to="rose-and-norma"]').click();`);
  if(['320','1440'].includes(phase))await shot('dense-'+phase+'-en-light');
  await evaluate(`document.getElementById('contentsButton').click();`);
  assert(await evaluate(`document.getElementById('contentsDialog').open`),'contents opens');
  await evaluate(`document.getElementById('contentsDialog').close();document.getElementById('sourcesButton').click();`);
  assert(await evaluate(`document.getElementById('sourcesDialog').open&&document.querySelectorAll('#sourcesList li').length===22&&document.getElementById('methodNote').innerText.length>100`),'sources and honest method accessible');
  await evaluate(`document.getElementById('sourcesDialog').close();`);
 }else if(phase==='behavior'){
  const gate=await evaluate(`(()=>{const before=document.getElementById('counter').innerText;document.querySelector('[data-mode="deep"]').click();return {open:document.getElementById('spoilerDialog').open,before,after:document.getElementById('counter').innerText,contents:document.getElementById('contentsList').innerText,body:document.getElementById('story').innerText}})()`);
  assert(gate.open&&gate.before===gate.after,'cover Deep opens warning without changing position');
  assert(!gate.contents.includes('Чарли хоронит')&&!gate.body.includes('уезжает в Уоррен'),'no ending titles or outcomes before consent');
  await evaluate(`document.querySelector('[data-ending-cancel]').click();`);
  assert(await evaluate(`document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true'`),'cancel preserves Essential');
  await evaluate(`document.getElementById('contentsButton').click();document.querySelector('#dialogModePicker [data-mode="deep"]').click();`);
  assert(await evaluate(`document.getElementById('spoilerDialog').open&&!document.getElementById('contentsDialog').open`),'contents Deep path also guarded');
  await evaluate(`document.querySelector('[data-ending-accept]').click();document.querySelector('#contentsList [data-go-to="algernon-buried"]').click();`);
  assert(await evaluate(`document.querySelector('#story h1').innerText==='Чарли хоронит Элджернона'&&localStorage.getItem('book-tiktok.flowers-for-algernon.lastScreen')==='algernon-buried'`),'consent permits Deep and saves stable ID');
  await load();
  const resume=await evaluate(`({text:document.getElementById('story').innerText,contents:document.getElementById('contentsList').innerText,essential:document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')})`);
  assert(resume.essential==='true'&&!resume.text.includes('Чарли хоронит')&&!resume.contents.includes('Чарли хоронит'),'reload resets Deep consent and masks saved ending label');
  await evaluate(`document.querySelector('[data-start="continue"]').click();`);
  assert(await evaluate(`document.getElementById('spoilerDialog').open`),'saved Deep Continue requires fresh consent');
  await command('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});await command('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27,nativeVirtualKeyCode:27});
  await until(()=>evaluate(`!document.getElementById('spoilerDialog').open`),'native Escape close');
  assert(await evaluate(`!document.getElementById('spoilerDialog').open&&document.querySelector('[data-mode="essential"]').getAttribute('aria-pressed')==='true'`),'Escape declines without changing mode');
  await evaluate(`document.querySelector('[data-start="continue"]').click();document.querySelector('[data-ending-accept]').click();document.getElementById('languageButton').click();document.getElementById('themeButton').click();`);
  assert(await evaluate(`document.querySelector('#story h1').innerText==='Charlie buries Algernon'&&document.documentElement.lang==='en'&&document.documentElement.dataset.theme==='light'`),'language and theme preserve saved Deep position');
  await evaluate(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'f',bubbles:true}));`);
  assert(await evaluate(`document.documentElement.dataset.focusMode==='true'&&document.querySelector('.topbar').getBoundingClientRect().height===0&&document.getElementById('nextButton').getBoundingClientRect().bottom<=innerHeight+1`),'focus hides header and retains safe Next');
  await evaluate(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));document.querySelector('#contentsList [data-go-to="final"]').click();document.getElementById('nextButton').click();`);
  assert(await evaluate(`Boolean(document.querySelector('[data-start]'))&&localStorage.getItem('book-tiktok.flowers-for-algernon.lastScreen')===null`),'final restart clears saved position');
  await evaluate(`document.querySelector('[data-start]').click();document.activeElement?.blur();document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));`);
  assert(await evaluate(`document.querySelector('#story h1').innerText==='What is hidden in the blots?'`),'keyboard next advances the real sequence');
  await evaluate(`document.getElementById('story').dispatchEvent(new PointerEvent('pointerdown',{pointerId:7,clientX:280,clientY:200,bubbles:true}));document.getElementById('story').dispatchEvent(new PointerEvent('pointerup',{pointerId:7,clientX:100,clientY:204,bubbles:true}));`);
  assert(await evaluate(`document.querySelector('#story h1').innerText==='The mouse finishes first'`),'horizontal swipe advances');
  await evaluate(`document.getElementById('story').dispatchEvent(new PointerEvent('pointerdown',{pointerId:8,clientX:140,clientY:200,bubbles:true}));document.getElementById('story').dispatchEvent(new PointerEvent('pointerup',{pointerId:8,clientX:144,clientY:350,bubbles:true}));`);
  assert(await evaluate(`document.querySelector('#story h1').innerText==='The mouse finishes first'&&document.documentElement.dataset.focusMode!=='true'`),'vertical gesture neither pages nor toggles focus');
  const point=await evaluate(`(()=>{const b=document.querySelector('#story p:not(.kicker)').getBoundingClientRect();return {x:b.x+20,y:b.y+10}})()`);
  await command('Input.dispatchMouseEvent',{type:'mousePressed',...point,button:'left',clickCount:1});await command('Input.dispatchMouseEvent',{type:'mouseReleased',...point,button:'left',clickCount:1});
  assert(await evaluate(`document.documentElement.dataset.focusMode==='true'`),'physical text tap enters focus');
  await command('Input.dispatchMouseEvent',{type:'mousePressed',...point,button:'left',clickCount:1});await command('Input.dispatchMouseEvent',{type:'mouseReleased',...point,button:'left',clickCount:1});
  assert(await evaluate(`document.documentElement.dataset.focusMode!=='true'`),'second text tap restores chrome');
 }else if(phase==='ios'){
  const install=await until(()=>evaluate(`document.getElementById('bookLibraryInstallDialog')?.open`),'iOS guide');assert(install,'iPhone browser auto-offers install guide');
  await evaluate(`document.getElementById('bookLibraryInstallDialog').close();document.documentElement.style.setProperty('--reader-safe-top','24px');`);
  const controls=await evaluate(`[...document.querySelectorAll('.topbar a,.topbar button')].filter(n=>n.getBoundingClientRect().width).map(n=>({id:n.id,top:n.getBoundingClientRect().top,right:n.getBoundingClientRect().right,icon:!!n.querySelector('svg'),label:n.getAttribute('aria-label')}))`);
  assert(controls.length===6&&controls.every(n=>n.top>=24&&n.right<=321&&n.icon&&n.label),'six icon controls fit below emulated status inset');
  await command('Page.addScriptToEvaluateOnNewDocument',{source:`Object.defineProperty(navigator,'standalone',{get:()=>true});`});await load();
  assert(await evaluate(`!document.getElementById('bookLibraryInstallDialog').open&&document.getElementById('bookLibraryInstallTrigger').hidden`),'standalone hides install guide and trigger');
 }
 assert(errors.length===0,'zero runtime exceptions');assert(requests.filter(u=>/^https?:/.test(u)).length===0,'zero HTTP runtime requests while offline');
 result.errors=errors;result.httpRequests=requests.filter(u=>/^https?:/.test(u));result.profile=profile;
});
result.profileRemoved=!fs.existsSync(result.profile);if(!result.profileRemoved)throw Error('profile cleanup failed');
fs.writeFileSync(path.join(here,'browser-'+phase+'.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({phase,visits:result.visits,checks:result.checks,profileRemoved:result.profileRemoved}));
