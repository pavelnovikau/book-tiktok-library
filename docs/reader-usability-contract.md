# Reader navigation integration

The public library starts fresh readers in Deep, the longest complete version. Saved deliberate mode choices remain valid; language, global reading font/theme and progress use their existing keys. `defaultMode`, runtime fallback, startup, cover Start and Restart must agree. Selecting Deep and giving permission to reveal a fiction ending are separate states.

`skills/book-tiktok/scripts/reader-usability.mjs` maintains the integration. The portable builder applies `repairReader` after settings integration. `npm run check` and `npm run build:site` assert the contract for every registered reader. Do not rebuild released stories from historical candidates to update their shell. For an already integrated reader, preserve the integration or fail validation; the repair is idempotent.

A service notice is not a story page. Remove only explicitly verified service IDs from serialized screens/routes. Never delete story IDs by an `intro`, `warning`, or `gate` substring. Notices must not count toward reading progress or Contents. Retained serialized story records, source/method records, media, mode reading times and route order remain exact. Screen-count metadata and catalogue counts use stored screen records minus title-only units grouped at runtime; they never sum the bilingual routes.

A title-only unit may be grouped only when it has `headingLevel: 1`, empty RU and EN bodies, and an immediately following same-route unit with real prose in both languages. Keep both serialized units. Render the exact prefix title before the next exact heading and body within one step; omit the title's separate Contents entry and navigation count. Old title IDs resolve to the following prose unit. Do not apply this rule to a title unit containing prose.

Independent versions stay independent (`routes` arrays, `screenIds` route metadata, or explicit `routeMode`). Cumulative level readers retain their existing nesting semantics. Do not replace an independent route with a level filter.

Readers that require Deep consent keep one document-local generic RU/EN dialog: “Полная версия раскрывает развязку. Читать?” / “The full version reveals the ending. Read on?” The cover can select Deep without consent. Start, Contents, hash/query entry and saved Continue gate entry into Deep prose. No spoiler-bearing full-screen notice follows acceptance. Reload, restored documents and lowering depth revoke permission. Pending entry is cleared on cancellation; cancel must not downgrade the selected default. Before permission, Contents and Continue labels must not disclose late plot titles. Storage never grants consent.

Old removed service IDs redirect to the first prose in their original mode. Unknown IDs resolve safely. Explicit `#mode/id`, legacy `#id`, `?mode=…&screen=…`, saved Continue and browser history must not bypass the gate. Generated current hashes include the selected mode and actual prose ID. Restart returns to the cover with the same selected mode.

For future changes, test fresh Deep/first prose across the registered fleet and exercise distinct runtime families for consent, reload, lowering depth, Contents, old service/title IDs, saved late Continue and history. Include narrow mobile and desktop/Serif checks. Preserve raw failures and state the actual browser coverage; emulated Chrome is not physical Safari.
