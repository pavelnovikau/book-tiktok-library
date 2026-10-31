# The Lost World — detailed editorial repair

Date: 2026-10-31. Verdict: **REBUILD**. Scope: all 144 original bilingual screen pairs read (288 language screens); the effective embedded corpus of the root published reader and the collector HTML was compared with the authoring JSON. The root contained the same 144 pairs and identical data. This is an audit of that delivery, not a new collector assignment.

## Reader finding

The package largely replaces an adventure with lessons on evidence, competence and responsibility. Even many `book` screens move from an incident immediately to an instruction. Essential is particularly affected: it withholds the actual story while presenting its moral interpretations. The novel's comedy, suspense and concrete movement need to carry the reading.

## Concrete findings in the original delivery

| Stable screen ID | Actual wording / defect | Correction and primary location |
|---|---|---|
| cover | «Что сильнее меняет человека… необходимость отвечать» / “becoming responsible for his choices” establishes a lesson as the premise. | Start with Malone's desire and Challenger's extraordinary claim; I–IV. |
| borrowed-heroism | «узнаваемый порог взросления» / “recognisable threshold of growing up” replaces the courting scene with a developmental thesis. | Tell Gladys's ideal and Malone's response; I. |
| honest-ignorance | «Следи за этим различием» / “Watch the distinction” instructs the reader instead of showing the failed disguise. | Restore the borrowed scientific question and its exposure; II–III. |
| different-strengths | «Команде нужны разные виды компетентности» / “A team needs different kinds of competence” displaces Roxton's actual introduction. | Show his deceptive Ballinger test and the practical preparations; VI. |
| preparation, competence-versus-bravado | «честно оценить собственные навыки» and “Judge an action’s usefulness” are advice added by the digest. | Remove the lesson screens; keep supported actions in VI. |
| landscape-as-action, ambiguous-sighting | Explanations about knowing and naming precede the forest and sighting themselves. | Restore the hidden river, bamboo and disagreement over the flying shape; VIII. |
| entry-and-exit | «Хорошая находчивость учитывает… последствия» is a prescription replacing the bridge's suspense. | Show the tree crossing and the deliberate loss of the bridge; IX. |
| better-view | “another hour of the same work may yield less…” makes a productivity analogy out of the treetop episode. | Restore the argument over leaving, Malone's idea, the face and the view; XI. |
| survival-bias | «отдельно оценивай… информацию и итог» is an exercise in decision analysis. | Preserve the wrong weapon, pursuit and empty camp without the external lesson; XII. |
| responsibility-shift | “his worth no longer depends…” asserts a psychological transformation too categorically. | Tell the reunion and rescue, without inventing a definitive inner motive; XIII. |
| campaign, battle-aftermath | The concrete violence is present and important, although framed as commentary. This is not a defect to erase. | Retain extermination and enslavement, separately attributing Challenger's celebration and Malone's unease; XIV. |
| balloon, weapons-have-limits | The predator scene is placed after the later balloon episode and retrospectively repairs its chronology with «Ранее…». | Put the predator scene before the balloon; XV. |
| queens-hall, gladys-ending, diamonds-choice | Core contains the public, romantic and material resolutions. Earlier local copy admits this, but the corrected brief requires decisive endings in Deep. | Put all resolutions after an explicit level-3 warning; XVI. |
| carry-forward, bedtime-question, final | Four questions, a counterfactual exercise and «Удивляйся, проверяй, замечай других» replace the ending experience. | Remove; end the deep story with Roxton's offered hand and keep only a neutral depth navigation final; XVI. |
| claim-classes, evidence-boundary | Evidence lessons interrupt the adventure; labels appear on every story screen. | Use `contentMode: narrative`; retain provenance in Sources and report only. |

No RU/EN change of plot outcome was found in the old pairs. Both languages share the same editorial failure; fluent translation does not repair it. Older green QA and source-attachment totals are not used as evidence of fidelity.

## Rewrite

All visible text was rewritten. The corpus is now 34 pairs, nested **13 / 23 / 34**, replacing 36 / 90 / 144. Counts follow actual scenes: there is no quota padding. The sequence runs from Gladys to the empty camp in Essential/Core, then through rescue, war, escape and homecoming in Deep. Both short modes have a deliberate suspense stop. The original abstract cover remains. Source metadata and method note were replaced; the one source is the actual novel. `contentMode` is `narrative` and `spoilerPolicy` is `full-plot-in-deep`.

## Evidence limits and self-check

The full lawful English edition is available and stored privately; selected narrative runs across I–XVI, including the entire plot's causal pivots, were read. Every retained incident is tied to those primary passages. This is not certification of every sentence of the unabridged novel, of its scientific claims, or of a particular Russian translation. The retelling contains no invented direct speech, private thoughts, scene, page number or resolved fate for the escaped animal.

Substantive self-check: both new language sequences read; all three nested story routes checked for missing antecedents and causal jumps; the warning, Sources notes, cover and final checked for ending leaks. Balloon chronology and the uncertain pterodactyl fate were specifically retained. Technical results and publisher requirements are recorded in QA.md and the eventual ready manifest.

## Final candidate self-check and local QA

The Essential route explicitly introduces Challenger’s participation and includes Malone’s lake/pit episode before he climbs out of the trap. Both full language sequences and each nested route were read for antecedents and causal links.

Final corpus: **34 rebuilt RU/EN pairs**; exact depths **13 / 23 / 34**. Maintained structural audit: **69 passes, 0 warnings, 0 failures**. Browser traversal covered **560 screen visits** at 320×568 and 1440×900, both languages, both themes and all depths. Exact rendered body text/title/progress, contained layout, bottom reachability, narrative-label suppression, sources, consent, reload, focus and keyboard controls passed. Mobile RU/dark and desktop EN/light narrative screenshots were visually inspected; the bilingual narrow consent dialog was also inspected. These are local checks, not independent editorial approval or physical Safari testing.

Publisher must preserve the book-local spoiler dialog, safe contents labels, navigation/mode guards and saved-Deep-title protection. They are absent from a plain maintained rebuild. The maintained shell supplies narrative presentation; no shared file was edited. See QA.md for reproducibility, limitations and final delivery details. Status: **ready-for-independent-check**; no publication has been performed.
