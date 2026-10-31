# Skin in the Game — QA

Date: 2026-10-31. Result: **PASS**. Default: **RU / dark / Deep**. One portable HTML, schema v2, Flexoki shell, embedded Geist and Geist Mono. No external runtime dependencies. No deployment or publication.

## Exact counts and density

Counts include the level-1 cover and level-1 final. Essential ⊂ Core ⊂ Deep is implemented by stable screen IDs and cumulative levels, with identical structure and provenance in RU and EN.

| Mode | Cumulative screens | RU words / estimated minutes | EN words / estimated minutes |
|---|---:|---:|---:|
| Essential | 30 | 1,675 / 10 | 1,877 / 9 |
| Core | 72 | 3,968 / 23 | 4,470 / 21 |
| Deep | 112 | 6,136 / 35 | 6,865 / 32 |

Incremental levels: **30 / 42 / 40**. Sources: **8** (one supplied EPUB plus seven external records). Provenance: **94 book / 4 corroboration / 14 synthesis**, including explicit book attribution on the cover. No orphan source IDs. Every referenced EPUB filename and fragment anchor was checked against the supplied edition and exists.

Body-only density, excluding EPUB footer locators: RU mean **45.2**, median **45**, range **40–56** words; EN mean **50.6**, median **50.5**, range **45–62** words. No screen below 35 body words. These are Unicode lexical counts; builder/auditor counts differ slightly by punctuation and by whether cover subtitle words are included. Reading times are builder estimates at RU 180 / EN 220 words per minute, not timed user tests.

## Reproduction and exact deterministic audit

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs \
  collector-output/skin-in-the-game/story-data.json \
  --out collector-output/skin-in-the-game/skin-in-the-game.html
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/skin-in-the-game/skin-in-the-game.html \
  --min-screens 112 --require-bilingual
```

The maintained builder and audit were used unchanged. Audit output (the auditor excludes cover subtitle words that the builder includes in its reading-time calculation):

```json
{
  "file": "/Users/pn/.t3/worktrees/smartcat/t3-f16df966/_artifacts/book-tiktok-library/collector-output/skin-in-the-game/skin-in-the-game.html",
  "format": "v2",
  "bytes": 410722,
  "screenCount": 112,
  "levels": {
    "1": 30,
    "2": 42,
    "3": 40
  },
  "modes": {
    "essential": 30,
    "core": 72,
    "deep": 112
  },
  "words": {
    "ru": 6129,
    "en": 6857
  },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

## Real-browser matrix

Automated with the installed Playwright library and real headless Google Chrome, loading `file://` directly. No HTTP server. Every run used `timeout 30`, a unique `mktemp -d` Chrome profile, a 27-second browser watchdog, `finally` browser close, and immediate profile cleanup. No preview tools or shared browser tabs were used.

| Viewport | Languages | Themes | Rendered screen checks | Result |
|---|---|---|---:|---|
| 320×568 | RU, EN | Dark, light | 856 | PASS |
| 390×844 | RU, EN | Dark, light | 856 | PASS |
| 1024×768 | RU, EN | Dark, light | 856 | PASS |
| 1440×900 | RU, EN | Dark, light | 856 | PASS |

Total **3,424** checked screen renders: (30 + 72 + 112) × 2 languages × 2 themes × 4 viewports. Each traversal asserted selected-mode count, expected localized title, matching active rail ID, visible provenance element, slide/document horizontal bounds, and all four top controls inside the viewport.

Interaction checks passed at every viewport:

- Chapters and Sources dialogs open/close; eight source records and bilingual method are present.
- Arrow, Page, Space, Back and Next navigation; horizontal pointer swipe advances, vertical gesture does not.
- Language/theme switches preserve the current screen. Language, theme, depth and remembered position persist through reload.
- Continue restores the remembered screen. Continuing a stored Deep screen from Essential raises depth automatically. Start over begins at the first argument screen.
- Final restarts at the cover and clears the remembered screen.
- Embedded Geist/Geist Mono load; no media images are used, so image decoding/credit checks are not applicable.
- Desktop rail is visible, scrollable and synchronized at 1024/1440. Top transparency controls remain reachable at 320.
- Zero console errors, zero page/runtime exceptions, zero attempted HTTP(S) runtime requests in all four runs.

Visual inspection covered mobile/desktop cover, dense prose, numerical worked example, checklist/list, source provenance, source dialog, final, RU/dark and EN/light. Comparison reasoning is textual rather than a separate comparison-card component. No documentary image screens are included. At 320×568 the body intentionally scrolls under the fixed header/footer; the checklist scroller was checked at scrollTop 234 with clientHeight 420 / scrollHeight 654, and the cover at scrollTop 506 with clientHeight 492 / scrollHeight 998. Source labels and the cover action are reachable. A screenshot taken immediately after a theme/layout change caught a compositor frame before paint; repeating after settling showed correct content. No artifact change was needed.

## Fidelity and evidence boundaries

- Exact Russian EPUB edition and translator are recorded in `sources.md`. English is a complete translation of this analytical digest; no claim is made to have read or reproduced the English edition.
- A claim map and full ledger were written before screen drafting. Source 1 remains the primary evidence; chapter/anchor locators, attribution and methodological boundaries stay in the artifact.
- The argument keeps asymmetry, filtering, minority compatibility, scale, coercive dependence, ethics, Lindy and dynamic survival separate. Objections are substantive screens, including inside Essential.
- No chapters, scanned cover, book illustrations or extended quotations are redistributed. Screens are original paraphrases. The multiplicative arithmetic and organisational application are labelled synthesis, not invented Taleb examples.
- The local argument reading was structured and selective across all chapters, glossary and appendix, not exhaustive line-by-line reading. Technical formulas were not independently proven or replicated.
- Taleb’s medical, geopolitical, historical and technological examples are attributed book claims, not independently established advice. Minority percentages are not presented as universal thresholds; Lindy is not treated as proof of moral rightness; personal stakes are not treated as sufficient evidence of expertise.
- Source 6 is abstract-only; source 7 is limited to an indexed publisher excerpt because direct full-text access failed. Source 8 uses the original publisher abstract and remains bounded to its constrained auction model. Author sources 3/4 are triangulation, not independent corroboration. Full source-specific access boundaries appear in `sources.md` and in bilingual source notes.
- Browser checks cover Chrome, not native Safari/Firefox or physical-device assistive technology. Local-storage behaviour can differ in restrictive file viewers.

## Scope and handoff

Only the four deliverables under `collector-output/skin-in-the-game/` are committed. No changes to the library index, catalogue, shared scripts, service worker, manifest, existing books, or shared work logs. No deployment, push, PR or external delivery. Temporary authoring/QA scripts, screenshots, reports and Chrome profiles were removed after results were recorded here.

## Artifact checksums

- `story-data.json`: 195,371 bytes; SHA-256 `39d2a3346c0f0f60624efd741ff629b789555f14e65702e5125be8051651c088`.
- `skin-in-the-game.html`: 410,722 bytes; SHA-256 `87d79afeca38878c8d28e7e3e2a7283c5d15834b04edc669e798c9b35779002f`.

Maintained script SHA-256 at build/audit time:

- `build_story.mjs`: `c88078eb41ae3d63bfd05e3a94834f2bc960f554ce3736965f3467398c44f88d`.
- `audit_story_html.mjs`: `9c65e6f399e622280380ea554d0c3a1ffc5806fecab828da9d2079d4a4529d68`.
