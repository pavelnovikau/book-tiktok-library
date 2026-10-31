# The Two Captains — implementation QA

**Parent status, 2026-10-31:** independent cold review completed, all required findings repaired, fresh audit and targeted browser checks passed. Ready for catalogue integration; not published. Collector-stage notes/fingerprints are retained below, with the final repair record at the end.


Date: 2026-10-31. Implementation self-check only; **independent cold editorial review remains the parent’s task**. Nothing published, committed or registered in the catalogue. Only the four authorized files in this collector directory are deliverables.

## Corpus and exact statistics

- Schema v2, stable slug `the-two-captains`; 144 unique IDs and complete RU/EN copy.
- Cumulative counts **36 / 90 / 144**; level distribution **36 / 54 / 54**. Cover and final are each level 1.
- Default: **RU / dark / Essential**; audience `teen-14-plus`; spoiler policy `full-plot-in-deep`.
- Provenance, including cover/final: **43 book / 25 corroboration / 76 synthesis**.
- **11 consulted sources**, 1 original embedded SVG cover, embedded Geist and Geist Mono. No publisher artwork reproduced.
- Ordinary body density: RU **42–52** words, EN **48–57** words. All 142 ordinary screens remain within the agreed ~35–75 band. Whole-corpus body mean: RU **46.97**, EN **53.40**.

| Mode | Screens | RU body words | EN body words | RU title/subtitle/body words | EN title/subtitle/body words | RU estimate | EN estimate |
|---|---:|---:|---:|---:|---:|---:|---:|
| Essential | 36 | 1,690 | 1,914 | 1,886 | 2,156 | 11 min | 10 min |
| Core | 90 | 4,222 | 4,820 | 4,727 | 5,447 | 27 min | 25 min |
| Deep | 144 | 6,764 | 7,690 | 7,560 | 8,700 | 42 min | 40 min |

Counts use the maintained builder’s Unicode word rule. Reading estimates use its 180 RU / 220 EN words per minute, not measured user reading time. The audit reports 7,555 RU / 8,693 EN words because its corpus total excludes the cover subtitle (5 / 7 words); this is not missing translation.

## Research and spoiler boundary

The official Azbooka PDF sample was visually read in full: **20 PDF pages**, with narrative on printed **pp. 7–22**, through the opening of chapter 5. **The complete novel was not read.** Later book facts are mediated by consulted criticism and the Russian State Library for Young Adults essay, as explicitly disclosed in both reader languages. The fuller claim map, source ledger, access limitations and source corrections are in `sources.md`.

Essential and Core give the premise and early adversity but preserve decisive late actions and resolution. Deep’s 16-screen ending section begins at screen **128**, ID `ending-warning`; the final screen is nonspoiling and available in every depth. Deep section titles are neutral, and the global Sources dialog/method notes do not name late culprits, betrayals or outcomes. External articles can contain spoilers and are labelled accordingly. No invented quotations, flight specifications, clinical claims or book page locators; excerpt page references are actual inspected printed numbers.

## Build and deterministic audit

Built only through the maintained `skills/book-tiktok/scripts/build_story.mjs`, with the current shared template and compact icon header. No shared shell modification or copied book reader.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/the-two-captains/story-data.json --out collector-output/the-two-captains/the-two-captains.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/the-two-captains/the-two-captains.html --min-screens 144 --require-bilingual
```

Final audit: **68 passes, 0 warnings, 0 failures**. Final standalone size: **462,280 bytes**. No remote scripts, styles, fonts, images or runtime requests. Optional source links and `href="./"` home navigation are intentional.

Maintained build inputs at collector-stage rebuild:

- `skills/book-tiktok/scripts/build_story.mjs`: `f0a5e65358aa159f9cc64266ff9629cc80fbe392a3f52025a25ce909f6c08c3b`
- `skills/book-tiktok/assets/standalone-template.html`: `690b5beae668868566c7680ebfed5f59736b49506bdee09b4046247a8d13e724`
- `skills/book-tiktok/assets/reader-header.html`: `0947f8417d61e5d8944e9ec010defef2bba747e5dc8583436ce4cf2729881623`

Final HTML SHA-256: `7d5cc057e52346270ef2dbe0b36f6ea7fcd12d3276eadc1a1d3fbb36b3f364d0`.
Story-data SHA-256: `4f31b0e1ff392be99c7c6b7f8b3b85d351866c7b1bed5d6b96877946f55fe587`.

## Collector-stage real-browser matrix (before parent repairs)

Local installed Google Chrome controlled through Playwright/CDP, navigating the actual `file://` standalone. **No server and no preview tools.** Every matrix cell visits all visible screens in all three depths for one language and both themes: `(36+90+144) × 2 = 540`. This produces **4,320 visits**, including every one of the 144 screens in RU/EN and light/dark at all four sizes.

| CSS viewport | RU visits, both themes | EN visits, both themes | Total | Result |
|---|---:|---:|---:|---|
| 320×568 | 540 | 540 | 1,080 | PASS |
| 390×844 | 540 | 540 | 1,080 | PASS |
| 1024×768 | 540 | 540 | 1,080 | PASS |
| 1440×900 | 540 | 540 | 1,080 | PASS |

