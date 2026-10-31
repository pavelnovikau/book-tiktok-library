# Dune — substantive pass 2 implementation, 2026-10-31

**EDIT implemented; ready-for-independent-check only.** All six required DUNE-SR findings have concrete source/runtime repairs. No independent PASS, publication or complete-edition certificate is asserted. The original `reviews/dune-source-rescue.json/.md` remain byte-identical and retain **REQUIRES-FIXES** for their original reviewed bytes.

## Reading and resulting story

Read all **38 existing RU/EN pairs**, current effective embedded HTML, exact **10 / 17 / 38** nested routes, current source ledger/ready manifest, BRIEF, CONTRIBUTING, local and installed book-tiktok instructions. Read current Giver/Hitchhiker/Accelerando runtime guards as read-only references. After repair, reread every revised pair and all cumulative routes in both languages. This is 38 unique bilingual pairs, not 65 different pairs; the three nested routes contain 65 positions per language. Actual delivery corpus exactly matches authoring and the maintained builder’s computed embedded data.

Seven prose pairs changed; `the-sietch` changes only source coverage/locator. Stable IDs, levels, media and all Essential/Core/final copy are unchanged. Counts remain 10 / 17 / 38 because the revised story fits those beats; no quota padding. The palace friendship change occurs before the duel, Paul’s death/survival vision belongs to the uncertain duel moment, and Jessica’s reassurance closes the Deep story. There are no new scenes, dialogue, motives, arena subplot, Fenring inner motive, sequels, films or management/moral lessons.

## Six implemented corrections

