# Selfie — final QA

Date: 2026-10-31. Isolated checkout: `/Users/pn/.t3/worktrees/smartcat/t3-a55de819/_artifacts/book-tiktok-library`; branch `collector/selfie`, cloned from the requested library. Only this book's `collector-output/selfie/` deliverables are committed. No catalogue, existing book, shared script, manifest, service worker or deployment was changed. No publication or external delivery occurred.

## Contract and corpus

| Item | Result |
|---|---|
| Schema | v2 |
| Essential / Core / Deep | **30 / 72 / 112**, cumulative, exact |
| Level 1 / 2 / 3 additions | 30 / 42 / 40 |
| Cover and final | One each; both level 1; included in counts |
| Nesting | Essential ⊂ Core ⊂ Deep, preserving order and IDs |
| Languages | RU primary/default; complete EN copy for every screen, source note, method and media credit |
| Defaults | Russian / dark / Deep |
| Provenance | 101 book / 6 corroboration / 5 synthesis; includes explicit cover label |
| Sources | **10**, including the supplied EPUB, publisher, substantive author interview, scientific sources and independent review |
| Media | One cover, embedded from the supplied EPUB; no remote media |
| Runtime dependencies | None; embedded CSS, JS, Geist, Geist Mono, cover and corpus |
| Standalone HTML | `selfie.html`, 664,398 bytes |

Reading estimates use the maintained builder's 180 RU / 220 EN words per minute, rounded up. They are reading-time estimates, not measured user sessions.

| Mode | RU words | EN words | RU minutes | EN minutes |
|---|---:|---:|---:|---:|
| Essential | 1,475 | 1,783 | 9 | 9 |
| Core | 3,508 | 4,260 | 20 | 20 |
| Deep | 5,451 | 6,593 | 31 | 30 |

Body density: RU mean 41.97 words, range 33–58; EN mean 50.53, range 44–67. Stable shared IDs, level, provenance, media and source references ensure structural parity. All screen-body numerical anchors were compared automatically across RU/EN after normalizing thousand separators: PASS, 112/112. Copy was checked for matching causal qualifiers and evidence boundaries. Translation length differs because natural English uses more separate words; no language contains an extra screen or an omitted argument.

## Build and deterministic audit

