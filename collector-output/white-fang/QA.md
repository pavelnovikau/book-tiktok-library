# White Fang — editorial repair QA, 2026-10-31

Status: **ready-for-independent-check**. This document replaces the earlier green collector/cold reviews. Those reviews established neither the requested reading experience nor whole-book fidelity. No root integration, publication or deployment is claimed.

## Content reviewed and rebuilt

Read all **96 original RU/EN pairs**, including titles, body, cover and final. The original authoring JSON, collector HTML embedded corpus and published root HTML embedded corpus were compared; all screen content matched. Computed-mode-only metadata differences, where present, were not narrative divergence. This is 96 unique bilingual pairs, not a triple-count of identical copies.

All ordinary story bodies and framing were rewritten as an original condensed narrative: **36 pairs**, replacing 96. `contentMode: narrative`; `spoilerPolicy: full-plot-in-deep`; fresh defaults RU/dark/Essential. The final counts follow the connected story, not a fixed quota.

Rebuilt the sled pursuit, den, camp, persecution, sale, cage, Scott relationship and southern ending as the animal’s life. Retained Bill’s offscreen death, the lynx fight, White Fang’s violence, Scott’s blows during chicken training, the judge’s ignorance of Hall’s wrongful last conviction and the puppy ending. No training advice, scientific claim or instant-gratitude rescue was added.

Essential/Core stop before the decisive bulldog fight. The intervention, developing attachment, southern home and Hall ending remain in Deep. Original geometric trail image, with neutral descriptive alt text and a short Smartcat credit.

| Depth | Cumulative screens | RU / EN words | RU / EN estimated minutes |
|---|---:|---:|---|
| Essential | 14 | 640 / 775 | 4 минут / 4 min |
| Core | 21 | 975 / 1155 | 6 минут / 6 min |
| Deep | 36 | 1698 / 1974 | 10 минут / 9 min |

Words/minutes are the maintained builder's title/subtitle/body count and reading estimates, not tested completion times. Source maps remain in JSON and Sources; there is no academic provenance label after narrative screens.

## Evidence and substantive check

Jack London, White Fang (1906), English novel, Project Gutenberg #910, Parts I–V.

Complete lawful source retrieved privately. Chronological narrative runs spanning all five parts and close checks of retained incidents; no claim of continuous every-paragraph reading or whole-book fidelity.

The shorter route explicitly reports Henry’s rescue when the longer fire scene is omitted. Primary IV.VI corrected a new unsupported throat-touch detail to the actual head-hiding gesture before readiness. The repeated gesture was condensed, and the shared final title made neutral.

The complete source files/extracts remain in private audit storage outside this repository. New prose contains no copied chapters, modern translation, invented direct speech, scene or page reference. The source ledger maps the actual retained incidents. A local structural pass is not a literary fidelity certificate; the publisher must read every rebuilt pair and check supporting passages. No source-access block prevents independent checking of the represented plot. Residual limits:

- No continuous word-for-word reading of the complete English source is claimed.
- London’s attributed animal experience is literature, not validation of modern animal behaviour or handling.
- No particular Russian translation is certified.

## Local structural and browser checks

Built with the maintained `build_story.mjs`, then preserved the book-local consent behavior described below. The current generic structural audit returned **69 passes / 0 warnings / 0 failures**. Exact embedded data match the authoring JSON; only the generated `modes` metadata is added. Unique IDs, nested counts, bilingual copy/source fields, offline assets and font invariants passed.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/white-fang/story-data.json --out collector-output/white-fang/white-fang.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/white-fang/white-fang.html --require-bilingual
```

**A plain rebuild needs the local consent restoration before delivery.** The private reproducibility script is `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/build_group.py`; it builds only these four packages and applies their small local changes. It does not edit the shared template. Do not treat an unpatched builder output as this checked candidate.

Final real Chrome/CDP matrix, local `file://`, network offline: both languages × both themes × all three depths, at both viewports. **568 visits** checked expected stable ID, exact rendered paragraphs and title, counter, document/slide width, header row, narrative-label suppression and text-bottom reachability.

| Viewport | Depth/language/theme combinations | Screen visits | Horizontal/document overflow | Max contained vertical scroll |
|---|---:|---:|---:|---:|
| 320 × 568 | 12 | 284 | 0 px | 434 px |
| 1440 × 900 | 12 | 284 | 0 px | 0 px |

The vertical scroll is intentional and contained inside the slide, especially on covers; this does not claim that every scene fits without scrolling. Desktop active rail entry stayed visible. The RU/dark mobile narrative and EN/light desktop narrative screenshots were visually inspected, along with a narrow bilingual consent dialog. Header controls are icons with localized accessible labels/tooltips; Home returns from collector preview to `../../index.html` and from root publication to `./`.

Additional interaction checks passed at both sizes: hidden Deep titles masked; hidden-Deep selection and Deep mode request consent; cancel retains position; keyboard cannot bypass a modal; lowering depth resets consent; saved Deep continuation reloads on a neutral cover, prompts again, then restores the exact ID; language/theme preserve position; start-over, arrows, Back and final Restart work; text tap enters focus with Next; swipe pages; vertical movement does not page/toggle; Escape restores chrome. Sources/Contents open and source counts fit. Offline fonts/images decoded, with zero runtime exceptions or external runtime requests.

Chrome used `timeout 30`, a unique temporary profile and owned-process-group cleanup on every run; profiles were removed, including failed preliminary runs. No server or Vite/HMR process was started. These checks use Chrome, not physical iPhone/Safari or an installed PWA. Parent owns the shared iPhone/PWA shell issue.

## Publisher integration requirements

- Keep `contentMode: narrative` and the maintained shell's corresponding label suppression.
- Update only through publisher-owned integration: counts/reading estimates changed from 24 / 60 / 96 to 14 / 21 / 36.
- Preserve the local `spoilerDialog`, session-only consent, masked contents, guards in `goToId`, `goToPosition` and `setMode`, and explicit spoiler policy used by neutral saved-position labels. Deep consent is reset on reload and on selecting a shorter mode. Hidden HTML JSON is not a secrecy/security boundary.
- Preserve the collector/root Home target handling. The original embedded geometric cover remains.
- Independent editorial review remains required. The ready manifest hashes all four canonical files and this detailed report; no catalogue, root reader, shared shell, git/PR/deploy or external messaging action was performed.

The authoritative delivery hashes are in `editorial-audit/2026-10-31/ready/white-fang.json`, avoiding a circular self-hash here.
