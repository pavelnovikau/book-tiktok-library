#!/usr/bin/env node
// Book-local consent adapter. The installed builder and shared Settings stay read-only.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
const dir = path.dirname(fileURLToPath(import.meta.url));
const builder = process.env.BOOK_TIKTOK_BUILDER || '/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs';
const out = path.join(dir, 'i-robot.html');
execFileSync(process.execPath, [builder, path.join(dir, 'story-data.json'), '--out', out], { stdio: 'inherit' });
let s = fs.readFileSync(out, 'utf8');
function once(old, replacement) {
  if (s.split(old).length !== 2) throw new Error('Book-local adapter needs exactly one anchor: ' + old.slice(0,90));
  s = s.replace(old, replacement);
}
once('  <script id="book-tiktok-data"', `  <!-- i-robot-local-consent:v2 — volatile; never persisted -->
  <style>
    #deepConsentDialog { width: min(calc(100% - var(--space-6)), 32rem); }
    #deepConsentDialog .dialog-body p { font: 400 var(--text-base)/1.5 var(--font-sans); }
    .deep-ack { display: flex; gap: var(--space-3); align-items: flex-start; padding: var(--space-3) 0; font: 400 var(--text-sm)/1.5 var(--font-sans); }
    .deep-ack input { min-width: var(--space-5); min-height: var(--space-5); accent-color: var(--color-primary); }
    #deepConsentDialog .dialog-footer { display: flex; gap: var(--space-3); flex-wrap: wrap; }
    #deepConsentDialog button:disabled { opacity: .5; cursor: default; }
    #deepConsentDialog .dialog-footer button { min-height: 44px; }
    #story h1:focus { outline: none; }
  </style>
  <dialog id="deepConsentDialog" aria-labelledby="deepConsentTitle" aria-describedby="deepConsentNotice">
    <div class="dialog-shell">
      <header class="dialog-header"><h2 id="deepConsentTitle"></h2></header>
      <div class="dialog-body"><p id="deepConsentNotice"></p>
        <label class="deep-ack"><input id="deepAcknowledgment" type="checkbox"><span id="deepAcknowledgmentLabel"></span></label>
      </div>
      <footer class="dialog-footer">
        <button class="button" type="button" id="deepCancel" autofocus></button>
        <button class="button button-primary" type="button" id="deepConfirm" disabled></button>
      </footer>
    </div>
  </dialog>
  <script id="book-tiktok-data"`);
