# Pirsig narrative rebuild — local QA, 2026-10-31

Status: **local self-check complete; ready for independent editorial checking**. This is not publication approval or a whole-book fidelity certificate. The corrected BRIEF supersedes the old green reviews and fixed screen quotas.

## Content and scope

- Read all **144 old RU/EN pairs**, then substantively checked all **52 rewritten pairs**, with each nested sequence considered on its own. Old authoring and collector/root embedded corpora were equal. Final authoring and collector embedded corpora are equal.
- New cumulative **20 / 38 / 52**; level increments **20 / 18 / 14**. No filler to preserve 144. Defaults RU / dark / Essential.
- `contentMode: narrative`, `contentRevision: 2026-10-31-editorial-rebuild`, `spoilerPolicy: full-plot-in-deep`.
- Main plot/argument is grounded in the existing complete personal Russian EPUB. Substantial selected reading across all 32 chapters; full reading of chapters 21, 23, 27, 31 and 32 and the prefatory note. Full continuous reading of every sentence is not claimed. EN translates the new account; no complete English-edition comparison. Exact print edition remains unidentified. Chapter 32 has conversion gaps; those passages were omitted rather than reconstructed.
- No invented dialogue, scene, motive, page number or scientific/medical result. Actual procedures and examples remain the narrator's. External biography, later-book metaphysics and added reader exercises were removed.
- Cover/final/warning are editorial framing. Scene/argument screens use the internal book provenance field, which the narrative renderer hides. No academic label is appended to story screens.
- **2 source records**, representing one private primary book and public association orientation; they share a public orientation URL and are not counted as independent editions. **1 original inline SVG**, a winding road and ridge, replaces the generic lesson/model graphic. No publisher illustration or book text is included.
- The source map and detailed stable-ID findings are in `sources.md` and `editorial-audit/2026-10-31/books/zen-and-the-art-of-motorcycle-maintenance.md`.

## Build and structure

Maintained tools, no copied reader and no shared-template modification:

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/zen-and-the-art-of-motorcycle-maintenance/story-data.json --out collector-output/zen-and-the-art-of-motorcycle-maintenance/zen-and-the-art-of-motorcycle-maintenance.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/zen-and-the-art-of-motorcycle-maintenance/zen-and-the-art-of-motorcycle-maintenance.html --min-screens 52 --require-bilingual
```

Final audit: **69 structural passes, zero warnings, zero failures**. This measures structure; editorial judgment comes from actual text/primary comparison above, and independent checking remains pending.

HTML: **330,082 bytes**. SHA-256: `d30f0d41e0f1f7fd7c561088b9d7200ec5fa63864217c78fd947bc28160803d0`.
Builder word totals (titles/subtitles/body): RU **1,134 / 2,157 / 2,975**; EN **1,315 / 2,483 / 3,415**. Automatic reading estimates: RU **7 / 12 / 17 minutes**; EN **6 / 12 / 16 minutes**. These are estimates, not timed reader studies.

## Real Chromium checks

Each viewport used an owned Chrome process group bounded by `timeout 30`, a unique temporary profile and `file://` navigation. No web server was started. Process group/profile cleanup ran after every phase; final check found **zero owned Chrome processes or profiles remaining**.

Viewports: **320×568, 390×844, 1024×768, 1440×900**. Every visible screen in every mode, in RU/EN and dark/light, was traversed: `(20 + 38 + 52) × 2 × 2 × 4 = 1,760 visits`.

Passed:

- Exact rendered heading and cumulative count; no document/content horizontal overflow; Next and header within viewport on body screens.
- Narrative screens show no `.source-label`, including no Синтез/Book argument evidence badge. Sources remain available via the compact header.
- Single header layout, Home target `./`, embedded font readiness, source dialog with two records, Contents dialog.
- Synthetic touch tap enters focus, Next remains available, and a second tap restores chrome.
- Saved Deep `hospital-door` reloads to the cover and displays a **generic spoiler-labelled Continue**, without the saved title. A retired old bookmark (`scale-limit`) falls back to the cover without a false Continue target.
- Cover Start remains reachable through vertical scrolling at smaller viewports and directly at 1440px. Cover scrolling is intentional; it is not claimed to fit entirely into 320×568.
- **Zero JavaScript exceptions and zero HTTP(S) page requests** in all four runs. Offline fonts and inline SVG render locally.

Representative settled screenshots were visually inspected at 320px and 1440px; light text/body and dark cover were inspected, and the generic analytical fallback art was corrected locally. Raw browser JSON and screenshots remain outside the repository in the worker's private audit workspace. Screenshots and layout checks are not proof of literary fidelity.

No physical iPhone/Safari/PWA, screen-reader, whole-library, production or clinical/historical verification is claimed. The reported global iPhone/PWA header issue remains the publisher's shared-reader investigation; local Chromium viewport checks must not be presented as that investigation being closed.

## Publisher handoff

The worker changed only this collector's four canonical files and its own audit/ready/group reports. The root reader, `books.json`, homepage, shared shell, installed skill and release files remain publisher-owned. No Git, PR, deploy or external messaging action was performed.

Integrate only after independently reading every revised pair and the sequence. Catalogue: **52 screens**, depth counts **20/38/52**, RU minutes **7/12/17** (EN **6/12/16**). Keep the philosophical-novel hybrid classification, narrative rendering, clear Deep warning and maintained saved-progress protection. Do not publish the source-blocked Dune/Left Hand/Project Hail Mary records as a consequence of this candidate being ready for checking.
