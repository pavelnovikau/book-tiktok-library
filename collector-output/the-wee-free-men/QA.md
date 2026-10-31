> **2026-10-31 pass 2 — current implementation QA:** narrative corpus is now 13/23/37 RU/EN screens, submitted as **ready-for-independent-check**. Earlier SOURCE-GAP and historical green results below refer to the superseded 96-pair essay. This addendum does not grant independent editorial PASS or publication.

> **2026-10-31 targeted rescue update:** SOURCE-GAP remains for specific dream-escape/climax links, not because a complete EPUB is mandatory. Newly inspected Penguin Schools Activity Sheet Four contains real chapter-8 Land of Winter fragments; Resource Three contains the henhouse encounter. These expand primary evidence beyond the earlier chapter-5 fragment, but do not establish the escape/return/climax chain. See [new acquisition map](../../editorial-audit/2026-10-31/source-rescue/the-wee-free-men.md). No new story, ready manifest, full-text claim or independent approval.

# The Wee Free Men — implementation QA

> **2026-10-31 corrected-brief audit: SUPERSEDED / SOURCE-GAP.** All 96 RU/EN pairs were re-read. REBUILD is required; no complete lawful novel was found, and the old Harper guide/interview URLs now return 404. Prior green QA below is historical and does not approve this as a condensed narrative. No new story, build or ready manifest has been issued. Current findings and exact source need: [total editorial audit](../../editorial-audit/2026-10-31/books/the-wee-free-men.md).

## Corrected-brief verification addendum

Final collector HTML was rechecked with the maintained structural auditor: **69 passes, zero warnings, zero failures** (`--min-screens 3 --require-bilingual`). This is structural evidence only. No ready status or narrative fidelity follows from it. See the linked current audit above for actual literary scope and source blocks.


## Historical QA (superseded for editorial approval)


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


---

## 2026-10-31 pass 2 — final narrative implementation checks

Status: **ready-for-independent-check only**. [Narrative report](../../editorial-audit/2026-10-31/books/the-wee-free-men-narrative-pass2.md) and [new acquisition](../../editorial-audit/2026-10-31/source-rescue/the-wee-free-men-pass2.md) supersede the old essay’s editorial/access state. Original history remains above; no fresh independent PASS or publication.

### Final corpus and meaningful source boundary

Old 96 RU/EN pairs were actually read and matched to the root effective embed. Replaced by **37 original pairs**, with connected prose saved first in `narrative-prose-pass2.md`. Every pair’s actual scene and consulted evidence is mapped in `source-map-pass2.json`. `contentMode` is genuinely narrative. The exact retained arc uses official opening and selected publisher passages plus selected primary quotations in attributed chapter criticism and substantial named event accounts. Complete novel/complete Russian translation were not read continuously; no new owned EPUB, OPF/spine or unabridged-edition verification is claimed. Scope/uncertainty is disclosed in Sources. No later Tiffany novel or film used.

| Mode | Cumulative screens | RU / EN words, builder | RU / EN estimated minutes |
| --- | ---: | ---: | ---: |
| Essential | 13 | 639 / 777 | 4 / 4 |
| Core | 23 | 1110 / 1335 | 7 / 7 |
| Deep | 37 | 1814 / 2201 | 11 / 11 |

Level populations 13 + 10 + 14, with level-1 cover and shared spoiler-safe final. Word counts include localized headings/subtitle; structural auditor excludes three cover-subtitle words and reports 1811 / 2198. Body-only Unicode token diagnostic: RU 1717 total, 24–57 per screen, mean 46.41; EN 2074 total, 25–71, mean 56.05. Bands are descriptive, not quotas. All three language/depth sequences read continuously; shallower modes deliberately leave the rescue unresolved.

### Preserved shell / maintained build

