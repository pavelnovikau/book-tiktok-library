# Seeing Like a State — implementation QA

Status: local technical checks and authoring self-check complete; **independent editorial/source review pending**. This file does not issue independent PASS or authorize publication.

New approved queued work. No pre-existing collector package or root reader for this slug was present at task start, so old pairs read: **0**. New authoring pairs read: **31** (RU and EN, including cover/final). Effective embedded pairs: **31**, mechanically compared with the authoring corpus and traversed in the browser. `contentMode: explanatory`; exact cumulative `targetModes`: **17 / 25 / 31**, derived after the prose draft and route self-check. Level increments: 17 / 8 / 6. Defaults: RU / dark / Essential.

## Editorial self-check

The argument proceeds from fiscal forestry and the remaking of forests through high-modernist confidence and four combined conditions, Brasília's intended and actual order, rural/informal dependency, métis, its adaptability and unequal availability, and the author's explicit rejection of a blanket attack on state/scientific knowledge. Each mode was checked as a continuous sequence. Mat Isa's complete case appears in Essential before its subsequent qualification names him. Deep inserts context and qualifications without being needed to repair a severed shallower case.

All 31 bilingual pairs were read in authoring. Numbers, names, conditional statements, attribution and outcomes were compared. Rendered titles/bodies were then matched to that data in every route/language/theme combination. This is the implementing worker's own content check, not an independent editorial review or certification of an official Russian translation.

Specific safeguards and corrections made before readiness:

- `brasilia`: retained Costa's plan and Niemeyer's buildings; explicitly differentiated influence from Le Corbusier's authorship. Rejected the erroneous editorial framing in one source.
- `four-elements`: added explicit authoritarian power in both languages and retained the conjunction, rather than treating any one element as a sufficient cause.
- `first-rotation` / `second-rotation`: retained genuine initial gains, delayed biological consequences and Scott's attribution; no universal claim that all forestry or planning fails.
- `fields-that-survived`: confined the Soviet/Tanzanian account to chapter 9's actual recap. Added no village names, invented dialogue, relocation totals or chapter-7 causal particulars.
- `mat-isa` / `metis-keeps-changing`: Mat Isa's actual ant intervention is distinguished from Scott's explicitly hypothetical use of a cheap pesticide.
- `metis`: revised a draft reciprocal “neither replaces the other” formulation into the narrower supported point that general rules alone do not supply situated skill.
- `public-goods`: English was narrowed from “depend on” to “owe much to,” matching the book's historically influenced/qualified account and the Russian text.
- `first-rotation` / `mat-isa`: the first 15/25/31 segmentation left Mat Isa's name unintroduced in Essential's later qualification and made the initial forestry success too implicit. Promoted these two existing paragraphs to level 1. Final counts are 17/25/31; no text or screen was padded/added.
- `simple-for-whom` / `unequal-access`: retained inequality in local custom and restricted access to practical knowledge. Locality is not equated with justice.

Evidence boundaries are in `sources.md`; chapter 9 was OCR-read, selected passages of chapters 1/4 checked, chapter-3 author excerpts used, and the Introduction's four-element passage checked through an explicit scholarly quotation. No continuous full-book reading is claimed.

## Build and structure

`build-local.mjs` calls the maintained `skills/book-tiktok/scripts/build_story.mjs`; it does not copy a different reader. `qa/build-evidence.json` records builder/template/header hashes. The only added presentation is book-local CSS: a typographic cover replaces the generic seven-node cover placeholder; per-screen source labels are hidden while embedded maps and the global Sources dialog remain available. The corpus stays explanatory. No PR29/unmerged settings implementation was copied or recreated. Publisher must apply the latest maintained shell at integration.

Maintained `audit_story_html.mjs`: **69 structural checks, 0 failures, 0 warnings** (`qa/structure.json`). This is technical validation, not proof of fidelity. `qa/corpus-check.json` records JSON/embedded equality, exact counts, defaults, source-map consistency and word density.

## Offline and browser checks

Book-owned `browser-qa.mjs` uses `file://`, CDP and offline network emulation. It starts no HTTP server. Every Chrome is launched under `timeout 30`, with an individual `mktemp -d` profile and isolated process group; it kills only the owned process/descendant tree and verifies profile/process cleanup.

- **320×568, 390×844, 1024×768, 1440×900:** all 31 pairs, all nested routes, both languages and both themes. **1,168 rendered screen visits** in the final four matrix reports: 292 per viewport. Correct title/body, counter, active rail and exact route counts; no horizontal overflow; source footers hidden. Long mobile text remains vertically scrollable.
- **390×844 and 1440×900 interactions:** language/theme retain the screen; Sources/method and Contents dialogs; Core chapter navigation; focus by keyboard and text pointer event; Escape; focus while paging; horizontal gesture advances without focus toggle; vertical gesture does not page/toggle; keyboard next; saved Continue; Start over; final restart clears remembered screen. Gesture events are emulated, not physical touch measurements.
- **320×568 iPhone UA / engine safe area:** automatic guide, localised guide, six accessible icon-only controls in one row, top=47px/bottom=34px inset simulation, reading scroll, safe-bottom Next in normal/focus mode, restored header, and guide/trigger hidden with `navigator.standalone`. No physical iPhone/Safari/PWA release test is claimed.
- All final reports: offline fonts loaded, zero external HTTP runtime requests, zero runtime/console exceptions, unique profile removed, no owned Chrome processes left, no server started. Optional source links are not runtime dependencies.

Representative cover and dense prose screenshots were visually inspected at phone/desktop widths. A rapid RU/theme screenshot initially caught an unfinished compositor frame; adding a 200ms/two-frame settle to the capture procedure produced readable text without changing the reader. An initial CSS-variable safe-area probe gave a false-negative geometry result; the final test uses Chrome's actual `Emulation.setSafeAreaInsetsOverride`, as in the maintained browser protocol. It passes with controls at y=70px under the 47px inset. These probe issues are not silently presented as reader fixes.

## Remaining limits

Independent content/source-sufficiency and bilingual review of every pair remains required. Evidence is a bounded central-argument account, not full chapter coverage or a complete-edition collation. OCR can contain errors; retained mechanisms have passage locators for a reviewer. No claim of contemporary independent forestry, medical or historical validation is made. The book's medical examples are not used.

Collector-only delivery. Root reader, catalogue, index, shared reader shell, release docs, Git/PR/deploy and production progress integration were not edited. No installed skill or shared log was changed. Physical iPhone/PWA and production behavior remain for publisher verification.
