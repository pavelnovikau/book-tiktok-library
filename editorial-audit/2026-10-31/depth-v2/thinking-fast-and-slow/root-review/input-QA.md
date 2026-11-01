# Local QA — expanded Thinking, Fast and Slow pilot

2026-11-01 Europe/Warsaw. Implementation checks only. Status: **ready-for-independent-check**, never self-PASS. Publication and root editorial acceptance remain open.

## Resulting scope and counts

The connected RU manuscript was written first, then translated into EN, before phone segmentation. There are 58 authoring units and 154 paired paragraphs, segmented into 97 bilingual screens. Every current collector screen ID (29/29, including cover/final) still exists; this preserves the slug and semantic resume anchors. The new authoring corpus is independent of the 29-screen collector. Its old HTML embedded screens match its old JSON; no root `<slug>.html` or exact catalogue slug entry exists at the inspected library root.

| Depth | Screens | RU body words | RU at 180 wpm | EN body words | EN at 220 wpm | Reader UI minutes RU / EN |
|---|---:|---:|---:|---:|---:|---|
| Essential | 25 | 2,292 | 12.73 min | 2,579 | 11.72 min | 14 минут / 13 min |
| Core | 68 | 5,873 | 32.63 min | 6,613 | 30.06 min | 35 минут / 32 min |
| Deep | 97 | 8,311 | 46.17 min | 9,347 | 42.49 min | 49 минут / 45 min |

Body counts use the installed builder’s Unicode lexical-word regex, excluding cover, headings, subtitles, method/source notes and UI, but including the shared final. Full UI estimates include cover and headings; that explains the larger estimates shown on the cover. They are estimates, not timed reader measurements. Exact machine metrics and density are in `qa/metrics-and-integrity.json`.

The 8,311-word RU body lies within the authorized 8–12k planning range; there is no length deviation to justify. It is about four times the old ~2,040-word body. Quantity itself does not certify completeness. Deep contains every draft paragraph once; Core contains 5,873 RU words, and Essential 2,292. Both shorter routes remain explanatory rather than lists of conclusions.

During route review, “third principle” was changed to “another principle” so Essential does not depend on a missing second principle. The anchor case and probability weights were promoted into Essential so the shared closing discussion introduces no unexplained mechanism. This derived 25/68/97 rather than preserving the preliminary 22-screen short route. No padding or independent prose was generated from a screen target.

## Structural and offline checks

- Maintained installed builder: `/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs`, read-only. No copied reader shell, runtime-logic patch, installed-skill edit, shared synchronization, content server or preview tool. Candidate-local CSS hides the unrelated generic seven-node “one model to take away” cover; the actual bilingual title/copy supplies a typographic cover. Header, Settings, Sources and state logic remain the maintained implementation.
- Deterministic audit: 69 checks, zero failures/warnings (`qa/structural.json`). This is a structural result only.
- Effective embedded screens and source records equal canonical JSON. `contentMode: explanatory`; RU/dark/Essential on fresh storage, Sans initially. Five global Sources records with honest book/publisher/reference roles. No remote runtime dependency; all fonts/licenses embedded.
- Offline `file://` Chromium traversal at 320×568, 390×844, 1024×768 and 1440×900, both languages, both themes, Sans and Serif, **each complete depth route**: 24 routes and 1,520 rendered visits per viewport. Titles and body paragraphs compared with data, exact counts/order checked, document/slide overflow checked and each body tail reached by scrolling. Zero unexplained runtime exceptions or remote requests.
- Settings gear opens without toggling theme; radio controls change actual theme/font; book ID, depth, counter and reading scroll preserved. Source and Contents dialogs, labels, icon-only one-row header, home link, rail and rail active ID checked.
- Actual platform-font records confirm embedded Geist for Sans in RU/EN, Source Serif 4 for RU Serif and Geist Serif for EN Serif. The localized fallback note remains visible. Not merely checking a CSS family declaration.
- Keyboard next/back, buttons, horizontal pointer swipe, vertical gesture discrimination, focus entry/exit, paging in focus, final restart, saved EN/Deep ID after reload, Continue and Start over checked. All 29 old stable IDs remain available in the new corpus.
- Additional iPhone-UA runs at 320 and 390 with actual CDP safe-area override (44 top/34 bottom): six controls in one row below the inset; guide automatic/open/close and EN manual localization; CDP touch swipe; emulated `navigator.standalone` hides guide/trigger. These are Chrome emulations, **not physical iPhone Safari/PWA tests**.
- Visually inspected final 320 light/RU Serif dense prose, desktop dark/EN quantitative case, and iPhone dark cover. Long phone prose intentionally scrolls vertically. No list/image layouts were added; no images are required by this text-led pilot.

