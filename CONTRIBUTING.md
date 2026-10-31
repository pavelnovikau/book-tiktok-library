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
  "genre": "systems-thinking",
  "screenCount": 90,
  "title": { "ru": "...", "en": "..." },
  "author": { "ru": "...", "en": "..." },
  "description": { "ru": "...", "en": "..." },
  "readingMinutes": { "essential": 12, "core": 30, "deep": 55 },
  "cover": { "type": "typographic", "mark": "SYSTEMS" }
}
```

If the genre is new, add one entry to `genres[]` with RU/EN labels. Supported card-cover types are `typographic`, `year`, `constraint` and `split`; `typographic` is the safe default.

## 3. Validate and preview

```bash
npm run check
python3 -m http.server 8000
```

Check at least 320×568 and 1440×900 in both themes and languages. Confirm the home control returns to the library and that there is no horizontal overflow.

## 4. Open a pull request

Use a fork, push your branch and open a PR. Include:

- the book and edition;
- exact Essential/Core/Deep screen counts and reading times;
- the source count and research method;
- a copyright/rights statement;
- mobile and desktop verification notes.

The automated check validates the catalogue, local files, bilingual metadata, counts that can be read deterministically, the home control and offline runtime invariants. A maintainer reviews content quality before merge. Merging to `main` publishes through Vercel automatically.