once('      function text() { return ui[state.language]; }', `      // Only this document lifetime can authorize Deep. Reload/downgrade revoke it.
      let deepAcknowledged = false;
      let pendingDeep = null;
      let consentFocus = null;
      const deepDialog = document.getElementById('deepConsentDialog');
      const deepCheck = document.getElementById('deepAcknowledgment');
      const deepConfirm = document.getElementById('deepConfirm');
      const revision = '2026-10-31-narrative-pass2';
      if (stored('narrativeRevision', '') !== revision) {
        removeStored('lastScreen'); // old analytical IDs never resume into new prose
        state.mode = 'essential';
        save('narrativeRevision', revision);
      }
      if (!data.screens.some(screen => screen.id === stored('lastScreen', ''))) removeStored('lastScreen');
      if (state.mode === 'deep') state.mode = 'essential';
      save('mode', state.mode);
      function consentCopy() {
        const ru = state.language === 'ru';
        document.getElementById('deepConsentTitle').textContent = ru ? 'Deep раскрывает развязки' : 'Deep reveals the resolutions';
        document.getElementById('deepConsentNotice').textContent = ru
          ? 'Deep содержит решения загадок всех девяти рассказов и финал сборника. Заголовки оглавления и текст этого режима могут раскрывать сюжет. Согласие действует до перезагрузки страницы или перехода в Essential/Core.'
          : 'Deep contains the solutions to all nine stories and the collection’s ending. Its contents titles and reading text may reveal the plot. Consent lasts until this page reloads or you switch to Essential/Core.';
        document.getElementById('deepAcknowledgmentLabel').textContent = ru ? 'Понимаю, что увижу развязки и финал.' : 'I understand that I will see solutions and the ending.';
        document.getElementById('deepCancel').textContent = ru ? 'Остаться без спойлеров' : 'Stay without spoilers';
        deepConfirm.textContent = ru ? 'Открыть Deep' : 'Open Deep';
      }
      function requestDeep(action) {
        if (deepAcknowledged) { action(); return; }
        if (pendingDeep) return;
        pendingDeep = action;
        consentFocus = document.activeElement;
        deepCheck.checked = false;
        deepConfirm.disabled = true;
        consentCopy();
        deepDialog.showModal();
        document.getElementById('deepCancel').focus();
      }
      function cancelDeep() {
        pendingDeep = null;
        deepCheck.checked = false;
        deepConfirm.disabled = true;
        deepDialog.close();
        if (consentFocus?.isConnected && !consentFocus.closest('dialog:not([open])')) consentFocus.focus({preventScroll:true});
        else els.contentsButton.focus({preventScroll:true});
      }
      deepDialog.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        const controls = [deepCheck, document.getElementById('deepCancel'), deepConfirm].filter(node => !node.disabled);
        const first = controls[0], last = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
      deepCheck.addEventListener('change', () => { deepConfirm.disabled = !deepCheck.checked; });
      document.getElementById('deepCancel').addEventListener('click', cancelDeep);
      deepDialog.addEventListener('cancel', event => { event.preventDefault(); cancelDeep(); });
      deepConfirm.addEventListener('click', () => {
        if (!deepCheck.checked || !pendingDeep) return;
        const action = pendingDeep;
        pendingDeep = null;
        deepAcknowledged = true;
        deepDialog.close();
        deepCheck.checked = false;
        deepConfirm.disabled = true;
        action();
        const heading = els.story.querySelector('h1');
        if (heading) { heading.tabIndex = -1; heading.focus({preventScroll:true}); }
      });
      window.addEventListener('pageshow', event => {
        if (!event.persisted) return;
        deepAcknowledged = false;
        cancelDeep();
        state.mode = 'essential'; state.position = 0;
        save('mode', 'essential');
        render();
      });
      function text() { return ui[state.language]; }`);
once('      function render() {\n        const list = visibleScreens();', `      function render() {
        if (state.mode === 'deep' && !deepAcknowledged) { state.mode = 'essential'; state.position = 0; }
        consentCopy();
        const list = visibleScreens();`);
once('      function goToId(id) {\n        let list = visibleScreens();', `      function goToId(id) {
        const target = data.screens.find(screen => screen.id === id);
        if (target?.level === 3 && !deepAcknowledged) { requestDeep(() => goToId(id)); return; }
        let list = visibleScreens();`);
once('        if (!modeOrder.includes(mode)) return;\n        const currentId = currentScreen().id;', `        if (!modeOrder.includes(mode)) return;
        if (mode === 'deep' && !deepAcknowledged) { requestDeep(() => setMode(mode)); return; }
        if (mode !== 'deep') deepAcknowledged = false;
        const currentId = currentScreen().id;`);
// Replace the generic seven-node analytical cover with this collection's actual nine stories.
const a = s.indexOf('const visual = coverMediaFor(screen) || `');
const b = s.indexOf('`;\n        return `<article', a);
if (a < 0 || b < 0) throw new Error('Missing maintained cover anchor');
s = s.slice(0,a) + 'const visual = coverMediaFor(screen) || `<div class="cover-visual" role="img" aria-label="${state.language === \'ru\' ? \'Девять рассказов, 1950 год\' : \'Nine stories, 1950\'}"><div class="cover-mark"><span class="cover-eyebrow">1950</span><div class="hero-number">9</div><span class="cover-eyebrow">${state.language === \'ru\' ? \'РАССКАЗОВ\' : \'STORIES\'}</span></div></div>' + s.slice(b);
fs.writeFileSync(out, s);
console.log('I, Robot: installed builder + book-local volatile Deep consent; shared files unchanged.');
