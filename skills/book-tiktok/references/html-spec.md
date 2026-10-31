# Standalone HTML specification

Use this reference when implementing or visually checking the artifact. New artifacts should use the v2 data contract and maintained builder rather than copying an older book.

## Authoring and build

- Keep research/content in `story-data.json` as described in [data-contract.md](data-contract.md).
- Build with `scripts/build_story.mjs`; deliver the generated `<book-slug>.html`.
- The final reader needs one HTML file and no build step. The JSON is an authoring source, not a runtime dependency.
- Do not carry another book’s data, images, sources, storage key, or title into a new artifact. The audit treats an unreachable second story corpus as a failure.

## File and runtime

- Embed CSS and JavaScript. Embed Geist, Geist Mono, the cover, and any archival images as data URLs.
- Do not use CDN imports, external scripts, remote stylesheets, runtime `fetch`, XHR, WebSocket, EventSource, or service workers.
- Direct source/credit links are allowed because they are optional navigation, not runtime dependencies.
- Namespace local storage with the book slug and persist theme, language, reading depth, and last screen ID.
- Include deterministic metadata generated from the structured data:

```html
<meta name="book-tiktok:schema" content="2">
<meta name="book-tiktok:screens" content="96">
<meta name="book-tiktok:languages" content="ru,en">
<meta name="book-tiktok:modes" content="24,56,96">
```

## Flexoki treatment

Start with these canonical identities and express use-site colors only through variables:

