# The Giver / Дающий — implementation handoff, 2026-10-31

Slug: `the-giver`. Verdict: **REBUILD / new approved-title build**. Status: **ready-for-independent-check**, not independent content acceptance or publication approval.

## What was actually read and written

The approved title in `BOOK_PLAN.md` was retained: Lois Lowry’s **The Giver**, the **1993 first novel**. No substitute was chosen. The dispatch slot’s earlier reviewer work is not counted as reading this book.

There was no existing `collector-output/the-giver/` package and no root Giver reader in the initial scoped inventory. Therefore old collector pairs read: **0**; old published pairs read: **0**; old divergence findings: **not applicable**. This is a new package, not a claimed audit of some absent earlier retelling.

Written: **27 new unique RU/EN pairs** (25 narrative scenes + cover + shared final). Actually read in authoring and effective HTML: **all 27 pairs / 54 language texts**. Every final embedded body/title was compared with the JSON, and the complete Deep sequence was read in order. Essential and Core were separately read as continuous RU/EN sequences to check missing antecedents and causal continuity. Three nested sequences contain **55 pair appearances (11 + 17 + 27)**; that is not 55 unique pairs. The final small revisions to apple/Gabriel/sled were read in both languages and rebuilt before final QA.

The connected manuscript was written first in **11 paragraphs per language** (`collector-output/the-giver/narrative-draft.md`), then segmented at scene beats. The final exact `targetModes` are **11 Essential / 17 Core / 27 Deep**, including the two framing screens. Level distribution is **11 / 6 / 10**. Original trial split was 10/17/27; moving the Christmas-family scene into Essential fixed the question-about-love antecedent and justified 11/17/27. No historical quota was retained, and no count-padding filler was added.

The short sequence follows Jonas’s worry and appointment, his relationship with the Giver, memory experiences, his changed relationships, the recording and the ensuing danger and journey. Specific actions, uncertainty and conflicting loyalties carry the account. It contains no advice to the reader, exercises, management takeaways or invented dialogue. “Release,” “Sameness” and “Elsewhere” are narrative terminology, not quotations invented for the package. RU/EN are original concise prose, not a published-translation claim.

## Exact edition and source scope

The original novel is *The Giver*, Houghton Mifflin, 1993, as identified in Scholastic’s bibliography. Authorised primary passages actually consulted in the 2014 Selman/Elizabeth guide refer to the hardcover **ISBN 9780547995663**: chapter 9 / pp. 70–71, chapter 13 / pp. 122–123, chapter 16 / pp. 159–160, chapter 20 / pp. 195–196. These are the guide’s printed edition references, not invented pagination. That full hardcover was not obtained or read continuously.

The requested PRH URL is a **Listening Library audiobook listing**, ISBN **9780553751376**, July 5, 2000, 4h 48m. Its interview was read; the audiobook was not listened to. It must not be described as the printed primary edition read for this task.

A title/creator-scoped Apple Books discovery considered both expanded EPUB directories and ZIP EPUB OPFs. The final exact metadata check inspected **218 candidates**, with **zero matching title/author editions**. There was no target OPF/spine/body extent to classify as full edition versus SmartReading condensation. An initial description-inclusive filter produced irrelevant matches; it was corrected to bounded title/creator matching, and none of those books was used. No unrelated private filenames are reproduced in this handoff.

The retained action is supported jointly by:

- Scholastic’s substantial 2003 BookFiles guide: read printed pp. 12–14, 18–46, plus selected p. 50 glossary and p. 63 bibliography material. Its questions, connected plot, character accounts and short embedded novel quotations support the retained chronology. It is not the full novel.
- Permission-labelled novel passages in the Selman/Elizabeth guide, plus selected expressly book-linked secondary notes. The guide mixes the novel with film material; screenplay excerpts and imagined classroom scenes were excluded.
- Lowry’s nine-page June 1994 Newbery speech, read across the document, especially its refusal to establish one uniquely correct ending.
- Current PRH listing/interview and its linked Gary D. Schmidt Reading Guide, questions 1–8.

Primary and secondary support are classified **per screen** in `collector-output/the-giver/source-evidence-map.json`, covering all 27 pairs. The guide supports the retained specific actions where a whole chapter was not read; the source map does not relabel those actions as primary-text reading. Five reader source records have spoiler-safe role/method notes. Full source/extract files were kept in private temporary research storage outside the public repository; only original paraphrase, metadata and locators are in this package.

No complete novel was read continuously. The retained chain has no identified essential missing action/link after the documented omissions, so the lack of a complete download is not treated as an automatic gate. This is **retained-scope support for independent review**, not certification of every scene, sentence, motive or relationship in the whole novel.

## Discovery routes and results

