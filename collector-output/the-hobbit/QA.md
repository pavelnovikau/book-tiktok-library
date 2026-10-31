# The Hobbit — collector QA

Date: 2026-10-31. Result: PASS after cold-review remediation, within the browser/emulation boundaries below.

## Package and scope

Exactly four deliverables in `collector-output/the-hobbit/`:

- `the-hobbit.html` — portable reader, embedded content/CSS/JavaScript/fonts.
- `story-data.json` — schema v2 bilingual content and source IDs.
- `sources.md` — evidence boundary, prior claim map, source ledger, rights notes.
- `QA.md` — this report.

The collector itself was built without editing the catalogue, shared template or another collector. The reviewed package was subsequently promoted into the library as `the-hobbit.html`; catalogue integration is verified separately below.

Built using the skill’s maintained `build_story.mjs`. Book-local additions to the generated HTML implement explicit spoiler consent and safe saved-position labels, a typographic cover, chapter anchors, descriptive provenance labels, accessible dialog names, compact desktop cover sizing, reduced-motion rendering, and focus-mode corrections (hide counter/citations, retain Next even on cover). The maintained theme tokens were inherited; shared theme/source work was not edited. A plain rebuild from JSON alone would need these reader customizations reapplied before replacing the shipped HTML.

## Exact counts, words and estimates

Counts include the cover and final screen. Levels: 36 at level 1, 54 at level 2, 54 at level 3. Modes are nested filters of one ordered 144-screen corpus.

| Mode | Visible screens | RU words | RU minutes | EN words | EN minutes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 36 | 1,742 | 10 | 1,944 | 9 |
| Core | 90 | 4,328 | 25 | 4,915 | 23 |
| Deep | 144 | 6,872 | 39 | 7,840 | 36 |

Word counts use the builder’s Unicode word rule and include screen titles, cover subtitle and bodies; navigation, source notes and chapter labels are excluded. Estimates use 180 RU / 220 EN words per minute, rounded up. Bedtime pauses or reading aloud take longer.

Body density: RU 37–47 words per screen (mean 42.13); EN 42–62 (mean 47.68). English is approximately 14% longer by total words; manual parity review found no omitted facts or qualifications. The auditor’s body/title totals are 6,865 RU / 7,832 EN because it excludes the cover subtitle.

Provenance: 59 book-event/image screens, 9 context/corroboration screens, 76 synthesis screens (including the cover and final). All 144 screens have source IDs; 10 distinct sources. No external media or protected cover/artwork; image-decode checks are inapplicable. The cover is original typography, not a reproduced jacket.

## Cold-review remediation

An independent cold review read the skill, references, all four files and all 144 RU/EN screens. Its verdict was READY WITH FIXES. The package was corrected before catalogue integration:

- Removed unsupported specifics about Fíli and Kíli’s final defence, Thorin’s burial objects, Bilbo’s exact chests and the precise mechanics of the 1937 Gollum bargain. The evidence disclosure now says the publisher guide supports event structure, not every detail.
- Corrected chapter anchors: departure to chapter 2, the final support from Lake-town to chapters 10–11, the confrontation to chapter 17, and Bilbo’s loss of consciousness/outcome to chapters 17–18.
- Reclassified four interpretive screens (`a-voice-nearby`, `c-rest`, `h-elvenking`, `k-self-naming`) as synthesis and made their interpretive status explicit in both languages.
- Replaced two semantic duplicates with distinct reader tools: a consequence map and a return test, preserving the agreed 36 / 90 / 144 nested counts.
- Corrected the Russian ring wording from an invisible “owner” to the person wearing it. RU/EN parity was rechecked after the change.

The source ledger records these removals and the narrower fidelity claim. The normalized JSON was re-injected into the customized reader rather than replacing the spoiler gates, focus behavior or mobile additions with a plain template rebuild.

## Skill audit

Command: `node audit_story_html.mjs the-hobbit.html --min-screens 144 --require-bilingual` using the skill’s installed auditor.

