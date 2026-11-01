Current root acceptance 2026-11-01T03:35:57.839990+00:00: PASS for the exact version in root-review/personal-review.json. Routes37/70/107; Deep13219RU/13988EN body words; UI77/67minutes. Earlier worker-phase counts, hashes and checks below are historical. Root read the complete bilingual retelling and selected actual primary passages, not the whole primary book continuously.

---

# Candidate QA and reading limits

Status: **ready-for-root-personal-check**. `rootPersonalAcceptance=false`; `publicationAllowed=false`.

## Exact content and reading counts

107 total bilingual screens: one cover and 106 reading fragments, including the shared final. Every reading fragment has two corresponding paragraphs. **212 RU and 212 EN draft paragraphs** match the structured data and embedded HTML exactly, in order. All six route exports also match exactly.

| Mode | Screens incl. cover/final | RU body words | EN body words | RU body minutes / reader estimate | EN body minutes / reader estimate |
|---|---:|---:|---:|---|---|
| Essential | 37 | 4,508 | 4,813 | 25.04 / 27 минут | 21.88 / 23 min |
| Core | 70 | 8,594 | 9,111 | 47.74 / 50 минут | 41.41 / 44 min |
| Deep | 107 | 13,197 | 13,960 | 73.32 / 77 минут | 63.45 / 67 min |

Body time uses **180 RU / 220 EN words per minute**. The unrounded body minutes above are estimates, not tested reading speed. Rounded-up body times are RU **26/48/74** and EN **22/42/64** minutes. The reader's more conservative labels include cover, title and subtitle text: RU **27/50/77**; EN **23/44/67**. Russian minute declension is correct for the actual labels.

Words use the maintained builder's Unicode lexical-token regex. Body excludes the cover, headings, subtitles, section labels, permanent interface, Sources and method notes; it includes the final. The builder's estimate text is **body + reading headings + cover**, not a count of every UI string.

| Mode / language | Body | Reading headings | Entire cover text | Builder estimate text | Repeated section labels, excluded |
|---|---:|---:|---:|---:|---:|
| Essential / RU | 4,508 | 168 | 44 | 4,720 | 97 |
| Essential / EN | 4,813 | 195 | 51 | 5,059 | 100 |
| Core / RU | 8,594 | 323 | 44 | 8,961 | 191 |
| Core / EN | 9,111 | 378 | 51 | 9,540 | 197 |
| Deep / RU | 13,197 | 495 | 44 | 13,736 | 291 |
| Deep / EN | 13,960 | 573 | 51 | 14,584 | 302 |

Reading-screen density: RU 100–155 body words, median 124.5; EN 99–154, median 132. Longer phone screens scroll vertically; all paragraph tails were reached in browser traversal.

## Why this volume

The 13,197-word RU body is justified by the retained causal argument across all 18 chapters: communication/feedback, distinct organ costs, development/reproduction, immune timing and cancer limits, pain/memory/sleep/aging, experimental appraisal/control, depression/personality, reward/addiction and the social-scale account of inequality and resources. The map contains 68 grouped cases, experiments or author illustrations with setup/result/limits. This is not 68 independent scientific replications.

The old root's 144 screens contain 6,252 RU body words; the distinct 51-screen collector contains 2,247. The new candidate has fewer screens than that root but much more explanatory room. Counts were derived after the completed exposition and selection of cumulative routes; the 12–18k planning range was neither a filler target nor an acceptance test. Omissions remain substantial and explicit in `sources.md` and the map. This volume does not establish fidelity or root acceptance.

## Source and editorial checks

Both prefaces and all 18 main bodies were read completely in bounded chunks. Hashes and continuous read ranges are recorded in `source-reading-ledger.json`; integrity checks confirm all 18 main-body ranges are covered and all private source hashes remain unchanged. Notes were selective: chapter 1 notes 1–14, chapter 4 notes 52–53 and chapter 10 note 280. **All notes read: false.** English translates the new condensation; published-English collation was not done.

The complete RU exposition was written before the corresponding EN. Worker continuity inspection retained standalone entry points for shorter modes: Selye is introduced on first use, allostatic load is glossed where it first reaches those routes, and no hidden Deep fragment is required to decode those terms. Actual cases demonstrate shorter-mode claims. The original full prose, route membership, source map, omissions and final text remain for root's own complete review. This is an implementation check, not independent editorial acceptance.

