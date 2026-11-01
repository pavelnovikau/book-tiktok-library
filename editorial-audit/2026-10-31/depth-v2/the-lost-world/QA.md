# The Lost World — expanded candidate handoff

Status: `ready-for-root-personal-check`. Unpublished. No self-PASS and no claim of root acceptance. Technical evidence does not establish literary fullness or source fidelity by itself.

The complete supplied English novel was read continuously through the ending in bounded outputs. Connected original Russian prose was completed first, corresponding English next, segmentation afterwards. All sixteen chapters are represented. There are122 narrative paragraph beats, not an inflation of the old34screen text. First-person Malone, embedded accounts, comic relationships, mistaken judgments, violence, distinct excursions, escape and the actual ending remain. Details and omissions are documented in the full scene map. The resulting8557RUwords lie within the adventure planning range because the retained scenes need that room; no quota was used to pad it.

## Exact reading metrics

Words use the maintained builder’s Unicode letter/number token regex, retaining internal apostrophes and dashes. Narrative words count only the122 narrative bodies. Titles, subtitles, cover/final and consent framing are separate. UI, section/kicker labels, method and Sources are outside these estimates. Exact machine values: `metrics.json`.

| Mode | All / narrative screens | RU narrative words | EN narrative words | RU narrative minutes at180wpm | EN at220wpm | RU / EN with titles, subtitles, framing | UI estimate RU / EN |
|---|---:|---:|---:|---:|---:|---:|---:|
| Главное / Essential |32 /30|2130|2553|11.8333|11.6045|2265 /2739|13 /13min|
| Суть книги / Core |68 /66|4681|5652|26.0056|25.6909|4898 /5952|28 /28min|
| Глубоко / Deep |125 /122|8557|10310|47.5389|46.8636|8933 /10815|50 /50min|

Deep framing body:89RU/104ENwords; its titles/subtitles:287RU/401ENwords. The structural auditor’s own word counter excludes the cover subtitle, giving8928RU/10809EN; these are neither narrative totals nor the builder’s subtitle-inclusive totals above.

Essential is explicitly an unfinished opening throughVIII, ending at the foot of the plateau. Core develops the story throughXII, ending with the camp mystery, before its explanation. Deep retains all chapters and ending after fresh consent. Working `route-<mode>-<lang>.md` files expose every exact sequence for root reading. The shared final is neutral, even after Deep. Lower covers, contents, Sources/method and saved-Deep resume labels reveal no decisive late outcomes.

## Mechanical and browser evidence

`qa/parity.json`: all authored/embedded screen fields match exactly; all122RU/EN draft paragraphs match the screen bodies in order; all top-level authored fields match except builder-generated mode time values. Mode labels themselves match. `verify.mjs` reproduces this and exact metrics. Cover and warning/final are explicitly excluded from narrative count. Warning/final provenance is editorial framing (`synthesis`), not an invented lesson attributed to Doyle.

`qa/structural-audit.json`:69structural conditions, zero warnings, zero failures on the final HTML. Builder and book-local patches are recorded in `build-record.json`; the installed skill, shell, fonts and licenses were consumed read-only. The clean builder was used, not another book’s HTML. Candidate-local code follows the accepted pilot’s fixed guard, uses `book-tiktok.the-lost-world.depth-v2.` and does not migrate older short-reader progress.

`qa/browser-320.json`, `browser-390.json`, `browser-1024.json`, `browser-1440.json`: representative cover, dense prose, cliff/camp scenes, later prose and final under both languages, both themes and Sans/Serif. Compact icon-only header and desktop rail checked. Actual platform-font queries verify custom Geist Sans, Geist Serif for English and Source Serif4 for Russian Serif. A dense320px paragraph scrolls89px to show its final character; end-character visibility also checked at other widths. At390px every screen in all three routes was navigated once in each language and the scene map was checked against the selected depth. These traversals are UI checks, not literary acceptance.

