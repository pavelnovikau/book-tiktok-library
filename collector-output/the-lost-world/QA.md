# The Lost World — QA

Post-review integration note (2026-10-31): applied the bilingual factual, chronological, parity and differentiation corrections listed in the source ledger. The maintained library shell restores the bilingual iOS installation guide while retaining the existing spoiler gates and focus behaviour. Counts remain **36 / 90 / 144**; the current deterministic audit reports **7,049 RU / 7,879 EN words**.

Date: 2026-10-31. Original collector result: **PASS**. The later cold-review corrections and maintained library shell were re-audited at integration: **68 passes, 0 warnings, 0 failures**; catalogue browser QA also passed. The detailed per-screen matrix below records the collector run and is not presented as a fresh 10,800-state traversal after the editorial corrections. Russian, dark theme, and Essential remain the fresh-reader defaults.

## Contract and density

| Nested depth | Visible screens | RU words | RU reading estimate | EN words | EN reading estimate |
|---|---:|---:|---:|---:|---:|
| Essential / Главное | 36 | 1,773 | 10 min | 1,953 | 9 min |
| Core / Сюжет | 90 | 4,386 | 25 min | 4,894 | 23 min |
| Deep / Разбор | 144 | 7,036 | 40 min | 7,862 | 36 min |

Counts include the single level-1 cover and final. Level distribution: **36 / 54 / 54**. Essential ⊂ Core ⊂ Deep is a stable-ID subsequence, not three separate stories. Each language has the same IDs, levels, sources, provenance, media, and chapter assignments.

Word counts use the maintained builder's Unicode-word definition and include titles, the cover subtitle, and body copy, including the small authored navigation button. They exclude shell UI, chapter labels, source labels, and bibliography. Reading estimates use 180 RU / 220 EN words per minute, rounded upward; pauses, reflection, and source consultation add time. Deep mean body density: **42.7 RU / 47.1 EN words per screen**. English is about 11.7% longer overall. The deterministic audit omits the three-word cover subtitle, hence its deep totals of **7,033 RU / 7,859 EN**; this is an accounting difference, not missing translation.

Non-cover provenance: 50 `book`, 7 `corroboration`, 86 `synthesis`; the cover is separately typed. Seven numbered sources and one embedded original conceptual illustration. No inherited book corpus, copied translation, external cover, or runtime asset dependency.

## Deterministic audit

Built from clean schema-v2 JSON with the maintained `build_story.mjs`, then applied the book-local shell fixes documented below. Final HTML audit command, from this package directory, with `BOOK_TIKTOK_SKILL` pointing to the installed skill:

```sh
node "$BOOK_TIKTOK_SKILL/scripts/audit_story_html.mjs" the-lost-world.html --min-screens 144 --require-bilingual
```

Current integration audit: **68 passes, 0 warnings, 0 failures**. Verified exact targets, valid source/media references, bilingual fields, unique IDs, shell hooks, offline invariants, and Flexoki identity. Embedded screen corpus was compared against `story-data.json` and is identical. HTML size: **445,441 bytes**. Public deliverables contain no private source filesystem paths.

## Real-browser matrix

Local headless Google Chrome, driven over CDP. Every session used a fresh `mktemp -d` profile, dedicated debugging port, a `timeout 30` limit, and process-group cleanup in `finally`/exit handlers. No development server was started. The shared preview could not open a local `file:` URL (`unsupported-protocol: file:`); local Chrome was used as required by the skill's QA protocol.

Each row traversed all screens in both languages × both themes × all three depths. Every traversed screen was also measured with focus CSS enabled: **5,400 normal visits plus 5,400 focus-layout checks** overall. The focus state itself is additional to the three depth modes.

| Viewport | Language/theme/depth combinations | Screen visits | Horizontal/clipping issues | Reader runtime errors | Result |
|---|---:|---:|---:|---:|---|
| 320x568 | 12 | 1,080 | 0 | 0 | Pass |
| 390x844 | 12 | 1,080 | 0 | 0 | Pass |
| 768x1024 | 12 | 1,080 | 0 | 0 | Pass |
| 1024x768 | 12 | 1,080 | 0 | 0 | Pass |
| 1440x900 | 12 | 1,080 | 0 | 0 | Pass |

All visible titles were nonempty, unique within the mode, and equal to the selected translation. Progress matched the mode count at each step. Checks included document width, scroll-body width, descendant horizontal bounds, topbar bounds, theme-specific heading colour, and the royal-violet action token. Vertical reading scroll is intentional on short screens and long content; it is not treated as unwanted overflow.

Visual inspection covered the cover illustration, dense night-journey prose, battle aftermath, four-question list, two-column provenance comparison, diamond valuation, and final screen. Samples included phone, portrait tablet, landscape tablet, and desktop, plus RU light and EN dark. At 320 px, long lists continue by vertical scrolling. At 1024/1440 px the desktop rail is visible, scrollable, and synchronized; the 1024 cover uses a single-column composition to avoid a cramped two-column layout.

