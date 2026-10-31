# Thinking, Fast and Slow — implementation report

2026-10-31. Verdict: REBUILD / approved new addition. Ready for independent check, not independently approved or published.

## Actual reading and previous delivery

No collector folder or root HTML existed for this assigned slug at intake. Therefore old pairs read: 0; new pairs read: 29 RU/EN (58 localized copies). The effective embedded corpus was compared to JSON. Every screen’s source and bilingual meaning was reviewed while writing; Essential/Core/Deep sequences were separately inspected for continuity. This is implementation review, not independent review.

## Evidence scope

The complete owned Russian EPUB was identified from OPF, copyright page, 117 spine entries, five parts, appendices and notes: Daniel Kahneman, Thinking, Fast and Slow (2011), Bakanov translation school 2013, AST 2014. Two local 5.2k/5.7k-word condensations were rejected. This implementation consulted selected supporting passages across all five parts, introduction and conclusion, not every paragraph of the volume continuously. Retained claims and cases are mapped to exact spine filenames below. The official Macmillan English introduction was additionally read; EN is an original translation of this condensation, not a full translation-fidelity comparison. No present-day scientific validity review is claimed; social priming and ego-depletion episodes are excluded rather than certified. The private edition and temporary extraction remain outside public Git.

## Concrete findings and resulting implementation

1. The source-candidate defect was edition identity, before any screen existed: two similarly named Kahneman EPUBs have two spine entries and about 5.2k/5.7k words; they cannot certify the work. The third has 117 entries and the AST copyright/translation page. `sources.md` records the distinction.
2. `two-systems`: avoided anatomical claims and the false equation fast=bad/slow=good. Source: content3–5 and content103.
3. `small-samples`, `base-rates`, `flight-instructors`: kept three distinct mechanisms rather than merging them into a generic warning about bias. Primary locations: content25–27, content36–38 / Introduction, content42–43.
4. `when-intuition-learns`, `interview-in-parts`, `outside-view`, `premortem`: retained the actual author/Klein conditions and procedures. No new team/project anecdotes were added. The hypothetical failed project is Klein’s expressly attributed procedure, not a claimed historical event.
5. `reference-point` through `same-outcomes-new-frame`: retained reference dependence, loss aversion, probability weighting, endowment, framing and the author’s own blind spots. No fixed universal loss-aversion coefficient or implied investment recommendation.
6. `two-selves`, `the-cold-hand`, `focusing-illusion`: retained the final part’s distinction between experience and memory; did not turn peak/end into an instruction to add pain.
7. Sources and access limitations live in the dialog. Local CSS hides repetitive per-screen footers while retaining `contentMode: explanatory` and source maps.

## Delivered arc and counts

Judgment and its limits → heuristics/statistics → confidence/skill/forecasting → prospect theory and choice → experience/memory → limits of self-correction. Counts are derived from prose: 14 / 24 / 29. Full screen evidence map: `collector-output/thinking-fast-and-slow/evidence-map.sol.json` and `sources.md`.

## Validation and remaining limits

69 deterministic structural checks, zero failures/warnings. Offline browser coverage: four widths × two languages × two themes × all 29 screens, exact mode counts, dialogs, fonts, saved ID, keyboard focus and single-row icon header; no exceptions, horizontal overflow or remote requests. JSON and embedded screens equal. No physical iPhone or deployed-site test. See `QA.md` and per-width JSON.

This is a central-argument condensation, not a continuous full-edition reading or bilingual textual collation. Later scientific controversies are outside this account; book results are not blanket-certified as current findings. Independent editorial check and publisher/root/catalogue integration remain open. No Git, PR, deploy, shared-shell or root-reader edits were made.

## Final local scroll check, 2026-10-31

Every body’s final paragraph is reachable by vertical scrolling at all four widths in RU/EN and both themes. Refreshed screenshots wait for the transition to finish. Source/prose/HTML were unchanged by this QA refinement.
