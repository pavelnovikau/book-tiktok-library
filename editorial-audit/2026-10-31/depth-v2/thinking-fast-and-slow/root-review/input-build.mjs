import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));const out=path.join(dir,'thinking-fast-and-slow.html');
process.stdout.write(execFileSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs',path.join(dir,'story-data.json'),'--out',out],{encoding:'utf8'}));
// Candidate-local presentation only: the maintained shell's generic seven-node
// "one model to take away" cover is unrelated to Kahneman's actual argument.
// Hide that default decoration and use its real bilingual title/copy as a
// typographic cover. Settings, header, source dialog and state code are intact.
const css=`<style id="kahneman-typographic-cover">
.cover-layout > .cover-visual:not(.has-image) { display: none; }
.cover-layout { display: flex; flex-direction: column; align-items: stretch; justify-content: center; }
.cover-actions { align-self: stretch; }
</style>\n`;
let h=fs.readFileSync(out,'utf8');if(!h.includes('</head>'))throw Error('head marker');fs.writeFileSync(out,h.replace('</head>',css+'</head>'));
