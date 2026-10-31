# Zen and the Art of Motorcycle Maintenance — post-review verification

2026-10-31. Independent cold review: READY WITH FIXES; parent implemented every localized finding and rebuilt on the maintained template. This is repair/implementation verification, not a second independent editorial review.

## Closed findings

Source 3’s globally visible note no longer discloses the later biographical event. The explicit event remains on Deep-only `later-biography`. Cover and `reading-contract` now say that Core reveals Phaedrus’s identity, while Deep reveals the ending and later biography. The reader is a philosophical novel analysis, not a meditation manual. The documented selective use of the complete local Russian EPUB is preserved without claiming a new full read.

Exact nested **36 / 90 / 144**; 9 sources. Stable paired RU/EN IDs, levels and references. No new source-access claim, private file, artwork or copied chapter. Source ledger records the content changes. Reading estimates remain approximate and exclude reflection.

## Current validation

- Deterministic audit: **68 passes, zero warnings/failures**.
- Real Chrome/CDP file:// matrix, 320×568, 390×844, 1024×768, 1440×900; `(36+90+144) × 2 languages × 2 themes × 4 viewports` = **4,320 screen visits**. Rendered heading/count, document and slide/cover bounds checked on every visit. Both embedded fonts loaded; zero runtime/console exceptions and zero HTTP(S) requests.
- Native Space activated focused Chapters and Sources without paging. Dialogs/source count, paging keys, cover focus, hidden Start/depth controls/counter, safe Next, F/Escape after focused Next and second-tap exit passed at every viewport. Ordinary-iOS guide discovery, persisted-focus suppression and standalone suppression passed under emulation.
- Maintained shell uses quiet cyan, the intermediate-desktop cover correction and existing library metadata. Whole-library QA passed all 24 readers, including cover containment at 900/960px, native keyboard activation, counters/filters/semantic covers, focus and iOS states, zero runtime errors.
- Representative mobile and desktop captures were inspected. Long screens scroll vertically; no physical Safari or screen-reader test is claimed. Each manually launched browser used timeout 30, an isolated temporary profile/port and finally cleanup of its owned process group/profile.

Collector HTML SHA-256: `bd40df59521f5927d0f1701244207772b89fb970cf630aebc80a867b8cd30e07`.

The historical collector report below is retained as original research/implementation history. Its earlier shell/color measurements and fingerprints are superseded by this report. Original full-book access and prior checks remain collector-reported within their stated limits.

---

# QA — Zen and the Art of Motorcycle Maintenance

2026-10-31. Final status: PASS with the evidence and test boundaries below. Exactly four deliverables are present in this collector folder. No catalogue, root runtime, shared script/template, LOG.md, deployment, push or commit was changed or performed.

## Contract and density

- Schema v2, maintained builder and maintained shell; original structured data, no borrowed book HTML.
- Exact cumulative counts, cover/final included: **Essential 36 / Core 90 / Deep 144**. Level increments: **36 / 54 / 54**.
- Default: **RU / dark / Essential**. English is a complete translation of this digest, not a claim that a full English edition was consulted.
- **144 unique IDs and 144 unique titles in each language.** Provenance: **108 book / 5 corroboration / 31 synthesis**. Cover’s synthesis label is explicit because ordinary source badges are not rendered on the maintained cover.
- **9 source entries:** one complete private local EPUB and eight external records. Source 1’s URL is explicitly only public orientation, not a full-text or edition link; it shares that orientation URL with source 7.
- **0 images**, deliberately typographic; no publisher cover or EPUB art. Embedded Geist and Geist Mono. Final HTML: **448,008 bytes**, with no runtime network dependency.
- Builder title/subtitle/body totals: RU **1,913 / 4,786 / 7,677**; EN **2,234 / 5,603 / 8,982** for Essential/Core/Deep.
- Body-only totals: RU **6,789**, mean **47.15**, median **47**, range **41–53**; EN **7,859**, mean **54.58**, median **55**, range **50–60** words. All 144 bodies meet the ordinary 35–75 word band.
- Builder reading estimates: RU **11 / 27 / 43 minutes**; EN **11 / 26 / 41 minutes**. These use the builder’s word rates, not timed reader studies.

## Deterministic audit

Executed with the maintained tool and exact requested flags:

```sh
node "$CODEX_SKILLS/book-tiktok/scripts/build_story.mjs" story-data.json --out zen-and-the-art-of-motorcycle-maintenance.html
node "$CODEX_SKILLS/book-tiktok/scripts/audit_story_html.mjs" zen-and-the-art-of-motorcycle-maintenance.html --min-screens 144 --require-bilingual
```

