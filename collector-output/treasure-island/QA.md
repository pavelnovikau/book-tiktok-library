# Treasure Island — editorial repair QA, 2026-10-31

Status: **ready-for-independent-check**. This document replaces the earlier green collector/cold reviews. Those reviews established neither the requested reading experience nor whole-book fidelity. No root integration, publication or deployment is claimed.

## Content reviewed and rebuilt

Read all **96 original RU/EN pairs**, including titles, body, cover and final. The original authoring JSON, collector HTML embedded corpus and published root HTML embedded corpus were compared; all screen content matched. Computed-mode-only metadata differences, where present, were not narrative divergence. This is 96 unique bilingual pairs, not a triple-count of identical copies.

All ordinary story bodies and framing were rewritten as an original condensed narrative: **34 pairs**, replacing 96. `contentMode: narrative`; `spoilerPolicy: full-plot-in-deep`; fresh defaults RU/dark/Essential. The final counts follow the connected story, not a fixed quota.

Removed reading lessons and analytical interludes. Rebuilt the inn, voyage, mutiny, stockade, coracle and treasure sequence as connected scenes; retained disclosure order for Ben’s work, the involuntary Hands shooting, the marooned men and Jim’s final nightmares. Did not invent Silver’s later fate.

Essential/Core stop after the stockade attack. Jim’s sea excursion, the treasure revelation, the mutiny outcome and homecoming remain in Deep. Original typographic 17— cover and its local island CSS; session-only spoiler dialog/navigation consent preserved from this book’s original runtime.

| Depth | Cumulative screens | RU / EN words | RU / EN estimated minutes |
|---|---:|---:|---|
| Essential | 12 | 582 / 696 | 4 минут / 4 min |
| Core | 20 | 947 / 1134 | 6 минут / 6 min |
| Deep | 34 | 1592 / 1897 | 9 минут / 9 min |

Words/minutes are the maintained builder's title/subtitle/body count and reading estimates, not tested completion times. Source maps remain in JSON and Sources; there is no academic provenance label after narrative screens.

## Evidence and substantive check

Robert Louis Stevenson, Treasure Island (1883), English novel, Project Gutenberg #120, I–XXXIV.

Complete lawful source retrieved privately. Chronological reading across the whole plot with close checks of retained incidents, not a claim of continuous every-paragraph reading or whole-book fidelity.

Essential introduces Black Dog as Bones’s associate, Ben’s hidden boat and the failed negotiations before the attack. A new resume regression was caught before readiness: the maintained cover expected an explicit spoilerPolicy. Adding full-plot-in-deep masks saved Deep titles; reload/consent was then retested. The shared final title is now neutral.

The complete source files/extracts remain in private audit storage outside this repository. New prose contains no copied chapters, modern translation, invented direct speech, scene or page reference. The source ledger maps the actual retained incidents. A local structural pass is not a literary fidelity certificate; the publisher must read every rebuilt pair and check supporting passages. No source-access block prevents independent checking of the represented plot. Residual limits:

- No continuous word-for-word reading of the complete English source is claimed.
- No particular Russian translation or uncertain future of Silver is certified.

## Local structural and browser checks

Built with the maintained `build_story.mjs`, then preserved the book-local consent behavior described below. The current generic structural audit returned **69 passes / 0 warnings / 0 failures**. Exact embedded data match the authoring JSON; only the generated `modes` metadata is added. Unique IDs, nested counts, bilingual copy/source fields, offline assets and font invariants passed.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/treasure-island/story-data.json --out collector-output/treasure-island/treasure-island.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/treasure-island/treasure-island.html --require-bilingual
```

**A plain rebuild needs the local consent restoration before delivery.** The private reproducibility script is `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/build_group.py`; it builds only these four packages and applies their small local changes. It does not edit the shared template. Do not treat an unpatched builder output as this checked candidate.

Final real Chrome/CDP matrix, local `file://`, network offline: both languages × both themes × all three depths, at both viewports. **528 visits** checked expected stable ID, exact rendered paragraphs and title, counter, document/slide width, header row, narrative-label suppression and text-bottom reachability.

| Viewport | Depth/language/theme combinations | Screen visits | Horizontal/document overflow | Max contained vertical scroll |
|---|---:|---:|---:|---:|
| 320 × 568 | 12 | 264 | 0 px | 351 px |
| 1440 × 900 | 12 | 264 | 0 px | 0 px |

The vertical scroll is intentional and contained inside the slide, especially on covers; this does not claim that every scene fits without scrolling. Desktop active rail entry stayed visible. The RU/dark mobile narrative and EN/light desktop narrative screenshots were visually inspected, along with a narrow bilingual consent dialog. Header controls are icons with localized accessible labels/tooltips; Home returns from collector preview to `../../index.html` and from root publication to `./`.

Additional interaction checks passed at both sizes: hidden Deep titles masked; hidden-Deep selection and Deep mode request consent; cancel retains position; keyboard cannot bypass a modal; lowering depth resets consent; saved Deep continuation reloads on a neutral cover, prompts again, then restores the exact ID; language/theme preserve position; start-over, arrows, Back and final Restart work; text tap enters focus with Next; swipe pages; vertical movement does not page/toggle; Escape restores chrome. Sources/Contents open and source counts fit. Offline fonts/images decoded, with zero runtime exceptions or external runtime requests.

Chrome used `timeout 30`, a unique temporary profile and owned-process-group cleanup on every run; profiles were removed, including failed preliminary runs. No server or Vite/HMR process was started. These checks use Chrome, not physical iPhone/Safari or an installed PWA. Parent owns the shared iPhone/PWA shell issue.

## Publisher integration requirements

- Keep `contentMode: narrative` and the maintained shell's corresponding label suppression.
- Update only through publisher-owned integration: counts/reading estimates changed from 24 / 60 / 96 to 12 / 20 / 34.
- Preserve the local `spoilerDialog`, session-only consent, masked contents, guards in `goToId`, `goToPosition` and `setMode`, and explicit spoiler policy used by neutral saved-position labels. Deep consent is reset on reload and on selecting a shorter mode. Hidden HTML JSON is not a secrecy/security boundary.
- Preserve the collector/root Home target handling. Also preserve the typographic 17— cover renderer and `.island*` CSS.
- Independent editorial review remains required. The ready manifest hashes all four canonical files and this detailed report; no catalogue, root reader, shared shell, git/PR/deploy or external messaging action was performed.

The authoritative delivery hashes are in `editorial-audit/2026-10-31/ready/treasure-island.json`, avoiding a circular self-hash here.


## Parent meaning corrections — 2026-10-31

Parent applied required independent meaning findings TI-REQ-01, TI-REQ-02 in RU and EN. Changed pairs: skeleton-pointer, silver-slips-away. Embedded data/derived reading estimates refreshed without replacing outer reader code or styles. This is a localized closure awaiting publisher validation, not a new independent PASS.
