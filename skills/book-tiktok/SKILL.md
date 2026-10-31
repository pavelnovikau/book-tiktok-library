---
name: book-tiktok
description: Research a book and build a faithful, engaging standalone HTML book story ("книго-тикток") for phone and desktop, with nested reading depths, RU/EN switching, and Flexoki light/dark themes. Use for swipeable book digests and bedtime reading; not for reproducing copyrighted full text or ordinary prose summaries.
---

# Book TikTok

Turn a book into a compact interactive reading experience in original words. Choose the writing approach from the actual work: tell a novel’s story, explain a nonfiction argument, and retain a practical book’s real procedures. A hybrid keeps its narrative and ideas in their original relationship. Write connected, engaging prose first; segment it into mobile screens afterwards.

Resolve `<skill-dir>` in commands below to the directory containing this `SKILL.md`. Do not assume a particular username or Codex home path.

## Establish the brief

- Identify the exact book from the request, cover, ISBN, or attached file. Verify ambiguous editions before writing.
- Honor the requested language, depth, destination, and visual system. For a Russian-language request, default to Russian and provide English through the toggle unless the user says otherwise.
- Honor an explicit length/depth constraint. Otherwise choose a justified length from the book and the current task; no count-confirmation gate is needed when the task leaves that choice to you. Ask only if a material conflict cannot be resolved from the brief.
- Historical screen totals are not quotas. After writing and segmentation, derive the exact cumulative Essential/Core/Deep counts, including cover and final, and record them in `targetModes`. If an explicit numerical constraint would force padding or remove essential material, explain the conflict before changing that constraint.
- If no output location is given, use `_artifacts/<book-slug>-book-tiktok/<book-slug>.html`. A descriptive filename is part of the deliverable; do not default to `index.html`.
- Treat delivery or publication as a separate action. Create the file without posting it externally unless the user explicitly authorizes that destination.

## Research and model the book

Read [references/content-model.md](references/content-model.md) before researching, outlining, or translating.

- Use user-provided or lawfully accessible book text when available. For a copyrighted book, do not hunt for pirated copies or imply that the full text was read when it was not.
- Identify the edition and evidence boundary. A downloaded complete edition, consulted passages, and a continuous full reading are different claims. Check that an EPUB is the work itself rather than an abridgment or a summary.
- For fiction, map characters, relationships, established motives, events, causality, atmosphere and unresolved tension against the primary text. Scenes must carry the story. Do not replace it with leadership, management, psychology or moral lessons; invent no scenes, dialogue or motives.
- For explanatory nonfiction, map the author’s main ideas, reasoning, real cases, qualifications and disagreement. For practical works, preserve the actual procedures and their limits. Independent fact checks may qualify a claim, but must not silently replace the author’s argument.
- Keep screen source IDs and honest attribution. `book` covers the author’s narrative as well as argument; `corroboration` and `synthesis` are available when actually needed, never mandatory quotas. No invented quotations, page references or definitive authorial intentions.
- If the accessible sources cannot support a faithful account, report the specific source gap rather than reconstructing the book from a blurb or reviews.

## Write, then segment

- Draft coherent prose in the appropriate form before dividing it into screens. Titles may name a scene, place, action or question; they need not state an abstract lesson.
- Use nested depths so Essential ⊂ Core ⊂ Deep. Read each sequence continuously: preserve the story/argument, transitions and causal links at every depth.
- Each extra screen must add meaningful book content. Merge repetition; do not stretch or split text to meet a quota. No mandatory motivational ending, durable mental model, application, management or moral synthesis.
- Preserve the book-specific spoiler promise. Decisive fictional endings belong only in Deep after clear consent when that is the agreed policy. Covers, Essential/Core, the shared final screen, resume labels and global source/method notes must respect the same boundary.
- Set `contentMode: "narrative"` only for genuinely narrative prose; use `"explanatory"` for explanatory/practical prose. This selects presentation, not editorial approval. Relabeling an unchanged analytical novel does not repair it. Legacy data without the field remains supported.

The exact count and source-map assertions are in [references/data-contract.md](references/data-contract.md).

## Build from clean structured data

For a new artifact, read [references/data-contract.md](references/data-contract.md) and [references/html-spec.md](references/html-spec.md).

- Write `story-data.json` using schema v2. Do not copy a previously generated book HTML; that leaks old content, images, and counts into the next artifact.
- Keep one stable screen ID, level, provenance type, source list, and media assignment across RU and EN.
- Build the portable HTML with the maintained shell:

```bash
node <skill-dir>/scripts/build_story.mjs story-data.json \
  --out <book-slug>.html
```

- The builder validates structure, resolves local images, embeds Geist Sans, Geist Mono, Geist Serif and the Source Serif 4 Cyrillic fallback with their licenses, computes mode counts and reading times, and produces one network-independent HTML file.
- Include a concise, spoiler-safe method/source disclosure describing what was actually read and checked. Narrative reading hides per-screen provenance/footnote chrome while retaining screen source maps and the accessible global Sources dialog.

The shared Settings gear replaces the theme toggle in the existing icon row. Use [references/reader-settings.md](references/reader-settings.md) for the global theme/reading-font contract, verified font coverage, legacy adapters and no-server QA. Keep UI controls Sans and the localized Serif fallback note visible. Never rebuild a released custom runtime merely to update its shell; synchronize it.

## Verify and hand off

Run the deterministic audit:

```bash
node <skill-dir>/scripts/audit_story_html.mjs <book-slug>.html \
  --min-screens <justified-minimum> --require-bilingual
```

Read the actual RU/EN prose and cross-check its scenes, mechanisms and qualifications against the evidence; a structural pass is not editorial approval. Then perform real-browser QA according to [references/html-spec.md](references/html-spec.md):

- programmatically traverse every screen in RU and EN and verify exact Essential/Core/Deep counts;
- inspect representative dense, list, image, comparison, cover, and final screens visually;
- test 320×568, 390×844, 1024×768, and 1440×900 in light and dark;
- verify language/position preservation, dialogs, fonts/images, keyboard/buttons/swipe, desktop rail, and zero horizontal overflow/runtime exceptions.

Report the final file path, exact mode counts, approximate reading times and word density, default language, standalone status, source count, QA result, and what was or was not delivered externally.
