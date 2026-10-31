# The Body Keeps the Score — detailed editorial repair

2026-10-31. Verdict: **REBUILD completed, ready for independent check**. Evidence scope is the main argument and selected supported cases, not every sentence of the full edition.

## Actual reading and delivery comparison

Read **144 old RU/EN pairs** at all levels. Old collector JSON, its HTML and root reader's effective embedded corpus had **0 copy divergences**. This is 144 distinct pairs read in three matching representations, not 432 different pairs. Root focus/header/install additions do not change these texts. Read and substantively self-checked **41 new pairs**, and assessed Essential/Core/Deep as argument sequences.

Owned complete Russian EPUB, read-only: «Тело помнит все. Какую роль психологическая травма играет в жизни человека и какие техники помогают ее преодолеть». Spine includes prologue, all five parts, all twenty chapters, epilogue and end matter. Actual `content0.html` identifies translator **Иван Чорный**, translation copyright **2019**, Eksmo design copyright **2020**. The OPF's 2014 date is not a verified Russian printing date. No new ISBN/date invented.

Consulted argument-bearing passages across chapters 1–20, prologue/epilogue and selected clinical cases; targeted rereading covered each specific case/turn retained in the condensation. **Not continuous full-edition reading; not verification of all clinical histories, notes or an English edition.** Private extraction is outside the repo at `group-9-private/the-body-keeps-the-score/`. Cases remain accounts by van der Kolk, not independently verified patient files. The public `sources.md` contains a chapter/screen map.

