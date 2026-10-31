# I, Robot — implementation QA

**Parent status, 2026-10-31:** independent cold review completed, all required findings repaired, fresh audit and targeted browser checks passed. Ready for catalogue integration; not published. Collector-stage notes/fingerprints are retained below, with the final repair record at the end.


Date: **2026-10-31**. This is the implementer's validation record, **not independent editorial/cold review**. Parent review and integration remain pending. No publication, git/PR work, catalogue/root-reader edits, shared-template edits or LOG entry were made.

## Deliverables and exact counts

Only `story-data.json`, `i-robot.html`, `sources.md`, and this `QA.md` are retained in the owned directory. Schema 2, stable slug `i-robot`; audience `teen-14-plus`; spoiler policy `full-plot-in-deep`. Default **RU / dark / Essential**.

| Cumulative mode | Screens | RU reading words | EN reading words | RU estimate | EN estimate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 30 | 1,680 | 1,852 | 10 min | 9 min |
| Core | 72 | 4,062 | 4,447 | 23 min | 21 min |
| Deep | 112 | 6,319 | 6,906 | 36 min | 32 min |

Counts include the level-1 cover and level-1 final. Additions: **30 level-1 / 42 level-2 / 40 level-3**. Reading words follow the maintained builder's Unicode token counter and include titles, cover subtitle and body, excluding sources/UI/captions. Estimates use its defaults, 180 RU / 220 EN words per minute, rounded up; they are reading estimates, not timed study measurements.

Body-only cumulative totals: RU **1,552 / 3,746 / 5,827**, EN **1,693 / 4,064 / 6,302**. Excluding the cover, body totals are RU **5,789**, EN **6,257**. All 111 non-cover screens fall within 35–75 body words: RU **48–57**, mean **52.15**; EN **52–61**, mean **56.37**. The audit's totals are RU **6,314**, EN **6,901**, five fewer each because it omits the cover subtitle; this is a counting-definition difference, not corpus drift.

**17 listed sources**; these include a collection review and nine story reviews by the same critic, not seventeen independent perspectives. Provenance: 36 `book`, 4 `corroboration`, 71 `synthesis`, plus one cover. Every source is used. One embedded original SVG priority illustration; no publisher artwork or external runtime assets. Final HTML: **423,735 bytes**.

## Actual reading/access boundary

The official PRH opening sample of “Robbie” was read, ending at Mrs Weston's dismissal of Robbie (1,551 whitespace-delimited words in the extracted sample including its publisher credit). The complete relevant nine-story plot-summary section of the publisher teacher's guide and discussion material were read, with contradictions recorded in `sources.md`. Author-interview passages, Suvin's Asimov section/caveat, Jenkins's collection review and all nine individual reviews were consulted. Googe access was to relevant openly indexed thesis passages; the direct PDF retrieval returned zero bytes. NIST framework sections and the opening of Turing's primary paper support bounded comparisons.

**No complete collection, complete lawful EPUB or complete thesis was read.** Plot beyond the Robbie sample is reconstructed and cross-checked through the publisher guide and criticism. The in-reader method and source notes say so. No invented quotations, dialogue, page locators, scenes or claims of complete-text fidelity. This companion provides original analysis, selected mechanisms and questions; it is not a chapter-by-chapter substitute or an abridged translation.

## Build and deterministic checks

