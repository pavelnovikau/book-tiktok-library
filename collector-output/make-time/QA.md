# Make Time — QA and handoff

Date: 2026-10-31. Collector branch: `collector/make-time`. Base: `5d266aa`. The public report deliberately omits transient checkout and private workstation paths.

## Delivered scope

Exactly four files under `collector-output/make-time/`: `story-data.json`, `sources.md`, `make-time.html`, `QA.md`. No catalogue, existing reader, shared script, service worker, manifest, global skill or deployment changes. No external delivery. No subagents. Original analytical paraphrase; no reproduced chapters, book drawings, or direct book quotations. Step/tactic names identify concepts. Source book remains private and is not committed.

## Claim map and fidelity

Map and full ledger were written in `sources.md` before screens. The argument runs: a meaningful day is displaced by Busy Bandwagon/Infinity Pool defaults → efficiency and willpower alone do not choose a purpose → select a middle-sized Highlight → reserve space and accept trade-offs → restore friction around distraction → sustain attention through bodily care → record what happened and refine the arrangement.

Essential contains the complete loop, criteria of urgency/satisfaction/joy, 60–90-minute heuristic, calendar protection, a disrupted-day example, friction/kryptonite/time-craters, communication expectations, energy/rest trade-offs, caffeine/sleep, food disagreement, caregiving, reflection, quick start, structural limits, and the final model. Core inserts planning tools, examples, communication/TV/work-entry tactics and energy mechanisms. Deep adds secondary experiments, author cases, independent checks and evidence boundaries. Each deeper screen has a named distinct job; no chapter was divided into arbitrary continuation cards. Counts were assigned to these jobs, not produced by splitting prose.

All 87 tactic numbers appear either individually or in mechanism-related groups. Grouping is intentional: this is an analytical digest, not an exhaustive replacement for each instruction in the book. Disagreements preserved: morning/evening, fasting/snacking, and rest/wholehearted engagement. Defaults and personal experiments remain the organizing logic. No claim that every tactic works for every reader or that sprint observations validate the complete package.

Provenance: 104 `book`, 3 `corroboration`, and 5 `synthesis` screens including the cover. Every screen carries source IDs. Eight source records: one local book and seven public companions/checks; the book's HTTP link is explicitly bibliographic, not a claim that the publisher page contains the full text. Exact EPUB locations and coverage crosswalk are in `sources.md`.

## Exact counts and density

| Mode | Cumulative screens | RU words, builder | EN words, builder | RU time | EN time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Essential | 30 | 1599 | 1837 | 9 min | 9 min |
| Core | 72 | 3883 | 4414 | 22 min | 21 min |
| Deep | 112 | 6087 | 6914 | 34 min | 32 min |

Levels: 30 / 42 / 40, strictly nested. Cover and final are level 1. Times are builder estimates (180 RU / 220 EN words per minute), not promised reading durations; reflection and source consultation take longer.

Body-only density, excluding headings/interface: RU 5297 words, mean 47.29, median 47, range 40–52; EN 6005, mean 53.62, median 54, range 48–59. Every body falls within the skill's ordinary 35–75-word band. EN is longer by about 13%; review found expansion from natural English phrasing rather than omitted Russian claims. Audit totals use the auditor's own tokenization and exclude the cover subtitle, so differ slightly from the builder's totals.

## Translation checks

- Shared stable IDs, levels, sources, provenance and body jobs by schema.
- Nonempty RU/EN copy on all 112 screens; unique titles in each language during traversal.
- Digit-sequence check for title+body: zero mismatches, including 60–90 minutes, tactic identifiers, three-day start, and 400 mg / 12 participants / 0, 3, 6 hours.
- Manual paired review preserved causal qualifiers, attribution, uncertainty, differences between personal experience and controlled studies, and the scope of synthesis.
- Russian is default, English is a translation of this analysis of the Russian EPUB. It does not pretend to reproduce the English book's wording.
- Interface, title, source notes, method, accessibility labels and progress switch language; position, depth and theme survive toggles.

## Build and deterministic audit

Used the maintained builder:

```sh
node ~/.codex/skills/book-tiktok/scripts/build_story.mjs \
  collector-output/make-time/story-data.json \
  --out collector-output/make-time/make-time.html
node ~/.codex/skills/book-tiktok/scripts/audit_story_html.mjs \
  collector-output/make-time/make-time.html --min-screens 112 --require-bilingual
```

The integration maintainer rebuilt the artifact with the current maintained template. Its compact localized home control, focus counter behavior and long-heading wrapping now work without generated-HTML patches. The editable JSON remains the canonical content source.

Final deterministic audit output (path shortened only):

```json
{
  "file": "collector-output/make-time/make-time.html",
  "format": "v2",
  "bytes": 397262,
  "screenCount": 112,
  "levels": { "1": 30, "2": 42, "3": 40 },
  "modes": { "essential": 30, "core": 72, "deep": 112 },
  "words": { "ru": 6082, "en": 6905 },
  "passes": 68,
  "warnings": [],
  "failures": []
}
```

