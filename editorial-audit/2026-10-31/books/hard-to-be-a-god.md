# hard-to-be-a-god — editorial repair, 2026-10-31

Verdict: **REBUILD completed; ready for independent check within the stated source scope.** Read all **112 original RU/EN pairs**; compared effective collector HTML JSON (identical). No root HTML/catalogue entry exists. Rewrote and reviewed **33 final pairs**, nested **8/13/33** rather than 30/72/112. New prose follows the search, palace intrigue, rescue, arguments, Kira's fate and the epilogue; philosophical speech remains part of the story.

## Findings by old ID

| Old stable ID | Actual wording / effect | Category | Repair / primary location |
|---|---|---|---|
| `cover`, `can-help` | «Аналитический спутник»; «Представьте: вы сильнее любого местного правителя…» | Wrong experience / hypothetical framing | Story begins with the childhood shot and moves to Rumata's undercover life. Prologue/ch. 1, https://www.rusf.ru/abs/books/tbb100.htm . |
| `god-not-literal`, `alien-not-past`, `two-identities` | Explanations of interpretive categories displace meeting the operative in his surroundings. | Broken narrative | Show the false name, Earth mission, hidden Midas and Kabani's hut. Ch. 1. |
| `institutional-cartography`, `model-vs-test`, `modest-protocol` | «карта» of institutions, falsification test, «Четыре вопроса вместо позы спасителя» | Unrequested frameworks | Removed. Vaga's actual bargaining, the minister's coercion and clearance bureaucracy carry the power relations. Ch. 2, 7–8. |
| `condor-not-caricature`, `time-horizons`, `condor-vulnerability` | Extended first-meeting interpretation; the crucial later reversal is absent. | Material omission | Keep first restraint dispute, then restore **Condor's call to remove Reba physically and Gug's shocked objection** after the coup. Ch. 1 and complete ch. 10. This prevents turning Condor into one unchanging moral position. |
| `person-as-refuge`, `hierarchy-of-rescue`, `kira-narrative-cost` | Kira is mostly discussed as a literary/ethical problem. | Scene displaced by criticism | Restore her waiting, concern, desire to know Rumata and final conversation. Ch. 3–4, 7–8, complete ch. 10. No invented private monologue. |
| `budakh-search`, `budakh-trap`, `liberation-not-system` | A search plus analysis without a clear enough court → false doctor → coup → release chain. | Causal omission | Connected narrative now shows the court performance, coercion behind poison, and Rumata's unwitting use in the intrigue. Ch. 5–8. |
| `gifts-capture`, `punish-replace`, `care-dependency`, `remake-person`, `pity-withdrawal` | Validly distinguished speeches are repeatedly interrupted by external caveats about aid and science. | Reading momentum | Retell the **actual** Budakh proposals and Rumata replies in four connected screens. Read complete dialogue, ch. 8. Arguments remain attributed; no universal aid policy is invented. |
| `lightning-demand`, `weapon-inheritance`, `hope-burden` | Main dramatic exchange diluted by explanatory extensions. | Pacing | Arata asks for weapons; Rumata refuses; Arata accuses his presence of creating false hope. Ch. 9. |
| `camera-blackout`, `violence-not-payoff`, `road-nonreturn`, `strawberry-image` | Useful uncertainties, but packaged as lessons about form. | KEEP boundaries / rewrite prose | Let Pashka's incomplete telling and the friends' reunion carry the withholding. Epilogue. No casualty total or choreographed rampage, no proof that the road is an authorial historical law. |
| `read-for-voices`, `safe-handoff`, `final` | Reader instructions and abstract takeaway questions end the book. | Unrequested lesson | Removed. Early depths stop at the unresolved search; Deep reaches the real last image. |
| `cover` / saved `strawberry-image` resume path | Old JSON lacked `spoilerPolicy`; actual browser could display “Continue: Red on his fingers” on an Essential cover. | **Spoiler metadata defect** | Added book-local `spoilerPolicy: full-plot-in-deep`, authors and adult audience. Rerun masks the title as “Continue Deep — ending spoilers”. Shared shell left untouched. |

