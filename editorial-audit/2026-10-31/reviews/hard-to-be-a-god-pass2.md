# Hard to Be a God — fresh independent recheck, round 2

**Verdict: REQUIRES-FIXES. All five prior findings, HG-01–HG-05, are CLOSED.** One small, pre-existing action detail remains in `palace-night` (HG-06 below). No substantive rewrite or source gap is required. This report does not approve the current hashes or any future changed hashes.

Reviewed 2026-10-31 by a new independent reviewer. I read the corrected BRIEF, first independent review, repair report and exact pass-2 ready manifest, then personally read **all 33 current RU/EN pairs**: every section, title, subtitle where present and body, plus cover/description, method/source notes and media alt/credit. I read the cumulative **8 Essential / 13 Core / 33 Deep** sequences in both languages. All six manifest-listed repaired pairs were included. Previous acceptance claims and QA counters were not used as literary evidence.

## Exact reviewed version

All paths below are relative to `/Users/pn/smartcat/_artifacts/book-tiktok-library`; the JSON also records absolute paths. The authoring and effective HTML corpus are identical except for the HTML’s generated `modes` labels/times. There is no root reader or root catalogue/index entry for this slug at the review boundary.

| File | SHA-256 |
| --- | --- |
| `collector-output/hard-to-be-a-god/story-data.json` | `7f340b24f744699f71164d4a0d48e8cd10aab877c37f3ade5d8f60d91face2ac` |
| `collector-output/hard-to-be-a-god/hard-to-be-a-god.html` | `53176ebbdc1806cf5513dccbdf4d85a21dd661057471a568759d486e30fb143c` |
| `collector-output/hard-to-be-a-god/sources.md` | `be60d15fd274369cf69b7046b66d78045897ac96bd7f4a46202b5489a9357545` |
| `collector-output/hard-to-be-a-god/QA.md` | `cfe107aa5cb975329fdcd29a2ac0d09008b198ec0bbc270c71008405627d61d8` |

These match `editorial-audit/2026-10-31/ready/hard-to-be-a-god.json`, pass 2, manifest SHA-256 `494f5147e022db892269f7fbc4d82c80f0f0f051e88bbe23e22dfde2665d35b8`. They were checked again before writing this report. The initial review’s JSON/Markdown remain unchanged at `b459ee984eec3b53ce3f2e357ef57317984de897352ec82ddc7ccf49a069d938` / `2c4855c54a6a9b00c000b5dc852c51a958ddd0f2c5f278525eafa742e5facbc6`.

## Primary evidence actually checked

