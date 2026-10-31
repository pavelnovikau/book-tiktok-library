# Seeing Like a State — implementation handoff

Verdict: **BUILD, approved queued work**. Status: **ready-for-independent-check**, subject to the exact hashes in the readiness manifest. No independent PASS, publication approval or whole-book fidelity certification is issued by this implementing worker.

Canonical package: `collector-output/seeing-like-a-state/`. Target: James C. Scott, *Seeing Like a State: How Certain Schemes to Improve the Human Condition Have Failed*, Yale University Press, original 1998 English work. Russian shelf label: «Благими намерениями государства»; no official Russian translation edition was consulted. Yale's linked paperback listing is dated 1999 and is distinguished from the original work's date; the 2020 reissue was not silently substituted.

## Starting state and reading scope

At task start no collector package or published root reader for this slug existed. **0 old pairs**, **31 new RU/EN authoring pairs** read, **31 embedded pairs** compared/traversed. There is no old-screen defect table to invent. The 20-book extension already approved this work; no new title or purchase/loan was proposed.

The read-only, title/author-scoped Apple Books filename/EPUB-metadata search found no matching package among 216 inspected OPF records. It inspected expanded EPUB directories as well as archives, exposed no unrelated filenames and changed no library files. No candidate means there was no claimed OPF/spine/full-body verification. Absence of an owned EPUB was not used as a blanket rejection.

Substantial actual 1998-book passages were found in public university course excerpts: chapter 1 (forestry/land-tenure selections), chapter 4 (planning/Brasília/Jacobs selections), and chapter 9 (pp. 309–341, OCR-read). Scott author excerpts cover high modernism; Yale's official four-condition description is cross-checked against a direct quotation of Scott's Introduction pp. 4–5 on p. 297 of Zhou's institutional article. That is indirect access to the Introduction passage, not reading the complete Introduction. `sources.md` gives exact consulted and omitted spans and maps every stable screen ID to a passage.

The accessible text supports the retained chain: selective legibility becomes transformation of the world; initial gains can conceal excluded interdependencies; destructive state projects combine four conditions; actual city and farming cases expose reliance on informal practice; métis is learned, situated and adaptable; it is neither an innocent local monopoly nor an argument to abandon science/state capacity. No essential missing link in this particular condensed arc was identified in the authoring self-check. Independent source-sufficiency review is still needed.

No private/full copyrighted text, source PDF, scan or raw OCR transcript was saved into this repository. No unofficial full-book retrieval, credential/subscription change, purchase, loan, or access bypass occurred. The later Cato essay and Theory Talk were discovery-only. No 2009/2017 book example or late lecture was imported as 1998 material.

## What was built

Connected original RU and EN prose was written first in `prose-ru.md` / `prose-en.md`; only then was it segmented by `authoring.py`. The final corpus has **31 paired screens**, nested **17 Essential / 25 Core / 31 Deep** including cover and final, with `contentMode: explanatory` and RU/dark/Essential defaults. These are derived counts, with no earlier quota to preserve. Each route reaches the author's qualification rather than an added motivational/management ending.

Essential carries forestry including initial success, the dangerous conjunction, Brasília's planned/lived contrast, the bounded agricultural comparison, informal order, métis, the complete Mat Isa case and the non-blanket critique. Core adds excluded forest uses, cadastral legibility, political constraints, Le Corbusier's real aspirations, Jacobs, work-to-rule, the pilot and unequal access. Deep adds restoration ecology, perspectival legibility, the deli keys, contract poultry, community transmission and Meiji scientific collaboration. Added depth supplies book content, not filler.

Route self-reading caught a defect in the initial 15/25/31 segmentation: Essential's later qualification named Mat Isa before introducing him, and the forestry success was too implicit. Promoted the existing `mat-isa` and `first-rotation` paragraphs to level 1. No prose or screens were added to meet a count; final counts are 17/25/31.

Every non-cover screen is `claimType: book`, with shared IDs/levels/source references across RU and EN. Source roles are not used as quotas. `sources.md` preserves detailed evidence; the reader keeps Sources in a dialog without academic source footers on reading screens. A typographic cover removes the generic seven-node “model” placeholder. Current maintained builder/header are used via the local wrapper. No unmerged PR29 settings behavior was copied or implemented; publisher applies the latest shell when integrating.

