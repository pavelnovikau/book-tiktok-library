Current root acceptance 2026-11-01T04:34:34.608971+00:00: PASS for the exact version in root-review/personal-review.json. Routes24/48/68; Deep9969RU/11120EN noncover-body words including shared final; UI58/53minutes. Earlier worker-phase metrics, hashes and pending statuses below are historical. Root read the complete bilingual retelling and selected actual primary passages, not the whole primary continuously. Missing source-image detail is disclosed here/in method notes rather than inserted into ordinary reading.

---

# Make Time — implementation QA

Status: ready-for-root-personal-check. rootPersonalAcceptance=false; publicationAllowed=false.

These are implementation checks on a draft, not editorial approval, full-English collation, scientific efficacy validation or physical Safari certification. Root must personally read both complete manuscripts, all six routes, the full coverage/omission map and key actual primary passages before publication.

## Exact text and reading estimates

Main body means the 66 authored prose units; it excludes cover, the shared final, titles, author subtitle, section labels, method/Sources and UI. Framing adds cover/final body, all titles and the author subtitle. The additional noncover-body convention (including final) is also in metrics.json. Rates: RU 180 / EN 220 words per minute. No length quota was enforced.

| Route | Screens | RU main body | RU body minutes | RU framing / reader total | RU UI | EN main body | EN body minutes | EN framing / reader total | EN UI |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| essential | 24 | 3,331 | 18.51 | 140 / 3,471 | 20 минут | 3,732 | 16.96 | 166 / 3,898 | 18 min |
| core | 48 | 6,934 | 38.52 | 247 / 7,181 | 40 минут | 7,741 | 35.19 | 299 / 8,040 | 37 min |
| deep | 68 | 9,900 | 55.00 | 335 / 10,235 | 57 минут | 11,034 | 50.15 | 410 / 11,444 | 53 min |

RU main-screen density: 130–168 words, median 150; EN: 143–187, median 167. These are measured densities after writing and segmentation, not imposed bands. Each scrollable screen is one connected two-paragraph thought unit. Cover and shared final are separately measured.

## Structural, parity, and integrity checks

- 69 deterministic audit assertions, no warnings/failures. Counts include cover and shared final. Essential IDs are an ordered subset of Core, itself an ordered subset of Deep.
- Canonical JSON equals the actual embedded screens and sources. All 132 RU and all 132 EN main-body paragraphs equal their drafts in order. All six route exports equal the embedded route bodies and framing exactly.
- All 87 tactic narratives are individually mapped to actual source file and 1-based inclusive paragraph ranges, a retained mechanism, depth and compression rationale. No whole main chapter is omitted. Image and secondary-example omissions are explicit.
- All 124 hashed read-only inputs remain byte-identical, including the private extraction, maintained skill/reference reader, old collector and historical review files. Local reader copies are byte-identical to their recorded maintained sources.
- One primary book-source entry; no duplicate sources used to imply breadth. No copied source chapters, EPUB, publisher artwork or private source quotations are present in the candidate.

## Actual offline Chrome matrix

| Viewport | Rendered visits | Interaction assertions in named block | Real nonzero scroll target | Before / after Settings |
|---|---:|---:|---|---|
| 320×568 | 1,120 | 30 | `.slide-scroll` | 35 / 35 px |
| 390×844 | 1,120 | 30 | `.slide-scroll` | 35 / 35 px |
| 1024×768 | 1,120 | 30 | `.slide-scroll` | 35 / 35 px |
| 1440×900 | 1,120 | 30 | `.desktop-contents` | 35 / 35 px |

Each matrix visits both languages × both themes × Sans/Serif × every screen in all three nested routes (8 × (24+48+68) = 1,120 rendered visits per viewport). The four standard matrices total 4,480. The additional emulated iPhone matrix at 320×568 repeats 1,120 visits and adds the install/safe-area/touch checks; it is reported separately rather than hidden in a claim of independent editorial review.

First actual RU reading-paragraph glyphs were inspected through CSS.getPlatformFontsForNode before eager preload of inactive fonts, after document.fonts.ready. Embedded Geist supplied the first paragraph at each viewport. Subsequent actual RU/EN reading paragraphs used custom Geist Sans, Source Serif 4 for RU Serif and Geist Serif for EN Serif. Merely checking CSS names was not used as font proof. This is not physical-device first-paint timing certification.

At 320, 390 and 1024 a real reading surface was scrolled to 35px before theme/font changes and remained at 35px. At 1440×900 all ordinary RU Sans reading units fit vertically: readingMax=0. Its real nonzero scroll test uses the desktop contents rail at 35px and verifies preservation through Settings. It does not falsely certify nonzero text scrolling on that fitting desktop view.

Covered behavior: fresh RU/dark/Sans/Essential despite seeded legacy EN/Deep progress; same stable ID and depth across language/Settings; Settings gear opens without changing theme; honest localized Serif fallback note; global v1 preferences survive reload; Sources and contents dialogs; F/tap focus, Escape restoration and Next preservation; previous/next buttons and arrow navigation; horizontal pointer swipe versus vertical gesture; desktop active rail and one-row icon geometry; final restart; Continue and Start over; lower-selected Core/Deep resumes explicitly name the deeper route in RU/EN; already-selected Deep Continue also names it; no nonfiction ending-spoiler modal. Old short progress remains untouched.

Emulated iPhone result: 44px top / 34px bottom safe area; six compact controls in one row, minimum top 67px, maximum right 308px; automatic RU install guide, manual EN guide, actual CDP touch swipe, and guide/trigger hidden in emulated standalone mode. Physical iPhone, Safari, and installed PWA behavior were not tested.

Visual inspection used local screenshots: 320 dense RU Serif and cover/final; 1440 EN burner procedure and RU cover/final. Header, typography, line wrapping, vertical scrolling, rail and footer were inspected. There is no image/comparison/list-card content to certify. Zero runtime exceptions and zero HTTP(S) runtime requests in every successful matrix; the HTML was loaded via file:// under offline network emulation, without a content server or preview tools.

## Honest harness history and cleanup

Two initial harness defects were corrected: a quoted English title broke an evaluated JavaScript assertion; a screenshot requested a Deep-only contents entry while Core was selected. These were test-script errors, not claimed reader fixes. The initial desktop attempt also exposed a vacuous reading-scroll assumption: no text overflow existed at that viewport. The final harness records and tests the real desktop rail instead. Failed and earlier proof files remain named as attempts/pre-entity-fix records and are not counted as final evidence.

Text-node apostrophes were initially encoded as &#x27;, which the stock builder could count as extra lexical tokens. Preparation now escapes only characters necessary in text nodes; final metrics count displayed words correctly. The HTML was rebuilt and all final matrices rerun against the final hashes. No primary text was changed to satisfy checks.

Every owned Chrome used /usr/bin/timeout 30, a unique mktemp profile, a dedicated detached process group and a finally cleanup. Every successful and failed recorded run reports profileRemoved=true and remainingOwnedPids=[]. No server, temporary profile, Chrome process, watcher or old task remains owned by this run.

The candidate is locally reviewable. Publication remains disallowed until root personally accepts the exact final hashes.
