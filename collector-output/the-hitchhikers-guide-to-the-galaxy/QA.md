> **2026-10-31 narrative pass 2: REBUILD delivered for independent check.** Current package is narrative 11/18/36 with maintained Settings and preserved custom spoiler/state guards. See the dated current record at the end; prior approvals/source-gap notices below are historical. No independent PASS or publication is claimed.

> **2026-10-31 targeted acquisition update:** newly read Salem Press publisher-sample first-novel account supports the Ford → Vogon → Heart of Gold chain. SOURCE-GAP is now specifically Magrathea approach/brain-threat/physical escape links, not an automatic no-full-EPUB verdict. Pan ISBN 9781529034523's endpoint returned a generic homepage, not novel text. See [new evidence map](../../editorial-audit/2026-10-31/source-rescue/the-hitchhikers-guide-to-the-galaxy.md). No rewrite, ready manifest or independent approval.

> **2026-10-31 corrected editorial audit: REBUILD / SOURCE-GAP; NOT READY.** All 96 RU/EN pairs and the effective root corpus were reviewed. Earlier analytical-companion approval below is historical and superseded. Complete first-novel primary access is still required; see `../../editorial-audit/2026-10-31/books/the-hitchhikers-guide-to-the-galaxy.md`. No new fidelity approval is claimed.

# The Hitchhiker’s Guide to the Galaxy — collector QA

Date: 2026-10-31. **Implementation/self-QA complete; ready for the parent’s cold editorial review.** This is not an independent editorial verdict or a publication approval.

## Deliverables and boundaries

Exactly four canonical files in this collector directory:

- `story-data.json`: schema-v2 original bilingual analytical corpus.
- `the-hitchhikers-guide-to-the-galaxy.html`: standalone reader, 391,762 bytes.
- `sources.md`: evidence boundary, map recorded before drafting, eight-source ledger and 96 per-screen locators.
- `QA.md`: this implementation/self-QA report.

Only this collector’s four files were created or edited. No child agent or other model was used. No catalogue, root reader, shared template/script, git operation, commit, PR, deployment, external delivery or message to another person was performed. Catalogue integration and independent cold review belong to the parent’s next stage.

## Exact corpus and density

Cumulative counts include the cover and final, both level 1. There are 24 level-1, 36 level-2 and 36 level-3 screens. Essential is a nested subset of Core, which is a nested subset of Deep, in one stable ordered corpus.

| Mode | Screens | RU words | RU estimate | EN words | EN estimate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 24 | 1,211 | 7 min | 1,406 | 7 min |
| Core | 60 | 3,043 | 17 min | 3,537 | 17 min |
| Deep | 96 | 4,854 | 27 min | 5,712 | 26 min |

Counts use the current builder’s Unicode word rule on titles, cover subtitle and bodies. They exclude interface labels, section labels, method/source notes. The deterministic auditor excludes the cover subtitle and therefore reports 4,848 RU / 5,706 EN. Reading estimates use the maintained 180 RU / 220 EN words per minute rule, rounded up; reflective or aloud reading takes longer.

Body-only density: RU **41–50**, mean **44.71**, total **4,292** words; EN **49–56**, mean **52.08**, total **5,000** words. Every body falls inside the requested roughly 35–75 range. EN title/subtitle/body total is 17.7% longer; manual self-review compared claims, quantities, qualifications and spoiler levels rather than equalizing lengths mechanically.

Eight sources. Assigned provenance: 13 reported book-event/image screens, 8 corroboration/context screens, 75 synthesis screens (including the cover and final). This is deliberately an analytical digest, with reading tools and interpretations distinguished from event evidence. All 96 screens carry source IDs and a claim-level locator shared by RU/EN; every ID resolves. No media files or publisher imagery are included. The cover is original typography.

## Evidence boundary and editorial scope

