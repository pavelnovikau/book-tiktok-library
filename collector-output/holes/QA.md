# Holes — local implementation checks

Status: **ready-for-independent-check**. These are implementation checks, not independent editorial acceptance or certification of the complete novel.

## Delivery

- Canonical authoring: `story-data.json` (schema 2, `contentMode: narrative`).
- Standalone reader: `holes.html`; sources: `sources.md`; this QA record: `QA.md`.
- Defaults: **RU / dark / Essential**. Embedded Geist and Geist Mono; offline Flexoki light/dark; royal-violet main action. Shared fonts, header, Settings PR29 and installed skill were not edited.
- Exact cumulative modes, cover and shared final included: **14 Essential / 23 Core / 39 Deep**. Levels: **14 / 9 / 16**. These follow manuscript segmentation; no historical screen quota existed.
- Computed reading labels: **5 / 7 / 11 minutes**, both languages. Builder totals, including titles/subtitle/framing: RU **753 / 1138 / 1899**; EN **924 / 1393 / 2355**.
- Narrative body density across 37 story screens: RU median **47**, range **25–87** words; EN median **57**, range **31–101**. Long screens scroll vertically; they were not expanded or split to meet a quota.
- **11** source records; no remote runtime asset, cover image, copied book chapter or full-text source file.

## Reproduction

```sh
node collector-output/holes/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/holes/holes.html --min-screens 39 --require-bilingual
node collector-output/holes/qa-holes.mjs 320 568 matrix
node collector-output/holes/qa-holes.mjs 390 844 matrix
node collector-output/holes/qa-holes.mjs 1024 768 matrix
node collector-output/holes/qa-holes.mjs 1440 900 matrix
node collector-output/holes/qa-holes.mjs 390 844 behavior
node collector-output/holes/qa-holes.mjs 1440 900 behavior
node collector-output/holes/qa-holes.mjs 320 568 ios
```

`build-local.mjs` invokes the maintained v2 builder and applies guarded, book-local changes: typographic narrative cover, Smartcat action tokens, localized spoiler consent, masked Deep contents and safe navigation hooks. It never writes the shared template, header, fonts or other readers. Build hashes of the maintained inputs are in `qa/build.json`. No copied reader is used.

## Structural and corpus checks

Maintained audit: **69 structural checks, zero warnings/failures**; receipt `qa/audit.json`. The authoring's every field, all RU/EN titles/bodies, stable IDs, levels, source arrays, defaults, method note and spoiler policy equal the effective embedded HTML corpus. Builder-computed reading labels are the only added field. Scene-map retained text/source assignments equal the actual corpus. Receipt: `qa/parity.json`.

Actual content reading: **39 unique RU/EN pairs / 78 language texts**, all read in authoring and extracted effective HTML. The complete Deep sequence was read, and Essential/Core were separately read as continuous filtered narratives in both languages. All late edited pairs and the cover were reread after corrections. Six cumulative language routes contain **152 language-screen appearances**, not 152 unique screens.

No earlier collector or published root `holes.html` existed. Old collector pairs read: **0**; old root pairs read: **0**; old/root divergence: not applicable. This is an approved queued title's first build.

## Browser, offline and mobile

Seven final bounded browser runs match the final HTML hash. **48 mode/language/theme/viewport cases, 1,216 screen renders, 145 recorded assertions**, zero runtime exceptions and zero external runtime requests. Every run used `file://` with the network forced offline. No server was started.

| Coverage | Observations |
| --- | --- |
| 320×568, 390×844, 1024×768, 1440×900 | All screens in every depth × RU/EN × dark/light traversed. Actual bodies/titles equal expected copy; counters equal 14/23/39; no horizontal overflow; last paragraphs and cover start action reachable by vertical scrolling. |
| Header and reading chrome | Compact icon-only row fits. Localized labels/tooltips, `./` Home contract, Sources/Contents and narrative provenance hiding checked. Embedded fonts load offline. |
| Desktop | Rail visible, scrollable and synchronized; active final brought into view. Deep rail selection cannot bypass consent. |
| Interaction | Buttons, keyboard, text-tap focus, focus-preserving paging and horizontal pointer swipe checked. A second text tap restores chrome. Language/theme retain exact scene and depth. Unknown stale IDs fall back to cover. |
| Sources | Global dialog opens with all 11 records and the localized, honest source/method boundary. No per-screen research chrome. |
| iOS emulation | iPhone user agent with **actual engine safe-area inset 47px top / 34px bottom**: all six icons below status inset; guide opens/localizes/closes; focus hides guide/header; exiting focus restores header. Standalone emulation suppresses guide and trigger. Vertical pointer drag does not page/toggle focus, and dense text remains programmatically scrollable. Native touch synthesis did not complete in bounded CDP runs and is **not claimed verified**. This is **Chromium emulation**, not physical Safari/PWA testing. |

Representative cover/dense prose/final screenshots were produced. Visually inspected: 1440px RU dark cover, 320px RU dark dense prose, 390px EN light dense prose and phone cover/final states. There are no image/list/comparison screens in this novel package to test.

Early test harness faults were corrected: a newline inside the evaluated JavaScript string, missing native Escape key codes, and a desktop swipe starting outside the reading surface. The final receipts are successful runs on the final reader hash. Two additional native-touch CDP attempts timed out; both owned browser trees/profiles were cleaned. The final suite separately tests vertical pointer gating and actual programmatic scroll reach; native-touch/physical Safari remains an explicit limit. No shared reader/UI was changed to satisfy the test harness.

## Spoiler checks

Essential/Core stop during Stanley's desert search. Reunion, the tragic past outcomes, ancestral fulfillment, decisive discoveries and final outcomes are **level 3 only**. Cover, shared final and global source/method notes disclose scope without giving those outcomes.

Deep consent is localized, explicit and volatile. Selecting Deep on the cover, a masked Deep chapter/rail item or saved Deep Continue asks before navigation. Escape/Cancel reveals no scene and preserves the save. Accepted Continue resumes the exact saved ID. Reload falls back to Essential and keeps a **generic** “Continue Deep — ending spoilers” label. Downgrading to Core revokes consent; final restart clears progress. No decisive Deep title appears in shallow contents.

## Evidence boundary and remaining work

Primary reading is selective: publisher sample chs. 1–4/start 5 plus short actual novel passages embedded in the named guides. Later actions are supported by the substantial guides and checked primary hinges in `source-evidence-map.json`; this is not full original-novel reading or a published translation. The separate `sources.md` ledger specifies every source's role, exact consulted extent, blocked routes and omissions.

Independent reading/source-sufficiency review remains pending. Physical iPhone/Safari verification and publisher integration remain outside this local check. No known failed final implementation check remains.

Every Chrome invocation used `/usr/bin/timeout 30`, an owned `mktemp -d` profile and a detached owned process group. All seven profiles were removed; zero owned browser processes remained after cleanup. Final proof: `qa/final-summary.json` and seven `qa/holes-*-*.json` receipts.

Only this collector and the assigned book report/ready manifest are written. No root reader, catalogue, index, shared shell/skill/fonts, installed skill, log, Git, PR, deploy or external message operation.