`qa/browser-consent.json`: native cancel/Escape, four real Deep→Essential/Core downgrade/resume chains across RU/EN, a downgrade at a scene shared with Core, picker re-entry, six fresh reload cases including saved Deep mode, retained late destination after acceptance, generic resume label, explicit final entry, invalid saved ID fallback, language position, Settings position/scroll, native keyboard focus and return, Sources/Contents dialogs, focus paging/exit, keyboard back, synthetic pointer swipe and final restart. Consent is never stored. Theme/font preferences survive reload in `bookLibrary.preferences.v1`.

Pagehide/pageshow with persisted flags was explicitly exercised for the BFCache lifecycle hook; this is event emulation, not a physical Safari back/forward-cache claim. Reloads and mode downgrades are actual reader operations. No physical iPhone, Safari, installed PWA, cross-origin preference sharing or production deployment was tested. Normal file-origin sharing across different downloaded readers is browser-dependent.

All five final browser reports bind to the final story/HTML hashes. Each Chrome had an independent `mkdtemp` profile, `timeout30`, detached owned process group and finally cleanup. Every report confirms profile removed and owned group no longer alive. No content server, preview tool or external runtime request was used; no runtime exceptions were observed. Early screenshots captured before compositing were discarded by reshooting after two frames and a settling interval. Final320ENdark/Sans,390RUlight/Serif and1440cover screenshots were visually inspected; dense text is deliberately scrollable.

## Scope safeguards and historical checks

The gate is session-only: every Deep picker or hidden level3target requests consent; an actual downgrade revokes it, as do leaving/reloading and restored-page lifecycle. A saved late ID remains the intended destination after acceptance. The root pilot’s previous downgrade bug was not copied. All Sources maps are selected-depth-only. The complete primary link is accessible and honestly warns that it contains the entire plot; embedded data are not a secrecy boundary.

Historical source corrections are retained: same-evening Gazette request; Wednesday appointment; separate earlier raid; later intact enclosure with open entrance; no invented returning-Malone shot; Roxton’s earlier shot/spent cartridge and capture account; second rescue shot misses; actual cave/fork/rope escape; no certain end for the escaped specimen. Primary windows in the scene map are prepared for root’s direct checks. Scientific/colonial views belong to fictional narrators/characters; no modern scientific validation or management/moral exercises have been inserted.

`protected-baseline.json` captured131existing files including the old assigned collector, old ready/reviews, root library files, accepted pilot and installed builder assets. Recheck found130byte-identical. The sole observed external change is parent `depth-v2/PLAN.json`: its timestamp advanced from2026-10-31T23:42:03.587388+00:00 to23:51:50.448742+00:00 and this book was marked assigned. This worker did not write that file or refresh the baseline to conceal the change. Old collector/ready/reviews, root/library files and installed skill remain byte-identical. The local old root’s144screens differ from the34screen collector; neither was replaced or newly accepted here.

Only files in this new book directory were written. No old files archived or old reviews changed. No parent log/status/plan, shared shell/catalogue/root-reader writes; no Git, PR, deploy, agent restart, delegated polling, external message or subagent. The task’s explicit ownership restriction overrides general shared-log close-out conventions.

Remaining: root must personally read complete final RU/EN prose and all six routes, compare the full map with the source, directly inspect key primary windows, review omissions, fiction/translation limits and ending handling, and accept/reject exact hashes. Until then this is a reviewable candidate, not a publication approval.


## Root personal acceptance - 2026-11-01

Current counts33/68/125. Root read every RU/EN pair and the shorter routes, reviewed the complete16-chapter map and checked the actual primary windows in root-review/reading-ledger.json. Bounded corrections and exact accepted hashes are in root-review/personal-review.json. Current root QA is under root-review/qa. Earlier worker evidence remains historical input-version evidence. Complete primary reading belongs to the writer; root primary checking is selective.
