// Execute the released navigation helpers in isolation; no browser/layout claims.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {readerData,assertReaderUsability} from '../skills/book-tiktok/scripts/reader-usability.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const catalogue=JSON.parse(fs.readFileSync(path.join(root,'books.json'),'utf8'));
for(const book of catalogue.books){
 const html=fs.readFileSync(path.join(root,book.file),'utf8');assertReaderUsability(html);
 const {data}=readerData(html), nodes=new Map(), values=new Map();
 const node=id=>{if(!nodes.has(id))nodes.set(id,{open:false,textContent:'',focus(){},close(){this.open=false},showModal(){this.open=true},addEventListener(name,handler){this[name]=handler}});return nodes.get(id)};
 const hasConsent=html.includes('id="readerConsent"');
 const context=vm.createContext({data,state:{mode:'deep',position:0,language:'ru'},modeOrder:Object.keys(data.modes),levels:{essential:1,core:2,deep:3},location:{hash:'',search:''},history:{replaceState(){}},URLSearchParams,
 document:{getElementById:id=>id==='readerConsent'&&!hasConsent?null:node(id)},els:{contentsDialog:node('contents'),sourcesDialog:node('sources')},
 stored:(key,fallback)=>values.get(key)||fallback,save:(key,value)=>values.set(key,value),removeStored:key=>values.delete(key),render(){},
 copyOf:s=>s.copy.ru,escapeHtml:s=>String(s),requiredMode:level=>level<=1?'essential':level===2?'core':'deep'});
 const helpers=html.slice(html.indexOf('      // reader-usability-v1'),html.indexOf('      function text()',html.indexOf('      // reader-usability-v1')));
 const functions=['goToId','goToPosition','setMode','start'].map(name=>html.match(new RegExp('      function '+name+'\\([^\\n]*\\{[\\s\\S]*?\\n      }'))[0]).join('\n');
 vm.runInContext(helpers+`\nfunction visibleScreens(){return routeScreens(state.mode)}\nfunction currentScreen(){return visibleScreens()[state.position]}\n`+functions,context);
 const run=code=>vm.runInContext(code,context);
 const expectedCount=data.screens.length-Object.keys(run('groupedTitles')).length;
 assert.equal(book.screenCount,expectedCount,book.file+' canonical count');
 const counts=run('modeOrder.map(m=>routeScreens(m).length).join(",")');
 assert.equal(html.match(/name="book-tiktok:modes" content="([^"]+)"/)[1],counts,book.file+' mode metadata');
 for(const mode of Object.keys(data.modes)){
  const first=run(`firstProse(${JSON.stringify(mode)})`);assert(first.copy.ru.body&&first.copy.en.body,book.file+' first prose');
 }
 for(const mode of Object.keys(data.modes)) {
  context.state.mode=mode;
  const first=run(`firstProse(${JSON.stringify(mode)})`);
  if(mode!=='deep') assert.equal(run(`safeTitle(firstProse(${JSON.stringify(mode)}))`),first.copy.ru.title||first.copy.ru.tocTitle||'',book.file+' shallow Contents must retain titles');
  else if(hasConsent) assert.equal(run(`safeTitle(firstProse('deep'))`),'Полная версия',book.file+' Deep must mask titles before consent');
 }
 context.state.mode='deep';
 if(hasConsent) assert(html.includes("remembered && rememberedMode(remembered) === 'deep' ?"),book.file+' Continue label must match remembered depth');
 run('start(false)');
 if(hasConsent){assert(node('readerConsent').open,book.file+' start consent');assert.equal(context.state.position,0);node('readerConsentAccept').click();}
 assert(context.state.position>0,book.file+' start enters prose');
 const shallow=Object.keys(data.modes).find(m=>m!=='deep');
 run(`setMode(${JSON.stringify(shallow)});setMode('deep');start(false)`);
 if(hasConsent){assert(node('readerConsent').open,book.file+' downgrade revokes');node('readerConsentCancel').click();assert.equal(context.state.position,0);assert.equal(context.state.mode,'deep');}
 const late=run('routeScreens("deep").at(-1)');values.set('lastScreen',late.id);
 run('start(true)');if(hasConsent){assert(node('readerConsent').open);node('readerConsentAccept').click();}assert.equal(run('currentScreen().id'),late.id);
 for(const [oldId,mode]of Object.entries(run('serviceRedirects'))){assert.equal(run(`resolveScreen(${JSON.stringify(oldId)}).id`),run(`firstProse(${JSON.stringify(mode)}).id`));values.set('lastScreen',oldId);assert.equal(run('rememberedMode(rememberedScreen())'),mode);}
 for(const [oldId,nextId]of Object.entries(run('groupedTitles'))){assert.equal(run(`resolveScreen(${JSON.stringify(oldId)}).id`),nextId);assert(!run('visibleScreens()').some(s=>s.id===oldId));}
}
console.log(`Reader navigation regressions passed: ${catalogue.books.length} released runtimes, mode counts, first prose, consent, downgrade, late Continue and legacy IDs.`);