Each run used `/usr/bin/timeout 30`, `/usr/bin/mktemp -d`, an isolated process group and `finally` cleanup, including the failed harness run. Reports confirm profile removal and zero surviving owned PIDs. Browser reports bind the exact candidate JSON/HTML/harness hashes. No other active browser instance was terminated.

## Harness corrections, not hidden product failures

The first screenshots were captured during the entrance opacity transition; screenshot timing was corrected and the final matrix recaptured after 350 ms. One initial iPhone check expected the pre-swipe saved ID after deliberately advancing with a touch swipe. The reader correctly saved the advanced screen; the harness now restores its intended fixture before testing reload. The original failed report is retained as `qa/browser-ios-390-harness-before-reset.json`; final iOS reports have zero failures and completed cleanup. No product shell/content workaround was made for either harness issue. A separate final visual finding removed the unrelated generic cover decoration through candidate-only CSS; the full final matrix was rerun.

## Editorial self-check and required next review

All 58 RU/EN units were authored/compared in meaning, all resulting screen pairs inspected through their data/rendering, and the three nested sequences checked for dependencies. This is the writer’s review. The source ledger separately identifies complete support sections, partial chapter coverage and omitted chapters; it does not claim a continuous full-book read. EN has not been collated with the complete English volume.

KAH-01 was checked against full `content92`: every branch of A/B and A′/B′ remains. KAH-02 was checked against full `content84`: independence, overall well-being and the long-shot exclusion are three distinct conditions. Two-toss outcomes preserve the possibility of loss. Controls, hash counts and lexical matching cannot establish any of these source meanings by themselves.

The next reviewer must read all 97 RU/EN pairs and all six language/depth routes; assess whether a reader understands **why** each mechanism works and how the five parts connect; inspect the 38-chapter omissions and experiment map; directly check key primary sections, the critical probability/risk qualifications, and any other disputed specificity. Under the latest BRIEF, the root personally performs and records final acceptance with exact hashes. A delegated PASS, word count or local technical check alone is insufficient.

Remaining boundaries: no continuous whole-volume reading, full English collation, exhaustive research-status review, physical iPhone/PWA test, production integration or external publication. Three later primary abstracts/method introductions qualify specific scope in Sources rather than silently rewrite the 2011 argument. No medical, financial, scientific or full-translation endorsement is claimed.

## Ownership and reproduction

Only this NEW candidate directory was written. Current collector, old ready manifest, reviews, books.json and prior records match intake hashes. No Git/PR/deploy/status/log/shared-shell action occurred. Root public readers were not created or changed.

Rebuild: `python3 prepare-candidate.py`; then `node build.mjs`, which invokes the maintained installed builder and applies only the documented local cover CSS. Audit command is recorded in `qa/structural.json`. Browser runs: `node browser-check.mjs 320` (likewise 390/1024/1440), and `node browser-check.mjs 320 --ios` / `390 --ios`. `node measure.mjs` checks embedding and hashes and writes the exact per-depth metrics. Do not use the later readiness manifest as editorial approval.
