# The Neverending Story — source ledger

Status: **SOURCE-GAP — no reader and no ready manifest.** Checked 2026-10-31. This is the assigned queued novel, not an audit of an existing delivery. The machine-readable assessment is [source-evidence-map.json](source-evidence-map.json); the implementation handoff is [the-neverending-story-sol-implementation.md](../../editorial-audit/2026-10-31/books/the-neverending-story-sol-implementation.md).

## Work and edition boundary

Michael Ende, *Die unendliche Geschichte*, first published by Thienemann in 1979. The actual primary edition consulted here was a **publisher sample**, not a complete book: *La historia interminable*, Miguel Sáenz translation (1982), revised for the Loqueleo Colombia edition, ISBN **9789585939301**, May 2016, sample copyright leaf identifying the December 2017 third reprint. The publisher lists 544 pages; its public PDF contains **15 PDF pages**, of which printed pp. **7–15** contain the opening narrative. The excerpt stops during the bookshop episode. It is neither a full novel nor a summary EPUB.

No Russian or English full edition was consulted. Ralph Manheim's translation is identified by the English publisher, but its body was not obtained. Any future RU/EN condensation must be original bilingual prose, with names checked against the chosen source edition; it must not claim to translate an entire edition.

The authorized Apple Books root was searched read-only for the assigned title and author: scoped title/creator fields in expanded OPF metadata and packaged EPUB OPFs, plus assigned-title filenames. No candidate matched. Consequently there is **no local OPF/spine/body-extent verification to report**. This says nothing about books outside that root. No unrelated library names are included in the saved record. No owned/private book text was copied into the repository.

## Consulted sources

### S1 — Primary novel excerpt, Loqueleo Colombia

