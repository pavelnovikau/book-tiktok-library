Current root personal acceptance2026-11-01:49/93/129screens;10644RU/11929EN body words; UI Deep63/58minutes. Exact accepted version and source/reading/QA limits: root-review/personal-review.md and personal-review.json. Historical implementation statements below are preserved; they do not describe the final hashes or grant broader source coverage.

---

# Will Storr — Selfie / Селфи

Status: **ready-for-root-personal-check**. `rootPersonalAcceptance=false`; `publicationAllowed=false`.

Implementation is complete inside this new `selfie/` directory. It was absent at the initial ownership check, so no other implementation was overwritten. Previous collector/ready/reviews, other books, root readers, catalogue, installed code, logs and global status were not edited. There were no subagents, Git operations, PR, deployment or external messages.

Open [selfie.html](selfie.html) directly. It is standalone, bilingual and offline, with RU/dark/Essential defaults, current Settings, Geist Sans/Serif and the honest Source Serif 4 Russian fallback. Its exact cumulative routes are 48/92/128 screens, including cover and final. Progress is fresh and book-local under `book-tiktok.selfie.depth-v2.`; a saved deeper Continue explicitly names its depth before it can raise it. No fiction spoiler modal applies.

## Review corpus

Read the sustained [Russian exposition](draft.ru.md), then its [English rendering](draft.en.md). Both were drafted before segmentation; historical and final hashes are separated in `prose-first.json`.

Then personally read each exact nested sequence, not only the Deep text:

| Route | Russian | English |
|---|---|---|
| Essential | [essential.ru.md](essential.ru.md) | [essential.en.md](essential.en.md) |
| Core | [core.ru.md](core.ru.md) | [core.en.md](core.en.md) |
| Deep | [deep.ru.md](deep.ru.md) | [deep.en.md](deep.en.md) |

Read [coverage-map.md](coverage-map.md) in full, including its whole-spine omissions table. Its JSON counterpart supplies exact checked paragraph locators for 64 developed units. `story-data.json`, route files and the embedded HTML have exact paragraph/data parity. Route copies include stable screen IDs and levels for checking sequence continuity.

The body has 10,764 RU /12,077 EN words: 59.8 /54.895454… minutes at 180/220 wpm. UI estimates include headings/cover framing and display 64 minutes RU /59 min EN for Deep. Essential body times are 22.65 /20.763636… minutes; Core 43.5 /39.931818… . Full exact inputs, fractions and excluded disclosures are in [metrics.json](metrics.json).

RU is 10.3% below the 12k planning orientation. It develops the principal reporting arcs rather than naming them, but remains a condensation. Extended biography, repeated statistics, incidental scandals, secondary campus incidents and lurid detail were deliberately compressed or omitted; their actual source ranges are named in the map. Root must judge whether any restoration is needed. A screen count or green QA result is insufficient evidence of editorial depth.

## Source boundary

The owned primary stays read-only outside this directory:

`/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/selfie-edition.json`

SHA256: `ec92b521a877c1385bc3d0f3a81c834ce5574f9f51da6852b0efe6f936d11766`.

All 1,159 main paragraphs (`OPS/ch1-3.xhtml`–`ch1-21.xhtml`, including continuations) were displayed/read continuously, plus complete methodology, acknowledgements and actual metadata. The complete extraction reports 97,266 words including endmatter; the main spine reports 92,278. Endnotes were selective. [reading-ledger.json](reading-ledger.json) records 30 actual bounded display acknowledgements, exact ranges and paragraph hashes, including the explicitly repaired first-chunk clipping. [route-reading-ledger.json](route-reading-ledger.json) records actual final route reading and all final revision rereads.

Metadata supports the Russian title, original copyright 2017 and Individuum Print 2019. The supplied metadata has no translator credit; previous-ledger translator/ISBN claims were not silently promoted to inspected facts. The English here is an original rendering of the original Russian exposition, without full official-English collation. The source extraction supplies no images, so original illustrations/diagrams could not be checked. No private primary snapshot, raw chapter or extraction was copied here.

