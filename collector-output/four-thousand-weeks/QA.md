# Four Thousand Weeks — QA and handoff

Date: 2026-10-31. Scope: `collector-output/four-thousand-weeks/` only. No catalogue integration, deployment, shared script edits, existing book edits, or global skill edits. Transient checkout and private workstation paths are deliberately omitted from this public report.

## Claim map and fidelity

The pre-writing map and complete working ledger are in `sources.md`. The argument follows finite life → impossible completeness → efficiency feedback → deliberate omission and commitment → attention and discomfort → uncertain plans and present value → intrinsic leisure → active patience → shared rhythms → ordinary significance → action without guarantees. The Essential reading is a complete version of that argument, including the eighty-year arithmetic anchor, email feedback case, material inequality, unsafe-commitment qualification, intrinsic leisure, shared-time constraints, and final action model.

Core adds examples, mechanisms and practical proposals; Deep adds secondary cases, philosophical detail, qualifications and synthesis. There are **30 level-1**, **42 level-2** and **40 level-3** screens, hence exactly **30 / 72 / 112 cumulative**. Cover and final are level 1. There is one stable ordered corpus; the modes filter it rather than replace it.

All fourteen chapters, the afterword, five final questions, and all ten appendix proposals are represented. Source-sensitive cases include Coutts/Lubbock, Kafka/Felice, the watermelon stream, Young, Setiya, Roberts, Minkkinen, digital nomads and the Swedish vacation study. Historical accounts are labeled as the book's accounts, rather than silently becoming independent evidence. Every screen carries source IDs; `bookLocator` records the EPUB chapter/appendix territory. Provenance totals: **97 book / 3 corroboration / 12 synthesis**, including the cover.

**Seven bibliography entries:** supplied EPUB, publisher, author interview, three primary corroborations, one independent review. Six are attached to screens; the review is a reception cross-check only. The current Russian publisher page identifies a newer edition; it is not represented as the source of the supplied EPUB. Exact local ISBN: **9785961486391**. EN is a translation of this original digest, not a consulted English book edition.

## Counts, words and reading time

| Mode | Screens | RU words, builder | EN words, builder | Estimated RU / EN |
| --- | ---: | ---: | ---: | --- |
| Essential | 30 | 1652 | 1906 | 10 / 9 min |
| Core | 72 | 3977 | 4629 | 23 / 22 min |
| Deep | 112 | 6169 | 7139 | 35 / 33 min |

Builder word counts include titles/subtitles/bodies. Estimates use its unchanged 180 RU / 220 EN words-per-minute assumptions; they are approximate, not promises of comprehension speed.

Body-only density, using Unicode word tokens with internal apostrophes/hyphens:

| Language | Total body words | Mean / screen | Median | Range |
| --- | ---: | ---: | ---: | ---: |
| RU | 5342 | 47.70 | 48 | 41–56 |
| EN | 6177 | 55.15 | 55 | 47–69 |

The audit has a slightly different tokenizer (6166 RU / 7135 EN including titles), not a missing-content discrepancy. No body was split merely to create an extra screen.

## Bilingual checks

- All 112 paired screens preserve their cognitive job, provenance, IDs, levels and sources. These structural fields exist once, shared by RU and EN.
- Reviewed the translations for causal polarity, uncertainty and evidence strength: no guaranteed calm, no literal doubling of life, no clinical efficacy from anecdotes, no individual causality from ecological data, no life-decision prescription from a laboratory choice experiment.
- Deterministic digit-token comparison of every title/body pair found **zero mismatches**, normalizing thousands separators. Spelled quantities were checked during translation.
- EN/RU body word ratios range approximately 1.02–1.33; no translation loses an argument or qualification. English naturally uses more separate words.
- Default RU/dark/Deep; UI, title, labels, disclosures and method switch languages. Position, depth and theme survive switching.

## Build and deterministic audit

Built from schema v2 using the maintained builder, never by copying another book HTML:

```sh
node ~/.codex/skills/book-tiktok/scripts/build_story.mjs \
  collector-output/four-thousand-weeks/story-data.json \
  --out collector-output/four-thousand-weeks/four-thousand-weeks.html
```

The integration maintainer rebuilt the artifact with the current maintained template. Its compact localized home control and focus counter behavior now work without generated-HTML patches. The editable JSON remains the canonical content source.

The artifact then passed the maintained deterministic bilingual audit:

```sh
node ~/.codex/skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/four-thousand-weeks/four-thousand-weeks.html \
  --min-screens 112 --require-bilingual
```

Final audit output (file path abbreviated):

