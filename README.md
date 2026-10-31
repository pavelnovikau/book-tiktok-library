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
- A push to `main` deploys the production site through Vercel. Pull requests run validation and can receive Vercel previews.

## Add a book

External contributors can fork the repository and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact contract.
The approved 58-title expansion is tracked in [BOOK_PLAN.md](BOOK_PLAN.md); the current handoff is [NEXT_STEPS.md](NEXT_STEPS.md).

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

`npm run qa:browser` runs real Chrome in separate short phases for discovery, reader layouts, focus/keyboard and iOS-install emulation. Each phase owns a temporary profile and a Chrome process group limited to 30 seconds. Reports and screenshots are saved outside the repository; set `BOOK_LIBRARY_QA_DIR` to choose that directory. This is browser emulation, not a physical iPhone test.

## 2026-10-31 release verification

Production is verified at **31 books / 3,673 screens**, adding exactly these five reviewed and repaired books to the previous 26 / 3,129. [PR #23](https://github.com/pavelnovikau/book-tiktok-library/pull/23) was squash-merged as `49ab18f1f4ca3a82392b2ad3aad6c2630e314758` with all three checks green and no review findings. At 18:01 UTC on 2026-10-31, production HTTP reads matched the catalogue, homepage and five reader files byte-for-byte. A separate production browser check rendered all 31 distinct cards, checked the counters and universal controls, opened all five routes and their Home links, and verified Hitchhiker consent/Cancel. Zero runtime errors. The existing `.html` links correctly redirect to their clean reader routes. This is deployment proof after merge.

| Book | Essential / Core / Deep | RU minutes | Listed sources |
| --- | ---: | ---: | ---: |
| White Fang | 24 / 60 / 96 | 7 / 18 / 29 | 6 |
| I, Robot | 30 / 72 / 112 | 10 / 23 / 36 | 17 |
| The Two Captains | 36 / 90 / 144 | 11 / 27 / 42 | 11 |
| The Wee Free Men | 24 / 60 / 96 | 8 / 18 / 29 | 13 |
| The Hitchhiker’s Guide to the Galaxy | 24 / 60 / 96 | 7 / 17 / 27 | 8 |

All five received independent full-pair cold reviews and the required parent repairs. Each root copy passed a fresh 68-check audit at its exact Deep total and has exact structured-data parity with its canonical collector package. The I, Robot list includes ten reviews by one critic; source totals do not imply independent witnesses. Access boundaries remain in each `sources.md` and the reader's method note. These checks do not claim new full-book reading or repeat the historical collector-wide matrices.

Fresh integration QA passed all 31 readers, 120 filter cases, 116 bilingual searches, 13 legacy routes, five homepage widths in both languages/themes, reader layouts, keyboard/focus and iOS browser/standalone behavior. Targeted root checks passed 64 saved-Deep resume states, 72 repaired-screen states, 40 localized source panels and 96 Hitchhiker consent actions. Additional iOS emulation checked all 31 readers at 320/390: 372 control hit tests, 124 actual Language clicks and 62 guide openings. No runtime errors, external reader requests or horizontal overflow were found. Representative homepage, new covers, repaired screens, safe Continue and focus screenshots were inspected.

The synchronizer is idempotent on all 31 readers. Canonical and installed templates use RU «Обзор» and safe fictional Deep-resume labels; the synchronizer propagates them to registered readers. Hitchhiker retains its local «Критика» label, generic Continue, session Core/Deep consent, Cancel/Escape behavior, Essential after reload, focus cover/source rules, reduced motion and static iOS control. Its main reader script remains byte-identical to the reviewed/repaired collector HTML. Copy its current HTML before shell synchronization; a plain rebuild discards those local features.

Evidence for this run is outside git at `/tmp/book-library-release-20261031/`. Existing 26 catalogue records and embedded corpora are unchanged. The five canonical four-file packages retain their ledgers; no other queued collector output is included. The latest authorized pipeline concurrency is ten workers, with one exclusive owner for shared release files.

## Repository policy

This repository accepts original analytical digests and lawfully reusable material. Do not submit pirated book text, copied chapters or fabricated quotations and page references. Existing book content is not placed under an open-content licence merely by being public; contributors must state the rights to their own submission.
