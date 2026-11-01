# Implementation QA — Children of Captain Grant, depth-v2

Status: **ready-for-root-personal-check**. `rootPersonalAcceptance=false`; `publicationAllowed=false`. These are implementation checks, not root's literary, source or publication acceptance. All work is confined to this new book directory; the old collector, root reader, catalogue, global ledgers, shared installed skill, other candidates and publication files were not edited. No subagents, Git, PR, deployment or content server were used.

## Result and volume

A complete original Russian adventure was written first; matching English followed; segmentation came after both connected drafts. Each has 30 connected episodes and 113 narrative paragraphs. Screens preserve those actual paragraphs, rather than expanding the old analytical headings. The three journeys occupy these narrative word counts:

| Horne part | Draft paragraphs | RU narrative words | EN narrative words |
|---|---:|---:|---:|
| I — formation, Chile, Thalcave, Pampas, flood | 1–43 | 4,711 | 5,728 |
| II — islands, sea danger, Australia and betrayal | 44–75 | 3,556 | 4,269 |
| III — New Zealand, order, island and return | 76–113 | 4,157 | 4,939 |
| Complete story | 1–113 | **12,424** | **14,936** |

The planning range was roughly 12–18k RU narrative words. Final size follows developed scenes and real omissions, not a word or screen quota. See the 66-chapter retention/omission table and 113-scene map. The omission list includes travel/scientific catalogues, historical digressions, the shirt tale, some graphic detail and several secondary scenes. No full French collation is claimed.

| Route / language | Screens | Narrative paragraphs | Narrative words | Framing body words | All heading words | UI estimate |
|---|---:|---:|---:|---:|---:|---:|
| Essential RU | 26 | 24 | 2,648 | 55 | 181 | 16 minutes |
| Essential EN | 26 | 24 | 3,242 | 66 | 249 | 16 minutes |
| Core RU | 69 | 67 | 7,370 | 55 | 460 | 43 minutes |
| Core EN | 69 | 67 | 8,890 | 66 | 597 | 42 minutes |
| Deep RU | 116 | 113 | 12,424 | 72 | 749 | 72 minutes |
| Deep EN | 116 | 113 | 14,936 | 87 | 970 | 71 minutes |

Word tokens follow the maintained builder's Unicode rule; hyphenated tokens count once. Narrative excludes headings and all framing. Heading totals include repeated section kickers, screen titles and cover subtitle. UI timing includes body, titles and subtitle, but excludes section kickers, Sources and controls. At the stated 180 RU / 220 EN words per minute, Deep narrative alone is 69.02 / 67.89 minutes; framing is 0.40 / 0.40 and headings 4.16 / 4.41 minutes. These are estimates, not measured reader speeds. `metrics.json` gives the exact breakdown for every route, the unique draft heading counts, time calculations and input hashes. The deterministic auditor's title/body total excludes the cover subtitle, explaining its four RU / six EN fewer words.

Essential ends after the condor rescue, Portuguese mistake and meeting Thalcave/Thaouka. Core continues through the flood, ocean and Australia, ending at the Snowy camp before exposure. They are continuous, explicitly unfinished beginnings. Deep preserves betrayal, the unsuccessful escape, captivity, rescues, the order's real effect, Ayrton's limited knowledge, the night voice, Grant's survival, the message solution, marooning, marriages and Paganel's final comic secret. Short modes reveal none of those decisive later answers.

## Reading and fidelity boundary

The whole frozen English witness was actually read in 34 bounded, untruncated contiguous outputs, including introduction, all 66 chapters and footer. `witness-reading-ledger.json` records exact original-byte range hashes, acknowledgements and incident notes. Rehashing verifies all 20,151 physical lines / 960,921 bytes without copying primary text into this directory. `witness-chapter-ranges.json` identifies all 26 + 19 + 21 chapters. Selective French checks cover four pages only; `sources.md` distinguishes their actual read ranges and chapter numbering from Horne's. Downloads and indexes were not counted as reading.

The prose retains people, decisions, comic mishaps, attraction, uncertain readings and consequences. It supplies no exercises, management principles or moral-summary ending. The major's later account of his night overhearing is placed in chronological scene order; its composite source locator is explicit. No private Helena/Ayrton dialogue or motive for Toline's departure has been supplied. No later Ayrton sequel outcome is imported.

Specific rails: Glenarvan's corrective Richardson geography is distinct from Toline's Bible prize; latitude is 37°11′, not seconds; longitude remains unknown; a reconstructed message date never becomes the wreck date. Island geography stays fictional. Colonial ambitions and claims remain situated in the characters' story; old zoological, dietary and geological episodes are not modern advice. The narrative is a condensation of this historical English witness, not an assertion that every scene of the 70-chapter French original was collated or retained.