These are predominantly omissions, unwanted interpretation and a delivery metadata defect, not a claim that every old analytical observation was factually false. Old green QA did not establish the corrected task's reading experience.

## Source boundary

Complete official author-site witness retrieved privately. Actual meaningful plot passages across all ten chapters were read through the ending before authoring, plus complete Budakh dialogue, final chapter and epilogue. Some long chapter middles/peripheral passages were not read continuously. **No every-word whole-novella reading, print-variant collation or whole-edition fidelity certification is claimed.** sources.md records exact coverage and scene locators. English is an original translation of the new condensation. Private full text stays outside the public repository. No film or review fills unread scenes.

## Checks and integration notes

Updated four collector canonical files. `contentMode: narrative`, no academic evidence footer in the actual new render. Structural audit **69 passes / 0 warnings / 0 failures**. Browser **432 instances**, all depths/languages/themes at 320×568 and 1440×900; no horizontal overflow, remote requests or runtime errors. Sources, default state and saved-Deep warning passed after correcting the metadata bug. Narrow screenshot inspected; physical iPhone/PWA remains untested. Details in QA.md.

Publisher attention: **33 total, nested 8/13/33, RU/EN 3/4/9 minute estimates**; use new description and explicit spoiler metadata when integrating. Save-progress IDs now carry different text or are gone: migrate/invalidate any prior circulated progress deliberately. Root/counter/catalogue/deploy work and independent editorial acceptance remain with the publisher. No shared-shell or installed-skill change was made.


---

## Pass 2 — substantive independent-review repairs, 2026-10-31

Current implementation verdict: **EDIT completed; ready-for-independent-check**, with no independent acceptance or publication certification. The earlier report above is retained as history; the independent **REQUIRES-FIXES** review found four substantive omissions/breaks plus one unsupported adjective in those earlier hashes.

Changed six paired bodies: `lightning-demand` and `hope-burden` restore Arata’s human targets, the distinction between Rumata’s lesser spoken reason and private land/serfdom argument, and his uneasy respect; `okana` clarifies the English attraction/information motive and completes the failed encounter → drunken return → confession/brine scene; `clearance-ritual` restores the bracelet/stamped-paper action that obtains Budakh; `final` explicitly recaps opening stakes rather than reopening them after the epilogue; `childhood-game` removes бумажным / paper. All **33 resulting RU/EN pairs** and nested **8/13/33** routes were read; stable IDs/counts, narrative presentation and all spoiler/progress code remain unchanged. No lesson, invented dialogue/motive, shooter identity, casualty count or accomplished escape was added.

Actual pass-2 primary reading and source limits are in the new sources.md addendum. It includes complete chapter 9, complete chapter 10, complete epilogue, complete Budakh dialogue and continuous local scenes needed for each correction; it is not a claim to reading every word of the whole novella or collating print/EN editions. Fresh official-site bytes match the checked private witness. Source sufficiency supports the particular retained events and arguments; no missing full-EPUB gate is imposed.

The maintained audit reports **69 passes / 0 warnings / 0 failures**. Fresh forced-offline browser matrix: **864 render instances** at 320/390/1024/1440, all modes/languages/themes; **80 saved-Deep paths**, compact header, Sources, fonts, vertical dense-screen scrolling, focus, keyboard and restart checks pass, with no remote HTTP/runtime exceptions. Physical iPhone/PWA and swipe gestures remain untested. HTML outside the embedded JSON is byte-identical to the pre-repair shell. Canonical/HTML parity is exact apart from generated mode timing data.

Full finding-by-finding implementation closure map: [repairs/hard-to-be-a-god-pass2.md](../repairs/hard-to-be-a-god-pass2.md). Exact paired before/after and personally read primary ranges: [hard-to-be-a-god-pass2-evidence.json](hard-to-be-a-god-pass2-evidence.json). Current four-file hashes are in `../ready/hard-to-be-a-god.json`. The independent review files remain untouched and their old verdict is not relabelled. Ready status requests an independent check of the new hashes; root integration and publication remain with the publisher.
