# Nonviolent Communication — implementation record, 2026-10-31

Status: **ready-for-independent-check**. Implementation completed for this assigned book; independent editorial review and publication remain outside this worker’s authority.

## Starting state

`collector-output/nonviolent-communication` did not exist at assignment start. The slug appears in neither `books.json` nor the 41-record repair inventory. There are zero pre-existing authoring, embedded-delivery or draft RU/EN pairs for this new approved work. No root reader, catalogue, shared shell or shared log will be edited.

Read `editorial-audit/2026-10-31/BRIEF.md` first, including the source-sufficiency clarification. Applied the repository's maintained `skills/book-tiktok` workflow and its content, data and HTML references.

## Source discovery and boundary

Read-only assigned-title search of Apple Books: no Rosenberg / Nonviolent Communication / Ненасильственное общение title match in the top-level names or 217 EPUB package metadata documents. No unrelated book names were output. No owned full Rosenberg edition or Smart Reading condensation was found; no claim about a hidden or unindexed library item is made.

Lawful public sources were found on PuddleDancer Press and CNVC. They include the explicitly labeled second-edition first chapter, the third-edition chapter-2 sample carrying ©2019, official chapter-3, chapter-9, chapter-10 and third-edition chapter-14 excerpts, Rosenberg's four-component handout, and supplementary author explanations. These are actual primary passages, not an unverified recap. The new account will retain only their supported central method and verified book cases. It will not claim cover-to-cover reading, a single collated printing, fidelity to an official Russian translation, or exhaustive coverage of all third-edition chapters.

The publisher's old ISBN-specific third-edition bookstore URL currently displays an upcoming fourth edition (February 2027, ISBN 9781934336489). It is not used to certify the third-edition text. The third-edition label comes from the official excerpt itself and CNVC's identified third-edition cover. No fourth-edition additions are incorporated.

Direct command-line HTTP reads of the publisher returned 403; they were abandoned. Public primary passages were accessible through normal web retrieval. No credentials, loans, purchases, subscriptions, unofficial full books or access bypass were used. No copyrighted full text or extraction was written to this public repository.

The completed source ledger, evidence map, exact counts, checks and limitations follow. The detailed per-screen map is also in the canonical `sources.md`.

## Completed implementation — BUILD, new approved record

There was no old corpus on which to issue KEEP/EDIT/REBUILD. Implementation verdict is **BUILD** for this already approved new work. This is not a source-gap package: the particular retained arguments and cases have direct primary coverage. It is also not an independent PASS or a whole-edition fidelity certificate.

Authored and reread **all 30 new RU/EN pairs**; inspected the actual effective embedded corpus after building and confirmed equality with canonical screen copy, sources and method note. Unique old pairs read: **0**, because this slug had neither a collector nor a published root reader at assignment start. No divergence between final authoring and embedded prose. Essential/Core/Deep were reread in order, not judged by lexical/source-count triage alone.

Final cumulative `targetModes` are **16 / 26 / 30** (level counts 16 + 10 + 4), derived after writing. Essential explains the aim, four components, request/demand and refusal boundaries, listening, self-forgiveness, anger steps, protection and gratitude. Core inserts the blame, principal, Phil, suit, John and appreciation cases, plus needs/strategies, reflection and a pause when unable to listen. Deep adds the different reactions to lateness, presence before advice, the author’s actual choice exercise and the father’s reminder card. There is no invented dialogue, new anecdote, imposed moral-coaching exercise or forced management synthesis.

The case sequence includes details checked against real primary text: the principal’s twenty-minute meeting overruns and teachers’ relapse into a label; Phil’s correction of Rosenberg’s guesses and request for the speaker’s own difficulties; twenty minutes of reproach after the uncapped pen stains a new light-gray suit; John’s three-week wait and fear of prison return without training; the four-year-old Scottie and the reminder card; and the participant finding hope and direction for relating to her eighteen-year-old son. The last case does not claim a repaired relationship. John’s case does not claim an eventual training grant or reduced reoffending. Felix is explicitly the author’s illustrative example, not a newly invented or independently verified family case.

## Concrete findings corrected during own draft review

These are findings in the new draft, not fabricated defects of a non-existent previous delivery.

