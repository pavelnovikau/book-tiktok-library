# The Wee Free Men — implementation QA

2026-10-31. Status: **ready for the parent’s cold editorial review and catalogue integration**. This is collector implementation QA, not independent editorial certification or publication approval. The commissioned audience is 14+; that is not a claim that all editions carry the same publisher age label.

## Canonical package

Exactly four files: `story-data.json`, `the-wee-free-men.html`, `sources.md`, `QA.md`. No book source files, publisher artwork, borrowed full text or temporary QA assets are included. No child agents, shared shell edits, catalogue/root reader changes, git operations, commits, PRs, deployment or external messages were performed.

Built from schema-v2 data with the current maintained builder, not another generated book:

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/the-wee-free-men/story-data.json --out collector-output/the-wee-free-men/the-wee-free-men.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/the-wee-free-men/the-wee-free-men.html --min-screens 96 --require-bilingual
```

Maintained builder SHA-256: `c88078eb41ae3d63bfd05e3a94834f2bc960f554ce3736965f3467398c44f88d`.

Maintained template SHA-256: `972227e8f427526990ca716d1373a0aea65b234faa2f1e87a949a3d4dc5bb0ac`.

Final JSON SHA-256: `d19465041c7fc4d0052b898ed9353925d431f2111be0a960c6c82b21a500424d`.

Final HTML SHA-256: `f1a3ad089d7bd436d7493ee4f8b70f2b921052aaae680cd1692c6e468edc10a8`; 386,353 bytes.

## Counts, words and sources

| Mode | Cumulative screens | RU words including title/subtitle/body | EN words including title/subtitle/body | Estimated RU / EN minutes |
|---|---:|---:|---:|---:|
| Essential | 24 | 1,295 | 1,446 | 8 / 7 |
| Core | 60 | 3,231 | 3,640 | 18 / 17 |
| Deep | 96 | 5,183 | 5,871 | 29 / 27 |

Level populations: 24 at level 1, 36 additional level 2, 36 additional level 3. Cover and final are both level 1. Estimates use builder rates of 180 RU / 220 EN words per minute, rounded up, and exclude time spent on navigation or sources. The audit reports 5,178 / 5,866 RU/EN words because its count excludes the cover subtitle; the builder’s figures above include it.

Body text alone: RU 4,638 words, 44–53 per screen, mean 48.31; EN 5,238 words, 50–61 per screen, mean 54.56. All 192 localized bodies lie inside the requested approximate 35–75 band. Title, section and provenance text are separate from these body counts. Counts use the builder’s Unicode word-token convention.

13 sources: official excerpt/foreword, work page, bibliography, two official teaching guides, two author interviews, four independent reviews and British Geological Survey, plus Russian publisher metadata. The original 12-source plot/theme map was written before screen prose. Source 13 was added during final metadata validation to correct the Russian title to **Маленький свободный народец**; it does not add plot claims. Provenance populations including the cover’s framing label: 28 book, 8 corroboration, 60 synthesis. The cover itself does not display a provenance footer. Both languages share each screen’s ID, level, provenance and source array.

## Evidence and spoiler boundary

Directly consulted book text is the official Penguin/Corgi sample, ISBN 9780552579193: publication leaf, Rhianna Pratchett foreword and chapter 1, printed pp. 1–20. The complete novel and a complete Russian translation were **not** read. Later events are bounded reports supported by publisher discussion questions and named reviews. No claim of full-text fidelity, invented dialogue, invented page references or complete scene chronology is made. Direct links, exact consulted locators, source access failures and exclusions are in `sources.md`.

Essential/Core retain publisher-level premise, early context, characters, mechanisms and themes but withhold the rescue outcome and decisive late mechanisms. Screens 85–94 are level 3, carry explicit RU/EN spoiler titles, and start with a warning before the nine ending screens. Their titles are absent from Essential/Core contents. Screens 95–96 return to spoiler-safe invitation/questions in all modes. This is a bounded ending discussion, not an exhaustive plot reconstruction.

The old remedies, fictional marriage custom and comic violence are explicitly treated as material for analysis rather than prescriptions. The opening bait plan receives an ethical caveat. Authorial sound associations are not asserted as Gaelic etymology; layered thought is not diagnosed; geology is distinguished from magical experience; a late vision is not declared proof of literal resurrection. Sources themselves may contain spoilers and are optional outward navigation.

## Deterministic audit

**68 passed, 0 warnings, 0 failures** on the final HTML. Additional data checks passed: exact counts, unique IDs, level-1 cover/final, shared language metadata, default RU/dark/Essential, explicit Deep spoiler placement and no private workstation path in HTML. No media assignments; no publisher cover. Embedded Geist and Geist Mono are the maintained assets.

## Native Chrome matrix

All tests used `file://` in native Google Chrome through a temporary CDP harness outside the repository. No server or `preview_*` tool was used. Each Chrome and harness invocation was bounded by `/usr/bin/timeout 30`, with a fresh temporary profile and OS-allocated dedicated debugging port. A `finally` handler terminated its process group and removed its profile on pass/failure; signal handlers covered interruption. Early attempts hit a 10-second CDP-request timeout in the harness during a 720-visit operation. The request bound was corrected to 25 seconds within the unchanged 30-second browser limit; all final matrix runs completed. No artifact fix was needed for that harness issue.