Each visit checks the expected localized title and document language, theme, selected-depth count, document/body/slide/story horizontal containment, zero vertical document overflow, five icon-only header controls in one row with labels/tooltips, and the active desktop rail entry where applicable. Cover checks additionally compare the actual cover layout, copy, artwork and actions with the reading viewport; document overflow alone is not the cover test. Assertions run after the short transition settles. Long slides scroll internally by design.

## Targeted interaction and visual checks

- **Native Space** on Sources, its Close button, language, theme, Chapters, depth, Next and Previous; no double advance or unintended reader navigation. Body Space, ArrowLeft and PageDown also tested.
- **Cover focus**: text tap hides chrome and Start/depth controls, retains Next; Next starts reading. **F and Escape immediately after Next**, while Next retains focus, work on phone and desktop.
- Reading-text tap enters/exits focus. Vertical pointer movement and native wheel scrolling do not become focus taps; horizontal pointer swipe navigates without toggling focus.
- Native internal scroll on the 320×568 cover reaches Start; native scroll on a long prose screen reaches its provenance footer. Neither creates vertical document overflow. Long Chapters dialog navigation reaches the final screen.
- Sources and Chapters open/close and navigate. All 11 sources present; Sources text checked for late-answer leakage. Font faces load, original cover SVG decodes, and Home retains `./`.
- Theme/language/depth/progress persist; reload offers Continue; Continue restores position. A stored Deep-only ID with Essential selected raises depth correctly. Start over begins the reading sequence; final Restart clears the saved position and returns to the cover.
- Twenty rapid language/theme switches preserve screen and theme in mobile RU and desktop EN checks.
- Visually inspected light covers/prose at 320, 1024 and 1440; dark mobile/desktop cover/prose, Sources and focus. Single-paragraph reading screens are intentional; there are no narrative list/comparison/quantitative layouts to certify separately.
- iPhone Safari **user-agent/touch emulation in Chrome** at **320×568 and 390×844**, both languages, ordinary/focus/standalone: auto guide once, manual reopen, acknowledgement persistence, localized Share → Add to Home Screen and relaunch guidance. Install icon remains in the same row, with six icon controls fitting at 320; guide and trigger are suppressed in focus and emulated `navigator.standalone`. The text explicitly says a website cannot remove Safari chrome itself.

**224 recorded high-level browser assertions passed**, in addition to per-screen checks. **0 console/runtime errors and 0 remote runtime requests** in final successful runs. A test-harness timing correction waited for animation/rail settlement; a guide reload harness correction stopped deleting its acknowledgement on every load. Neither required editing the shared shell.

## Limitations and handoff

This is source-backed analytical synthesis, not a full-edition reading or a chapter substitute. Some scholarly access was limited to an abstract or selected sections, itemised per source. Browser results are Chrome results; no physical iPhone, native Safari, VoiceOver or Android device certification is claimed. Independent editorial judgement, catalogue integration and any later publication belong to the parent.

Every manually started Chrome used **`timeout 30`**, a unique temporary user-data directory and debugging port, and an owned process group. The launcher closes the browser and terminates its owned process group and deletes the profile in `finally`, including failures. Research PDFs, browser scripts, dependency files, screenshots and raw reports are scratch outside the repository and are removed after this summary; no Chrome, Vite/HMR connection or local server is intentionally left running.

## Independent cold review and parent repairs — 2026-10-31

Fresh independent review read all 144 RU/EN pairs, all 20 official sample PDF pages and targeted criticism. Parent closed all three required findings: removed unsupported document theft specificity; removed unverified siege specificity and added source 11 for marriage; repurposed resolution-two-roles as a distinct comparison of reputational restoration, moral judgement and prosecution, citing Zholkovsky sections III.1/III.3. Its navigation title stays neutral and the source-backed outcome discussion remains Deep-only. Counts remain 36/90/144; the slightly shorter corpus now estimates 42 RU / 40 EN minutes in Deep.

Final-build targeted QA passed 48 changed-screen states and 16 source-panel states across 320/390/1024/1440, RU/EN and both themes. The relationship screen renders [3,11], the repurposed screen cites [4], bodies and neutral title match JSON, and text bottoms stay reachable. Fresh audit 68/68, exact data parity, zero runtime errors, external requests or horizontal overflow. The 4,320-visit collector matrix was not repeated.

Current SHA-256: JSON `aa5d8c2c65b0463612574cda8020d1ddfdb64b92eeca289cb6659c78fdac4f0d`; HTML `b5aa2b4159bbc50a61aa67432fd16c4aabd401a6415f8880b9927e1ff178157a`; shared template `373caac52171dd92c0de3048dd6d59b08a627c7fcd0b998f8aceda6f345d69f1`. Earlier fingerprints and broad matrices above identify the collector stage, not a claim of repeating that entire matrix after these localized repairs.

Ready for parent catalogue integration. No publication is claimed. Owned Chrome processes/profiles were cleaned; no server was started.