Built with the current maintained builder and shared icon header; no private shell or post-build UI patch.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/i-robot/story-data.json --out collector-output/i-robot/i-robot.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/i-robot/i-robot.html --min-screens 112 --require-bilingual
```

Result: **68 passes / 0 warnings / 0 failures**. Additional content checks: 112 unique stable IDs; exact target counts; level-1 cover/final; all references valid and all sources used; non-cover density in range; no scripts, network links or event-handler attributes in body copy; no flagged late-resolution phrases in levels 1/2. These are implementation/self-checks, not an independent factual endorsement.

## Collector-stage real-browser matrix (before parent repairs)

Local Google Chrome, `--headless=new`, CDP automation against **file://**, no server, no preview tools. Every visible screen traversed in every mode, both languages and both themes, checking exact title, counter position, mode count, document bounds, slide bounds and desktop rail state.

| Viewport | Languages | Themes | Exact modes | Screen visits | Result |
| --- | ---: | ---: | --- | ---: | --- |
| 320 × 568 | 2 | 2 | 30 / 72 / 112 | 856 | PASS |
| 390 × 844 | 2 | 2 | 30 / 72 / 112 | 856 | PASS |
| 1024 × 768 | 2 | 2 | 30 / 72 / 112 | 856 | PASS |
| 1440 × 900 | 2 | 2 | 30 / 72 / 112 | 856 | PASS |

**3,424 final matrix visits** = (30 + 72 + 112) × 2 languages × 2 themes × 4 viewports. Zero document/body horizontal overflow; zero slide horizontal overflow; zero document/body vertical overflow. Vertical scrolling **inside** the slide is intentional for the cover and dense 320px screens, and is not hidden by document overflow. Desktop cover-copy, visual and layout rectangles were explicitly checked against the reading-pane edges at 1024 and 1440, rather than inferring containment from document width alone.

Geist and Geist Mono reported loaded; the embedded SVG decoded. Rapid twenty-cycle language/theme switching preserved decoded media and fonts. Zero observed runtime exceptions, console errors or external HTTP(S) runtime requests.

## Interaction and focus checks

Passed at phone 390 × 844 and desktop 1440 × 900:

- Native CDP Space keydown/keyup on focused Chapters, language, theme, Sources, Start and Next controls. Buttons activate natively; Space on Chapters preserves the cover. Unfocused Space advances, ArrowLeft returns.
- **F after Next while Next remains focused**, Next while focused, then Escape: focus enters, persists through paging and exits. Header, progress, rail, Back and non-reading cover controls hide; content and safe Next remain.
- Text taps toggle focus twice; vertical gestures do not toggle it; horizontal swipes page and do not toggle focus.
- Header controls are icons only, with accessible names and tooltips in both language states. One compact row; Home retains `href="./"`. Home navigation itself was not followed into a catalogue/root reader outside this assignment.
- Chapters and Sources open/close; 17 sources and the explicit incomplete-reading method note render. Inline provenance also opens Sources.
- Hidden-ID fallback exercised through an existing bound chapter control with its target changed to the Deep warning: mode raises to Deep and navigates by stable ID. The normal Essential contents intentionally do not expose spoiler titles.
- Saved position, Continue, Start over, language/theme position preservation and final Restart clearing saved progress all pass.

Cover focus received explicit containment, hidden-chrome and reachable-Next assertions at all four viewports, RU/EN and both themes. Cover, focused cover, representative dense Deep and final screenshots were captured for all four sizes × both languages × both themes. Representative outputs were visually inspected at each size, including 320px scrolling, 1024px stacked cover containment and 1440px two-column cover. Screenshots and automation scratch were removed to retain exactly the four canonical files.

## iOS guidance checks and limits

Chromium with an iPhone Safari user agent, at 320 × 568: guide auto-opens once; copy honestly says a website cannot hide Safari chrome; Share → Add to Home Screen and relaunch from the Home Screen rather than Telegram are present. Manual guide localizes to EN, closes, and remembers dismissal. All six controls including the install icon share one reachable row without text labels or a second install row. Focus hides the trigger and suppresses opening the guide.

Separate emulation of `navigator.standalone` and of the `(display-mode: standalone)` query suppresses both guide and trigger. This is behavioral emulation, **not a physical iPhone/Safari installation test**. The standalone HTML works from a file without networking; actual Home Screen installation depends on the parent library's hosting/PWA context, which this assignment does not modify.

## Spoiler/editorial boundary

Essential forms a complete question/thesis/case-invitation/qualification/final-model arc. Core adds circumstances and analytical distinctions without selected resolutions. The first Deep screen is an explicit warning before the first disclosed solution. The final story's steering explanation and the selected solutions to individual stories appear only at level 3. Byerley's identity is preserved as unresolved, not falsely established.

Global source titles/notes and the method note were self-checked: they warn that linked external pages can contain spoilers without describing the late outcomes. The full working ledger is for reviewers and explicitly includes spoilers. No film action plot, Reichert novels, later-series solution or formal later Zeroth Law is silently added. Fictional laws are explicitly distinguished from actual AI safety guarantees.

Remaining limitations: no full-edition sentence/scene/translation verification; incomplete primary text; secondary plot sources have documented errors; original synthesis is substantial; age 14+ is an editorial recommendation. Independent cold editorial review and parent integration remain required before publication.

## Collector-stage rebuild identity

SHA-256 of the validated content and maintained construction inputs:

- `collector-output/i-robot/story-data.json`: `49e7a575e1282ecf5e93b33b72579f138dd539e0a5ba1f5d49bb0d3681f04113`
- `collector-output/i-robot/i-robot.html`: `1973ba1fce148c3a1b68602ea021db2fcd06ef320c6322a6e8d86ef943aed0e7`
- `skills/book-tiktok/scripts/build_story.mjs`: `f0a5e65358aa159f9cc64266ff9629cc80fbe392a3f52025a25ce909f6c08c3b`
- `skills/book-tiktok/assets/standalone-template.html`: `690b5beae668868566c7680ebfed5f59736b49506bdee09b4046247a8d13e724`
- `skills/book-tiktok/assets/reader-header.html`: `0947f8417d61e5d8944e9ec010defef2bba747e5dc8583436ce4cf2729881623`

Each manually launched Chrome was run under `/usr/bin/timeout 30`, with a unique temporary profile and debug port. Owned detached process groups received cleanup in `finally`; post-cleanup checks found no process using any owned profile, and every profile was removed. No Chrome, Vite, HMR connection or server belonging to this task remains.

## Independent cold review and parent repairs — 2026-10-31

Fresh independent review read all 112 RU/EN pairs and returned READY WITH FIXES. Parent applied both required findings: rules-and-intensity and runaround-equilibrium now cite [2,5,8], attaching the already-listed Googe thesis to the strengthened-self-preservation detail; the shared Russian review role now reads «Обзор», without overstating literary criticism as a research review. The reviewer identified the relevant indexed thesis passage on p.34. Direct full-thesis/full-collection reading remains unclaimed.

Final-build targeted QA passed 32 changed-screen states and 16 source-panel states across 320/390/1024/1440, RU/EN and both themes. Rendered source references include 2,5,8; raw literary-review roles read «Обзор» / “Review”. Exact data parity and the fresh 68-check audit pass. Zero runtime errors, external requests or horizontal overflow; text bottoms remain reachable. The 3,424-visit collector matrix was not repeated.

Current SHA-256: JSON `1390d2e11ff42451eff698cde9ee02e2eac012cb57335dfe7739ffb9ddada52f`; HTML `ab6d14ae97c2c19a4eddd6bd0dec865dcaf22cebd692918cbab987bae016de6c`; shared template `373caac52171dd92c0de3048dd6d59b08a627c7fcd0b998f8aceda6f345d69f1`. Earlier fingerprints and broad matrices above identify the collector stage, not a claim of repeating that entire matrix after these localized repairs.

Ready for parent catalogue integration. No publication is claimed. Owned Chrome processes/profiles were cleaned; no server was started.