1. Actual author site `https://loislowry.com/`, `/books/`, `/speeches/`: web-tool timeouts on some routes; ordinary HTTP successfully retrieved Books/Speeches. Actual Speeches link yielded `https://loislowry.com/wp-content/uploads/2019/11/the_giver.pdf` (200, nine pages). Older `/pdf/Newbery_Award.pdf` and guessed `/books/the-giver/` did not supply usable text.
2. Requested `https://www.penguinrandomhouse.com/books/104094/the-giver-by-lois-lowry/`: 200, current metadata/description/interview read. Followed its actual Reading Guide link to `/readers-guide/`: 200, questions 1–8 and attribution read.
3. Official Scholastic `https://www.scholastic.com/content/dam/teachers/activities/migrated-files-in-body/the-giver-bookfile.pdf`: 200, 64-page guide, selected substantial sections read as above.
4. Harvard’s *Giving Guidance on “The Giver”* established the Selman/Elizabeth resource’s book/film context and linked Walden’s resources. Historical Walden `/wp-content/uploads/2014/03/Giver_EdGuide_V4b.pdf`: 404. Accessible `https://www.reellifewithjane.com/wp-content/uploads/2014/05/The-Giver-Educators-Resource-Guide.pdf`: 200, 28 pages, permission/edition credit checked. Used only labelled novel excerpts and book-specific notes; not passed off as a current Walden-hosted download.
5. PRH Canada `/books/104094/the-giver-by-lois-lowry/9780553751376/excerpt`: direct fetch was a client-rendered shell; search showed an indexed opening fragment. No complete chapter reading or substantive source ID is claimed from that. PRH US `/excerpt/`: 404.
6. Current HMH Connections teacher-guide sample: discovered via search, direct fetch timed out; not counted as reading. Guessed additional Scholastic literature-circle/literature-guide paths were 404; no content filled from them.
7. TeachingBooks hub timed out; discovery leads are not counted as accessed book text or as an interview read.
8. Government of Newfoundland and Labrador alternate-format listing `/Home.aspx/Book/209`: public metadata for Laurel Leaf ISBN 0440237688; logged-out listing had no public book links. No eligibility assertion, sign-in, loan, URL manipulation or bypass was attempted.
9. Title-scoped owned Apple Books check: zero target editions, as above. No purchases, subscriptions, credential requests, external messaging or unofficial full-book hunting. Unused search-result recaps/classroom copies supplied no book text.

Direct sources, sizes, PDF SHA-256 values and exact page/kind distinctions are available in `sources.md`, the scene evidence map and this handoff’s build evidence. Private research scratch used for the lawful guide downloads: `/var/folders/78/c4cjg2412cjc0sxqpcm986rc0000gn/T/the-giver-evidence-dww8tvd8/`. It is outside the public Git tree and contains only this task’s retrieved research material.

## Concrete self-corrections

These are authoring corrections, not claims about an earlier published Giver reader.

| Screen ID | Initial problem | Final correction and evidence |
| --- | --- | --- |
| `cover` | “what no one else remembers” / “чего больше никто не помнит” was too universal, since the Giver also remembers. | Community has given the memories up; Scholastic pp. 24–26 and PRH premise. |
| `the-apple` | “Asher notices nothing” added a reaction not established in the consulted guide passages. | Removed; kept the apple’s brief change and Jonas’s puzzlement, Scholastic pp. 24–25, 42. |
| `gabriel` | EN “small” was less precise than RU’s poor growth. | EN now says he is not growing well and sleeps badly, Scholastic pp. 23, 45. |
| `the-sled` | “Snow on his face,” cold-air sensation and a stated strange reaction exceeded the consulted account’s specificity. | Neutral sled-ride title and actual question about absent snow/hills, Scholastic p. 25. |
| `the-christmas-tree` → `love` | Essential skipped the memory that made Jonas ask about love. | Christmas family scene raised from level 2 to 1. Essential now has the emotional antecedent, Scholastic pp. 39–40 and authorised chapter-16 excerpt in guide p. 14. Counts become 11/17/27. |
| `what-he-sees` | “selects the smaller infant” used a plausible but unverified selection detail. | Removed; retained injection/death/father’s voice only, Scholastic p. 27. |
| `what-he-sees` | “does not give Jonas his old father back” was added interpretive rhetoric. | Replaced with the supported action: he stays with the Giver that night, Scholastic p. 27. Giver’s explanation of father remains attributed. |
| `the-plan` / `the-hill` | Risk of implying that the unseen community definitely changed after escape. | Memory return is an expectation in the plan; weakening memories are experienced by Jonas. No completed social outcome is reported, Scholastic pp. 26–29; primary chapter-20 excerpt, guide p. 19. |
| `the-lights` | Risk of adopting Lowry’s personal optimistic interview answer as a definite plot outcome. | Only sled/descent/lights/singing are narrated. No later rescue/death verdict; PRH guide Q5 and Lowry’s 1994 speech keep the ending open. |
| Cover/shell | Maintained template’s fallback artwork speaks in “system/model” terms inappropriate to this story. | Book-local patch removes the analytical cover graphic and keeps a quiet text cover; `contentMode:narrative` hides source chrome but is not offered as editorial repair by itself. |

