# Local QA — The Structure of Scientific Revolutions

Status: implementation checks complete; **independent editorial check pending**. This document is not an independent PASS.

## Corpus and editorial check

- New approved queued title; no previous assigned collector package or published root reader existed to repair or compare.
- Original connected RU/EN prose was drafted before IDs, levels and exact target counts were assigned. Draft and segmentation map are preserved in the book's implementation evidence folder.
- All **35 unique RU/EN pairs** in the final effective embedded HTML were read and compared. Essential, Core and Deep were checked as nested argument sequences in both languages. This is an implementation self-check, not a translation certificate.
- Exact cumulative counts, including cover/final: **Essential 16 / Core 27 / Deep 35**. Levels: 16 level-1, 11 level-2, 8 level-3. No previous quota was retained.
- `contentMode: explanatory`; `spoilerPolicy: not-applicable`; defaults RU / dark / Essential. All non-cover screens are attributed to the book and carry checked primary passage references.
- Preserves paradigm, normal science, anomaly, crisis, revolution, incommensurability and progress; actual cases carry the reasoning. The 1969 postscript is identified as part of the enlarged 1970 edition. No universal-relativism claim or innovation-management lesson is added.
- Source identity and selective-reading limits are disclosed in `sources.md` and the bilingual Sources dialog. Main-chapter extract printing is unidentified; chapter XIII uses a separately credited 1996 reserve excerpt. No continuous full-book reading or edition collation is claimed.

## Maintained build and audit

```sh
node skills/book-tiktok/scripts/build_story.mjs \
  collector-output/the-structure-of-scientific-revolutions/story-data.json \
  --out collector-output/the-structure-of-scientific-revolutions/the-structure-of-scientific-revolutions.html

node skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/the-structure-of-scientific-revolutions/the-structure-of-scientific-revolutions.html \
  --min-screens 35 --require-bilingual
```

The audit reports **69 structural checks, zero failures, zero warnings**. It does not establish editorial fidelity. Builder word totals, including screen titles/subtitles: RU 982 / 1,692 / 2,207 and EN 1,164 / 2,001 / 2,620. Computed reading estimates: RU 6 / 10 / 13 minutes; EN 6 / 10 / 12 minutes. Four sources, one original embedded cover. The standalone HTML is 317,280 bytes at this build.

## Real-browser checks

Book-scoped Chrome CDP checks follow the maintained browser protocol, using a file URL with network disabled, no local server, a unique `mktemp -d` profile and `timeout 30` for every browser phase. Each phase terminates its owned process group and removes its profile in cleanup, including failures.

- Full traversal at **320×568, 390×844, 1024×768 and 1440×900**, RU/EN, dark/light, all three depths: 48 matrix cells and 1,248 screen visits. Checks compare actual titles and complete paragraph bodies with authoring data, route order, exact counters, rail breakpoint and horizontal overflow. No horizontal overflow found; longer content remains vertically scrollable.
- Every canonical screen object, source object and `targetModes` matches the effective embedded HTML. Embedded Geist/Geist Mono faces load; the original SVG cover decodes. Zero runtime exceptions, unexplained console errors or HTTP(S) runtime requests during the checks.
- Buttons, keyboard navigation, Chapters and Sources dialogs, depth selection and language/theme position preservation checked. Compact icon-only header checked at 320px with localized labels/tooltips and `href="./"` home contract.
- Text tap and F enter focus; Escape exits; Next preserves focus. Horizontal pointer swipe changes screen without toggling focus; vertical pointer motion does neither. These are programmatic browser pointer checks, not a claim of physical-device gesture testing.
- Save/reload/Continue, Start over, final restart and rail synchronization checked. A remembered Deep screen resumed from Essential raises depth to Deep correctly.
- iPhone browser user-agent emulation: automatic/manual install guide, localization and close behavior checked. Six header icons remain on one row within 320px with a simulated 47px safe-top inset. `navigator.standalone` emulation suppresses guide/trigger. This is **not a physical iPhone/PWA test**.
- Visually inspected screenshots: 390px RU/dark cover, 320px EN/light dense prose and Sources dialog, 1440px RU/dark final with active rail, 320px simulated iPhone safe-area header.

Detailed machine results, screenshots, tool hashes and the book-scoped test script are in [the implementation evidence folder](../../editorial-audit/2026-10-31/books/the-structure-of-scientific-revolutions-sol-implementation-evidence/).

## Handoff limits

Independent review still needs to assess all changed pairs and their primary passages. Publisher-owned root integration, catalogue/home navigation in production, deployed saved progress and real-device behavior are outside this worker's ownership. Settings PR29, shared shell, installed skill, root files, catalogue/index, logs, Git, PRs and deployment were not edited or run by this worker.