| Finding | Changed IDs / runtime | Correction and directly checked witness |
|---|---|---|
| DUNE-SR-001 high | reader runtime; `deep-warning` retained | Bilingual native modal before Deep mode or first level-3 ID, including Contents and saved Continue; no late contents/rail titles before consent. Memory-only acknowledgement revoked on downgrade/reload, Cancel/Escape preserve safe mode/ID/scroll. Existing generic saved-Deep labels retained; acceptance recovers original saved ID. |
| DUNE-SR-002 | `the-imperial-fleet`, `the-wall-breaks` | Preparation stays before battle; southern raid/dead-son/captured-Alia news moves **after breach and assault begins**. No revenge-as-initiating-motive. [SparkNotes section 11](https://www.sparknotes.com/lit/dune/section11/) Summary first two paragraphs; [Reactor 19](https://reactormag.com/rereading-frank-herberts-dune-dune-part-nineteen/) **second Summary**, last paragraph. |
| DUNE-SR-003 high | `two-years`, `spice-and-power`, `the-last-duel` | Explicit prophetic religious allegiance; Paul experiences Stilgar becoming worshipper; at the duel he sees death as sacrifice/survival as invincibility feeding the legend and sees no way to halt holy war. His experience, not omniscient guarantee or completed future war. [SparkNotes 9](https://www.sparknotes.com/lit/dune/section9/) Summary; [Reactor 20](https://reactormag.com/rereading-frank-herberts-dune-dune-part-twenty/) **second Summary**, Stilgar paragraph and uncertain duel; [O’Reilly 3](https://www.oreilly.com/tim/herbert/ch03.html) **embedded Herbert passage beginning He sampled the time winds**, final death/survival alternatives. Surrounding biological criticism excluded. |
| DUNE-SR-004 | `the-settlement` | Irulan named emperor’s daughter and proposed dynastic alliance; Jessica/Chani negotiate, Chani doubts Paul’s promise; both women’s concubine status distinguished from dynastic marriage. Jessica’s history/wives assurance remains **her** reassurance. [Official PRH opening](https://sites.prh.com/dune/read-an-excerpt), Jessica paragraph; [Reactor 20](https://reactormag.com/rereading-frank-herberts-dune-dune-part-twenty/), **second Summary**, closing paragraphs. No invented official marriage for Jessica, enacted wedding/reign or sequel outcome; unreliable guide wife/concubine reversal not used. |
| DUNE-SR-005 | `the-poisoned-tooth`, `the-last-duel` | Piter identified as baron’s Mentat adviser; Feyd-Rautha **Harkonnen** as nephew/heir. [SparkNotes 1](https://www.sparknotes.com/lit/dune/section1/) Summary baron/Piter/Feyd; [O’Reilly 4](https://www.oreilly.com/tim/herbert/ch04.html), prose before final-combat quotation; Reactor 20 second Summary. O’Reilly’s identifying prose remains secondary. |
| DUNE-SR-006 | `the-sietch`, `spice-and-power` | Adds source 9/G6 to Kynes/father project; restores worm-cycle → spice, Paul/Jessica’s prepared means to end the cycle, spice-fed Guild prescience/navigation, credible **unexecuted** threat → compliance. No chemical procedure or completed spice destruction. [SparkNotes 6](https://www.sparknotes.com/lit/dune/section6/) dying Kynes/father Summary; [O’Reilly 3](https://www.oreilly.com/tim/herbert/ch03.html) water-stealer/melange exposition; [O’Reilly 4](https://www.oreilly.com/tim/herbert/ch04.html) Guild exposition and distinct quoted reflection; **first Summary** of Reactor 19, last Paul/Jessica paragraph, then Reactor 20 second Summary. |

Exact old/new copy, screen arrays and primary/secondary source locators are in `repairs/dune-substantive-pass2.json`; current 38-row source map is in `collector-output/dune/sources.md`. New source **18** is Reactor Part Nineteen, role `reference`, with bilingual outcome-safe access note. Fictional ecology/prescience are not presented as real science.

## Evidence scope

Scope is the **1965 first novel** and three internal books, without collating a particular complete edition or published Russian translation. Prior rescue acquisition is retained read-only. This pass rechecked PRH’s opening relationship passage; SparkNotes 1/6/9/11; first-novel O’Reilly ecology/Guild/combat context and explicitly identified Herbert quotations; both Reactor 19 Summary sections and Reactor 20’s second Summary. Reactor direct requests returned 403; substantial public indexed Summary text was read through ordinary web search, without restriction bypass. Critic Commentary was not used as Herbert primary narrative. No purchase, account, unofficial full-book mirror or private/full novel text in the repository.

These passages support the particular retained causal links; whole-book continuous fidelity remains unestablished. No critical source gap is knowingly retained in those six corrections. Source sufficiency and prose still require an independent reviewer’s judgment, not a blanket complete-EPUB gate or a self-certificate.

## Runtime preservation and exact publisher hooks

Maintained local `build_story.mjs` wrote only an **external temporary** `builder-data-only.html`. Its `book-tiktok-data` was ported into the existing collector reader, retaining original CSS, embedded media and complete focus/install/icon-header code. Never ship the temporary builder output: it lacks the Dune gate. Do not clean-rebuild the collector/root from JSON during Settings integration.

Preserve these exact hooks while synchronizing the accepted Settings/Geist shell:

- Dialog `#duneSpoilerDialog[data-book-spoiler-guard="dune-v1"]`, associated `#duneSpoilerTitle`, `#duneSpoilerCopy`, `#duneSpoilerCancel`, `#duneSpoilerAccept` and ARIA linkage.
- Closure block from `// DUNE-SR-001 begin` through `// DUNE-SR-001 end`: `warnedDeep`, `pendingDeepEntry`, `deepReturnFocus`, `requestDeepConsent(action)`, `finishDeepConsent(accepted)`, click/cancel/close listeners; saved Deep mode resets to Essential **without changing lastScreen**.
- `setMode`: guards Deep **before any mutation**, revokes `warnedDeep` on downgrade. `goToId`: checks target level before automatic mode raising. `goToPosition`: checks candidate before moving. `contentsHtml`: filters level 3 while unacknowledged for **both** mobile dialog and desktop rail.
- Existing `renderCover` generic label and `start(continueSaved)` routing through guarded `goToId`; retain stable IDs and `deep-warning` in the sequential story. No consent token enters local/session storage.

Installed `connectSettingsRuntime` recognized the current `els.themeButton` handler in an in-memory check. It preserved every listed function, dialog/guard and corpus byte-for-byte while adapting only the theme handler. Accepted Settings/fonts still belong to parent/publisher; the final synchronized root reader must repeat consent/cancel/downgrade/reload/resume checks. No shared/installed file was modified here.

## Verification and handoff

- **69 structural checks**, no warnings/failures.
- Four real Chrome viewports, RU/EN × light/dark × all modes, **1,040 rendered route visits**; exact titles, complete body and counters, every body tail reachable, no horizontal overflow. Embedded media/fonts decode.
- 320/1440 consent/focus/navigation/source suites; all **42** (21 per language) saved Deep targets tested through cancellation and renewed acceptance; actual offline file reload and storage denial. Zero runtime page errors or external runtime requests.
- Settled cover/gate/dense/tail/settlement captures at all four widths; 320/desktop representative screenshots inspected. Initial screenshots caught fade-in; the final visual phase waits for the existing animation. No production animation/CSS change was necessary.
- Each Chrome had `timeout 30`, fresh unique profile, owned process group; all profiles removed, owned-process scans zero. No server or shared preview tools.

Detailed current receipts and screenshots are external: `/var/folders/78/c4cjg2412cjc0sxqpcm986rc0000gn/T/dune-substantive-pass2-z3eyjb66`. `QA.md` is the canonical readable test summary. Original pre-pass four files, ready manifest and review hash snapshots are preserved externally there; the pre-existing whole-library baseline is untouched.

Only authorized writes: four Dune canonical files, this report, own repair JSON and `ready/dune.json`. Original independent reviews and older Dune reports/acquisition record stay read-only. No root/catalogue/shared-shell/LOG edit, Git, PR, deployment, outbound messaging, subagent or waiting on another worker.

Remaining limits: independent content/source review pending; no continuously read complete edition/published translation, no physical iPhone/Safari verification; final shared Settings integration is publisher-owned. No publication is authorized by this ready record.