## Interaction and offline results

Passed at each viewport:

- language switching preserves current position, depth and theme; document language/title and UI labels update;
- exact mode filtering and hidden-target navigation automatically raising Essential to Core through the explicit spoiler button;
- Sources and Chapters dialogs open/close, with seven sources and localized method disclosure;
- next/back, keyboard navigation, horizontal pointer swipe, and chapter selection;
- tap focus, second-tap exit, F entry, Escape exit even after Next receives focus, and focus retained during paging;
- header/progress/rail/back/counter hidden in focus; safe-area-aware Next remains inside viewport; cover focus also has Next and hides its mode/action chrome;
- vertical movement is not treated as a tap; interactive elements, long presses, text selection, and open dialogs do not trigger unintended focus/navigation;
- native Chrome mouse input enters focus and native Escape exits it, in addition to programmatic pointer/keyboard tests;
- saved position, Continue, Start over, reload persistence, and final restart;
- fresh RU/dark defaults; embedded Geist and Geist Mono both decode to loaded font faces; the SVG image decodes;
- direct `file:` loading with browser networking disabled and cache disabled: **zero HTTP(S) runtime requests** and zero reader exceptions;
- home icon resolves to the library `index.html` two levels above this collector folder; an actual home click was verified at 320 px. At the eventual flat hosted-library location the link uses `./`, and a flat local-file copy uses `./index.html`. The library must be present beside/above the reader; it is not bundled inside this single-book HTML. Optional source links intentionally need internet when followed.

This is desktop Chrome with emulated viewport sizes, not a claim of physical-device Safari or Android testing.

## Findings fixed locally

1. Give `counter` the focus-mode hiding hook; make Escape safe after a navigation button gains focus.
2. Avoid intercepting native keyboard activation on interactive elements, and tolerate non-element event targets.
3. Make desktop cover columns shrinkable, with a stacked cover at 900–1100 px; allow long continuation labels and source titles to wrap.
4. Resolve the collector-versus-flat-library home location without embedding a private path.
5. Enforce royal violet (`#5B2FC2`) as the single action identity and warm Flexoki backgrounds. Apply explicit token colours to reading elements: rapid theme switching had exposed stale inherited text colours. The final traversal asserts the expected light/dark heading colour on every screen.
6. Hide cover controls in focus while retaining Next. Remove unrelated install-guide markup from this standalone collector package.

These are modifications to this HTML only. Shared templates and scripts were not edited. Rebuilding the HTML directly from the maintained builder requires reapplying these local hardening changes; keep the finalized HTML as the delivery artifact.

## Narrative and evidence review

Full source: lawful, unabridged Project Gutenberg #139, all sixteen chapters. Research method and per-chapter ledger are recorded in `sources.md`: full-book structural survey plus targeted close reading, not a claim of equal line-by-line scrutiny. Bibliography: Gutenberg catalogue and CiNii. Literary context: Portsmouth Conan Doyle Collection. Bounded scientific corrections: Natural History Museum, Smithsonian Human Origins, AABA.

Essential is substantially spoiler-light: it does not reveal the bridge sabotage, escape mechanism, live London demonstration, Gladys's marriage, diamond reward, or final travel choice. Core gives the complete causal arc, including sabotage and the public demonstration; Deep supplies backstory, mechanisms, alternative readings and limits. All level-2/3 screens visibly say **Спойлеры / Spoilers**.

The fictional expedition is never represented as corroborated history. Creature identifications remain qualified where the novel is uncertain; the London pterosaur's final fate is not asserted as known. The racial portrait of Zambo, ethnic explanation of Gomez, cranial hierarchy, conquest rhetoric, and ownership assumptions are examined rather than silently modernized. The killing of all male ape-men and enslavement of females and young remain explicit without graphic detail. Modern corrections are not attributed to Doyle; interpretations are not presented as proved authorial intent.

## Delivery and cleanup

Only these files belong to the package:

- `the-lost-world.html` — self-contained reader;
- `story-data.json` — clean authoring corpus;
- `sources.md` — source ledger, claim map, rights and evidence boundary;
- `QA.md` — this report.

No publication, catalogue integration, commit, or push was performed. All Chrome processes/profile directories and temporary QA scripts, JSON reports and screenshots created by this task were removed after inspection. Other sessions' browser processes were not touched.

Final artifact checksums (QA report excluded to avoid a self-referential hash):

- `the-lost-world.html` — SHA-256 `27415172023476ddad856cd25164cca900fc18280e6bc3d073a0d9a5e6ac7906`
- `story-data.json` — SHA-256 `0d84ba33ee688c255d681f9bde1dd26d2fd53e45408a3dc19cea1a44be107104`
- `sources.md` — SHA-256 `fa66350f67e27d8610d6eb9852a06e52b52614ab7433454e956f7403ede122d3`