Final result:

```json
{
  "format": "v2",
  "bytes": 448008,
  "screenCount": 144,
  "levels": { "1": 36, "2": 54, "3": 54 },
  "modes": { "essential": 36, "core": 90, "deep": 144 },
  "words": { "ru": 7672, "en": 8975 },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

Audit word counts omit cover subtitle metadata and therefore differ slightly from builder totals. No generated-HTML patch was applied; rebuilding from story-data.json reproduces the audited story.

## Evidence boundary

The complete Russian EPUB was found in the maintainer’s existing Apple Books/iCloud personal library, inspected and consulted read-only. Translation credited to **М. Немцов**. Electronic identity: FB2 document UUID **25a2e2f2-4c07-41e2-8662-55c0b0139c04**, version 1, document creation **2009-08-02**, FB2EPUB converter **1.0.28.0**. This identifies the conversion; **publisher, ISBN, print-edition year and authorized provenance of this old personal conversion are not established by its metadata**. No DRM bypass or web full-text acquisition occurred.

Four parts, all 32 numbered chapters, author’s note, translator’s essay and notes are present. Later authorial afterword not identified. A few chapter-32 sentences show conversion damage. No original text is redistributed or repaired into the digest.

Actual reading: all chapter boundaries and structure inspected; opening/middle/ending passages selectively consulted; targeted sections checked for the principal argument and examples; chapters **27 and 32** read in full and chapter **31** resolution consulted directly. This is an analytical, selective close consultation of a complete local text, **not line-by-line reading of the entire work**. The exact boundary is visible in the reader’s method/source notes as well as sources.md. There are no fabricated page references or hidden private workstation paths.

## Content, spoilers and duplication review

The claim map preceded screen writing and is recorded in sources.md. Every screen was reviewed in paired RU/EN authoring and again through its cognitive job in the complete sequence. The Essential route remains coherent on its own: participation → classical/romantic split → limits of method → Quality → practical care → institutional and relational costs → qualified mental model. Core inserts the intellectual architecture, pedagogy and Phaedrus’s identity. Deep adds finer mechanisms, historical checks and the full ending.

Essential preserves discovery of the identity resolution, glass door and final ride. Core can reveal conceptual identity without telling the full resolution. A visible spoiler notice is present on the cover, and screen 133 gives a dedicated bilingual warning before screens 134–141 disclose the ending and later biography. The later death of Chris is clearly separated from the novel’s trip and from an authorial afterword not consulted locally.

The road trip, Chautauquas, classical/romantic division, Quality, Phaedrus, Bozeman, writing classes, university conflict, DeWeeses, mountain ascent/descent, Poincaré, stuck screw, gumption and father–son arc all retain distinct roles. The work is presented as a philosophical novel with an unreliable/reconstructive dimension, not a Zen manual or generic self-help programme. The narrator’s reservation about identifying Quality and Tao is explicit. Classroom recognition is not promoted to a scientific proof of ontology; psychiatric crisis neither proves nor refutes an idea. Later Lila concepts are bounded as sequel context.

Duplication review differentiated the closest recurring ideas: question versus classroom evidence (60/70), changed understanding versus artistic responsiveness (22/57), conceptual former self versus ending integration (47/138), attention to work versus decoration (103/104). One overlapping grading screen was replaced with the concrete case of the successful student opposing grades (67), and one general atmosphere screen with the distinct conceptual-ghosts/gravitation argument (28). These replacements add book-specific evidence rather than quota padding. No pair of English screens exceeds **0.16** token-set Jaccard similarity after common stopword removal; this is a supporting lexical check, not a semantic proof.

An eight-consecutive-word overlap check against the local Russian book’s sections found **0 body overlaps**. No quotations or copied source passages are included. No Cyrillic was found in English body/title copy. Identical stable IDs, levels, provenance and source references underlie both languages; names, dates, numerical claims and causal qualifications were reviewed together.

## Real-browser matrix

Local Google Chrome via native CDP, loading the standalone **file://** artifact. No preview, server, Vite or HMR process. Each browser used **timeout 30**, a unique temporary profile and dedicated dynamically allocated debugging port. Cleanup terminated only that run’s detached process group and removed its profile in finally, including on error.

Each viewport traversed `(36 + 90 + 144) × 2 languages × 2 themes = 1,080` screen visits. Final sequential runs:

| Viewport | Visits | Layout/title/count/provenance failures | JS/console errors | HTTP(S) requests |
|---|---:|---:|---:|---:|
| 320×568 | 1,080 | 0 | 0 | 0 |
| 390×844 | 1,080 | 0 | 0 | 0 |
| 1024×768 | 1,080 | 0 | 0 | 0 |
| 1440×900 | 1,080 | 0 | 0 | 0 |

**4,320 final matrix visits.** Every visit checked rendered title, mode counter, active rail ID, provenance on non-cover screens, document/body bounds and horizontal slide overflow. Final restart checked in every language/theme/mode combination. Both embedded fonts reported loaded. No image decoding is needed.

Focused interaction checks passed at every viewport: Chapters and Sources dialogs open/close, nine source entries render, five top controls remain in bounds, Next/back, ArrowRight/ArrowLeft, PageDown/PageUp/Space, horizontal pointer swipe, vertical pointer motion not treated as a page gesture or focus tap, language/theme position preservation, saved Continue after reload, Start over, automatic depth raising when continuing a saved hidden screen. Focus mode activates by tap and F, survives paging, hides header/back/rail, keeps Next inside safe viewport bounds, and exits by Escape or tap. Desktop rail is visible and scrollable at 1024/1440, hidden on phones, and the active final item is visible after rendering.

An exploratory parallel-browser run produced one transient Escape-focus assertion failure at 390×844. The isolated rerun and the complete final sequential four-viewport matrix passed; no artifact change was needed for that transient.

Actual Chrome screenshots were visually inspected: cover at all four sizes; 320/1024 comparison in light; 390 three-step notebook and provenance in dark; 390 explicit spoiler warning in English/dark; 1440 final in Russian/light. Typography, wrapping, comparison stacking, vertical scroll areas and fixed navigation remained usable. Image and quantitative-screen checks are not applicable: this collector contains neither content imagery nor an invented quantitative evidence panel. Temporary captures and QA harness were removed after inspection.

## Practical limits

- Short phones intentionally scroll the cover and longer screens vertically; content is not promised to fit above the fold. Header transparency controls and reading navigation stay accessible.
- The maintained chapter picker lists the selected mode’s visible screens. Choosing a deeper mode exposes deeper chapters; Continue can raise mode for a saved hidden ID.
- Pointer tests use dispatched browser events rather than a physical touch device. No screen-reader, clinical, archival-history or external scholarly peer review was performed.
- External corroboration is selective: museum artifacts, the author’s archival voice, Poincaré, Plato, a scholarly reference and modern reception. It does not independently validate every scene or the entire metaphysics.
- Final output is local and unregistered. No deployment, upload, push, commit or outside message was sent.

## Complete per-screen density register

All bodies were reviewed for a distinct contribution; title/source/position/overflow checks traversed each in both languages, themes and every applicable mode. The counts below are body-only.

| # | Stable ID | Level | Provenance | RU / EN words |
|---:|---|---:|---|---:|
| 1 | `cover` | 1 | synthesis | 48 / 58 |
| 2 | `reading-contract` | 1 | synthesis | 45 / 50 |
| 3 | `genre-boundary` | 2 | book | 44 / 50 |
| 4 | `trip-context` | 3 | corroboration | 43 / 52 |
| 5 | `inside-landscape` | 1 | book | 45 / 53 |
| 6 | `secondary-roads` | 2 | book | 45 / 53 |
| 7 | `weather-resistance` | 3 | book | 45 / 52 |
| 8 | `chautauqua` | 1 | book | 44 / 54 |
| 9 | `two-tempos` | 2 | synthesis | 45 / 54 |
| 10 | `reader-position` | 3 | synthesis | 44 / 54 |
| 11 | `maintenance-disagreement` | 1 | book | 45 / 53 |
| 12 | `technology-hostility` | 2 | book | 47 / 54 |
| 13 | `delegation-limit` | 3 | synthesis | 44 / 53 |
| 14 | `classical-romantic` | 1 | book | 41 / 52 |
| 15 | `not-personality-test` | 2 | synthesis | 44 / 55 |
| 16 | `diagram-meaning` | 3 | book | 44 / 54 |
| 17 | `beer-can-shim` | 2 | book | 47 / 56 |
| 18 | `material-brand` | 3 | synthesis | 46 / 54 |
| 19 | `care-before-skill` | 1 | book | 49 / 54 |
| 20 | `careless-shop` | 2 | book | 45 / 53 |
| 21 | `anticipatory-care` | 3 | book | 48 / 55 |
| 22 | `machine-changing` | 2 | book | 46 / 54 |
| 23 | `technology-participation` | 1 | book | 49 / 52 |
| 24 | `scale-limit` | 3 | synthesis | 49 / 53 |
| 25 | `ghost-enters` | 1 | book | 47 / 55 |
| 26 | `chris-present` | 1 | book | 48 / 55 |
| 27 | `fatigue-judgment` | 2 | book | 47 / 52 |
| 28 | `conceptual-ghosts` | 3 | book | 48 / 58 |
| 29 | `reason-inheritance` | 1 | book | 46 / 53 |
| 30 | `method-disciplines` | 2 | book | 44 / 53 |
| 31 | `diagnostic-notebook` | 2 | book | 46 / 55 |
| 32 | `deduction-induction` | 3 | book | 50 / 54 |
| 33 | `empty-tank` | 2 | book | 47 / 54 |
| 34 | `test-the-test` | 3 | book | 44 / 55 |
| 35 | `hypothesis-abundance` | 1 | book | 44 / 50 |
| 36 | `relevance-question` | 2 | synthesis | 47 / 55 |
| 37 | `young-scientist` | 2 | book | 46 / 53 |
| 38 | `valued-observation` | 3 | synthesis | 47 / 56 |
| 39 | `hume-kant` | 2 | book | 47 / 55 |
| 40 | `a-priori` | 3 | book | 46 / 56 |
| 41 | `einstein-motive` | 3 | book | 46 / 55 |
| 42 | `india-disappointment` | 3 | book | 48 / 55 |
| 43 | `zen-boundary` | 1 | book | 46 / 54 |
| 44 | `mountain-setting` | 2 | book | 48 / 56 |
| 45 | `bozeman-return` | 1 | book | 46 / 53 |
| 46 | `archaeology-memory` | 2 | book | 48 / 52 |
| 47 | `phaedrus-former-self` | 2 | book | 45 / 56 |
| 48 | `reconstruction-limit` | 2 | synthesis | 49 / 55 |
| 49 | `campus-recognition` | 2 | book | 48 / 53 |
| 50 | `church-reason` | 1 | book | 45 / 54 |
| 51 | `purpose-shell` | 2 | synthesis | 50 / 54 |
| 52 | `accreditation` | 3 | book | 47 / 57 |
| 53 | `funding-truth` | 2 | book | 48 / 54 |
| 54 | `radical-teacher` | 3 | book | 49 / 53 |
| 55 | `deweese-bridge` | 1 | book | 47 / 53 |
| 56 | `barbecue-instructions` | 2 | book | 47 / 54 |
| 57 | `assembly-art` | 2 | book | 45 / 56 |
| 58 | `peace-condition` | 3 | book | 46 / 56 |
| 59 | `instructions-limit` | 3 | synthesis | 49 / 55 |
| 60 | `quality-question` | 1 | book | 48 / 55 |
| 61 | `definition-trap` | 2 | book | 47 / 55 |
| 62 | `grading-problem` | 2 | book | 48 / 53 |
| 63 | `one-brick` | 1 | book | 47 / 55 |
| 64 | `coin-exercise` | 3 | book | 47 / 54 |
| 65 | `imitation` | 2 | book | 47 / 57 |
| 66 | `withheld-grades` | 2 | book | 45 / 56 |
| 67 | `successful-student-dissent` | 2 | book | 53 / 57 |
| 68 | `intrinsic-purpose` | 2 | book | 48 / 53 |
| 69 | `working-student` | 3 | book | 49 / 56 |
| 70 | `shared-recognition` | 1 | book | 44 / 53 |
| 71 | `consensus-limit` | 3 | synthesis | 47 / 54 |
| 72 | `rhetoric-practice` | 2 | book | 47 / 53 |
| 73 | `quality-removal` | 1 | book | 45 / 51 |
| 74 | `elimination-method` | 3 | synthesis | 47 / 55 |
| 75 | `utility-ground` | 3 | synthesis | 50 / 53 |
| 76 | `beyond-aesthetics` | 2 | book | 47 / 54 |
| 77 | `subject-object-dilemma` | 1 | book | 47 / 54 |
| 78 | `qualities-ambiguity` | 3 | book | 49 / 56 |
| 79 | `third-entity` | 2 | book | 48 / 54 |
| 80 | `quality-before-division` | 1 | book | 45 / 53 |
| 81 | `quality-event` | 2 | book | 48 / 56 |
| 82 | `present-past` | 3 | book | 49 / 55 |
| 83 | `experience-analogy` | 2 | book | 47 / 56 |
| 84 | `disagreement-test` | 3 | book | 50 / 53 |
| 85 | `objectivity-concern` | 3 | synthesis | 48 / 53 |
| 86 | `quality-tao` | 2 | book | 46 / 55 |
| 87 | `narrator-reservation` | 1 | book | 48 / 57 |
| 88 | `mountain-care` | 1 | book | 48 / 55 |
| 89 | `unequal-load` | 2 | book | 48 / 53 |
| 90 | `turning-back` | 2 | book | 44 / 56 |
| 91 | `courage-forms` | 3 | synthesis | 46 / 54 |
| 92 | `summit-metaphor` | 3 | synthesis | 47 / 53 |
| 93 | `poincare-selection` | 1 | book | 49 / 51 |
| 94 | `geometry-convention` | 2 | book | 49 / 53 |
| 95 | `classical-beauty` | 2 | book | 47 / 53 |
| 96 | `narrator-research` | 2 | book | 49 / 57 |
| 97 | `poincare-primary-check` | 3 | corroboration | 49 / 55 |
| 98 | `stripped-screw` | 1 | book | 47 / 56 |
| 99 | `stuckness-opening` | 2 | book | 46 / 53 |
| 100 | `screw-value` | 3 | synthesis | 49 / 55 |
| 101 | `cultivated-feel` | 2 | book | 48 / 57 |
| 102 | `force-feedback` | 3 | synthesis | 50 / 55 |
| 103 | `art-relationship` | 1 | book | 47 / 57 |
| 104 | `decoration-limit` | 2 | book | 49 / 56 |
| 105 | `inner-outer` | 2 | book | 46 / 53 |
| 106 | `ritual-boundary` | 3 | synthesis | 47 / 57 |
| 107 | `gumption-fuel` | 1 | book | 49 / 56 |
| 108 | `setbacks-hangups` | 2 | book | 53 / 59 |
| 109 | `assembly-sequence` | 3 | book | 45 / 53 |
| 110 | `intermittent-fault` | 3 | book | 47 / 55 |
| 111 | `parts-setback` | 3 | book | 49 / 53 |
| 112 | `value-rigidity` | 1 | book | 45 / 56 |
| 113 | `monkey-trap` | 2 | book | 47 / 57 |
| 114 | `ego-trap` | 2 | book | 48 / 57 |
| 115 | `anxiety-trap` | 3 | book | 45 / 54 |
| 116 | `boredom-trap` | 3 | book | 50 / 55 |
| 117 | `impatience-trap` | 2 | book | 48 / 58 |
| 118 | `mu-question` | 1 | book | 47 / 53 |
| 119 | `mu-diagnostic` | 3 | synthesis | 50 / 57 |
| 120 | `muscle-traps` | 3 | book | 48 / 56 |
| 121 | `work-environment` | 3 | synthesis | 46 / 54 |
| 122 | `gumption-no-guarantee` | 1 | synthesis | 47 / 56 |
| 123 | `chicago-conflict` | 1 | book | 50 / 55 |
| 124 | `rhetoric-dialectic` | 2 | book | 47 / 60 |
| 125 | `seminar-power` | 3 | book | 47 / 58 |
| 126 | `greek-genealogy` | 1 | book | 47 / 54 |
| 127 | `arete` | 2 | book | 46 / 54 |
| 128 | `plato-primary-check` | 3 | corroboration | 49 / 52 |
| 129 | `history-boundary` | 2 | synthesis | 49 / 57 |
| 130 | `argument-cost` | 1 | book | 48 / 55 |
| 131 | `mythos` | 3 | book | 50 / 54 |
| 132 | `sanity-truth` | 1 | synthesis | 49 / 55 |
| 133 | `ending-warning` | 3 | synthesis | 48 / 55 |
| 134 | `shadow-face` | 3 | book | 47 / 56 |
| 135 | `chris-misses-father` | 3 | book | 46 / 56 |
| 136 | `planned-separation` | 3 | book | 48 / 57 |
| 137 | `hospital-door` | 3 | book | 51 / 56 |
| 138 | `identity-return` | 3 | book | 46 / 57 |
| 139 | `view-over-shoulder` | 3 | book | 48 / 56 |
| 140 | `hope-not-proof` | 3 | synthesis | 47 / 55 |
| 141 | `later-biography` | 3 | corroboration | 49 / 56 |
| 142 | `lila-boundary` | 2 | corroboration | 49 / 55 |
| 143 | `beyond-craft-recipe` | 2 | synthesis | 48 / 56 |
| 144 | `final` | 1 | synthesis | 47 / 50 |

HTML SHA-256: `067fb0652611c66878684e82803cabe8f882d80a22bc31e348628df6e8c66145`.
