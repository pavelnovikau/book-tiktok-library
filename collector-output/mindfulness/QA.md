# Mindfulness — repaired collector QA

Date: 2026-10-31. Status: PASS after cold-review corrections and parent verification. This is a repair/implementation report, not a claim of a second independent review.

## Contract and source boundary

Exact cumulative Essential / Core / Deep: **30 / 72 / 112**; levels 30 / 42 / 40. Cover and final are level 1. RU and EN share stable IDs, levels, source references and provenance. Defaults: RU / dark / Deep. Standalone HTML embeds both Geist fonts, CSS, JavaScript and data; no network dependency or publisher artwork.

The original collector consulted a complete local Russian EPUB read-only: Williams and Penman, «Осознанность: как обрести гармонию в нашем безумном мире», translated by Ю. Цыбышева, scientific editor Н. Никольская, МИФ 2014, ISBN 978-5-00057-213-9. It inspected metadata, spine and structure plus substantive passages across all 12 chapters and weekly practice schedules. This is selective consultation, not line-by-line reading of every paragraph. Edition fingerprint and the metadata date anomaly remain in sources.md. The repair pass did not reread the whole EPUB. No original EPUB, private path, image or meditation script is redistributed.

## Closed cold-review findings

- `nice-boundary`: NICE NG222 1.8.5 is explicitly scoped to higher-risk people who remitted with antidepressant medication alone; group MBCT/CBT options depend on decisions about continuation. Other remission pathways are separate. The eight-session / two-to-three-month schedule belongs to 1.8.6. Official NICE recommendations and the PubMed primary abstract were rechecked during repair.
- `action-menu`: replaced the inaccurate completion framing with enjoyment, mastery/control and continuing with awareness, preserving the distinct week-eight completion screen. Corrected two-column list markup after the final 320px traversal exposed overflow in the longer Russian label.
- `general-memory`: dominant provenance is corroboration. Heeren et al. is described as quasi-experimental with matched controls, not randomized; the narrow, non-diagnostic interpretation stays explicit.
- Quiet Flexoki cyan, actual counter hiding, native Space activation on focused controls, F/Escape after Next, cover-focus text plus Next and bilingual iOS browser/standalone guidance all use the repaired maintained shell. The cover's depth picker and Start actions hide in focus mode.

Clinical limits remain visible inside Essential: reading is not clinician-led MBCT/MBSR, no medication-change instruction, no zero-risk or universal-benefit promise, stopping and obtaining support are legitimate, and acceptance does not excuse danger or structural constraints.

## Content and density

Eleven sources, all used. Provenance: 89 book / 9 corroboration / 14 synthesis screens. The cold reviewer read all 112 paired RU/EN screens and found no material padding, fabricated finding, dangerous instruction or translation drift; the three localized findings above were corrected. Internal EPUB chapter locators stay attached to book-specific claims; no print pages invented.

| Mode | Screens | RU words | EN words | RU minutes | EN minutes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 30 | 1594 | 1866 | 9 | 9 |
| Core | 72 | 3824 | 4420 | 22 | 21 |
| Deep | 112 | 6029 | 6879 | 34 | 32 |

Builder counts include titles, subtitle and body/list indices, excluding interface text. Estimates use 180 RU / 220 EN words/minute and exclude practice/reflection. Auditor totals are 6023 RU / 6872 EN because its subtitle handling differs.

## Validation performed after repair

- Deterministic auditor: **68 passes, zero warnings/failures**; exact targets and offline construction passed.
- Real Google Chrome via Playwright/CDP, file://, no server or collaborative preview. Each viewport used `timeout 30`, an isolated temporary profile/port and finally cleanup of the owned process group/profile.
- 320×568, 390×844, 1024×768, 1440×900: each visited `(30 + 72 + 112) × 2 languages × 2 themes = 856` states; **3,424 visits** total. Actual rendered titles, counts, document and slide overflow checked on every screen. Zero layout issues, runtime/console errors or HTTP(S) requests. Both embedded fonts loaded.
- Native Space opened focused Chapters and Sources without paging; both dialogs/source count, paging keys, focus on cover, hidden Start/depth picker/counter, safe-area Next, F/Escape after focused Next and second-tap exit passed at every viewport.
- iPhone browser emulation showed the guide; saved focus and standalone emulation suppressed it. No physical Safari or screen-reader test is claimed.
- Visually inspected mobile cover/list and desktop evidence/provenance screens in light and dark; short-phone content remains vertically scrollable by design.
- Whole-library QA after initial integration passed all 21 readers, native Space, catalogue counts/covers/filters, phone/desktop focus and iOS browser/standalone states with zero runtime errors.

The initial repair QA caught a real Russian list overflow and it was fixed. A later QA harness attempt targeted an intentionally closed dialog item with a physical click and timed out; the harness was corrected to invoke chapter navigation programmatically, then the final full matrix passed. Neither failed attempt is counted as a pass.

## Reproduction

From repository root:

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/mindfulness/story-data.json --out collector-output/mindfulness/mindfulness.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/mindfulness/mindfulness.html --min-screens 112 --require-bilingual
```

Collector HTML SHA-256: `774683e6b1063b488c6948cb898086045794c202c4efa65078ca5bec129654e5`.
Story data SHA-256: `bc59a88779005b8ac3ed0f13cef5916fb6d545d9b181d52795e8d6eb1a25ef14`.
Root reader additionally receives library metadata/install normalization through `scripts/apply-reader-shell.mjs`. Publication is tracked by the parent in BOOK_PLAN.md and the repository history.