Commands, run from the isolated library checkout:

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs \
  collector-output/selfie/story-data.json \
  --out collector-output/selfie/selfie.html
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/selfie/selfie.html --min-screens 112 --require-bilingual
```

Final audit output (file path shortened only here):

```json
{
  "file": "collector-output/selfie/selfie.html",
  "format": "v2",
  "bytes": 664398,
  "screenCount": 112,
  "levels": { "1": 30, "2": 42, "3": 40 },
  "modes": { "essential": 30, "core": 72, "deep": 112 },
  "words": { "ru": 5440, "en": 6582 },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

**PASS: 68 checks, zero warnings, zero failures.** Audit word counts exclude the cover subtitle; the builder's mode word counts above include it. This explains the 11-word difference for each full-language total.

Maintained tool SHA-256 at build:

- `build_story.mjs`: `c88078eb41ae3d63bfd05e3a94834f2bc960f554ce3736965f3467398c44f88d`
- `audit_story_html.mjs`: `9c65e6f399e622280380ea554d0c3a1ffc5806fecab828da9d2079d4a4529d68`

No maintained builder, template or audit source was edited.

## Real-browser QA

Used Playwright with installed Google Chrome, loading the final HTML directly via `file://`; no server or collaborative preview. Each browser run used its own temporary profile and `timeout 30`; contexts closed and profiles removed in `finally`. No Chrome processes or profiles from this task remain.

Every mode was traversed through rendered navigation controls in both languages and both themes at each viewport. Assertions checked expected localized title, exact position/count, uniqueness, provenance presence and absence of document/slide/title horizontal overflow.

| Viewport | Languages × themes × modes | Screen checks | Runtime errors | External requests | Horizontal overflow |
|---|---:|---:|---:|---:|---:|
| 320×568 | 2 × 2 × 3 | 856 | 0 | 0 | 0 |
| 390×844 | 2 × 2 × 3 | 856 | 0 | 0 | 0 |
| 1024×768 | 2 × 2 × 3 | 856 | 0 | 0 | 0 |
| 1440×900 | 2 × 2 × 3 | 856 | 0 | 0 | 0 |
| Total | 48 traversals | **3,424** | **0** | **0** | **0** |

Additional checks passed on all four sizes:

- Initial language RU and theme dark; embedded cover decoded (natural width 1281 px); both embedded font faces loaded.
- Language switch preserved screen ID and depth; theme toggle worked.
- Sources dialog opened/closed and contained exactly 10 entries; Chapters dialog opened/closed.
- All top controls remained within viewport in RU and EN at 320 px.
- Arrow, Page and Space keys; forward/back buttons; horizontal pointer swipe; vertical gesture did not navigate.
- Reload offered Continue; resuming preserved the saved ID. Start over returned to the first reading screen.
- A saved Deep-only screen resumed from Essential raised the depth to Deep.
- Final restart returned to the cover and cleared saved position.
- At 1024 and 1440 px the chapter rail was visible, scrollable, and its active item was kept in view.

Representative screenshots were inspected: dark RU phone cover, quantitative evidence card, long methodology prose, question list, desktop comparison and final; light EN phone revised-authenticity card and comparison, tablet cover and desktop comparison. One initially overflowing Russian title was shortened without changing the claim, then all layouts were rerun. Long phone cover/evidence screens use the shell's vertical scrolling; there is no lost text. Temporary screenshots and QA scripts were removed after inspection.

## Fidelity and evidence audit

The claim map and source ledger preceded screen writing. All eight numbered parts, including zero, remain represented. Essential is a complete argument rather than selected tips: painful ideal → social self → cultural/historical ideal → inwardness → good/authentic self → competitive and self-esteem promises → causal caveat → digital scoring → human limits and acceptance.

Preserved qualifications include multiple causes of suicide, within-culture variation, limits of split-brain inference, collectivism's own pressures, risks of total personal responsibility, Esalen causality limits, narcissism versus self-esteem, disputed generational findings, benefits of individualism, inequality, CJ's explicit atypicality, ambiguous generational changes, disagreement over Heinz's diagnosis, personality change and responsibility after self-acceptance. The 2022 self-esteem review is separately labelled corroboration and appears in Essential.

A late close check found an important internal turn: part 7 revises the early no-authentic-self intuition. `authentic-reconsidered` preserves Storr's bounded return to stable traits in Essential, without reviving Esalen's perfect inner divinity. An unestablished restorative-niches prescription was removed. The conclusion was checked directly against full local paragraphs about change, acceptance, personal projects and environment.

Known limitations and boundaries:

1. The exact supplied Russian EPUB was the principal source. Structure, key analytical passages across every part, notes and methodology were consulted; long narrative stretches were sampled rather than read continuously in full. No claim of an exhaustive line-by-line reading is made.
2. Source 1's URL is bibliographic; its evidence is the local EPUB. No invented print pages. English translates this digest, not an English edition. Locators use EPUB filenames and selected XHTML paragraph indices.
3. Historical/religious/economic chains are Storr's synthesis, not a single demonstrated causal mechanism. Interviews, unpublished archival tapes and clinical records reported by the book were not independently re-investigated. Selected scientific abstracts/review passages are not an exhaustive literature update.
4. Later studies are clearly separated from the 2017 text. The 2022 review complicates simplistic anti-self-esteem conclusions; the perfectionism meta-analysis is bounded to its population. No claim is made about current 2026 platform effects or population prevalence.
5. The maintained shell's chapter lists contain screens visible in the current depth. Hidden-screen automatic depth raising was verified through saved-position Continue; there is no direct hidden entry in that filtered chapter list.
6. Pointer swipe was tested using dispatched browser PointerEvents, not a physical touchscreen. No screen-reader or human reading-comprehension study was performed.
7. The private supplied cover is embedded and credited, with no claim of a transferable publication licence. No external deployment occurred. The digest uses original paraphrase, no copied chapters and no direct quotation passages.

## Session record

Produced the source ledger/claim map, authored and checked 112 bilingual screens, built with the maintained v2 Flexoki shell, passed deterministic and browser QA, removed temporary source-processing/browser files, and prepared only the four requested deliverables for commit. Shared catalogue integration remains outside this collector's scope.