## Specific findings resolved before readiness

| Screen ID | Finding / draft risk | Resolution and support |
|---|---|---|
| `brasilia` | One source's editorial preface loosely attributes the city to Le Corbusier. | Corrected to Costa's plan/Niemeyer's key buildings and doctrinal influence; actual book ch. 4, pp. 118, 130 explicitly distinguishes authorship. |
| `four-elements` | A truncated account could treat legibility alone as fatal or omit the authoritarian qualification. | All four conditions and their conjunction are explicit in both languages; Scott Introduction pp. 4–5 as directly quoted in Zhou p. 297, Yale description, ch. 9 p. 340. |
| `first-rotation`, `second-rotation` | A simple failure story would erase genuine initial gains or imply immediate damage. | Initial profitability and delayed ecological consequences retained; ch. 1 pp. 18–22. Historical causes remain Scott's explanation. |
| `fields-that-survived` | Detailed reconstruction of unread agrarian chapters would overstate evidence. | Retained only the actual ch. 9 p. 310 recap, without numbers, named villages, full resettlement chronology or invented local causality. |
| `mat-isa`, `metis-keeps-changing` | An invented village tale, a hypothetical pesticide becoming an event, or Essential naming the person before his case. | Actual mango/ant/nipah procedure and outcome from pp. 333–334 now appear in every route; pesticide remains Scott's supposition on p. 335. |
| `metis` | Draft “neither replaces the other” could overstate a universal reciprocal claim. | Narrowed to the supported claim that general rules alone do not supply situated skill; pp. 313–319. |
| `public-goods` | English “depend on” could be stronger than the Russian and source wording. | Changed to “owe much to”; explicitly retains citizenship, public health, education, equality before law and the non-blanket critique; pp. 339–341. |
| `simple-for-whom`, `unequal-access` | Local knowledge might be romanticized as automatically just/free. | Retained customary inequalities and knowledge monopolies; ch. 1 pp. 34–36, ch. 9 pp. 334–335. |

These are implementation/source findings, not fabricated defects in a nonexistent older delivery. No invented anecdote, dialogue, exercise, new village name, modern analogy, generic agency lesson or definitive-author-intent claim was added.

## Validation and handoff limits

Maintained structural audit: **69 checks, 0 failures, 0 warnings**. Effective embedded corpus matches JSON for copy, source maps, defaults, method and derived counts. Browser checks traverse all routes at 320×568, 390×844, 1024×768 and 1440×900 in RU/EN and light/dark: **1,168 rendered screen visits** across the final four matrices. No horizontal overflow, unexpected runtime/console error or external HTTP runtime request. Embedded offline fonts load.

Phone/desktop interaction checks cover dialogs, navigation, focus, gesture discrimination, saved Continue, Start over and final restart. Emulated iPhone coverage uses engine insets 47px top/34px bottom and verifies the six-icon header, reading scroll, safe Next, focus restoration, localized installation guidance and standalone hiding. No physical iPhone/Safari/PWA test is claimed. Capture timing and an invalid initial safe-area probe were corrected in the test harness; no shared-shell fix was inferred from them.

Each Chrome used `timeout 30`, an individual `mktemp` profile and owned-tree cleanup; no server was started and final reports verify no owned browser/profile leftovers. `QA.md`, the `qa/` JSON reports and screenshots record the local evidence. These checks establish technical behavior and authoring consistency, **not independent editorial fidelity**.

Open limits: independent review of every pair and source sufficiency; OCR rather than a collated full edition; selected chapter coverage (not exhaustive chapters 5–8/10); no continuous full-book reading; no official-translation certification; historical/ecological claims not independently replicated; physical-device and production validation outstanding. Collector package is ready for an independent check of the retained argument, not preapproved for publication.

Only the assigned collector folder and this uniquely named implementation report/readiness manifest were created. Root/catalogue/index/shared shell/installed skills/logs were not edited; no Git, PR, deploy, external message or subagent actions occurred.
