# Howl’s Moving Castle — Sol implementation handoff

2026-10-31. Assigned slug: `howls-moving-castle`. New approved queued work, not an audit of an existing published reader. Implementation verdict: **REBUILD / new faithful narrative package**. Publication state: **ready-for-independent-check**, subject to the exact hashes in the ready record. No independent PASS is asserted.

## Delivered

Canonical files, all under `collector-output/howls-moving-castle/`:

1. `story-data.json`
2. `howls-moving-castle.html`
3. `sources.md`
4. `QA.md`

Supporting files are confined to the same collector (continuous prose draft, segmentation script, local build wrapper, original SVG cover, scoped QA script/reports/screenshots). The substantive evidence map is `editorial-audit/2026-10-31/books/howls-moving-castle-sol-implementation-evidence.md`. The machine-readable handoff is `editorial-audit/2026-10-31/ready/howls-moving-castle.json`.

## Result and actual reading

The retelling uses Jones’s **1986 novel**, with connected original RU/EN prose rather than a management/psychology companion. It retains the sisters’ exchange, Sophie’s bargain and active interference, Howl’s vanity and kindness, Michael’s attachments, Calcifer’s complaints and restrictions, Donne’s curse, the tutor/King episodes, the move, and the late causal chain. No invented scene, dialogue, moral, exercise, film-war plot or sequel material is introduced.

The prose was written continuously before division and mode assignment. Exact resulting counts are **15 / 25 / 39**, including cover/final; estimated reading time **5 / 8 / 13 minutes** in each language. No historic total existed for this slug and no quota was padded. **0 old pairs** existed. The implementer read **39 final RU/EN pairs**, separately followed the nested Essential/Core/Deep routes, and checked actual embedded JSON equality against authoring data.

Essential and Core pause after the flower-shop move. All 14 late-answer screens are level 3. A book-local localized dialog guards Deep selection and saved hidden-ID resume; consent is fresh each document session. Shallow contents never expose late titles, and the cover’s saved-Deep label is generic. The shared final/source notes stay spoiler-safe. Narrative presentation keeps sources in the accessible global dialog.

## Evidence, with an honest boundary

Apple Books title/author metadata search inspected **216 expanded EPUBs / 216 OPFs**, with no assigned-title match or OPF parse failure. No candidate spine/body could be verified; this is not an assertion about all aliases, PDFs or storage locations, and no unrelated filename is exposed.

The legal HarperCollins sample on Litres identifies ISBN **9780007380459**; the accessible opening was read. Indexed library bibliography confirms the original 1986 novel/reprint distinction; direct opening returned 403. The rest of the retained story is backed by substantial public chapter-event guides, a second late-chapter guide, and selectively read actual Jones passages quoted in the guides. Those roles are separated in the ledger and map. No locked content was bypassed, no unofficial full text was sought, and no private full text was saved.

Primary anchors include the opening hats/family/May Day material, hearth restrictions, Calcifer’s account of the bargain, Howl’s stated attempts at lifting Sophie’s spell, the stick rescue, Howl taking the Witch’s heart and Calcifer’s voluntary return. Detailed guides support the exact heart-separation/body-restoration sequence and the fortress/wind chain. These are not relabelled as primary continuous reading. The source map also records a compressed secondary-entry attribution that was rejected in favour of the corroborated chapter-event sequence.

No presently identified essential retained link lacks an accountable locator within this scope. Full-edition fidelity, omitted side episodes, exact pagination and comparison with a published Russian translation remain unverified. A complete edition was **not** read continuously; there is **no translation certificate**.

## Concrete implementation corrections

- Move the castle-entry bridge to level 1 so Essential does not jump from departure to an unexplained interior.
- Make Angorian the explicit object of Sophie’s belief about Howl’s love in RU/EN; remove the ambiguous English “her.”
- Remove the Essential-only reference to an as-yet unintroduced household dog during the sea-duel return.
- Attribute the possible danger of demon control to Pentstemmon instead of implying an inevitable fatal rule.
- Correct the chapter-11 source-ID offset on Wales/teacher/poem screens.
- Replace administrative cover-credit wording with author/year.

Exact draft wording, fixes and source locations are in the evidence map.

## Validation and remaining work

The maintained builder and deterministic audit passed **69 structure checks, zero warnings/failures**. Scoped offline Chrome checks traversed **1,264 route positions** across four viewports, both themes/languages and all modes; final phase reports show zero runtime errors or HTTP(S) runtime requests. They additionally verify dialogs, embedded assets, compact header, Deep cancel/accept/resume, saved IDs, focus/taps, keyboard/swipe, restart, rail and emulated iOS/safe-area behaviour. All Chrome processes/profiles were owned, bounded by `timeout 30` and cleaned; no server was started.

Unresolved limits: independent content review is still required; complete-edition/translation scope remains limited; physical iPhone/PWA and production integration are publisher checks. No root reader, catalogue/index, shared shell, installed skill, root log, Git/PR/deploy or external message was touched. Settings PR 29 was left alone.