No extra tale was fabricated to justify Deep. Omitted details include the earlier trainee’s name, family relationship and detailed fate; needle anatomy/disposal; detailed dream/medication scenes; specific battlefield injuries/dialogue; film romance/sensor/injection/barrier material; mapped distances and any sequel epilogue. This preserves the supported first-novel action without using memory to fill those gaps.

## Reader implementation and spoiler routes

Maintained `skills/book-tiktok/scripts/build_story.mjs` builds the clean structured data. `collector-output/the-giver/build-local.mjs` adds only this book’s consent gate, masked Deep titles, stable rendered ID, generic saved-Deep protection and text-cover treatment. It uses exact shell anchors and fails for inspection if the maintained shell changes. No shared shell or installed skill was synced. The separate Settings/Geist checkout was not read/copied or implemented; final accepted UI remains publisher work.

All entry routes were considered: cover Deep picker, dialog Deep picker, hidden Deep Contents item, desktop Deep rail item, and saved Deep Continue. All require local explicit consent before revealing a level-3 screen. Cancel and native Escape preserve state; reload and downgrade revoke consent. Pre-consent Deep titles are generic; the saved label is generic rather than a last-scene title. Keyboard paging is blocked while the modal is open; Next/swipe operate on the consent-controlled visible sequence. No hash/query deep-link route exists in this maintained shell.

Essential/Core end before the recording is shown. Deep alone includes Gabriel’s receiving capacity, returned trainee memories, the recorded revelation, plan, departure, pursuit and final descent. Cover/final/global notes contain no outcome. Optional external links warn that the source itself can contain spoilers. Source maps remain embedded, while the reading screens show the story without research labels.

## Validation and limits

Structural audit: **69 passes, no failures or warnings**. Exact authoring/effective-data equality, exact counts and strictly nested IDs checked. Builder words including titles/framing: **374/458** RU/EN Essential, **581/708** Core, **922/1129** Deep; estimates **3/4/6 minutes**. All 25 narrative bodies are compact, averaging about 32 RU / 39 EN words. Two short Deep beats separate the urgent news from the physical departure; they are linked actions, not padding to a prescribed total.

Browser matrix: **320×568, 390×844, 1024×768, 1440×900**, three modes × two languages × two themes, **48 cases / 880 renders**. Exact rendered prose, counts, IDs, scroll reachability, compact icon header, no horizontal overflow, desktop rail and offline font loading were checked. Zero unexplained runtime exceptions or external requests. This does not prove literary fidelity. Sources/Contents, language/theme persistence, rapid switches, focus, Next/Back/keys/swipes/restart and all spoiler routes passed.

Emulated iPhone Safari: native 47px safe-area inset, install guide/localisation/closing, six controls below the inset, focus hiding and standalone suppression passed. This is not a physical iPhone/PWA test. A native-Escape check initially failed because the CDP fixture omitted native key metadata; supplying key code 27 and waiting for native modal closing fixed the test, with no reader code change.

Every Chrome run had `timeout 30`, its own `mktemp -d` profile and debugging port, an internal 29-second cleanup deadline and owned-process-group cleanup. All reported profiles were removed; no server was started. Representative final-hash screenshots were visually read for phone cover/prose, desktop rail, warning, Sources, common final and iOS inset.

Remaining limits: independent content acceptance is pending; a full continuous novel reading has not occurred; guide-supported scenes must not be relabelled primary chapters; physical device and final production/catalogue/progress integration are untested. The publisher must apply/retest accepted shared Settings/Geist work. These limits are recorded rather than called a literary PASS.

## Files and ownership

Canonical collector files: `story-data.json`, `the-giver.html`, `sources.md`, `QA.md`. Additional owned files: connected manuscript, authoring/local-build/evidence-map scripts, `source-evidence-map.json`, browser harness, JSON check receipts and screenshots. The ready manifest records exact canonical paths and SHA-256 values.

Only `collector-output/the-giver/`, this uniquely named report and its explicitly requested ready manifest were written. No unrelated file was removed or changed. No root reader, `books.json`, `index.html`, shared shell/skill, installed skill, shared log, Git/PR/deploy or external communication operation was performed. Parent/publisher owns independent acceptance and publication.
