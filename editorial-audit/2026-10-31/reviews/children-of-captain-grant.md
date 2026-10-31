# Children of Captain Grant — independent content review

Date: 2026-10-31. **REQUIRES-FIXES** — one local, source-supported correction; no new rebuild requested.

## Reviewed version and reading

Read all **37 revised RU/EN pairs (74 language screens)**, including all titles, subtitles, cover, warning and final, and read the cumulative **Essential 14 / Core 23 / Deep 37** sequences in both languages. The collector HTML embeds exactly these screens; only generated `modes` metadata differs from the authoring JSON. Current ready-manifest hashes match all four author deliverables.

| Captured artifact | SHA-256 |
|---|---|
| `collector-output/children-of-captain-grant/story-data.json` | `f5e1163a4c1f6d743693535810d141e8beaa7540541831b0cd8a06447c2ffdc3` |
| `collector-output/children-of-captain-grant/children-of-captain-grant.html` | `a774ffcfeef3a2b15823ecec0be03e39f08c15f6713514f79979e82f6682f76f` |
| `editorial-audit/2026-10-31/ready/children-of-captain-grant.json` | `841d72882ca4d8e93ce3e5751b87f327910613928e286ef967c5293a575bf8d4` |

The root reader currently contains **144 old pairs**, not this candidate; its effective embedded corpus was inspected for that distinction. I did not reread the old 144-pair story or certify it. Root hash: `0adbab3c5853ef622bf8592255ab06828269dd8a159d185bcbc357ec9ab01280`. The detailed JSON records absolute paths, bytes, route IDs and evidence locations.

## Reader judgment

The rewritten text now tells an adventure. The damaged message produces a search; the children make its stakes personal; Robert and Thalcave act under danger; Paganel is both useful and fallible. The wrong ship, wrong language and tattoo secret preserve comedy. Betrayal, the presumed loss of Duncan, captivity, the mistaken order and reunion have a supported causal sequence. There are no inserted management lessons, exercises, invented direct quotations or scientific digressions.

The short routes can legitimately stop at the Snowy camp. Essential uses brisk but understandable ellipses between continents; Core adds the false trail, tree escape, farewell, sea journey and comic episodes. Deep completes the rescue, Ayrtons disposition, marriages and Paganel ending. I do not require every peripheral episode or a particular screen count. Both languages preserve the same meaningful story; their one source error is shared.

## Required finding: GRANT-CONTENT-01

**`toline-geography` — Core and Deep.**

RU: «Учёный хохочет над учебником. … Паганелю — книгу, из которой выучил свои ответы».

EN: “The scholar laughs at the textbook. … Paganel the book from which he learned his answers.”

This is the wrong book and changes the final comic gesture. In [Horne, Part II, Chapter XII](https://www.gutenberg.org/cache/epub/2083/pg2083-images.html), Paganel laughs at Tolines answers. Glenarvan then gives the boy a corrective geography, Richardsons Compendium. Toline accepts it without conviction; the next morning Paganel finds Richardsons Geography in his pocket. Toline is leaving the corrective gift behind, not giving Paganel the source of his erroneous lessons. The boys prize book earlier in the scene is a Bible, a separate object.

Primary passage actually read: private `ch-2-XII.txt`, lines **187–202, 224–360, 362–389**, under `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/children-of-captain-grant`. The final two ranges establish both the gift and its abandonment.

**Smallest correction:** retain the scene and position. In both languages make Paganel laugh at the answers, briefly establish Glenarvans gift, and identify the abandoned book as that corrective geography. Keep the mimosa and departure. No new scene, speech, moral, screen or count change is needed.

## Primary checking and limits

Independent checks covered the shark/bottle and three documents; the children and Helena; Robert learning seamanship; Paganel boarding/staying; Andes, earthquake, condor; Camões; drought, Thaouka and wolves; false captive; ombú/flood/fire and Thalcave farewell; islands, cabin and storm; Ayrtons claims, wagon and train; Toline; Majors tracking, shooting and stolen letter; Halley, abandonment, war and capture; Kara-Tete, digging and Robert; tomb/vent escape; Duncan and mistaken order; island bargain; night voice/reunion; message solution; return, marriages, colony project and tattoos. Exact checked locations and what was inspected are listed in the JSON, rather than treating the authors source ledger as independent proof.

The main witness is the **66-chapter Horne-edited English version** of Verne ([PG 2083](https://www.gutenberg.org/cache/epub/2083/pg2083-images.html)). Directly checked relevant French passages in Hetzel 1868 [I.II](https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_1/Chapitre_II), [III.XVII](https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XVII), [III.XXI](https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XXI) and [III.XXII](https://fr.wikisource.org/wiki/Les_Enfants_du_capitaine_Grant/Partie_3/Chapitre_XXII): minutes, wrong-country order/arrest, final message/double name, and closing fates/comedy. I do **not** claim a full French comparative collation or continuous every-paragraph reading of the complete English or French book. Russian is an original condensation, not an audited published translation. Tabor and spectacular animal/geological events were reviewed as the novels world, not validated as empirical facts. Complete lawful witnesses are accessible; there is no retained-plot source gap.

## Publisher handoff

No optional taste changes are required. Correct GRANT-CONTENT-01 in RU and EN, then validate the small edit against the cited passage and bind approval to the resulting new authoring/HTML hashes. This report itself is **not** a PASS on the current hashes.

Preserve `contentMode: narrative`, `spoilerPolicy: full-plot-in-deep`, the existing Deep warning, book-local consent dialog, `setMode` / `goToId` / `goToPosition` guards, consent reset, masked contents and neutral saved-Deep continuation labels, stable saved IDs and Home target handling. Static inspection found these protections in the reviewed collector; no fresh browser matrix was performed. A plain rebuild must not discard them.

Only this review Markdown and JSON were written. No reader, collector, root, shared file, Git/PR/deploy or external message was changed; no subagent was used.
