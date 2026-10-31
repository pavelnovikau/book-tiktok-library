# QA — The Children of Captain Grant

2026-10-31. Implementation self-check only; **independent cold editorial review and catalogue integration remain with the parent**. No publication, deployment, git operation, shared-template edit, or LOG update was performed.

## Build and contract

Built from schema-v2 `story-data.json` using the maintained `skills/book-tiktok/scripts/build_story.mjs` and its latest available shared template plus `reader-header.html`. A final rebuild produced the exact HTML tested in the browser.

- Total: **144** unique stable screen IDs. Levels: **36 / 54 / 54**; cumulative **36 / 90 / 144**. Cover and final are level 1.
- Defaults: **RU / dark / Essential**. Audience: `teen-14-plus`; policy: `full-plot-in-deep`.
- Provenance including cover: **69 book / 67 synthesis / 8 corroboration**. The cover is one synthesis item; every factual screen has source references. Every screen also has a working `evidence` locator or analytical job in the JSON.
- **8 sources**, **1 original embedded SVG cover**, **2 embedded variable fonts** (Geist and Geist Mono). No publisher artwork, copied dialogue, remote runtime assets, server or service worker.
- Reader file: **455,112 bytes**, standalone under `file://`.

| Mode | Screens | RU words | EN words | RU estimate | EN estimate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 36 | 1,775 | 2,099 | 10 min | 10 min |
| Core | 90 | 4,473 | 5,241 | 25 min | 24 min |
| Deep | 144 | 7,190 | 8,432 | 40 min | 39 min |

Word totals above use the builder's Unicode counter for title + subtitle + body, excluding interface, section labels, source notes and media credits. Body-only totals: **6,452 RU / 7,529 EN**. All 143 non-cover screens are inside the ordinary density band: **40–50 RU words** (mean 44.87) and **47–60 EN words** (mean 52.36). The deterministic auditor reports 7,183/8,426 words because its count excludes the cover subtitle; this is a counter-scope difference, not corpus drift. Estimates use 180 RU / 220 EN words per minute and round upward; actual reading and discussion take longer.

## Deterministic audit

Commands run:

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/children-of-captain-grant/story-data.json --out collector-output/children-of-captain-grant/children-of-captain-grant.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/children-of-captain-grant/children-of-captain-grant.html --min-screens 144 --require-bilingual
```

Result: **68 passes, 0 warnings, 0 failures**. Exact mode nesting, bilingual fields, source/provenance/media references, fonts, offline invariants and responsive shell hooks passed.

## Real Chrome matrix

Chrome was driven with Playwright over a dedicated CDP port, loading the standalone `file://` directly. Each manually started process was wrapped in **`timeout 30`**, used a separate `mktemp -d` profile and detached owned process group, and was closed/killed with profile removal in `finally`. No preview tools or web server were used.

Every mode was traversed in both languages and both themes at every viewport: `(36 + 90 + 144) × 2 × 2 × 4 = 4,320` actual rendered visits. Each visit checked the title, counter, active rail item, document width/height and slide width. The cover's layout, visual, title, mode picker and action columns were checked against the actual slide bounds in every state; document overflow alone was not used as a cover test.

| Viewport | Rendered visits | Document X overflow | Slide X overflow | Document Y overflow | Functional checks |
| --- | ---: | ---: | ---: | ---: | ---: |
| 320 × 568 | 1,080 | 0 | 0 | 0 | 32 / 32 |
| 390 × 844 | 1,080 | 0 | 0 | 0 | 32 / 32 |
| 1024 × 768 | 1,080 | 0 | 0 | 0 | 32 / 32 |
| 1440 × 900 | 1,080 | 0 | 0 | 0 | 32 / 32 |

All dimensions above are CSS pixels; maximum overflow is **0**. Slide **vertical** scrolling remains intentional, especially at 320×568 and for the cover at 1024×768. It does not scroll the document or create horizontal clipping. At 1440×900 every tested slide fits vertically. The desktop rail remained scrollable and its active entry was synchronized and visible.

Passed functional checks at all four viewports:

- A single compact header row has only the five SVG icon controls. Each has a tooltip and an accessible name, and each lies within the header and viewport. The iOS hint adds a sixth icon in that same row.
- Native Space on focused Sources and Contents opens their dialog without paging. Language and theme Space activates only that control; Space on the home anchor does not page; Space on Next advances exactly once. A cover action also responds once. Unfocused-body Space and arrow navigation work.
- **F and Escape work immediately after Next while Next retains focus.** Text tap toggles focus; the cover's controls disappear while reading content and Next remain; Next preserves focus mode.
- Source and contents dialogs open and close. Sources has eight entries. Bound navigation to a currently hidden Deep screen raises the depth correctly.
- Language/theme changes preserve position. Reload offers Continue and Start over; Continue restores the remembered screen; final Restart clears the remembered location.
- A horizontal pointer gesture advances; vertical movement and a long press do not toggle focus.
- Embedded fonts and cover decode. **Zero console/runtime exceptions and zero external runtime requests.**

