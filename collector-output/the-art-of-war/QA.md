# QA — Sunzi, The Art of War

Post-review integration note (2026-10-31): restored Giles’s stated consequences for recklessness and cowardice; corrected II.15 to enemy provisions obtained in enemy territory; separated manuscript copying from burial dating with a tenth source; removed the unsupported emotional-contagion mechanism; and placed the military deception principle in Essential with an explicit non-transfer boundary. The maintained library shell restores the bilingual iOS installation guide and hides the actual counter in focus mode. Counts remain **22 / 46 / 70**; the current deterministic audit reports **4,557 RU / 5,159 EN words**.

Date: 2026-10-31. Original collector result: **PASS**. The later cold-review corrections and maintained library shell were re-audited at integration: **68 passes, 0 warnings, 0 failures**; catalogue browser QA also passed. The detailed matrix below records the collector run and is not presented as a fresh 2,208-screen traversal after the editorial corrections. Russian, dark and Deep remain the defaults. One portable HTML contains fonts, CSS, JavaScript and corpus with no runtime dependency or publisher art.

## Exact counts and density

Counts are cumulative and include the level-1 cover and final. Essential ⊂ Core ⊂ Deep. Raw levels: **22 / 24 / 24**.

| Mode | Screens | RU reading words | EN reading words | Estimated RU / EN minutes |
|---|---:|---:|---:|---:|
| Essential | 22 | 1,402 | 1,614 | 8 / 8 |
| Core | 46 | 2,963 | 3,377 | 17 / 16 |
| Deep | 70 | 4,541 | 5,132 | 26 / 24 |

Reading-word totals use the maintained builder's definition: title + subtitle + body, with HTML removed. Section labels, source notes, method disclosure, and interface chrome are excluded. The deterministic auditor excludes the cover subtitle, so its independently reported totals are **4,532 RU / 5,123 EN**; the nine-word subtitle in each language explains the difference. Body-only totals: **4,163 RU / 4,636 EN**. Mean body density across all 70 screens: **59.5 RU / 66.2 EN words**. Across the 69 non-cover screens: approximately **59.9 / 66.6**. Every ordinary non-cover screen has at least 35 body words; the longest English list/evidence screen reaches 77. English reading copy is about 13% longer, with no missing arguments or qualifications in either language.

Numerals in every paired RU/EN body were compared programmatically: **zero mismatches**. Titles are unique per language. Shared stable IDs, levels, sources, provenance, and cognitive jobs live outside translated copy.

## Provenance distribution

| Mode | Cover | Book argument | Corroboration | Synthesis |
|---|---:|---:|---:|---:|
| Essential | 1 | 17 | 0 | 4 |
| Core | 1 | 35 | 3 | 7 |
| Deep | 1 | 49 | 7 | 13 |

**10 sources**, all referenced. Provenance labels describe whose argument is being reported, not an accuracy score. The cover is framing; the final is synthesis. All factual/book screens have source IDs. Exact chapter/paragraph or source-section locators are preserved in JSON and in `sources.md`.

## Fidelity and evidence boundary

All thirteen chapters appear in original order, with the main movement preserved: assessment → expenditure → intact outcomes → security → collective configuration → relative advantage → friction → variation → observation → terrain and responsibility → human situations → irreversible loss → human intelligence. Essential remains a complete argument and reaches every chapter; Core and Deep insert explanation rather than replace that argument.

The primary reading base is the complete public-domain Giles 1910 base text, Project Gutenberg #17405. Selected notes in #132 are separately attributed. Modern context uses the open Bowdoin apparatus, Morillo's abstract, Columbia's description and contents of Mair, Boorman's public chapter summary, the opening pages of Lorge's official excerpt, and Lewis's public historical chapter summary. The paywalled modern works were **not** read in full. A broken publisher appendix link was excluded. No local Smart Reading file was used or represented as a full book. The ledger records direct URLs, access date, scope, claim map, caveats, and 70 screen locators.

Textual assertions are not empirical validation. Authorship, exact composition date, and the traditional Sun Wu biography remain uncertain. The manuscript is a fragmentary early witness, not an autograph. Mair's dating and non-historicity positions are attributed hypotheses. The chapter IV defense/attack variant and VIII's problematic nine-part heading are visible. Later commentary, translator decisions, and modern organizational examples are marked and separated. Numerical ratios remain textual illustrations, with no fabricated modern conversions. Coercion, internal secrecy, and instrumental treatment of people remain present. Incendiary warfare and intelligence retain their architectural roles without executable procedures. No quotation collage, direct prose quotations, fabricated pages, or publisher cover appears.

## Build and deterministic audit

