# Book TikTok Library

Public, contribution-friendly library of dense standalone book stories. Each book is a single bilingual HTML file with nested reading depths and light/dark themes based on [Flexoki by Steph Ango](https://stephango.com/flexoki).

Live site: https://book-tiktok-library.vercel.app

Git hosting: https://github.com/pavelnovikau/book-tiktok-library

Vercel project: `pavelnovikaus-projects/book-tiktok-library`. A merge to `main` is the production release path; pull requests are the contribution path.

## How it works

- `books.json` is the catalogue. Its additive `discovery.version: 1` extension separates work types, fiction genres, nonfiction subjects and bilingual topic names/aliases. Legacy schema-2 sections, collections and audience/spoiler metadata remain available internally.
- `index.html` builds one common catalogue with search, All / Fiction / Nonfiction and one native genre/subject selector. Cards and book/screen/topic counters come from the manifest. Every card has its own thesis-driven inline SVG motif and Flexoki tone declared in `books.json`; the validator rejects repeated motifs.
- Every book remains a standalone HTML file and can be opened without the library shell.
- `manifest.webmanifest` and `sw.js` let the site run as an iOS/Android Home Screen app. The shell and catalogue are cached immediately; book HTML is cached after it is opened.
- `scripts/apply-reader-shell.mjs` adds shared focus mode, optional PWA metadata and the maintained compact icon header to registered books. The header and optional iOS guide share one row; localized tooltips and accessibility labels explain the icons. Focus mode toggles by tapping non-interactive text; only reading content and Next remain.
- A push to `main` builds the public allowlist and deploys it through Vercel. Pull requests run validation and can receive Vercel previews.

## Add a book

External contributors can fork the repository and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact contract.
The historical expansion is tracked in [BOOK_PLAN.md](BOOK_PLAN.md); it is suspended during the active repair. The current handoff is [NEXT_STEPS.md](NEXT_STEPS.md).

The complete reusable Codex skill lives in [`skills/book-tiktok`](skills/book-tiktok). It includes the research/content contract, portable RU/EN reader template, embedded Geist fonts, example story data, builder and deterministic auditor. To install it, ask Codex to install the skill from:

```text
https://github.com/pavelnovikau/book-tiktok-library/tree/main/skills/book-tiktok
```

Then invoke it as `$book-tiktok`. Keep the whole folder together; the scripts resolve templates and fonts relative to `SKILL.md` and contain no machine-specific paths.

```bash
npm run check
npm run sync:readers
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Finding a book

Search works in either UI language across both RU/EN titles, authors, descriptions, localized genres/subjects and the controlled topic vocabulary. Words combine with AND; word prefixes match, punctuation and Russian е/ё are normalized, and short terms such as AI / ИИ match whole words. For example, `фантастика`, `стоицизм`, `sci-fi` and `Sapolsky` work in both interfaces.

Type, genre/subject and query compose with AND. Type counts respect the current query and genre/subject; selector counts respect the current type and query. Only options used by books of the current type are offered, except that an active zero-count option stays visible when switching type. Clear all returns to the complete catalogue and clears the URL filters. A book with several matching tags appears once. Hybrid works can have both work types: Pirsig is explicitly presented as a philosophical novel and is discoverable through fiction and philosophy. Type totals can therefore overlap; All always counts distinct books. Audience is never a work-type or navigation rule.

Share current filters with `?type=fiction&topic=adventure&q=Verne` (omit defaults). Existing `section` links map to their corresponding new subject, and `section=fiction-adventure` opens Fiction. Former collections map to visible controls: `for-son` → Fiction, `taleb` / `sapolsky` → author search, `practices` → Nonfiction, `unassigned` → All. A notice explains that the link has been updated; these are new discovery views, not hidden historical subsets. The mappings live in `books.json` and old parameters are replaced by the canonical visible filters. Unknown filters are cleared with a notice. Language/theme preferences retain their existing storage key; standalone reader progress and URLs are unchanged.

`npm run qa:browser` runs real Chrome in separate short phases for discovery, reader layouts, focus/keyboard, iOS-install/safe-area emulation and revised-reader traversal. Each phase owns a temporary profile and a Chrome process group limited to 30 seconds. Reports and screenshots are saved outside the repository; set `BOOK_LIBRARY_QA_DIR` to choose that directory. This is browser emulation, not a physical iPhone test.

## 2026-10-31 editorial repair — release 08

Seven sealed narrative readers contain **274 RU/EN pairs**: Howl’s Moving Castle 15/25/39, Northern Lights 17/22/43, Ender’s Game 16/25/39, To Kill a Mockingbird 14/28/41, The Hobbit 15/23/35, Holes 14/23/39 and Have Space Suit—Will Travel 17/25/38. Six additions and one replacement yield **53 books / 2,206 screens**; the other 46 readers and catalogue entries remain byte-identical. Flowers and Dune are excluded from this release.

[Localized publisher acceptance](editorial-audit/2026-10-31/publisher-findings/release-08-localized-acceptance.json) closes five required findings across four books. Reversing only the recorded edits reproduces all four originally reviewed authoring **and HTML** hashes; the original REQUIRES-FIXES reviews remain unchanged. Hobbit, Holes and Heinlein carry fresh matching independent PASS. Source boundaries remain selective: publisher samples, identified substantial guides and selected author passages. Hobbit’s specific Oxford-supported causal link remains explicitly credited to the independent reviewer. The publisher separately accessed the DBE passages for the narrowed Mockingbird cover; the parent’s earlier timeout remains recorded. No continuous complete-edition or published-translation certificate is claimed.

Reviewed custom HTML is ported without rebuilding its corpus, then synchronized with the maintained Settings/header/offline-font shell. All seven preserve actual source maps and a global Sources dialog while narrative screens hide provenance chrome. Removed/cover saved IDs fall back to Essential; retained Hobbit IDs resume through current consent, and old session approval cannot reopen Deep. Howl’s root now also revokes ending consent when depth is lowered. Six distinct semantic cover motifs and bilingual story descriptions integrate the additions with existing discovery and the unchanged statistics strip/equal tabs.

The [release08 receipt](editorial-audit/2026-10-31/publisher-findings/release-08.json) binds exact inputs/roots, reading times and release state. Focused verification covers 7×69 structural assertions, Settings/platform fonts/native radio isolation including Hermes, actual corrected copy, Sources/progress/swipe, focus, consent cancel/accept/reload/downgrade, old/current Hobbit IDs, dense 320/390/desktop tails, safe-area emulation, discovery and offline standalone use. [Proof](editorial-audit/2026-10-31/publisher-findings/release-08-proof/) includes harness diagnostics separately from product changes. The public allowlist contains 64 assets; collector/audit/private/source trees are excluded. Physical iPhone/Safari/PWA testing is not claimed.

Release07 is now separately [production verified](editorial-audit/2026-10-31/publisher-findings/release-07-production-verification.json): 58 actual HTTP200 hashes match accepted head `2fbd3f5…`, twelve revised live readers work in RU/EN at320, native PHM consent/resume/reload/downgrade and Giver/Earthsea custom consent pass, private/source probes return404. Its original pending receipts remain preserved. Release08 is live only when its own exact-head merge and production verification are recorded.

## 2026-10-31 editorial repair — release 07

The sealed release accepts **12 readers / 334 RU/EN pairs**: Kahneman, Meadows, Behave, Determined, Project Hail Mary, The Giver, Ostrom, Earthsea, the Goldratt corpus, 1873, Kuhn and Scott. Seven additions and five replacements yield **47 books / 2,076 screens**. The other 35 roots and catalogue entries remain byte-identical. Heinlein arrived after seal and is queued for the next publisher.

[Fresh localized acceptance](editorial-audit/2026-10-31/publisher-findings/release-07-localized-acceptance.json) closes 14 findings against current hashes; reversing only the recorded changes reproduces all 10 originally reviewed authoring hashes. Those original REQUIRES-FIXES reviews remain unchanged. Kuhn/Scott retain matching-hash independent PASS. Source limits remain explicit: selective/excerpt-supported scope, identified secondary PHM later-action evidence, original reviewer’s actual Mindscape reading after publisher repeat timeout, separate Kuhn editions/printings, and Scott’s inaccessible nonessential bibliography record.

The [release07 receipt](editorial-audit/2026-10-31/publisher-findings/release-07.json) binds inputs, roots, counts, reading times and publication state. Exact corpora, source maps, custom narrative covers/consent and the accepted Settings/offline Geist module are retained. 1873/TOC migrate actual old storage safely; removed IDs return to Essential cover and restart cannot resurrect old progress. PHM gains renewed document-local Deep consent. Exact title/category queries avoid new token collisions; the prior Russian Determined title remains searchable. The public build allows 58 assets only.

Validation: 12×69 structural assertions, unchanged reviewed-content reconstruction, full effective-corpus/source parity, idempotent shell, targeted Settings/platform-font/state/native-key/cold-font checks, offline reading, RU/EN fiction consent/cancel/reload, dense mobile tails, focus/safe-area and discovery/new-title searches. [Focused proof](editorial-audit/2026-10-31/publisher-findings/release-07-proof/) does not certify physical iPhone/Safari/PWA or complete editions. This receipt’s merge/production evidence determines deployment; no live claim follows from local tests.

## 2026-10-31 editorial repair — release 06

Accepted content: *Atomic Habits* 13/20/24, *Protocols · sleep, light and attention* 10/16/22 and *Hermes & Nous · research brief* 12/17/22 — 68 RU/EN pairs, intended **40 books / 2,327 screens**. Three completed independent PASS reviews bind the unchanged canonical packages. Clear is a concise central-method account from actual author/publisher excerpts; Huberman is selected reading of the introduction, Sleep1–3 and PersonalGrowth1 with medical qualifications; Hermes preserves its public core and conditional proposals, with two underlying internal documents still inaccessible. Neither complete-edition fidelity nor validated demand/implementation is claimed.

Settings [PR29](https://github.com/pavelnovikau/book-tiktok-library/pull/29) merged first after fresh independent R1/R2 closure at `a976d547…`, all three checks green. All50 actual production hashes match UI merge `7e1f96f…`; cold font/scroll and native radio regressions also pass live. This content branch preserves that UI across all40 readers. Exact accepted HTML is synchronized without rebuilding its corpus; the other37 roots/entries are unchanged. Hermes legacy keys/removed IDs migrate safely and cannot resurrect after restart. Atomic Habits has a unique four-stage habit-cycle cover motif.

The [release06 receipt](editorial-audit/2026-10-31/publisher-findings/release-06.json) binds inputs/roots and exact publication state. Local checks pass 3×69 structure,2,496 rendered positions with reachable tails, source/state/migration/consent preservation, portable/Settings/font persistence, discovery/stats/equal tabs, safe-area/focus and offline reading. The public build contains51 allowlisted assets only. Actual40-book deployment is claimed only after its own merge and production proof. Kahneman/Meadows arrived after sealing and remain for the next publisher.

[Release05 final verification](editorial-audit/2026-10-31/publisher-findings/release-05-verification.json) preserves its original evidence and confirms all50 assets,39 books/2,453 screens, live Sources/progress/renewed ending consent, all56 quotation displays and six private404 responses. See [fresh UI closure](editorial-audit/2026-10-31/publisher-findings/release-06-ui29-closure.json) for the distinct a976d547 acceptance; the original a09d38dc REQUIRES-FIXES report is unchanged. No physical iPhone/Safari/PWA/BFCache certification.

## 2026-10-31 editorial repair — release 05

Three accepted readers contain 98 RU/EN pairs: *Meditations* 18/30/39, *Antifragile* 11/17/24 and *The Left Hand of Darkness* 11/15/35. The intended catalogue is **39 books / 2,453 screens**. Antifragile replaces the old 144-screen analytical reader; the other two titles are newly registered. The remaining 36 readers and their catalogue entries are unchanged.

Meditations and Antifragile match completed independent PASS hashes. Meditations preserves all fourteen paired quotations, translators and book/section attributions, the XII.36 = Rogovin XII.35 concordance, and its embedded 1914 archival title leaf. Antifragile retains a selected central argument supported by author Chapter 1, interview, essay, draft and explicitly later explanations; it does not claim every chapter or offer medical or investment prescriptions. Left Hand’s original REQUIRES-FIXES review remains intact: four bounded publisher closures remove unsupported details, distinguish interrogation drugs, and restore Estraven’s stated political explanation. Guides and references remain labelled as such; no new primary-novel or full-edition reading is claimed.

Accepted collector HTML is integrated without plain rebuilding. Bespoke covers, quotation objects, content modes and source maps remain exact. Valid saved IDs survive; unavailable IDs return to the cover safely. Left Hand renews Deep consent on reload and hides saved ending titles. Catalogue motifs show a common city and two tracks across ice; Antifragile keeps its unique convex-response motif. Statistics, equal tabs, inset-safe icons and offline reading remain.

The [release05 receipt](editorial-audit/2026-10-31/publisher-findings/release-05.json) binds exact inputs and roots. Focused checks cover 3×69 structural assertions, 3,200 rendering visits, 56 quotation displays with attribution and reachable final lines, corrected-copy reachability, source scope/progress/restart/consent, focus, discovery, safe-area and offline reading. Public output contains 50 allowlisted assets only. Browser emulation is not a physical-iPhone/Safari/PWA test. Publication is established only by an exact-head merge and actual production verification; this integration does not claim 39 live.

Release04 is now [production-verified](editorial-audit/2026-10-31/publisher-findings/release-04-verification.json): all 48 served asset hashes match merge `be5b08c`, 37 books/2,499 screens, all four relevant readers pass live source/state/consent/corrected-copy checks, and private paths return 404. Its previous pending handoff is preserved separately. Root retains coordination of Settings PR29; its unmerged UI and installed skills are outside this release.

## 2026-10-31 editorial repair — release 04

Four new readers add 146 RU/EN pairs: *Hard to Be a God* 8/13/33, *Adventures of Huckleberry Finn* 24/36/54, *Nonviolent Communication* 16/26/30 and *The Fifth Discipline* 11/22/29. The catalogue contains **37 books / 2,499 screens**. All previous 33 reader files are byte-identical to release03.

Huck and Senge match completed independent PASS reviews. HardGod's sole remaining HG-06 detail and NVC's two meaning/role findings are explicitly closed against the cited primary passages; their original REQUIRES-FIXES reviews remain unchanged. [The receipt](editorial-audit/2026-10-31/publisher-findings/release-04.json) binds accepted input/root hashes, actual source boundaries and publication state. These are concise supported accounts, without full-edition or published-translation certification. NVC retains the selected central-method scope; Senge distinguishes the official sample from his separately consulted article and beer-game evidence.

The accepted collector runtime, source maps, Sources dialog and bespoke presentation remain intact. Huck keeps its custom consent dialog; HardGod gains document-local consent for Deep and saved endings. Every new reader preserves valid stable progress and discards unavailable IDs. Four distinct catalogue motifs and controlled genres/subjects describe the actual stories or methods. Long card titles wrap at phone width. Statistics, equal tabs and the compact safe-area icon row remain.

Validation covers 4 × 69 structural checks, 4,832 rendering visits, RU/EN Sources/progress/restart, native/custom consent including Huck Escape/downgrade, focus/swipe, safe-area, and offline PWA/standalone reading. The public allowlist has 48 assets; collector/audit/private/full-text trees are excluded. Browser emulation is not a physical-iPhone/PWA test. Settings PR29 remains separate; Meditations arrived after this batch sealed and is not included. Actual production is claimed only when the receipt records its successful HTTP and interaction verification.

## 2026-10-31 editorial repair — release 03

Eleven reader revisions are accepted: four match completed independent PASS hashes; seven close nine required local findings against the actual primary passages. The original REQUIRES-FIXES reviews remain unchanged, with explicit replacement-hash acceptance in the [release03 receipt](editorial-audit/2026-10-31/publisher-findings/release-03.json). These are condensed stories/arguments, with source scope and edition limits preserved. There are 457 revised RU/EN pairs: 274 narrative pairs and 183 explanatory pairs.

| Accepted reader | Essential / Core / Deep | RU minutes | EN minutes |
| --- | ---: | ---: | ---: |
| Awareness Through Movement | 19 / 35 / 42 | 6 / 10 / 12 | 5 / 10 / 11 |
| Zen and the Art of Motorcycle Maintenance | 20 / 38 / 52 | 7 / 12 / 17 | 6 / 12 / 16 |
| Letting Go: The Pathway of Surrender | 16 / 32 / 39 | 5 / 9 / 11 | 5 / 9 / 11 |
| Make Time — Jake Knapp and John Zeratsky | 19 / 39 / 51 | 6 / 11 / 14 | 5 / 10 / 13 |
| Monday Begins on Saturday | 11 / 17 / 29 | 3 / 5 / 8 | 3 / 5 / 8 |
| Accelerando | 14 / 26 / 52 | 4 / 8 / 15 | 4 / 8 / 15 |
| Why Zebras Don't Get Ulcers | 25 / 42 / 51 | 7 / 12 / 15 | 7 / 11 / 13 |
| The Lost World | 13 / 23 / 34 | 4 / 6 / 9 | 4 / 6 / 9 |
| Treasure Island · Robert Louis Stevenson | 12 / 20 / 34 | 4 / 6 / 9 | 4 / 6 / 9 |
| White Fang — Jack London | 14 / 21 / 36 | 4 / 6 / 10 | 4 / 6 / 9 |
| The Children of Captain Grant | 14 / 23 / 37 | 4 / 7 / 10 | 4 / 6 / 10 |

The catalogue now contains **33 books / 2,353 screens**. Monday is newly registered under the existing fiction/fantasy/science-fiction vocabulary, with bilingual author, general audience, full-plot-in-deep policy and a distinct enchanted-lab cover. No age shelf or extra header row is added. Seven spoiler-bearing readers start a fresh document at Essential; explicit consent protects both Deep selection and saved ending resumption. Accelerando retains its custom cover and modal runtime. All eleven discard removed saved IDs and retain valid stable progress. The other 22 root readers are byte-identical to base main.

Validation: library/portable-skill checks, 11 × 69 bilingual structural checks, 15,200 RU/EN/light/dark/depth/width rendering visits, Sources, progress, native/custom consent, phone safe-area/focus/swipe, standalone and cached offline reading. Browser emulation is not a physical iPhone/PWA test. The public allowlist contains 44 files; collector, audit, private, research and skill trees are excluded. Hard to Be a God remains excluded pending independent repair review. Settings and font selection are a separate UI feature, absent from this book release.

Release02 has now been verified against actual production: all 43 assets match merge 87fc7638933a0187ab650d45fadfeacaeaf0242f, all six readers pass live source/progress/consent interaction checks, and the catalogue serves 32 books / 3,168 screens. Its [receipt](editorial-audit/2026-10-31/publisher-findings/release-02.json) retains the old pending observation and pre-release evidence. Release03 publication is established only by its own PR/check/merge and production evidence, not by this local acceptance.

## 2026-10-31 editorial repair — release 02

This release accepts five nonfiction revisions from hash-matched independent PASS reviews (221 RU/EN pairs) and the first repaired fiction narrative, *Amphibian Man* (35 pairs). Its full 35-pair independent review required only two causal corrections; the reviewer has now rechecked both and issued a matching-hash PASS. Fresh publisher passage checks accept both: pain/suffocation causes the leap, and Guttiere remains unseen to avoid drawing Ichthyander back onto dangerous land. Reverting just those two screen objects reproduces the exact reviewed authoring hash; the other 33 pairs and metadata are unchanged.

| Accepted reader | Essential / Core / Deep | RU minutes | EN minutes |
| --- | ---: | ---: | ---: |
| Four Thousand Weeks | 21 / 32 / 52 | 6 / 10 / 15 | 6 / 9 / 14 |
| Mindfulness | 14 / 26 / 30 | 4 / 8 / 9 | 4 / 7 / 8 |
| A Guide to the Good Life | 18 / 32 / 36 | 5 / 9 / 10 | 5 / 8 / 9 |
| The Body Keeps the Score | 21 / 33 / 41 | 7 / 10 / 12 | 6 / 9 / 11 |
| Amphibian Man | 12 / 19 / 35 | 4 / 6 / 10 | 4 / 5 / 10 |
| Selfie | 27 / 39 / 62 | 8 / 11 / 16 | 7 / 10 / 16 |

The integrated catalogue has **32 books / 3,168 screens**. Together with release 01, nine books have accepted repairs; the other 23 published books retain unestablished editorial status. No other pending candidate or late 1873/TOC repair is included. Primary reading boundaries, source links, author attribution and `contentMode` remain exact. Nonfiction source checks do not certify every underlying clinical claim or whole-edition fidelity.

Amphibian Man has a distinct sea/air cover, existing controlled science-fiction/adventure discovery, internal `teen-14-plus` audience and `full-plot-in-deep` policy. No age shelf or extra header row is introduced. Narrative screens hide per-screen source footers, while the global Sources dialog and embedded mappings remain. A document-local ending-consent guard covers both the depth picker and saved Deep continuation, resets on reload, and keeps ending titles out of lower-depth contents and resume labels. Removed saved IDs are discarded; valid stable IDs remain resumable. The compact icon row, safe-area protection, equal homepage tabs and statistics strip are preserved.

[Release 02 receipt and source acceptance](editorial-audit/2026-10-31/publisher-findings/release-02.json) records exact input/root hashes, local checks and the actual merge/production state. Publication is established only by that receipt's production evidence. The public build allowlist remains unchanged in scope: registered readers, catalogue/PWA shell, fonts and icons only. No private primary text, collector package, audit or research folder is deployed.

The 41-record baseline and previous release evidence below remain historical. Legacy standalone-auditor limitations for 1873, Theory of Constraints and Hermes/Nous are unchanged. Browser emulation is not a physical iPhone/PWA test.

## 2026-10-31 editorial repair — release 01

The baseline has **41 records under audit**: 31 published works, nine structured unpublished packages and source-only Project Hail Mary. Earlier technical/cold-review approvals followed an analytical-companion brief and do not establish the requested fidelity. The expansion/refill queue remains suspended. [The current brief](editorial-audit/2026-10-31/BRIEF.md) authorizes ten repair workers and one publisher, with immediate publication only after independent checks.

This release independently reads and accepts exactly **three rewritten nonfiction readers, 125 RU/EN pairs**. No fiction story is editorially repaired by this release. The catalogue remains **31 books / 3,504 screens**; the other 28 published books retain unestablished editorial status. Earthsea receives only a saved-depth consent guard, and The Hobbit only RU `o-settlement` «Такой послевкусие» → «Такое послевкусие»; neither is a literary rebuild. The other 27 embedded corpora are unchanged. All 31 receive the shared header correction.

| Rewritten, independently accepted and published | Essential / Core / Deep | RU minutes | Source boundary |
| --- | ---: | ---: | --- |
| The Art of War | 15 / 30 / 36 | 4 / 8 / 10 | Giles 1910 thirteen-chapter base text; no Chinese/manuscript certification |
| Essentialism | 18 / 28 / 36 | 5 / 8 / 10 | Complete owned Russian edition, targeted argument/case reading; not every paragraph |
| Skin in the Game | 19 / 37 / 53 | 5 / 10 / 14 | Complete owned Russian edition, targeted passages plus final chapter/epilogue; not whole-edition line-by-line verification |

Published through [PR #25](https://github.com/pavelnovikau/book-tiktok-library/pull/25), code head `738363c7666b7808aca08acb819108559f19536a`, squash `1e8f9d4d4699c832a4f43b8da35c2a1d21750e22`. All three checks passed; no review findings. At 2026-10-31T19:12:09.062835+00:00, production HTTP matched all **35/35** intended files (homepage, catalogue, PWA files and all 31 readers). Collector, audit and skill paths returned 404. A separate production browser check confirmed 31 cards / 3,504 screens, equal 320/390 RU/EN tabs, five relevant reader routes, safe-area header placement and Sources for all three rewrites, with zero runtime errors. [The hash receipt](editorial-audit/2026-10-31/publisher-findings/production-http.json) is deployment proof, not whole-library editorial approval. Group 2’s three fantasy books remain REBUILD/SOURCE-GAP; the two bounded fixes do not change that status.

Per-book publisher findings live in [publisher-findings](editorial-audit/2026-10-31/publisher-findings/); the release receipt distinguishes integration, merge and production verification. Public sources remain available in each reader. Private/full book text is excluded from the repository. Worker source blockers already reported for I, Robot, The Two Captains, Dune and A Fall of Moondust require lawful primary coverage; no replacement narrative is certified from their excerpts or reviews. Further worker results belong to a subsequent publishing batch.

The skill now chooses narrative, explanatory or practical/hybrid writing from the actual book: prose first, segmentation afterwards, exact counts from justified content, no mandatory lesson or count-confirmation gate. Optional `contentMode` supports narrative/explanatory presentation; no unchanged analytical fiction was relabelled. Narrative reading hides per-screen provenance chrome while keeping source maps and the global Sources dialog. Installed-skill changes were mirrored file by file after comparing for unrelated differences.

Homepage tabs now have equal widths, RU/EN labels wrap, and the statistics strip remains. The compact icon-only header reserves the iOS status safe area, which the previous flat-padding override discarded. Normal/focus/standalone/scroll checks use actual engine safe-area overrides; physical-device behavior remains untested. The synchronizer shares the same module with new builds and preserves legacy readers and book-specific spoiler controls.

`npm run build:site` emits an explicit public allowlist: catalogue/PWA shell, registered root readers, fonts and icons. Vercel serves that output only. Collector, audit, skill and source directories are never deployment assets. The original external baseline ZIP and its manifest retain 195 files and are not overwritten.

Validation includes the library/package check, skill validation, exact root/canonical parity, idempotent shell synchronization, discovery/mobile/legacy/focus/iOS checks and full revised-reader traversal. The v2 auditor passes 69 checks for each rewritten root. Its standalone audit still has pre-existing compatibility failures for legacy 1873 metadata, orphan TOC corpus in Theory of Constraints, and Hermes/Nous detection; the library validator/browser checks pass those readers. Those legacy editorial/structural issues are not claimed repaired here. Reports/screenshots remain outside Git at `/tmp/book-publisher-qa-20261031/`.

## Repository policy

This repository accepts original-word condensed narratives, explanations and lawfully reusable material. Do not submit pirated book text, copied chapters or fabricated quotations and page references. Existing book content is not placed under an open-content licence merely by being public; contributors must state the rights to their own submission.
