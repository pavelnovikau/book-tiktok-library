Current root acceptance 2026-11-01T04:01:32.422095+00:00: PASS for the exact version in root-review/personal-review.json. Routes29/61/85; Deep7870RU/9095EN main-body words; UI46/44minutes. Earlier worker-phase numbers, hashes and pending statuses below are historical. Root completely read the bilingual retelling and selected actual primary passages, not the whole primary book continuously.

---

# Local QA — A Guide to the Good Life, depth-v2

Current candidate:29 Essential /61 Core /85 Deep screens. Explanatory presentation, RU/dark/Essential/Sans on fresh state. Status: **ready-for-root-personal-check**, not editorial acceptance. `rootPersonalAcceptance=false`, `publicationAllowed=false`.

## Content and evidence

The complete English introduction,22 chapters and reading program were read in numeric/spine order through bounded untruncated displays. The reading ledger binds every range to the exact file hash, distinguishes actual main-text reading from source inventory, and limits Russian consultation to the edition page and complete editor preface. Chapter20 was read and is substantively represented. No new web acquisition or current treatment-efficacy certification was made.

Connected RU was written first, corresponding EN next, screen segmentation last. There are73 units and153 actual paired paragraphs. The implementation checked meaning during authorship; the Essential RU/EN route was reread as a cumulative sequence, including recovery of a truncated display range. Core/Deep ordering was inspected against the complete manuscripts and chapter map. This is implementation review, **not root's required full personal reading** or an independent editorial PASS. All resulting routes are available as `route-{essential,core,deep}.{ru,en}.md` for root's reading. Root must also check the original primary passages and deliberate omissions before publication.

`verify.mjs` checks every actual RU and EN paragraph against its connected draft, with no missing/duplicated paragraph; all153 pairs agree. All authored top-level fields and screens match the effective HTML embedding. Full-body, cover-framing and title/subtitle word counts are separately bound in `metrics.json`.

| Mode | Screens | RU body words | EN body words | RU UI estimate | EN UI estimate |
|---|---:|---:|---:|---|---|
| Essential |29|2,576|2,980|16 минут|15 min|
| Core |61|5,639|6,509|33 минуты|32 min|
| Deep |85|7,932|9,170|47 минут|44 min|

Body includes the source-derived final doubt and reading-program account; it excludes the added cover. Body-only Deep is44.07min RU /41.68min EN at180/220wpm, rounded up to45/42. UI estimates include titles/subtitle and cover text. They are estimates, not timed reading observations. Average Deep body density is94.4RU /109.2EN words per exposition screen. These totals are results, not acceptance thresholds.

The earlier84-screen segmentation and7,908RU /9,134EN body counts are explicitly superseded in `qa/superseded-metrics-01.json`. Two sharper attributed arguments were restored before the final85-screen checks. Earlier browser reports bearing `before-` or `initial-` in their names are historical diagnostics only, not current proof; their screenshot filenames may have been overwritten by later runs.

## Build and deterministic checks

`build.mjs` invokes the maintained read-only `build_story.mjs` and applies only book-local patches demonstrated by the accepted nonfiction pilot: typographic cover, new depth-v2 progress namespace, explicit deeper-mode Continue label, and correct RU minute inflection. The maintained offline Settings/header/font implementation is retained. No shared or installed file is changed.

- `structural-audit.txt`:69 passes, zero warnings/failures; exact85-screen corpus and29/61/85 nested counts.
- `parity-check.json`:153 actual paired draft paragraphs preserved in order; all authored fields match the embedding;24 complete-source chapter-map entries (introduction,22 chapters, reading program).
- Two source records, no external media or runtime dependencies, one cover and one final, unique screen IDs, no fiction spoiler policy/modal and no synthesized coaching screens.
- New book state prefix: `book-tiktok.a-guide-to-the-good-life.depth-v2.`. Shared preferences remain at `bookLibrary.preferences.v1`. Legacy short-reader language/depth/position cannot silently select a location in this expanded corpus.

## Bounded offline browser evidence

Current report files: `qa/browser-320.json`, `qa/browser-390.json`, `qa/browser-1024.json`, `qa/browser-1440.json`, `qa/browser-ios-320.json`. Each binds the current exact authoring JSON, standalone HTML and browser-check script hashes. All five report `local-checks-completed`.

