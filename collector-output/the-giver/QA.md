# The Giver — local implementation QA

Status: **ready for independent content check**. The checks below verify this collector package’s structure and reader behaviour. They are not a literary PASS or publication approval.

## Corpus actually checked

- New approved title; no earlier `the-giver` collector corpus or root reader was found. Old pairs read: **0**.
- Written and read: **27 unique RU/EN pairs**, comprising 25 narrative scene pairs, a cover and shared final framing. Both languages of every effective embedded screen were read and compared with the canonical JSON. Essential/Core were also read as continuous sequences; Deep was read in its full order.
- Exact cumulative counts: **Essential 11, Core 17, Deep 27**, including cover/final. Level distribution: **11 / 6 / 10**. Nested sets grow strictly.
- Builder word totals (title/subtitle/body): Essential **374 RU / 458 EN**, Core **581 / 708**, Deep **922 / 1129**. Computed reading labels: **3 / 4 / 6 minutes** in each language. Narrative bodies average about **32 RU / 39 EN words**, range **15–41 RU / 21–57 EN**.
- `contentMode: narrative`; fresh **RU / dark / Essential**. Five source records. No media/cover image. Screens use original concise prose, not a published-translation claim.

## Reproducible local build/checks

From the shared library root:

```sh
python3 collector-output/the-giver/author-story.py
node collector-output/the-giver/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/the-giver/the-giver.html --min-screens 27 --require-bilingual
node collector-output/the-giver/qa-giver.mjs 320 568 matrix
node collector-output/the-giver/qa-giver.mjs 390 844 matrix
node collector-output/the-giver/qa-giver.mjs 1024 768 matrix
node collector-output/the-giver/qa-giver.mjs 1440 900 matrix
node collector-output/the-giver/qa-giver.mjs 320 568 behaviour
node collector-output/the-giver/qa-giver.mjs 1440 900 behaviour
node collector-output/the-giver/qa-giver.mjs 390 844 ios
```

The authoring script segments the existing connected manuscript. The local build calls the maintained v2 builder, then applies only book-local consent and narrative-cover additions. It fails if expected maintained-shell anchors have changed. Do not replace it with a copied reader or run repository-wide sync for this package.

The deterministic audit returned **69 structural passes, zero failures, zero warnings**. `qa/consistency.json` proves canonical fields/screens/sources equal the effective HTML data, checks nested IDs and Deep-only reveal screens. `qa/build.json` records builder/template/header hashes and the final HTML hash. Browser report hashes must match that final HTML.

## Browser/offline/mobile coverage

Real headless Chrome, local `file:` document, network emulated offline; no server. Each invocation uses `timeout 30`, its own `mktemp -d` profile, a dedicated debugging port, an internal 29-second cleanup deadline, full owned-process-group termination and profile removal in `finally`.

All screens were traversed and exact rendered title/body compared at **320×568, 390×844, 1024×768, 1440×900**, each across 3 depths × RU/EN × dark/light. This is **48 matrix cases / 880 screen renders**, not 880 distinct texts read. All cases passed: exact counts, correct ID/position, full body equality, no horizontal overflow, reachable text/action after vertical scrolling and no narrative provenance chrome. Desktop rail visibility/active item were checked at 1024/1440. Embedded fonts loaded offline. Zero unexplained runtime exceptions or external runtime requests.

Representative screenshots were visually inspected: phone cover/controls, RU dark and EN light prose, desktop prose/rail, Sources, spoiler warning and shared final. There are no list/image/comparison screens to pretend to have checked. The 320px cover scrolls; its Start control remains reachable. One icon-only header row stays inside the viewport.

Behaviour checks cover:

- Cover Deep selector, Contents Deep item, desktop Deep item and dialog mode selector require this book’s explicit consent. Cancel/Escape preserve the current screen and depth. Keyboard paging cannot bypass the modal.
- Every Deep title is masked before consent. Reloading with saved Deep opens the cover in Essential with the generic **Continue Deep — ending spoilers** label. Continue asks again, then restores the saved Deep ID. Downgrading revokes consent.
- Core chapter navigation raises depth; language/theme/rapid switching preserve ID and depth. Sources and Contents open/close. Home retains `href="./"`.
- Start over, Next/Back, ArrowRight, swipe and final restart work. Final restart clears remembered screen. Tap/F toggle focus; Next remains visible. Escape restores chrome. Vertical movement does not toggle focus or page.
- Emulated iPhone Safari opens/localises/closes the install guide; six header controls fit below an actual engine **47px** safe-area inset. Focus hides the install UI. Emulated standalone suppresses it. This is not a physical iPhone/PWA result.

One added QA check initially failed to close the native dialog because its synthetic CDP Escape lacked native key metadata. The harness now sends Escape with virtual/native key code 27 and allows the native close task to run. The route then passed without changing reader behaviour.

## Evidence, spoiler and remaining limits

See `sources.md` and `source-evidence-map.json`. No full novel was read continuously. The primary passages actually consulted are selected authorised excerpts from chapters 9, 13, 16 and 20; remaining retained actions are explicitly mapped to substantial official guides, with author material used to preserve ending ambiguity. Full-book fidelity is not inferred from a fetch or this technical audit.

Essential/Core stop before the recording is shown. The decisive mechanisms, ensuing action and last scene are level 3. Cover, common final, pre-consent contents, generic saved-Deep label and global source/method notes do not disclose those outcomes. External source links carry a spoiler notice. The last scene is not resolved with a film or later-book outcome.

The separate Settings/Geist worker’s unmerged code was not copied; no shared settings/font changes were implemented. Existing maintained builder fonts/header were used. Publisher must apply accepted shared UI and recheck resulting integration. Glyph-by-glyph font coverage and physical-device PWA behaviour are not certified here.

No root reader, catalogue, index, shared shell/skill, shared log, Git, PR, deploy or external messaging operation was performed. Independent content acceptance and production integration remain with the parent/publisher.


## Parent correction of independent findings — 2026-10-31

GIV-001: parent directly checked the Scholastic BookFiles official guide, printed pp. 24 and 42 (zero-based PDF 23 and 41), apple during catch and Jonas’s recollection. Removed only the unsupported in-hand placement in RU/EN; did not replace it with an in-air detail from memory. Chapter 3 of the primary novel was not read for this correction. The source-evidence-map limit now makes this exact boundary explicit.

Only the embedded data/derived reading estimates changed. Outer reader runtime/styles and unrelated pairs remain byte-identical. Focused browser verification is pending. Original independent reviews remain unchanged; this is not a new independent PASS or a publication claim.

Parent focused browser regression: passed across 320/390/768/1440 px, RU/EN and both themes. Exact changed copy, complete body-tail reachability, zero horizontal overflow/runtime exceptions/remote requests; Behave added source links and scope notes visible; both fictional saved-Deep covers conceal late titles and warn explicitly; The Giver renews consent on downgrade/reload and cancellation retains Essential. Combined report: 160 assertions. Owned Chrome process/profile removed. Not physical iPhone/PWA or a new independent literary PASS.


## Parent metadata correction CM-01 — 2026-10-31

Description now identifies the first novel in Lowry’s cycle, removing the author-debut claim. All27 RU/EN screen pairs, sources and runtime/consent/Settings code are unchanged; only description metadata and initial RU meta tag changed. Independent catalogue reviewer checked the author biography; parent repeat fetch timed out, no fresh direct biography reading claimed. Original reviews and release07 receipt remain historical; next publisher validates integration.