```json
{
  "file": "collector-output/four-thousand-weeks/four-thousand-weeks.html",
  "format": "v2",
  "bytes": 410395,
  "screenCount": 112,
  "levels": {"1": 30, "2": 42, "3": 40},
  "modes": {"essential": 30, "core": 72, "deep": 112},
  "words": {"ru": 6166, "en": 7135},
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

Standalone HTML embeds fonts, CSS, JavaScript and the full corpus. There are no runtime dependencies, fetches, services or remote assets. No book illustration/cover is embedded; the maintained typographic cover uses no copyrighted artwork.

## Bounded real-browser QA

Used installed Google Chrome headless through the DevTools Protocol, opening the actual standalone `file://` HTML. Each invocation used `/usr/bin/timeout 30`, a distinct `mkdtemp` profile and dedicated debugging port. Process-group termination and profile deletion ran in `finally` and exit/signal handlers. No server was started. Temporary harness, screenshots and machine reports were inspected and removed after summarizing them here.

Every viewport traversed **all screens in all three modes**, in **both languages and both themes**: `(30 + 72 + 112) × 2 × 2 = 856` rendered screens per viewport, **3424 total**. At each step checked exact expected title, unique ID sequence, selected-mode counter, source label, rail selection and horizontal overflow. Final restart was tested for each combination.

| CSS viewport | Rendered screens | Max document / content horizontal overflow | Rail | Runtime errors | External requests |
| --- | ---: | --- | --- | ---: | ---: |
| 320×568 | 856 | 0 / 0 px | hidden | 0 | 0 |
| 390×844 | 856 | 0 / 0 px | hidden | 0 | 0 |
| 1024×768 | 856 | 0 / 0 px | visible and scrollable | 0 | 0 |
| 1440×900 | 856 | 0 / 0 px | visible and scrollable | 0 | 0 |

Additional passing checks at all four widths:

- Defaults RU/dark, embedded Geist and Geist Mono availability, counts and metadata.
- Language/theme round trip preserves position; source and contents dialogs open and close; chapter selection closes the dialog.
- A saved Core-only chapter reopened from Essential raises depth automatically to Core. Continue and Start over behave correctly. Final restart clears the saved chapter.
- Back/Next, arrow keys, horizontal pointer swipe, and vertical scroll. A long question list really scrolls on both phone viewports.
- Text tap enters focus and the second tap restores the shell; F enters and Escape exits. Focus persists while paging. Header, progress, desktop rail, Back **and counter** hide; Next remains within the viewport with a minimum 44 px height.
- Vertical pointer movement does not become a page swipe or focus tap. Links/buttons, active text selection and a 600 ms long press do not toggle focus.
- All top controls lie inside the 320 px viewport. Desktop rail is scrollable and its active chapter stays synchronized. Reduced-motion emulation is supported.

Visually inspected screenshots of RU/dark phone and desktop covers; the long five-question list at 320 px and desktop; phone/desktop focus layouts; and EN/light dense mortality prose, comparison, numerical anchor and final. Text remains readable, content scrolls when needed, and the primary action stays available. Image decoding is not applicable: the corpus intentionally has no raster/media assets.

These are emulated Chrome desktop/phone CSS sizes, not physical iOS or Android device testing. The invisible/chosen-depth chapters are not listed in the inherited contents UI; automatic raising was exercised through a saved chapter. The Home control retains the maintained `./` link; catalogue placement is left to the integrator.

During integration, the maintainer rebuilt the root reader from this JSON on the current template and ran the automatic whole-library browser gate across ten readers at 320×568, 390×844 and 1440×900. Catalogue counts, compact home navigation, focus enter/exit, topbar bounds and horizontal overflow passed with zero runtime errors. This supplements rather than replaces the collector's four-viewport matrix above.

## Evidence boundaries and limitations

The private full EPUB was available. Consultation combined a paragraph-level structural survey with close reading of argument-bearing passages and all ten proposals; it was not uninterrupted line-by-line reading. No extracted book text, chapter copy, extended quotation or source images are distributed. The compact English version is not an independently checked translation against an English edition.

This is Burkeman's philosophical synthesis, supported by examples, not a validated universal productivity or therapeutic protocol. Gilbert/Ebert was checked at abstract level; Roberts is a teaching account; Hartig is ecological and correlational, checked through its abstract. None justifies medical guidance or a universally correct commitment rule. Historical and biographical examples were not separately audited against archives. The conditional eighty-year calculation is not a prediction of individual survival. Device changes and contemplative exercises are optional proposals, not established cures.

No deployment, catalogue registration, external delivery, PR or push occurred. Exactly the four requested deliverables are included in the commit.

## File integrity

- `story-data.json` SHA-256: `cab74d85b824a8a32cdde17999341c44b84e80ed2c5fcb695d507a687b17deff`.
- Final HTML SHA-256: `5e0ccd0c34e7a54db09929b1957b7f0630cadaf4b82c1ced968968ecceea52a0`.
