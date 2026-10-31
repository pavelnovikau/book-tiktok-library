# Have Space Suit—Will Travel — local implementation QA

2026-10-31. **Prepared for independent check; this is not independent editorial approval.** New approved queued title; no existing published reader or collector corpus was replaced.

## Delivered corpus

- Canonical authoring: `story-data.json`; portable reader: `have-space-suit-will-travel.html`; evidence: `sources.md`; this record: `QA.md`.
- `schemaVersion: 2`, `contentMode: narrative`, RU / dark / Essential defaults, `spoilerPolicy: full-plot-in-deep`.
- **17 / 25 / 38** cumulative Essential / Core / Deep screens, including cover and shared final. Level additions: **17 + 8 + 13**. No historical screen quota was retained; counts were derived from 35 drafted narrative paragraphs plus cover, warning and final.
- Builder word totals (title/subtitle/body): RU **931 / 1,362 / 2,113**; EN **1,166 / 1,702 / 2,653**. Estimated minutes: RU **6 / 8 / 12**, EN **6 / 8 / 13**. These are calculated estimates, not a length promise or a padding target.
- Narrative body density, excluding framing: RU min/median/max **39 / 54 / 65** words (mean 53.9); EN **44 / 68 / 85** (mean 67.3).
- Five disclosed source entries: three chapters of actual author text in a lawful Baen sample, one substantial Robert James guide, one publisher identity entry. These are not five independent complete-book witnesses.

## Content and scope

The implementation author read all **38 unique RU/EN pairs** (**76 localized screen versions**) and the three resulting nested sequences. The resulting route orders are saved in the content map; overlapping screens are not counted as newly reviewed pairs each time.

The opening retains the Moon ambition, soap competition, failed first prize, Oscar’s restoration, and unexpected radio reply. The middle preserves Peewee/Mother Thing relationships, the door obstruction and removed ship brain, the three-in-two-suits escape, air limits, recapture, Pluto and failed cell escape. Deep alone continues through the mutual rescues, treatment, proceedings and return. Humour is carried by the wrapper, napkin, radio-fit problem, Peewee’s behaviour and the actual final incident. No invented dialogue, new scene, exercise, management analogy, moral conclusion, or claim of definitive authorial intent has been added.

Selected Baen author passages in chapters 1–3 were consulted. The later events are checked at the retained granularity against James’s official-hosted summaries of chapters 4–12 and their short embedded author quotations. **No full continuous novel reading or published-Russian-translation check is claimed.** The full novel was not obtained. `sources.md` maps every screen and causal link and records excluded details. An independent reviewer must judge the guide-dependent part on that explicit scope.

## Build and exact corpus checks

Rebuild only this collector:

```sh
python3 collector-output/have-space-suit-will-travel/segment-prose.py
node collector-output/have-space-suit-will-travel/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/have-space-suit-will-travel/have-space-suit-will-travel.html --min-screens 38 --require-bilingual
```

`segment-prose.py` segments the original `prose-first.md`; it does not generate filler to hit a quota. `build-local.mjs` invokes the maintained builder and adds only this novel’s consent guard, generic protected resume, all-depth masked chapter navigation, prose cover and local focus-action tokens. It changes no shared template, reader-header, installed skill or font code. The home link remains `./` for the publisher’s root integration.

The maintained audit reports **69 structural checks, zero failures**. One warning, `source coverage gaps: ending-warning`, is intentional: that screen is a consent/navigation notice and asserts no sourced book event. It is not an unsupported part of the narrative. `qa/structure.json` retains the exact output.

A separate comparison confirms exact equality of authoring and effective embedded **screens, sources and method notes**. Counts are recalculated from actual levels. See `../../editorial-audit/2026-10-31/books/have-space-suit-will-travel-sol-implementation.evidence/content-map.json`.

## Browser checks

Chrome opened the generated **local file with network disabled**; no HTTP/Vite server was used. Every invocation ran under `timeout 30` with a separate `mktemp -d` profile, owned detached process group, and unconditional cleanup. All reports record `profileRemoved: true`. No other worker’s Chrome was touched.

| Viewport | Coverage | Result |
| --- | --- | --- |
| 320×568 | All modes × RU/EN × dark/light; every title/body and counter; one-row icon header; horizontal bounds; last paragraph reachable | Local checks passed |
| 390×844 | Same complete matrix | Local checks passed |
| 1024×768 | Same matrix; visible synchronized scrollable desktop rail | Local checks passed |
| 1440×900 | Same matrix and desktop rail checks | Local checks passed |
| 390×844 and 1440×900 | Consent/cancel, hidden Core/Deep chapter navigation, language/theme position preservation, dialogs, progress/resume, buttons/keys, tap focus, horizontal swipe, vertical gesture, final restart | Local checks passed |
| 320×568 iPhone emulation | Install instructions, localization, six icons below a real engine 47px safe-area inset, scroll/focus stability, standalone guide suppression | Local checks passed |
| 320×568 and 1440×900 cover controls | Scrolled Start/depth controls reachable, 44px targets, Deep opens warning before content | Local checks passed |

The four full matrices performed **1,280 screen renders** in total: `(17+25+38) × 2 languages × 2 themes × 4 viewports`. Every displayed title and paragraph was compared with the authoring corpus; no horizontal overflow or inaccessible last paragraph was found. Source footnotes/provenance chrome stay hidden in narrative mode; the Sources dialog remains accessible. Empty media is intentional: no images, documentary scans, or invented scene art need to load. Embedded maintained Geist and Geist Mono load offline. This does **not** certify complete Cyrillic font coverage; settings/font work under PR29 remains separate.

There were **zero unexplained application runtime exceptions** and **zero remote page-runtime requests** in every completed browser phase. The first matrix attempt had a quoting error in the newly written QA harness; it was fixed before the successful complete matrix and was not an artifact runtime error.

Screenshots in `qa/` cover the default Russian dark cover, Russian narrative, English light narrative and final, consent dialog, Sources and emulated iPhone safe area. Representative saved images were inspected: reading text is unobscured, desktop measure is bounded, the phone header is compact, and the simulated status inset is reserved. Cover buttons below the first phone viewport are reachable by scrolling. Real iPhone Safari/PWA hardware was **not** tested. List/comparison/image screens are absent by editorial choice, so those fixture types are not claimed tested.

## Spoiler and saved-progress checks

- The cover warns about Deep without giving an outcome. Essential/Core stop at `no-way-out` before `ending-warning` and all decisive results.
- Clicking Deep or any hidden level-3 chapter opens a bilingual modal. Cancel keeps position and depth. Keyboard cannot page through the open modal.
- All level-3 chapter titles are masked before consent, including on the desktop rail. Direct hidden Core navigation raises only to Core.
- Deep resume uses only the generic label `Continue Deep — ending spoilers` / `Продолжить Deep — спойлеры финала`; it exposes no saved ending title.
- Reload preserves the saved ID but resets active Deep to Essential; resuming requires fresh consent. Downgrading revokes consent.
- The shared final, global source notes and descriptions disclose method and route behaviour without revealing outcomes.

## Remaining work and limits

Independent content review is pending. No independent PASS, whole-book fidelity certificate, continuous reading claim, or certified translation is issued by this implementation worker. No unsupported essential link is currently identified in the retained arc; the later source scope remains less direct than a full-primary-text check. Actual iPhone/PWA behaviour, publisher integration, library registration, publication and production verification remain with their respective owners. No root/catalogue/index/shared-shell/installed-skill/log files, Git/PR, deployment or external messages were touched.