Standalone: embedded CSS/JS/Geist/Geist Mono; zero runtime HTTP requests, no runtime dependencies or service worker. Source hyperlinks are optional outbound navigation. Media count zero: typographic template cover, no redistributed EPUB art. Source dialog image-decoding checks are therefore not applicable; embedded fonts loaded successfully.

## Bounded real-browser verification

Preview was tried first. It rejected the local artifact with `Invalid preview URL (unsupported-protocol: file:; input length 124)`. Fallback: local Google Chrome headless via CDP, opening the exact `file://` artifact, no HTTP server. Each launch used `/usr/bin/timeout 30`, its own `mktemp -d` profile and dedicated debugging port. Full launched process groups were terminated and profiles removed in cleanup, including failed exploratory checks. Final process check found no `make-time-qa` Chrome process. Temporary scripts, logs and screenshots were removed after this report; only the four requested deliverables remain.

For each viewport the browser traversed every screen in both languages and both themes, in all three modes: `(30+72+112) × 2 × 2 = 856` rendered positions, `3424` across the matrix.

| Viewport | RU/EN × light/dark × all modes | Header fit | Horizontal overflow | Focus | Runtime errors |
| --- | --- | --- | --- | --- | ---: |
| 320×568 | PASS, 856 | PASS | 0 px | PASS | 0 |
| 390×844 | PASS, 856 | PASS | 0 px | PASS | 0 |
| 1024×768 | PASS, 856 | PASS | 0 px | PASS | 0 |
| 1440×900 | PASS, 856 | PASS | 0 px | PASS | 0 |

Checks:

- Default RU/dark and exact mode counts from rendered corpus/metadata/controls.
- Exact title and counter on every rendered position; provenance present on all non-cover screens. Measurement suppresses the transient slide-in transform during exhaustive layout checks; final snapshots use normal rendering. Clipped entry animation is not misreported as horizontal scrolling.
- Rapid repeated language/theme toggles preserve the current position and selected depth.
- Embedded Geist and Geist Mono report loaded.
- Chapters and Sources open/close; all eight source records appear; a retained hidden-screen chapter control exercises automatic depth raising. Normal contents show the selected mode's chapters only.
- Arrow, Page and Space navigation; visible Next/Back; horizontal pointer swipe advances; vertical pointer movement does not advance or toggle focus.
- Focus toggles by text tap and F, exits by second tap and Escape, survives paging; header/rail/back/counter hidden, Next inside viewport. Interactive controls, selected text, long press and scroll movement are ignored by the focus toggle.
- Short-phone slide body scrolls vertically; longer views fit this ordinary body without needing scroll. Dense comparison and source material remain scrollable.
- Saved position survives reload; Continue restores it; Start over starts at the first content screen; final restart returns to a clean cover and clears lastScreen.
- Desktop rail visible and scrollable, active entry synchronized.
- Zero runtime exceptions, zero unexplained console errors, zero HTTP network requests.
- Visual inspection: phone comparison/list/prose/focus; desktop cover, evidence/provenance and final. Both themes inspected. Images not applicable. All displayed source facts are text, not screenshot-derived.

## Known limitations and evidence boundaries

The supplied EPUB is the primary content authority; package metadata identifies the Russian edition. Long tactic groups were inspected through paragraph extraction with targeted full passages for central mechanisms; sample-day illustrations and schedules were not transcribed or treated as evidence. EN is analytical parity with RU, not an independently read full English edition. The reflowable source has no stable page references.

The book supplies author experiences and hypotheses, not equal-quality proof for every tactic. The caffeine study checks a fixed high dose in a small healthy-sleeper sample, not all beverage schedules; walking evidence concerns divergent ideation rather than all cognition. Evolutionary analogy, fasting, morning-cortisol timing, chocolate and meditation are not promoted into independently validated clinical protocols. No cited source validates the entire four-step package. Personal trials remain vulnerable to confounding and expectation effects. The independent review is reader response, not an outcome study.

Browser coverage is desktop Chrome with emulated viewports, not physical iOS/Android or a full assistive-technology audit. Safe-area CSS is inherited and the Next control was checked inside all emulated viewports; actual notched-device insets were not measured. Home links to `./` for eventual root-level library integration; in this unregistered collector folder it does not launch the main catalogue. Registration, root-copying and deployment are deliberately deferred to the maintainer.

During integration, the maintainer rebuilt the root reader from this JSON on the current template and ran the automatic whole-library browser gate across nine readers at 320×568, 390×844 and 1440×900. Catalogue counts, compact home navigation, focus enter/exit, topbar bounds and horizontal overflow passed with zero runtime errors. This supplements rather than replaces the collector's four-viewport matrix above.

## Integrity

- `story-data.json` SHA-256: `c743c6bfbc2ef52e9b3367979d24826d145d5d329baed74b5da55e5dbe3e7830`
- `make-time.html` SHA-256: `eecc02626649b69ddf1d1546b50a8f2e5d8857870271c9ba888f4b3aad76c4dc`
