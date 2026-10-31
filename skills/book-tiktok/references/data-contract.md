# Book TikTok v2 data contract

Use this reference when starting a new artifact, preparing structured story data, or diagnosing count/source drift. The v2 workflow keeps book content outside the UI shell until build time so one book cannot leak into the next.

## Build flow

1. Identify the actual work, edition, writing form and evidence boundary; honor explicit user length constraints.
2. Map the narrative/argument/procedures and sources, then write connected original-word prose.
3. Segment it into coherent nested modes, derive exact cumulative counts from the justified content, and write one `story-data.json` following this contract.
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
  "defaultMode": "essential",
  "contentMode": "explanatory",
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
- `targetModes` records the exact cumulative Essential/Core/Deep counts derived from the finished, justified content. Include cover and final. The builder fails on any mismatch; it must never pad prose to satisfy this assertion. Honor explicit user constraints, but do not add a confirmation gate when the task permits you to choose length.
- Optional `contentMode` is `narrative` or `explanatory`. Choose by the actual prose: fiction is normally narrative; nonfiction/practical prose normally explanatory; hybrids preserve the work’s own mix. Narrative presentation hides per-screen provenance/source-footnote chrome, preserving embedded source maps and the accessible global Sources dialog. Omit the field to retain legacy presentation; never relabel an unchanged analytical fiction digest as a repair.
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
  - `book` — the author’s narrative, argument, example, procedure or evidence;
  - `corroboration` — independent factual scaffolding or a qualified challenge;
  - `synthesis` — an explicitly attributed digest inference when useful and permitted. No type is a mandatory quota; no management, moral or motivational synthesis is required.
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

## Counts, continuity and spoilers

Write faithful prose first, then segment it. Historical totals and suggested density bands are not quotas. When the task leaves length to you, choose it and derive `targetModes` from the finished screens. Only a conflict with an explicit user constraint needs clarification; a single requested Deep total does not itself require a separate approval gate for its nested split.

Every deeper screen adds real story, reasoning, cases, procedures or qualifications. Each nested sequence must read coherently, with transitions and causal links intact. Scene/place/action/question titles are valid; titles need not state lessons. Merge repetition rather than splitting prose to hit a number.

Keep the book-specific spoiler policy. For `full-plot-in-deep`, decisive endings belong only in level 3 behind a clear warning/consent. The level-1 final is shared by all modes, so it must remain spoiler-safe. Covers, global source notes, pre-consent contents and saved-resume labels must also remain safe.

## Working checks before build

- Scenes, motives, mechanisms and factual claims are supported by actual consulted evidence; evidence gaps and access boundaries are explicit.
- The Essential sequence is an intelligible story/argument on its own, respecting its spoiler promise.
- Core and Deep preserve Essential order and causal continuity while adding meaningful content.
- No invented scenes, dialogue, examples, motives or compulsory lessons; no quota padding.
- RU/EN preserve names, quantities, events, qualifications and spoiler boundaries.
- The method note describes actual reading/verification, not just a downloaded edition.
- No content was inherited from another book. A structural audit is necessary but does not establish editorial approval.
