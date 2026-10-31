# Behave — post-review repair verification

2026-10-31. Cold review: READY WITH FIXES; parent has applied and verified every required fix. This report separates the new verification from the historical collector report below.

- Rebuilt on the current portable template: focus hides the actual counter; native Space activates focused Chapters/Sources; F/Escape works after Next; cover focus hides Start/depth controls and retains Next; iOS guidance is suppressed in focus and standalone mode; quiet cyan action colors.
- Fixed the desktop-cover minimum-width defect with a stacked cover at 900–1199px. Verified actual cover bounds inside the story pane, not only document overflow.
- `empathy-imaging`: both languages now identify the experimental cue signaling a partner's pain. This wording was checked against Singer et al. (2004), PubMed 14976305; no direct observation of the partner's painful stimulus is implied.
- Exact nested 36 / 90 / 144; 49 sources. Builder totals 7,635 RU / 8,970 EN words in Deep; estimates 11 / 27 / 43 min RU and 11 / 26 / 41 min EN. Auditor totals 7,631 RU / 8,961 EN. Deterministic audit: 68 passes, zero warnings/failures.
- New file:// real Chrome QA: **6,480 screen visits** over 320×568, 390×844, **900×768, 960×768**, 1024×768 and 1440×900; all RU/EN × themes × depths, 1,080 states per viewport. Every rendered heading/count and document/slide/cover bounds passed; embedded fonts loaded. Zero runtime/console errors or HTTP(S) requests.
- At every viewport, native Space on Chapters and Sources, dialogs/source count, paging keys, cover focus, safe Next, hidden counter/cover controls, F/Escape after Next, tap enter/exit, and iOS browser/saved-focus/standalone behavior passed. Browsers used timeout 30 with isolated profiles/ports and finally process-group/profile cleanup. No physical Safari or screen-reader QA claimed.
- The independent reviewer read all 144 paired screens, found no material scientific overclaim, repeated job requiring deletion or translation qualifier reversal, and verified primary research boundaries. They did not certify fidelity against an unavailable full edition. The source-backed analytical companion boundary remains explicit and unchanged.

Current collector HTML SHA-256: `f1fc9b5a3ae85d4950554afe46824cb7d832f492948e3c74b7aaad4d76a687a7`.

The historical report below describes the original build. Its violet-color and old-shell PASS claims are superseded by the repaired-shell checks above; prior counts should be read as pre-repair measurements.

---

# Behave · collector QA

Date: 2026-10-31.
Destination: `collector-output/behave/` only. Final deliverables: `story-data.json`, `behave.html`, `sources.md`, `QA.md`. No catalogue, root reader, shared template or LOG edits; no deployment, push or PR.

## Evidence boundary

No full lawful local English or Russian edition was available. No cover-to-cover reading is claimed. The synthesis uses official publisher bibliographic material, exposed Google Books contents, the ungated opening of the introduction in The Scientist, Sapolsky’s accessible written interviews and the official TED talk synopsis. The complete lecture was not watched or transcribed. Full chapters, notes, every anecdote and the Russian translation were not verified. No invented page numbers, quotations or publisher artwork.

Scientific scaffolding is independently sourced, including 2023–2026 updates on adolescence, oxytocin, genetics, serotonin and human neurogenesis. Historical, animal, observational-human, experimental-human, theoretical, author-interpretation and editorial-inference moves are distinguished in the relevant copy. `sources.md` records actual consulted coverage, access limits and a full stable-ID claim map. This is a source-backed analytical companion, with substantial explicit synthesis, rather than an edition-based exhaustive summary.

“Biology without determinism” here excludes single-factor fatalism and biomarker verdicts. It does not misrepresent Sapolsky: his rejection of free will is explicitly identified as the author’s philosophical position, not a settled empirical consensus. No diagnosis, treatment advice, criminal prediction, sex/race essence or moral evaluation from biomarkers is supplied.

## Exact corpus and density

| Mode | Cumulative screens | RU words | EN words | RU estimated minutes | EN estimated minutes |
|---|---:|---:|---:|---:|---:|
| Essential | 36 | 1,902 | 2,243 | 11 | 11 |
| Core | 90 | 4,785 | 5,608 | 27 | 26 |
| Deep | 144 | 7,633 | 8,963 | 43 | 41 |

Counts include one cover and one final screen, both level 1. Levels: 36 / 54 / 54. Essential is a complete causal path with direct evidence, qualification, social consequences and final change account; Core and Deep insert screens into the same order.

Word totals above use the maintained builder’s Unicode tokenizer on titles + subtitle + bodies, excluding section labels, interface, method dialog and source notes. Body-only totals: RU 6,734; EN 7,895. Mean body length: 46.76 RU / 54.83 EN words. Body ranges: 41–52 RU / 44–64 EN. English runs about 17% longer; quantities, qualifications and cognitive jobs were checked for parity. Numeric-token comparison across all 142 interior screen pairs found no mismatches after thousands- and decimal-separator normalization.

Provenance: 22 book-argument screens, 46 independent-corroboration screens, 75 synthesis screens (including the final), 1 cover. Sources: 49 total — 25 primary, 18 scientific/reference reviews or authoritative accounts, 3 author sources, 2 lawful book/preview sources, 1 publisher source. These roles are not confidence rankings.

## Editorial review of all screens

All 144 RU/EN pairs were reviewed for a distinct cognitive job, qualifications and source attachment. Every pair has the same stable ID, level, claim type and sources. No exact duplicate titles or bodies in either language. Pairwise token-set similarity was used as a triage aid, not as a semantic proof: the highest English pair was 0.237, distinguishing defensive circuitry from hippocampal context circuitry. The early-environment/development bridge, risk/trust examples and moral-evaluation/empathy transition were reviewed as distinct causal jobs.

