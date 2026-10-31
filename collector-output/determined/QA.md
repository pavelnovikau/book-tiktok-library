# Determined — Robert M. Sapolsky — post-review verification

2026-10-31. Independent cold review: READY WITH FIXES; parent implemented every localized finding and rebuilt on the maintained template. This is repair/implementation verification, not a second independent editorial review.

## Closed findings

Basic desert no longer equates deserved blame with the intrinsic goodness of suffering; `long-term-question` adds a concrete hypothetical study instead of repeating a caveat; `selection-not-prescription` now explains the outbreak/selection and later transmission, and is classified as corroboration. The long Russian title on `safe-message` was rewritten after final QA caught 320px overflow. No scientific fact or clinical instruction was added without a source. Empirical evidence, philosophical inference and normative design remain distinct.

Exact nested **36 / 90 / 144**; 32 sources. Stable paired RU/EN IDs, levels and references. No new source-access claim, private file, artwork or copied chapter. Source ledger records the content changes. Reading estimates remain approximate and exclude reflection.

## Current validation

- Deterministic audit: **68 passes, zero warnings/failures**.
- Real Chrome/CDP file:// matrix, 320×568, 390×844, 1024×768, 1440×900; `(36+90+144) × 2 languages × 2 themes × 4 viewports` = **4,320 screen visits**. Rendered heading/count, document and slide/cover bounds checked on every visit. Both embedded fonts loaded; zero runtime/console exceptions and zero HTTP(S) requests.
- Native Space activated focused Chapters and Sources without paging. Dialogs/source count, paging keys, cover focus, hidden Start/depth controls/counter, safe Next, F/Escape after focused Next and second-tap exit passed at every viewport. Ordinary-iOS guide discovery, persisted-focus suppression and standalone suppression passed under emulation.
- Maintained shell uses quiet cyan, the intermediate-desktop cover correction and existing library metadata. Whole-library QA passed all 24 readers, including cover containment at 900/960px, native keyboard activation, counters/filters/semantic covers, focus and iOS states, zero runtime errors.
- Representative mobile and desktop captures were inspected. Long screens scroll vertically; no physical Safari or screen-reader test is claimed. Each manually launched browser used timeout 30, an isolated temporary profile/port and finally cleanup of its owned process group/profile.

Collector HTML SHA-256: `eca147012816be8c3639f8595521e89a9fe95d81f05e30ea7558b8dab7dfd802`.

The historical collector report below is retained as original research/implementation history. Its earlier shell/color measurements and fingerprints are superseded by this report. Original full-book access and prior checks remain collector-reported within their stated limits.

---

# Determined — collector QA

Completed 2026-10-31. Scope: this directory only. No shared catalogue, root reader, shared template, LOG.md, deployment, push or PR was changed/performed.

## Delivery

- `determined.html`: standalone offline HTML, 475,760 bytes; embedded Geist and Geist Mono; no remote runtime dependencies, publisher artwork, copied book passages or invented page citations. No raster/media assets; cover is the maintained abstract HTML composition. Sources are optional outbound links.
- RU default, dark default, Deep default; complete EN content and interface parity; Flexoki light/dark; one violet primary action per screen.
- `story-data.json`: schema v2 authoring corpus. `sources.md`: claim map, direct URLs, consulted coverage and gaps. `qa/`: reproducible build/QA helpers, audit, matrix logs, review ledger and 24 screenshots.
- The library Home link retains maintained `href="./"`; this collector directory has no root catalogue. Actual library registration is deliberately out of scope.

## Exact cumulative counts and words

Counts include cover and final, both level 1. Essential ⊂ Core ⊂ Deep.

| Mode | Screens | RU words | EN words | RU minutes | EN minutes |
|---|---:|---:|---:|---:|---:|
| Essential | 36 | 1,923 | 2,228 | 11 | 11 |
| Core | 90 | 4,840 | 5,637 | 27 | 26 |
| Deep | 144 | 7,765 | 9,045 | 44 | 42 |

Words use the maintained builder tokenizer, counting title + subtitle + body, excluding UI/source notes. Reading times are rough calculations at 180 RU / 220 EN words per minute, not a promise of comprehension time. Layer sizes: 36 level-1, 54 additional level-2, 54 additional level-3.

Non-cover body density: RU mean 47.08 words, range 39–52, total 6,732; EN mean 55.27, range 46–60, total 7,904. Cover bodies are intentionally shorter. Translation length differs naturally; stable IDs, sources, levels and qualifications are shared.

## Provenance and evidence boundary

32 sources. Screen distribution: 18 `book`, 34 `corroboration`, 91 `synthesis`, 1 cover. `corroboration` includes independent scientific findings, authoritative conceptual distinctions and objections; it does not mean every source supports Sapolsky. The high synthesis share is deliberate and disclosed: this is an analytical synthesis under incomplete book access, not a claim to have reconstructed a complete reading.

