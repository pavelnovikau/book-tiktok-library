# To Kill a Mockingbird — Sol implementation handoff

2026-10-31. **NEW BUILD / ready-for-independent-check.** The user already approved this title; it replaces the completed Neverending Story source-search slot. No new title approval was requested or inferred. This report contains ending information for the independent checker.

Canonical folder: `collector-output/to-kill-a-mockingbird/`. Four canonical files: `story-data.json`, `to-kill-a-mockingbird.html`, `sources.md`, `QA.md`. `source-evidence-map.json` covers all 41 pairs; `prose-first.md` preserves the connected bilingual manuscript before segmentation. Build and QA tools/proofs stay in the same folder. The ready manifest supplies exact SHA-256 hashes and paths.

## What was actually read

No existing Mockingbird draft/root reader was present: old unique pairs read **0**, old collector **0**, old production **0**. New pairs written/read **41** (82 RU/EN texts), with all 41 effective HTML pairs read and checked for equality to authoring data. The four subsequently revised pairs were read again in effective HTML. Essential/Core/Deep routes were checked for continuous relationships and stopping points; repeated appearances are not counted as new unique pairs.

The work is Harper Lee’s **1960 novel**, excluding the film, stage texts and *Go Set a Watchman*. No complete novel or published Russian translation was read. Exact title/author matching in read-only Apple Books OPF metadata found no target among 216 expanded-EPUB records; no matching spine was available to classify as full, abridged or summary. No unrelated filenames or text were exposed.

Evidence comes from the official DBE 117-page *Mind the Gap* guide (ISBN of guide 978-1-4315-1942-2), its permission-labelled Vintage novel passages, the HarperCollins permission-labelled chapter-one opening at eCampus (novel ISBN 9780060935467), the primary chapter-23 conversation hosted by National Constitution Center, and NEA’s official reader guide p.3. The exact primary passages read and the guide-only links are listed in `sources.md` and mapped per screen. Teacher prompts were not treated as evidence by themselves. The complete final chapters were not read in primary form; the guide explicitly supplies their retained actions.

The consulted guide plus primary hinges supports this particular retained chain. No unresolved essential event/motive/causal-link gap has been identified for that chain. This is a reason to submit it to independent checking, not a whole-book fidelity certificate. No full-text reading, authorised translation or independent PASS is claimed.

## Narrative implemented

Original concise prose follows Scout/Jem/Dill’s interest in Boo through the gifts, trousers and blanket, then the hostility around Atticus’s defence, the jail night and courtroom. Core expands the school/household, Dubose, Calpurnia, Alexandra and Raymond episodes. Deep alone supplies the verdict, the conflicting responses, Tom’s death, continued threats, Halloween attack, recognition, sheriff’s decision and porch return. Every event belongs to the novel; no contemporary analogy, invented scene/dialogue or lesson about the reader’s life was substituted for it.

Moral complexity remains inside the actions: Jem’s anger and Atticus’s admiration at Dubose; the church objection and welcome; Raymond’s chosen pretence; Maudie’s tentative hope against Jem’s outrage; the teacher’s incompatible claims; and the sheriff’s protection of Boo after the court failed Tom. Guide interpretations are not assigned to an omniscient narrator as authorial intent.

The preserved manuscript produced **14 Essential / 28 Core / 41 Deep** screens (14/14/13 by level), cover/final included. No historical quota was retained. Approximate reading: RU 4/7/9 min, EN 4/7/10 min. `contentMode: narrative`, RU/dark/Essential defaults, offline embedded fonts, Flexoki neutral themes, royal-violet focus action and maintained icon-only header.

## Concrete implementation findings and corrections

No legacy wording is fabricated for a new title. These are findings in the authored draft or consulted material, corrected before handoff:

| Stable ID | Finding / earlier wording | Correction and support |
|---|---|---|
| `cunningham` | The shallow route said “отца Уолтера Каннингема” although its school/lunch inserts were absent. Broken antecedent. | Introduced Walter as Scout’s classmate in the same screen; [DBE pp.27, 59, 61](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=75). |
| `first-day` | “почему Уолтер Каннингем не принимает денег” omitted the poverty cause. | Explicit lack of money for lunch; [DBE pp.25–27](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=42). No unsupported new loan speech. |
| `mockingbirds` | “другое его предупреждение / another warning from him” depended on an omitted Core beat. | Self-contained air-rifle gift and Atticus warning; [DBE p.46, including actual chapter-10 quotation](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=62). |
| `outside-the-jail` | Crowd demanded the doorway but its purpose was too implicit in the short route. | Stated the threat to Tom; [actual chapter-15 extract, DBE p.59](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=75), and [NEA p.3](https://www.arts.gov/sites/default/files/Reader-Resources-ToKillaMockingbird.pdf#page=3). No deliberate psychological tactic assigned to Scout. |
| `interrupted-afternoon` | “приходит / he arrives” lost its antecedent when the father/son insert was reordered. | Explicitly named Atticus in both languages; [DBE p.82](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=98). |
| `the-next-morning` | “долго спорили / argued for a long time” sounded like witnessed jury-room knowledge. | “совещались / deliberated”, with Maudie’s hopeful assessment kept hers; [DBE p.81](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=97). |
| `the-injured-arm`, `toms-account` | Risk of inheriting guide compression as certainty: physical impossibility, or Tom witnessing Bob’s beating. | Injury is a defence inference; Tom’s account is attributed; no witnessed beating is asserted. [DBE p.69 and p.81](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=85). The map openly labels this guide-supported hinge. |
| `sheriffs-account`, `another-porch` | Risk of treating the sheriff’s protective version as settled forensics, or inventing final dialogue from memory. | Preserved his insistence/protective function and the porch/domestic return only; [DBE p.96](https://www.education.gov.za/Portals/0/Documents/Manuals/MTG%20EFAL%20P2n%20TKAM%2019_01_2015%20WEB.pdf#page=112). Primary full chapters 30–31 remain unread; no exact last dialogue imported. |

Also excluded unchecked material/causal details, Bob’s suspected Taylor break-in and invented private thoughts. The NCC introduction calls the case a murder trial; only its actual chapter-23 excerpt was used. The guide’s “Aunt Agatha” typo, church formulation and necessary-arrest generalisation were not imported.

## Verification and remaining work

Maintained v2 build plus exactly scoped maintained shell application; no copied reader. Book-local consent/text-cover/token patch is reproducible in `build-local.mjs`. No shared Settings, font or UI implementation was edited. The first local colour-token check caught a CSS specificity conflict; corrected only the collector-local selector and reran checks against the resulting final hash.

The final artifact passes **69 structural checks** with no warning/failure. Seven offline file-based Chrome runs give **154 assertions**, **48 matrix cases** and **1,328 screen renders**, covering both languages/themes and all nested depths at 320×568, 390×844, 1024×768 and 1440×900. Actual body/title, counts, reachability and horizontal bounds are checked. Screenshots of cover, dense prose, desktop rail and iOS-safe-area view were visually inspected. No runtime exception or external runtime request. All owned profiles/processes removed; no server or preview tool used.

Book-local consent covers cover picker, contents, rail, direct ID, navigation and saved Deep resume; Deep titles are masked before consent, saved labels generic, and reload/downgrade revoke consent. Sources remain available globally without academic labels on narrative screens. Local browser proof includes focus, gestures, keyboard/buttons, language/theme stability, saved-position/restart and emulated iOS/standalone/inset behaviour.

**Pending:** independent review of every pair and its particular evidence; publisher integration with the separately repaired accepted shared Settings/font work, root/catalogue/index and final production/progress checks. Physical iPhone/PWA was not tested. Do not publish from this worker’s status alone.

Ownership observed: only `collector-output/to-kill-a-mockingbird/`, this report and `ready/to-kill-a-mockingbird.json` were written. No subagents, Git, PR, deploy, external messages, root reader, catalogue/index, shared shell, installed skill or log edits.