For every mode/language/theme combination, each expected stable ID was opened through the reader’s actual chapter navigation, allowed to render, and checked against its localized title and counter. Every slide was scrolled to its bottom to check reachability; top controls, slide width, active rail ID and rail visibility were measured. The complete matrix was rerun after the Russian title/source metadata correction.

| Viewport | Screen visits | Unique IDs | Horizontal overflow | Unreachable text bottoms | Runtime errors | Remote runtime requests |
|---|---:|---:|---:|---:|---:|---:|
| 320×568 | 720 | 96 | 0 px | 0 | 0 | 0 |
| 390×844 | 720 | 96 | 0 px | 0 | 0 | 0 |
| 1024×768 | 720 | 96 | 0 px | 0 | 0 | 0 |
| 1440×900 | 720 | 96 | 0 px | 0 | 0 | 0 |

Total: **2,880 visits** = (24 + 60 + 96) × 2 languages × 2 themes × 4 viewports. Desktop rail was visible, scrollable, synchronized and kept the active item in view in all 1,440 desktop visits. Both font faces reported `loaded` in every viewport. Source links were inspected as optional anchors; none was opened as a runtime dependency. Home’s maintained `./` link is present; catalogue integration was deliberately outside this collector’s scope.

Representative cover, ordinary/dense prose, explicit spoiler/provenance and final screens were visually inspected in both themes and languages across phone/tablet/desktop screenshots. Captures waited for content animation to settle; initial early-animation captures were not treated as final appearance. The longer corrected Russian title was rechecked. There are no list, photo, numerical chart or comparison-layout screens in this prose corpus, so those layout categories are not claimed as tested.

## Behavior and iOS checks

Final control suites passed at 320×568 and 1440×900; a 390×844 suite also passed before the metadata-only correction. They cover:

- ArrowRight/Space navigation on the reading surface; Space on focused language, Sources and Chapters controls activates that control without an extra page advance.
- Both dialogs open/close; Deep chapter navigation; language/theme preserve stable position and depth; source list/method disclosure present.
- Pointer tap enters focus; header/progress/rail/back/counter disappear while text and safe-area Next remain. Cover focus retains real title/body plus Next and hides normal cover actions/mode controls.
- F toggles and Escape exits after clicking Next while its button retains focus. Vertical pointer drag does not toggle focus or navigate; a horizontal swipe advances without becoming a tap. Swipe checks used pointer-event sequences in the real browser, not a physical touch panel.
- Final restart clears remembered progress; reload offers Continue; Continue restores stable ID; Start over begins the selected depth.
- Hidden-ID automatic depth raising: test-only DOM reassignment of a bound chapter button exercised the maintained handler. This is not claimed as a visible hidden-chapter UI, because the maintained contents lists show only the selected mode.

At 390×844 with iPhone Safari user agent emulated in Chrome, the install guide auto-opened, localized RU/EN, closed, reopened manually, hid in focus, and restored its manual trigger after focus exit. With `navigator.standalone=true` injected before page initialization, guide and trigger remained suppressed. These checks were repeated against the final metadata build. No claim is made to have tested physical iPhone Safari, a real installed Home Screen session, browser chrome removal, hosting, deployment, or a service-worker install. The file is offline standalone; the parent owns catalogue/PWA integration.

## Handoff limitations

Technical checks do not establish independent literary quality or full-book fidelity. The analytical depth is deliberately interpretation-heavy and its screen jobs/provenance are exposed for cold review. Remaining work belongs to the parent: cold editorial review, any requested corrections, catalogue/root integration and publication decision. Temporary research downloads, screenshots, scripts and native profiles are removed after the implementation checks. Only the four canonical files remain.
