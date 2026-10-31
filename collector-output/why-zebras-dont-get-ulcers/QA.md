# QA — Why Zebras Don't Get Ulcers

Date: 2026-10-31. Status: **PASS**, with evidence boundaries and shell limitations below. All work is isolated on branch `collector/why-zebras-dont-get-ulcers` in this local clone of the library. No shared catalogue, existing book, deployment or outside log was edited.

## Exact delivery contract

- Schema: v2; default language **RU**, complete **EN** parity; default dark / Deep.
- Cumulative modes (including cover and final): **Essential 36 / Core 90 / Deep 144**.
- Level increments: **36 / 54 / 54**. Every mode retains the same order; Essential is a strict subset of Core, itself a strict subset of Deep.
- **144 unique IDs and 144 unique titles in each language**. All 144 screens, including cover and final, have provenance: **124 book / 12 corroboration / 8 synthesis**. The cover has an explicit bilingual visible Synthesis label because the maintained shell does not render its ordinary source badge.
- **13 sources**: supplied EPUB plus 12 primary/authoritative records, including one explicitly author-linked baboon paper. Chapter locators and screen-to-source index are in sources.md; bookLocation fields retain local chapter references.
- **0 images**: deliberately typographic maintained cover, not a missing asset. Geist and Geist Mono are embedded. **453,377 bytes**; no runtime network dependency.
- Builder reading estimates, RU: **11 / 26 / 41 minutes**; EN: **10 / 23 / 37 minutes**. Estimates use 180 RU / 220 EN words per minute and are not timed reader studies.
- Builder title/subtitle/body word totals, RU: **1,846 / 4,541 / 7,225**; EN: **2,036 / 5,014 / 8,032**.
- Body-only density: RU **6,296 words**, mean **43.72**, median **44**, range **37–52**; EN **6,949 words**, mean **48.26**, median **48**, range **41–60**. Counts use Unicode words with internal apostrophes/hyphens; audit totals below differ slightly because they exclude cover subtitle metadata.

