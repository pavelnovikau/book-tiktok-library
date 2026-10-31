# Mindfulness — editorial repair, group 10

Verdict: **REBUILD**, with the primary-text scope below. Collector ready for independent check; no publication or whole-book fidelity certificate.

## Actual review

Read **all 112 old RU/EN pairs**, including titles, sections, subtitles, body text, cover and final, and inspected the source ledger and method note. Compared authoring JSON, collector HTML embedded corpus and root published HTML embedded corpus: screen copy identical in all three. Reader scripts use these screens for mode filtering/rendering; no later prose replacement found. Computed mode metadata may differ; no content difference. The same bilingual pair is counted once, not three times. Root reader was read only.

Primary edition: Williams/Penman, «Осознанность: как обрести гармонию в нашем безумном мире», MIF 2014, ISBN 9785000572139, translation Ю. Цыбышева, scientific editor Н. Никольская. The complete owned expanded EPUB was identified by metadata, 12 chapters and full spine; not a Smart Reading summary. Read-only access. This repair read the continuous central explanation in chapter 2 from «Наше беспокойное сознание» through the chapter end, the seven doing/being contrasts in chapter 3, the full weekly-progression section in chapter 4, principal complete instructions for body/breath (ch5), body scan (ch6), three-minute breathing space (ch7), sounds/thoughts (ch8), difficulty (ch9), befriending (ch10), day-activity balance and post-pause action (ch11), and continuation/motivation (ch12). Read additional whole passages for Alex, Lucy, raisin stages, habitual seat, expectations, movement limits and the cinema/whispering-commentary image. This gives the meaningful central argument and all eight program stages, not continuous cover-to-cover reading of every case, empirical claim, poem or note. EN is a new translation of this account, not collation with a complete EN edition.

Official author recordings page was inspected as a cross-check of this first book's practices; the later *Deeper Mindfulness* material is excluded. Current NCCIH safety page was consulted only for the separately identified safety qualification, not as the book's argument. Publisher web copy was inspected for identification, not accepted as efficacy proof. The anomalous 2001 copyright field in the RU package is not used to redetermine the English work's date.

## Findings by existing stable screen ID

| ID | Delivered wording / defect | Required correction / primary location |
| --- | --- | --- |
| `cover` | “Рамка и доказательства” / “карта книги” advertises an analytical companion. | Introduce the lived problem and the actual progressive program; ch2–4 and ch12. |
| `book-versus-therapy`, `service-context`, `nice-boundary`, `prevent-trial`, `tame-workload` | Opening detour of service structure, NICE and trial statistics delays the book for multiple screens. | One proportionate qualification; begin the book's emotion/doing-mode explanation, ch2–3. Clinical detail belongs in Sources rather than this short reading sequence. |
| `keep-planning` | “Первичный анализ 2026 года…” substitutes a later neuroscience paper. | Remove from book sequence. The book's doing/being distinction is ch2–3, not this later analysis. |
| `emotion-components` | EN adds the specific phrase “complete exhaustion”; RU only says “общей оценки”. | Rewrite both from the four-component explanation, ch2 «Наше беспокойное сознание», rather than infer a new translation claim. |
| `lucy-case` | “Он не доказывает, что карьерный успех вызывает депрессию…” interrupts a real case with an unsolicited methodological lesson. | Restore Lucy's study/work strategy, successes and fear-of-failure loop in short connected prose; ch2. |
| `week-one-autopilot` | Good real scene is isolated from its explanation by separate commentary screens. | Keep Alex's party/pajama error as the first week's entry; ch5 opening. |
| `right-to-stop` / `manageable-example` | Repeats source/dose/trauma boundary across several screens while giving little of the actual process. | Retain manageable difficulty and bodily response, prepared by earlier practices; ch9 «Практика пятой недели» and complete difficulty instructions. Put current safety qualification in one separate screen. |
| `no-cancer-inference` | A necessary narrow distinction becomes another independent screen, fragmenting Elana's story. | Do not infer a cancer cure; omit this case from a shortened sequence rather than retell a medical outcome. Ch9 case is not efficacy evidence. |
| `structural-limits`, `review-actual-day`, `thought-check`, `difficult-person-limit` | Compiler elaborations about poverty, review questions, deadlines and dangerous relationships become part of the reading. | Remove substituted lessons. Keep the book's actual limits on changing work, activity list and three action choices; ch11. |
| `reception-boundary` | A review's assessment interrupts the final week. | Remove reception from reading screens; continuation follows directly from ch12. |
| `portable-model` / `final` | “Рабочая модель пересказа” and a four-verb mnemonic replace the author's closing return to daily practice. | End on feasible personally meaningful practice and the imperfect small return, ch12 «Время выбора». |

The parallel old RU/EN argument had the same editorial defects; no separate material translation error was established merely from wording differences. Supplementary research may be accurate yet still displace the requested condensed book.

## What changed

Rewrote all 30 new pairs in connected prose; retained stable IDs when the subject survives. Changed cumulative counts **30/72/112 → 14/26/30** after writing, without padding. Each depth was reread in order: Essential retains the central argument and complete progression, Core adds procedures/examples, Deep adds subordinate explanations. `contentMode: explanatory`, fresh RU/dark/Essential. No “Synthesis” screens, invented quotes, scenes, motives, modern anecdotes or page numbers. Source anchors identify chapters/subsections, not fabricated print pages.

The rewritten sequence includes a real book scene (Alex), Lucy's established history and the book's own cinema image. It preserves raisin attention, natural breath, body scan, movement, hourglass breathing space, sounds/thoughts, manageable difficulty, widening goodwill, exhaustion funnel, activity balance, three action options and flexible continuation. No modern productivity framework is added.

## Checks

Maintained `build_story.mjs` rebuilt this collector HTML only. JSON has unique screen IDs, exactly one cover/final, known source IDs, paired copy and exact nested counts. Generated embedded screens equal authoring. An owned Chrome process with unique temporary profile and timeout 30 rendered every revised screen offline at 320×568 and 1440×900 in RU/EN × dark/light (eight combinations): no horizontal overflow or runtime exception; all nested contents counts and source dialog checked. Home href remains `./` for eventual root integration. No server; owned process tree and profile removed. Private browser JSON/screenshots and source extracts are outside the repository. The 320px screenshot was visually inspected. These are structural checks, not an independent editorial judgment.

## Limits / publisher action

Scope is a condensed account of the central explanation and eight-week program, not verification of every book anecdote, biomedical promise or note. Broad brain, immune and longevity promises are neither silently proved nor replaced by a new science lecture: they are outside this shortened account. The absolute harmlessness claim is explicitly qualified by NCCIH once. Full scripts and exact daily schedules are not replaced by this short reader; the source dialog links official recordings. Publisher must assess whether this deliberately shorter 30-screen scope is appropriate; it must not label it an exhaustive full-book fidelity audit.

Publisher must independently read the revised pairs and evidence, integrate through the maintained root reader, recalculate catalogue counts/times/description, and preserve the maintained icon header, focus mode, and progress fallback for removed IDs. Do not overwrite the live shell with an arbitrary collector copy. No book-specific spoiler gate is required for this nonfiction. No root reader/catalogue/shared-shell edit, Git/PR/deploy or external messaging was performed.

Additional final local checks: maintained `audit_story_html.mjs --require-bilingual` passed all 69 structural checks with no warnings or failures. Actual browser pointer taps entered/restored focus mode, retained text and Next, and hid/restored the header. Vertical pointer movement and horizontal swipes did not toggle focus. This is desktop Chrome interaction evidence, not an iPhone/PWA production-device test.
