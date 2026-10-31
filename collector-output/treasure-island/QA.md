# Treasure Island — QA report

Post-review integration note (2026-10-31): corrected three primary-text locators (`geography-makes-action`, `women-at-edge`, `opening-ending-mirror`), strengthened the bilingual treatment of Silver’s wife and the novel’s racial prejudice, and clarified the spoiler-light promise as early plot revelations without the ending. The maintained library shell restores the bilingual iOS installation guide; cover focus is explicitly exempted; native Space activation on interactive controls is preserved. Counts remain **24 / 60 / 96**; the current deterministic audit reports **6,359 RU / 7,366 EN words**.

Date: 2026-10-31. Original collector result: **PASS** for the authored corpus, deterministic audit and isolated Chrome matrix. The later cold-review corrections and maintained library shell were re-audited at integration: **68 passes, 0 warnings, 0 failures**; the catalogue browser QA also passed. The detailed matrix below records the collector run and is not presented as a fresh traversal after the editorial corrections.

## Deliverables and scope

- `story-data.json`: schema v2 authoring corpus, exact `targetModes` 24/60/96.
- `treasure-island.html`: standalone, embedded Geist and Geist Mono, no runtime network dependency. RU/dark/Essential fresh default; complete EN parity and Flexoki light/dark.
- `sources.md`: seven-source ledger, narrative/claim map, locators and explicit research limits.
- `QA.md`: this report and all-screen editorial ledger.

All task writes are confined to this collector directory, apart from bounded temporary Chrome profiles which were removed. No shared catalogue, root reader, shared template, LOG.md, deployment, push or PR was changed by this task. Hidden files hold local authoring/finishing code, QA code, reports and representative screenshots. Temporary primary-text research downloads were removed; no copied chapter is a deliverable.

## Count and density contract

| Cumulative mode | Screens, including cover/final | RU words | EN words | RU time | EN time |
|---|---:|---:|---:|---:|---:|
| Essential | 24 | 1,550 | 1,780 | 9 min | 9 min |
| Core | 60 | 3,853 | 4,477 | 22 min | 21 min |
| Deep | 96 | 6,339 | 7,340 | 36 min | 34 min |

Word totals above use the maintained **builder** definition: title + optional subtitle + body, excluding section labels, source notes and interface. Reading-time estimates use the builder's 180 RU / 220 EN words per minute; they are mechanical estimates, not tested reading times for every 14-year-old. Deep is 13,679 bilingual words in total. Body-only totals are RU 5,823 / EN 6,693; means 60.66 / 69.72 words per screen, ranges 37–71 / 43–80. This is dense original paraphrase, not copied text.

The deterministic **auditor** reports RU 6,333 / EN 7,333 because its counter omits the cover subtitle (6 RU / 7 EN words). This is a tool counting difference, not missing content. Raw levels are 24 level-1 + 36 level-2 + 36 level-3; first cover and last final are level 1. One stable ID, level, evidence kind, source set and narrative job serves both languages.

## Spoiler boundaries

- Essential contains premise, early discoveries, themes and craft, with no treasure outcome, late manoeuvres or final character fates.
- Core may reveal Parts I–IV, including the mutiny and stockade attack (chapter XXI). Its post-attack screens discuss earlier material and craft. It does not continue Jim's sea adventure or resolve the search.
- Deep's bilingual warning is raw screen **60**, before the full continuation at screen 61. A separate native bilingual consent dialog also guards choosing Deep, hidden Deep chapters, saved-position Continue and forward navigation. Cancel leaves current text intact. Reader keyboard navigation is suspended while the warning is open.
- Later chapter titles and remembered spoiler-bearing titles are masked until consent. Downgrading to Core/Essential relocks the full-spoiler layer. A fresh page load requires fresh consent even for saved Deep progress.
- The shared final is safe in every mode. Sources dialog notes are non-revealing. External source links may expose spoilers, as the bilingual method disclosure states. Embedded JSON and authoring/research files are not a security boundary against intentional inspection.

## Evidence and fidelity

Seven sources: 1 primary novel + 2 primary author essays + 4 museum/library/specialist reference pages. Source attachment counts: novel 85; composition essay 6; romance essay 2; historical piracy 2; pirate myths 2; Glasgow map account 1; works chronology 2. Some screens cite more than one source. Evidence labels: plot 51, interpretation 28, historical context 5, author testimony 3, synthesis/framing 9 (including cover).