Current qualifications checked through [VA psychotherapy overview](https://www.ptsd.va.gov/professional/treat/txessentials/overview_therapy.asp), [Grossman's abstract](https://pubmed.ncbi.nlm.nih.gov/37230290/) and [Otgaar et al.'s accessible review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6826861/). SAGE's original review route timed out; lawful PMC material was available. These qualifications retain attribution and do not replace the author's position.

## Specific old-screen findings

| Stable old ID(s) | Problematic wording / effect | Correction | Primary-text location or support |
|---|---|---|---|
| `cover`, `reading-contract` | Opens with “границы медицинских доказательств” and a three-voice tutorial | Keep the non-graphic/skip/stop promise; put access detail in Sources and start the book with Tom. | Ch. 1, `content1.html`; prologue. |
| `event-versus-aftermath`, `tom-loyalty` | General thesis is Essential; Tom's concrete refusal is Core | Restore the actual encounter and refusal to the opening Essential sequence. Loyalty is his expressed explanation, not a guessed motive. | `content1.html`, return visit and refusal of medication. |
| `pharmacology-history` | General “критикует превращение химического объяснения…” | Restore the hospital-pool/lab change that concretely carries the author's institutional criticism. Preserve his initial enthusiasm and avoid claiming drugs are useless. | Ch. 2, `content10–11.html`. |
| `case-not-effect`, `scan-boundary`, `triune-caveat` | Repeated evidence warnings displace the clinical/causal sequence | Remove standalone tutorials and unsupported literal brain architecture. Keep scan limitations attached to the actual reminder account. | Chs. 3–4, `content11–19.html`. |
| `stan-ute` | “Истории … используются для сопоставления” abstracts the experience | Say which reported response differs: Stan mobilizes, Ute disconnects. Do not add traumatic graphic detail or diagnostic rules. | Ch. 4, `content17–18.html`, particularly depersonalization passage. |
| `ownership`, `interoception`, `alexithymia`, `body-map`, `signal-uncertainty` | Many adjacent fragments repeatedly end in diagnostic cautions | Consolidate the author's sense-of-self argument into `ownership`, retaining the limits in scope/medical note. | Ch. 6, `content24–29.html`. |
| `porges-model`, `polyvagal-dispute` | Author model and later critique are separated by intervening screens | Keep the actual theory and the explicit contemporary dispute together in Deep. No silent substitution of today's science for his account. | Ch. 5, `content19–24.html`; Grossman abstract above. |
| `marilyn-context` | “История … связывает трудности…” reduces a person to a general caution | Restore the work/tennis/intimacy contrast with confirmed occupation. The new authoring draft was itself checked and corrected to **operating-room nurse** before readiness. No old-reader factual error about this occupation is alleged. | Ch. 8, `content37.html`, opening. |
| `felitti-puzzle` | “неожиданная проблема” never says what the puzzle was | Restore weight loss followed by regained weight/protective meaning, without giving dieting instructions or diagnosing abuse from obesity. | Ch. 9, `content43–44.html`. |
| `ace-not-destiny`, `cptsd-update` | Separate editorial/modern-classification screens occupy Essential | Keep observational scope beside ACE; identify developmental-trauma disorder as the author's proposal. Do not rename it ICD-11 CPTSD. | Chs. 9–10, `content43–50.html`. |
| `memory-not-video` | Existing title suggests an innocuous general memory lesson while body makes a stronger author claim | Preserve the actual strong persistence position with a better title and a contiguous accuracy/suggestion qualification. Do not dilute author disagreement into consensus. | Ch. 11, `content52.html`; Ch. 12, `content57–59.html`; Otgaar review. |
| `support-verification`, `forensic-boundary`, `memory-title-limit`, `story-ownership`, `listening-without-leading` | The digest repeatedly teaches its own principles | Remove those standalone lessons; keep necessary limits around the precise memory claim and preserve the positive role of language. | Chs. 11–14; these old screens identify themselves as synthesis. |
| `first-line-therapy`, `conversation-caricature` | Modern corrective blocks can replace the author's actual critique | State his skepticism first, then explicitly identify the VA's contemporary adult evidence. Keep disagreement legible. | Ch. 13, `content65–68.html`; VA overview. |
| `emdr-trial`, `rem-hypothesis` | Evidence notes spread across an obligatory ten-slot block | Condense the author's interest, comparison and mechanism hypothesis into related screens; do not make sleep analogy an established mechanism. | Ch. 15, `content74–79.html`. |
| `yoga-choice`, `yoga-not-athletics`, `yoga-review-difference`, `yoga-later-review` | Abstract choice statements and review statistics outweigh Annie's actual experience | Return the bodily-learning argument and the first-class adverse response/later change. Do not turn it into an instruction to endure harm or a universal yoga claim. | Ch. 16, `content81–83.html`. |
| `compassion-not-proof`, `imagined-support`, `method-transfer`, `alpha-theta`, `technology-cost`, `measurement-outcome` | The ending detours through the digest's ethics, inference and technology lessons | Retain book-specific IFS/structures/neurofeedback explanations; one distinct evidence-boundary screen suffices for unequal support. | Chs. 17–19; `content83–98.html`; VA overview. |
| `care-not-performance`, `current-guidance`, `integrated-reading`, `final` | The ending becomes an external verdict on the book | Finish with actual theatre programmes and the author's collective-prevention appeal, then return to the opening question of agency. | Ch. 20 and epilogue, `content99–104.html`. |

No material bilingual contradiction was found among the 144 old pairs. The primary problem was fragmentation, genericization of cases and replacement by repeated digest-writer commentary. Several factual qualifications were valuable and remain beside the relevant claims.

## Delivered changes

All prose reauthored as an explanatory condensation; **21/33/41** replaces **36/90/144**. The five-part argument remains recognizable: veterans' experience → alarm/body → childhood relationships → memory → several routes to recovery and prevention. Restored concrete source-supported details without invented dialogue or motives. No graphic retellings, home trauma-processing exercises, doses or diagnostic checklist.

`contentMode: explanatory`; fresh RU/dark/Essential. Preserved user-provided cover and permission to skip/stop. There was no separate bespoke consent gate in the old reader. Sources condensed to four stable-ID entries; the old statistic-heavy comparison atlas is not carried forward. All four canonical collector files updated. External baseline retains originals; root reader/catalogue/shared shell not touched.

## Verification and remaining work

Final build passed; maintained HTML audit: **69 passes, zero warnings/failures**. Final Chrome check rendered every new pair in RU/EN and dark/light at 320×568 and 1440×900; exact rendered text, no horizontal overflow, body Next visibility, mode endings, Sources, default settings and Home passed. Zero runtime exceptions or remote runtime requests. Mobile/desktop screenshots inspected. Private QA directory: `group-9-private/the-body-keeps-the-score-browser/`. Unique Chrome profile and 30-second process bound; owned group/profile cleaned in finally; no server.

This is ready for independent source/editorial review, not self-certified publication or whole-edition fidelity. Selected primary material is accessible; no access block remains for these retained passages. Full clinical-history verification, exhaustive modern clinical review and full English-edition collation were not performed. Real-device PWA/header behavior remains publisher work.

Publisher must update the live reader/catalogue only after approval, recompute reading times/counts/description, and account for removed/reworked saved IDs. Source evidence and clear author disagreement should survive integration. No Git, PR, deploy or external messages performed.
