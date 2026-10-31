# Book TikTok Library

Public, contribution-friendly library of dense standalone book stories. Each book is a single bilingual HTML file with nested reading depths and Flexoki light/dark themes.

Live site: https://book-tiktok-library.vercel.app

## How it works

- `books.json` is the catalogue and the single place that lists books and genres.
- `index.html` reads the catalogue and automatically builds the cards, book/screen counters and genre filters.
- Every book remains a standalone HTML file and can be opened without the library shell.
- A push to `main` deploys the production site through Vercel. Pull requests run validation and can receive Vercel previews.

## Add a book

External contributors can fork the repository and open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for the exact contract.

```bash
npm run check
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Repository policy

This repository accepts original analytical digests and lawfully reusable material. Do not submit pirated book text, copied chapters or fabricated quotations and page references. Existing book content is not placed under an open-content licence merely by being public; contributors must state the rights to their own submission.