The lawful primary text was consulted through openings/endings of all 34 chapters and targeted decisive passages, not a claimed fresh line-by-line reading of the whole novel. The composition essay was read in full; relevant romance-essay passages and institutional reference sections were consulted. The source ledger gives the exact limits. No invented pages, exact in-world date, confirmed post-escape Silver biography, diagnostic certainty or map identification is supplied.

Editorial review checked RU and EN together for equivalent events, qualifications, names and causal order. It preserves Jim's impulsiveness and luck; Silver's real charm, murder and concrete protection; navigational/material limits; the changing value of the map; Ben's independent labour; the temporal reveal; and the novel's uneasy ending. Violence is plain and consequential without graphic elaboration. Historical practice, author testimony and our inference remain distinguishable.

There is no edition/publisher art, no copied chapter and no long quotation. Images/archival image decoding cases are not applicable: the original cover is typography. Prose is the main story form; the long list tested visually is the source dialog.

## Build and deterministic audit

```sh
python3 .author.py
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs story-data.json --out treasure-island.html
python3 .finish.py
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs treasure-island.html --min-screens 96 --require-bilingual
```

The maintained builder creates the artifact. `.finish.py` changes this output only: a typographic cover replaces the shell's generic model graphic; visible provenance gains fiction-appropriate labels and locators; hidden chapters can raise depth with spoiler gating; cover layout and focus counter visibility are corrected locally; the requested royal-violet palette is restored independently of the shared shell's library skin; a library installation prompt is removed from this standalone collector. It does not edit the builder or shared template.

Latest deterministic audit: **68 passes, 0 warnings, 0 failures**, exact 96 corpus screens and 24/60/96 cumulative modes. Audit evidence: `.audit.json`.

## Real-browser matrix

Each row represents 3 modes × 2 languages × 2 themes. Every visible screen was traversed through rendered reader controls and checked against its expected ID, title and counter. Cover/final are included. Every top control was checked inside the viewport; story/body paragraph widths and document/slide horizontal overflow were measured on every traversal.

| Viewport | Combinations | Screen renders | Result |
|---|---:|---:|---|
| 320×568 | 12 | 720 | PASS |
| 390×844 | 12 | 720 | PASS |
| 1024×768 | 12 | 720 | PASS |
| 1440×900 | 12 | 720 | PASS |

Total: **48 combinations, 2,880 screen renders**, zero horizontal-overflow findings and zero runtime exceptions. Individual screen measurements are retained in `.qa-320.json`, `.qa-390.json`, `.qa-1024.json` and `.qa-1440.json`.

At every viewport the interaction run also checks fresh defaults, embedded fonts, violet action token, locked chapter titles, bilingual warning/cancel, hidden-screen mode raising, language/theme position preservation, rapid switches, sources/contents dialogs, saved Deep title masking, gated Continue after reload, Start over, button and ArrowRight navigation, pointer tap focus, horizontal swipe while focused, rejection of vertical movement as a page/tap, Escape/F, modal keyboard guarding, dense-screen locator reachability by vertical scrolling, cover CTA reachability and final restart. Desktop additionally checks a visible, scrollable rail and active-chapter visibility. All network requests were file/data only. Both WOFF2 files were separately checked for Cyrillic Я and ё coverage with fontTools.

Representative **actual Chrome screenshots** were visually inspected at all four widths: cover, cover controls after vertical scroll, spoiler warning, dense English scene, its bottom/source locator, final, focused reading and source dialog. The 320px dense text remains readable and intentionally scrollable; no fit-by-font-shrinking was used. At 1024/1440 the story column and persistent rail fit without cover overflow. Initial transitional screenshots were retaken after animation completion. A shared-shell palette change discovered visually was fixed locally and the whole matrix rerun. An early QA helper disappeared on reload; the test harness was corrected and passing reports supersede that failed test run.

Chrome was launched under `timeout 30`, with a dedicated debugging port and a fresh `mktemp -d` profile for each run. Only the owned process group was terminated. Every report records `profileRemoved: true`; a post-run inventory found no `treasure-qa.*` profile or Chrome process using one. No local server or Vite process was started. No collaborative preview was used.

## Every-screen editorial inspection

All 96 RU/EN screen pairs were inspected for a distinct job, chronological/source fidelity, unnecessary splitting and spoiler placement. The ledger below records the reason each remains. Related screens have different jobs: the two black spots are first intimidation versus contested command; the map's arrival, empty pit and reconstructed chronology are distinct stages; Silver's first appeal, tactical help and non-acquittal are different evidentiary moves. Framing/count guidance, safe stopping, warning and final have necessary reader functions rather than adding invented plot. No duplicated narrative beat is used merely to make the target count.

