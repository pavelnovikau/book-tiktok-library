# Protocols — collector QA

Result: PASS after independent cold-review remediation. Checked 2026-10-31. Catalogue integration is verified separately after promotion.

## Deliverables and boundary

- `huberman-protocols.html`: one portable offline HTML, 477,253 bytes. Embedded Geist and Geist Mono, including Cyrillic; inline CSS/JS. No runtime network dependency, copied publisher artwork, book passages or quotations. Cover is the maintained shell’s typographic composition.
- `story-data.json`: schema v2, stable bilingual IDs and source references.
- `sources.md`: edition identification, claim map, domain checks, source ledger and access limitations.
- This report. Local QA harnesses, profiles and screenshots were working material and are not part of the public four-file collector package.

No lawful complete local edition was found in filename discovery of the supplied Smartcat trees; no unauthorized edition was sought. The full book was **not read**, and chapter-by-chapter completeness is **not claimed**. The artifact is an original analytical atlas using official publisher/book descriptions and public Huberman Lab materials, checked against external medical/scientific evidence. Its topic order is editorial, not an invented table of contents. No page references are fabricated.

The book is identified through Penguin / Cornerstone Press, ISBN 9781529921298, published 15 September 2026, listed at 688 pages. Publisher marketing establishes the premise, not medical efficacy. Research is targeted and current to the check date, not an exhaustive registered systematic search. A systematic review in the source ledger is an original research synthesis, not a tertiary summary of the book.

## Exact nested counts, words and time

Counts include the level-1 cover and final. Essential is a subset of Core, which is a subset of Deep. Level counts: **36 / 54 / 54**; cumulative counts: **36 / 90 / 144**.

| Mode | Screens | RU words | EN words | RU reading time | EN reading time |
|---|---:|---:|---:|---:|---:|
| Essential | 36 | 1,883 | 2,130 | about 11 min | about 10 min |
| Core | 90 | 4,667 | 5,264 | about 26 min | about 24 min |
| Deep | 144 | 7,428 | 8,446 | about 42 min | about 39 min |

Words use the maintained builder’s Unicode token definition and include titles, cover subtitle, body and list indices, excluding interface/source-dialog copy. Its auditor excludes the cover subtitle, reporting 7,419 RU / 8,434 EN; that difference is expected. Body only: 6,508 RU / 7,361 EN, averaging **45.2 / 51.1 body words per screen**. Body ranges including cover: 24–57 RU / 29–64 EN. Time is a mechanical estimate (180 RU / 220 EN words per minute), not time for reflection or medical decisions.

RU default; complete EN copy, source notes, disclosure and interface. Dark default, Flexoki light/dark available. Numeric anchors are identical between translations. Each screen has one shared level, ID, provenance and source list.

## Sources and epistemic checks

**50 sources:** 11 official author/publication-context sources; 1 publisher; 23 institutional/professional references or consensus documents; 11 systematic reviews/meta-analyses; 4 primary studies. The 38 scientific/institutional entries contain 37 external sources and one Huberman-coauthored study (22), explicitly not independent replication.

Screen provenance: 1 cover, 16 author-position screens, 43 evidence-check screens, 84 synthesis screens. `book` remains the schema type; the visible label is **Author position / Позиция автора**, avoiding a false claim of chapter access. The Huberman-coauthored breathing trial is also displayed as Author position and identifies the overlap in its body. Provenance is not a confidence grade.

Medical coverage and independent checks:

- Sleep/light: CDC, AASM CBT-I guidance, expert light consensus, caffeine systematic review and laboratory vigilance study; sun-gazing risk and light-therapy contraindication context.
- Exercise: WHO public-health guidance; no personal clearance, intensity, pulse-zone or sprint prescription.
- Nutrition: current WHO dietary guidance, 2025 BMJ fasting review, 2024 isocaloric trial and NIDDK diabetes precautions; no individual fasting window, fluid or diet prescription.
- Stress/focus: primary breathing study distinguished from independent breathwork review; NCCIH meditation/relaxation evidence, retrieval-practice review, binaural-entrainment review and hearing safety.
- Temperature: 2025 cold-water review, AHA cold-shock risk, sauna review and observational cohort, CDC heat-illness guidance, 2024 cold/hypertrophy meta-analysis. Alertness, acute recovery, adaptation and longevity are separate outcomes.
- Supplements: NIH ODS/NCCIH, magnesium and theanine reviews. Evidence by ingredient/outcome, labeling and drug-interaction limits, renal/thyroid/liver/pregnancy contexts. Ashwagandha avoidance in pregnancy/breastfeeding is explicit. No brand endorsement, stack, dosage or treatment substitution.

Official sponsorship and the Momentous commercial link are disclosed. Review-level author disclosures still matter: external provenance is not a guarantee of no financial ties. No blanket clinical validation of the complete protocol bundle is claimed.

The source-access check recorded transport outcomes. Some direct automated routes were blocked, minimal or redirected; official indexed pages, abstracts and alternate official retrieval routes were used where available. These outcomes are not described as complete full-text access, and no access controls were bypassed. The original book’s complete text was never acquired.

## Independent cold-review remediation

The independent reviewer read the skill, all three references, all four canonical files and every RU/EN screen. Verdict: READY WITH FIXES, with no critical medical error. All required fixes were applied before promotion:

- `stress-no-water` now cites the CDC MMWR case series on dangerous underwater hyperventilation and breath-holding in addition to cold-shock guidance; its warning was preserved.
- `sleep-two-process` now describes a simplified scientific two-process model, cites Borbély et al. (2016), and distinguishes circadian Process C from homeostatic Process S.
- The Russian `review` role now displays as **Обзор исследований**, not **Рецензия**. The correction was also made in the installed and repository skill templates so future books inherit it.
- `nutrition-tre-trial` now reports no statistically significant additional effect and names the actual population: adults with obesity plus prediabetes or diet-controlled diabetes.
- Essential gained direct diabetes/restrictive-eating and temperature-safety boundaries; the supplement-regulation statement is explicitly scoped to the United States.
- The misleading ID `temperature-alcohol` became `temperature-stacking`. Two overlapping synthesis screens were rewritten with separate jobs: transfer across populations/contexts and a one-change trial with a predefined stopping rule.

The source ledger, JSON and embedded HTML were updated together. The exact 36 / 90 / 144 nesting did not change.

## Build and deterministic audit

The maintained builder was used:

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs story-data.json --out huberman-protocols.html
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs huberman-protocols.html --min-screens 144 --require-bilingual
```

The maintained builder preserves the quiet Flexoki cyan action tokens. Artifact-local adjustments retain a localized text library control and the Author position label; the reusable template correction changes the Russian research-review label for future builds. The final structured corpus embedded in HTML was compared exactly against the JSON screens/sources.

Post-review audit: **68 passes, 0 warnings, 0 failures**. Unique IDs, bilingual copy, nested counts, source references, offline shell hooks and Flexoki identities pass. There are zero duplicate titles, duplicate bodies, empty bodies or numerical translation mismatches. Exact-string uniqueness is not treated as proof against semantic padding; the cold review identified the closest overlaps, and the two strongest were rewritten as described above.

## Isolated real-Chrome QA

Chrome 155, local `file://` artifact, CDP; no web server and no collaborative preview. Each launch used `timeout 30`, a unique `mktemp -d` profile, an automatically allocated dedicated debugging port, and `finally` cleanup through Browser.close, process-group termination and profile deletion. No unrelated Chrome processes were touched.

Matrix: **320×568, 390×844, 1024×768, 1440×900 × RU/EN × light/dark × Essential/Core/Deep = 48 combinations**. All screens were traversed using the actual navigation handler: **4,320 screen visits**. Saved matrix files contain per-mode counts, scrolling screens, layout failures and errors. All final matrix runs pass.

Verified:

- Exact count/title/position for every screen in every combination; nonempty content; side padding at least 12 px; no document or slide horizontal overflow.
- Vertical overflow is scrollable rather than clipped. Long 320 px screens intentionally require scrolling; text is not reduced to illegible sizes.
- All five top controls stay inside the viewport at 320 px. Library `href="./"` is retained; this collector is not registered into the shared root library.
- Desktop rail is visible and scrollable; its active ID is synchronized and the active entry remains inside the visible rail after animation frames.
- Language/theme preserve screen and mode. Both dialogs open/close; all 50 source entries render. Hidden-screen mode raising is exercised through the actual bound chapter handler with an injected target ID, since the normal contents list shows the selected mode’s screens only.
- Buttons, Arrow/Page/Space keys, final restart, saved progress, Continue and Start over. Trusted CDP ArrowRight/F/Escape events supplement DOM-event assertions.
- Focus mode by text tap and F; Escape exit; header/rail hidden and Next retained; focus persists across paging. Vertical gesture does not page/focus; horizontal pointer swipe pages without toggling focus. These are browser event-path checks, not physical-device touch certification.
- Embedded fonts load; font cmap checks include Cyrillic. No external image is present; image decoding is not applicable to the typographic cover.
- **16 interaction configurations × 24 checks = 384 assertions**, plus a final author-overlap provenance check in all 16 size/language/theme combinations. **Zero unexplained runtime/console errors**.

One intermediate Chrome launch failed to start during concurrent machine activity; its profile was cleaned and that configuration passed on retry. Initial QA-harness synthetic-event targeting issues were corrected before the recorded passing suite. No unresolved artifact failure remains.

## Visual review

All **144 RU Deep screens at 320×568 dark** were captured and inspected in contact sheets during collection, including padding, title wrapping, content rhythm and duplicates. Representative cover, list, comparison, quantitative guidance, dense evidence, safety, provenance and final screens were inspected for all 16 size/language/theme settings. The post-review browser matrix reran every screen and interaction configuration; its temporary screenshots were not published. No publisher art or medical illustration implies additional source access.

Screenshots are viewport captures: lower text on long phone cards is reached by scrolling, confirmed by the full traversal. The screenshot set is supporting QA, not a second story corpus.

## Catalogue integration

The promoted root reader was processed by the shared reader shell, retaining the exact `href="./"` home contract while adding the maintained iOS install guidance and standalone/focus visibility rules. Whole-library validation passed with **12 books, 1,299 screens, 8 declared sections / 7 populated shelves and 12 unique semantic cover motifs**. Browser QA covered the catalogue and every promoted reader at 320×568, 390×844 and 1440×900: runtime errors 0, horizontal overflow 0, focus mode passed, and iOS browser/standalone guide behavior passed. The catalogue entry is `health-protocols` / `practices`, adult, 144 screens, with an original cyan stepped protocol-stack motif.

The catalogue shell derives all counters from `books.json`; the expected post-integration labels are `12 книг`, `1299 экранов`, `7 разделов`, with `Практики · 5`. Catalogue and service-worker freshness rules use network revalidation, so this promotion does not depend on clearing an old PWA cache manually.

## Final artifact identity and cleanup

HTML SHA-256: `fc2f059e7f33f7514d73050229f6dfac4ae3f34178636f8b11fd938ce388f6a9`.

The public collector package contains exactly the standalone HTML, `story-data.json`, `sources.md` and this QA report. The promoted root reader and catalogue entry are separate integration files. Final process/profile cleanup was checked after the post-review browser matrix.
