import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));
const out=path.join(dir,'selfie.html');
process.stdout.write(execFileSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs',path.join(dir,'story-data.json'),'--out',out],{encoding:'utf8'}));
let h=fs.readFileSync(out,'utf8');
const replace=(a,b)=>{if(h.split(a).length!==2)throw Error('Patch anchor count: '+a.slice(0,90));h=h.replace(a,b)};
replace('</head>',`<style id="selfie-typographic-cover">
.cover-layout > .cover-visual:not(.has-image) { display:none; }
.cover-layout { display:flex; flex-direction:column; align-items:stretch; justify-content:center; }
.cover-actions { align-self:stretch; }
.story-slide h1 { overflow-wrap:anywhere; }
</style>\n</head>`);
replace('const storagePrefix = `book-tiktok.${data.slug}.`;','const storagePrefix = `book-tiktok.${data.slug}.depth-v2.`;');
const line=h.split('\n').find(l=>l.includes('const primaryLabel ='));
if(!line)throw Error('Resume label missing');
const expression=line.trim().slice('const primaryLabel = '.length,-1);
replace(line,'        const rememberedMode = remembered ? modeOrder[remembered.level - 1] : state.mode;\n'+
'        const primaryLabel = remembered && remembered.level > levels[state.mode] ? (state.language === "ru" ? "Продолжить в режиме «" + data.modes[rememberedMode].label.ru + "»" : "Continue in " + data.modes[rememberedMode].label.en) : ('+expression+');');
const pattern=/(<script id="book-tiktok-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
const m=h.match(pattern);if(!m)throw Error('Embedding missing');
const d=JSON.parse(m[2]);
for(const mode of Object.values(d.modes)){
 const n=parseInt(mode.minutes.ru,10),word=n%100>=11&&n%100<=14?'минут':n%10===1?'минута':n%10>=2&&n%10<=4?'минуты':'минут';
 mode.minutes.ru=`${n} ${word}`;
}
h=h.replace(pattern,(_,a,b,c)=>a+JSON.stringify(d,null,2).replaceAll('<','\\u003c')+c);
fs.writeFileSync(out,h);
