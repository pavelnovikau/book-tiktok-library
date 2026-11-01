Current root personal acceptance2026-11-01:49/93/129screens;10644RU/11929EN body words; UI Deep63/58minutes. Exact accepted version and source/reading/QA limits: root-review/personal-review.md and personal-review.json. Historical implementation statements below are preserved; they do not describe the final hashes or grant broader source coverage.

---

# Selfie — implementation QA

Status: ready-for-root-personal-check. This is implementation self-review. `rootPersonalAcceptance=false`, `publicationAllowed=false`.

## Final artifact and text

The standalone `selfie.html` contains the complete bilingual data and offline fonts. It opens from `file://`; no content server or runtime remote requests are required. Defaults are RU / dark / Essential, with explanatory presentation. There is one source, a typographic cover and no supplied media. This nonfiction has no fictional-ending spoiler dialog.

The original connected Russian exposition was completed before English, and both preceded segmentation. Historical drafting hashes remain in `prose-first.json`; later continuity corrections and final hashes are distinguished there. The final connected drafts contain 192 body paragraphs each. Exact draft → JSON → embedded-data parity and six route-copy parity passed. `parity.json` binds their final hashes.

| Cumulative route | Screens, including cover/final | RU body words | EN body words | RU body minutes at 180 wpm | EN body minutes at 220 wpm | Displayed UI estimate RU / EN |
|---|---:|---:|---:|---:|---:|---|
| Essential | 48 | 4,077 | 4,568 | 22.65 | 4568/220 =20.763636… | 24 минуты /23 min |
| Core | 92 | 7,830 | 8,785 | 43.5 | 8785/220 =39.931818… | 47 минут /43 min |
| Deep | 128 | 10,764 | 12,077 | 59.8 | 12077/220 =54.895454… | 64 минуты /59 min |

The UI estimate means the reading time displayed by the reader. Its exact inputs are title + subtitle + body, including cover framing. It excludes section labels, Sources and repeated controls. The exact UI-time fractions are RU 4317/180,8284/180,11376/180 and EN 4866/220,9361/220,12843/220 for Essential/Core/Deep. The interface rounds upward. `metrics.json` separately records body, headings, cover framing, section labels and authored source/method disclosure words. The deterministic audit's aggregate `words` field is not a main-body metric.

Across 127 non-cover screens, RU body density is 47–148 words, median 84, mean 84.7559055; EN 53–167, median 96, mean 95.0944882. Counts follow the prose and natural paragraph breaks. No pilot screen count was copied. RU is 1,236 words below the 12k planning orientation (10.3%); actual, located omissions and compression are in the coverage map. Depth adequacy remains a root editorial decision.

## Actual reading and evidence

All 1,159 main paragraphs in 19 consecutive files `OPS/ch1-3.xhtml`–`OPS/ch1-21.xhtml` were displayed and read in order, together with metadata, acknowledgements and all 7 methodology paragraphs. Thirty bounded display chunks and exact paragraph/range hashes are in `reading-ledger.json`. The first chunk's initial clipping of `ch1-3 P021` was repaired by displaying that whole paragraph separately before its acknowledgement. This repair is explicitly recorded.

Notes were selective: `OPS/ch2.xhtml P045,111,113,131,141,223`. This is not a claim of continuous reading of all endnotes. No raw source extraction, copied chapters or long primary quotations were written into the deliverable. A mechanical normalised 20-token overlap check found zero exact overlaps between the supplied Russian paragraphs and the final original Russian body; this is not independent editorial or legal acceptance.

All six RU/EN routes were actually displayed and read as sequences in 24 bounded chunks. After two final context clarifications (Buller’s gang role and the post-war compromise), all six changed chunks were displayed and read again in full. Deep had already been read after those changes. `route-reading-ledger.json` preserves the original acknowledgements, six final reread acknowledgements, effective final chunk hashes and six final route hashes. The implementation reader is not root.

The map covers 64 units and has 94 checked locator ranges, argumentative functions and transitions. It also covers every main-spine file and names substantive omissions. `qa/record-verification.json` verifies source hashes, continuous paragraph order, map locators, final route-reading hashes, final content parity and the browser reports.