Transition screens carry a specific cross-timescale dependency rather than introducing a separate summary. Five initially general-purpose screens were replaced with concrete independent mechanisms: context circuitry, serotonin in group-living mice, stress timing, sensitive periods and lactase persistence. Original thought experiments are explicitly identified; none is presented as a measured result or a book anecdote. Dense screens remain in the ordinary body-word band. No material was copied from another book.

## Maintained build and deterministic audit

Built with:

```sh
node skills/book-tiktok/scripts/build_story.mjs story-data.json --out behave.html
node skills/book-tiktok/scripts/audit_story_html.mjs behave.html --min-screens 144 --require-bilingual
```

Final audit: **68 passes, zero warnings, zero failures**. Schema v2; exactly 144 unique screens; exact `targetModes` 36/90/144; bilingual provenance and valid source references; standalone/offline invariants pass. The audit reports RU 7,629 / EN 8,954 because it excludes the cover subtitle; this is the sole expected difference from builder word totals.

One Behave-local CSS correction follows generation: explicit light/dark selectors reapply token-based root/body backgrounds and reading text colors after theme changes. Shared files were not modified. This fixed stale inherited foreground/background colors observed during rapid switching in local Chrome. To reproduce the exact HTML after the maintained build, insert before the first `</style>`:

```css
/* Behave-local theme invalidation guard; shared shell remains unchanged. */
html[data-theme="light"], html[data-theme="light"] body { color: var(--color-text); background: var(--color-bg); }
html[data-theme="light"] .story-slide, html[data-theme="light"] .story-slide :is(h1,h2,p,li) { color: var(--color-text); }
html[data-theme="light"] .story-slide :is(.muted,.kicker,.source-label,.fact-label,.cover-eyebrow) { color: var(--color-text-muted); }
html[data-theme="dark"], html[data-theme="dark"] body { color: var(--color-text); background: var(--color-bg); }
html[data-theme="dark"] .story-slide, html[data-theme="dark"] .story-slide :is(h1,h2,p,li) { color: var(--color-text); }
html[data-theme="dark"] .story-slide :is(.muted,.kicker,.source-label,.fact-label,.cover-eyebrow) { color: var(--color-text-muted); }
```

The final audit was rerun on the corrected HTML.

## Isolated real-browser matrix

Native local Google Chrome, headless CDP; each run had a unique `mkdtemp` profile, dedicated ephemeral debug port and `/usr/bin/timeout 30`. Loaded directly over `file://`; no local server or collaborative preview. Runs exercised real rendering and DOM event handlers; navigation and gesture assertions were automated. Motion was reduced for deterministic geometry; representative screenshots were visually inspected.

| Viewport | Languages | Themes | Modes | Screen visits | Errors / horizontal overflow |
|---|---|---|---|---:|---|
| 320×568 | RU, EN | Light, Dark | Essential, Core, Deep | 1,080 | 0 / 0 |
| 390×844 | RU, EN | Light, Dark | Essential, Core, Deep | 1,080 | 0 / 0 |
| 1024×768 | RU, EN | Light, Dark | Essential, Core, Deep | 1,080 | 0 / 0 |
| 1440×900 | RU, EN | Light, Dark | Essential, Core, Deep | 1,080 | 0 / 0 |

Total: **48 language/theme/mode/viewport cases; 4,320 rendered screen visits**. Every case traversed every screen visible in that mode, matching stable IDs, localized titles, counters and exact counts. Checked document and scroll-body horizontal bounds, text/card bounds, selected-rail identity, nonempty content, scrollability and access to content bottom. Correct theme text color was asserted on every title after the contrast fix. Phone vertical scrolling is intentional; the cover and comparisons can extend below the fold.

Additional behavior passed at all four sizes:

- RU/dark fresh defaults; language and theme changes preserve current screen, depth and progress.
- Chapters and Sources dialogs open/close; all 49 source entries and localized boundary note present.
- Mode filtering in the dialog; deep chapter selection; retained hidden-ID navigation raises to the required level. The latter exercises the shell’s hidden-ID fallback using a retained navigation node, not a publicly listed hidden chapter.
- Start, Back/Next, Arrow/Page keys, Space, horizontal pointer swipes and vertical-gesture rejection.
- Tap focus and second-tap exit; F/Escape; hidden header/Back, safe Next, preserved focus while paging.
- Reload persistence; Continue resumes the saved ID; Start over begins at the first interior screen; final Restart returns to cover and clears saved progress.
- All top controls fit at 320 px. Desktop rail is visible and independently scrollable at 1024/1440, with active item synchronized after the next animation frame.
- Embedded Geist and Geist Mono loaded; font cmap inspection confirms Cyrillic coverage in both. No raster media: image decoding is not applicable. Cover is the maintained typographic visual, not publisher art.
- Zero JavaScript/runtime errors and zero HTTP(S) resource requests. Optional source links were inspected as navigation links, not followed during offline QA.

Visual inspection covered cover, method/disclosure, dense prose, two-column/stacked comparison, ordered steps, provenance and ending at phone and desktop sizes, across RU/EN and light/dark. Twenty representative screenshots were captured; selected samples were visually inspected. Screenshots and test scripts were temporary and removed after review.

## Cleanup and limitations

All owned Chrome process groups were terminated; unique profiles were removed, including after initial assertion failures. No owned Chrome, server, HMR session or temporary profile remains. Only the four requested deliverables remain in this directory.

The standalone file is readable offline; linked scientific sources require a network when opened. Reading-time estimates assume 180 RU / 220 EN words per minute and do not include source consultation. No exhaustive literature-search claim, full-book claim or external delivery. The maintained relative home link is `./`; catalogue integration remains outside this collector-only task.