Work: Arkady and Boris Strugatsky, «Трудно быть богом» / *Hard to Be a God*. Primary witness: [complete Russian electronic text on the official author site](https://www.rusf.ru/abs/books/tbb100.htm). A fresh live request returned HTTP 200 and **370,398 bytes**, byte-identical to the existing read-only private witness at `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-4-private/hard-to-be-a-god.html`; SHA-256 `02ef0f659c7e11b1fe60a85fce2be24b68fbac61e47a7a85add49df70cdf900d`. I read the passages directly from that matching witness. Retrieval was not counted as whole-book reading.

This recheck personally read: prologue P001–P008 and P127–P199; chapter 1 P098–P174; chapter 2 P023 and P118–P148; chapter 3 P055–P132; chapter 4 P022–P061 and P180–P218; chapter 5 P016–P034 and P120–P158; **complete chapter 6 P001–P033**; chapter 7 P148–P224 and P249–P280; chapter 8 P059–P151 and P177–P219, including the complete Budakh dialogue; **complete chapter 9 P001–P053**, **complete chapter 10 P001–P103**, and **complete epilogue P001–P037**. Truncated tool displays were re-read at the omitted ranges.

P numbers are independently regenerated nonempty HTML paragraph ordinals within each heading, not print pages. This extraction has 199 prologue paragraphs and 158 in chapter 5; earlier parsers’ slightly different ordinals should not be silently substituted. The JSON maps these actual readings to screen IDs. No complete source text or extraction was written into this repository.

This is selected continuous primary reading across the work, not an every-word continuous reading of the whole novel. No print edition, textual variants or published English translation were collated. EN is the translation of this condensation. The available primary evidence is sufficient for these retained events and arguments; no source gap blocks the localized correction below.

## HG-01–HG-05 closure decisions

| Finding | Decision | Directly checked result and primary locator |
| --- | --- | --- |
| **HG-01** — Arata’s argument | **CLOSED** | `lightning-demand` now includes the nobles, descendants, armies and supporters he intends to burn, plus the promised return of the weapons. `hope-burden` labels mortality as the lesser spoken argument, gives Rumata’s private land → serfdom → new barons forecast, and keeps his uneasy inferiority beside Arata. Arata’s charge that hope weakens his resolve and his departure/gold question remain. Both languages attribute the forecast to Rumata. **Complete chapter 9**, especially P023–P025 and P039–P052. |
| **HG-02** — Okana/Kira resolution | **CLOSED** | EN clearly identifies Okana’s attraction as the means Rumata considers using for information. Both languages show his departure without completing the encounter, subsequent drunken carousing with Pampa, Kira’s alarm, his confession and her brine response. The local relationship scene no longer ends at the growing lie. **Chapter 2 P023; chapter 3 P132; chapter 4 P022–P061 and P180–P218**, especially P215–P218. |
| **HG-03** — Budakh’s release | **CLOSED** | `clearance-ritual` distinguishes the useless authorization from a release order and supplies the actual bypass: purification bracelets, stamped paper, direct prison approach, the claim that the bishop gave him Budakh, delivery by the monks and removal of the noose. **Chapter 8 P059–P124**, especially P069, P079–P082 and P107–P124. |
| **HG-04** — closing chronology | **CLOSED** | `final` explicitly starts at the story’s outset and ends by naming the opening stakes in both languages. After the Deep epilogue it is a marked recap, not a renewed claim that Budakh is missing or Kira still awaits rescue. It preserves the lower-depth ending promise. Checked against **chapter 8 release, complete chapter 10 and complete epilogue**, and the actual shared `renderScreen()` body. |
| **HG-05** — target material | **CLOSED** | The unsupported paper adjective is gone in RU/EN. The cap description is supported by the rolled pirate headband, and aiming higher before the shot is explicit in the primary scene. **Prologue P127–P155**, especially P137–P152. |

## One remaining required correction

### HG-06 — unsupported weapon-breaking action

**Low; `palace-night`; Deep only.**

Current RU: «Румата отбивается, ломает оружие нападающих, но их слишком много».

Current EN: “He fights back and breaks their weapons, but there are too many.”

The checked capture scene establishes axes left on the floor and sprained arms after the first rush. A spear then knocks Rumata off the window ledge; he struggles against the crowd and is finally captured in a net. It does **not** establish the particular action of breaking the attackers’ weapons. Disarming or repelling them does not establish breakage. This is a small unsupported action detail, not a request to expand the battle or change its style.

**Primary locator:** [chapter 6, P029–P033](https://www.rusf.ru/abs/books/tbb100.htm), especially the first axe-bearing rush in P029 and the spear/crowd/net sequence in P032. The complete chapter was read and these paragraphs rechecked directly.

**Minimal correction — delete only that clause in both languages:**

- RU: «Румата отбивается, но их слишком много».
- EN: “He fights back, but there are too many.”

No extra scene, motive, philosophical lesson or new route is needed. The publisher can directly validate this bounded correction against the cited passage under the corrected BRIEF, rebuild and record new hashes. This report itself is **not a PASS on those future hashes**.

## Whole concise story, attribution and routes

The condensation carries its story through named people, encounters, danger and relationships. Kira’s brine and Pampa’s beer retain humour. The Budakh discussion remains an exchange at a meal: proposals to provide, protect, punish, give gradually and change desires receive Rumata’s actual objections. The Arata exchange now supplies the competing argument and Rumata’s inner historical forecast without converting either speaker into an editorial mouthpiece. No exercises, modern analogies or generic reader lessons replace these scenes. The repaired causal and attribution distinctions survive in EN. No optional prose-style changes are requested.

Essential’s eight screens form a comprehensible, spoiler-safe opening. Core’s thirteen add the road, Midas, Vaga, Pampa and the now-resolved Okana/Kira episode. Both close with explicitly identified opening stakes rather than pretending to tell a complete ending. Deep’s 33-screen route moves past its warning through coup, interrogation, Order takeover, actual releases, poison explanation, Budakh and Arata disputes, then the changed Earth discussion and last night with Kira. HG-06 is its only remaining required correction.

The late sequence is coherent: Budakh is sedated for travel; Condor reverses position and Gug objects; the helicopter conversation raises Kira’s vulnerability; Earth remains an imagined journey and Pampa’s castle an uncompleted shelter plan; the attack interrupts them. Kira’s death precedes Pashka’s incomplete Earth account. There is no invented definitive individual shooter, revenge choreography, victim total, announced cure or settled future for Arkanar. Pashka’s road connection stays uncertain. The last narrative scene is the author-supported berry-juice image; the following shared screen openly returns to the opening.

Decisive outcomes remain level 3 after the bilingual warning. Current `visibleScreens()` / `contentsHtml()` filtering hides those titles at lower depth, and `renderCover()` uses a generic saved-Deep warning. Cover, descriptions, method/source notes and media text do not disclose the decisive ending. Narrative mode suppresses academic labels and uses the actual method note. These are text/code checks, not browser or device certification. No browser matrix was needed or run; earlier rendering counts were not treated as literary evidence.

Only `reviews/hard-to-be-a-god-pass2.md` and `.json` were written. The first review, ready manifest, collector and root files were preserved. No Git/PR/publish/watch, subagents, external messages or worker polling/waiting. The publisher owns the small correction, rebuilt hashes and integration.
