---
name: book-tiktok
description: Research an idea-driven book and build a dense, source-backed standalone HTML book story ("книго-тикток") for phone and desktop, with nested reading depths, RU/EN switching, and Flexoki light/dark themes. Use for swipeable book digests and bedtime reading; not for reproducing copyrighted full text or ordinary prose summaries.
---

# Book TikTok

Turn a book into a compact interactive reading experience, not a decorative slide deck. Preserve the author’s actual thesis, causal logic, evidence, qualifications, and consequences while keeping every screen easy to absorb.

Resolve `<skill-dir>` in commands below to the directory containing this `SKILL.md`. Do not assume a particular username or Codex home path.

## Establish the brief

- Identify the exact book from the request, cover, ISBN, or attached file. Verify ambiguous editions before writing.
- Honor the requested language, depth, destination, and visual system. For a Russian-language request, default to Russian and provide English through the toggle unless the user says otherwise.
- **Set screen count with the user before research/build.** If the request does not already give an agreed Essential/Core/Deep triple, offer three book-appropriate options with exact cumulative counts and estimated reading time, mark one as recommended, and wait for the choice. Do not silently choose the density.
- If the user gives only a Deep total such as `96`, propose and confirm the nested split, for example `24/56/96`; one total is not enough for the `targetModes` contract. Counts include the cover and final screens, which are both level 1.
- A useful starting offer for substantial nonfiction is Compact `20/40/60` (about `10/25/40 min`), Full `24/56/90` (about `12/32/55 min`), and Maximum `30/75/120` (about `15/45/75 min`); adjust the actual numbers and time estimates to the book, but always show numbers rather than vague “short/long” labels. If the user explicitly says to decide for them, choose the recommended option and state the chosen counts before proceeding.
- If no output location is given, use `_artifacts/<book-slug>-book-tiktok/<book-slug>.html`. A descriptive filename is part of the deliverable; do not default to `index.html`.
- Treat delivery or publication as a separate action. Create the file without posting it externally unless the user explicitly authorizes that destination.

## Research and model the book

Read [references/content-model.md](references/content-model.md) before researching, outlining, or translating.

- Use user-provided or lawfully accessible book text when available. For a copyrighted book, do not hunt for pirated copies or imply that the full text was read when it was not.
- Triangulate the argument with official publisher material, substantial author interviews, primary historical or technical sources, and serious independent reviews.
- Build a claim map and source ledger before screens: central question, thesis, causal mechanism, evidence, consequences, counterarguments, limitations, and durable mental model.
- Mark each screen as the book’s argument, independent corroboration, or the digest’s synthesis. Keep source IDs attached to factual claims; never invent page numbers, quotations, or certainty.

## Honor the agreed density

- Use nested depths so Essential ⊂ Core ⊂ Deep. Do not create three unrelated summaries.
- Treat the user-approved cumulative counts as the target contract. Record them in `targetModes` and make the builder/auditor enforce them.
- Dense histories, systems books, and handbooks may legitimately need 90–130+ screens; include that option instead of capping the initial offer at 60.
- Each deeper screen must add a mechanism, case, consequence, caveat, application, or synthesis. Never split prose to hit a quota.
- Give each screen one cognitive job. A strong title states the claim; the body earns it.

The planning bands and screen taxonomy are in [references/data-contract.md](references/data-contract.md).

## Build from clean structured data

For a new artifact, read [references/data-contract.md](references/data-contract.md) and [references/html-spec.md](references/html-spec.md).

- Write `story-data.json` using schema v2. Do not copy a previously generated book HTML; that leaks old content, images, and counts into the next artifact.
- Keep one stable screen ID, level, provenance type, source list, and media assignment across RU and EN.
- Build the portable HTML with the maintained shell:

```bash
node <skill-dir>/scripts/build_story.mjs story-data.json \
  --out <book-slug>.html
```

- The builder validates structure, resolves local images, embeds Geist and Geist Mono, computes mode counts and reading times, and produces one network-independent HTML file.
- Include a method/source disclosure so the reader can distinguish the book’s claims from corroboration and synthesis.

## Verify and hand off

Run the deterministic audit:

```bash
node <skill-dir>/scripts/audit_story_html.mjs <book-slug>.html \
  --min-screens <justified-minimum> --require-bilingual
```

Then perform real-browser QA according to [references/html-spec.md](references/html-spec.md):

- programmatically traverse every screen in RU and EN and verify exact Essential/Core/Deep counts;
- inspect representative dense, list, image, comparison, cover, and final screens visually;
- test 320×568, 390×844, 1024×768, and 1440×900 in light and dark;
- verify language/position preservation, dialogs, fonts/images, keyboard/buttons/swipe, desktop rail, and zero horizontal overflow/runtime exceptions.

Report the final file path, exact mode counts, approximate reading times and word density, default language, standalone status, source count, QA result, and what was or was not delivered externally.
