# Hard to Be a God — independent content review

**Verdict: REQUIRES-FIXES.** Reviewed 2026-10-31. Read all **33 current RU/EN pairs**, including titles, section labels and bodies, plus the bilingual cover/description, source/method notes and media text. Evaluated the three nested sequences: **8 Essential / 13 Core / 33 Deep**. This is a new primary-text review; previous QA and old reviews do not establish this verdict.

Four substantive, localized repairs remain: Arata's philosophical exchange, the Okana/Kira scene's missing resolution, the action that frees Budakh, and the shared closing screen's return to unresolved opening stakes after the Deep ending. A fifth finding is a one-word factual cleanup. **There is no source gap and no request to rebuild the whole package.**

## Exact reviewed delivery

| File | SHA-256 |
| --- | --- |
| `collector-output/hard-to-be-a-god/story-data.json` | `5c759919f72aa5901d3c0987ce69584455646513e8d071a2d52e2f01379e9ddd` |
| `collector-output/hard-to-be-a-god/hard-to-be-a-god.html` | `4057f8fbf78892f0f7f0046b63b8f172759aaebaf67eb44b7f22a2dc1210dfa6` |
| `collector-output/hard-to-be-a-god/sources.md` | `186cae1aeaa29d8071a593e50aa0a00c8d22da7d36a1bdbb0a1a23638cfa68c9` |
| `collector-output/hard-to-be-a-god/QA.md` | `da172799dfb4546b850e171117bab11c0f4068fc6892cc248c332e1f648f62be` |

All four match the ready manifest at review time. The collector HTML's effective `book-tiktok-data` corpus has the same 33 paired texts and ordering as authoring JSON; its generated top-level `modes` addition is not a content divergence. No root `hard-to-be-a-god.html` or corresponding catalogue/index entry exists at this review boundary, so there is no published root corpus to certify.

## Primary evidence and limits