Built with the maintained skill builder, never copied from another book:

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs story-data.json --out the-art-of-war.html
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs the-art-of-war.html --min-screens 70 --require-bilingual
```

Final audit: **68 passes, 0 warnings, 0 failures**. Schema v2; exact targets 22/46/70; 70 unique IDs; complete bilingual copy; valid sources/provenance; correct metadata; offline invariants; responsive shell; Flexoki identity; no unreachable legacy corpus.

One local presentation fix follows the builder output: explicit token-based text colors avoid stale inherited light/dark colors in nested reading content after rapid switching in Chrome 155. No shared template or skill file was changed. If rebuilding, preserve this rule immediately before `</style>`:

```css
/* Collector-local explicit text colors keep rapid theme changes stable in nested content. */
#story .slide-scroll,
#story .cover-copy h1,
#story .cover-copy > p:not(.kicker):not(.cover-subtitle),
#story .compare-item strong,
#story .compare-item p,
#story .story-list strong,
#story .fact p { color: var(--color-text); }
```

Current integrated HTML was audited after the cold-review fixes. SHA-256: `e5a98bbba1908241825e0cd41b65f37556743ff6245a582c6e6094b2f728db46`.

## Isolated real-browser matrix

Chrome **155.0.8059.86**, DevTools Protocol, Node 26.5.0, direct `file://` loading; no web server. Each browser was a separate `mktemp -d /tmp/art-of-war-qa.XXXXXX` profile with its own ephemeral debugging port and detached process group, launched under **timeout 30**. The harness used `finally` cleanup to terminate the group and delete the profile. No preview or shared browser was used.

Every viewport tested RU and EN × light and dark × Essential/Core/Deep: **48 configurations**, **2,208 rendered screen visits in the final matrix**. Each mode independently traversed its complete corpus using rendered navigation controls. An animation frame was allowed per visited screen. Tests asserted expected title, uniqueness, exact counter, positive content, provenance, scrollability, horizontal bounds, top controls, and appropriate nested text color.

| Viewport | Configurations | Screen visits | Maximum horizontal overflow | Result |
|---|---:|---:|---:|---|
| 320×568 | 12 | 552 | 0 px | Pass |
| 390×844 | 12 | 552 | 0 px | Pass |
| 1024×768 | 12 | 552 | 0 px | Pass |
| 1440×900 | 12 | 552 | 0 px | Pass |

At all sizes:

- Fresh-profile defaults: RU / dark / Deep / cover at 1 of 70.
- All five topbar controls remain inside the viewport, including 320 px; vertical reading content remains scrollable and its end reachable.
- Language and theme rapid toggles preserve the current screen, mode, and saved stable ID; document title, `lang`, descriptions, buttons, source/method text, and dialogs localize.
- Contents and Sources open and close in both languages. Ten source rows and method disclosure appear. Native Escape closes either dialog.
- Buttons, Arrow/Page keys, Space, forward/back horizontal pointer swipes, and final restart pass. Vertical gestures do not page or activate focus.
- Native CDP keyboard events separately confirm F, Escape, and ArrowRight; DOM events cover the broader key/pointer matrix.
- Text tap toggles focus. Header, rail, and back control hide; Next remains inside the safe viewport with at least 44 px height. Focus survives paging. A second tap or Escape restores chrome. Interactive targets, selection, long press, and vertical movement do not accidentally activate focus.
- Reload exposes Continue and Start over. Continue restores the stable ID. A remembered level-3 screen while Essential is selected automatically raises depth to Deep and opens the intended screen. Start over begins at the first reading screen; the final screen clears saved position and returns to the cover.
- Desktop rail is visible at 1024 and 1440, scrollable, and synchronized to the active stable ID at every step. Phone rail is replaced by Contents.
- Both embedded font faces load. FontTools additionally confirms Cyrillic coverage in Geist and Geist Mono. Image decode is **not applicable**: media count is zero; the cover is the maintained typographic motif.
- Full matrix used reduced-motion emulation; native-key and visual checks also used normal motion. Visual snapshots finish slide animations before inspection, avoiding partially faded frames.
- Browser loaded and traversed with network emulation set offline. **0 HTTP(S) runtime requests**, **0 unexplained console/log errors**, **0 runtime exceptions** in final runs.

## Visual inspection and issues resolved

Visually inspected actual screenshots: 320 cover/dark; 320 five-factor list/light; 320 dense chapter XIII prose/EN/dark; 390 nine-situation long list/RU/dark; 390 quantitative evidence card/EN/light; 1024 two-column comparison/EN/light; 1440 typographic cover/RU/light; 1440 final/EN/dark. Checked hierarchy, line wrapping, source/provenance treatment, vertical continuation, footer clearance, rail synchronization, and settled contrast. Reading text, lists, comparisons, and cover pass in the final artifact.

Earlier QA exposed a real nested inherited-color issue during fast theme changes; the local CSS rule above resolved it, and all 48 final configurations include color assertions. A JavaScript style-flush experiment was insufficient and was removed. Early screenshot samples caught animations in progress; final captures explicitly finish those animations. Waiting on animation promises in headless Chrome exceeded a bounded run, so that harness approach was replaced with deterministic animation completion and rerun. Early keyboard harness failures came from dispatching synthetic events at `document` instead of a DOM element and omitting native virtual-key codes; corrected tests pass. These are recorded rather than counted as final passes. No unresolved product failure remains.

## Scope and limits of this QA

Only this collector directory was written. No catalogue, root reader, shared template, LOG, deployment, push, or PR was changed. No catalogue-wide tests, deployment, Safari/iOS device run, or screen-reader certification is claimed. The canonical Home anchor remains `href="./"`; in collector staging it resolves to this directory, and root-library integration is intentionally not performed. Optional external evidence links were researched separately, not clicked during offline runtime QA. Screenshots and temporary harness files were inspection aids and are removed after results are recorded; the deliverables are the requested four files.

Final cleanup verified: no task-owned Chrome/timeout process remains; all task profiles and temporary harness/screenshot files removed. 1 orphaned profile directory from an earlier bounded harness run was removed after confirming no browser used it. No server was started.
