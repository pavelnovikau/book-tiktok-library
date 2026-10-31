# Contributing a book

Спасибо — внешние книги принимаются через fork и pull request.

## 1. Prepare the standalone book

Add one descriptively named root-level file such as `thinking-in-systems.html`.

The file must:

- work as a standalone HTML document with embedded CSS, JavaScript, fonts and images;
- support Russian and English;
- provide Essential, Core and Deep reading depths;
- use Flexoki light/dark themes;
- contain a compact home control in the top bar linking to `./`;
- support the shared focus-mode contract: a tap on non-interactive text hides reader chrome while preserving text and Next; a second tap restores it;
- identify sources and distinguish the book’s argument from independent corroboration and synthesis;
- contain no remote runtime scripts or stylesheets.

Do not submit copyrighted full text, copied chapters, pirated source files, invented quotations or invented page references. A digest should restate ideas in the contributor’s own words and cite lawful sources.

## 2. Register it in `books.json`

Add the book to `books[]`. The homepage derives its book count, screen count, cards and filters from this file automatically.

Required fields:

```json
{
  "slug": "thinking-in-systems",
  "file": "thinking-in-systems.html",
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

Use an existing `sections[]` ID unless the book genuinely requires a new primary shelf. Sections partition the catalogue: every book has exactly one. Collections are optional filters and may overlap: a book can belong to several, while `"collections": []` places it under the automatic `No collection` / `Без подборки` filter. A book also has any number of kebab-case `tags[]`. `audience` is `general`, `teen-14-plus` or `adult`; `spoilerPolicy` is `not-applicable`, `spoiler-free` or `full-plot-in-deep`. Supported card-cover types are `typographic`, `year`, `constraint` and `split`; `typographic` is the safe default.

Every catalogue cover also needs a semantic `motif` and a Flexoki `tone`. A motif is not decoration chosen at random: its geometry should encode the book’s central mechanism, such as a bottleneck for a constraints book, one surviving line for essentialism, a finite dot field for a book about limited time, a round door and returning road for a threshold story, a stepped protocol stack for a layered decision atlas, a routed map for a voyage, an isolated plateau for exploration, contour lines for strategic terrain, a remapped joint network for embodied learning, a route through an archipelago for a journey shaped by names and choices, nested fields for distinctions of control, a knot opening into a free line for release, or layered somatic traces for remembered threat. Existing motifs are `balance`, `crash`, `bottleneck`, `relay`, `distill`, `clock`, `weeks`, `mirror`, `stress`, `acceleration`, `door`, `protocol-stack`, `treasure-map`, `plateau`, `terrain`, `body-map`, `archipelago`, `control-field`, `open-knot` `somatic-trace` `attention-return` `causal-layers`, `inherited-path` and `quality-bridge`; each is used by one book only. Existing tones are `red`, `orange`, `yellow`, `green`, `cyan`, `blue` and `magenta`. Add a new renderer and validator entry when a genuinely new book needs a new motif. Do not reuse a generic circle or copy another card’s geometry.

## 3. Validate and preview

```bash
npm run sync:readers
npm run check
python3 -m http.server 8000
```

Run `sync:readers` after registering the file; it injects the maintained focus-mode and Home Screen metadata idempotently. Check at least 320×568 and 1440×900 in both themes and languages. Confirm the home control returns to the library, focus mode toggles without misreading a scroll or swipe, and there is no horizontal overflow.

## 4. Open a pull request

Use a fork, push your branch and open a PR. Include:

- the book and edition;
- exact Essential/Core/Deep screen counts and reading times;
- the source count and research method;
- a copyright/rights statement;
- mobile and desktop verification notes.

The automated check validates the catalogue, local files, bilingual metadata, counts that can be read deterministically, the home control and offline runtime invariants. A maintainer reviews content quality before merge. Merging to `main` publishes through Vercel automatically.