| Stable ID | Initial wording / defect | Final correction and direct supporting location |
| --- | --- | --- |
| `felix-socks` | EN initially said “two balled-up pairs”, while the source describes two balls of socks, not an established pair count. Translation-specific unsupported specificity. | Changed to socks in two balls under the table and three beside the television; [official chapter 1, The NVC Process](https://www.nonviolentcommunication.com/pdf_files/nvc2-chapter-one.html). RU was not changed into a pair count. |
| `have-to-choose-to` | “найдя другие способы заработка” / “finding other ways to earn” could imply an already established new income. Unsupported outcome. | The author recognizes that he could earn differently, and reports stopping clinical reports. The text now preserves possibility rather than inventing a subsequent income history; [chapter 9, printed p. 137](https://www.nonviolentcommunication.com/email/20201201/Chapter9.pdf). |
| `phil-wants-honesty` | RU initially broadened Phil’s comparison to everyone he had heard. | Limited it to speakers the group had had/invited; [chapter 3, printed pp. 32–33](https://nonviolentcommunication.com/wp-content/uploads/2024/12/nvc3-chapter3.pdf). |
| `empathic-guessing` | Essential referred to Phil although his full case is only inserted in Core. Broken shallow-mode continuity. | Replaced the name dependency with the directly supported procedure of checking guesses and accepting corrections; the actual Phil exchange remains in Core, same primary location. |
| `principal-meeting` | A short draft stopped at the renewed label and could obscure the eventual clarification. | Added that they eventually do identify the specific actions; [chapter 3, printed p. 29](https://nonviolentcommunication.com/wp-content/uploads/2024/12/nvc3-chapter3.pdf). |
| `appreciation-for-a-direction` | An explicit research-style sentence about the book not proving an eventual relationship outcome interrupted the reading. | Kept only the participant’s concrete contribution/hope/direction. The outcome limit is recorded in the source ledger rather than becoming a research lecture; [chapter 14, printed pp. 211–212](https://www.nonviolentcommunication.com/email/20201126/Chapter14NVC3.pdf). |

## Deliverables and presentation

The four canonical files are `collector-output/nonviolent-communication/story-data.json`, `nonviolent-communication.html`, `sources.md`, and `QA.md`. Additional owned files are `build-local.mjs`, `browser-qa.mjs`, and this book’s `qa/` proof. Sources remain in the Sources dialog; per-screen provenance labels are hidden without changing `contentMode: explanatory` or dropping source maps.

`build-local.mjs` invokes the maintained builder and adds a small book-local CSS block. It removes the generic seven-node analytical cover placeholder and keeps a text-first cover with the actual book explanation. It retains embedded Geist/Geist Mono, Flexoki dark/light, the maintained compact icon-only header, depth/language/theme controls, focus mode, progress and iOS guidance. No shared shell or tool was changed. No artwork or copyrighted cover was copied.

Defaults are **RU / dark / Essential**. Word totals including titles: **753 / 1,281 / 1,489 RU**, **869 / 1,467 / 1,704 EN**. Computed minutes: **5 / 8 / 9 RU**, **4 / 7 / 8 EN**. Body median: 44 RU and 52 EN words; no quota padding. There is no pre-existing nonfiction spoiler consent to migrate or fictional ending to conceal.

## Final validation evidence

- Maintained deterministic HTML audit: **69 checks, zero failures/warnings**. Effective data has one corpus, valid IDs/source references and exact nested counts. Canonical and embedded sources/method/copy agree.
- Actual standalone `file://` Chrome, network explicitly offline: **320×568, 390×844, 1024×768, 1440×900 × RU/EN × dark/light**, all three modes. **1,152 screen visits**, zero title/body/count mismatches, zero horizontal overflow, working vertical scrolling, loaded offline fonts, synchronized desktop rail, single-row icon header and no per-screen provenance chrome.
- 390px and 1440px interaction checks: 22 each covering navigation keys, gestures, language/theme state, both dialogs, hidden-target depth, focus, Continue/Start over, final restart and safe-area placement.
- iPhone-UA emulation at 320px: automatic and manual/localized install guide, six-icon row, 47px top inset and standalone guide suppression. **Not a real iPhone/Safari/PWA production-device test.**
- Final seven browser JSON reports contain tested authoring and HTML SHA-256 values matching this final package. Runtime reader errors: **0**; external HTTP requests: **0**.
- Visually inspected 320px RU dark cover/dense principal case, 1440px EN light cover and 320px iOS safe-area header. Screenshots and machine reports remain in the owned collector `qa/` folder.
- Each Chrome invocation was bounded by `timeout 30`, with a unique `mktemp -d` profile and owned detached process group terminated in `finally`. No server. Process/profile inspection found none of this worker’s Chrome processes or profiles remaining.

See the canonical `QA.md` for commands and proof filenames. These results establish local structure/behavior and the writer’s source-backed implementation, not independent editorial approval.

## Honest remaining limits and next owner

The exact source-by-source reading boundary and all 30 stable IDs are mapped in `sources.md`. Full complete chapters 4–8, third-edition mediation, counseling and the main protective-force chapter were not read continuously. Their unverified case narratives and full institutional procedures are not reconstructed. Core retained concepts have actual author support in consulted book chapters, his handout and clearly identified supplementary works. Protection is limited to the author’s directly available protective/punitive distinction, corroborated by the official Center text. No complete-book reading, unified-printing collation, official-Russian-translation equivalence or therapeutic efficacy is certified.

The particular omitted causal links are the complete mediation step/case chain and counseling transitions, the protective-force school case, and chapter-specific narratives in the unread main-book chapters. They remain outside the promised central-method scope. An independent checker should judge the selected arc using the supplied primary locations; absence of a full EPUB alone is not used as a rejection rule.

Publisher action remains: independently read every changed pair and supporting primary passages; assess the disclosed scope; integrate the book into the root reader/catalogue and validate production/mobile/progress behavior before release. This worker performed no Git/PR/deploy, external messaging, subagents, root reader/catalogue/index/shared-shell/shared-log edit, or waiting on other workers. Assigned record completed: **nonviolent-communication only**.
