# Huck Finn — local implementation QA

Date: 2026-10-31. Status: **local checks passed; ready for independent content check**. This record is not an independent editorial PASS and does not authorize or certify publication by this worker.

## Canonical package

- `story-data.json`: v2, `contentMode: narrative`, `spoilerPolicy: full-plot-in-deep`.
- `adventures-of-huckleberry-finn.html`: standalone bilingual reader; fonts/CSS/JS embedded, no runtime network dependency.
- `sources.md`: witness identity, exact access/reading scope and a primary-text map for every stable ID.
- This file: implementation checks and remaining limits.

All 54 unique RU/EN pairs were read. No prior Huck Finn reader/collector or catalogue entry existed. Generated embedded content matches authoring; the only expansions are the builder’s computed mode labels/minutes. Plain JSON-to-HTML parity is not used as evidence of editorial fidelity.

| Depth | Exact cumulative count | RU words | EN words | RU / EN minutes |
| --- | ---: | ---: | ---: | ---: |
| Essential | 24 | 1,917 | 2,334 | 11 / 11 |
| Core | 36 | 2,839 | 3,455 | 16 / 16 |
| Deep | 54 | 4,227 | 5,124 | 24 / 24 |

Level additions: 24 / 12 / 18. Cover and common final are included. RU body mean 75.9 words; EN 91.9. The mode duration is an estimate, not a reading promise. Deep’s Russian duration uses the explicit correct inflection `24 минуты`.

## Reproducible build and checks

Run from the repository root:

```sh
python3 collector-output/adventures-of-huckleberry-finn/author-story.py
node collector-output/adventures-of-huckleberry-finn/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/adventures-of-huckleberry-finn/adventures-of-huckleberry-finn.html --min-screens 54 --require-bilingual
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 320 568 matrix
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 390 844 matrix
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 1024 768 matrix
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 1440 900 matrix
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 320 568 behaviour
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 390 844 behaviour
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 1440 900 behaviour
node collector-output/adventures-of-huckleberry-finn/qa-huck.mjs 390 844 ios
node collector-output/adventures-of-huckleberry-finn/verify-huck.mjs
```

The HTML builder itself is maintained shared code; the wrapper owns only this book’s consent, presentation and provenance-preserving additions. **Do not replace the final HTML with plain builder output**, which lacks the local spoiler guard. No shared template/header file was edited. Rebuilding through the wrapper was byte-stable. The verification helper rejects stale browser hashes and requires all eight final browser receipts.

## Results

- Maintained deterministic audit: **69 checks, 0 warnings, 0 failures**. Receipt: `qa/huck-structure.json`.
- Canonical/embedded parity, exact target counts, source-map coverage for all 54 IDs, duration calculation and stable rebuild: `qa/huck-consistency.json`.
- Four viewport matrix reports: `qa/huck-{320,390,1024,1440}-matrix.json`. Each covers Essential/Core/Deep × RU/EN × dark/light: **48 combinations, 1,824 rendered-screen visits** overall. Each visit compares the **whole rendered paragraph text**, title, stable ID, progress and expected count, checks every header control within one row, and checks horizontal bounds and reachability of the final paragraph. No body is clipped beyond reachable vertical scrolling. Cover actions are reachable at 320px. The desktop rail follows the active entry.
- Behaviour reports at 320/390/1440: hidden Core chapter raises mode; a hidden Deep chapter cannot reveal its body before consent; cancellation and keyboard cannot bypass the warning. Repeated language/theme switches preserve mode and ID. Pointer swipe works; a vertical gesture does not turn a page or toggle focus. Tap/F/Escape focus, buttons, dialogs, Start over and final restart were exercised.
- Saved Deep regression: on reload the cover’s label is **generic** (`Continue Deep — ending spoilers` / RU equivalent), active depth is Essential, the remembered Deep ID remains saved, and Continue requires fresh book-local consent. Acceptance restores that ID in Deep. Downgrading revokes consent. Every level-3 TOC title is masked before consent. The common final, cover, description and global Sources notes disclose no ending outcome.
- `qa/huck-390-ios.json`: iPhone user-agent emulation, automatic install guide, localized instructions, manual trigger, standalone suppression. Chrome engine safe-area override: top 47px / bottom 34px; all six header icons stay below the inset and inside one row; focus hides install UI and returns to correct placement. **No physical Safari/iPhone test is claimed.**
- All phases load the local file with networking emulated offline: **zero runtime exceptions, zero external runtime requests**. Both embedded font families decode. Sources links are optional external navigation, not loading dependencies. No image assets are required.
- All browser runs use a dedicated `mktemp -d` profile, their own process group and `timeout 30`. Cleanup terminates that group and deletes the profile in normal and failure paths. No server is used. All final receipts record `profileRemoved: true`.

## Visual inspection

Representative PNGs are local evidence in `qa/`. The 320px dark cover and dense Russian reading screen and the 1440px English light reader were inspected. The phone uses full-size readable prose and vertical scrolling; header icons stay in one compact row. The desktop has a restrained reading column and scrolling contents rail. Additional captures show Sources, focus, consent and the emulated iOS safe area. There are no list/comparison/photo screens in this narrative to inspect.

## Editorial boundaries

The primary source is the complete Gutenberg English witness #76. Actual reading was selected substantive scenes across all 43 chapters, not a continuous every-paragraph reading. The Russian prose is a new retelling, not a published translation. Each retained event/motive has a chapter map. No full private text or extraction is included in this repository, no invented dialogue/pages are used, and no future Jim-family reunion or Pap-murder explanation is supplied.

The saved HTML is ready for another reader to check all 54 changed pairs and their primary support. Publication, root/catalogue integration, legal/translation completeness and independent editorial acceptance remain unclaimed. See `editorial-audit/2026-10-31/books/adventures-of-huckleberry-finn-sol-implementation.md` for the substantive report and concrete self-review corrections.