Work: Arkady and Boris Strugatsky, «Трудно быть богом» / *Hard to Be a God*. Witness: [complete Russian electronic text on the official author site](https://www.rusf.ru/abs/books/tbb100.htm). A specific print edition or variant was not collated. EN translates this condensation; it is not presented as a published English translation.

I checked the live author-site witness against the existing read-only private HTML at `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-4-private/hard-to-be-a-god.html`. The bytes match: **370,398 bytes**, SHA-256 `02ef0f659c7e11b1fe60a85fce2be24b68fbac61e47a7a85add49df70cdf900d`. No private/full primary text was written into public Git.

Actual reading covered the Tell/highway sequence; Kabani, Midas and the full first Condor dispute; Vaga's meeting and Okana's letter; Kira's home/refuge conversations; the failed Okana encounter and the drunken-return/confession sequence; both court passages; **complete chapter 6**; the chapter-7 identity/gold/duel/false-physician interrogation and Order reveal; the actual chancellery/prison/Pampa release; **the poison account and complete Budakh dialogue**; **complete chapter 9**, including Rumata's inner reflections; **complete chapter 10**; and **the complete epilogue**. The JSON records the exact selected paragraph ranges and associated screen IDs. Those P indices are generated locally within the checked HTML chapters, not invented print pages.

This is selected continuous primary reading across the work, not an every-word whole-edition certification. The disclosed boundary in `sources.md` is acceptable in itself. The complete primary witness supports the existing central sequence and the concrete corrections below. No missing full edition blocks them.

## Required findings

### HG-01 — restore the actual Arata dispute

**High; `lightning-demand`, `hope-burden`; Deep.**

Current RU: «ему нужны небесные молнии, чтобы рушить крепости»; «Даже если доверить оружие Арате, тот смертен, и оно попадёт в другие руки».

Current EN: “he wants more than gold: heavenly lightning to destroy fortresses”; “Even if Arata could be trusted with the weapons, he is mortal; they would pass into other hands.”

The primary scene goes beyond fortifications and future weapon ownership. Arata promises to destroy nobles, their descendants and supporters. Rumata explicitly gives mortality as only a lesser spoken objection; inwardly he anticipates rebel victors distributing land, requiring serfs and producing new barons. He nevertheless feels diminished beside Arata. Dropping both the threat and the internal historical argument changes the philosophical conflict into a problem of weapon custody.

**Evidence:** chapter 9, complete visit, especially local P039–P048. Read the whole scene, including the surrounding hope argument and departure.

**Smallest correction:** retain the two screens, add Arata's actual human targets, and add a short, explicitly attributed account of Rumata's inner objection. For example: «Румата приводит вслух лишь один довод; про себя он боится, что победители, раздавая землю, снова потребуют крепостных и превратятся в новых баронов». EN must carry the same distinction. Keep his uneasy respect; do not turn his prediction into an external narrator's universal lesson.

### HG-02 — finish the Okana/Kira scene and clarify the English motive

**Medium; `okana`; Core and Deep.**

Current RU: «После ночных похождений дома ждёт Кира. Румата пытается отделить одну жизнь от другой и чувствует, как между ними растёт ложь».

Current EN includes “Exploiting her desire for information repels him” and ends “he feels the lies growing between them.”

The English can mean that Okana desires information. Actually Rumata wants information and considers exploiting her attraction to him. He cannot go through with the encounter and leaves. Later, drunk after carousing with Pampa, he frightens Kira. In the morning he admits that what she saw was no dream; she offers to bring brine. The current cutoff retains the growing lie but removes its immediate resolution, Kira's response and the scene's affectionate humour.

**Evidence:** chapter 2 P023; chapter 4 P022–P053 and P181–P218, especially the final confession and response. These are actual adjacent narrative passages, not inferred motives.

**Smallest correction:** change the English to “Using her attraction to him to obtain information…” and replace the vague final sentences with the failed encounter, drunken return and confession/brine resolution. These events fit the same screen and reveal no protected ending. Do not suggest that he completed an affair with Okana or that this particular lie remained unconfessed.

### HG-03 — show the action that defeats the paper trap

**Medium; `clearance-ritual`; Deep.**

Current RU: «Румата пробивается через списки, кабинеты и разрешения… Наконец Румата добирается до настоящего врача и выводит его из заключения».

Current EN: “Rumata struggles through lists, rooms and permissions… At last Rumata reaches the real physician and brings him out of confinement.”

The useless document is present, but the means of escape from that procedure disappears. The opening also suggests a completed circuit of offices and permissions. In the primary scene he instead takes purification bracelets from the chest and goes directly to the prison with the stamped paper. He declares that the bishop has given him Budakh, and the guards hand the physician over. This observable action is the causal and comic payoff.

**Evidence:** chapter 8 P059–P082 and P103–P124, read continuously at both locations.

**Smallest correction:** replace the generalized traversal with taking the bracelets, displaying the paper and demanding Budakh as his own. Do not add administrative errands he does not perform. The JSON contains a short paired correction example.

### HG-04 — the shared final screen resets Deep's story

**Medium; `final`; Deep.**

Current RU: «Но Будаха ещё нужно найти, Киру — уберечь… Поиски ведут всё ближе к Рэбе».

Current EN: “Yet Budakh must still be found, Kira kept safe… The search draws him closer to Reba.”

In Deep this follows the rescue, Kira's death and the Earth/berry-juice epilogue. The unmarked present-tense reopening of the original tasks breaks the route. The current HTML directly renders this same body in all modes and marks this screen final; no mode-specific closure repairs it.

**Evidence:** chapter 8 release, complete chapter 10 and complete epilogue; actual final screen order and `renderScreen()` in the reviewed collector.

**Smallest correction:** explicitly frame the shared closing paragraph as a return to the opening situation — for example, start RU «В начале истории у Руматы есть…» / EN “At the story’s outset, Rumata has…” and keep the following stakes within that frame. A neutral recap also works. Preserve lower-mode spoiler safety; do not add late outcomes to a level-1 screen.

### HG-05 — remove the invented material of the target

**Low; `childhood-game`; every route.**

Current RU: «с бумажным колпаком на голове». Current EN: “with a paper cap on his head.”

The primary target is rolled from Pashka's pirate headband, then unfolded and worn again. The text does not make it paper.

**Evidence:** prologue P140–P155, checked directly.

**Smallest correction:** delete «бумажным» / “paper”, or name the rolled headband. This is a minor factual cleanup, not the meaningful basis for rejecting the package.

## Route, spoiler and fidelity judgment

Essential's eight-screen opening is intelligible and leaves the outcomes protected. Core's thirteen-screen sequence adds intelligible context, but `okana` needs its local resolution. Deep carries the real narrative through the epilogue, with the substantive repairs above.

The Budakh conversation already preserves the proposals and objections as the characters' own debate. Condor's change of position and Gug's objection are supported. Kira's Earth journey remains imaginary and the castle remains a plan, not an accomplished escape. The attacker is not assigned an invented definitive identity. The aftermath stays indirect, without invented revenge choreography, victim totals, cure or future for Arkanar. Pashka's road association remains uncertain, and the last berry-juice image is primary-supported.

Decisive outcomes are level 3, after the bilingual warning. The current contents filter hides those titles at lower depths, and the saved-Deep cover label uses a generic spoiler warning. Cover, descriptions, method/source notes and media text do not reveal the decisive ending; the external source is marked as containing the full plot. These are current copy/code checks, not a fresh browser/device certification. No browser matrix was run.

The parent can repair these localized findings. The publisher should validate the corrected paired wording against the cited passages, rebuild, check all three routes and refresh the ready hashes. **This review does not approve publication of the current hashes.** No collector, root or shared file was changed; no Git, PR, publish, messaging or agent action was taken.

