# Book TikTok v2 data contract

Use this reference when starting a new artifact, preparing structured story data, or diagnosing count/source drift. The v2 workflow keeps book content outside the UI shell until build time so one book cannot leak into the next.

## Build flow

1. Obtain the user’s approved cumulative Essential/Core/Deep counts. If they provide only a total, propose and confirm a split; counts include cover and final.
2. Create a claim map and source ledger in working notes.
3. Write one `story-data.json` following this contract.
   A minimal working example is available at `assets/story-data.example.json`.
4. Build the final descriptive HTML:

```bash
node <skill-dir>/scripts/build_story.mjs story-data.json \
  --out <book-slug>.html
```

5. Run `audit_story_html.mjs` on the generated HTML. The reader needs only that HTML; the JSON is a working source, not a delivery dependency.

Do not create a new book by copying a previously generated HTML file. Reuse the v2 builder and template instead.

## Top-level object

```json
{
  "schemaVersion": 2,
  "slug": "example-book",
  "title": { "ru": "Название", "en": "Title" },
  "description": { "ru": "Краткое описание", "en": "Short description" },
  "defaultLanguage": "ru",
  "defaultTheme": "dark",
  "defaultMode": "deep",
  "targetModes": { "essential": 24, "core": 56, "deep": 96 },
  "methodNote": { "ru": "...", "en": "..." },
  "sources": [],
  "media": {},
  "screens": []
}
```

- `schemaVersion` must be `2`.
- `slug` and every screen/media ID are stable lowercase kebab-case identifiers.
- `title`, `description`, and other localized fields require complete `ru` and `en` values.
- `targetModes` records the cumulative Essential/Core/Deep counts approved by the user. These counts include the cover and final screens. The build fails if the corpus does not match them exactly.
- The builder computes mode counts and reading times. Optional `modes.<mode>.label` and `modes.<mode>.minutes` may override labels or estimates.
- The default delivery filename is `<slug>.html`, not `index.html`, so a shared file remains identifiable.

## Sources

```json
{
  "id": 1,
  "title": "Direct source title",
  "url": "https://example.org/direct-page",
  "role": "author",
  "note": {
    "ru": "Какой тезис или факт поддерживает источник.",
    "en": "Which claim or fact this source supports."
  }
}
```

Required roles are `book`, `publisher`, `author`, `primary`, `review`, and `reference`. Prefer direct pages over search results. Source IDs are positive integers and must be unique.

The source ledger in working notes should additionally record access date, evidence boundary, useful passages in paraphrase, and claims that remain uncertain. Do not put copyrighted full text into the ledger.

## Screens

```json
{
  "id": "main-mechanism",
  "level": 1,
  "claimType": "book",
  "sources": [1, 3],
  "media": "mechanism-diagram",
  "copy": {
    "ru": {
      "section": "II · Механизм",
      "title": "Сильный заголовок формулирует тезис",
      "body": "<p>Текст экрана.</p>"
    },
    "en": {
      "section": "II · Mechanism",
      "title": "A strong title states the claim",
      "body": "<p>Screen body.</p>"
    }
  }
}
```

- `level: 1` appears in every mode; `2` adds the core; `3` adds deep detail.
- `claimType` is required on non-cover screens:
  - `book` — the author’s argument or evidence;
  - `corroboration` — independent factual scaffolding or a qualified challenge;
  - `synthesis` — the digest’s inference, analogy, or practical translation.
- `sources` may be empty only when the screen is framing, navigation, or clearly marked synthesis that makes no external factual claim.
- RU and EN must preserve the same quantities, names, causal qualifiers, claim type, sources, and cognitive job.
- `body` accepts restrained semantic HTML. Supported presentation classes in the clean template include `lede`, `muted`, `hero-number`, `fact`, `fact-label`, `compare`, `compare-item`, `metric-grid`, `metric-card`, `story-list`, `steps`, and `index`.

The first screen must be the single level-1 cover:

```json
{
  "id": "cover",
  "level": 1,
  "type": "cover",
  "sources": [],
  "copy": {
    "ru": { "section": "Начало", "title": "...", "subtitle": "...", "body": "<p>...</p>", "visualAlt": "..." },
    "en": { "section": "Start", "title": "...", "subtitle": "...", "body": "<p>...</p>", "visualAlt": "..." }
  }
}
```

The last screen must be the single level-1 final screen and set `"final": true`.

## Media

```json
{
  "cover-image": {
    "file": "./cover.jpg",
    "alt": { "ru": "Описание изображения", "en": "Image description" },
    "credit": { "ru": "Источник и лицензия", "en": "Source and license" }
  }
}
```

The builder resolves `file` relative to the JSON, embeds it as a data URI, and removes the path from the final artifact. A prebuilt image `dataUri` is also accepted. Every media item needs bilingual alt text and credit; an empty credit is allowed only for a user-supplied private cover.

## Screen-count gate and density profiles

Do not choose the count silently. If the user did not specify a full triple, offer three concrete profiles with exact cumulative mode counts and approximate reading time, recommend one, and wait. If they provided only a Deep total, propose and confirm its Essential/Core/Deep split. Counts include cover and final. Record the selected triple in `targetModes` before research and corpus writing.

Use these as proposal bands:

| Profile | Essential | Core | Deep | Typical use |
|---|---:|---:|---:|---|
| Compact | 16–24 | 30–48 | 45–64 | One main idea, short argument |
| Standard | 20–30 | 42–68 | 64–90 | Most idea-driven nonfiction |
| Dense | 24–36 | 56–90 | 90–130+ | Systems books, histories, handbooks |

Choose the proposal from an initial assessment of the book, then honor the user’s selection. A deeper layer is justified only by a distinct mechanism, case, consequence, caveat, application, or synthesis. If later research proves the selected count unsuitable, ask again with a reasoned revision; never pad or silently change it.

## Working checks before build

- Every central claim has at least one supporting source or an explicit evidence gap.
- The Essential sequence still forms a complete causal argument on its own.
- Core and Deep preserve the Essential order and insert detail rather than telling a different story.
- Each title states a claim; each body earns it; no two screens perform the same cognitive job.
- All numerical anchors and qualifications match across languages.
- No screen contains material inherited from another book.
