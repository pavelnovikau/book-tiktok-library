import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const dir=path.dirname(fileURLToPath(import.meta.url));
execFileSync('python3',[path.join(dir,'prepare.py')],{stdio:'inherit'});
const out=path.join(dir,'essentialism.html');
process.stdout.write(execFileSync(process.execPath,['/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs',path.join(dir,'story-data.json'),'--out',out],{encoding:'utf8'}));
let h=fs.readFileSync(out,'utf8');
function replace(old,value){if(h.split(old).length!==2)throw Error('Local patch anchor count: '+old.slice(0,100));h=h.replace(old,value)}
replace('const storagePrefix = `book-tiktok.${data.slug}.`;','const storagePrefix = `book-tiktok.${data.slug}.depth-v2.`;');
replace("mode: modeOrder.includes(stored('mode', data.defaultMode || 'deep')) ? stored('mode', data.defaultMode || 'deep') : 'deep',","mode: modeOrder.includes(stored('mode', 'essential')) ? stored('mode', 'essential') : 'essential',");
replace("function text() { return ui[state.language]; }",`// Invalidate stale content IDs without touching old readers or their keys.
      const rawRemembered = stored('lastScreen', '');
      if (rawRemembered && !data.screens.some(s => s.id === rawRemembered && s.type !== 'cover')) {
        removeStored('lastScreen'); removeStored('lastMode'); state.mode = 'essential'; save('mode', 'essential');
      }
      function rememberedScreen() { return data.screens.find(s => s.id === stored('lastScreen', '') && s.type !== 'cover') || null; }
      function rememberedMode(screen) {
        const saved = stored('lastMode', '');
        return modeOrder.includes(saved) && levels[saved] >= screen.level ? saved : requiredMode(screen.level);
      }
      function text() { return ui[state.language]; }`);
replace("const rememberedId = stored('lastScreen', '');\n        const remembered = rememberedId && rememberedId !== screen.id ? data.screens.find((item) => item.id === rememberedId) : null;",'const remembered = rememberedScreen();');
replace("const primaryLabel = resumeHasEnding ? (state.language === 'ru' ? 'Продолжить Deep — спойлеры финала' : 'Continue Deep — ending spoilers') : remembered ? text().continuePrefix + copyOf(remembered).title + text().continueSuffix : text().start;",`const resumeDepth = remembered ? rememberedMode(remembered) : 'essential';
        const primaryLabel = remembered ? (state.language === 'ru' ? 'Продолжить' : 'Continue') + (levels[resumeDepth] > 1 ? ' · ' + modeLabel(resumeDepth) : '') + (state.language === 'ru' ? ': «' : ': “') + copyOf(remembered).title + text().continueSuffix : text().start;`);
replace("if (currentScreen().type !== 'cover') save('lastScreen', currentScreen().id);","if (currentScreen().type !== 'cover') { save('lastScreen', currentScreen().id); save('lastMode', state.mode); }");
replace(`const rememberedId = continueSaved ? stored('lastScreen', '') : '';
        if (rememberedId) goToId(rememberedId);
        else goToPosition(Math.min(1, visibleScreens().length - 1), 'forward');`,`const remembered = continueSaved ? rememberedScreen() : null;
        if (remembered) {
          const destination = rememberedMode(remembered);
          if (levels[destination] > levels[state.mode]) { state.mode = destination; save('mode', destination); }
          goToId(remembered.id);
        } else {
          removeStored('lastScreen'); removeStored('lastMode');
          goToPosition(Math.min(1, visibleScreens().length - 1), 'forward');
        }`);
replace("removeStored('lastScreen');\n          goToPosition(0, 'forward');","removeStored('lastScreen'); removeStored('lastMode');\n          goToPosition(0, 'forward');");
replace(`state.language = state.language === 'ru' ? 'en' : 'ru';
        save('language', state.language);
        render();`,`const oldScroll = els.story.querySelector('.slide-scroll');
        const oldRatio = oldScroll && oldScroll.scrollHeight > oldScroll.clientHeight ? oldScroll.scrollTop / (oldScroll.scrollHeight - oldScroll.clientHeight) : 0;
        const id = currentScreen().id;
        state.language = state.language === 'ru' ? 'en' : 'ru';
        save('language', state.language);
        render();
        const restore = () => { if (currentScreen().id !== id) return; const el=els.story.querySelector('.slide-scroll'); el.scrollTop=oldRatio*Math.max(0,el.scrollHeight-el.clientHeight); };
        restore(); document.fonts.ready.then(() => requestAnimationFrame(restore));`);
replace("start: 'Начать просмотр'","start: 'Начать чтение'");
// The global Sources dialog exposes the exact supplied extraction convention.
const sourceEnd="els.sourcesList.innerHTML = data.sources.map((source) => `<li><a href=\"${escapeHtml(source.url)}\" target=\"_blank\" rel=\"noreferrer\">${escapeHtml(source.title)}</a><span class=\"source-role\">${escapeHtml(text().sourceRoles[source.role] || source.role)}</span><p>${escapeHtml(source.note[state.language])}</p></li>`).join('');";
replace(sourceEnd,sourceEnd+`
        const map=document.createElement('li');
        map.innerHTML='<details id="primary-locations"><summary>'+ (state.language==='ru'?'Главы, файлы и абзацы':'Chapters, files and paragraphs') +'</summary>'+data.unitMap.map(u=>'<p><strong>'+escapeHtml(u.title[state.language])+'</strong><br>'+u.primaryRanges.map(r=>escapeHtml(r.file)+' P'+String(r.start).padStart(3,'0')+'–P'+String(r.end).padStart(3,'0')).join('; ')+'<br>'+u.screens.map(s=>escapeHtml(s.id)+' ['+s.level+']').join(', ')+'</p>').join('')+'</details>';
        els.sourcesList.append(map);`);
replace('</head>',`<style id="essentialism-local-presentation">
/* Book-local typographic cover; the template's generic seven-node model is absent. */
.cover-layout > .cover-visual:not(.has-image) { display:none; }
.cover-layout { display:flex; flex-direction:column; align-items:stretch; justify-content:center; }
.cover-actions { align-self:stretch; }
.source-label { display:none; }
#primary-locations { overflow-wrap:anywhere; }
:root, :root[data-theme="dark"] {
 --color-primary:var(--essentialism-focus,#5B2FC2);
 --color-primary-hover:var(--essentialism-focus-hover,#4B24A4);
 --color-primary-active:var(--essentialism-focus-active,#3E1C8A);
 --color-on-primary:var(--essentialism-paper,#FFFCF0);
 --color-focus-ring:var(--essentialism-ring,#B39AE1);
}
</style>\n</head>`);
fs.writeFileSync(out,h);
console.log('Candidate-local namespace/resume/source-map/presentation patches applied. Shared builder and Settings unchanged.');