## Maintained build and deterministic audit

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs story-data.json --out why-zebras-dont-get-ulcers.html
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs why-zebras-dont-get-ulcers.html --min-screens 144 --require-bilingual
```

Final audit output (absolute file path as executed):

```json
{
  "file": "/Users/pn/.t3/worktrees/smartcat/t3-96c8e01e/_artifacts/book-tiktok-library/collector-output/why-zebras-dont-get-ulcers/why-zebras-dont-get-ulcers.html",
  "format": "v2",
  "bytes": 453377,
  "screenCount": 144,
  "levels": {
    "1": 36,
    "2": 54,
    "3": 54
  },
  "modes": {
    "essential": 36,
    "core": 90,
    "deep": 144
  },
  "words": {
    "ru": 7221,
    "en": 8026
  },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

The shell was generated from the skill's maintained standalone template, not copied from another book. No generated-HTML patch was used. The source data is the editable canonical deliverable; it rebuilds with the maintained builder.

## Real-browser QA

Used local Google Chrome through Playwright, loading **file://** directly, with HTTP(S) requests blocked and logged. No server or collaborative preview was started. Each run used `timeout 30`, its own `mktemp -d` profile, a browser-context close in finally, targeted process cleanup and profile removal. Temporary QA scripts, images and profiles were removed after inspection.

Each viewport traversed every screen of every mode in both languages and both themes: `(36 + 90 + 144) × 2 × 2 = 1,080` screen visits; **4,320 visits** across the final four-viewport matrix. Additional focused interaction checks/revisits are not included in that matrix total.

| Viewport | Matrix visits | Aggregate checks | Failures | JS/console errors | HTTP(S) requests |
|---|---:|---:|---:|---:|---:|
| 320×568 | 1080 | 34 | 0 | 0 | 0 |
| 390×844 | 1080 | 34 | 0 | 0 | 0 |
| 1024×768 | 1080 | 35 | 0 | 0 | 0 |
| 1440×900 | 1080 | 35 | 0 | 0 | 0 |

For each visit checked rendered title, expected counter, active chapter ID, visible provenance, document/body horizontal bounds and slide horizontal overflow. Verified final restart in every language/theme/mode combination. Verified all four top controls remain inside the viewport at 320 px; desktop rail is visible at 1024/1440 and its active item follows navigation. Inspected captured rail positions after browser rendering.

Focused checks at 390×844: next/back behavior through matrix traversal; ArrowRight/ArrowLeft, PageDown/PageUp and Space; language/theme changes preserve current screen; language/theme/mode survive reload; saved Continue, Start over, and automatic raising of depth when resuming a saved hidden screen; synthetic horizontal pointer swipe advances, vertical pointer motion does not. Long final-screen text can be scrolled to the bottom. Both dialogs open/close and the sources dialog renders all 13 entries. Embedded fonts report ready. No content images require decoding.

Visual inspection: actual Chrome renders of cover at 320, 390, 1024 and 1440; dark and light cover examples; dense numerical evidence, four-item list, two-column/stacked comparison, provenance line and final screen. Captures initially caught the beginning of a CSS entrance animation; recaptured with finite animations disabled for stable inspection. This was capture timing, not missing content. No artifact changes were needed for that capture issue.

## Content and parity review

- Claim map and source ledger were written before screens. All 18 chapter structures and selected mechanisms/examples/qualifications were consulted in the exact supplied unpacked EPUB.
- Bodies are original paraphrases, with **no quotations**, copied chapters or distributed source EPUB. No fabricated print pages, image credits or English-edition reading claim.
- Shared screen ID, depth, provenance and sources guarantee structural RU/EN parity; quantities and causal qualifications were reviewed in paired authoring. No Cyrillic leakage in English copy. EN word totals are somewhat longer because of language structure, not extra claims.
- Preserved acute benefit versus chronic cost; HPA timing/feedback/receptors; organ-specific mechanisms; acute versus prolonged immune changes; reverse causation in human studies; hormone/genetics history; heterogeneous aging; reproductive resilience; no blame for pregnancy outcomes, cancer or depression.
- Added selective checks on ulcer etiology, human coronary associations, glucocorticoid resistance, cancer evidence, insulin resistance, Cushing syndrome, hippocampal causal direction, historical candidate genes, depression care, meditation safety and workplace interventions.
- Health caveats are visible on the cover, in Sources/Method and in treatment-sensitive screens. No diagnosis, doses, treatment changes, cure promises or automatic stress–disease causation.

## Known limitations and evidence boundaries

1. This is a selective analytical reading of the supplied Russian EPUB, not an exhaustive line-by-line verification of every chapter and every cited study. The full English edition was not consulted; English translates this digest.
2. File publication metadata is 2021; it does not make book-era science current. External checks are selective safeguards, **not a systematic review through 2026**. Source access date does not mean source publication date.
3. Source 1's HTTP URL identifies the matching publisher edition; the actual book evidence came from the private local EPUB. It is not a public full-text link. The directory fingerprint and chapter paths are recorded in sources.md.
4. Observational human associations do not establish individual causation. Animal mechanisms are labeled and bounded. The baboon-culture paper is by the book's author and is not independent replication.
5. Small phones intentionally use vertical slide scrolling; cover content, its Start control and long final/comparison text may extend below the first viewport. Top transparency controls and reading navigation remain accessible. The maintained chapter picker lists screens visible in the chosen mode; deeper material is exposed by selecting a deeper mode, while a saved hidden ID automatically raises depth on Continue.
6. Pointer checks used browser-dispatched pointer events, not a physical touch device. No screen-reader or external medical-specialist review was performed. Browser traversal and deterministic checks do not substitute for either.
7. The skill shell has no catalogue Home control; this collector artifact is deliberately standalone and unregistered. Integrating catalogue navigation is outside this isolated collector task.
8. No deployment, push, PR, catalogue update or external delivery occurred. Only the four requested files are committed under this slug.

## Artifact integrity

HTML SHA-256: `e8e4589a61d287dbe1689df67934870d4c62549838bac4ee4fe65a4ac3ccb601`.

Final commit SHA is reported in the collector handoff rather than embedded here, avoiding a self-referential commit hash.
