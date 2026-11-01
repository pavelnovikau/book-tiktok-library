import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));const out=path.join(dir,'a-guide-to-the-good-life.html');
process.stdout.write(execFileSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs',path.join(dir,'story-data.json'),'--out',out],{encoding:'utf8'}));
// Candidate-local presentation only: the maintained shell's generic seven-node
// "one model to take away" cover is unrelated to Irvine's actual argument.
// Hide that default decoration and use its real bilingual title/copy as a
// typographic cover. Settings, header, source dialog and state code are intact.
const css=`<style id="irvine-typographic-cover">
.cover-layout > .cover-visual:not(.has-image) { display: none; }
.cover-layout { display: flex; flex-direction: column; align-items: stretch; justify-content: center; }
.cover-actions { align-self: stretch; }
</style>\n`;
let h=fs.readFileSync(out,'utf8');if(!h.includes('</head>'))throw Error('head marker');h=h.replace('</head>',css+'</head>');
// Expanded content gets a fresh book-progress namespace; global Settings persist.
const prefix='const storagePrefix = `book-tiktok.${data.slug}.`;';
if(h.split(prefix).length!==2)throw Error('Expected one progress namespace');
h=h.replace(prefix,'const storagePrefix = `book-tiktok.${data.slug}.depth-v2.`;');
// Continue explicitly names a deeper route before it changes the selected mode.
const resumeLine=h.split('\n').find(line=>line.includes('const primaryLabel ='));
if(!resumeLine||h.split(resumeLine).length!==2)throw Error('Expected one resume label');
const oldExpression=resumeLine.trim().slice('const primaryLabel = '.length,-1);
h=h.replace(resumeLine,
 '        const rememberedMode = remembered ? modeOrder[remembered.level - 1] : state.mode;\n'+
 '        const primaryLabel = remembered && remembered.level > modeOrder.indexOf(state.mode) + 1 ? (state.language === "ru" ? "Продолжить в режиме «" + data.modes[rememberedMode].label.ru + "»" : "Continue in " + data.modes[rememberedMode].label.en) : ('+oldExpression+');');
// Book-local time inflection; the installed builder is read-only.
const pattern=/(<script id="book-tiktok-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
const match=h.match(pattern);if(!match)throw Error('Missing embedded data');
const embedded=JSON.parse(match[2]);
for(const mode of Object.values(embedded.modes)){
 const n=Number.parseInt(mode.minutes.ru,10);if(!Number.isInteger(n))throw Error('Invalid reading minutes');
 const word=n%100>=11&&n%100<=14?'минут':n%10===1?'минута':n%10>=2&&n%10<=4?'минуты':'минут';
 mode.minutes.ru=`${n} ${word}`;
}
h=h.replace(pattern,(_,a,b,c)=>a+JSON.stringify(embedded,null,2).replaceAll('<','\\u003c')+c);
fs.writeFileSync(out,h);