**No full lawful local edition was confirmed. The entire book was not read.** Direct book consultation: official TOC and selected passages in chapters 1–2 from the official UK sample. Later architecture comes from TOC plus author interview/summary material; complete chapters 3–15, interlude prose, notes, all examples and edition-specific nuances remain unverified. Abstract-only, indexed-only and blocked sources are identified individually in sources.md. Audio was not claimed as listened to. Independent research is never asserted to appear in the book merely because it is included here.

The corpus distinguishes the author's argument, empirical result, philosophical inference, serious compatibilist/libertarian objections and digest synthesis. It separates causation from strict determinism, prediction, exculpation and policy. It explicitly rejects fatalism and makes no legal, medical or psychiatric recommendations or biomarker-based predictions of individuals.

## Every-screen content inspection

All 144 bilingual screens were read during authoring and reviewed against their cognitive jobs after assembly; see `qa/screen-review.tsv`, one row per stable screen. Checked mechanisms, examples, consequences, qualifications and transitions rather than splitting prose to reach the quota. No exact duplicate title or normalized body in either language; no ordinary body below 39 RU / 46 EN words. No quota-only continuation screens retained.

Related distinctions recur intentionally in different jobs: forecasting versus control in chaos; statistical versus individual inference in neuroscience; exculpation versus prevention in justice; effort versus authorship in change. These are not presented as newly discovered book findings. The 36-screen Essential path independently retains thesis, causal continuity, scientific objections, a serious critical bridge, change, justice, merit, practical tension and final model. Core/Deep insert detail in order.

## Deterministic audit

Command:

```sh
node skills/book-tiktok/scripts/audit_story_html.mjs determined.html --min-screens 144 --require-bilingual
```

Result: **68 passes, 0 warnings, 0 failures**. Exact mode counts, bilingual corpus, provenance/source references, offline invariants and maintained shell checks passed. The audit's separate word counter excludes subtitle words: 7,759 RU / 9,038 EN; the table above consistently uses builder totals.

## Isolated real-browser matrix

Actual installed Chrome in headless mode, loaded by `file://`, no web server. Each launch wrapped with `timeout 30`, its own `mktemp -d` profile and a unique debugging port; process group terminated and profile deleted in `finally`. No shared browser was attached or killed.

| CSS viewport | Languages | Themes | Modes | Render visits | Result |
|---|---|---|---|---:|---|
| 320×568 | RU, EN | dark, light | 36/90/144 | 1,080 | pass |
| 390×844 | RU, EN | dark, light | 36/90/144 | 1,080 | pass |
| 1024×768 | RU, EN | dark, light | 36/90/144 | 1,080 | pass |
| 1440×900 | RU, EN | dark, light | 36/90/144 | 1,080 | pass |

Total **4,320 real DOM renders** in the final matrix: all screen IDs in all nested modes, both languages and both themes at every viewport. Per-render title, selected-mode position, horizontal overflow and rail selection checked. Zero horizontal overflow >1px; zero runtime/console errors; zero HTTP(S) requests from the artifact. Embedded fonts loaded; image decoding N/A because no images are used. Desktop rail displayed, scrollable and active item visible after navigation. All five compact top controls fit at 320px.

Functional checks at every viewport: language/theme switch preserves position; 32-item Sources dialog and Chapters dialog open/close; selecting a hidden Deep screen from Essential raises mode; forward/back keyboard; actual Next buttons; synthetic pointer swipe; vertical gesture and long-press discrimination; focus by text click and F, Escape exit, second click exit, paging retains focus, header/rail/counter hidden and Next remains inside viewport; saved progress, Continue, Start over and final restart.

Visual review: 24 settled screenshots (six representative screens × four viewports), inspected individually and as `qa/contact-sheet.png`: cover, dense causal prose, evidence-boundary fact box, comparison, sequential checklist and final. Both themes/languages represented. At 320px, longer content intentionally scrolls vertically; off-screen continuation is not truncation. No forced small-font fitting. Raster/image layout N/A. This is desktop Chrome emulation of CSS viewports, not physical iPhone/Safari validation.

## Local fixes and reproducibility

Used the maintained builder without editing shared files. Collector-only postprocessing in `qa/local-finish.py` applies the requested royal-violet action tokens (the installed shell had teal defaults), exposes hidden-depth chapters in the Chapters dialog, hides the counter in focus mode, permits long title wrapping, and stacks comparison columns on phones. An initial 320px overflow of 2px in the antifatalist heading was corrected. Early screenshots caught an entrance-animation phase; final captures await settled animations. The final complete browser matrix was rerun after geometry changes and passed.

```sh
python3 qa/author.py
node skills/book-tiktok/scripts/build_story.mjs story-data.json --out determined.html
python3 qa/local-finish.py
node qa/browser-qa.mjs
```

The builder's installed shared version can change independently; these helpers document the local finishing delta. Do not rerun on a different shared shell without re-auditing. Final HTML SHA-256: `ecac9358d71dd97f5cf6337aed8e2958efaae4a569ec9fa4f16d6131ce8be858`.

No external delivery or publication performed. Cleanup verification follows in the final execution record below.

Cleanup verified: 0 Chrome processes using this task’s profile prefix; 0 `/tmp/determined-qa-*` profiles; no server started.
