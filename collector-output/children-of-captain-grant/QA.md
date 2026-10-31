# The Children of Captain Grant — editorial repair QA, 2026-10-31

Status: **ready-for-independent-check**. This document replaces the earlier green collector/cold reviews. Those reviews established neither the requested reading experience nor whole-book fidelity. No root integration, publication or deployment is claimed.

## Content reviewed and rebuilt

Read all **144 original RU/EN pairs**, including titles, body, cover and final. The original authoring JSON, collector HTML embedded corpus and published root HTML embedded corpus were compared; all screen content matched. Computed-mode-only metadata differences, where present, were not narrative divergence. This is 144 unique bilingual pairs, not a triple-count of identical copies.

All ordinary story bodies and framing were rewritten as an original condensed narrative: **37 pairs**, replacing 144. `contentMode: narrative`; `spoilerPolicy: full-plot-in-deep`; fresh defaults RU/dark/Essential. The final counts follow the connected story, not a fixed quota.

Rebuilt the damaged message, children, Andes, Thalcave, flood, sea passage, Australia and late rescue as story. Confirmed 37°11′ means minutes. Explicitly restored Glenarvan killing Kara-Tete and the final Paganel comedy; kept Tabor/Maria Theresa within the novel’s geography. Omitted inconsistent wreck dates and adopted none of the narrator’s racial rankings.

Essential/Core stop at the Snowy camp before Ayrton’s exposure. Betrayal, New Zealand, the Duncan explanation, Grant’s reunion and closing fates remain in Deep. Original geometric globe/route/letter image, with neutral descriptive alt text and a short Smartcat credit.

| Depth | Cumulative screens | RU / EN words | RU / EN estimated minutes |
|---|---:|---:|---|
| Essential | 14 | 689 / 847 | 4 минут / 4 min |
| Core | 23 | 1084 / 1305 | 7 минут / 6 min |
| Deep | 37 | 1744 / 2096 | 10 минут / 10 min |

Words/minutes are the maintained builder's title/subtitle/body count and reading estimates, not tested completion times. Source maps remain in JSON and Sources; there is no academic provenance label after narrative screens.

## Evidence and substantive check

Jules Verne, In Search of the Castaways: Charles F. Horne-edited historical English version, Project Gutenberg #2083, 66 chapters (26 + 19 + 21). French Hetzel 1868 I.II, III.XVII, III.XXI and III.XXII additionally consulted through Wikisource.

The English source is a historical edited version, not the complete 70-chapter French original. Chronological narrative runs in all 66 English chapters plus retained-scene checks support this condensed plot. Four French chapters resolve the coordinate, mistaken order and ending checks. No full French comparative collation is claimed.

The short route introduces Thaouka, the water-scouting party and the Australian arrival. Core includes the Snowy stop as well. The flood-to-farewell order and storm-to-farm transition were checked for unintended flashbacks and repetition. Every retained scene has primary chapter locators in sources.md.

The complete source files/extracts remain in private audit storage outside this repository. New prose contains no copied chapters, modern translation, invented direct speech, scene or page reference. The source ledger maps the actual retained incidents. A local structural pass is not a literary fidelity certificate; the publisher must read every rebuilt pair and check supporting passages. No source-access block prevents independent checking of the represented plot. Residual limits:

- Full comparative collation against all 70 French chapters has not been performed.
- The Horne English edition is not represented as the complete French original.
- No continuous every-paragraph reading, scientific/geographical validation or Russian-translation-wide fidelity is claimed.

## Local structural and browser checks

Built with the maintained `build_story.mjs`, then preserved the book-local consent behavior described below. The current generic structural audit returned **69 passes / 0 warnings / 0 failures**. Exact embedded data match the authoring JSON; only the generated `modes` metadata is added. Unique IDs, nested counts, bilingual copy/source fields, offline assets and font invariants passed.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/children-of-captain-grant/story-data.json --out collector-output/children-of-captain-grant/children-of-captain-grant.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/children-of-captain-grant/children-of-captain-grant.html --require-bilingual
```

**A plain rebuild needs the local consent restoration before delivery.** The private reproducibility script is `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/build_group.py`; it builds only these four packages and applies their small local changes. It does not edit the shared template. Do not treat an unpatched builder output as this checked candidate.

Final real Chrome/CDP matrix, local `file://`, network offline: both languages × both themes × all three depths, at both viewports. **592 visits** checked expected stable ID, exact rendered paragraphs and title, counter, document/slide width, header row, narrative-label suppression and text-bottom reachability.

| Viewport | Depth/language/theme combinations | Screen visits | Horizontal/document overflow | Max contained vertical scroll |
|---|---:|---:|---:|---:|
| 320 × 568 | 12 | 296 | 0 px | 466 px |
| 1440 × 900 | 12 | 296 | 0 px | 0 px |

The vertical scroll is intentional and contained inside the slide, especially on covers; this does not claim that every scene fits without scrolling. Desktop active rail entry stayed visible. The RU/dark mobile narrative and EN/light desktop narrative screenshots were visually inspected, along with a narrow bilingual consent dialog. Header controls are icons with localized accessible labels/tooltips; Home returns from collector preview to `../../index.html` and from root publication to `./`.

Additional interaction checks passed at both sizes: hidden Deep titles masked; hidden-Deep selection and Deep mode request consent; cancel retains position; keyboard cannot bypass a modal; lowering depth resets consent; saved Deep continuation reloads on a neutral cover, prompts again, then restores the exact ID; language/theme preserve position; start-over, arrows, Back and final Restart work; text tap enters focus with Next; swipe pages; vertical movement does not page/toggle; Escape restores chrome. Sources/Contents open and source counts fit. Offline fonts/images decoded, with zero runtime exceptions or external runtime requests.

Chrome used `timeout 30`, a unique temporary profile and owned-process-group cleanup on every run; profiles were removed, including failed preliminary runs. No server or Vite/HMR process was started. These checks use Chrome, not physical iPhone/Safari or an installed PWA. Parent owns the shared iPhone/PWA shell issue.

## Publisher integration requirements

- Keep `contentMode: narrative` and the maintained shell's corresponding label suppression.
- Update only through publisher-owned integration: counts/reading estimates changed from 36 / 90 / 144 to 14 / 23 / 37.
- Preserve the local `spoilerDialog`, session-only consent, masked contents, guards in `goToId`, `goToPosition` and `setMode`, and explicit spoiler policy used by neutral saved-position labels. Deep consent is reset on reload and on selecting a shorter mode. Hidden HTML JSON is not a secrecy/security boundary.
- Preserve the collector/root Home target handling. The original embedded geometric cover remains.
- Independent editorial review remains required. The ready manifest hashes all four canonical files and this detailed report; no catalogue, root reader, shared shell, git/PR/deploy or external messaging action was performed.

The authoritative delivery hashes are in `editorial-audit/2026-10-31/ready/children-of-captain-grant.json`, avoiding a circular self-hash here.


## Parent meaning corrections — 2026-10-31

Parent applied required independent meaning findings GRANT-CONTENT-01 in RU and EN. Changed pairs: toline-geography. Embedded data/derived reading estimates refreshed without replacing outer reader code or styles. This is a localized closure awaiting publisher validation, not a new independent PASS.
