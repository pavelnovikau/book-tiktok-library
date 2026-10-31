# The Hobbit — total editorial audit, 2026-10-31

**Editorial verdict: REBUILD. Delivery state: SOURCE-GAP; not ready for independent publication check.**

The current reader delivers an ethics workbook around Tolkien's plot. It does not deliver the requested short, connected adventure. All 144 RU/EN pairs were read in full (288 localized screens), including cover and final, and the Essential/Core/Deep subsequences were examined. No complete edition was available to support a faithful new narrative. No replacement story has been fabricated. The audit is complete; the literary repair is blocked.

## What the reader actually receives

Essential has 36 screens. It jumps from a framing question to loss, trust, rest, fear, compassion, leadership, tools, public consequences and moral judgment. The dinner, departure, troll encounter, cave capture, ring discovery, rescues and barrel escape are all level 3. The named events that would give the lessons meaning are withheld even from Core. Core (90 screens) adds more interpretation and reading instructions; Deep (144) finally supplies events, repeatedly interrupting them with a lesson. Renaming these screens or removing their footers cannot repair this sequence.

The book's comic movement is repeatedly explained rather than experienced. Each episode becomes an abstract claim before it has been told. The ending then dissolves into publication history, textual variants, research qualifications and bedtime advice. A concise narrative needs a new causal sequence, not a quota-preserving line edit.

## Actual delivery comparison

The 144 screen objects in `story-data.json`, the collector HTML's `book-tiktok-data`, and the root reader's effective embedded corpus were identical at intake, including both languages, levels, IDs, source arrays and titles. The two HTML files differ as files because of shell integration; there is **no unpublished better story** hidden in the collector. Embedded `modes` adds generated labels/minutes to the JSON. Runtime code reads the embedded array directly and filters by level; no alternative literary corpus was found. Root/catalogue/shared shell were read only. At handoff, JSON and collector still match exactly; the sole root-versus-collector literary difference is the RU grammar correction in `o-settlement` described below. All remaining screen objects match the root baseline.

Historical levels are 36/90/144. There are 76 screens labeled synthesis, 59 book, nine context. These labels are descriptive inventory, not a fidelity test. Counts have not been changed because no source-backed replacement has been authored.

## Work and evidence actually inspected

Target work: J. R. R. Tolkien, *The Hobbit, or There and Back Again*, first published 1937. The package intends the modern post-1951 chapter-5 story. It does **not** identify a complete English printing that was actually read, nor a Russian translation collated with it. The Russian digest is its own wording; publication-title spelling is not translation verification.

Fresh source search: Apple Books EPUB title/creator metadata (216 immediate EPUB entries; 217 recursively, including an additional nested entry), then author-matched metadata/navigation search; no assigned title or matching Tolkien edition. Targeted Spotlight filename discovery found the existing digests/audit extracts, not a source novel. The search was limited to these assigned works; unrelated private titles were not exported. This is a scoped search, not proof that no copy exists anywhere.

Fresh lawful external consultation:

- [Penguin Random House teacher's guide](https://www.penguinrandomhouse.com/books/179206/the-hobbit-by-jrr-tolkien/teachers-guide): continuously read the chapter 1–19 **plot summaries**, with adjacent relevant commentary/questions. This establishes a broad plot outline; it is not Tolkien's prose. The guide itself has a raven-name inconsistency in chapter 15, so it cannot certify all details.
- [PRH work/edition page](https://www.penguinrandomhouse.com/books/179206/the-hobbit-by-jrr-tolkien/): modern paperback ISBN 9780345339683, description and edition metadata; not full-text access.
- Official/publisher/estate sample searches and licensed library discovery did not yield a readable complete modern novel. [Libby title record](https://share.libbyapp.com/title/1044887) appeared in discovery; a title record is not an active loan or a read edition. Search hits for unattributed uploaded complete PDFs were not opened as a substitute.

The inherited Tolkien Estate, bibliography and archival references may support their own context claims. They do not supply the missing continuous novel. This pass does not re-certify every inherited historical assertion. No private/full copyrighted source was added to the repository.

## Concrete findings

Locations below identify supporting material or the actual package, not invented novel page numbers. A verdict of unwanted interpretation is an experience failure under BRIEF.md, not an accusation that an interpretation is impossible.

| Screen ID(s) | Concrete wording / defect | Required correction and evidence scope |
|---|---|---|
| `cover` | “самостоятельный разбор приключения и выбора” / “exploration of adventure and choice” accurately advertises the old product, not the requested reading experience. Tap instructions also occupy the opening. | Replace with a short story invitation after the narrative exists; keep depth/spoiler instructions compact. The [publisher work page](https://www.penguinrandomhouse.com/books/179206/the-hobbit-by-jrr-tolkien/) supports the premise, not an interpretive curriculum. |
| `a-party`, `a-contract`, `a-departure` versus `a-desire` | The concrete opening is Deep-only; Essential instead says “Следите, какие обычные качества…” / “Watch which ordinary qualities…”. | Tell the intrusion and departure in the spoiler-light route. Guide chapters 1–2 establish their place in the opening. A full chapter 1 is needed for faithful comic texture and relations. |
| `a-two-inheritances` | “не медицинский диагноз и не закон наследственности” / “not a diagnosis or a law of heredity” interrupts the family joke. | Keep the conflict of respectability and curiosity through Bilbo's situation; remove the unsolicited diagnostic disclaimer. Guide chapter 1 discussion is context, not narrative prose. |
| `b-ensemble`, `b-thorin` | “Не обязательно… запоминать” / “Keep that gap between status and judgement open” turns company introduction into instructions to a student. | Introduce companions through the actual encounter, preserving Thorin's dignity and comedy without an imperative addressed to the reader. Full chapter 1 required. |
| `b-gandalf` | “не значит иметь право… распоряжаться его страхом” / “does not automatically justify deciding what dangers they should face” imports a mentor-consent debate. | Tell what Gandalf says/does and Bilbo's established reactions. Do not supply a new moral controversy as Tolkien's action. Guide chapter 1 supports recruitment only. |
| `b-trolls`, `b-blades` | A short incident is immediately generalized as “Присвоенное название не заменяет умения” / “A title cannot replace competence” and possession versus knowing its use. | Keep the mishap, danger, rescue and discovery moving together. Guide chapter 2 supports the outline; full scene needed for voices, timing and causality. |
| `b-belonging`, `c-help` | “Для серьёзного взросления важнее…” / “Accepting help is also a skill” replaces road events with prescriptions. | Remove as independent lesson screens; weave only demonstrated changes in relationships into narrative. No primary text was read that supplies these prescriptions. |
| `c-rest`, `c-map`, `c-moon-letters` | Elrond's concrete contribution is postponed to Deep while Core says owning a map is not understanding it. | Give the visit and clue in their causal place without turning them into a knowledge-management metaphor. Guide chapter 3 supports the visit; exact clue/conditions require the modern novel. |
| `d-fear`, `d-learning`, `d-shelter` | “Страх сообщает о риске, а не о твоей ценности” / “A mistake becomes experience through attention” adds psychological teaching. | Rebuild the storm/cave/capture/escape as events. Guide chapter 4 supports the broad chain, not a theory of personal worth. |
| `d-goblin-song`, `d-machinery` | “Слушайте функцию…” / “whom ingenuity serves” discusses songs and technology instead of telling the peril. | Preserve threatening rhythm and concrete menace through original narrative prose, without quoting songs or adding an essay. Full chapter 4 needed. |
| `e-rule`, `e-fairness`, `e-ring`, `e-pocket` | Core explains fairness before it tells what was wagered; the actual ring and pocket question are Deep-only. | Tell the encounter in connected order at the chosen spoiler boundary. Guide chapter 5 is a summary, not verification of exact bargaining or all motives. |
| `e-mercy` | Title calls Gollum “беспомощного” / “vulnerable enemy”; the body still describes an active threat. | Prefer a concrete title naming Bilbo's choice rather than declaring Gollum helpless. Verify the precise threatened escape, pity and action in modern chapter 5 before writing it. This is misleading framing, not a proven event error from a complete edition. |
| `f-network`, `f-bounds`, `f-mentor-leaves` | “никто не становится бесконечным ресурсом” / “no advice to abandon people deliberately” changes the journey into boundaries coaching. | Remove those lessons; keep each helper's actual acts and conditions. Guide chapters 6–7 establish sequence, not these instructions. |
| `g-stream`, `g-spiders`, `g-missing-thorin` | Useful event kernels are closed by a general lesson about care or competence. Essential gets `g-leadership`: “Лидерство начинается с чужой нужды.” | Retain only verified events in a new continuous forest episode. Do not elevate the compiler's leadership thesis over the rescue. Guide chapter 8 supports broad events; direct chapter needed for chronology and tone. |
| `h-observation`, `h-plan-limit`, `h-cells`, `h-barrels`, `h-outside-barrel` | The plan is analyzed before the reader sees the prison or the means of escape. | Connect confinement, discovery, keys, barrels and Bilbo's own predicament. Preserve comic inconvenience without a separate planning lecture. Guide chapter 9 supports the outline. |
| `i-consequence` | “Практика для читателя: назовите три группы…” / “A reader exercise: name three groups…” is an invented assignment. | Delete from narrative. Let the town and its inhabitants enter through what happens. No author-text source is claimed for this exercise. |
| `j-before-danger`, `j-courage`, `k-distrust` | General courage/manipulation lessons repeatedly interrupt the approach and conversation. | Preserve Bilbo's established fear, acts and the actual exchange's effects. Full chapters 11–12 are required for faithful texture; the guide cannot validate every attributed intention. |
| `l-rights`, `l-enough`, `m-loyalty`, `m-judgement` | “кому мы верны” / “state reasons and answer for an action” turns a treasure crisis into a seminar in ethics. | Tell the competing demands and Bilbo's actual decision after Deep consent; let the situation carry the tension. Guide chapters 15–17 establish an outline only. |
| `n-five-armies`, `n-unconscious`, `o-thorin-death`, `o-fili-kili` | Decisive outcomes currently sit at level 3; they must not be casually moved into a new Essential/Core route. | Preserve the Deep-only outcome boundary. Their inherited details still require primary-text verification; no assertion of full ending fidelity is made here. |
| `o-settlement` | RU “Такой послевкусие” is ungrammatical; EN has “That aftermath.” | RU corrected locally to “Такое послевкусие”; preferably replace the entire lesson with verified aftermath narrative during rebuild. This is a concrete RU copy defect, not a dispute about Tolkien. |
| `p-returned` | “Проведите тест возвращения” / “Run the return test” asks readers to process their own life. | Delete the invented exercise. The homecoming should carry the ending; no primary source supplies this activity. |
| `q-1937` through `q-revision-model`, `r-theory`, `r-boundary` | After the narrative return, the reader gets an extended bibliographical/research course. | Put concise edition/source information in Sources, outside the story's momentum. Context is not a replacement for the missing novel. |
| `r-bedtime`, `r-fantasy`, `final` | Reading instructions and “notice, attempt, accept help, care and judge” give the digest writer the last word. | Replace with a spoiler-safe close appropriate to the selected depth; no personal-growth prescription and no invented continuation of Tolkien's ending. |

RU/EN parity: the same unwanted analytical treatment appears in both languages throughout. No material event uniquely invented by one language was established from the available primary material. This is not a certification of literary translation accuracy; no complete Russian edition was consulted.

## Repair decision and precise unresolved need

A lawful complete English modern edition, explicitly post-1951 (all 19 chapters), readable continuously and with its edition/copyright leaf, is needed. An owned EPUB/FB2/PDF or licensed active library access would suffice. A complete Russian translation is needed only to claim fidelity to a named translation; otherwise RU must remain original paraphrase checked against the English source. An uploaded summary, a guide's discussion questions, manuscript finding aid or films do not close this gap.

Once access exists: read continuously; write the concise adventure as connected prose; split into justified short screens; build coherent nested routes that stop short of the decisive resolution in Essential/Core. Then set `contentMode: narrative`, remove the per-screen academic footer through the maintained shell, and regenerate using maintained tools. No count is proposed before that work. All fictional scenes/motives must come from the edition, not the replacement writer.

## Publisher attention

- This package is **blocked**, despite the older green QA. No ready manifest has been issued. Story JSON and HTML have deliberately not been reclassified as a completed narrative. The one RU grammar correction (`Такой послевкусие` → `Такое послевкусие`, ID `o-settlement`) is collector-local and can be ported separately by the publisher.
- The current Hobbit HTML has bespoke explicit Core/Deep consent, session-level approval, neutral saved-progress text when the remembered title exceeds approved depth, safe contents filtering and book-specific cover wording. A plain rebuild from the generic template would lose these behaviors. Preserve them when integrating the future narrative; do not carry the old hardcoded `36 / 90 / 144` string into changed counts.
- `sourceLabel()` currently prints `Синтез`/`Synthesis` or book/context labels under screens, including the cover. A maintained narrative-mode renderer must suppress this academic footer and leave Sources available separately. A data flag alone cannot rewrite the current story.
- No root reader, catalogue, shell, installed skill, Git, PR, deploy, external messaging or other collector was changed. Root LOG updates belong to the coordinating publisher under this ownership restriction.

## Checks and review record

Completed: full bilingual manual reading; exact JSON-to-embedded-corpus comparison of collector and published root; level/subsequence review; spoiler-boundary inspection; source-access research. No new HTML was built and no ready/browser pass is claimed for literary content. The grammar-only patch preserves the existing bespoke reader code byte-for-byte. The old browser matrix remains historical technical evidence only. In this repair the source/QA status notices change and the single RU grammar error in `o-settlement` is corrected in authoring JSON and the collector embedded corpus. No narrative rebuild is claimed; the root retains the old wording pending publisher action. Private research/extraction stays outside the repository. The original four files remain recoverable from the supplied external baseline.


Maintained structural audit on the final collector HTML: `audit_story_html.mjs --min-screens 3 --require-bilingual` reports **69 passes, zero warnings, zero failures**. This checks structure/offline/bilingual metadata only and does not approve the literary corpus. JSON-to-collector equality and exact intended baseline differences were rechecked after the local fixes.

## Full read inventory

Every ID below was actually read in RU and EN; this inventory is coverage, not a claim that every sentence is verified against an unavailable novel.

- 1–8: `cover`, `a-voice-nearby`, `a-two-inheritances`, `a-good-morning`, `a-party`, `a-contract`, `a-departure`, `a-desire`.
- 9–16: `b-grievance`, `b-thorin`, `b-ensemble`, `b-gandalf`, `b-trolls`, `b-blades`, `b-troll-humour`, `b-belonging`.
- 17–24: `c-rest`, `c-elves`, `c-map`, `c-names`, `c-moon-letters`, `c-sword-memory`, `c-depth-limit`, `c-help`.
- 25–32: `d-fear`, `d-shelter`, `d-goblin-song`, `d-machinery`, `d-capture`, `d-rescue`, `d-separated`, `d-learning`.
- 33–40: `e-language`, `e-rule`, `e-gollum`, `e-fairness`, `e-ring`, `e-pocket`, `e-mercy`, `e-compassion`.
- 41–48: `f-network`, `f-animals`, `f-beorn`, `f-mentor-leaves`, `f-reunion`, `f-trees`, `f-beorn-arrival`, `f-bounds`.
- 49–56: `g-attention`, `g-path`, `g-perspective`, `g-spider-humour`, `g-stream`, `g-spiders`, `g-missing-thorin`, `g-leadership`.
- 57–64: `h-tools`, `h-elvenking`, `h-observation`, `h-plan-limit`, `h-cells`, `h-barrels`, `h-outside-barrel`, `h-responsibility`.
- 65–72: `i-public`, `i-legend`, `i-master`, `i-trade`, `i-arrival`, `i-bilbo-doubt`, `i-last-support`, `i-consequence`.
- 73–80: `j-before-danger`, `j-wait`, `j-small-sign`, `j-balin`, `j-door`, `j-tunnel`, `j-cup`, `j-courage`.
- 81–88: `k-smaug`, `k-flattery`, `k-self-naming`, `k-distrust`, `k-bare-patch`, `k-barrel-clue`, `k-retreat`, `k-possession`.
- 89–96: `l-rights`, `l-value`, `l-dragon-sickness`, `l-good-sides`, `l-arkenstone`, `l-smaug-death`, `l-relief`, `l-enough`.
- 97–104: `m-loyalty`, `m-pride`, `m-mediator`, `m-means`, `m-siege`, `m-jewel-gift`, `m-confrontation`, `m-judgement`.
- 105–112: `n-battle`, `n-common-enemy`, `n-viewpoint`, `n-heroism`, `n-five-armies`, `n-thorin-sortie`, `n-unconscious`, `n-scale`.
- 113–120: `o-loss`, `o-apology`, `o-wealth-use`, `o-settlement`, `o-thorin-death`, `o-fili-kili`, `o-dain-bard`, `o-value`.
- 121–128: `p-home`, `p-respectable`, `p-song-return`, `p-write`, `p-long-return`, `p-auction`, `p-epilogue`, `p-returned`.
- 129–136: `q-1937`, `q-origin`, `q-child-reader`, `q-revised`, `q-original-gollum`, `q-1960`, `q-archive`, `q-revision-model`.
- 137–144: `r-fantasy`, `r-theory`, `r-bedtime`, `r-boundary`, `r-providence`, `r-eucatastrophe`, `r-next-book`, `final`.

## Audited content fingerprints

- `collector-output/the-hobbit/story-data.json`: SHA-256 `c923a7d7e71e75f37dacea0a9f197aba15c8234121a884d154c147466aed38e1`.
- `collector-output/the-hobbit/the-hobbit.html`: SHA-256 `29803a33e5fe5be54b6030e30913b109250ddf69b4e0f446aa832d232330ed66`.
- `the-hobbit.html`: SHA-256 `cb33ea1dda4a5b8caadb7373c3b2051fbda1ae0ee88e01ae8fae12851857fb9e`.

---

## 2026-10-31 targeted rescue addendum — latest BRIEF clarification applied

**Implementation verdict: REBUILD completed; ready-for-independent-check.** The earlier blanket stop based on absence of a complete EPUB is superseded for the **retained concise arc** only. The earlier audit and its findings remain historical evidence; no independent PASS/publication claim is made.

New acquisition: the actual publisher `Read Sample` from ISBN 9780345339683 was found inside the Ballantine page, obtained and read from the chapter-1 opening through Gandalf's recognition. Foster's actual chapter-summary text 1–19 and relevant scene commentary were re-read, then assessed claim by claim. The unavailable Glasgow extract was explicitly rejected after its permission-expiry notice. Full novel/translation reading is not claimed. [Acquisition/evidence map](../source-rescue/the-hobbit.md) supplies exact supported links and exclusions.

The worker read the 144 bilingual intake pairs (288 localized screens) and compared the root's effective embedded screens with canonical authoring: no literary divergence at this pass. All 35 replacement bilingual pairs (70 localized screens) were authored/read and examined in each nested sequence. Old abstract instruction screens including `a-desire`, `d-learning`, `g-leadership`, `i-consequence`, `p-returned` and the research/history tail were removed. Existing defects listed above motivated a new narrative rather than a mechanical retagging.

The replacement follows recruitment → road → goblins/Gollum → forest/prison → Lake-town/Mountain/dragon. Deep continues the treasure crisis, devastation, siege, negotiation, battle, farewell and return. Retained actions and causes are mapped to actual evidence. Unsupported specifics (including exact burial objects, secondary losses and first motives for taking the jewel) were not reconstructed. Essential has a coherent brief opening adventure with the decisive ending withheld; Core fills escape details and reaches the trapped company. The shared final merely explains the stopping boundary and leaks no result.

Counts changed from **36 / 90 / 144** to **15 / 23 / 35**, recorded exactly in `targetModes`; no quota padding. Current builder word totals: Essential RU/EN 742/878, Core 1,119/1,327, Deep 1,726/2,057. Narrative presentation with Sources dialog replaces per-screen research framing.

Build: maintained builder + preserved book-local gate/cover/resume code + maintained reader-shell command scoped to this collector HTML. Offline/mobile browser check made 1,168 complete rendered-screen visits at four prescribed sizes in RU/EN/light/dark/all modes; runtime exceptions 0, remote runtime requests 0, overflow/reachability failures 0. Fresh/cancelled consent and saved-Deep generic-label/reopen safety checked. Screenshot inspection covered 320/1440 EN-light narrative views. Physical iOS and exact translation fidelity remain untested. QA uses timeout30 and owned-profile/process-group cleanup.

Only the four assigned collector files plus this book's acquisition/report/ready record are changed. Root reader/catalogue/publication are left to the publisher. The ready manifest contains canonical absolute deliverable paths and current SHA-256 hashes; it requests independent content checking rather than certifying it.

Final source and sequence check: excluded exact pocket-question/leap mechanics, precise troll voice imitation, Beorn’s animal form and the unstated auction cause. Promoted the actual troll rescue to Essential so captivity resolves before the Rivendell scene; Core/Deep remain 23/35. The retained events, not a target quota, justify the final Essential count of 15. Fresh final build and browser results supersede interim rescue-package fingerprints; the ready manifest carries the definitive hashes.
