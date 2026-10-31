# To Kill a Mockingbird — local implementation QA

2026-10-31. Status: **ready-for-independent-check**, not an independent literary PASS or publication approval.

## Corpus

New implementation of the already approved Harper Lee 1960 novel. No previous Mockingbird collector/root corpus existed to repair; old pairs read: 0. Wrote and read 41 new RU/EN pairs (82 language texts), then checked the effective embedded HTML corpus against canonical JSON. All canonical fields match. Re-read the revised school, air-rifle, jail and interrupted-afternoon pairs after the final edits. Reviewed the Essential/Core/Deep routes for antecedents, causality and spoiler boundaries.

`contentMode: narrative`; RU / dark / Essential default; `spoilerPolicy: full-plot-in-deep`. Original bilingual condensation, not a claimed published translation. No film, stage or *Go Set a Watchman* material. Scene/character actions carry the narrative; no lessons about the reader’s life, leadership, exercises or invented dialogue.

The manuscript was saved as `prose-first.md` before segmentation. Exact cumulative totals, including cover and final, are **14 / 28 / 41**; level counts **14 / 14 / 13**. Counts were derived from meaningful scenes, without padding to historical totals. Maintained builder word estimates, including headings and cover copy: RU **569 / 1102 / 1616**, EN **718 / 1375 / 2016**. Computed reading estimates: RU **4 / 7 / 9 min**, EN **4 / 7 / 10 min**. Four sources; no images/media dependencies.

Evidence scope is a substantial official DBE chapter guide plus checked primary passages, including a permission-labelled publisher excerpt and the NCC document excerpt. Full novel not read continuously; no exact owned OPF match found among 216 checked metadata records. Guide-only trial and final-chapter support is explicit in `sources.md` and `source-evidence-map.json`. Evidence sufficiency for the retained sequence remains independently reviewable; a structural pass cannot establish whole-book fidelity.

## Build

```bash
python3 collector-output/to-kill-a-mockingbird/segment-prose.py
node collector-output/to-kill-a-mockingbird/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/to-kill-a-mockingbird/to-kill-a-mockingbird.html \
  --min-screens 41 --require-bilingual
```

`build-local.mjs` runs the maintained v2 builder, then the maintained shell application with exactly this collector HTML as its argument. It applies a bounded book-local patch for spoiler consent, safe contents/resume labels, story ID instrumentation, a text-only narrative cover and the tree’s royal-violet action token. It does not copy a reader or edit shared Settings/font code. Build-input hashes and the scoped application are recorded in `qa/build.json`. The min-screens assertion is this finished corpus’s count, not an editorial quality threshold.

Deterministic audit: **69 passes, 0 warnings, 0 failures**. Actual JSON/effective corpus, nested counts, unique stable IDs, bilingual fields, source references and offline constraints pass. The maintained builder supplies embedded Geist/Geist Mono and the one-row icon header. Narrative screens hide academic provenance labels; the global Sources dialog and embedded mappings remain available.

## Browser evidence

`qa-browser.mjs` uses the generated HTML through `file://` with the network set offline. Each invocation starts `/usr/bin/timeout 30` Chrome with its own `mktemp -d` profile, dedicated port and owned process group, and removes both process tree and profile on success/failure. No server or preview tool was used.

Final runs: seven; **154 assertions**, **48 matrix cases**, **1,328 complete screen renders**. Matrix includes all screens in each nested mode, both languages and themes at **320×568, 390×844, 1024×768 and 1440×900**. Each rendered title/body matches the effective corpus, counters match the selected mode, all text is reachable by vertical scrolling, and horizontal overflow is zero within the one-pixel allowance. The cover start control remains reachable by scrolling at 320 px.

- Fresh RU/dark/Essential/cover and offline font decoding.
- Single compact icon-only control row at phone width; localised labels; Home retains `./` for publisher placement.
- Cover, Contents, desktop rail and saved Deep resume require consent; cancel/Escape preserve position; all Deep titles masked beforehand. Reload and downgrade revoke consent; saved Deep labels remain generic. Modal keyboard navigation cannot reveal a screen behind it.
- Core chapter selection raises depth; language/theme changes and rapid repeated switching preserve screen ID and mode.
- Contents and Sources open/close; all four source records fit. Desktop rail is visible, scrollable and brings the active screen into view.
- Buttons, keyboard, final restart/cleared saved progress, pointer tap focus, horizontal swipe and vertical-gesture discrimination.
- iPhone Safari emulation: installation instructions/trigger, localisation, actual engine safe-area override of 47 px, focus restoration and standalone suppression. This is not a physical iPhone or installed-PWA test.
- Zero runtime exceptions, no external runtime requests, all seven profiles removed; process check found zero remaining Chrome processes carrying the owned profile prefix.

Visually inspected saved screenshots: 320 RU/dark cover, 320 EN/light dense paper-bag scene, 1440 RU/dark scene and rail, and 390 iOS safe-area view. Representative final, source, spoiler-dialog, focus and remaining viewport captures are also retained under `qa/`.

Final evidence: `qa/structure.json`, `qa/consistency.json`, `qa/final-summary.json`, seven `qa/mockingbird-*.json` reports and screenshots. Their hashes are anchored in the ready manifest.

## Remaining scope

Independent content acceptance is pending. The publisher owns accepted shared Settings/font integration, root/catalogue/index placement, final saved-progress/production integration and publication. Physical-device behaviour is untested. This worker wrote only this collector folder, its named implementation report and ready manifest; no Git/PR/deploy, external messages, root/shared/log/installed-skill edits or subagents.


## Parent local correction — 2026-10-31

TKAM-R1: the two cover clauses now name Tom Robinson and qualify hostility as coming from many white neighbours, avoiding narrator-certified town-wide consensus. All40 other reviewed screen records remain unchanged. The fresh independent reviewer actually checked the DBE guide chapter14/22 and qualification answer at printed58/79/99 (PDF74/95/115); parent repeat retrieval of that PDF timed out, so no fresh direct DBE reading is claimed. This narrows the same supported premise, not a new motive, legal judgment or ending revelation.

Only embedded data/derived mode estimates and the matching connected manuscript(s) were refreshed. Outer code/styles and bespoke spoiler guards are byte-identical. Older segmentation generators are pre-correction preparation artifacts; the updated story-data.json is the maintained builder input. Original independent review remains unchanged; localized publisher validation is pending, not self-issued PASS.

Parent focused regression completed: 176 assertions across the four corrected readers, RU/EN and 320/390/768/1440 widths with light/dark representative cases. Exact changed copy, scroll tails, no horizontal overflow/runtime/network requests, saved-Deep warning, cancel and accepted restore passed. Ender uses browser confirm; the harness explicitly accepts/dismisses it. Failed harness diagnostic retained separately; no product-runtime correction was needed. Owned Chrome/profile cleaned. Per-reader structural result remains 69 passes. Not physical iPhone/PWA or new independent literary approval.
