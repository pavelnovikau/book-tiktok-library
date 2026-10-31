# Amphibian Man — narrative repair self-check, 2026-10-31

Status: ready for independent editorial check, **not publication certification**. The old analytical companion's green review is superseded. Only the four local canonical files and this book's audit/manifest were changed.

Read all 96 original RU/EN pairs and compared their embedded collector HTML corpus: exact screen equality. No root reader/catalogue record exists for this slug. Rewrote all 35 final pairs, then reread them in their three nested sequences. Final counts **12 Essential / 19 Core / 35 Deep**, versus 24/60/96. Defaults RU/dark/Essential, bilingual parity, `contentMode: narrative`. One primary source, one retained original embedded cover. Chapters/locators and the actual primary reading boundary are in sources.md; this is not certification of every word or textual variant in the book.

Self-check covered causality, named people/relationships, gift/refusal, the false letter, capture/escape chain, unresolved paternity, restricted bodily prognosis and the unshown arrival. Early paths do not disclose marriage, paternity claim, trial, guardianship, escape or epilogue. Deep's `spoiler-warning` precedes all 15 later narrative screens. Source notes and final remain spoiler-safe. No reader exercise or per-screen “Синтез” / “Аргумент книги” labels remain in rendered narrative.

Maintained commands:

```
node skills/book-tiktok/scripts/build_story.mjs collector-output/amphibian-man/story-data.json --out collector-output/amphibian-man/amphibian-man.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/amphibian-man/amphibian-man.html --min-screens 3 --require-bilingual
```

Result: **69 structural passes, no warnings/failures**. This is structural evidence only. Built 300,772-byte standalone HTML; 1,684 RU / 2,003 EN words including cover subtitle/titles. Auditor excludes three subtitle words.

Actual Chrome CDP check ran the generated `file://` artifact, with no server: **528 screen render instances**, every mode × RU/EN × dark/light at **320×568 and 1440×900**. Expected contents counts matched; each expected screen title and body rendered; no document/text horizontal overflow; Sources dialog opened; no academic source footer in narrative; no runtime exceptions or remote HTTP requests. All 16 Deep IDs were checked through **64 saved-return paths** (RU/EN × Essential/Core): the generic spoiler warning masked the title, hidden entries stayed out of contents, Continue raised the depth and opened the correct body, and final Restart cleared saved progress. Narrow screenshot visually inspected. A Chrome process under `/usr/bin/timeout 30` used a unique mkdtemp profile; its owned process group was killed and the profile deleted in finally. No other process was touched.

Private harness/results/screenshots: `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-4-private/qa-amphibian-man/`. This check is desktop Chrome emulating viewport sizes, not a physical iPhone/PWA test. No root-shell/header fixes or production checks are claimed. File hashes belong in the separate ready manifest after these records are finalized.


## Parent meaning corrections — 2026-10-31

Parent applied the two required independent-content findings AMP-01 and AMP-02 in both languages. Counts remain 12/19/35. Generated embedded corpus and reading estimates refreshed while preserving all existing outer reader code/styles. This is a localized correction awaiting publisher validation, not a new independent PASS. Previous review hashes refer to the earlier two omissions.
