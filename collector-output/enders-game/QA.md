# Ender’s Game — local QA

2026-10-31. **Local implementation checks completed. Independent content review is pending.** No whole-book fidelity certificate, continuous-reading claim or professional translation certificate is issued by this file.

## Canonical delivery

- `story-data.json`
- `enders-game.html`
- `sources.md`
- `QA.md`

Work: Orson Scott Card’s 1985 novel. Narrative mode; RU / dark / Essential by default. Both languages share screen IDs, levels and source maps. The HTML is a standalone file with embedded CSS, JavaScript, Geist and Geist Mono. Twenty-four external source links are optional navigation through the Sources dialog; none is a runtime dependency.

Exact cumulative counts, cover and shared final included:

| Mode | Screens | Approximate RU time | Approximate EN time |
| --- | ---: | ---: | ---: |
| Essential | 16 | 5 min | 4 min |
| Core | 25 | 7 min | 6 min |
| Deep | 39 | 10 min | 9 min |

Levels: 16 / 9 / 14. Thirty-seven narrative pairs plus cover/final. Final effective corpus: 1,623 RU / 1,953 EN title-and-body words under the maintained audit’s tokenization. Narrative body-only density averages 39 RU / 47 EN words; ranges 17–74 RU / 23–88 EN. Density is diagnostic, not a quota. Initial 17/26/40 counts became 16/25/39 when the seven-word arrival fragment was merged into the departure beat.

## Editorial scope and parity

Wrote connected prose first, segmented afterwards. Read all 39 final bilingual pairs and each resulting mode sequence: 80 mode-pair appearances / 160 language appearances. Canonical fields and all embedded screen copies match exactly; see `qa/consistency.json` and `evidence/routes-ru-en.md`.

The source scope is selected primary material plus accountable guides, with source roles disclosed. The full novel was not available/read continuously. `evidence/primary-hinges.md` distinguishes actual author passages from the guide or critical wrapper and records the exact supporting locations. `evidence/screen-map.json` maps every narrative pair. Teachers’ questions were not treated as answers. No invented scene, speech, example, exercise, management analogy or new moral was added. Source adequacy for the retained arc remains available for independent challenge.

## Structure and offline behavior

Maintained builder: `skills/book-tiktok/scripts/build_story.mjs`, run by this book’s reproducible `qa/build.mjs`. Maintained audit: `skills/book-tiktok/scripts/audit_story_html.mjs … --min-screens 39 --require-bilingual`. Result: **69 structural checks, zero warnings, zero failures** in `qa/audit.json`.

The book-local build patch adds Deep consent and substitutes a quiet title page for the shell’s generic analytical diagram. No shared UI, skill or font code was edited or copied from the separately reviewed Settings PR29. The builder/header input hashes are in `qa/build.json`.

## Actual browser coverage

The final HTML hash was tested in six bounded Chrome runs. File URL only, network offline, no server and no preview_* tools.

- 320×568, 390×844, 1024×768 and 1440×900; both themes, both languages, all depths: **48 combinations, 1,280 screen renders**.
- Exact mode/contents counts, canonical title/body rendering on every screen, no document/story/content horizontal overflow, and usable vertical scrolling for long prose.
- Embedded fonts load; no network runtime requests or runtime exceptions.
- Single compact icon header, localized labels/tooltips, `./` Home contract, persistent desktop rail.
- Language/theme preserve the stable current ID; Contents and all 24 Sources entries open correctly. The mobile Sources dialog stays within the viewport and scrolls.
- Native Deep warning accepts/refuses correctly. Refusal keeps shallow content; no Deep titles in unconsented contents. Saved Deep uses a generic resume label, asks again on reload, and restores the exact ID only after acceptance. Downgrading revokes consent.
- Focus by keyboard and actual CDP touch hides chrome and preserves text/Next; restore preserves position. Previous/keyboard/swipe follow the selected nested sequence; a vertical gesture neither changes screen nor triggers focus. Final/restart clears the remembered position.
- Emulated iOS: automatic and manual guide, Share/Add-to-Home-Screen route, six header icons in one row at 320, simulated safe-top inset, guide hidden in focus and navigator.standalone mode. **Physical iPhone/Safari/PWA was not tested.**

Final browser assertions: **99**, all true. Detailed final-hash records: `qa/checks-{320,390,1024,1440,behavior,ios}.json`, `qa/browser-{320,390,1024,1440}.json`, `qa/final-summary.json`.

Representative screenshots inspected: dark mobile and desktop shower scene; light 320 English dense Graff scene; light 390 English cover and scrolling Sources; light 1440 English cover; 1024 final/rail. They show the actual maintained fonts, not a copied unmerged font fix. The empty media map is intentional: no unlicensed cover or decorative image was introduced.

Superseded `qa/failure-*.json` files record initial harness assumptions and are explained in the implementation report. The corrected assertions measure settled slides rather than the 180 ms entry transform and check display:none for focus. They are not waived outstanding failures.

## Cleanup and limits

Each Chrome used its own mkdtemp profile under this owned QA tree, a hard `/usr/bin/timeout 30`, and owned process-group cleanup. Final check: **zero remaining profiles, zero owned Chrome processes, no server started**.

No root reader/catalogue/index, shared shell, installed skill or log was edited; no Git, PR, deployment, purchase, loan, credentials or external messaging action was taken. Publisher must perform independent content acceptance, accepted Settings/font integration, root/progress/catalogue integration and production/real-device checks. This package’s status is **ready-for-independent-check** only.


## Parent local correction — 2026-10-31

EG-EN-001: parent checked SparkNotes Chapter4 Launch, Summary (not speculative Analysis), the buckle assault/arm-grab/collision paragraph. The boy breaks his arm, not the wall. Only the ambiguous EN object is made explicit; RU is unchanged. This restores bilingual clarity using the same accountable event source; no complete primary chapter4 reading or new physical event is claimed.

Only embedded data/derived mode estimates and the matching connected manuscript(s) were refreshed. Outer code/styles and bespoke spoiler guards are byte-identical. Older segmentation generators are pre-correction preparation artifacts; the updated story-data.json is the maintained builder input. Original independent review remains unchanged; localized publisher validation is pending, not self-issued PASS.

Parent focused regression completed: 176 assertions across the four corrected readers, RU/EN and 320/390/768/1440 widths with light/dark representative cases. Exact changed copy, scroll tails, no horizontal overflow/runtime/network requests, saved-Deep warning, cancel and accepted restore passed. Ender uses browser confirm; the harness explicitly accepts/dismisses it. Failed harness diagnostic retained separately; no product-runtime correction was needed. Owned Chrome/profile cleaned. Per-reader structural result remains 69 passes. Not physical iPhone/PWA or new independent literary approval.
