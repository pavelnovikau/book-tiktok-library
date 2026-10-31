# Book TikTok Library

Public, contribution-friendly library of dense standalone book stories. Each book is a single bilingual HTML file with nested reading depths and Flexoki light/dark themes.

Live site: https://book-tiktok-library.vercel.app

Git hosting: https://github.com/pavelnovikau/book-tiktok-library

Vercel project: `pavelnovikaus-projects/book-tiktok-library`. A merge to `main` is the production release path; pull requests are the contribution path.

## How it works

- `books.json` is the catalogue and the single place that lists books, sections, tags and collections.
- `index.html` reads the catalogue and automatically builds section shelves, cards, search, filters and book/screen/section counters.
- Every book remains a standalone HTML file and can be opened without the library shell.
- `manifest.webmanifest` and `sw.js` let the site run as an iOS/Android Home Screen app. The shell and catalogue are cached immediately; book HTML is cached after it is opened.
- `scripts/apply-reader-shell.mjs` adds the shared focus mode and optional PWA metadata to registered books. Focus mode toggles by tapping non-interactive text; only the reading content and Next remain.
- A push to `main` deploys the production site through Vercel. Pull requests run validation and can receive Vercel previews.

## Add a book

External contributors can fork the repository and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact contract.
The agreed 21-book Maximum-density expansion is tracked in [BOOK_PLAN.md](BOOK_PLAN.md).

```bash
npm run check
npm run sync:readers
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Repository policy

This repository accepts original analytical digests and lawfully reusable material. Do not submit pirated book text, copied chapters or fabricated quotations and page references. Existing book content is not placed under an open-content licence merely by being public; contributors must state the rights to their own submission.