Used read-only installed `/Users/pn/.codex/skills/book-tiktok` builder. Built the new data/fonts/metadata into an external intermediate, then synchronized its generated corpus with this book’s released outer shell. Preserved same-book cover geometry, focus/install scripts and navigation; changed the cover’s analytical labels to book-specific labels. Installed Settings and compact icon header bytes were imported, not edited. Full Sans/Mono/Serif/Cyrillic fallback fonts and license texts are embedded. No remote runtime dependency.

- Installed builder SHA-256: `29386ade13039878dbfd1ead72deae294ccf2dfb9181a71c63190bd8b7ee02e4`.
- Installed template SHA-256: `11f556efa62134a9f4c2ecbcbc8e8271c1bb4157b29391ae3176ee446bf45ce9`.
- Installed Settings adapter SHA-256: `49d323167a9175b60bd2f0d8d5f77d47fe92d82bcd0dca8d113d22414b945482`.
- All four embedded WOFF2 buffers matched installed font files byte for byte; complete three upstream license files present. Browser platform-font records on Russian serif paragraphs showed actual Source Serif 4 and supported Geist Serif glyphs, not a renamed Mono/system substitute. Sans/Mono loaded in the matrix; Serif faces load only when selected.

Default RU / dark / Essential. Essay saved-screen IDs are invalidated once by `contentRevision`, while language, legacy/global theme and global font preferences persist. Exact authoring→HTML screen/source/method equality verified; builder adds derived `modes` metadata only. No unreachable second corpus.

### Structural and offline browser checks actually run

Maintained `audit_story_html.mjs --min-screens 3 --require-bilingual`: **69 checks, zero warnings, zero failures**, final descriptive collector HTML. This minimum is merely structural; it does not ask the author to pad to 96 screens.

Native Chrome `file://` only, external runtime blocked/offline emulation, unique temporary profile and dedicated ephemeral CDP endpoint per phase, `/usr/bin/timeout 30`, owned process-group/profile cleanup. No content server or `preview_*`.

| Viewport | Visits across both fonts | IDs | Horizontal overflow | Unreachable final paragraph tails | Runtime exceptions / HTTP runtime requests |
| --- | ---: | ---: | ---: | ---: | ---: |
| 320×568 | 584 | 37 | 0 | 0 | 0 / 0 |
| 390×844 | 584 | 37 | 0 | 0 | 0 / 0 |
| 1024×768 | 584 | 37 | 0 | 0 | 0 / 0 |
| 1440×900 | 584 | 37 | 0 | 0 | 0 / 0 |

Total **2336 actual DOM-navigation visits** = (13+23+37) × two languages × two themes × two fonts × four viewports. Each title/counter selection was checked against the correct stable ID; every slide scrolled to its bottom and its last paragraph measured within the scrolling viewport. Desktop rail was visible, current item synchronized and within view. Layout matrix uses reduced-motion emulation and two animation frames; it does not represent a physical device or measure performance during animation. Native page runtime exceptions and attempted HTTP(S) runtime requests were zero; additional control/visual suites also collected zero console errors.

Representative 320 and 1440 cover, English serif kitchen, Russian dark confrontation, shared final, and warning screenshots visually inspected. Preserved geometric cover, no publisher artwork. Prose-only corpus: no photo/list/comparison/chart layout invented merely to exercise a template.

### Navigation, Settings, focus and spoiler checks

