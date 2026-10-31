# Essentialism — QA

Date: 2026-10-31. Status: **PASS**. Local collector artifact only; no deployment, catalogue edit, or external delivery.

## Artifact and contract

- Exact supplied edition: Greg McKeown, «Эссенциализм. Путь к простоте», И. Айзятулова translation, МИФ 2015, ISBN 9785000573471; original copyright 2014.
- Maintained schema-v2 builder and deterministic auditor from `/Users/pn/.codex/skills/book-tiktok/scripts/`; no shared shell, catalogue, or book files modified.
- Cumulative Essential / Core / Deep: **30 / 72 / 112**, including cover and final, both level 1.
- Level distribution: **30 level-1 + 42 level-2 + 40 level-3**. Strict subset checks passed. Stable IDs and source lists are shared by RU/EN.
- Default: **RU / dark / Deep**. Complete EN parity. Book argument 92 screens (cover included); corroboration 2; synthesis 18 (final included). Every screen has a provenance type; cover adds an explicit visible bilingual label because the maintained cover renderer does not display its normal provenance footer.
- Sources: **6**, all disclosed in the bilingual Sources dialog; detailed claim map, actual access and limits in `sources.md`. Book screens include an `epubLocator` to the exact local chapter, avoiding fabricated print pages.
- Network-independent single HTML: embedded CSS, JavaScript, Geist and Geist Mono. No runtime network requests. Source hyperlinks are optional navigation only.
- Media: **0**; intentional maintained typographic cover. No publisher cover, copied illustration, or external image dependency. Image decoding checks are not applicable.

## Density and estimates

Builder word counts include title, subtitle where present, and body; no interface text:

| Mode | Screens | RU words | EN words | RU minutes | EN minutes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 30 | 1569 | 1774 | 9 | 9 |
| Core | 72 | 3782 | 4269 | 22 | 20 |
| Deep | 112 | 5885 | 6621 | 33 | 31 |

Reading estimates use the maintained builder's 180 RU / 220 EN words per minute. They are approximate and exclude reflection, scrolling and source consultation. Independent body-only whitespace count: RU 5272 words, mean 47.07, median 47, range 42–72; EN 5859, mean 52.31, median 52, range 45–83. One EN list screen exceeds the ordinary 75-word band to retain its complete selection procedure. No empty bodies or duplicate localized titles. Audit word totals differ slightly because its parser does not count the subtitle in the same way; exact audit totals are preserved below.

## Deterministic audit

Command:

```sh
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs collector-output/essentialism/essentialism.html --min-screens 112 --require-bilingual
```

Exact output:

```json
{
  "file": "/Users/pn/.t3/worktrees/smartcat/t3-2a932e0b/_artifacts/book-tiktok-library/collector-output/essentialism/essentialism.html",
  "format": "v2",
  "bytes": 401816,
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
    "ru": 5880,
    "en": 6613
  },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

## Real Chromium QA

Chromium via Playwright 1.64.0-alpha-1790635538000, local `file://` loading, no HTTP server. Each browser run used its own temporary persistent profile and `timeout 30`; browser contexts were closed and profiles removed in `finally`. No shared browser instance was used.

| Viewport | Light | Dark | Traversal per theme |
| --- | --- | --- | ---: |
| 320×568 | PASS | PASS | 428 |
| 390×844 | PASS | PASS | 428 |
| 1024×768 | PASS | PASS | 428 |
| 1440×900 | PASS | PASS | 428 |

Each run traversed every screen in every mode in both languages: 2 × (30 + 72 + 112) = 428 rendered-screen checks; **3424 checks across the eight size/theme combinations**, excluding targeted repeats. Assertions: localized title matches structured source, exact position and denominator, nonempty content/provenance, no horizontal document or slide overflow. Default language/theme, persistent depth and strict counts were checked in the browser.

Other checks passed:

- All topbar controls remain within the 320px viewport; content has independent vertical scrolling. Dense screens may need scrolling on small phones by design.
- Desktop rail visible and scrollable at 1024/1440. Active chapter visibly synchronized on representative navigation/screenshots.
- RU/EN and theme changes preserve current screen/position and chosen depth.
- Chapters and Sources dialogs open/close; sources and method are bilingual.
- Hidden-screen `goToId` mode raising exercised through a retained chapter-button reference after reducing depth. Normal chapter lists show the currently selected depth only; they do not expose every hidden item at once.
- Embedded Geist and Geist Mono load. No images to decode.
- Begin, Next, Previous, ArrowRight, PageUp, Space and horizontal pointer swipe; vertical pointer movement did not navigate in targeted checks.
- Saved screen survives reload; Continue restores it, Start over begins again, final Restart clears remembered position and returns to cover.
- **Zero runtime/console errors and zero HTTP(S) requests** in all eight runs.

Visual inspection: 320px light cover, long selection screen and final; 390px dark English list and comparison; 1024px light cover; 1440px dark cover and independently sourced sleep/quantitative screen. Text, contrast, nested-mode controls, rail and provenance were legible. Initial capture timing preceded the entrance animation; final visual captures waited two animation frames and disabled finite screenshot animations. No artifact edit was necessary for that capture issue. Temporary browser scripts, screenshots and raw result files were removed after inspection; checks are recorded here.

## Fidelity and limitations

- Preserves all four book parts, Explore–Eliminate–Execute as a cycle, choice, unequal returns, trade-offs, buffers, 90% and minimum/ideal selection criteria, all four editing moves, boundaries, small progress, routine, presence and the leadership appendix.
- Retains the book's explicit limits: refusing a good option does not guarantee a better one; four-burner metaphor is not an instruction to abandon family/health; the digital-access intent was still unfinished when described.
- Actual reading boundary: OPF/NCX, edition information, structure and relevant argument/example passages across all 20 chapters and appendix; **not a claim of line-by-line reading of every paragraph**. Exact supplied EPUB is authoritative; anniversary additions are excluded. English is a new translation of the digest, not reproduced original English prose.
- Author anecdotes, business outcomes, historical and sporting examples are not independently verified. Herbie is explicitly identified as a fictional case from *The Goal*. Elite anecdotes and polar/policing stories do not establish causal effects.
- Primary sleep and subtraction abstracts support only narrow claims. The latter postdates the book. No whole-package validation, universal 90% optimum, universal 50% buffer, medical prescription, or promise of equal freedom to refuse.
- Additional concerns about unequal power, duties of care, reverse-pilot risk and arbitrary metrics are explicitly synthesis. The independent practitioner review is favorable reception evidence, not an outcome trial.
- No copied chapters, extended quotations, source EPUB, or publisher imagery included. No publication, push, PR or shared-library registration performed. A parent integrator can handle catalogue/home integration separately; this collector changes only its own directory.

## Reproducibility

- HTML SHA-256: `7f431aedcd0714a7124a00e60ed612348e4591d508a66f7266957a575a0f9229`.
- Data SHA-256: `dfdf66d42d68d0afe1761bc9185891398e769f86fcc58c05c1920220ff06d0b7`.
- build_story.mjs SHA-256: `c88078eb41ae3d63bfd05e3a94834f2bc960f554ce3736965f3467398c44f88d`.
- audit_story_html.mjs SHA-256: `9c65e6f399e622280380ea554d0c3a1ffc5806fecab828da9d2079d4a4529d68`.

Rebuild with the maintained builder using `story-data.json`, then run the audit command above. The HTML is the complete runtime artifact; the other three files preserve editable data, evidence and QA.
