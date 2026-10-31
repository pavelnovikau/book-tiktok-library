# Meditations — implementation QA, 2026-10-31

State: **worker-local checks passed; ready for independent content check.** This is not an independent PASS, publication approval, or production receipt.

## Package and actual reading

- Canonical authoring: `story-data.json`; generated portable reader: `meditations.html` (406,731 bytes).
- New approved title: no prior collector corpus or published root reader existed for this slug. Existing delivery/draft pairs read: 0. Final pairs actually read: **39 RU/EN pairs / 78 language screens**; the nested sequences were inspected for continuity.
- Exact cumulative counts: **Essential 18 / Core 30 / Deep 39**, level increments 18 / 12 / 9, asserted in `targetModes`. Counts follow the retained connected argument; no historical total or filler quota.
- `contentMode: explanatory`; fresh **RU / dark / Essential**. Reader times: RU **7 / 11 / 14 minutes**, EN **7 / 11 / 14 minutes**.
- Approximate body-word statistics: RU **2,355**, median **58**, range **35–79** per screen; EN **2,748**, median **69**, range **39–90**. The maintained builder's title/body token counts are RU **1,159 / 1,885 / 2,492**, EN **1,344 / 2,206 / 2,908**. These are descriptive word-count estimates, not quotas.
- **14 paired quotation excerpts**: all RU excerpts visually checked against the original 1914 Rogovin scan; all EN excerpts exact in numbered Long/Gutenberg; 13 additionally compared with MIT. Same primary passage in each language. Common closing locator XII.36 = original Rogovin XII.35, explicitly attributed.
- Complete editions obtained; selected passages across all twelve books read and compared. Continuous reading of both editions, complete Greek/translation fidelity, and coverage of every section are not claimed. Exact quotation ledger and 39-row evidence map: `sources.md`.

## Reproduction and local presentation

```sh
node collector-output/meditations/build-meditations.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/meditations/meditations.html --min-screens 39 --require-bilingual
node collector-output/meditations/qa/browser-meditations.mjs traverse
node collector-output/meditations/qa/browser-meditations.mjs interactions
```

The book-local wrapper invokes the maintained v2 builder; it does not copy its reader shell. Its small reproducible adjustments hide generic research footers while retaining source arrays, the Sources dialog and `contentMode`; shrink the documentary title leaf on phones; and change RU Start to «Начать чтение». Desktop retains the full title-leaf credit, and source attribution remains in Sources. No shared template, root reader, catalogue or index was edited.

No previous book-specific code or spoiler consent existed to replace. This nonfiction has no fictional-ending consent gate; ordinary saved Deep restoration was tested. No other book was modified.

## Deterministic checks

Maintained HTML auditor: **69 checks, 0 warnings, 0 failures**. Metadata and exact nested counts match the authoring corpus; every embedded screen equals canonical JSON. Stable IDs, RU/EN copy, source IDs, offline assets and responsive hooks pass. Raw output: `qa/structure-audit.json`.

`qa/quotation-check.json` distinguishes all fourteen exact Gutenberg matches and the thirteen additional MIT comparisons. MIT spells `judgement` where Gutenberg has `judgment`; two other excerpts have comma differences. MIT XII actually stops inside §26 and does not verify the closing quote. It is not counted as a successful comparison. Russian OCR was a locator aid only: quotation authority is the image of the 1914 page. Mechanical checks do not establish literary fidelity or independent approval.

## Offline, mobile and interaction checks

The standalone file was opened as a local `file:` document with Chrome networking explicitly offline. Each phase launched Chrome with **`/usr/bin/timeout 30`**, its own **`mktemp -d`** profile and dedicated debug port; `finally` kills the owned detached process group and removes that profile. No HTTP server was started. Both reports bind to the current HTML SHA-256. Both profiles were removed, and a final process inspection found no owned Chrome residue.

**1,392 positions** were traversed: (18 + 30 + 39) × RU/EN × light/dark × **320×568, 390×844, 1024×768, 1440×900**. Every position was checked for the exact title, mode count/counter, quotation text, zero horizontal overflow and reachable vertical scroll tail. All 39 distinct pairs appear in every full traversal. All 16 layout/language/theme combinations retain one compact accessible icon-only header row; desktop rails show the correct active item. Long text scrolls inside its reading area without losing the navigation.

Interaction phase: **27 checks**. Language/theme preserve position. Sources exposes three sources, actual evidence scope and translator concordance. Contents opens, closes and navigates. Buttons, keyboard and horizontal pointer swipes work; vertical gestures do not page. A reading-text tap enables focus, a second restores chrome; F, Escape and paging preserve the expected focus state. Reload offers Continue; Continue restores the stable ID; Start over restarts reading; a saved hidden Deep screen raises depth; final Restart clears saved progress.

At 320 px the header remains below an **emulated 47 px iOS status safe area**. Emulated iPhone Safari offers the install guide, retains its compact-row trigger and can reopen it manually. Emulated standalone hides guide and trigger. **No physical iPhone/PWA test is claimed.**

Runtime exceptions: **0**. External runtime requests: **0**. Embedded Geist, Geist Mono and the documentary image decode offline. Raw reports: `qa/browser-traverse.json`, `qa/browser-interactions.json`, `qa/content-scope.json`, `qa/build-inputs.json`.

Settled screenshots, captured after animation completion, remain outside public Git at `/Users/pn/smartcat/_private/book-tiktok-evidence/meditations-20261031/browser-qa/`. Visually inspected fresh RU/dark/Essential cover, saved cover, RU waking quote, dense RU anger passage, 320 EN/light quotation and final, desktop final/rail and safe-area cover. The phone cover's initial oversized title leaf was capped locally. Some 320 px reading screens intentionally require vertical scrolling; the final paragraph remains reachable above the navigation.

## Handoff boundary

No Git, PR, deploy, root-shell/catalogue changes, external messages or subagents. Publisher integration and independent editorial review are outstanding. Final package status: `ready-for-independent-check`. Source limits concern selective reading, historical translation differences and MIT truncation; no unsupported essential argument link remains in the retained text.
