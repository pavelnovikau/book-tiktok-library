# Shared reader settings

The homepage and every released reader have one Settings gear in the existing compact icon row. It replaces the direct theme toggle. Settings contains only Theme (Dark/Light) and Reading font (Sans/Serif). Keep the statistics strip, equal homepage tabs, language control and all reader navigation/consent behavior.

## Maintained sources

- `assets/reader-settings-head.html`: embedded font declarations, reading/UI styles and global preference API.
- `assets/reader-settings.html`: localized native dialog, radio groups, Escape/Tab/focus return.
- `scripts/reader-settings.mjs`: font/license embedding and explicitly recognized runtime adapters.
- `assets/reader-header.html`: one-row icon geometry, localized labels/tooltips, Settings gear and safe-area rules.
- `scripts/build_story.mjs`: includes both Settings blocks for future v2 builds.
- Repository `scripts/apply-reader-shell.mjs`: applies the same module to the homepage and readers without rebuilding embedded books. 1873/TOC and Hermes now use schema v2 with one-time migration from their actual old storage keys; legacy runtime adapters remain supported. Unknown theme runtimes fail explicitly.

Run `npm run sync:readers` after a new release. A root reader may contain bespoke consent, saved-ID invalidation or editorial guards that a clean build would erase: synchronize its shell instead. Rebase on current `origin/main`, preserve the released HTML/corpora and reapply maintained patches; never restore an older book to resolve a UI conflict. Do not update an installed skill until the PR is merged.

## Persistence contract

`localStorage['bookLibrary.preferences.v1']` holds:

```json
{"version":1,"theme":"dark","readingFont":"sans"}
```

A new browser defaults to RU / dark / true Geist Sans. A valid v1 preference wins over every old per-book theme. On first use, the visited page migrates its valid legacy theme; font starts as Sans. Malformed/unsupported v1 data falls back to that page's valid legacy theme, then dark. Language, depth, last screen/slide ID, focus mode and consent remain under their existing page-specific keys and policies. Storage denial still permits changing settings in the open document. Storage events and `pageshow` refresh active/restored pages.

The module calls `BookSettings.connect(legacyTheme, setter)` inside each real runtime, replacing its old theme click handler. The setter updates closure state and the existing theme key without rendering the story again. Theme/font changes therefore preserve the exact screen, depth, progress and scroll position. The header observer paints a gear even after a legacy render updates the control's text. Do not add a second handler that toggles theme when the gear is opened.

Preferences are origin-scoped. A downloaded `file://` reader remains network-independent; cross-file storage sharing under `file://` is browser-dependent. Hosted homepage/readers on one origin share settings normally.

## Font provenance and honesty

The existing variable Geist Sans (internal 1.800) is reused byte-for-byte. Its cmap contains all 66 Russian letters, including Ё/ё. Hermes previously named Geist without embedding it; synchronization now embeds the same verified Sans/Mono there too.

- Geist Serif Regular: `geist@1.9.0`, internal 1.001, unmodified `dist/fonts/geist-serif/GeistSerif-Regular.woff2`. Official release: https://vercel.com/blog/introducing-geist-serif ; package: https://registry.npmjs.org/geist/1.9.0 . npm tarball integrity: `sha512-uxiyxH5PaKDaK2//ln06NxJEz5gc6771BTwSs1YFgNnASGtp1SYD3VZShSIijvlNwDjMgHnzqye4MmIUTspEzw==`.
- Source Serif 4 Regular: Adobe tag `4.005R`, internal 4.005. Unmodified source: https://raw.githubusercontent.com/adobe-fonts/source-serif/4.005R/WOFF2/TTF/SourceSerif4-Regular.ttf.woff2 . License: https://github.com/adobe-fonts/source-serif/blob/4.005R/LICENSE.md .

Geist Serif is a **display** face, currently a static Regular with no Russian glyphs. Serif mode uses actual Geist Serif for supported Latin and Source Serif 4 for Cyrillic. Both are static 400; reading styles disable synthetic weights/italics. All controls remain Geist Sans. The concise RU/EN Settings note names the Russian fallback even when Sans is selected. No Mono substitution, fake bold, remote font requests or claim of Russian Geist Serif support.

All WOFF2 data and complete upstream SIL OFL 1.1 notices travel inside each standalone HTML, including the homepage. Unmodified license copies accompany source fonts under `assets/fonts/`. `python3 scripts/check-fonts.py` (repository command; requires fontTools with WOFF2 support) audits SHA-256, cmap, axes, weights and license notices without network access.

## QA

`npm run check` checks catalogue/builder invariants and exact maintained Settings/font bytes on the homepage and all registered readers. `npm run qa:settings` runs a separate no-server CDP harness. It fulfills same-origin fixture routes from the checkout, blocks external runtime requests, and uses real offline `file://` readers separately. Each phase owns a unique temporary profile and a `timeout 30` Chrome process tree; cleanup removes both. Override `CHROME_BINARY` if needed.

Coverage: every released reader at 320/390/900/1440, RU/EN, dark/light and both fonts; Chrome platform-font records for Cyrillic/Latin probes and actual reading paragraphs; homepage → v2 → 1873 → TOC → Hermes → home/reload persistence; legacy migration/invalid storage/denied storage; native modal focus/Tab/Escape/selected states; real page state/reading position/depth; Sources; focus mode; emulated iPhone insets/install heading; existing native/custom saved-Deep consent including Hitchhiker. A pre-existing reader without an explicit consent guard is listed as a legacy limit, not certified as guarded. Existing book-specific session-consent policy is preserved.

The harness does not start a content server, use shared preview tabs, install a service worker or claim physical iPhone/Safari testing. Its iOS geometry is Chrome emulation. QA reports/screenshots stay outside Git; private full-book sources never enter the public repository.
