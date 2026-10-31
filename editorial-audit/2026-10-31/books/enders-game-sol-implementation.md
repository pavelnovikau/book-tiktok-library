# Ender’s Game — Sol implementation handoff

2026-10-31. Verdict: **new approved-title build / REBUILD of the requested experience**. This is an implementation handoff, not an independent content PASS or publication certificate. This working report contains spoilers.

Owned package: `collector-output/enders-game/`. Report: this uniquely named file. Ready record: `editorial-audit/2026-10-31/ready/enders-game.json`, to be written only after the final local checks. Root readers, catalogue, index, shared shell, installed skills, logs, Git, PRs, deployment and external messages are outside this worker’s changes.

## What was read and built

The assigned title was already approved in BOOK_PLAN.md’s fiction queue. There was no previous `enders-game` collector package or published root reader to audit: **0 old pairs read**. A new original RU/EN condensation was written as eleven connected manuscript paragraphs per language, then divided into narrative beats. An initial forty-screen split exposed a seven-word arrival screen; that fragment was merged into the departure scene. The exact resulting counts are **Essential 16 / Core 25 / Deep 39**, comprising 16 level-1, 9 level-2 and 14 level-3 screens. No historical screen quota was preserved or padded.

All 39 final RU/EN pairs were read during the authoring/effective-corpus check, including the cover and shared final. The resulting Essential, Core and Deep sequences were followed continuously: **80 mode-pair appearances / 160 language appearances**, with 39 unique pairs / 78 language texts. The generated HTML’s embedded screens and all canonical authoring fields equal story-data.json; the exported reading routes are derived from that effective corpus. This counts implementation reading, not independent literary review or translation certification.

The story follows the monitor and Stilson, Peter and Valentine at home, Graff’s recruitment and shuttle isolation, the computer jokes, Alai and zero gravity, the Giant, Petra/Bonzo and Dink, the siblings’ net identities, Valentine’s letter, Dragon/Bean and rigged matches, the showers, the lake and renewed departure, Command School and its strain, and—only in warned Deep—the decisive mechanisms, ending and coda. Actions, relationships and consequences carry the prose. There are no leadership lessons, exercises, invented conversations, added management analogies or compulsory moral ending.

## Source identity and scope

This is the **1985 novel**, not the 1977 short story, film or sequel. The exact first printing was not consulted. The direct opening excerpt is Tor Teen 2013 / ISBN 9780765337320, supplied with Tom Doherty Associates / Dial-A-Book permission; it is novel text despite movie tie-in packaging. Primary passages quoted in the Halmstad thesis are identified as Starscape 2002. The April 2004 Hatrack and 2007 named GradeSaver guides support the original novel’s coda before later sequel retellings.

A read-only Apple Books metadata search checked 218 candidate OPF records in expanded and archived EPUBs and found no exact title/author edition. No target OPF/spine/body was therefore available to classify. No unrelated filenames or private full text have been put in the package. No purchases, loans, login, credentials, subscription changes or unofficial full-text downloads were used.

The evidence basis is deliberately narrower than whole-book reading: a publisher-authorized first chapter; official author/publisher guide/commentary; selected actual novel quotations in a named university-repository essay and Kessel’s published criticism; detailed accountable chapter accounts; and actual primary passages reproduced in the named GradeSaver guide at the decisive hinges. Teacher questions are not answers. Critical judgments were not silently turned into Card’s narrative or a final moral verdict.

Detailed support and limits:

- `collector-output/enders-game/sources.md` — 24 source entries, roles and consultation boundary.
- `collector-output/enders-game/evidence/primary-hinges.md` — exact checked hinges and edition/quotation-wrapper distinction.
- `collector-output/enders-game/evidence/screen-map.json` — all 37 narrative pairs mapped to retained propositions, source IDs and original chapter locations.
- `collector-output/enders-game/evidence/manuscript-ru-en.md` — connected prose before segmentation; an initial draft, with subsequent corrections recorded below.
- `collector-output/enders-game/evidence/routes-ru-en.md` — all final effective reading routes.

No complete novel was fetched or read continuously. For the retained story there is no identified missing essential action/causal link after the targeted checks; that is not a certification of omitted material or every wording of the novel. A reviewer can inspect and challenge every guide-backed link separately.

## Concrete editorial choices and corrections

