# Accelerando — implementation self-check, 2026-10-31

**Ready for independent check only. Not a publication approval or whole-novel fidelity certificate.** Corrected BRIEF replaces the previous analytical assignment.

## Result

Rebuilt all prose from the 104-pair root analytical digest into **52 new RU/EN pairs**, `contentMode: "narrative"`. Four canonical files now exist in `collector-output/akselerando/`. There was no prior collector folder for this slug. Historical 30/70/104 quotas are replaced by justified **14/26/52** nested counts. The three routes were separately reread for continuity. Essential/Core end at the threshold of first contact; Deep follows the remaining plot. Final is a spoiler-safe closing, not a set of life lessons.

| Mode | Screens | RU title/subtitle/body words | EN title/subtitle/body words | RU / EN estimate |
| --- | ---: | ---: | ---: | --- |
| Essential | 14 | 698 | 834 | 4 / 4 min |
| Core | 26 | 1,312 | 1,541 | 8 / 8 min |
| Deep | 52 | 2,679 | 3,132 | 15 / 15 min |

Word counts use the maintained builder's Unicode definition; the structural auditor excludes the cover subtitle and therefore reports 2,675 RU / 3,127 EN. Counts include cover/final. One primary source, one original embedded SVG cover. No old book-cover image or review material remains. No word-floor padding.

## Substantive check

Read every original 104 RU/EN pair from effective root HTML, not a draft inferred from it. Read every replacement 52-pair sequence and compared Russian/English for the same actions, relationships, uncertainty and spoiler levels. Checked every final screen against the scene map in `sources.md`. Explicitly checked that the first act introduces Pamela, Annette and Sadeq in Essential even when Core-only introductions disappear.

The source is a complete author-hosted edition. Actual reading was selected continuous primary scenes across all nine chapters, plus targeted full sequences; **continuous reading of every line is not claimed**. No secondary synopsis is used to supply the later plot. Important self-check corrections: genetic screening was distinguished from genetic editing; Amber's birth was not assigned to Annette; the ghost's time claim was kept unverified; the decoy inhabitants' reality remained a question; Aineko's manipulation account and Manfred's explanation were attributed.

## Construction and local additions

Built with `node skills/book-tiktok/scripts/build_story.mjs collector-output/akselerando/story-data.json --out collector-output/akselerando/akselerando.html`. Six maintained-builder invocations during this repair; only the final candidate is identified by the ready manifest. No shared script/template/installed skill changed.

Book-local HTML additions, which a plain builder does not reproduce:

- Start in Essential on **every page load**, even with a saved legacy Deep mode; language/theme preferences still work.
- A localized accessible Deep confirmation guards both `setMode` and hidden-ID `goToId`, including Continue. Cancel and Escape retain the prior state; accepting enables Deep for the current page lifetime. Generic resume copy reveals no Deep title. Reopening the page renews consent.
- Hide the duplicate decorative cover at widths <=1100px and in focus. At 320px the title moved from y≈446 to y≈110, leaving the story introduction visible immediately.

The body corpus and JSON match exactly. Main shared template already honors narrative mode by suppressing per-screen provenance. Publisher must preserve the local additions or supply maintained equivalents before root integration. The root catalogue/reader were not changed here.

## Structural and browser evidence

Final command: `node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/akselerando/akselerando.html --min-screens 52 --require-bilingual` — **69 passes, zero warnings/failures**.

Final isolated-Chrome matrix: `(14+26+52) × 2 languages × 2 themes × 4 viewports` = **1,472 normal reading-state visits**, at 320×568, 390×844, 1024×768 and 1440×900. All screens in every mode: correct localized title, correct counter, reachable text bottom, no document/reader horizontal overflow, reachable Next and no academic evidence label after the story. **28 recorded assertions per viewport**, including aggregate matrix cases (not 112 different features).

Native key checks passed F with Next focused, and Escape exits focus. Deep entry, button cancellation, native Escape cancellation, exact hidden saved-ID restoration, safe generic Continue, Sources with the method note, Home `href="./"`, and Restart clearing progress all passed. Sources stays in its dialog. No HTTP runtime requests in offline mode; zero observed runtime/console errors. Fonts and SVG are embedded. Screenshots of stable EN/light cover/prose states were visually inspected across all four widths. This is Chromium desktop/mobile metrics, **not physical iPhone Safari or installed-PWA verification**. Full gesture/iOS-install flows were not rerun or certified here.

The shared preview tool rejected file URLs (`unsupported-protocol: file:`). Used direct `file://` CDP without any server. Every manual Chrome used `/usr/bin/timeout 30`, a unique temporary profile and detached process-group cleanup in `finally`. Final process/profile check found zero owned Chrome processes and zero owned profiles. Earlier incomplete keyboard automation lacked native virtual key codes; the final run used native key events and passed. Earlier matrices are not added to the final 1,472 count.

Private research, browser scripts, PNGs and raw browser reports are stored outside the public repository under the external audit workspace. No source text or extraction was written here.

## Handoff limits

Independent editorial reading of every changed pair remains required. Review is evidence-scoped to selected primary scenes; there is no whole-edition line-by-line fidelity claim. No physical iOS/PWA check or publication is claimed. Publisher owns root replacement, catalogue screen/minute/description updates and live verification. No git/PR/deploy/external messaging, root reader, catalogue or shared-shell edits were performed.


## Parent meaning corrections — 2026-10-31

Parent applied required independent meaning findings ACC-01 in RU and EN. Changed pairs: fatal-negotiation. Embedded data/derived reading estimates refreshed without replacing outer reader code or styles. This is a localized closure awaiting publisher validation, not a new independent PASS.