- [Publisher's 15-page sample](https://www.loqueleo.com/co/uploads/2019/07/9789585939301.pdf).
- [Edition page](https://www.loqueleo.com/co/libro/la-historia-interminable).
- Role: **primary novel text, bounded excerpt**. Read the rights leaf and opening narrative, printed pp. 7–15. Direct PDF retrieved and extent checked; SHA-256 `fbdc2d5f6470b609eb48300d2119c18c4bda154b768d80595c1f0e09fa51bf78`, 1,699,899 bytes, 15 extracted pages.
- Supports the opening's physical setting, Bastian's conversation with Koreander, the relationship background he discloses, and the particular book that attracts him. Does not reach the actual departure with the book, school attic or either quest.
- Metadata caution: the current product page contains an unrelated Babar promotional sentence. That sentence is not evidence about this novel; identity and translation were checked on the sample's rights leaf.

### S2 — Santillana / Grup Promotor, 2018 Catalan reading guide

- [Official 28-page guide](https://back-edupack.santillana.es/file/repository/La_historia_interminable_938924.pdf).
- Role: **publisher teaching guide**, with some explicitly quoted primary passages. Inspected its introduction, teacher commentary, questions, quoted extracts and answer key. Direct PDF retrieved; SHA-256 `fa060ec1f3bed2cb2775b7d46cc6c4a4ec22d0334ed759a396f0016f3653d294`, 508,280 bytes, 28 extracted pages.
- Useful bounded evidence: relationship sequence in printed p. 4; primary quotation about the two kinds of world crossing in p. 18; actual game answers in pp. 26–27, rather than the questions alone. Those answers corroborate several named stations and details in both halves.
- Limits: the guide does not narrate the late causal chain continuously. Its learning/values interpretations are the guide's, not a replacement for Ende's events or a definitive authorial meaning. Its question about who permits Bastian to leave is **not** itself an answer.
- Page convention: the cover is PDF p. 1; guide printed p. 18 is PDF p. 19. Guide references to novel pages belong to its Catalan edition, not to the Spanish, German or English editions.

### S3 — Viviana Gómez, Santillana / Loqueleo Colombia teaching project

- [Official eight-page teacher guide](https://www.loqueleo.com/co/uploads/2019/03/proylect-g7-la-historia-interminable-pages.pdf).
- Role: **accountable publisher guide**, not novel text. Inspected all eight pages, especially workshops 5–7. Direct PDF retrieved; SHA-256 `6daf652d97cd8d786634c5c24696dc2ad95562142c5be614018847288b50bb85`, 1,517,609 bytes, eight extracted pages.
- Printed p. 6 explicitly supplies Atreyu's purpose in the confrontation over the gem; printed p. 7 distinguishes the 1984 film's coverage from the whole novel. Other late stations are identified, but many actions and outcomes are left for students to retrieve from the book.
- Limits: the wish-loss table on p. 5 has no filled answers. The Aiuola/Mine questions on p. 6 likewise have no answers. Their wording must not be expanded into verified plot. The guide's classroom morality exercises will not be adapted into reading screens.

### S4 — Michael Ende official site, work/characters/lexicon page

- [Die Unendliche Geschichte](https://www.michaelende.de/die-unendliche-geschichte).
- Role: **official estate/publisher context and selected reference entries**, not complete novel text. Consulted the work description, relevant character entries and the short Amargánth entry. Supports work identity, the existence of Bastian's second journey and several bounded character/place facts. Some entries also contain interpretation, speculation or later material; those must not silently become novel events.
- Not sufficient to connect the second arc's wishes, conflict and return.

### S5 — Michael Ende official site, composition history

- [The Neverending Story](https://www.michaelende.de/en/author/biography/neverending-story).
- Role: **official biographical account**, not primary narrative. Consulted the composition account and interpretation caveat. Supports the significance of finding a way out of Phantásia to the book's development; does not supply the missing late scenes.

### S6 — Thienemann German edition record

- [Die unendliche Geschichte, ISBN 9783522202602](https://www.thienemann.de/produkt/die-unendliche-geschichte-isbn-978-3-522-20260-2).
- Role: **publisher bibliography/description**, not whole-book evidence. Metadata inspected: 2019 edition, 480 pages. Its lawful “Blick ins Buch” link leads to a Bic-Media widget; no primary body from that widget was acquired.

### S7 — English edition record

- [Penguin Random House Elementary Education](https://penguinrandomhouseelementaryeducation.com/book/?isbn=9780525457589).
- Role: **publisher bibliography only**. Identifies Ralph Manheim, Dutton Books for Young Readers, March 1997, 400 pages, ISBN 9780525457589. No full English text read.

## Access attempts that did not supply evidence

- Oqueleo's [Galician sample link](https://www.oqueleo.com/uploads/2020/05/a-historia-interminable.pdf), linked by its [edition page](https://www.oqueleo.com/libro/a-historia-interminable): search/fetch metadata initially reported a 39-page sample; the follow-up redirected, and direct retrieval returned 403. No complete sample reading or later-arc coverage claimed.
- Roman and Patrick Hocke's *Phantásien-Lexikon* is identified on the [official Ende site](https://www.michaelende.de/buch/die-unendliche-geschichte-das-phantasien-lexikon). Its [Lesejury sample](https://www.lesejury.de/media/samples/509/9783522200509_leseprobe.pdf) could not be retrieved (503). Search snippets are discovery only, not checked primary hinges or a complete lexicon reading.
- Official biography/product pages sometimes returned 503 to direct retrieval while browser-independent web extraction remained available. Only the actually extracted relevant text is counted.
- Generic recap results, film/TV material, unattributed full-book PDFs and user-uploaded copies were not adopted as plot authority. No unofficial full-text download, purchase, loan, account action or access bypass was used.

## Sufficiency decision

The guides and official reference material **do support particular facts**; they are not being discarded because they are not full text. However, this combination leaves essential links in the requested whole-novel story unverified. In particular it cannot yet sustain the sequence from Bastian's wishes and their cost through the damaged friendship and the specific route back, or the complete relation between the reading frame and its conclusion. See gaps G1–G6 in the evidence map.

The narrowest useful next evidence is primary passages for those links, or a substantial accountable guide that actually supplies the missing actions and causes, with selected primary hinges checked. A complete owned edition would be convenient, **not a universal prerequisite**. No first-half-only reader, invented connective prose, target counts or publication-ready certificate has been produced.

---

## 2026-10-31 — source rescue pass2, subsequent candidate

The preceding ledger is the unchanged first-pass history. Pass2 has now produced a **candidate for independent checking**, with both halves of the novel. This is not an independent content PASS or a whole-edition reading certificate. The new [pass2 report](../../editorial-audit/2026-10-31/books/the-neverending-story-source-rescue-pass2.md) and [pass2 evidence map](../../editorial-audit/2026-10-31/source-rescue/the-neverending-story-pass2.json) describe the later evidence and supersede the old SOURCE-GAP decision **for this retained condensation**. The original `source-evidence-map.json` remains unchanged as history.

### What this worker actually consulted

Read all six publicly extracted SuperSummary chapter-account pages, from prologue/chapter 3 through chapters 23–26, and relevant analysis/quotation passages. These are substantial professionally published event accounts, not unanswered classroom questions. No individual guide author byline was visible; institutional accountability is to SuperSummary. Its stated reference edition is Ralph Manheim's English translation, Penguin, 1984. I did **not** acquire or read that full edition, buy a guide, log in, unlock a paywall or extract protected hidden content.

Read selected sections and quotations in Marcus Schnöbel's 1995 state-examination study, selected passages in Albert Meier's novel section, H. J. Schueler's 1987 essay and selected Maria Nikolajeva material as publicly reprinted by Gale/Encyclopedia.com, and Brian Stableford's named EBSCO article. These are secondary criticism/reference accounts. Explicit novel quotations within them were checked **as reproduced primary excerpts**, separately from their surrounding interpretation; they are not a continuous primary-edition reading or a newly obtained publisher-authorized late-chapter preview. No critic's symbolic interpretation becomes a scene or an author-certified meaning in the reader.

For the opening, I reconsulted the actual S1 Spanish sample, printed pp. 7–15. Its 15-page extent, 1,699,899 bytes and SHA-256 remain as recorded above. This was an authoring check of the already obtained opening, not claimed as new late-arc sourcing. The translation/rights-leaf metadata above is retained from pass1. No complete RU, EN, DE or ES edition was obtained. The RU and EN are original condensation prose, with Russian names rendered for this retelling, not an official published translation.

The earlier scoped Apple Books title/creator search found no matching work. I relied on that recorded result rather than rerunning the exhausted search. Consequently pass2 has no newly found EPUB, OPF/spine/body inspection or full-versus-condensation classification to claim. No unrelated library filenames or private book body were saved.

### Source numbers used by the new story-data.json

The new JSON uses numeric IDs; these do not rename the historical S1–S7 ledger.

| Data ID | Direct source | Actual role and consulted locator |
|---|---|---|
| 1 | [Loqueleo primary sample](https://www.loqueleo.com/co/uploads/2019/07/9789585939301.pdf) | Same S1; actual opening pp. 7–15. |
| 2 | [SuperSummary prologue–3](https://www.supersummary.com/the-neverending-story/prologue-chapter-3-summary/) | Secondary events: opening and first Quest. |
| 3 | [SuperSummary 4–7](https://www.supersummary.com/the-neverending-story/chapters-4-7-summary/) | Secondary events; selected primary quotations. |
| 4 | [SuperSummary 8–12](https://www.supersummary.com/the-neverending-story/chapters-8-12-summary/) | Secondary continuous account of the reading frame. |
| 5 | [SuperSummary 13–18](https://www.supersummary.com/the-neverending-story/chapters-13-18-summary/) | Secondary events; selected quotation hinges. |
| 6 | [SuperSummary 19–22](https://www.supersummary.com/the-neverending-story/chapters-19-22-summary/) | Secondary events and causes, kept separate from evaluative analysis. |
| 7 | [SuperSummary 23–26](https://www.supersummary.com/the-neverending-story/chapters-23-26-summary/) | Substantial late-event account, not novel body. Spoilers. |
| 8 | [SuperSummary quoted passages](https://www.supersummary.com/the-neverending-story/important-quotes/) | Primary excerpts reproduced in a guide; adjacent interpretation excluded. |
| 9 | [Marcus Schnöbel, 1995](https://d-nb.info/1050266595/34) | Selected synopsis, structural event lists and quoted primary places; bibliography identifies Stuttgart 1979. Not a peer-reviewed monograph. |
| 10 | [Albert Meier, Postmoderne](https://www.litwiss-online.uni-kiel.de/wp-content/uploads/2017/03/Deutschsprachige-Texte-der-Postmoderne-Albert-Meier_Postmoderne.pdf) | Selected printed pp. 92–95: commentary and quotations, not a full edition. |
| 11 | [Gale critical anthology](https://www.encyclopedia.com/children/academic-and-educational-journals/neverending-story) | Schueler, *Seminar* 23.4 (1987), 355–374, and selected Nikolajeva passages, with explicitly reproduced primary quotations. |
| 12 | [Brian Stableford / EBSCO](https://www.ebsco.com/research-starters/literature-and-writing/neverending-story-michael-ende) | Named reference account; Form and Content section. |

Schnöbel PDF: 164 pages, 1,175,461 bytes, SHA-256 `973ac49fcbbd48d99d7bd81ebc4b6ffa404351a14c68ee38d98d592675d54099`. Download and extraction used an automatically removed temporary directory outside the repository. Meier/Gale/SuperSummary/EBSCO were consulted through web extraction; I do not invent download hashes for them.

### What changes the evidence decision

G1 now has a continuous chapter-XII/XIII account plus Schnöbel's explicitly quoted Old Man command and entry passage (PDF pp. 148–149; printed pp. 144–145). G2 has the guide's actual quoted memory rule, alongside successive event examples. G3 has a continuous event chain and Schnöbel's primary injury quotation (PDF p. 90, printed p. 86, note 366). G4 has the changed desire stated in the event account and Schueler's explicit primary quotation. G5 has an actual mining quotation, a continuous obstacle/exit account and independently differentiated help. G6 has the continuous closing account, quoted paternal response/tears, and an independent reference check. Exact per-gap/screen locators are in the pass2 map; none of this is inferred from a teacher's question.

Secondary page citations are reported as the source gives them. They were not checked against a complete owned edition. In particular Meier's printed p. 93 contains a suspicious novel-page reference, 466; it is not adopted as a certified 1979 page locator. The plot overview's loose Sikanda description and the guide's claim that the mirror alone marks physical entry were also not adopted. The reader retains the force/self-drawing distinction and separates mirror contact from the later entry.

### Fresh access limits

- The Mythlore/Filmer landing page was accessible, but its linked full article returned 403. No full Filmer reading or support is claimed; it was not retried or bypassed.
- The Vienna Phaidra candidate returned no readable body to web extraction; the direct request supplied an empty file. No thesis body was read or counted as evidence.
- An incorrectly guessed SuperSummary chapter-group route was inaccessible; its ordinary linked `chapters-8-12-summary/` supplied the actual account. No protected route was used.
- The first pass's failed Oqueleo, Lesejury and Bic-Media requests were not repeated. Unofficial full-book results were not opened as book sources or downloaded.

The supported candidate omits minor subplots rather than inventing them. Its public Sources notes remain spoiler-safe; this research ledger and the linked external accounts contain plot spoilers. Independent review must assess the 35 pairs and this mixed evidence boundary before any release.


## Parent chronology correction — 2026-10-31

NES-ORDER-001: moved the existing the-price record immediately before acharis, as the independent review requires. Every screen field, RU/EN word, ID, level, source mapping and media assignment is unchanged; Essential/Core ID order is exactly unchanged. Only Deep’s two adjacent records change order. The matching connected draft and preparation metadata order are synchronized. The original review checked the Chapter XVIII account and DNB dissertation printed148/PDF152; its exact source locators remain preserved. Outer reader code/styles, Settings/fonts and bespoke consent guard are byte-identical. No extra invented narrative, full-edition reading or independent self-PASS.