- Native keyboard and pointer suites at 320 and 1440: ArrowRight, F, Escape, tap focus, horizontal pointer swipe, vertical-drag discrimination, Sources native Escape, final restart. Focus hides header/rail/progress/back/counter and keeps text/Next. These are Chrome pointer events, not physical phone touch tests.
- RU/EN switching preserves stable screen. Settings changes theme/font without rendering a new story node, preserving nonzero phone scroll (80 px), selected depth and position. Settings closes back to its trigger. Native Sources dialog remains accessible; no per-screen academic badges.
- Explicit Deep request opens native warning before mode/contents change; cancel and native Escape stay safe. Hidden late-ID navigation also requests consent before rendering title/body. Accept allows the action. Downgrading revokes consent, so re-entry warns again.
- Saved late position: reload opens safe cover/contents; visible button is neutral `Продолжить` / `Continue`, with no remembered scene title. Continue warns; cancel does not reveal content; accept restores the exact stable late ID. Consent is closure-only, never persisted. Pagehide/pageshow revocation tested with synthetic page-transition events, not an actual bfcache navigation journey.
- Storage-denial phase overrides localStorage/sessionStorage methods to throw; reading, Settings, navigation/focus and native spoiler cancellation still work in the open document.
- Chrome with iPhone Safari user agent: install guide appears after its existing 450ms delay, closes/reopens, hides in focus. Six visible controls remain one row; with 24px simulated safe top all were at y=47 and x=12…378 inside 390 px. Injected `navigator.standalone=true` suppresses guide and trigger. No physical Safari/iPhone/PWA install/hosting claim.

Test-harness corrections, retained honestly: wrong initial radio selector names; animation measured before settling; oversized combined-font phase exceeded request bound; native Escape initially omitted virtual-key codes; desktop pointer coordinates initially landed in the rail; iOS auto-guide was first asserted before its 450ms delay. Corrected harness and bounded per-font phases then passed. Artifact content/guard was not silently skipped to turn these into success. Four early completed Node harness processes that held their handles open were explicitly stopped; no associated Chrome/profile remained. Final harness exits explicitly after owned cleanup.

### Handoff scope

Files/hashes are in the ready manifest. Private source sample, intake backups, build scripts, raw QA JSON and screenshots stay outside the public repository. The only public deliverables changed are the assigned collector package and new pass-2 reports/ready manifest. Root reader SHA-256 remains `8bd3aad2d8cc97e0762d8e2c1c58578fc4802ae8aeb6599dbb8b15d76dc880b3`; catalogue/root/home/shared shell/installed skill/original audit/rescue/Git/PR/deploy were not changed. No source purchase, credential use, external message or subagent. Independent literary check is still required before a publisher decides to integrate.


### 2026-10-31 pass 2 — final targeted assertions

Additional final browser suites checked **146 counter/progress selections** (all nested modes × RU/EN) against exact 13/23/37 values and embedded metadata; seeded old essay revision/Deep/late ID were invalidated safely; English warning/cancel/accept and pre-consent title withholding passed. No runtime/console errors or HTTP(S) runtime requests. These supplement the 2336 layout visits without inflating that matrix count.

Deploy/review the exact submitted HTML hash. A fresh generic builder output alone lacks this book-local volatile consent integration; preserve/reapply the reviewed guard when synchronizing Settings or rebuilding. The working intermediate and integration script were kept privately outside public Git; no shared builder/installed-skill change is part of this package.


## Parent local correction — 2026-10-31

WFM-NP2-F01: corrected only the reflexive object in eggs-in-the-henhouse, RU грели → грелись and EN them → themselves. The Feegles’ excuse is that they were warming themselves under the hen, not warming eggs/stones. Parent checked the actual Pratchett henhouse dialogue reproduced in official Puffin Schools Resource Three, PDF page21/index20; classroom invention prompts are not used as novel actions. Source2 mapping, every other36 pair, IDs/levels/order/counts and all outer runtime/Settings/fonts/consent code remain unchanged. The connected manuscript is synchronized. No full primary novel reading or independent self-PASS claimed.

Parent focused regression: 48 checks passed; the corrected paragraph rendered exactly in Essential/Core/Deep in both languages,13/23/37 totals, complete body tails, zero horizontal overflow. The original body36otherpairs, runtime and reviewed guards remain unchanged. Zero runtime exceptions/remote requests; owned Chrome/process/profile cleaned. Existing large matrices remain historical; no physical Safari/PWA claim or self-issued independent PASS.