Post-review result: 68 passes, 0 warnings, 0 failures. Exact metadata/corpus/target counts: 36 / 90 / 144. Unique stable IDs, RU/EN copy, valid source IDs, correct cover/final placement, responsive hooks and offline invariants pass. Embedded screens are byte-equivalent as parsed JSON objects to the source JSON screens. HTML contains no private filesystem paths, file URLs or temporary-profile paths.

## Browser matrix

Local Playwright-driven Chromium, opening the final standalone HTML through file navigation with offline mode enabled and HTTP/HTTPS interception. Each row covers both languages, all three depths, and normal/focus reading.

| Viewport | Themes | Complete screen visits | Result |
| --- | --- | ---: | --- |
| 320 × 568 | light + dark | 2,160 | PASS |
| 390 × 844 | light + dark | 2,160 | PASS |
| 768 × 1024 | light + dark | 2,160 | PASS |
| 1440 × 900 | light + dark | 2,160 | PASS |
| 1024 × 768 (additional skill orientation) | light + dark | 2,160 | PASS |

Required four sizes: 8,640 visits. Including additional orientation: 10,800 visits. Every visit asserted matching localized title, valid selected-mode position, exact mode count, zero page or reading-area horizontal overflow, and no outer-page vertical overflow. Long reading bodies remain internally vertically scrollable; this is intentional at 320 × 568. Focus visits also asserted hidden chrome/counter and a visible, safe, at-least-44px Next target. Normal visits asserted topbar controls stay within bounds and desktop rail appears at the intended breakpoint.

Both embedded font faces loaded offline. Zero runtime/page exceptions, unexplained console errors or attempted HTTP/HTTPS runtime requests in the matrix. No runtime fetch/XHR/WebSocket/EventSource/service-worker dependencies are present. Source links are optional external exits.

## Functional checks

39 navigation/spoiler/focus assertions passed:

- Russian/dark/Essential fresh default; Essential contents expose no Deep death-title.
- Core and Deep warnings appear before depth changes; Cancel and Escape preserve the previous mode.
- Consent is scoped to the session. A saved Deep position without consent reopens safely in Essential, with a generic Continue label and a fresh gate before restoring Deep.
- Hidden remembered-screen navigation raises depth only after consent.
- Language/theme switching preserves stable screen ID; Continue restores progress; Start over selects first content; final Restart clears the bookmark.
- Chapters and Sources dialogs work, including all 10 links and localized method text.
- Inline citations open Sources.
- Next/Back, arrows, Page keys, Space, pointer swipe and chapter selection work.
- Tap toggles focus; a second tap and Escape restore chrome; F toggles it.
- Focus survives paging; vertical drag and horizontal swipe do not become accidental focus taps.
- At desktop width, the rail is visible, scrollable, synchronized to active screen, and hidden in focus.
- Home control has localized accessible labels and the exact required `href="./"`. Clicking navigates to the host directory.

8 additional touch/selection/rapid-switch assertions passed: actual emulated touchscreen tap/second tap, ignored long press, ignored existing text selection, citation interaction without focus toggle, rapid RU/EN + theme switching with correct final state and resolved light-theme text contrast.

9 iOS/standalone-emulation assertions passed: guide automatically opens once in iPhone browser emulation; exact Share → Add to Home Screen route is localized; relaunch-from-Home-Screen advice is present; manual trigger works; focus hides trigger/guide; emulated installed mode suppresses both. This is Chromium emulation of iPhone user-agent/standalone signals, not physical-device or real Safari validation. No claim is made that ordinary Safari chrome can be forcibly removed.

Home integration: the promoted root reader retains the exact `href="./"` contract, where it returns to the library catalogue. The catalogue entry uses the `fiction-adventure` section, `for-son` collection, `teen-14-plus` audience and `full-plot-in-deep` spoiler policy. Its original green round-door/return-road cover motif is registered in the renderer and validator rather than reusing another book’s geometry.