The rat-care passages remain distinct. MRI volume is not counted as dead neurons; an unlocated twin-study setup is not attributed to this edition. Cancer onset/progression/survival and distress are separate. Historical receptor models and endocrine hypotheses stay historical. Five narrow current qualifications are labeled explicitly and mapped to official sources or the original research abstract. The full modern medical literature was not reviewed.

## Structural and browser results

The maintained deterministic audit completed **69 passes, zero warnings and zero failures**. `contentMode=explanatory`; fresh default RU / dark / Essential / Sans. The standalone HTML is 819,753 bytes and needs no runtime files or network. It embeds the maintained Geist Sans/Mono/Serif and Source Serif 4 fallback with licenses. Six sources remain accessible globally with their roles.

Five isolated real-Chrome runs covered **320×568, 390×844, 1024×768, 1440×900**, plus 320×568 with emulated iPhone user agent/safe areas. At each viewport the harness visited all three modes in RU/EN, dark/light and Sans/Serif: **8,560 screen visits in 120 route/configuration traversals** across the final five reports. Each visit checked the actual title and every paragraph against data, mode count, bounds and reachable paragraph tail. There were zero runtime exceptions and zero remote runtime requests.

Interactions checked language/position preservation, Settings, source/contents dialogs, fonts, focus mode, buttons/keys, horizontal swipe versus vertical scroll, desktop rail, final restart, Continue and Start over. All visible top controls fit one labeled icon-only row at 320 px. The iPhone emulation additionally checked a 44 px safe top inset, mobile touch swipe, localized install guide and standalone hiding of its guide/trigger. **This is Chrome emulation, not physical iPhone/Safari or PWA installation certification.**

Actual platform-font records show embedded Geist for Sans, Source Serif 4 for Russian Serif and Geist Serif for English Serif. Serif controls stay Sans and the Settings fallback note remains visible. Visual inspection covered the final-build 320 px RU Serif nurse case, 1440 px resumed cover, 390 px RU final, 1024 px EN immune-mechanism screen and the emulated-iPhone nurse screen. Screenshots' older `quantitative` filename labels refer to that immune-mechanism screen; no unimplemented chart/list/image type is claimed.

The focused preference supplement proves a new document was loaded using `performance.timeOrigin`: global light/Serif, EN and the expanded-book position survive a real same-file reload and Continue. A separately identified synthetic storage event refreshes dark/Sans without paging. Cross-file `file://` preference sharing is browser-dependent and was not certified. No hosted app server was started.

## Progress and preferences

Book progress uses **`book-tiktok.why-zebras-dont-get-ulcers.depth-v2.`**. The harness seeded the old slug's EN/Deep/last-screen keys and verified the candidate still starts freshly in RU/Essential. Old short/other-sequence progress does not silently resume here. A remembered deeper screen is offered with an explicit deeper-mode Continue label in both languages before the reader changes depth. Continue, Start over and final restart were exercised.

Global theme/font use the maintained `bookLibrary.preferences.v1` key. The candidate-local build changes only typographic cover decoration, its progress namespace, explicit deeper Continue copy and RU time inflection. The installed builder, shell, fonts and shared Settings assets were read-only.

Every manually launched Chrome used its own `mktemp -d` profile and `/usr/bin/timeout 30`, a dedicated process group/port, and cleanup in `finally`. All six final browser/preference reports confirm **profile removed and zero remaining owned PIDs**. No Chrome, HMR connection or profile owned by these runs remains.

## Integrity and remaining gate

`qa/metrics-and-integrity.json` binds the current drafts/data/HTML, browser inputs, actual source ranges and protected inputs. Root HTML, old collector, accepted-pilot review/build files and installed shared assets match the recorded protected hashes. No Git/PR/deploy, catalogue/global-ledger write or publication occurred.

Root must personally read the complete resulting RU/EN prose and all cumulative routes, compare coverage and omissions with the work, directly check critical source passages, and record acceptance against exact hashes. Structural/browser passes and this worker's map cannot grant that acceptance. `ready.json` binds the deliverables and retains both acceptance/publication flags as false.
