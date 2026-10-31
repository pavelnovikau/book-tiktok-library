# Northern Lights — Sol implementation handoff

2026-10-31. **REBUILD / first implementation of an approved queued work.** Status: **ready-for-independent-check**. This is the implementation author’s record, not independent editorial approval.

## Work, ownership and material read

Philip Pullman’s *Northern Lights* (1995), first novel of *His Dark Materials*; *The Golden Compass* is its US title. Minor UK/US excerpt differences are acknowledged. No sequel, film, television or stage development is used as novel evidence.

At the start there was no `collector-output/northern-lights` package to repair; the queue marked the book not started. Old collector pairs read: **0**. Old published pairs read: **0**. This handoff does not claim to have audited an old published reader. Newly written and read: **43 bilingual pairs / 86 language texts**, including cover and shared final; **41 narrative scene screens**. The effective embedded HTML corpus was read, not merely the authoring JSON. Essential, Core and Deep were checked as continuous sequences: **17 / 22 / 43**, or 82 pair appearances. Three final source/causal corrections and the shorter cover were reread after rebuild.

Writes were limited to `collector-output/northern-lights/`, this report and its evidence directory, and `ready/northern-lights.json`. Root readers/catalogue/index, shared shell, settings, fonts, installed skill and logs were not edited. No subagents, Git, PR, deployment or external messages were used.

## Source assessment

Scoped Apple Books metadata search: **217 expanded OPFs plus one ZIP EPUB OPF**, no metadata read errors, no matching author/title edition. No unrelated filenames were recorded. Because no match was found, no target spine/body could be classified as full edition, abridgment or summary. This is not a claim that a complete EPUB was verified or read.

The retained chain is supported by substantial accountable guidance and checked primary hinges, rather than a complete primary reading:

- Scholastic’s 17-page opening extract at [LoveReading4Kids](https://www.lovereading4kids.co.uk/extract/955/Northern-Lights-by-Philip-Pullman.html): the entire first-chapter text on PDF pp. 3–17 was read via local OCR. Its print ISBN/year are unspecified. This is a primary sample, not a condensation or a complete edition.
- Helen Mason’s [official ZigZag Education inspection PDF](https://zigzageducation.co.uk/samplepdf/English/s5161.pdf), 111 PDF pages, June 2013: all 23 chapter prose summaries, relevant factual answer keys and selected authentic novel quotations were consulted. Its named base edition is Scholastic UK, 2011 [1995], no ISBN supplied. Questions were not treated as their own answers; imaginative exercises and film comparison material were excluded. Direct shell fetches returned 403; the official PDF was readable through the web tool, without bypassing access controls or finding an unofficial full text.
- [Systime’s publisher supplement](https://supplerendematerialer.systime.dk/fileadmin/indhold/SupplerendeMaterialer/A_Short_History_of_Literature_in_English/Fantasy/Pullmanwebopg.pdf): northern-arrival passage and five paired English UK/US primary extracts, including Pan at sea and the consul’s cloud-pine test. The Danish translation was excluded.
- A short original passage in the Scholastic 2019 description carried by [Foyles](https://www.foyles.co.uk/book/his-dark-materials-northern-lights-gift-edition/philip-pullman/9781407198705), narrowly checking a character’s stated Dust/original-sin position; the blurb did not fill plot gaps.
- [PRH’s first-volume listing](https://www.penguinrandomhouse.com/books/136447/his-dark-materials-the-golden-compass-book-1-by-philip-pullman/), Knopf paperback 2002, ISBN 9780375823459, used for bibliographic identification and the broad rescue premise. The complete edition was not read.

No essential link in the **retained concise sequence** is reconstructed from memory. Its later action chain, especially the last chapter, remains guide-backed. Quoted primary landscape/sound fragments in that section do not establish a false claim that the whole primary scene was read. The map makes that distinction screen by screen. No whole-book fidelity or translation certificate is offered.

Full source scope and locators: `collector-output/northern-lights/sources.md` and `source-evidence-map.json` (43 records). Read-only search and actual access records: `books/northern-lights-sol-implementation-evidence/owned-edition-search.json` and `source-access.json`. No copyrighted sample, OCR, complete source text, borrowed cover or private edition was placed in the collector/public tree.

## Narrative and exact changes

Wrote 16 connected original prose paragraphs per language in `narrative-ru.md` and `narrative-en.md`, then divided at narrative beats. The segmenter asserts that every manuscript story sentence appears in the same order; no quota filler was added. Derived counts are **17 Essential / 22 Core / 43 Deep**, including cover/final; physical levels are 17 + 5 + 21. All story screens use `claimType: book`; `contentMode: narrative` hides per-screen research chrome while keeping source maps and the global Sources dialog.

The story follows Lyra and Pan through the forbidden room, Roger’s disappearance, the London party and flight, the Costas and John Faa, the alethiometer, Trollesund and Iorek, then the northern quest and its consequences. Coram and Serafina retain a personal history. Adults’ contradictory actions carry the moral complexity: no management essay, modern religious/political lesson, reader exercise, invented speech or invented scene replaces events. Lyra’s absurd tales are described as tales she tells inside the novel, not reported as things Asriel really did.

Essential/Core stop with the children found inside Bolvangar and the urgent threat still unresolved. Deep adds the other northern scenes, outcomes and the first novel’s last scene. It does not import later explanations of Dust or prophecy identities.

Concrete self-review findings and corrections:

| Stable screen ID | Draft wording / defect | Final correction | Evidence |
| --- | --- | --- | --- |
| `the-bear-without-armour`, `armour-and-snow` | Kaisa’s arrival originally followed armour recovery. | Night visit precedes recovery and departure. | Guide ch. 11, printed p. 53 / PDF p. 58. |
| `before-the-fight`, `a-outrance` | Naming originally followed the duel. | Silvertongue naming moved before the combat. | Ch. 20, printed pp. 84–85 / PDF pp. 89–90. |
| `a-outrance` | “Iofur can already feel victory.” | Observable taunting replaces private-feeling specificity. | Actual novel battle quotation, printed p. 84 / PDF p. 89. |
| `the-party` | “At a party she overhears the adults.” | Mrs Coulter/London named in the shared sentence, so Essential has the needed context; Church-body identity stated as a story fact. | Chs. 2, 4–5, printed pp. 16, 23, 27. |
| `lyras-jordan` | “Her friend Roger works in the kitchens.” | Optional job detail omitted because it was not specifically established in the consulted passages. Friendship/exploration retained. | Ch. 3, printed p. 20; publisher description. |
| `tall-stories` | “But stories will not persuade John Faa to take her along.” | Removed implied persuasion/decision mechanism; Faa simply still refuses. | Ch. 8, printed p. 38 / PDF p. 43. |
| `asriels-plan` | “He gives the alethiometer back to Lyra.” | He tells her to keep it; no unverified physical handover. | Ch. 21, printed p. 89 / PDF p. 94. |
| `cover` | Long warning and “Deep · спойлеры” label clipped/extended the 320px cover. | Concise spoiler warning, short Deep label, separate full consent dialog. Fresh Start control fits on screen. | Final mobile screenshot and browser receipt. |

These are findings in the implementation draft, not fabricated defects attributed to an absent old book. The complete reading record is in `northern-lights-sol-implementation-evidence/implementation-reading.json`.

Negative controls: Tony Makarios is kept distinct from Billy Costa; Iofur is not replaced with a film king’s name; no film event reordering; no sequel fate for Lee, witches or other characters; Asriel’s claims are attributed to him rather than asserted as author-certified truth. No invented primary quotations or novel page citations appear in the reading prose.

## Build, integration boundary and verification

Four canonical files created:

1. `collector-output/northern-lights/story-data.json`
2. `collector-output/northern-lights/northern-lights.html`
3. `collector-output/northern-lights/sources.md`
4. `collector-output/northern-lights/QA.md`

`build-local.mjs` calls the maintained v2 builder and adds only this book’s spoiler/cover behavior and local violet action treatment. Shared settings PR29 is left to its separate review. Embedded fonts are unchanged maintained assets. A book rebuild records builder/template/header input hashes in `qa/build.json`.

The deterministic audit records **69 structural checks**, zero warnings/failures. Corpus parity confirms canonical/embedded equality for all screens, sources, method note, counts and policy, plus complete manuscript segmentation in each language. These mechanical checks do not certify fidelity.

Real Chromium checks used offline `file://` navigation at **320×568, 390×844, 1024×768, 1440×900**, both languages, both themes and every screen of every depth: **1,312 rendered checks**, no horizontal overflow, runtime exception or remote runtime request. Embedded Geist and Geist Mono loaded offline. Mode counts, source-dialog access, hidden source labels, one-row icon header, desktop rail synchronization and localized controls were exercised.

Deep mode selection, hidden chapter selection and saved Deep Continue require consent. Cancellation preserves the shallow position. Reload and downgrade revoke consent. Contents hide Deep titles before consent; cover resume uses a generic warning instead of an ending title. Final copy and global source/method notes stay safe. Buttons, keyboard, horizontal swipe, vertical-scroll non-navigation, focus taps/keyboard, Next in focus, dialogs, language/theme/ID preservation, Continue, Start over and restart were checked. iPhone browser install-guide behavior, six-control header with simulated 24px inset, and emulated standalone suppression were checked.

Visually inspected final screenshots: fresh 320px RU/dark cover, dense 320px EN/light prose, 1440px EN/dark rail/prose, 390px shared final and 320px safe-area emulation. Physical Safari/installed-PWA behavior was **not** tested. The home control preserves `href="./"` for eventual root placement; actual library navigation after integration is the publisher’s check.

Each Chrome phase used `timeout 30`, its own `mktemp -d` profile, owned-process-group cleanup and profile deletion. No server was started. All final receipts bind to the current HTML hash. Detailed commands and results: canonical `QA.md`, `qa/structure-audit.json`, `qa/corpus-parity.json`, and four `qa/browser-*.json` receipts.

Approximate reading times: RU **5 / 6 / 11 min**, EN **5 / 5 / 11 min**. Builder word totals: RU **737 / 919 / 1853**, EN **886 / 1093 / 2224**. Story body words average **40.7 RU / 48.4 EN**; ranges **21–64 / 22–80**. No images need decoding; cover is typographic.

## Remaining limits and handoff

Independent editorial review is pending; publisher owns integration, catalogue/discovery treatment, root reader and publication. This worker makes no changes there. No new semantic cover motif or shared shell change is claimed.

The absence of a complete primary edition and a continuously read published Russian translation remains a disclosed evidence limit. The selected, source-supported retelling is ready to be assessed on those particular retained links. Review may request additional primary reading; this record does not preempt that judgment. No unresolved essential retained-story gap was filled with invented text. Runtime QA is Chromium emulation rather than a physical iPhone test. Global Settings PR29 remains separate.

The ready record contains canonical paths and SHA-256 hashes, exact counts, this report and evidence paths, specific changes, evidence scope, boundaries and unresolved review items. Its status is only `ready-for-independent-check`.
