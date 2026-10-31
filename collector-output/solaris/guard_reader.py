# -*- coding: utf-8 -*-
"""Apply Solaris-only volatile spoiler consent after the maintained builder.

No shared/installed shell is changed. Fail closed if its expected anchors drift.
"""
from pathlib import Path

p = Path(__file__).with_name('solaris.html')
h = p.read_text()
if 'SOLARIS_VOLATILE_CONSENT_V1' in h:
    raise SystemExit('Solaris guard already present; rebuild before applying.')

def replace_once(old, new):
    global h
    assert h.count(old) == 1, ('maintained-shell anchor changed', old[:90])
    h = h.replace(old, new, 1)

replace_once('  <dialog id="sourcesDialog">', '''  <!-- SOLARIS_VOLATILE_CONSENT_V1: package-local, never persist consent. -->
  <dialog id="solarisSpoilerDialog" aria-labelledby="solarisSpoilerTitle" aria-describedby="solarisSpoilerCopy">
    <div class="dialog-shell">
      <header class="dialog-header"><h2 id="solarisSpoilerTitle"></h2></header>
      <div class="dialog-body"><p id="solarisSpoilerCopy"></p></div>
      <footer class="dialog-footer">
        <button class="button" id="solarisSpoilerCancel" type="button" autofocus></button>
        <button class="button button-primary" id="solarisSpoilerAccept" type="button"></button>
      </footer>
    </div>
  </dialog>

  <dialog id="sourcesDialog">''')

replace_once('      function text() { return ui[state.language]; }', '''      // SOLARIS_VOLATILE_CONSENT_V1. Stored depth is not consent.
      let deepConsent = false;
      let pendingDeep = null;
      const spoilerDialog = document.getElementById('solarisSpoilerDialog');
      const spoilerCancel = document.getElementById('solarisSpoilerCancel');
      const spoilerAccept = document.getElementById('solarisSpoilerAccept');
      if (state.mode === 'deep') state.mode = 'essential';

      function requestDeepConsent(proceed) {
        if (deepConsent) { proceed(); return; }
        document.querySelectorAll('dialog[open]').forEach((dialog) => dialog.close());
        pendingDeep = proceed;
        const ru = state.language === 'ru';
        document.getElementById('solarisSpoilerTitle').textContent = ru ? 'Открыть сюжет и финал?' : 'Reveal plot and ending?';
        document.getElementById('solarisSpoilerCopy').textContent = ru
          ? 'Deep раскрывает поздние события, решения персонажей и последнюю сцену. В продолжении есть самоубийство и утрата. Подтверждение действует только до перезагрузки или выхода из Deep.'
          : 'Deep reveals later events, the characters’ decisions and the final scene. It includes suicide and loss. Consent lasts only until reload or leaving Deep.';
        spoilerCancel.textContent = ru ? 'Без спойлеров' : 'Keep the ending';
        spoilerAccept.textContent = ru ? 'Открыть Deep' : 'Open Deep';
        spoilerDialog.showModal();
        spoilerCancel.focus({ preventScroll: true });
        spoilerDialog.scrollTop = 0;
      }
      spoilerAccept.addEventListener('click', () => {
        const proceed = pendingDeep;
        pendingDeep = null;
        deepConsent = true;
        spoilerDialog.close();
        if (proceed) proceed();
      });
      spoilerCancel.addEventListener('click', () => {
        pendingDeep = null;
        spoilerDialog.close();
      });
      spoilerDialog.addEventListener('cancel', () => { pendingDeep = null; });
      window.addEventListener('pageshow', (event) => {
        if (!event.persisted) return;
        deepConsent = false;
        pendingDeep = null;
        if (spoilerDialog.open) spoilerDialog.close();
        if (state.mode === 'deep') {
          state.mode = 'essential';
          state.position = 0;
          render();
        }
      });

      function text() { return ui[state.language]; }''')

replace_once('''      function goToPosition(position, direction) {
        const list = visibleScreens();''', '''      function goToPosition(position, direction) {
        const list = visibleScreens();
        if (list[position]?.level === 3 && !deepConsent) {
          requestDeepConsent(() => goToPosition(position, direction));
          return;
        }''')
replace_once('''      function goToId(id) {
        let list = visibleScreens();''', '''      function goToId(id) {
        if (data.screens.some((screen) => screen.id === id && screen.level === 3) && !deepConsent) {
          requestDeepConsent(() => goToId(id));
          return;
        }
        let list = visibleScreens();''')
replace_once('''      function setMode(mode) {
        if (!modeOrder.includes(mode)) return;''', '''      function setMode(mode) {
        if (!modeOrder.includes(mode)) return;
        if (mode === 'deep' && !deepConsent) {
          requestDeepConsent(() => setMode(mode));
          return;
        }
        if (mode !== 'deep') deepConsent = false;''')
p.write_text(h)
print('Solaris-only volatile consent installed; corpus unchanged.')
