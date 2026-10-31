# Adventures of Huckleberry Finn — implementation and evidence report

2026-10-31 · assigned slug `adventures-of-huckleberry-finn` · status **ready-for-independent-check** after local validation. Independent content acceptance and publication have **not** been performed.

## Scope and verdict

**REBUILD / new approved package.** There was no assigned collector folder, root Huck Finn reader, or catalogue entry when work began. Existing delivery/draft pairs read: **0**, because none existed. New unique RU/EN pairs authored and read: **54** (108 localized screens, including cover and common final). Both languages were reread from the generated embedded corpus, and the nested Essential/Core story was checked for references that depended on excluded screens. The external historical baseline was not modified.

Only this collector folder and uniquely named evidence/report/ready files were written. Root reader, `books.json`, homepage, shared shell/template, release documents and root work log remain publisher-owned. No Git, PR, deployment, external messaging or subagent action was taken.

## What was read and what can be established

The exact witness is **Mark Twain, Adventures of Huckleberry Finn, Project Gutenberg #76, English illustrated HTML**, fetched from <https://www.gutenberg.org/files/76/76-h/76-h.htm>. Its title/subtitle, author and full sequence I–XLII plus The Last identify the novel rather than a sequel or condensation. The [catalogue record](https://www.gutenberg.org/ebooks/76) supplies language, ebook ID, illustration credit and update date. This is an electronic witness; no claim of first-printing or manuscript collation is made.

The complete file was downloaded outside the public tree: 653,544 bytes; SHA-256 `62e7dca69517602ac2cffa39fbaeb1b309016d79a85d993d301114ebe857bf8a`. Its working location is `/tmp/huck-primary-20261031-sol-worker/pg76.html`, with chapter extractions `01.txt`–`43.txt`. The source remains available at the direct URL, so the temporary extraction is not the only way to inspect the evidence.

Reading consisted of the opening and **targeted primary scenes across all 43 chapters**, with repeated checks of each retained causal link. XLII and The Last were read through. This does **not** mean continuous reading of every paragraph of the approximately novel-length full file. Availability, selected-scene reading and full-edition fidelity are different claims. The exact retained-action map, by stable ID and chapter anchor, is in the collector’s `sources.md`.

This evidence supports the retained arc, including its difficult ending. There is no unresolved missing primary link for the scenes retained here. Full dialectal/literary/translation fidelity is not certified. RU is a fresh paraphrase from the English evidence, not a named published translation. No Apple Books lookup or restricted access was needed. No purchase, loan or account action was taken.

## Resulting reading

Essential follows Huck from the widow’s restrictive household to Pap’s violent custody, the staged murder, Jim’s island refuge, life on the raft, the fog trick and apology, Cairo and the hunters, the missed turn and collision, the feud, the false royalty, the theatre scam, the Wilks inheritance fraud and Jim’s sale. It ends with Huck tearing up the letter and setting out to recover his friend. This is an intentional unresolved endpoint, explained on the cover and final screen.

Core inserts meaningful scenes without making Essential depend on them: Tom’s early gang, Pap’s false reform, the cannon/bread search, Jim’s shelter and the drifting house, the Walter Scott wreck, church and the hidden note, dawn and stars, the pirate collection, the forged reward poster, Elizabeth and the inheritance’s public gift/sale. Each additional scene contributes atmosphere, character or an actual complication, rather than a lesson.

Deep adds the snake prank, Solomon dispute, Boggs/Sherburn sequence and all events beyond Huck’s rescue decision. The Phelps identities, Tom’s elaborate evasion, Jim leaving his cell to help move the grindstone, the warning letters, shot, nursing decision, recapture, will, Tom’s foreknowledge, Pap’s identity and final intended departure are retained in disclosure order. Jim’s legal freedom is **not** earned through service to Tom; his care for Tom is his own consequential decision. Tom’s knowledge and appetite for adventure remain part of the harm in the ending. No later reunion of Jim’s family, Pap’s killer, or accomplished western journey is invented.

Huck’s conflict is kept in his remembered words and actions, rendered indirectly: helping Jim feels like theft and sin to him; betraying him also becomes unbearable. The apology and letter do not become a claim that he has permanently shed every prejudice. Humour stays attached to real episodes: Sunday robbers, the judge’s reform, corpse-search breakfast, mock royalty, the Nonesuch audience, picks called knives, spoon counting, butter under the hat. Material injustice remains in sale, separation, violence, capture, chains, threatened lynching and the doctor’s limited defence of Jim. No racial slurs are reproduced and no dialogue or quotation marks were fabricated.

## Length derived from the text

There was no inherited Huck Finn screen quota. Final cumulative `targetModes` are **24 / 36 / 54**: 24 level-1 screens, 12 level-2 additions and 18 level-3 additions. Counts include cover and final.