Each phase traversed1,400 actual rendered visits: every selected-mode screen in RU/EN × dark/light × Sans/Serif × Essential/Core/Deep. Total7,000 visits. The viewport dimensions were320×568,390×844,1024×768,1440×900; the fifth phase repeats320×568 with an emulated iPhone user agent and44/34px safe-area insets. Every rendered visit checks the actual localized heading/body text, mode count, horizontal bounds and reachable paragraph tail after scrolling. There were zero unexplained runtime errors and zero HTTP(S) runtime requests. The only listener reserved by the harness is the temporary Chrome CDP port; no content server is started.

Each phase also passed28 standard interaction assertions (140 total), supplemented by native-dialog, real-pointer, global-preference and saved-mode tests:

- Language changes preserve stable screen ID, position and depth. All mode selectors and reachable tails agree with the embedded corpus.
- Settings opens without toggling theme. Theme/font radio controls preserve reading state and scroll, show the localized Source Serif4 Cyrillic fallback note, and persist through reload. A supplied global v1 preference wins over the book's legacy theme. Cross-file `file://` preference sharing is browser-dependent and is not certified here.
- CDP platform-font records show actual custom Geist Sans in RU/EN; actual Source Serif4 for Cyrillic and Geist Serif for Latin in Serif mode. All embedded font faces load offline; UI remains Sans.
- Native Settings initial focus, Tab containment, native Escape and focus return to the gear pass. Sources and Chapters open and close; both source records are accessible.
- Actual paragraph pointer taps enter and exit focus; keyboard F/Escape works; header/rail/chrome hide and Next remains. Focus persists while paging. Horizontal gestures advance; vertical gestures neither advance nor enter focus.
- Buttons, keyboard next/previous, chapter navigation/rail synchronization, saved Continue, Start over and final restart pass. A saved Deep target resumed from either shallower mode explicitly names Deep/«Глубоко» in both languages before raising the mode; no fiction spoiler modal appears. Legacy old keys remain untouched.
- All visible header controls are labeled icon-only SVG buttons/links in one row inside the viewport; home points to `./`. The rail is visible at desktop widths.
- Emulated iPhone guide auto-opens in Russian, closes and manually opens in English, and hides along with its trigger in emulated standalone mode. The six-control row fits at320px and lies below the44px safe area. Actual CDP touch swipe advances. This is **Chrome emulation, not a physical Safari/iPhone/PWA test**.

Screenshots were inspected locally:320 cover,320 dense Cyrillic Serif/mother case,320 English tennis argument,1440 final with active rail, and emulated-iPhone cover. Typography is legible, header compact, long text scrolls inside the reading area and the final/restart remains reachable. No image/comparison-table fixture is claimed because this manuscript uses prose and a typographic cover. The filename `320-quantitative.png` is the adapted harness label for the tennis argument, not a claim of a quantitative experiment.

Every phase used its own `mktemp -d` profile and detached owned process group under `/usr/bin/timeout 30`. `finally` kills only that group/its uniquely identified profile processes and removes the profile. Every report records `profileRemoved=true`, `remainingOwnedPids=[]`. There is no remaining owned Chrome, profile, Vite/HMR connection or content server.

## Reproduction and handoff

From this directory only:

```sh
python3 assemble.py
python3 map-coverage.py
node build.mjs
node verify.mjs
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs a-guide-to-the-good-life.html --min-screens 85 --require-bilingual
node browser-check.mjs 320
node browser-check.mjs 390
node browser-check.mjs 1024
node browser-check.mjs 1440
node browser-check.mjs 320 --ios
```

The source-reading ledger describes reading already performed; regenerating its inventory is not a new reading. `finalize.py` checks current QA bindings and refreshes `ready.json` after documentation is final. Rebuilding or editing content invalidates the old HTML/QA hashes until rechecked.

No subagents, Git/PR/deploy, publication, shared skill/shell edit, root reader/catalogue edit, workspace log or global status mutation occurred. The old collector and historical reviews remain intact. Root's full RU/EN/route/source reading and explicit editorial decision remain outstanding by design.