The first novel (1979) is the work being analysed. Public edition identity: [Del Rey, ISBN 9780345418913, 1997](https://penguinrandomhousesecondaryeducation.com/book/?isbn=9780345418913). No private edition is claimed. No private filesystem path appears in the HTML or source identity.

The complete novel was **not read**, acquired or downloaded. Consulted material consists of the publisher’s lawful Chapter One excerpt/metadata, Adams’s public introductory essay and interview, publisher series guidance, an institutional teaching unit, the open Kropf abstract, substantial Woodford criticism with accompanying event/character reference sections, and Gaiman’s personal reminiscence. The omnibus-hosted source contributes only Adams’s introductory essay, not the omnibus narrative. The full Kropf article and paywalled Nature review were not read or relied on. Unauthorized full-book PDF results were ignored; no borrowing/access control was bypassed.

The prior map and ledger support a bounded original analytical reading, **not** edition-complete or page-by-page fidelity. Late event evidence is secondary, chiefly sources 5 and 7; details without that support were not reconstructed. Particular facts available only in source 7 (for example missile transformations, Zaphod’s brain mystery and Marvin’s role in the final escape) are attached to its specific section, not presented as direct full-text observation. Source 7’s substantial Woodford essay supplies the interpretive dispute; the overall argument was not derived solely from its plot synopsis. The opening analysis is grounded in the publisher’s actual excerpt, and Adams’s interview challenges reducing the work to genre parody.

No invented novel page/chapter references, verbatim narrative/dialogue, poem text, reconstructed internal monologue, published Russian translation or official artwork is supplied. Technical devices are explicitly treated as fiction. The vacuum episode supplies no real survival countdown or breathing advice. Comic drinking is not promoted. The guard’s coercion, the mice’s demand and the machine self-destruction joke are bounded fictional material; the latter is not represented as real mental-health causation or advice.

Essential invites reading the novel without its ending, numerical answer, Earth-computer revelation, mice’s identity/demand or Magrathea resolution. Core adds early episodes, characters and Magrathea’s planet-making premise while withholding those decisive revelations and the outcome. Deep includes an explicit warning screen before its later revelations and a warning dialog before the mode exposes its contents/title list. The sourced ending is narrowly stated: escape from the mice/police danger, Marvin’s attributed causal role, return to the ship and departure towards the restaurant. The restaurant visit and later instalments are excluded.

## Build and book-local HTML changes

Built from `story-data.json` through **the current `skills/book-tiktok/scripts/build_story.mjs`** and its maintained standalone template. The source JSON screens and parsed embedded HTML screens are equal. Default fresh state: Russian, dark, Essential. Embedded Geist and Geist Mono load offline. The quiet Flexoki cyan action treatment is inherited from the maintained shell.

Book-local post-build changes in the owned HTML only:

- Original compact typographic cover and fiction-appropriate provenance labels.
- Accessible session-scoped Core/Deep consent dialog. Cancel/Escape retain the previous depth; a new session starts in Essential. Restoring a hidden saved position asks for the required consent before raising depth. Saved-position copy never exposes a Deep title.
- Focus cover hides its visual and retains title/body and safe Next. Focus also hides inline source chrome; the full source panel remains available after leaving focus.
- iOS install trigger is placed as a static header control, preserving the guide but preventing the original fixed control from intercepting the language button. Focus hides the header and trigger. This repair passed actual pointer clicking in iPhone emulation at both 320 and 390 widths.
- Accessible dialog names and reduced-motion handling.

**Rebuild limitation:** a plain builder invocation recreates the common shell and corpus but does not recreate these book-local HTML additions. Preserve/reapply them during later integration or rebuilding. No shared shell was changed within this commission.

## Deterministic audit

Command run against the final HTML:

`node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/the-hitchhikers-guide-to-the-galaxy/the-hitchhikers-guide-to-the-galaxy.html --min-screens 96 --require-bilingual`

Result: **68 passes, 0 warnings, 0 failures**. Counts, targets, stable IDs, both languages, valid sources, cover/final placement, offline invariants, responsive hooks and Flexoki checks pass. No runtime fetch/XHR/WebSocket/EventSource/service-worker dependency, remote script/style, private path or evidence-book file is present. Sources are optional outward navigation.

## Real-browser matrix

Native headless Google Chrome controlled with local Playwright over an isolated CDP connection. The actual standalone artifact was opened through `file://`, with browser context offline and HTTP/HTTPS attempts monitored. No content server or `preview_*` tool was used.

| Viewport | Themes | Languages / modes | Screen-state visits | Result |
| --- | --- | --- | ---: | --- |
| 320 × 568 | dark + light | RU/EN; Essential/Core/Deep | 1,440 | PASS |
| 390 × 844 | dark + light | RU/EN; Essential/Core/Deep | 1,440 | PASS |
| 1024 × 768 | dark + light | RU/EN; Essential/Core/Deep | 1,440 | PASS |
| 1440 × 900 | dark + light | RU/EN; Essential/Core/Deep | 1,440 | PASS |

Total **5,760** visits: each visible screen in each mode/language/theme, both normal and focus. Checks assert exact localized title, counter/index and mode count; no document or reading-region horizontal overflow; no outer-page vertical overflow; visible content; stable theme; bounded top controls; expected desktop rail and active item. Focus checks assert hidden header/rail/back/counter/citations, visible text and a Next target at least 44px inside viewport bounds, including the cover. Longer content scrolls within the reader, as intended.

Both embedded fonts loaded. Across successful matrix and functional runs: **0 page exceptions, 0 console errors, 0 attempted HTTP/HTTPS runtime requests**. There are no embedded images to decode.

## Functional and iOS checks

**38 functional assertions at 390 × 844 plus 38 at 1440 × 900** passed:

- Core/Deep warnings; cancellation by button/Escape; correct counts after acceptance.
- Next/Back, chapter selection, arrows, PageUp, body Space and pointer swipe.
- **Space on focused Next and Back activates exactly once**; Space on language preserves position.
- **F and Escape work after clicking Next**, including when Next retains keyboard focus.
- Tap/second tap toggle focus; it survives paging; horizontal swipe and vertical drag do not become focus taps.
- Theme/language preserve stable position; Sources and Chapters open and close; all eight source links and the explicit full-text disclosure appear.
- Saved Deep state reopens safely in Essential; generic Continue copy; restoring a hidden saved target prompts consent and raises mode only after acceptance.
- Final Restart clears the bookmark; focus on cover hides the typographic visual, shows text and Next, and Next advances.
- Home retains the required `href="./"`. Catalogue navigation from a promoted root reader is not claimed/tested, because root integration is outside this collector’s ownership.

**8 additional assertions at 390 × 844** passed: actual emulated touchscreen tap/second tap; ignored long press and non-empty text selection; native Space on Sources/Chapters opens their dialogs without advancing; rapid RU/EN/theme switches preserve position; Start over ignores the bookmark.

**14 iOS/standalone assertions** passed: six each at 320 × 568 and 390 × 844 in iPhone browser emulation, plus two for installed mode. The guide opens once, includes the RU and EN Share / Add to Home Screen route, closes, remains manually available, and is suppressed in focus. `navigator.standalone` emulation suppresses both guide and trigger. The maintained copy explains the need to relaunch from the Home Screen rather than Telegram and does not promise that an ordinary Safari page can remove browser chrome.

This is **Chromium emulation**, not physical iPhone/iPad, actual Safari, or hosted installation testing. File portability/offline rendering is tested; hosted PWA/catalogue integration and deployment are not.

## Visual self-inspection

Inspected stable screenshots of cover, prose/provenance, English final and spoiler dialog at 320 dark, 390 light, 1024 dark and 1440 light; also inspected focus covers at 320 and 1024. The small-phone cover was compacted so its title appears before the decorative panel can dominate the viewport. Focus cover fits text and Next. Desktop rail remains readable and synchronized; mobile long text remains scrollable above navigation. No clipped horizontal text or inaccessible Next target appeared in the inspected frames.

There are no standalone documentary images, quantitative plots, comparison grids or long-list screens, so those optional visual categories are inapplicable. Screenshots verify presentation, not the historical/literary truth of the content. Independent editorial challenge remains the next stage.

## Cleanup

Every Chrome launch used `/usr/bin/timeout 30`, a unique temporary profile and Chrome-assigned unique debugging port. Browser contexts/connections were closed and process groups terminated in `finally` on success and failure. One profile recreated preferences during shutdown; after confirming no owned Chrome process remained it was removed. Final cleanup verifies zero owned Chrome processes and zero remaining owned temporary profiles. Scratch research extracts, scripts, screenshots and raw QA reports outside the repository were removed; no book source files are in the deliverables. Exactly the four canonical files remain.

---

## 2026-10-31 narrative pass 2 — current record
Status: **ready-for-independent-check**, not an independent PASS, approval to publish, full-novel read or universal fidelity claim. Earlier analytical-companion QA is preserved above and superseded.

### Content and build

- Re-read all **96 original RU/EN pairs** and the effective root corpus; intake screens matched collector/JSON. Read **36 new pairs** and the three ordered modes after writing connected prose. All new embedded screens and source objects match canonical JSON.
- A real narrative replacement: 33 story beats and cover/warning/final framing. Old lessons, exercises, role-label discussions and critic-debate screens are removed. Actual events and comic causality carry the sequence. Exact new counts were derived after prose, not padded to the old 24/60/96 targets.
- Preserved this book's custom runtime, typographic cover and spoiler/hidden-bookmark behavior, inside the installed builder's current validated data, offline fonts, Settings, header and focus shell. Book-local adapter: `pass2/build-narrative.mjs`. The installed skill was read-only. No root/shared synchronization run.
- Strengthened downgrade and page-restoration revocation, invalidated removed old saved IDs safely. Core and Deep require real consent before exposing their content. Generic Continue reveals no saved Deep title. Numeric answer, late Earth/brain and escape outcomes remain level 3; shared final, cover, shallower contents and global source notes are safe.

| Mode | Cumulative screens | RU words | EN words | RU / EN minutes |
| --- | ---: | ---: | ---: | ---: |
| Essential | 11 | 465 | 560 | 3 / 3 |
| Core | 18 | 730 | 888 | 5 / 5 |
| Deep | 36 | 1470 | 1774 | 9 / 9 |

Word totals follow the maintained builder (title, subtitle, body; not source notes/UI). Body density: RU 23–48 words, mean 37.53; EN 25–56, mean 45.11. Defaults RU / dark / Essential / Sans. Five active evidence sources. No count quota was used.

### Meaningful technical checks on final HTML

[Structured audit](pass2/structure.json): **69 passes, zero warnings/failures**. [Combined receipt](pass2/validation.json) records final authoring/HTML SHA-256, source parity and all proof hashes.

[Browser matrix](pass2/browser-matrix.json): **1,040 screen-state visits**, all 11/18/36 screens × RU/EN × dark/light × 320×568, 390×844, 1024×768, 1440×900. Checked actual body strings, final body-character reachability, exact mode counts, no horizontal overflow, synchronized desktop active rail, and compact labelled icon row. Source footnote/provenance chrome is absent in narrative. [320 cover](pass2/cover-320.png), [320 Deep prose](pass2/deep-320.png), [1440 cover](pass2/cover-1440.png), [1440 Deep prose](pass2/deep-1440.png) visually inspected after completing entrance animations; early transitional captures were replaced.

[Consent/state](pass2/browser-consent.json): **17 checks** of Core/Deep picker gates, contents-origin entry, Cancel, native Escape, downgrade, a retained hidden-navigation handler, saved Core/Deep Continue, neutral resume labels, reload, removed legacy IDs, bilingual position preservation, spoiler-safe global Sources and simulated restored-page consent revocation.

[Interactions](pass2/browser-interaction.json): **15 checks**, including Settings without position/depth loss, close-event focus return, four actual offline fonts, Cyrillic Serif fallback and Sans UI, real text tap, paging in focus, Escape, touch swipe, vertical movement without false tap/page, keyboard paging, final restart, preferences after reload, desktop cover/rail focus and restoration.

[iOS emulation](pass2/browser-ios.json): **5 checks**: manual install guide, localization, all six controls in one row at 320, simulated nonzero top padding, `navigator.standalone` suppression. This is Chrome emulation; physical iPhone Safari/PWA and actual OS safe-area behavior remain untested.

Each browser phase used `file://`, CDP offline mode, zero HTTP(S) page requests and zero runtime exceptions. No content server or `preview_*` tool. Every Chrome was bounded with `timeout 30`, owned unique `mktemp -d` profile, detached-process-group cleanup and profile removal on success/failure. Final process check found no owned Chrome left. Receipts: `pass2/cleanup-*.json`. Root reader still matches intake SHA; no Git/PR/deploy/external messages/subagents or root/catalogue/shared-shell/installed-skill/log edits.

### Source and editorial limits

New primary quotations were read **inside** named commentary, not complete later novel chapters. Some connective actions rest on detailed professional narration cross-checked against Gale/Salem and selected quotations. See the exact [source-rescue report](../../editorial-audit/2026-10-31/source-rescue/the-hitchhikers-guide-to-the-galaxy-pass2.md), not historical QA as authority. The parent must freshly read the 36 pairs, the sequence and source evidence. Only after independent approval may the publisher integrate/publish the matching hashes.
