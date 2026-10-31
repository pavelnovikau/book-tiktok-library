# Have Space Suit—Will Travel — implementation handoff

2026-10-31. Assigned implementation worker only. **REBUILD / new-approved-title**, submitted as **ready-for-independent-check**, not an independent PASS.

## Assignment and starting state

The assigned work is Robert A. Heinlein’s **1958 novel**, not its graphic adaptation or another juvenile. The title was already approved in `BOOK_PLAN.md`; no new selection was made. `editorial-audit/2026-10-31/BRIEF.md` was read first, followed by `CONTRIBUTING.md`, the maintained `skills/book-tiktok/SKILL.md` and its content/data/HTML references.

There was **no existing assigned collector folder or root reader** when work started. Published pairs compared: **0**; prior collector pairs compared: **0**. There is consequently no honest old-screen defect table or before/after count to report. The external baseline was not modified. This is a new implementation under the corrected editorial brief, rather than a repair labelled as though it had been published.

Owned writes are restricted to `collector-output/have-space-suit-will-travel/`, this uniquely named report and its sibling evidence directory, and `editorial-audit/2026-10-31/ready/have-space-suit-will-travel.json`. Root readers, catalogue, index, release records, shared shell, installed skill and logs were left to their owners. No agents, Git/PR/deploy action, or external messages were used.

## Source acquisition and actual reading

Read-only, assigned-title metadata discovery covered **217 OPF records in 216 expanded Apple Books EPUB directories** and **49 PDF metadata records**, with **zero assigned-title candidates**. No unrelated filenames are exposed in the report or evidence. With no matching candidate there is no assigned OPF/spine/body extent to certify. This is not a blanket “no EPUB, no work” conclusion.

Lawful direct discovery found Baen’s **2005 electronic sample, ISBN 9781416505495**, with its edition notice and contents. It is actual prose from the original novel, not a recap. The contents comprise Tony Daniel’s introduction and **three** novel chapters. Selected substantial author passages were read in chapters 1–3: the Moon ambition, school/family, pharmacy contest, Ace and wrapper, postmark/prize, restoration, napkin, radio-fit problem and final call. Complete sample files were fetched for inspection, but neither continuous sample reading nor whole-novel reading is claimed. The introduction was excluded as a source of Heinlein events.

For the later story, the official Virginia Edition resource page links **Robert James, Ph.D., *Have Spacesuit, Will Travel Lesson Plans***. Its 26-page PDF is a substantial accountable chapter guide, keyed to a Del Rey / Ballantine paperback whose precise printing is unstated. Chapter summaries on **PDF pages 2–17** cover all **12 chapters** and were read; selected quiz cross-checks on pp.17–19 were also consulted. Its short quoted author passages help anchor the retained relationships and argument inside the hearing. This source is identified as a **guide**, not relabelled primary/full text. The later narrative is kept at the granularity its detailed action summaries and quotations support.

World Space Week’s English PDF returned 404 and Simon & Schuster returned 403; neither is claimed read as a final evidence source. A tempting shoe/fall detail seen in indexed World Space Week material was removed rather than supported by unavailable text. The graphic adaptation was explicitly excluded. No purchases, loans, credentials, subscription changes, access bypass, unofficial full-text hunting, or private copyrighted text in the repository were used. Retrieval status, sizes and hashes are in [source-access.json](have-space-suit-will-travel-sol-implementation.evidence/source-access.json).

**Evidence scope:** three selected author-text chapters plus an official-hosted detailed guide for the complete retained arc. **No complete novel obtained; no continuous whole-book reading; no certified Russian translation; no self-certification of whole-book fidelity.** There is no currently identified unsupported essential link in the particular compact sequence retained. A later full-primary check could refine detail or expose an omission; that limitation remains visible to the independent reviewer and reader.

## Content and resulting routes

`prose-first.md` holds a connected original RU/EN story written before screen assignment. `segment-prose.py` segments its **35 narrative paragraphs**, adds cover, spoiler warning and shared final, and derives the exact count assertions. No target was filled with moral commentary or artificial splits.

The delivered copy tells Kip’s actual adventure: an unaffordable Moon ticket becomes a soap competition; the disappointing prize becomes Oscar; restored radio brings the homing call; Kip is captured helping the fugitives. Peewee’s intelligence, doll, grammar and childlike vulnerability remain part of her relationship with Kip; her lunar abduction and the Mother Thing’s police-like role make the opening situation intelligible. The missing ship brain forces a walk; Mother Thing’s ruined vacuum equipment and Peewee’s tourist suit make that walk dangerous; air shortage drives the collapse and recapture. Pluto’s cold and the failed cell escape preserve the constraints rather than substituting a competence lesson.

**Essential: 17; Core: 25; Deep: 38**, including cover and final. Level additions: **17 + 8 + 13**. Before counts: **not applicable**. Essential and Core end at `no-way-out`, with the companions’ fate unresolved. Core adds actual school/pharmacy/suit/radio/Peewee/route/prison detail. Deep alone continues through the counterplot and beacon, mutual rescue, treatment, the proceedings and return. The final comedy remains a concrete incident from the novel, not a new moral.

Every resulting RU/EN pair was read: **38 unique pairs / 76 localized screen versions**, including framing; all three nested routes were read for continuity. Repeated overlap is not counted as additional distinct content review. The effective embedded HTML screens, sources and method note match the authoring JSON exactly. [content-map.json](have-space-suit-will-travel-sol-implementation.evidence/content-map.json) records stable IDs and source locations; the canonical [sources.md](../../../collector-output/have-space-suit-will-travel/sources.md) gives a substantive, screen-by-screen evidence/causality map.

