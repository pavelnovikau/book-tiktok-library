# Howl’s Moving Castle — implementation QA

Date: 2026-10-31. State: prepared for independent check, not independently approved.

## Corpus and scope

New queued title from BOOK_PLAN.md; no existing root reader, catalogue entry or collector corpus was modified. Exact work: Diana Wynne Jones’s 1986 novel. Content mode `narrative`; defaults `ru` / `dark` / `essential`.

- Exact nested screens, cover and final included: **15 Essential / 25 Core / 39 Deep**.
- Levels: 15 at level 1, 10 additional at level 2, 14 additional at level 3.
- All **39 RU/EN pairs** read by the implementer; 0 old pairs existed. Essential and Core sequences were read separately, with the same unresolved flower-shop stopping point.
- Builder reading-time estimates: **5 / 8 / 13 minutes** in both languages.
- Builder title/subtitle/body word counts: RU **850 / 1406 / 2228**; EN **1044 / 1685 / 2654**. These are estimates of reading volume, not screen quotas.
- The 37 narrative bodies average 54.8 RU / 64.7 EN words, range 35–72 RU / 43–88 EN. Counts were derived after the continuous original prose and segmentation; no old target was retained or padded.
- 32 direct source records, with explicit excerpt/guide/quotation/metadata roles and access scope. One embedded original typographic SVG cover. No remote runtime assets.

## Reproduce, scoped to this collector

```sh
python3 collector-output/howls-moving-castle/segment-draft.py
node collector-output/howls-moving-castle/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/howls-moving-castle/howls-moving-castle.html --min-screens 39 --require-bilingual
node collector-output/howls-moving-castle/qa/check-reader.mjs
```

`build-local.mjs` invokes the maintained builder and adds only this book’s session-local spoiler consent. The maintained builder already includes the compact icon header, embedded Geist/Geist Mono, focus mode and iOS guide. No shared shell, installed skill, unmerged settings/font code or catalogue-wide reader sync was copied or changed.

## Deterministic results

`qa/structural-audit.txt`: 69 structural checks passed, no warnings or failures. This verifies data/runtime structure, not literary fidelity. `qa/build-result.txt` records the builder counts. Runtime-parsed embedded JSON was compared to the canonical authoring JSON in every browser phase; only builder-computed mode metadata and embedded media differ.

## Browser results

Final file tested with network HTTP(S) blocked, directly from its standalone file URL. Four phases have saved JSON results in `qa/`: `layout-phone.json`, `layout-desktop.json`, `interaction.json`, `ios.json`. The artifact binding is recorded in `qa/verified-artifact.json`.

- **320×568, 390×844, 1024×768, 1440×900**, both languages and both themes. Every screen in all three modes was traversed at each combination: **1,264 rendered route positions** total. Exact mode counts, matching rendered titles, nonempty prose, no horizontal overflow, hidden narrative footnotes, bounded single-row icon header and visible desktop rail were checked.
- Embedded Geist, Geist Mono and SVG cover decoded offline. No external runtime requests or unexplained runtime/console errors in the final phases.
- Sources dialog exposes all records and honest method notes. Language/theme changes preserve the screen. Buttons, chapter navigation, keyboard and horizontal swipe work; a vertical gesture does not page.
- Deep selection requires an explicit localized warning. Cancel preserves the shallow route. Session reload does not inherit spoiler consent from a saved Deep mode. Cover resume uses a generic spoiler warning instead of the hidden screen title. Accepted resume restores the exact saved ID; cancellation keeps the cover intact. The same guarded ID entry also protects the hidden saved chapter path.
- Focus mode verified by keyboard at 320/1440 and by taps on reading text: chrome hides, Next remains, paging preserves focus, second tap/Escape restores chrome. Final restart returns to the cover.
- Emulated iPhone browser: automatic/manual install guide and a **47px simulated safe top inset** tested at 320px, with compact controls inside the viewport. Emulated standalone mode suppresses the install guide. This is not a physical iPhone, Safari or PWA installation test.
- Screenshots visually inspected: phone cover/dense/final, desktop dense/final, consent modal, focus and iOS safe-area cases. At 320px the cover and densest prose use the intended vertical scroll; the header and Next stay available.

The added tap check initially hit a **QA harness** global-constant redeclaration. The harness expression was isolated and rerun successfully. No reader content/code defect was hidden by that failure.

Each phase launched `/usr/bin/timeout 30` with its own `mktemp -d` profile and an owned process group. Finally/exit cleanup terminated that group and removed the profile. No local server was started. Reports record profile removal.

## Editorial limits and handoff

The separate implementation evidence map records every stable screen, the actual consulted locations, source limitations, the Angorian-entry attribution discrepancy and six implementation corrections. No retained essential link is presently identified as unsupported within the disclosed guide-plus-selected-passage boundary. That assessment is for independent checking, not a whole-edition fidelity certificate.

No full primary edition was read continuously and no published RU translation was certified. Omitted subplots, exact print pagination and unconsulted wording remain outside scope. The publisher still owns independent content approval, root/catalogue integration and production/PWA verification. No Git, PR, deploy or external messaging action was performed.


## Parent local correction — 2026-10-31

HMC-R1/R2: parent directly checked the HarperCollins/Litres chapter-one family passage: Fanny is Martha’s birth mother and Sophie’s stepmother. Only the collective EN relationship is narrowed. Parent also checked the public SuperSummary Chapter7 narrative account: Sophie is still worried about Martha before the scarecrow chase, while Michael’s clarification comes later. The opening now explicitly looks back to that earlier belief, retaining the existing compressed two-letties order. Source9 and other source IDs unchanged. The guide is secondary; no complete primary chapter7 or full-novel reading is claimed.

Only embedded data/derived mode estimates and the matching connected manuscript(s) were refreshed. Outer code/styles and bespoke spoiler guards are byte-identical. Older segmentation generators are pre-correction preparation artifacts; the updated story-data.json is the maintained builder input. Original independent review remains unchanged; localized publisher validation is pending, not self-issued PASS.

Parent focused regression completed: 176 assertions across the four corrected readers, RU/EN and 320/390/768/1440 widths with light/dark representative cases. Exact changed copy, scroll tails, no horizontal overflow/runtime/network requests, saved-Deep warning, cancel and accepted restore passed. Ender uses browser confirm; the harness explicitly accepts/dismisses it. Failed harness diagnostic retained separately; no product-runtime correction was needed. Owned Chrome/profile cleaned. Per-reader structural result remains 69 passes. Not physical iPhone/PWA or new independent literary approval.
