# Contributing a book

Спасибо — внешние книги принимаются через fork и pull request.

## 1. Prepare the standalone book

Add one descriptively named root-level file such as `thinking-in-systems.html`.

The file must:

- work as a standalone HTML document with embedded CSS, JavaScript, fonts and images;
- support Russian and English;
- provide Essential, Core and Deep reading depths;
- use Flexoki light/dark themes with the maintained Settings modal;
- use a single compact row of icon-only header controls with localized tooltips and accessibility labels; replace the direct theme toggle with the shared Settings gear (Dark/Light and Sans/Serif), keep the home control linking to `./` and the optional iOS guide trigger in that same row;
- support the shared focus-mode contract: a tap on non-interactive text hides reader chrome while preserving text and Next; a second tap restores it;
- identify sources and distinguish the book’s narrative/argument from independent checks and any digest inference;
- contain no remote runtime scripts or stylesheets.

Do not submit copyrighted full text, copied chapters, pirated source files, invented quotations or invented page references. Write in original words and cite lawful sources. Fiction must tell the author’s story through supported events, characters and causal links; nonfiction must convey the author’s argument and actual examples; practical/hybrid works retain their real procedures and the relationship between narrative and ideas. Do not substitute management or moral lessons, invented scenes or quota padding. Write connected prose first, segment afterwards, then derive exact nested counts. A task that leaves length to the author needs no additional count-confirmation gate.

The optional v2 `contentMode` is `narrative` or `explanatory`. Narrative mode hides per-screen provenance/footnote chrome while keeping screen source maps and the accessible global Sources dialog. Omission preserves legacy behavior. Changing that field alone does not repair an analytical retelling. Preserve the book’s spoiler boundary in all modes, cover/final, contents, resume labels and global source/method notes. State which edition and passages were actually consulted; a fetched full text does not mean it was read continuously.

## 2. Register it in `books.json`

Add the book to `books[]`. The homepage derives its book count, screen count, cards and filters from this file automatically.

Required fields:

```json
{
  "slug": "thinking-in-systems",
  "file": "thinking-in-systems.html",
  "workTypes": ["nonfiction"],
  "genres": [],
  "subjects": ["systems-society"],
  "section": "systems-work",
  "tags": ["systems", "management"],
  "collections": ["practices"],
  "audience": "general",
  "spoilerPolicy": "not-applicable",
  "screenCount": 90,
  "title": { "ru": "...", "en": "..." },
  "author": { "ru": "...", "en": "..." },
  "description": { "ru": "...", "en": "..." },
  "readingMinutes": { "essential": 12, "core": 30, "deep": 55 },
  "cover": { "type": "typographic", "mark": "SYSTEMS", "motif": "bottleneck", "tone": "cyan" }
}
```

Use existing `discovery.types`, `discovery.genres`, `discovery.subjects` and `discovery.topics` IDs. `workTypes[]` contains `fiction`, `nonfiction` or both for an honest hybrid; a hybrid also needs a bilingual `workTypeLabel` explaining its form (for example, “Философский роман / Philosophical novel”). Fiction needs at least one genre; nonfiction needs at least one subject. Genres and subjects may overlap across books. Tags reference the controlled bilingual `discovery.topics` vocabulary; add a localized label and a few relevant aliases for a new topic, rather than an unbounded keyword list. Authors belong in `author`, not in genres. Do not assign work type from audience.

Keep an existing `sections[]` ID and `collections[]` assignments for schema-2 compatibility. Every book still has one legacy section; collections may overlap or be empty. Neither is a public navigation control, and empty collections need no special public label. New legacy section/collection IDs also need an explicit mapping to visible type/topic/query controls in `discovery.legacySections` or `discovery.legacyCollections`. The additive discovery extension leaves existing standalone and story-data contracts unchanged; the shell and validator also accept an older schema-2 catalogue without the extension.

`audience` is internal context: `general`, `teen-14-plus` or `adult`; `spoilerPolicy` is `not-applicable`, `spoiler-free` or `full-plot-in-deep`. Keep spoiler notices accurate and do not turn audience into an age shelf or profile. Supported card-cover types are `typographic`, `year`, `constraint` and `split`; `typographic` is the safe default.

Every catalogue cover also needs a semantic `motif` and a Flexoki `tone`. A motif is not decoration chosen at random: its geometry should encode the book’s central mechanism, such as a bottleneck for a constraints book, one surviving line for essentialism, a finite dot field for a book about limited time, a round door and returning road for a threshold story, a stepped protocol stack for a layered decision atlas, a routed map for a voyage, an isolated plateau for exploration, contour lines for strategic terrain, a remapped joint network for embodied learning, a route through an archipelago for a journey shaped by names and choices, nested fields for distinctions of control, a knot opening into a free line for release, layered somatic traces for remembered threat, a known latitude with several possible longitudes for a search constrained by partial evidence, or a body crossing a shore between confined air and open water. Newly registered motifs show an observer above a closed city, a raft following a branching river, two speakers linked through four communication components, four learning practices joined by a fifth feedback path, a common city linked by reason, and two tracks converging across broken ice. Existing motifs are `habit-cycle`, `balance`, `crash`, `bottleneck`, `relay`, `distill`, `clock`, `weeks`, `mirror`, `stress`, `acceleration`, `door`, `protocol-stack`, `treasure-map`, `plateau`, `terrain`, `body-map`, `archipelago`, `control-field`, `open-knot`, `somatic-trace`, `attention-return`, `causal-layers`, `inherited-path`, `quality-bridge`, `convex-response`, `latitude-search`, `conditioned-trust`, `rule-loop`, `testimony-compass`, `chalk-boundary`, `scale-question`, `sea-air`, `enchanted-lab`, `watchtower`, `river-raft`, `needs-bridge`, `five-disciplines`, `common-city`, `ice-crossing`, `dual-frame`, `stock-flow`, `two-orbits`, `memory-spectrum`, `commons-rules`, `paradigm-shift` and `legibility-grid`; each is used by one book only. Existing tones are `red`, `orange`, `yellow`, `green`, `cyan`, `blue` and `magenta`. Add a new renderer and validator entry when a genuinely new book needs a new motif. Do not reuse a generic circle or copy another card’s geometry.

## 3. Validate and preview

```bash
npm run sync:readers
npm run check
npm run qa:settings
```

Run `sync:readers` after registering the file; it injects the maintained Settings module, focus mode and Home Screen metadata idempotently without rebuilding book corpora. [Settings contract, fonts/licenses and no-server QA](skills/book-tiktok/references/reader-settings.md) cover v2 and legacy readers. Theme and reading font are global; preserve each book’s language, depth, position and bespoke spoiler consent. Serif uses Geist Serif for Latin and Source Serif 4 for Russian; the localized note must remain visible in Settings. Check at least 320×568 and 1440×900 in both themes and languages. Confirm the home control returns to the library, focus mode toggles without misreading a scroll or swipe, and there is no horizontal overflow.

## 4. Open a pull request

Use a fork, push your branch and open a PR. Include:

- the book and edition;
- exact Essential/Core/Deep screen counts and reading times;
- the source count and research method;
- a copyright/rights statement;
- mobile and desktop verification notes.

The automated check validates the catalogue, local files, bilingual metadata, counts that can be read deterministically, the home control and offline runtime invariants. A maintainer reads the actual RU/EN content and checks its scenes/mechanisms against supporting passages before merge. Passing the structural audit does not establish editorial approval. Merging to `main` publishes through Vercel automatically.
