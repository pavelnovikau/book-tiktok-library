import fs from 'node:fs';

const asset = name => fs.readFileSync(new URL(`../assets/${name}`, import.meta.url), 'utf8');
const font = (family, file, weight = '400') => `@font-face { font-family: "${family}"; src: url("data:font/woff2;base64,${fs.readFileSync(new URL(`../assets/fonts/${file}`, import.meta.url)).toString('base64')}") format("woff2"); font-weight: ${weight}; font-style: normal; font-display: swap; }`;

export function settingsHead({ includeSans = false } = {}) {
  const faces = [font('Geist Serif', 'GeistSerif-Regular.woff2'), font('Source Serif 4', 'SourceSerif4-Regular.woff2')];
  if (includeSans) faces.push(font('Geist', 'Geist-Variable.woff2', '100 900'), font('Geist Mono', 'GeistMono-Variable.woff2', '100 900'));
  // Standalone redistribution travels with full, unmodified font licenses.
  const licenses = ['LICENSE.txt', 'GeistSerif-LICENSE.txt', 'SourceSerif4-LICENSE.md'].map(name => `<script type="text/plain" data-font-license="${name}">\n${asset(`fonts/${name}`)}\n</script>`).join('\n');
  return asset('reader-settings-head.html').replace('__SETTINGS_FONT_FACES__', faces.join('\n')).replace('__SETTINGS_FONT_LICENSES__', licenses);
}
export function settingsBody() { return asset('reader-settings.html'); }

// Small, deliberately recognized adapters. Preserve each reader's corpus and
// bespoke navigation/consent logic. Unknown runtimes fail instead of guessing.
export function connectSettingsRuntime(html, filename) {
  if (html.includes('BookSettings.connect(')) return html;
  const adapters = [
    {
      pattern: /els\.themeButton\.addEventListener\('click', \(\) => \{\s*state\.theme = state\.theme === 'dark' \? 'light' : 'dark';\s*save\('theme', state\.theme\);\s*render\(\);\s*\}\);/,
      code: "window.BookSettings.connect(state.theme, function (theme) { state.theme = theme; save('theme', theme); document.documentElement.dataset.theme = theme; });"
    },
    {
      pattern: /themeButton\.addEventListener\('click', function \(\) \{\s*state\.theme = state\.theme === 'dark' \? 'light' : 'dark';\s*storageSet\('([^']+)', state\.theme\);\s*applyTheme\(\);\s*\}\);/,
      code: "window.BookSettings.connect(state.theme, function (theme) { state.theme = theme; storageSet('$1', theme); applyTheme(); });"
    },
    {
      pattern: /case 'theme':\s*state\.theme = state\.theme === 'dark' \? 'light' : 'dark';\s*save\('theme', state\.theme\);\s*applyTheme\(\); render\(\); break;/,
      code: "case 'settings': break; // The maintained Settings module owns this control."
    },
    {
      pattern: /themeButton\.addEventListener\('click', function \(\) \{ state\.theme = state\.theme === 'dark' \? 'light' : 'dark'; save\(\); render\(\); \}\);/,
      code: "window.BookSettings.connect(state.theme, function (theme) { state.theme = theme; save(); });"
    }
  ];
  const adapter = adapters.find(item => item.pattern.test(html));
  if (!adapter) throw new Error(`${filename}: unrecognized theme runtime; wire Settings explicitly`);
  html = html.replace(adapter.pattern, adapter.code);
  if (adapter === adapters[2]) {
    html = html.replace('data-action="theme"', 'data-action="settings"');
    const anchor = '  /* Navigation */';
    if (!html.includes(anchor)) throw new Error(`${filename}: missing legacy adapter anchor`);
    html = html.replace(anchor, "  window.BookSettings.connect(state.theme, function (theme) { state.theme = theme; save('theme', theme); applyTheme(); });\n\n" + anchor);
  }
  return html;
}