| # | ID | Level | RU / EN body words | Editorial job / duplication check |
|---:|---|---:|---:|---|
| 1 | `cover` | 1 | 37 / 43 | Cover establishes desire and explicit depth promises. |
| 2 | `reading-pact` | 1 | 53 / 61 | Route contract explains counts and the four evidence labels. |
| 3 | `door-to-adventure` | 1 | 53 / 62 | The unfamiliar guest changes the safety of home. |
| 4 | `billy-bones` | 2 | 54 / 62 | Bones combines intimidation with fear of former associates. |
| 5 | `jim-before-hero` | 2 | 57 / 68 | Jim's ordinary work explains his access to adult information. |
| 6 | `one-legged-nightmare` | 2 | 53 / 61 | An identifying silhouette creates expectation before a meeting. |
| 7 | `black-dog-returns` | 2 | 55 / 65 | Black Dog makes an old connection an immediate threat. |
| 8 | `livesey-refuses` | 2 | 57 / 64 | Livesey supplies calm professional resistance rather than bullying. |
| 9 | `first-black-spot` | 2 | 56 / 66 | The first spot imposes urgency; paper is not a magical cause of death. |
| 10 | `two-deaths` | 2 | 56 / 73 | Bereavement changes the starting home without turning the novel into grief instruction. |
| 11 | `mothers-fair-share` | 1 | 55 / 65 | A specific debt establishes a risky boundary on taking money. |
| 12 | `chest-has-records` | 2 | 55 / 70 | The packet makes information more important than visible coin. |
| 13 | `escape-from-inn` | 2 | 55 / 64 | Escape requires outside help; the map is not a superpower. |
| 14 | `map-promises-world` | 1 | 60 / 65 | The chart makes a destination and funded voyage imaginable. |
| 15 | `flint-without-presence` | 2 | 59 / 65 | An absent dead captain still shapes behaviour through interested accounts. |
| 16 | `desire-is-contagious` | 1 | 58 / 69 | Shared desire joins people whose motives differ. |
| 17 | `trelawney-tells` | 2 | 58 / 62 | Expedition resources do not compensate for failed secrecy. |
| 18 | `bristol-opens` | 1 | 56 / 72 | Bristol earns the reader's desire to depart through Jim's excitement. |
| 19 | `silver-first-meeting` | 1 | 57 / 69 | The first pleasant meeting tests the nightmare's simple identifying sign. |
| 20 | `crutch-is-not-character` | 2 | 63 / 72 | Physical impairment is separated from moral character. |
| 21 | `parrot-and-money` | 2 | 56 / 66 | A repeated sound links comic shipboard life and money imagery. |
| 22 | `smollett-unpopular` | 1 | 58 / 67 | Unpopular practical competence challenges easy liking. |
| 23 | `ship-small-world` | 2 | 58 / 66 | Spatial confinement makes shipboard access and trust consequential. |
| 24 | `voyage-rhythm` | 1 | 65 / 67 | Voyage routine creates attachments before the decisive discovery. |
| 25 | `routine-has-cracks` | 2 | 55 / 62 | Arrow exposes cracks without inventing an unshown murder. |
| 26 | `apple-barrel` | 1 | 58 / 68 | The barrel supplies the first major reversal through accidental overhearing. |
| 27 | `silvers-long-game` | 2 | 61 / 69 | Silver's delayed rebellion reveals strategic patience, not kindness. |
| 28 | `mutiny-means-control` | 2 | 61 / 75 | Mutiny is explained as control of a ship and its necessities. |
| 29 | `secret-council` | 2 | 59 / 71 | Adults must use a child's incomplete evidence discreetly. |
| 30 | `unequal-knowledge` | 1 | 61 / 73 | Unequal knowledge explains suspense without constant fighting. |
| 31 | `island-not-postcard` | 1 | 60 / 67 | Sensory landfall defeats the map-as-holiday fantasy. |
| 32 | `shore-leave` | 2 | 57 / 64 | The shore-leave decision separates groups and Jim acts without orders. |
| 33 | `tom-refuses` | 2 | 57 / 67 | Tom's refusal exposes coercion and murder; Alan is reported, not witnessed. |
| 34 | `danger-has-weight` | 1 | 64 / 73 | The physical cost of fear preserves adventure's stakes without graphic detail. |
| 35 | `ben-gunn-appears` | 2 | 63 / 72 | Ben introduces an independently situated person outside shipboard calculations. |
| 36 | `cheese-and-company` | 2 | 63 / 73 | An ordinary craving gives isolation a human scale, not a second plot recap. |
| 37 | `marooning-defined` | 2 | 58 / 61 | The historical term clarifies punishment without historicising fictional Ben. |
| 38 | `doctor-takes-pen` | 1 | 61 / 65 | A narrator switch covers genuinely separate action with limited witnesses. |
| 39 | `water-and-stockade` | 2 | 58 / 66 | Water and timber define what refuge actually provides. |
| 40 | `overloaded-jolly-boat` | 2 | 59 / 67 | Boat capacity and current change the defenders' material resources. |
| 41 | `flag-has-two-effects` | 2 | 57 / 67 | One flag has both rallying and targeting consequences. |
| 42 | `gray-chooses` | 2 | 60 / 73 | Gray's decision prevents a frozen reliable/unreliable crew taxonomy. |
| 43 | `jim-rejoins` | 2 | 63 / 72 | Two separately narrated routes reconnect with both useful knowledge and anxiety. |
| 44 | `silvers-embassy` | 2 | 59 / 77 | Bargaining tests command before force is used. |
| 45 | `stockade-attack` | 2 | 56 / 69 | The assault establishes Core's exact stopping point without any later result. |
| 46 | `courage-feels-afraid` | 1 | 63 / 71 | Fear distinguishes courage from emotional invulnerability. |
| 47 | `loyalty-and-obedience` | 1 | 65 / 72 | Loyalty is separated from obedience without recommending recklessness. |
| 48 | `greed-not-one-uniform` | 1 | 61 / 71 | Desire for money is examined through limits, not good/bad money stereotypes. |
| 49 | `silver-double-vision` | 1 | 63 / 67 | Silver's appeal is kept distinct from evidence of reliability, without later fate. |
| 50 | `geography-makes-action` | 2 | 60 / 69 | An author essay supports a bounded reading of place-specific incident. |
| 51 | `sound-before-sight` | 2 | 64 / 76 | Acoustic restriction makes the unseen a different craft mechanism from geography. |
| 52 | `older-jim-telling` | 2 | 64 / 72 | Retrospective voice is distinguished from the younger experiencing perspective. |
| 53 | `women-at-edge` | 2 | 62 / 71 | The chosen gender boundary is noticed without cancelling enjoyment or universalising it. |
| 54 | `two-historical-clocks` | 1 | 59 / 70 | Story time, writing time and contextual period are separated. |
| 55 | `pirate-myth-boundary` | 2 | 59 / 65 | Museum context limits the treasure-map myth without criticising fiction for being fiction. |
| 56 | `story-begins-as-map` | 1 | 58 / 67 | Institutional and author testimony explain the map's generative role. |
| 57 | `serial-and-cliff-edge` | 2 | 63 / 68 | Serial publication supplies a reading context without a monocausal cliffhanger claim. |
| 58 | `read-with-three-questions` | 1 | 64 / 70 | Three reading questions are explicitly the digest's approach, not author instructions. |
| 59 | `safe-place-to-stop` | 1 | 67 / 74 | Safe stopping point protects first-time readers; this transition is functional. |
| 60 | `spoiler-warning` | 3 | 65 / 65 | Bilingual full-spoiler warning is functional and precedes every Deep-only narrative event. |
| 61 | `coracle-plan` | 3 | 62 / 68 | The second unauthorised departure introduces the coracle and its risks. |
| 62 | `cutting-hawser` | 3 | 63 / 74 | Cutting a cable achieves one aim while surrendering control to the tide. |
| 63 | `coracle-at-sea` | 3 | 60 / 71 | Learning the coracle restores physical scale and environmental indifference. |
| 64 | `aboard-hispaniola` | 3 | 63 / 65 | Boarding trades isolation for dependence on a dangerous specialist. |
| 65 | `hands-bargain` | 3 | 63 / 75 | Hands's useful expertise and hidden knife make temporary cooperation unstable. |
| 66 | `hands-confrontation` | 3 | 64 / 74 | Failed priming, the knife and involuntary shots preserve the actual sequence. |
| 67 | `wrong-camp` | 3 | 65 / 76 | A familiar refuge has changed while Jim was elsewhere. |
| 68 | `silver-protects-jim` | 3 | 62 / 72 | Silver's protection creates a concrete reciprocal need without moral conversion. |
| 69 | `jim-tells-truth` | 3 | 64 / 75 | Confession is Jim's risky remaining agency in captivity. |
| 70 | `second-black-spot` | 3 | 59 / 71 | The second spot shows contested group authority rather than repeating the first fright. |
| 71 | `parole-and-promise` | 3 | 65 / 77 | Parole turns an inconvenient promise into a specific choice. |
| 72 | `doctor-map-bargain` | 3 | 65 / 75 | The doctor's inexplicable concession establishes a new information gap. |
| 73 | `skeleton-pointer` | 3 | 62 / 72 | The skeletal pointer makes navigation materially inseparable from prior violence. |
| 74 | `voice-among-trees` | 3 | 60 / 74 | The voice is a deliberate delaying action, not a confirmed ghost. |
| 75 | `empty-excavation` | 3 | 61 / 73 | The empty pit reveals a changed situation rather than an inherently false map. |
| 76 | `ambush-at-pit` | 3 | 61 / 63 | An unseen allied plan intervenes before the mutineers' retaliation. |
| 77 | `bens-hidden-work` | 3 | 63 / 76 | Ben's earlier labour explains the actual treasure location and the map's lost value. |
| 78 | `chronology-versus-discovery` | 3 | 64 / 70 | Reconstructing chronology distinguishes prior events from later knowledge of them. |
| 79 | `cave-is-not-pit` | 3 | 62 / 66 | The cave offers relief and raises the hoard's previous human cost. |
| 80 | `leaving-three-behind` | 3 | 60 / 74 | Leaving three men supplies an ethically uncomfortable departure rather than a clean celebration. |
| 81 | `silver-slips-away` | 3 | 65 / 76 | Silver's escape and the narrator's later speculation are explicitly separated. |
| 82 | `jim-does-not-return` | 3 | 65 / 78 | Arrival, refusal to return and nightmares preserve the novel's actual last emphasis. |
| 83 | `ending-has-two-truths` | 3 | 63 / 70 | A psychological reading is bounded by details, expressly not a diagnosis. |
| 84 | `silver-without-acquittal` | 3 | 66 / 73 | Specific gratitude is distinguished from acquittal using opposed textual evidence. |
| 85 | `smollett-final-judgement` | 3 | 64 / 73 | The captain's assessment contrasts collective dependability with successful individual risk. |
| 86 | `different-futures` | 3 | 66 / 72 | Different later uses of money are reported without turning them into a universal deservingness law. |
| 87 | `coins-have-weight` | 3 | 62 / 67 | Transport and sorting give wealth weight, labour and a change of narrative rhythm. |
| 88 | `who-paid-for-gold` | 3 | 68 / 77 | The hoard's victims are considered without inventing a complete ownership history. |
| 89 | `borrowed-adventure-materials` | 3 | 71 / 80 | Authorial literary debts describe a tradition and transformation, not wholesale copying. |
| 90 | `lost-map-rebuilt` | 3 | 65 / 73 | Reconstruction reverses the map/text relation and acknowledges a missing original. |
| 91 | `silver-model-not-identity` | 3 | 65 / 78 | A composite character is distinguished from a biographical identification the essay does not name. |
| 92 | `no-curse-required` | 3 | 64 / 76 | Human mechanisms explain apparently supernatural power without dismissing experienced fear. |
| 93 | `opening-ending-mirror` | 3 | 64 / 70 | Opening/ending comparison tracks changed meanings rather than retelling the ending again. |
| 94 | `what-remains-unknown` | 3 | 65 / 79 | Named gaps prevent adaptations and speculation from silently filling the text. |
| 95 | `reread-one-scene` | 3 | 63 / 70 | A particular rereading task revisits first impressions rather than repeating a plot beat. |
| 96 | `final` | 1 | 68 / 77 | Mode-safe final returns to the novel and preserves its uncertainty and pleasure. |

## Final artifact identity

- `story-data.json`: 183,455 bytes; SHA-256 `24a7c8e40ed4b8f1971432dceaa76d667f94a2b84f26fbe2a1621bc5dfe21055`.
- `treasure-island.html`: 420,769 bytes; SHA-256 `76f05aa1a8e0bacbc4fced259dd35883f9d328e9f921c689aafb6867d43f843a`.