Post-integration library QA passed with **11 books, 8 declared sections, 7 populated shelves, 4 collections and 1,155 screens**. The browser suite rechecked the catalogue at 320 × 568, 390 × 844 and 1440 × 900, then all 11 promoted readers: runtime errors 0, horizontal overflow 0, focus mode passed, and iOS browser/standalone guide behavior passed. The catalogue renderer produced 11 distinct semantic SVG motifs; `door` was present and unique. A stable 1440 × 1200 screenshot of the filtered fiction/adventure shelf was visually inspected: the Hobbit card’s round green door and returning road are distinct from the adjacent acceleration curve, with no card/title clipping in the inspected frame.

## Visual inspection

Stable-paint screenshots were inspected for:

- 320 × 568 RU dark cover, dense large-type synthesis, and final.
- 390 × 844 EN light long-list screen.
- 768 × 1024 EN light spoiler dialog and reading screen; EN dark final in focus.
- 1440 × 900 EN light cover, chapter rail and source labels.

No clipping of horizontally laid-out content or inaccessible navigation was found. Small-phone long text scrolls within the slide rather than underneath the fixed footer. Cover, dense/list, final, provenance and dialog layouts are legible. No documentary images, comparison grids or quantitative charts are present, so those optional visual categories are not claimed as tested. Theme/language screenshots were captured after settling the paint; a reduced-motion rule avoids transient blank slide animation.

## Content and spoiler review

Essential is substantially spoiler-light: premise, small-hero growth, reading tools, ordinary pleasures and moral questions; no named deaths or detailed dragon/battle resolution. Core adds selected episodes, mechanisms and interpretations, but does not give the complete ending. Deep narrates all 19 chapters’ main arc, including riddles/escape, forest rescue, barrels, dragon discovery, Bard’s action, competing claims, the Arkenstone decision, battle, named losses, settlement, return and epilogue.

Songs, riddles, narrator humour and indirect speech are discussed in original prose; no song lyrics, riddle texts, reconstructed dialogue or extended quotations are reproduced. Modern narrative and publication variants are separated. 1937 publication, 1951 Gollum revision, unfinished 1960 rewrite and actual 1966 edition are distinguished. No invented page numbers or Russian-edition wording.

## Evidence boundary — exact reader disclosure

### RU

Это самостоятельный аналитический дайджест, не текст романа и не перевод какого-либо издания. В проверенной локальной библиотеке EPUB/FB2/PDF «Хоббита» не найден; полный текст романа не читался и не загружался. Каркас событий сопоставлен с открытым издательским руководством по главам 1–19, но руководство не является романом и не подтверждает каждую подробность; неподтверждённая конкретика опущена. Контекст сверялся с Tolkien Estate, архивной описью и библиографией. Страницы и дословные цитаты не заявляются. «Книга» означает сообщаемое событие или образ; «Контекст» — внешние сведения; «Синтез» — нашу интерпретацию. Essential почти без спойлеров; Core раскрывает эпизоды; только Deep содержит всю развязку. Внешние источники могут сами содержать спойлеры.

### EN

This is an original analytical digest, not the novel’s text or a translation of any edition. No EPUB/FB2/PDF edition of The Hobbit was found in the checked local library; the full novel was neither read nor downloaded. The event structure was compared with the public publisher chapter guide for chapters 1–19, but that guide is not the novel and does not verify every detail; unsupported specifics are omitted. Context was checked against Tolkien Estate, an archival finding aid and bibliography. No page references or verbatim quotations are claimed. “Book” identifies reported events or imagery; “Context” identifies external evidence; “Synthesis” identifies our interpretation. Essential is substantially spoiler-light; Core reveals episodes; only Deep contains the full resolution. External sources may themselves contain spoilers.

A source ledger is not a claim to have read a full edition or unexamined archival items. The consulted guide contains some errors; the raven is correctly called Roäc here. Source 9’s erroneous date for the later novel was not reused. External source pages themselves can contain spoilers.

## Cleanup

All QA Chromium launches used unique `mktemp -d` profiles and a 30-second timeout. Contexts were closed in finally blocks and temporary profile trees removed by scoped cleanup. Screenshots were returned in memory; no screenshot files, QA scripts, local web server, HMR connection or source ebook was left behind. Final check after shutdown: 0 owned Chromium processes, 0 temporary QA profiles; exactly the four requested deliverables remain.