Palette source and rationale: [Flexoki by Steph Ango](https://stephango.com/flexoki).

```css
:root {
  --color-bg: #fffcf0;
  --color-text: #100f0f;
  --color-primary: #1c6c66;
}
```

- Light is warm paper, not pure white; dark is warm near-black, not blue-black.
- Muted Flexoki cyan is the single focus-action color: use cyan-700 (`#1C6C66`) with paper text in light mode and cyan-500 (`#2F968D`) with ink text in dark mode. These darker-than-default UI steps preserve normal-text contrast and feel quieter during bedtime reading. Use the accent for one primary action per screen, not decoration.
- Status colors are for actual status only.
- Use Geist for reading and Geist Mono for section labels, indices, and quantitative anchors.
- Define sizes as `--text-*`, `--space-*`, `--radius-*`, or control tokens before use.
- Do not use emoji, decorative glyphs, left-accent borders, gradients, or glass effects.
- Keep image treatment quiet: documentary crops, restrained borders, factual captions.

## Responsive reading shell

### Phone, 320–440 CSS px

- Use `100dvh`, safe-area insets, a fixed shell header/footer, and a vertically scrollable slide body.
- Keep home, Chapters, language, Sources and theme in one compact row of icon buttons at 320 px. Every button needs a localized accessible label and tooltip. The optional iOS install-guide icon belongs in that same row; never add a second header row that reduces reading space. This is Pavel's explicit reader requirement and supersedes older text-only/no-glyph rules for these controls.
- Keep a compact home icon in the existing top bar with `href="./"`; localize its accessible label as `К библиотеке` / `Back to library`. Do not add a separate navigation row for it.
- Include the iOS standalone metadata and the maintained in-reader install guide. In iPhone/iPad browser mode, explain that a page cannot programmatically remove Safari chrome, show the exact `Share → Add to Home Screen` route, and tell the reader to relaunch from the Home Screen rather than Telegram. Offer the guide automatically once and keep a manual trigger outside focus mode. Hide both in `display-mode: standalone` / `navigator.standalone` and in focus mode so an installed reader still shows only the text and Next.
- Ensure horizontal overflow is impossible while long lists and evidence screens remain vertically scrollable.
- Use at least 44 px for primary touch targets; compact topbar controls may be slightly smaller when still comfortably tappable.

### Tablet and desktop

- At about 900 px, introduce a persistent scrollable chapter rail and a centered reading column; do not merely stretch the phone card.
- Keep the active chapter visible in the rail and synchronize it after keyboard, button, swipe, and chapter navigation.
- On cover screens, use the extra width for a balanced visual/copy composition. On reading screens, cap text measure around 700–780 px.
- Preserve the same content, mode, ID, source, and progress model across breakpoints.

## Story behavior

- Modes are nested by level so Essential ⊂ Core ⊂ Deep, and progress uses the selected mode count.
- Chapters navigate by stable screen ID and may raise the depth if a selected screen is hidden.
- The final screen restarts cleanly; a remembered position offers Continue and Start over.
- Support explicit buttons, horizontal pointer/swipe gestures, Arrow/Page keys, and Space for next.
- Do not hijack vertical scrolling as a page gesture.
- Support a focus mode that toggles when the reader taps non-interactive text. It hides the header, progress, desktop rail, back control, and other reader chrome while preserving the current text and a safe-area-aware Next button. A second tap restores the chrome; `F` toggles it and `Escape` exits it on desktop. Ignore links, buttons, dialogs, text selection, long presses, and scroll/swipe gestures, and preserve focus mode while paging.
- Use native dialogs or an equivalently accessible modal pattern for Chapters and Sources.
- Give large embedded images `decoding="sync"` or preserve decoded elements so rapid language/theme switching does not show partial scans.
- Display whether a screen is the book’s argument, independent corroboration, or synthesis.

## Accessibility and semantics

- Set document `lang` on every language switch.
- Localize `title`, dialog headings, aria labels, navigation labels, captions, method text, and image alt text.
- Preserve visible keyboard focus and semantic buttons.
- Mark progress decoration as hidden from assistive technology while exposing a textual progress label.
- Keep contrast readable in both themes and do not encode meaning through color alone.
- Support `prefers-reduced-motion`.

## Static verification

Run:

```bash
node <skill-dir>/scripts/audit_story_html.mjs <book-slug>.html \
  --min-screens <justified-minimum> --require-bilingual
```

The v2 audit verifies the structured corpus rather than trusting only metadata. It checks exact level/mode counts against the user-approved `targetModes`, unique IDs, bilingual copy, provenance types, source/media references, offline invariants, responsive shell hooks, Flexoki identity, and unreachable legacy story data.

## Browser QA protocol

Do not use the collaborative preview to verify a page you just authored. Use the available local/browser automation path and keep any manually launched headless Chrome bounded and isolated.

Test 320×568, 390×844, 1024×768, and 1440×900. At minimum:

1. Load the cover in the default language and theme.
2. Switch language and theme rapidly; wait for images to decode and inspect the cover.
3. Assert exact Essential/Core/Deep counts against the user-approved `targetModes`, metadata, and structured data.
4. Programmatically traverse every screen in RU and EN; verify unique, non-empty titles, valid position, and no horizontal overflow.
5. Visually inspect representative cover, dense prose, long list, image, comparison, quantitative, provenance, and final screens.
6. Open and close both dialogs; test hidden-screen chapter navigation and automatic mode raising.
7. Confirm embedded fonts and images decode.
8. Test buttons, keyboard, pointer swipe, saved position, Continue, Start over, and final restart.
9. Toggle focus mode by tap and keyboard at phone and desktop widths; verify that only reading content and Next remain, that vertical scrolling and horizontal page swipes are not misread as taps, and that exiting restores the full shell.
10. At 320 px, assert every top control lies inside its container. At 1024/1440, assert the rail is visible, scrollable, and synchronized.
11. Emulate iPhone Safari in ordinary browser mode and verify the install guide opens, localizes, closes, and remains available from its trigger. Emulate standalone mode and verify the guide and trigger are absent. Do not claim that ordinary Safari can be forced into fullscreen.
12. Collect console/runtime exceptions and require zero unexplained errors.

When manually launching headless Chrome, use `timeout 30`, a unique `mktemp -d` profile, and a dedicated debugging port. Terminate the full process tree and delete the profile immediately, including on failure. Do not leave a local server, Chrome process, or temporary profile running after QA.