| Mode | Screens | RU words | EN words | Estimated RU / EN minutes |
| --- | ---: | ---: | ---: | ---: |
| Essential | 24 | 1,917 | 2,334 | 11 / 11 |
| Core | 36 | 2,839 | 3,455 | 16 / 16 |
| Deep | 54 | 4,227 | 5,124 | 24 / 24 |

Counts use the maintained builder’s title + subtitle + body convention. Body-only density among 52 narrative screens: RU 62–88 words, mean 75.9; EN 74–107 words, mean 91.9. These are diagnostics after writing, not target bands used to add filler.

## Concrete self-review corrections

These are corrections found while building the **new** package, not defects attributed to an absent historical Huck Finn edition.

| ID / area | Earlier wording or behaviour | Correction and primary support |
| --- | --- | --- |
| `judith-loftus` | “платье из плавучего дома” / “a dress from the floating house” depended on a Core-only event. | Essential now simply introduces the dress. IX supplies the salvage and XI the disguise. |
| `night-raft` | “Теперь они прячутся днём…” introduced the raft as if its acquisition were already known in Essential. | Added a concise backward link to catching the raft at the island. IX, XII and XV are mapped explicitly. |
| `buck-on-bank` | “София бежит…” left Essential readers without her family identity. | “София Грэнджерфорд” / “Sophia Grangerford”; XVIII establishes the relationship and elopement. |
| `forty-dirty-dollars` | Reference to “the printed notice” presumed the Core poster scene. | Introduces a **forged reward notice** within Essential itself; XXXI gives the handbill and $40 claim. |
| Saved Deep and contents | The plain builder has no book-local consent implementation. | Added a bilingual modal, masked level-3 TOC titles, guarded mode/chapter/position transitions, generic saved-Deep label and renewed consent on reload. No source-based ending title is shown before consent. |
| Cover | Shared template’s unused fallback graphic says “system/idea/consequence” and “model to carry forward”. | Removed that fallback from this book’s rendering; the cover is typographic narrative copy. No other reader was altered. |
| Deep duration | Builder’s Russian inflection would read “24 минут”. | Book-local explicit duration is “24 минуты”; no shared builder edit. |

## Build, runtime and checks

`author-story.py` keeps the book’s bilingual prose and emits the canonical JSON plus two prose review exports. `build-local.mjs` invokes the maintained `skills/book-tiktok/scripts/build_story.mjs`, then applies bounded, asserted book-specific consent, cover and colour changes. A plain builder rerun alone would remove these additions; use the local wrapper. A repeated wrapper build reproduced the same final HTML bytes. The shared compact header module is embedded unchanged.

The result defaults to RU/dark/Essential, uses narrative mode, includes embedded Geist/Geist Mono, Flexoki paper/ink and one violet primary action, and works as a local standalone file. Two source records are exposed only in Sources: one full primary witness and its metadata record. Reading screens carry no academic provenance labels. Source maps remain embedded.

The maintained auditor reports **69 structural checks, no warnings, no failures**. The local Chrome matrix traverses the actual rendered bodies for **all three modes × two languages × two themes × four viewports** (320×568, 390×844, 1024×768, 1440×900): 48 combinations / **1,824 screen visits**. Expected titles, body text, mode counts and progress match, with no horizontal overflow; final paragraphs and cover start controls are reachable by vertical scrolling. Desktop rails are visible and keep the active item in view.

Additional behaviour phases at 320, 390 and 1440 check dialogs, hidden chapter mode raising, repeated language/theme switches, keyboard, buttons, swipe, vertical gestures, focus mode, save/resume, cancellation and renewed Deep consent. An iPhone user-agent phase checks the install guide and its localization, standalone suppression, and a **real Chrome engine safe-area override** with 47px top / 34px bottom. The six controls fit one row below that inset; focus restores the correct header placement. This is emulation, **not physical iPhone/Safari testing**.

All browser phases run with network emulated offline. There are zero runtime exceptions and zero external runtime requests. Chrome is launched under `timeout 30`, in its own process group and `mktemp -d` profile. Each run kills only that group and removes its profile, including failure paths. No server was started. Reports and representative screenshots are in this collector’s `qa/`; their HTML hashes must match the ready receipt. Screenshots of the 320px cover/dense copy and 1440px English light reader were visually inspected; narrow screens deliberately scroll rather than shrink the prose.

## Remaining limits and publisher handoff

Independent content review is still pending. Local structural/browser checks establish implementation behaviour, not independent editorial acceptance. Publication has not occurred. All 54 changed pairs, the narrative sequence and corresponding primary passages remain available for that check.

The publisher should retain the book-local wrapper additions and generic Deep resume label, preserve the pre-final Essential/Core boundary, and integrate only the collector HTML whose hash matches the final ready receipt. Catalogue/root/index work belongs to the publisher. Classify this as fiction/adventure with satire where supported by the existing taxonomy. Younger-reader suitability, if recorded, is **internal metadata only**; do not introduce a public “children’s book” shelf or claim this is a harmless story without slavery or violence. Root work-log/release entries remain for the publisher because this worker’s file ownership excludes them.