Separate iOS-behaviour emulation passed **20/20 checks**, covering 320 and 390 widths, RU/EN guidance, native Space on the install icon, one-time automatic opening, manual reopening, and suppression of both guide and trigger during focus. Standalone suppression was checked through both `navigator.standalone` and `display-mode: standalone`. Guidance explicitly says the page cannot hide browser chrome and gives **Share → Add to Home Screen → relaunch from that icon, not Telegram**. At 320 px the guide is a vertically scrollable native dialog.

This tests the reader's detection and UI logic in Chrome with iPhone UA/standalone emulation. It is **not** a physical-device Safari or actual Home Screen installation certification.

## Visual inspection

Inspected screenshots of the 390 phone cover, 1024 and 1440 desktop covers, narrow 320 dense English content and RU final, light desktop content and the iOS guide. Text, original vector cover, provenance, rail, controls and focus action remained legible and horizontally contained. This corpus uses prose screens rather than artificial comparison/list layouts; no unused layout type is claimed as tested.

## Content and spoiler checks

The claim/plot/theme map and ledger were written in `sources.md` before screen prose. RU/EN share IDs, levels, provenance, references and evidence locators. Numerical/qualifier parity was checked during authoring. In particular: approximate character ages, 37°11′ south, the distinction between latitude and longitude, and edition counts agree in both languages.

Essential/Core were inspected for the ending and decisive later disclosures. They do not identify the final place, expose the later identity revelation, explain the decisive letter error, or state the reunion outcome. Twelve consecutive Deep-only screens begin with an explicit full-spoiler warning. Their later event headings also avoid giving the answer away before the warning. The global Sources dialog and method note were inspected separately and tested for the late spoiler terms; neither leaks them. Optional external original-text links can contain spoilers, as disclosed.

The analytical companion distinguishes historical colonial/ethnographic language from its own position and qualifies fantastic animal and geothermal episodes. It does not promote adventure scenes into zoological, geological or safety guidance. The final island is identified as the novel's geography, without claiming its modern existence.

## Source boundary and limitations

The lawful PG2083 file is the Horne-edited historical English version (66 chapters), not the 70-chapter French original. Selected passages across all three parts were read; no continuous full-book or full-original reading is claimed. Seven French chapter pages and the original contents were consulted, with key detailed checks for the coordinate and late resolution. The Centre international Jules Verne publication record was consulted through its indexed record after a full-page fetch timed out. The ledger distinguishes this from full-text access. Modern Russian translations, adaptations and publisher artwork were not used.

The result is an original, source-backed analytical companion. Interpretations and discussion exercises are explicitly synthesis, not claims of Verne's formal thesis. Independent editorial review has not occurred in this implementation run. The parent should cold-review narrative fidelity, translation nuance, density and spoiler boundaries before integration.

## Artifact identity and cleanup

HTML SHA-256: `b3dabc87add9ba2a7c1a705be0d31d08861f12e8b9c8735853a9b72f5958e613`.

Canonical retained files only: `story-data.json`, `children-of-captain-grant.html`, `sources.md`, `QA.md`. Research downloads, authoring helper, QA scripts, per-viewport reports and screenshots were kept outside the repo and removed at handoff. Owned Chrome/profile checks after QA found **0** running Chrome processes and **0** remaining temporary profiles. No Vite/HMR or server was started.

## Independent editorial review — parent acceptance, 2026-10-31

A separate codex_2 / gpt-6.1-sol / max reviewer read the skill and references, CONTRIBUTING.md, all four collector files and all 144 RU/EN screen pairs. Verdict: **READY; no required fixes or blocking findings**. A fresh deterministic audit passed 68/68 with zero warnings/failures and exact JSON/HTML correspondence. Targeted primary-text checks covered edition boundaries, latitude notation, reconstructed date versus wreck date, late identity/instruction/naming details and the ending; official corroboration and spoiler boundaries also passed. Verification was targeted, not continuous full-novel reading. No repeated browser matrix was claimed. The review left the collector files unchanged.

Parent integration adds the shared library shell to the root-level published copy and a unique latitude-search catalogue cover. The four collector files remain the source package. The root copy passed a fresh 68-check audit at 36/90/144. Library validation passed at 26 books / 3,129 screens; integration Chrome QA passed all 26 readers on phone/desktop, catalogue covers/filters, focus and emulated iOS browser/standalone behaviour with zero runtime errors. Publication remains dependent on the PR checks and deployment verification.
