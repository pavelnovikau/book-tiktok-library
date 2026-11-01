// Shared integration contract for standalone reader navigation. No story authoring.
import assert from 'node:assert/strict';
export const contractVersion = 'reader-usability-v1';
export function readerData(html) {
  const match = html.match(/<script id="book-tiktok-data"[^>]*>([\s\S]*?)<\/script>/);
  assert(match, 'Missing reader data');
  return { raw: match[1], data: JSON.parse(match[1]) };
}
function arrayEnd(raw, start) {
  let depth = 0, quoted = false, escape = false;
  for (let i = start; i < raw.length; i++) {
    const c = raw[i];
    if (quoted) { if (escape) escape = false; else if (c === '\\') escape = true; else if (c === '"') quoted = false; }
    else if (c === '"') quoted = true;
    else if (c === '[' || c === '{') depth++;
    else if ((c === ']' || c === '}') && --depth === 0) return i + 1;
  }
  throw new Error('Unclosed JSON array');
}
export function repairReader(html, { serviceIds = [] } = {}) {
  if (html.includes('// reader-usability-v1')) { assertReaderUsability(html); return html; }
  const { raw, data } = readerData(html);
  const removed = new Set(serviceIds);
  for (const id of removed) {
    const s = data.screens.find(s => s.id === id);
    assert(s && (s.kind === 'notice' || ['deep-warning', 'deep-notice'].includes(id)), `Unverified service screen ${id}`);
  }
  const grouped = {};
  for (let i = 0; i < data.screens.length - 1; i++) {
    const screen = data.screens[i], target = data.screens[i + 1];
    if (!removed.has(screen.id) && screen.type !== 'cover' && screen.headingLevel === 1 &&
        !screen.copy.ru.body.trim() && !screen.copy.en.body.trim()) {
      assert(target.copy.ru.body.trim() && target.copy.en.body.trim() && target.routeMode === screen.routeMode, 'Title must prefix actual prose in the same route');
      grouped[screen.id] = target.id;
    }
  }
  let next = raw.replace(/("defaultMode"\s*:\s*)"[^"]*"/, '$1"deep"');
  // Keep every retained serialized screen object byte for byte, including escaping.
  const screenStart = next.indexOf('[', next.indexOf('"screens"'));
  const screenEnd = arrayEnd(next, screenStart);
  const items = []; let cursor = screenStart + 1;
  while (cursor < screenEnd - 1) {
    while (/[\s,]/.test(next[cursor])) cursor++;
    if (cursor >= screenEnd - 1) break;
    const end = arrayEnd(next, cursor), item = next.slice(cursor, end);
    if (!removed.has(JSON.parse(item).id)) items.push(item);
    cursor = end;
  }
  next = next.slice(0, screenStart) + '[' + items.join(',') + ']' + next.slice(screenEnd);
  if (data.routes) for (const [mode, ids] of Object.entries(data.routes)) {
    if (!Array.isArray(ids)) continue;
    const routesAt = next.indexOf('"routes"');
    const key = new RegExp('"' + mode + '"\\s*:\\s*\\[').exec(next.slice(routesAt));
    const start = routesAt + key.index + key[0].lastIndexOf('['), end = arrayEnd(next, start);
    next = next.slice(0, start) + JSON.stringify(ids.filter(id => !removed.has(id))) + next.slice(end);
  }
  html = html.replace(raw, () => next);
  html = html.replace(/(<meta name="book-tiktok:screens" content=")\d+("\s*\/?>)/, (_, a, b) => a + (data.screens.length - removed.size - Object.keys(grouped).length) + b);
  const retained = data.screens.filter(s => !removed.has(s.id) && !grouped[s.id]);
  const modes = Object.keys(data.modes);
  const modeCounts = modes.map(mode => Array.isArray(data.routes?.[mode]) ? data.routes[mode].filter(id => !removed.has(id) && !grouped[id]).length : data.routes?.[mode]?.screenIds ? 1 + data.routes[mode].screenIds.filter(id => !grouped[id]).length : retained.filter(s => data.screens.some(s => s.routeMode) ? !s.routeMode || s.routeMode === mode : s.level <= ({essential:1,core:2,deep:3})[mode]).length);
  html = html.replace(/(<meta name="book-tiktok:modes" content=")[^"]+("\s*\/?>)/, (_, a, b) => a + modeCounts.join(',') + b);
  const start = html.indexOf("      const data = JSON.parse(document.getElementById('book-tiktok-data')");
  const end = html.indexOf('    })();', start);
  assert(start >= 0 && end >= 0, 'Unsupported reader closure');
  let runtime = html.slice(start, end);
  const needsConsent = data.spoilerPolicy === 'full-plot-in-deep' || /requestDeep|requestSpoilers/.test(runtime);
  const stateEnd = runtime.indexOf('\n      };', runtime.indexOf('      const state =')) + '\n      };'.length;
  assert(stateEnd > 20);
  const textAt = runtime.indexOf('      function text()');
  assert(textAt > stateEnd);
  runtime = runtime.slice(0, stateEnd) + '\n' + integration(needsConsent, grouped, Object.fromEntries(serviceIds.map(id => {
    const screen = data.screens.find(s => s.id === id);
    return [id, screen.routeMode || (screen.level === 3 ? 'deep' : screen.level === 2 ? 'core' : 'essential')];
  }))) + '\n' + runtime.slice(textAt);
  runtime = runtime.replace(/mode: modeOrder.includes\(stored\('mode', [^\n]+/, "mode: modeOrder.includes(stored('mode', 'deep')) ? stored('mode', 'deep') : 'deep',");
  function replaceFunction(name, body) {
    const re = new RegExp('      function ' + name + '\\([^\\n]*\\{[^\\n]*\\}\\n|      function ' + name + '\\([^\\n]*\\{[\\s\\S]*?\\n      }', 'g');
    assert(re.test(runtime), `Missing ${name}`); re.lastIndex = 0;
    runtime = runtime.replace(re, () => body + '\n');
  }
  for (const [name, body] of Object.entries(navigation)) replaceFunction(name, body);
  replaceFunction('visibleScreens', `      function visibleScreens() { return routeScreens(state.mode); }`);
  replaceFunction('modeCounts', `      function modeCounts() { return Object.fromEntries(modeOrder.map(mode => [mode, routeScreens(mode).length])); }`);
  replaceFunction('bindRenderedControls', `      function bindRenderedControls() {
        document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode)));
        document.querySelectorAll('[data-go-to]').forEach(button => button.addEventListener('click', () => {
          goToId(button.dataset.goTo); if (els.contentsDialog.open) els.contentsDialog.close();
        }));
        document.querySelectorAll('[data-start]').forEach(button => button.addEventListener('click', () => start(button.dataset.start === 'continue')));
        document.querySelectorAll('[data-open-sources]').forEach(button => button.addEventListener('click', () => els.sourcesDialog.showModal()));
      }`);
  runtime = runtime.replace(/        els.story.dataset.(?:mode|screenId) = [^\n]*\n/g, '').replace(/        syncHash\(\);\n/g, '');
  runtime = runtime.replace('els.story.innerHTML = renderScreen(currentScreen());', "els.story.innerHTML = renderScreen(currentScreen());\n        els.story.dataset.mode = state.mode;\n        els.story.dataset.screenId = currentScreen().id;\n        syncHash();");
  runtime = runtime.replace(/        if \(state.mode === 'deep' && !(?:uxConsent|deepConsent)\) \{ state.mode = 'essential'; state.position = 0; \}\n/g, '');
  runtime = runtime.replace(/function renderScreen\(screen\) \{[\s\S]*?\n      }/, block => block.replace('${copy.title ?', '${prefixHeading(screen)}${copy.title ?'));
  // Existing cover graphics and copy stay intact; only resolve safe saved targets.
  runtime = runtime.replace(/const remembered = rememberedId && rememberedId !== screen.id \? data.screens.find\(\(item\) => item.id === rememberedId\) : null;/g, 'const remembered = rememberedScreen();');
  runtime = runtime.replace(/const primaryLabel = ([^\n]+);/g, (match, expression) => `const primaryLabel = needsConsent && !uxConsent && remembered && rememberedMode(remembered) === 'deep' ? (state.language === 'ru' ? 'Продолжить полную версию' : 'Continue full version') : (${expression});`);
  runtime = runtime.replace(/function contentsHtml\(\) \{[\s\S]*?\n      }/, block => block.replace('const list = data.screens;', 'const list = visibleScreens();').replace(/copyOf\(screen\).title \|\| copyOf\(screen\).tocTitle|copyOf\(screen\).title/g, 'safeTitle(screen)'));
  // Keep older title masking wired to the shared document-local consent.
  runtime = runtime.replace(/\bdeepConsent\b|\bspoilersAccepted\b/g, 'uxConsent');
  runtime = runtime.replace(/^        updateSpoilerText\(\);\n/gm, '');
  // Older candidates may install entry handlers between rendering helpers.
  // Remove their hash/query-entry blocks; shared startup below handles both.
  runtime = runtime.replace(/      \/\/ (?:Explicit|URL|Deep-link)[^\n]*\n/g, '');
  const marker = "      els.story.addEventListener('pointercancel', () => { pointerStart = null; });";
  const tail = runtime.indexOf(marker); assert(tail >= 0);
  runtime = runtime.slice(0, tail + marker.length) + '\n\n' + startup;
  // Extra candidate-local hash entry blocks occur before renderCover in two families.
  runtime = runtime.replace(/      const entryParams[\s\S]*?(?=      function )/g, '');
  runtime = runtime.replace(/      const requestedMode[\s\S]*?(?=      function )/g, '');
  html = html.slice(0, start) + runtime + html.slice(end);
  // Reuse a single generic dialog; no obsolete plot-bearing dialog remains.
  html = html.replace(/\s*<dialog\b[^>]*id="(?:spoilerDialog|deepConsentDialog|depthConsent)"[\s\S]*?<\/dialog>/g, '');
  if (needsConsent) html = html.replace('<script id="book-tiktok-data"', consentMarkup + '\n  <script id="book-tiktok-data"');
  assertReaderUsability(html);
  return html;
}
export function assertReaderUsability(html) {
  const { data } = readerData(html);
  assert.equal(data.defaultMode, 'deep', 'Fresh readers must default to Deep');
  assert(!data.screens.some(s => s.kind === 'notice' || ['deep-warning', 'deep-notice'].includes(s.id)), 'Service-only pages must not enter a reading route');
  assert(html.includes("mode: modeOrder.includes(stored('mode', 'deep')) ? stored('mode', 'deep') : 'deep',"), 'Runtime fallback must select Deep');
  assert(html.includes('// reader-usability-v1'), 'Missing maintained navigation integration');
  assert(!/if\s*\(state.mode\s*===?\s*'deep'\)\s*state.mode\s*=\s*'(essential|brief)'/.test(html), 'Startup must not downgrade Deep');
}
const consentMarkup = `<dialog id="readerConsent" aria-labelledby="readerConsentTitle" aria-describedby="readerConsentText"><div class="dialog-card"><header class="dialog-header"><h2 id="readerConsentTitle"></h2></header><div class="dialog-body"><p id="readerConsentText"></p></div><div class="dialog-actions"><button class="button" type="button" id="readerConsentCancel"></button><button class="button button-primary" type="button" id="readerConsentAccept"></button></div></div></dialog>`;
function integration(needsConsent, grouped, redirects) { return `
      // reader-usability-v1: selected depth and spoiler permission are separate.
      const initialHash = location.hash;
      const serviceRedirects = ${JSON.stringify(redirects)};
      const needsConsent = ${needsConsent};
      const groupedTitles = ${JSON.stringify(grouped)};
      let uxConsent = false;
      let pendingEntry = null;
      const consentDialog = document.getElementById('readerConsent');
      function rawRouteScreens(mode) {
        if (Array.isArray(data.routes?.[mode])) return data.routes[mode].map(id => data.screens.find(s => s.id === id));
        if (data.screens.some(s => s.routeMode)) return data.screens.filter(s => !s.routeMode || s.routeMode === mode);
        return data.screens.filter(s => s.level <= levels[mode]);
      }
      function routeScreens(mode) { return rawRouteScreens(mode).filter(s => !groupedTitles[s.id]); }
      function prefixHeading(screen) {
        return Object.entries(groupedTitles).filter(([, target]) => target === screen.id).map(([id]) => '<h1 data-heading>' + escapeHtml(copyOf(data.screens.find(s => s.id === id)).title) + '</h1>').join('');
      }
      function firstProse(mode) { return routeScreens(mode).find(s => s.type !== 'cover'); }
      function resolveScreen(id, mode = state.mode) {
        if (Object.hasOwn(groupedTitles, id)) id = groupedTitles[id];
        if (Object.hasOwn(serviceRedirects, id)) return firstProse(serviceRedirects[id]);
        return data.screens.find(s => s.id === id) || firstProse(mode);
      }
      function rememberedScreen() {
        const id = stored('lastScreen', '');
        return id ? resolveScreen(id) : null;
      }
      function rememberedMode(screen) {
        const oldId = stored('lastScreen', '');
        if (Object.hasOwn(serviceRedirects, oldId)) return serviceRedirects[oldId];
        const candidate = stored('lastMode', state.mode);\n        const saved = modeOrder.includes(candidate) ? candidate : state.mode;
        return screen.routeMode || (routeScreens(saved).includes(screen) ? saved : requiredMode(screen.level));
      }
      function safeTitle(screen) {
        return needsConsent && state.mode === 'deep' && !uxConsent && screen.type !== 'cover'
          ? (state.language === 'ru' ? 'Полная версия' : 'Full version') : (copyOf(screen).title || copyOf(screen).tocTitle || '');
      }
      function syncHash() {
        try { history.replaceState(null, '', '#' + state.mode + '/' + currentScreen().id); } catch (_) {}
      }
      function changeMode(mode) {
        if (mode !== 'deep') uxConsent = false;
        state.mode = mode; state.position = 0; save('mode', mode);
      }
      function requestEntry(mode, id, direction = 'forward') {
        const target = routeScreens(mode).find(s => s.id === id) || firstProse(mode);
        const enter = () => {
          if (mode !== state.mode) changeMode(mode);
          state.position = routeScreens(mode).indexOf(target);
          state.direction = direction; render();
        };
        if (needsConsent && mode === 'deep' && target.type !== 'cover' && !uxConsent) {
          pendingEntry = enter;
          if (els.contentsDialog.open) els.contentsDialog.close();
          if (els.sourcesDialog.open) els.sourcesDialog.close();
          const ru = state.language === 'ru';
          document.getElementById('readerConsentTitle').textContent = ru ? 'Полная версия' : 'Full version';
          document.getElementById('readerConsentText').textContent = ru ? 'Полная версия раскрывает развязку. Читать?' : 'The full version reveals the ending. Read on?';
          document.getElementById('readerConsentCancel').textContent = ru ? 'Отмена' : 'Cancel';
          document.getElementById('readerConsentAccept').textContent = ru ? 'Читать' : 'Read';
          if (!consentDialog.open) consentDialog.showModal();
          document.getElementById('readerConsentCancel').focus({preventScroll:true});
        } else enter();
      }
      if (consentDialog) {
        document.getElementById('readerConsentAccept').addEventListener('click', () => {
          const action = pendingEntry; pendingEntry = null; uxConsent = true;
          consentDialog.close(); if (action) action();
        });
        const cancel = () => { pendingEntry = null; consentDialog.close(); syncHash(); };
        document.getElementById('readerConsentCancel').addEventListener('click', cancel);
        consentDialog.addEventListener('cancel', () => { pendingEntry = null; syncHash(); });
      }
      function followEntry(hash, useQuery = false) {
        const parts = String(hash).replace(/^#/, '').split('/');
        const params = new URLSearchParams(useQuery ? location.search : '');
        const mode = modeOrder.includes(parts[0]) ? parts[0] : (params.get('mode') || state.mode);
        if (!modeOrder.includes(mode)) return;
        const requested = parts[1] || params.get('screen') || (parts[0] && !modeOrder.includes(parts[0]) ? parts[0] : firstProse(mode).id);
        const screen = resolveScreen(requested, mode);
        const targetMode = Object.hasOwn(serviceRedirects, requested) ? serviceRedirects[requested] : (screen.routeMode || mode);
        requestEntry(targetMode, screen.id);
      }
`; }
const navigation = {
  goToPosition: `      function goToPosition(position, direction) {
        const list = visibleScreens();
        const target = list[Math.max(0, Math.min(position, list.length - 1))];
        requestEntry(state.mode, target.id, direction);
      }`,
  goToId: `      function goToId(id) {
        const screen = resolveScreen(id);
        const mode = screen.routeMode || (visibleScreens().includes(screen) ? state.mode : requiredMode(screen.level));
        requestEntry(mode, screen.id);
      }`,
  setMode: `      function setMode(mode) {
        if (!modeOrder.includes(mode) || mode === state.mode) return;
        removeStored('lastScreen');
        const id = currentScreen().id;
        changeMode(mode);
        // Independent versions always begin at their cover. Cumulative readers
        // retain a shared page only when it does not bypass renewed consent.
        if (!data.routes && !data.screens.some(s => s.routeMode) && !(needsConsent && mode === 'deep')) {
          const index = visibleScreens().findIndex(s => s.id === id);
          if (index >= 0) state.position = index;
        }
        render();
      }`,
  start: `      function start(continueSaved) {
        const remembered = continueSaved ? rememberedScreen() : null;
        if (remembered) requestEntry(rememberedMode(remembered), remembered.id);
        else requestEntry(state.mode, firstProse(state.mode).id);
      }`
};
const startup = `      render();
      if (initialHash || new URLSearchParams(location.search).has('mode') || new URLSearchParams(location.search).has('screen')) followEntry(initialHash, true);
      window.addEventListener('hashchange', () => followEntry(location.hash));
      window.addEventListener('pagehide', () => { uxConsent = false; });
      window.addEventListener('pageshow', event => {
        if (!event.persisted) return;
        uxConsent = false; pendingEntry = null;
        if (consentDialog?.open) consentDialog.close();
        state.position = 0; render();
      });

`;