## Browser QA on the final hashes

| Chrome viewport | Final report | Rendered visits | Result |
|---|---|---:|---|
| 320×568 | `qa/browser-320.json` | 2,144 | PASS |
| 390×844 | `qa/browser-390.json` | 2,144 | PASS |
| 1024×768 | `qa/browser-1024.json` | 2,144 | PASS |
| 1440×900 | `qa/browser-1440.json` | 2,144 | PASS |
| Emulated iPhone 390×844 | `qa/browser-ios-390.json` | 2,144 | PASS |

Each run traversed every visible screen in each exact route, both languages, dark/light and Sans/Serif: `(48+92+128)×2×2×2=2144`. All 10,720 rendered visits checked actual titles and paragraph text, route counts, horizontal bounds and visibility of the last paragraph after scrolling to the bottom. There were no runtime exceptions, remote requests or traversal failures. The final HTML SHA256 is `6b68e7d860173198f71a7da7db5e56321ac35e4d3d3f64bd1a7b18453a35c605`.

The 320 cold run confirmed both Serif faces were unloaded before the first real Settings switch. It began on `debbie` at scrollTop 110 and counter 2/48; after selecting Serif and waiting for font completion, the same ID, counter and exact 110 px position remained. Native Chrome arrow-key events changed Theme and Reading font radio selections; Tab stayed inside the modal, and Escape returned focus to the gear. Platform-font records show custom Geist Sans, actual Source Serif 4 for Russian Serif and actual Geist Serif for English Serif. The Settings note accurately names the Cyrillic fallback.

Other checks cover icon-only labeled single-row controls, Sources/method, Contents, desktop rail synchronisation, language-position preservation, keyboard/buttons, focus paging and Escape. Native Chrome mouse input verified tap-to-enter/exit focus, a 650 ms long press that did not toggle focus, and actual text selection without paging or focus changes. The iPhone emulation additionally used native CDP touch events for taps, horizontal paging and vertical scrolling without paging/focus. Synthetic pointer-direction checks are recorded separately; they are not represented as hardware touch testing.

Real page reloads preserved saved Deep progress, then preserved a lowered Essential selection. The deeper Continue action visibly named «Глубоко» /Deep while retaining 48 Essential screens until clicked. Explicit continuation resumed the exact saved Deep ID. Start over respected the lower depth. A fixture seeded the actual old collector ID `rocket-in-fog` under the real legacy key names; the new depth-v2 reader ignored it and left the old keys untouched. This tests a real legacy ID and key contract, not the user's existing browser profile.

The emulated iPhone run checked 44 px top /34 px bottom insets, RU auto-install guidance, EN manual guidance and the emulated standalone flag. This is Chrome emulation, not physical Safari, iPhone or installed-PWA acceptance. Home retains the shell's `./` integration contract; no root catalogue was created or changed.

Five final screenshots were personally inspected: 320 dense RU/light/Serif, 390 cover RU/dark/Sans, 1024 reportage EN/dark/Serif, 1440 final RU/dark/Serif, and emulated-iPhone dense RU/light/Serif. Typography, paragraph layout, the compact header and desktop rail were legible. The first small-width build exposed a long-heading overflow; the local candidate's heading wrap fixes it. No shared shell was edited. List/image/comparison layouts are not applicable to this prose-only candidate.

The maintained deterministic audit passed 69 checks with zero warnings and failures (`qa/static-audit.json`). The maintained builder and installed assets were used read-only. Each Chrome run owned a unique `mktemp` profile and a `timeout 30` process group. Every `finally` cleanup reports profile removed and zero surviving owned PIDs. No Vite/HMR or content server was started.

## Boundaries

The text-only Russian source establishes neither image/diagram coverage nor a full official-English comparison. Supplied metadata establishes the Russian title and copyright 2017/Individuum Print 2019; it does not establish a translator credit. Storr’s secondary-source and edited-interview method, specialist-review limits, acknowledged bias and scientific disputes remain disclosed. No present-day scientific validation or independent editorial review was performed.

Root must personally read the final connected RU/EN expositions, all six exact routes, the coverage/omissions map and selected actual primary passages before any publication. Structural/browser passes do not grant that acceptance.