## Structural and offline browser checks

Maintained `audit_story_html.mjs`: **69 passes, zero warnings, zero failures** on the final HTML. `verify.mjs`: **57 substantive checks passed**, including exact paragraph text equality between both connected drafts, authoring JSON and embedded HTML; framing/title parity; valid ranges and rehashed complete witness; all 66 chapters mapped; exact nested route counts; old progress isolation. Installed shared builder/settings/template hashes still match the build record. No alien pilot narrative markers were found.

Chrome 155.0.8059.86, Node v26.5.0, macOS arm64. Loaded directly through `file://` with network offline; no server. Four viewport matrices:

- 320×568, 390×844, 1024×768 and 1440×900.
- At each: RU/EN × dark/light × sans/serif × all three modes, every reachable screen: **1,688 render states per width, 6,752 total**.
- Each state checks route IDs/order, actual rendered paragraph arrays against JSON, title, horizontal bounds, scroll tail, active desktop rail item, hidden per-scene provenance and depth-filtered Sources map.
- Both lower depths check that every level-3 title is absent from contents and Sources. A dense paragraph's final character is geometrically visible after scrolling to its end at every width.
- Platform font inspection of actual paragraph glyphs confirms embedded Geist sans in both languages, Source Serif 4 for Russian serif and Geist Serif for English serif. Settings accurately names the Cyrillic serif fallback. Dark/light and font changes preserve story position and scroll.
- One compact accessible icon row; desktop rail at the intended breakpoint; Settings and Sources open and close; keyboard Escape works. Screenshots inspected: narrow cover and dense English tail, and the desktop Russian serif condor scene. Screenshots are supporting samples, not a substitute for all-state checks.
- All six final browser reports record zero runtime exceptions and zero HTTP(S) requests.

Every Chrome invocation uses `/usr/bin/timeout 30`, its own `mkdtemp` profile and detached owned process group. `finally` kills that group and removes the profile; final reports verify the process group no longer exists and the profile is absent. A subsequent process-table check found no owned `grant-depth-v2-` Chrome process. No existing browser instance was terminated.

## Consent, navigation and persistence

Fresh namespace: `book-tiktok.children-of-captain-grant.depth-v2.` Shared theme/font preferences persist; old collector progress cannot silently reopen rewritten scenes. Deep permission is a volatile variable, never a stored approval.

- All **188** saved late-ID combinations: 47 level-3 IDs × two languages × two lower modes. Continue labels stay neutral, no ending title appears, dialog cancellation preserves the lower view, confirmation reaches the requested scene in Deep.
- Four real downgrade cases, four real file reload cases, a saved Deep mode, BFCache/pageshow emulation, explicit final-screen entry, every mode picker, and positional navigation are guarded. Lowering depth revokes approval. Reload cannot restore approval; saved Deep mode resets before a spoiler rail is rendered.
- Default dialog focus is Cancel. Escape cancels. An inline warning precedes paragraph 68; direct late saved entries require the same explicit dialog.
- Keyboard paging, reader focus mode, actual CDP pointer tap/swipe, synthetic pointer regression, vertical-gesture isolation, final restart and invalid saved IDs work. Focus hides header/rail/previous while retaining Next.
- Shared theme/font persistence, ignored old progress keys and denied-storage reading/Settings/session consent are checked. No consent key is persisted.
- iPhone user-agent and standalone-property emulation verify the bilingual Home Screen guide and compact row. **No physical iPhone, native Safari, installed PWA or native touch certification is claimed.**

One initial native `Input.dispatchTouchEvent` harness attempt timed out; its failure report is retained as `qa/browser-consent-initial-failed.json`. The harness then used actual Chrome pointer input plus explicit gesture assertions; the final `browser-consent.json` passes on the final content hashes. This does not establish native touch behavior on physical hardware.

## Reproduction and handoff

From this book directory, with the same read-only installed skill:

```sh
python3 segment.py
node build.mjs
python3 make-map.py
node verify.mjs
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs children-of-captain-grant.html --require-bilingual
node browser-check.mjs 320
node browser-check.mjs 390
node browser-check.mjs 1024
node browser-check.mjs 1440
node browser-check.mjs consent
node browser-check.mjs ios
```

The reader is the one standalone HTML; drafts, JSON, maps and QA are review materials. It embeds fonts/settings and needs no adjacent runtime files. `ready.json` records exact hashes and keeps every root acceptance gate false. Root must personally read the complete resulting RU and EN text and all nested routes, compare coverage and omissions, and inspect the key primary mechanisms before any publication. Literary engagement and edition/fidelity acceptance remain root's decision.
