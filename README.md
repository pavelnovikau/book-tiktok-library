# Book TikTok Library

Current2026-11-01: Zebra personally accepted at37/70/107 after complete bilingual retelling reading, shorter-route continuity,18-chapter/68-grouped-case map and45 selected primary passages. Deep13219RU/13988EN body words. Publication pending; six expanded books already live. Irvine, Make Time, Essentialism and Four Thousand Weeks await personal reading. Selfie remains assigned; Behave source coverage incomplete. All62 positions require individual root acceptance. This statement supersedes historical notes below.

Current2026-11-01: Children of Captain Grant PR42 is personally accepted, merged31de7b22 and production-verified at26/69/116,12410RU/14921EN narrative words. Six expanded works are personally accepted/live; production58books/2615screens. Next personal reading: Zebra, Irvine, Make Time, Essentialism. Their worker files are hash-ingested only. Behave actual-primary gaps remain. All62 positions retain individual root acceptance. Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-06-receipt.json. This statement supersedes historical notes below. New Sol max preparation assigned: Four Thousand Weeks and Selfie; separate personal acceptance remains required.

Current2026-11-01: Children of Captain Grant is personally accepted at26/69/116 after complete RU/EN retelling reading, full coverage/omission maps and selected actual primary checks. Deep12410RU/14921EN narrative words; publication being prepared. Five expanded works are live. Next personal reading: Zebra, Irvine, Make Time, Essentialism. Their completion hashes are verified; prose is unaccepted. Behave actual-primary coverage remains incomplete. All62 positions retain individual root acceptance. This statement supersedes historical release notes below.

Current2026-11-01: White Fang PR41 is personally accepted, merged43cb318c and production-verified at36/51/89,8173RU/10071EN narrative words. Five expanded works are personally accepted/live; production58books/2536screens. Next personal reading: Children of Captain Grant, then Zebra, then Irvine. Make Time remains assigned. Other62-position replacements still require separate root acceptance. Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-05-receipt.json.

Current2026-11-01: White Fang is personally accepted at36/51/89 after root reading and chronology/actor/route repairs; publication is being prepared. Four earlier expanded works are live. Next personal reading: Children of Captain Grant, then Zebra, then Irvine. Zebra and Irvine callbacks are hash-ingested only; Make Time remains assigned. Behave source coverage remains incomplete. All62 positions retain individual root reading and acceptance.

Current2026-11-01: Lost World PR40 is personally accepted and production-verified at33/68/125 (8562 RU narrative words). Four expanded works are accepted/live. Production58books/2483screens; White Fang and Children of Captain Grant await root reading. Evidence: editorial-audit/2026-10-31/publisher-findings/expanded-depth-04-receipt.json. This current statement supersedes earlier release notes below.

Current expanded-depth repair,2026-11-01: Lost World personally accepted at33/68/125 (8562 RU narrative words); release being prepared. Three expanded books are already live. White Fang and Children of Captain Grant await personal root reading. See NEXT_STEPS.md.

Current expanded-depth repair, 2026-11-01: Treasure Island PR39 is personally accepted and live (28/48/96; 9,121 RU narrative words). Three expanded works are accepted/live; other positions need separate root reading. Production: 58 books / 2,392 screens. See editorial-audit/2026-10-31/publisher-findings/expanded-depth-03-receipt.json and NEXT_STEPS.md.

Current depth repair,2026-11-01: expanded Kahneman is personally accepted and live throughPR38 (27/74/110;9694RU body words). Together with Hard to Be a God, two expanded works are accepted; other positions require separate personal review. Production58books/2330screens. See editorial-audit/2026-10-31/publisher-findings/expanded-depth-02-receipt.json and NEXT_STEPS.md.

Public, contribution-friendly library of dense standalone book stories. Each book is a single bilingual HTML file with nested reading depths and light/dark themes based on [Flexoki by Steph Ango](https://stephango.com/flexoki).

Live site: https://book-tiktok-library.vercel.app

Git hosting: https://github.com/pavelnovikau/book-tiktok-library

Vercel project: `pavelnovikaus-projects/book-tiktok-library`. A merge to `main` is the production release path; pull requests are the contribution path.

Current repair authority: [the personal depth-review plan](editorial-audit/2026-10-31/depth-v2/PLAN.md) and [NEXT_STEPS.md](NEXT_STEPS.md). A historical factual PASS does not establish sufficient maximum reading depth. The first personally accepted expanded story is [Hard to Be a God](editorial-audit/2026-10-31/depth-v2/hard-to-be-a-god/root-review/personal-review.md), published through PR37.

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
