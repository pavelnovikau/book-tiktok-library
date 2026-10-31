# skin-in-the-game — editorial repair audit

2026-10-31. Verdict: **REBUILD completed; ready for independent check within the documented primary-reading scope.** This is not a whole-book fidelity certificate.

## Delivery actually read

Original collector: 112 RU/EN pairs. Published effective `book-tiktok-data`: 112 pairs, identical screen-for-screen to the collector. Both languages, titles and bodies were read, including the repeated EPUB footers. New delivery: 53 rewritten RU/EN pairs; cumulative Essential/Core/Deep 19/37/53 rather than 30/72/112. All new pairs were substantively self-checked, and all three paths were checked for continuity. The baseline remains in the external baseline.zip.

## Concrete defects and corrections

| Old stable ID(s) | Problematic wording / experience | Correction and primary evidence |
|---|---|---|
| cover | “Аналитический конспект русского EPUB: 30 / 72 / 112 экранов” followed by EPUB and source labels | Replace production description with the real question of reward and consequences. Edition and access scope belong in Sources. `ch1-3.xhtml`. |
| disagreement | “Ссылка на чужие слова или институциональное положение не устраняет личной ответственности...” | This substitutes an adjacent general lesson for the actual section. Rewrite around arguing with intended position rather than convenient literal words. `ch1-24.xhtml#id150`, “Этика несогласия”. |
| bounded-application | “Воображаемая команда получает премию за запуск...” | Invented organisational case. Delete rather than polish or attribute to Taleb. No primary-book location supported this invented team. |
| decision-audit | “Практический перенос конспекта...” and three-item list | Remove the digest's exercise. End with the author's return to lived consequences. `ch1-30.xhtml#id195` is the epilogue, which refuses a conventional summary. |
| multiplicative-example | “Пример конспекта: капитал 100...” | Remove invented arithmetic and recover the author's casino case. `ch1-30.xhtml#id186`: different players versus one player returning repeatedly. |
| lindy-objection | Reviewer Perezgonzalez placed inside Essential | Remove outside review from the author's reading sequence. Keep Lindy as Taleb's mechanism and attribution; `ch1-20.xhtml#id108`, `#id116`. |
| ergodicity-research, ergodicity-dispute | Later Peters paper and abstract-only response interrupt the last chapter | Remove the secondary literature excursion. Rebuild from the actual chapter 19 argument, read continuously through epilogue. |
| intervention-counterfactual, protect-dissent, expertise-not-dismissal, mobility-is-not-justice, reverse-stereotype, commitment-not-truth, objections | Repeated “возражение конспекта”, “вывод конспекта” and generic interpretive qualifications | Remove companion-author voice. Retain genuine internal qualifications through `stake-not-sufficient` (Taleb's fool/crook distinction, `ch1-7.xhtml#id14`), `hostages` (`ch1-17.xhtml#id79`), `defensive-medicine` (`ch1-12.xhtml#id47`) and the conditional surgeon case (`ch1-22.xhtml#id121`). These are in-book complications. |
| eat-turtles | “История о черепахах даёт ... образное правило” without telling the story | Tell the actual fishermen/Mercury episode in original short prose. `ch1-12.xhtml#id37`. |
| green-lumber | “неверно понимал термин” hides the memorable mistake | State the actual confusion between green-painted and unseasoned timber, and the contrast with the informed narrator's bankruptcy. `ch1-22.xhtml#id123`. |
| wealth-and-preferences | General discussion of sellers' interests replaces the scene | Restore Taleb leaving an elaborate prestigious dinner hungry. `ch1-22.xhtml#id135–136` (two fragment anchors, not print pages). |
| bonuses-before-crash, hidden-tail, smoothness-is-not-safety, payoff-shape | Four adjacent micro-essays repeat the same abstraction | Compress into the Rubin case and the distinction between private bonuses and later losses. `ch1-4.xhtml#id6`; technical appendix is no longer required to read the argument. |
| most bodies | EPUB locators and defensive “это не...” qualifications recur after the actual idea | Remove appended locators; store precise locations in metadata/sources.md. Keep only qualifications that materially prevent misreading, such as actual clinical advice or a conditional thought experiment. |
| final | “Сохраните модель...” turns the ending into a reader checklist | Reconnect to the epilogue's choice against a neat final lesson; original paraphrase, no copied maxim. `ch1-30.xhtml#id195`. |

No general RU/EN disagreement was found in the original, but fidelity in both languages inherited the same editorial substitutions. New English is a translation of the digest from the Russian source, not an English-edition quotation.

## Evidence scope and limits

Full supplied Russian edition identified from OPF and spine, 2018, Nikolay Karayev, ISBN 978-5-389-15581-7. Meaningful argument reading covered the introduction, source passages through all 19 chapters and complete final chapter with epilogue; targeted scenes and internal qualifications were revisited before drafting. This was not continuous reading of every paragraph of the entire edition. Structural availability, reading scope and independent historical/scientific verification remain distinct. Complete source ledger and all 53 screen locators: `collector-output/skin-in-the-game/sources.md`. Extracted private text stays outside the public repository.

## Changes, checks and handoff

Four canonical collector files replaced/rebuilt. `contentMode: explanatory`; RU/dark/Essential; one owned-edition source; no publisher images. Counts shrink because duplicate expositions and companion material were removed, not because a shorter quota was imposed. Core and Deep insert actual cases and in-book complications rather than become separate essays.

Structural auditor: 69 passes, zero failures/warnings. Browser: 872 screen renders across 320×568 and 1440×900, both languages/themes, all depths; no overflow, offscreen header controls, network runtime request or runtime exception. Sources and real focus tap work. These are UI checks, not an editorial verdict. Physical iPhone/PWA remains publisher verification.

Publisher must independently read revised pairs and evidence, integrate the root reader/catalogue, and review removed saved-progress IDs. The maintained shell's source labels remain shared behaviour. No root/shared/catalogue/Git/PR/deploy/external-message action taken. Ready manifest records only this collector package and this report.
