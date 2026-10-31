# The Fifth Discipline — collector QA, 2026-10-31

Status: **ready-for-independent-check**. These are collector self-checks, not an independent editorial PASS or publication approval.

- New approved queued work: no previous assigned collector package or root reader existed when work began. Previous pairs read: 0. New pairs read: **29 RU/EN pairs (58 screens)**. Every depth was checked in its filtered order and the actual HTML routes were traversed.
- Exact basis: Senge’s second edition (2006), consulted in the official 2025 Cornerstone Press reissue sample, ISBN 9781905211203. No matching full or condensed owned EPUB was found. The sample, the author’s complete book-based 1990 article and checked MIT/history passages support this retained central argument. Full-book reading is not claimed; scope and per-screen locations are in `sources.md`.
- Delivery: 29 screens; nested Essential / Core / Deep = **11 / 22 / 29**, cover and final included. Defaults **RU / dark / Essential**, `contentMode: explanatory`. Five source records; one original embedded SVG numeral cover, credited Smartcat, not a copied publisher cover.
- Word totals including titles/subtitles: RU **563 / 1153 / 1538**, EN **675 / 1372 / 1808**. Estimated reading time **4 / 7 / 9 minutes** in each language. Body density: RU median 49, range 28–53 words; EN median 59, range 31–63. Density was measured after writing, not used as a drafting quota.
- Built with the maintained `build_story.mjs`, standalone template and compact header asset. Current deterministic `audit_story_html.mjs --min-screens 29 --require-bilingual`: **69 structural checks, zero failures or warnings**. The minimum records the finished content total; it was not a quota.
- Embedded HTML JSON equals canonical `story-data.json` exactly, including source maps, edition, media and supplied localized reading-time strings. The browser also checked this equality on every phase. No inherited corpus from another book.
- **992 rendered screen checks** = all screens in each actual Essential/Core/Deep route × RU/EN × light/dark × four viewports (320×568, 390×844, 1024×768, 1440×900). Exact title/body/current-ID/counter correspondence; no document or slide horizontal overflow. Embedded Geist, Geist Mono and cover decode checked. Desktop rail visible above the breakpoint, active row synchronized and visible.
- **436 additional browser assertions** across seven phases, including defaults and exact corpus equality. Buttons, Arrow keys, Space, horizontal touch swipe, tap/keyboard focus, Escape, dialog open/close and Sources localization; language/theme preserve position. Reload offers Continue; a remembered hidden level-3 ID raises Essential back to Deep on Continue. Start over and final restart tested; restart clears saved position.
- Emulated iPhone at 390 and 320: install guide automatic/manual entry, localization and close; six icon controls in one row with localized accessible labels/tooltips. With a simulated 47 px top safe-area token, controls remained below it; after vertical touch scroll and focus exit, header remained reachable. Standalone emulation hides guide/trigger. The 320 px Sources dialog stays within the viewport and scrolls. This is Chromium emulation, not a physical iPhone/Safari/PWA test.
- Visually inspected saved cover/prose screenshots at 320 and desktop widths, 1024 cover, focus/final and 320 safe-area/Sources dialog. The 320 px cover uses the maintained vertical-scroll layout; the start/depth controls are below the initial cover fold. Explanatory presentation retains the shell’s small provenance/source footer; no research-report paragraphs follow reading screens.
- Offline throughout: file URLs, CDP network emulation offline, **zero HTTP(S) runtime requests and zero runtime exceptions**. No local server was started.
- Every Chrome instance launched under `/usr/bin/timeout 30` with its own `mkdtemp` profile and detached owned process group. Cleanup killed only that owned group and removed the profile in `finally`; all seven reports confirm profile removal. No persistent Vite/CDP/server process was introduced.

Self-check corrections: fixed the Russian personal-mastery title; moved the four-link-versus-three-link research explanation out of the reading screen into Sources; narrowed the RU simulator title from “does not teach” to “does not guarantee learning” to match the author’s qualification and EN; supplied grammatical `4 минуты` as a per-book data value. No shared code was changed.

Remaining limits: the complete 2006 edition and later cases/chapters were not read continuously; the publisher sample stops at the opening of chapter 3. This condensation does not certify the book’s entire later argument or independently prove the effectiveness of the five disciplines. Independent review, publisher integration, catalogue/root-reader decisions and physical iPhone/PWA testing remain outside this worker’s authority.

Private reproducibility material (authorized PDFs, source-page OCR, browser script/reports and screenshots) is outside the repository: `/var/folders/78/c4cjg2412cjc0sxqpcm986rc0000gn/T/the-fifth-discipline-evidence-jl01pfbo`. Source hashes and direct URLs are in `sources.md`; no private/full source text is in the collector package.

Maintained inputs used for this build:

- `skills/book-tiktok/scripts/build_story.mjs` — `ef38b2a383527cf34cb70d8e5db69e215db810cec6f28edc0f2925f7d5120639`
- `skills/book-tiktok/assets/standalone-template.html` — `2024c323007601a842d0aece92f916a2832b1eb65f9e61c057c960d3932db83b`
- `skills/book-tiktok/assets/reader-header.html` — `0e4a13a63aa6091a0b9c541347406c7624402229eb26a1aa4503ca3834e5b801`
- `skills/book-tiktok/scripts/audit_story_html.mjs` — `36d2dc8ebf8fe55ac37a6fa17362d4c9a99584c9be7f28517e50804c999a0d86`