| Stable ID | Earlier draft problem / risk | Final handling and evidence |
| --- | --- | --- |
| `peter`, `bedside` | Valentine’s sibling relationship was implicit; Peter could become a flat villain. | Explicit sister introduction, actual protective intervention, and the night apology without claiming to know Peter’s motive. Primary quotation in Lindberg, novel p.15; chapter-2 account. |
| `letter` | RU draft said «всё хуже хочет жить своей жизнью», an awkward overstatement compared with EN. | «Военная учёба идёт всё успешнее, но Эндеру всё тяжелее»; matches the EN burden of training and the chapter-9 account. No diagnosis or invented suicidal intent. |
| `floating` | Draft’s «не за что держаться» was unnecessarily literal. | «нет привычного верха и низа» in both languages; no invented room fittings or restraint mechanism. |
| `bean`, `rigged-matches` | English nickname intruded into RU; short-route name lacked an introduction. | Consistent RU Боб / EN Bean; named as a soldier when first appearing in Essential. Ender recognizes his own repetition of Graff’s treatment, with no instruction to the reader. |
| `one-more-battle` | Draft used «уничтожением солдат» for a training game, and the gate tactic needed an actual answer source. | «замораживанием» / freezing; checked the final ritual win against GradeSaver chapters 11–12, not a teacher’s prompt or the film’s simplified condition. |
| `lake`, `valentine-asks`; removed `eros` fragment | Essential skipped the transfer antecedent; Eros had a seven-word stand-alone screen. | Command School destination introduced at the lake transition; Eros arrival/training joined to the renewed departure. Derived counts changed 17/26/40 → 16/25/39. |
| `showers` | Dink was named before a relationship was given in Essential. | Explicitly identified as Ender’s friend/companion; primary remorse passage and chapter-12 account retained. No disclosed death in shallow routes. |
| `last-exam` | A generic triumphant summary would falsify Ender’s motive. | Actual wish to break the rules so he can stop commanding; checked the quoted primary interior passage reproduced in the chapter-14 guide. Planet/weapon/outcome only in Deep. |
| `explanation`, `adults-answer` | Adult justification could be presented as the reader’s final moral. | Actual backlash and adult explanation attributed to their speakers. Sources distinguish primary emotional passage from guide context; no imposed absolution. |
| `familiar-landscape` | Film/sequel contamination and unexplained recognition were particular risks. | Years later on the colony, not Eros; Ender’s conclusion about ansible contact is explicit. Primary cocoon/queen passages in chapter-15 guide plus the separate chapter account. |
| `queen`, `two-books`, `long-search` | A capsule ending could imply the queen is already restored, or drop the Peter relationship. | The cocoon stays with Ender; Peter’s conversation precedes the posthumous book; search remains unresolved. No sequel resolution. |
| `final` and global notes | Shared final, contents or resume could leak the ending. | Navigation-only shared final; neutral source notes warn about external spoilers. Deep titles are absent until consent, and remembered Deep has a generic resume label. |

## Build and local verification

Built from clean schema-v2 data with the maintained `skills/book-tiktok/scripts/build_story.mjs`; audited with its maintained `audit_story_html.mjs`. No copied reader or unmerged Settings/Geist code. `contentMode: narrative` removes per-screen source chrome while keeping the global Sources dialog and embedded source map.

Two bounded book-local adaptations are reproducible in `collector-output/enders-game/qa/build.mjs`: explicit Deep consent on mode/resume entry, renewed after reload/downgrade; and a plain title page replacing the shell’s generic analytical seven-node illustration. The maintained compact icon header, embedded fonts, Flexoki palette, focus behavior and iOS guide are inherited. Shared files were not edited. Settings PR29 remains a separate publisher/integration concern.

Final technical results and hashes are recorded in QA.md, `qa/audit.json`, `qa/consistency.json`, `qa/checks-*.json`, `qa/browser-*.json` and the ready record. The local browser matrix covers 320×568, 390×844, 1024×768 and 1440×900, RU/EN, dark/light and all three modes; all selected screens are traversed. Native consent, saved resume, language/theme preservation, Sources/Contents, focus and navigation are checked separately. Offline tests use file URLs, embedded fonts, and no server. Emulated iOS/safe-area checks do not claim a physical iPhone/PWA test.

Final local results: **69 structural checks**, no warnings/failures; **48 browser combinations / 1,280 screen renders / 99 assertions**, all successful for the final HTML hash; no runtime exceptions or external runtime requests. Six final-hash browser runs were cleaned. Dense/mobile/cover/source-dialog/desktop representative screenshots were inspected. The current version’s counts remain 16/25/39; no publication or independent acceptance is implied by these technical results.

Initial local test harness corrections are retained as superseded `qa/failure-*.json` evidence: a 4-second CDP timeout was too short for an entire traversal; an overflow assertion measured the shell’s in-flight 180 ms translation; a focus assertion expected visibility:hidden instead of the maintained display:none. The final harness waits appropriately, measures settled content and checks the real hiding contract. These were corrected test assumptions, not unexplained waived product failures.

All manually launched Chrome runs have a separate owned mkdtemp profile, a hard `timeout 30`, and process-group/profile cleanup. No server or preview_* tools were used. The final manifest must bind the final HTML/data/report hashes and remain **ready-for-independent-check**.

## Remaining limits / publisher handoff

Independent content acceptance is pending. Whole-novel continuous reading, first-printing collation and a professional translation certificate are not claimed. Publisher owns accepted shared Settings/font integration, real iPhone/PWA verification, root-reader/catalogue/progress integration, release checks and publication. This worker changed none of those shared/release surfaces and sent no external messages.