Storr’s own methodological limits are retained: secondary literature and interviews, specialist manuscript review in whole or part, changed names, edited/combined quotations, acknowledged bias and disputes within social psychology. Journalism, historical reconstruction and experimental claims are distinguished. No current scientific-validity certificate is implied. [sources.md](sources.md), `source-identity.json` and `source-method.json` hold the detailed record.

## Root's required primary checks

Root must personally open selected actual primary passages, alongside the complete final RU/EN/routes/map. The following are substantive check locations, not replacement outlines or pasted extracts. Locators are inclusive 1-based positions in each `paragraphs` array, not print pages.

| Actual primary location | Check against the final exposition |
|---|---|
| `OPS/ch1-3.xhtml P024–043, P045–059` | O’Connor's multifactor/entrapment account; Flett's explicit lack of evidence for an increase; Meredith's comparison loop. |
| `OPS/ch1-4.xhtml P028–054, P069–112`; `ch1-5.xhtml P008–016` | Pridmore's gang reputation, religious testimony and persistent anger; avoid total-transformation or supernatural-proof claims. |
| `OPS/ch1-6.xhtml P020–032, P043–055`; `ch1-7.xhtml P001–030` | Cultural/historical inference, group versus individual limits, context and competing East/West claims. |
| `OPS/ch1-8.xhtml P034–100`; `ch1-9.xhtml P001–026` | Father Martin's actual project and the bad-self historical bridge, without invented dialogue or diagnosis. |
| `OPS/ch1-10.xhtml P026–056`; `ch1-11.xhtml P005–020, P078–123`; `ch1-12.xhtml P001–022` | Rogers, Esalen, the author's ambivalent participation, authentic-core challenge and social-pain limits. |
| `OPS/ch1-14.xhtml P045–078`; `ch1-15.xhtml P001–006, P025–044` | Actual tapes/institutional response; Baumeister's correction from high esteem to narcissism; unresolved generation dispute. |
| `OPS/ch1-17.xhtml P029–076`; `ch1-18.xhtml P044–086` | Jeremy's reported labour, Faber's aspirations and Kate's competing argument; avoid treating plans as delivered capability. |
| `OPS/ch1-18.xhtml P089–117`; `ch1-19.xhtml P001–038` | CJ as an extreme, possibly performed account, not a clinical diagnosis or a representative generation. |
| `OPS/ch1-20.xhtml P009–035`; `OPS/ch2.xhtml P223` | Heinz reporting sources, Hutchinson's real objection and support, sister's correction, multiple pressures rather than a single blame story. |
| `OPS/ch1-20.xhtml P039–057`; `ch1-21.xhtml P002–028, P030–039` | Stable traits without immutability, the author's late self-correction, limits plus responsibility, attainable projects and actual affectionate fogbound ending. |
| `OPS/ch1-23.xhtml P001–007`; `ch1-2.xhtml P014` | The author's full methodological statement and group-average warning. |

All table shorthand `ch1-*.xhtml` refers to the same `OPS/` directory. The original source remains at its private path. `read-primary.py <chunk-number>` can redisplay the bounded source-reading plan locally without writing primary text into this candidate; use the map for exact selective locations.

## QA and final gate

[QA.md](QA.md) describes final tests and their limits. The final deterministic audit passed 69 checks, zero warnings/failures. Five browser runs passed 10,720 rendered visits with both languages, themes and fonts. They include genuine cold first Serif at nonzero scroll, native Settings arrow keys, actual reload/lower-depth/deeper-resume, a real legacy-ID fixture, native taps/selection, emulated touch, overflow/last-line checks and owned Chrome cleanup. Screenshots and hash-bound reports are under `qa/`.

No hardware Safari/iPhone/PWA test, independent review, root personal acceptance or full official-English comparison is claimed. The Home link retains `./`; catalogue integration and publication were deliberately left untouched under the assigned scope.

[ready.json](ready.json) binds the final deliverables and evidence by SHA256. Its readiness means ready for root's personal check only. Root must not publish until personally reading this entire review corpus and selected actual primary passages and recording acceptance through its own authorized workflow. Nothing in this candidate sets that acceptance.