## Specific editorial decisions and corrections

These are implementation findings and final controls, not fabricated defects in an earlier published version.

| Screen ID | Issue avoided / correction made | Supporting location |
| --- | --- | --- |
| `beaten-by-a-postmark` | Winning words do not win Kip the first prize; duplicate-entry priority matters. | Baen ch.3, opening prize announcement. |
| `pressure-and-a-napkin` | Preserve real comic event and suit constraints; omit gas-mixture/pressure/drug instructions. Do not present speculative suit design as modern safety advice. | Baen ch.3, restoration and dinner passages. |
| `radio-in-the-helmet` | Kip’s homemade radio works but does not fit; he buys a finished one. Do not grant him a perfect invented engineering triumph. | Baen ch.3, radio passages. |
| `peewee-and-her-doll` | Retain mistaken rescue, Moon abduction and police-like Mother Thing role; omit numerical age because the guide’s rounded ages conflict. | James PDF pp.6–7, ch.4. |
| `lunar-sleep` | Removed shoes/fall specificity whose direct witness was unavailable; kept bouncing, exhaustion and noticed tears. | James PDF p.8, ch.5. |
| `a-ship-without-a-brain` | Door interference and missing control brain explain why escape becomes a walk. Peewee’s refusal to leave the Mother Thing is a concrete action. | James PDF pp.8–9, ch.5. |
| `forty-miles`, `the-station-ahead` | Tourist equipment and incompatible bottles cause air crises; rescue reply does not mean they safely entered the station. | James PDF pp.9–10, chs.5–6. |
| `the-open-cell` | Attack is by **a** wormface; do not assert it is the original named leader. Mutual rescue remains central. | James PDF pp.11–12, ch.8. |
| `the-mothers-device` | Do not claim Mother Thing only went outside after the explosion. Preserve lab bargain → covert equipment → outside signal sequence. | James PDF p.12, ch.8. |
| `the-cold-outside` | Frozen appearance does not establish actual death; failure of line/air hoses is narrative, not instructions. | James PDF p.12, ch.8. |
| `a-room-near-vega` | Reassurance and request not to withhold knowledge replace an overly broad invented statement of both characters’ wishes. | James PDF pp.12–13, ch.9. |
| `kip-before-the-judges` | Preserve the conflicting arguments, tribunal’s security purpose and rejected rescue testimony, rather than making a general moral about humanity. | James PDF pp.14–15, ch.11. |
| `the-decision` | Kip’s threat is desperate speech, not proven ability to create a star. His request to return home precedes the favourable verdict. | James PDF p.15, ch.11. |
| `a-sheet-of-mathematics` | Retain scientific gifts, public sharing and MIT, without asserting an unverified catalogue of technologies solved by the page. | James PDF p.16, ch.12. |
| `cover`, `final` | Shared framing, source notes, contents and resume must not disclose decisive outcomes. | Book-specific spoiler policy and resulting reader checks. |

## Build, behaviour and mobile/offline verification

The maintained builder and deterministic audit were used. `build-local.mjs` adds only this collector’s book-specific consent guards, protected generic Deep resume, masked chapter titles and prose cover; it invokes the maintained builder rather than copying a reader. No shared template/header or unmerged font code was edited or copied. Source maps remain embedded and available through the Sources dialog; per-screen academic chrome is absent in narrative mode.

The maintained structural audit completed **69 checks with zero failures**. Its one `ending-warning` source-coverage warning is expected for a navigation screen making no book claim. This result establishes structure, not fidelity.

Chrome local-file QA ran offline at **320×568, 390×844, 1024×768 and 1440×900**, all depths, both languages and both themes. Each complete matrix compares every displayed body/title and counter, header icon row, horizontal bounds and last-paragraph reachability. The four matrices cover **1,280 screen renders**. Additional phases verify dialogs, position preservation, hidden-screen depth changes, explicit Deep consent/cancel, masked contents, safe saved resume, fresh consent after reload, focus/tap/key/swipe/vertical gesture behaviour, final restart, desktop rail, and reachable cover controls. iPhone browser/standalone emulation checks the real engine 47px safe-area inset and install-guide behaviour. These are emulation results, not physical-device claims.

All completed phases show zero unexplained application exceptions, zero remote page-runtime requests and deleted profiles. Each Chrome invocation ran under `timeout 30` with its own `mktemp -d` profile and owned process-tree cleanup; no server was started or left running. Representative stored phone/desktop, source/consent and safe-area screenshots were inspected. The embedded maintained fonts loaded; Cyrillic font coverage and PR29 settings/font work are not separately certified by this implementation.

Canonical [QA.md](../../../collector-output/have-space-suit-will-travel/QA.md) contains exact reading totals, estimates, density, commands, phase results and limits. The ready manifest binds the four canonical deliverables and evidence to SHA-256 hashes so the independent reviewer and publisher can check exactly this artifact.

## Unresolved work

Independent editorial review is still required, particularly scrutiny of the guide-dependent later arc. There is no implementation-issued independent PASS. Physical iPhone/PWA hardware, production integration and external publication have not been verified or performed here. The publisher owns catalogue/root integration and any subsequent delivery. No unsupported retained essential causal link has been identified; absence of a complete-primary witness remains an evidence limitation, not silently upgraded certainty.
