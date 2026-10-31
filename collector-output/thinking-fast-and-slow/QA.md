# Local QA — Thinking, Fast and Slow

2026-10-31, implementation self-check only. Status: ready for independent content check; no publication or independent PASS claimed.

- New addition: no prior assigned collector or root reader existed. Read/reviewed 29 new RU/EN pairs (58 copies), plus each nested sequence. Exact counts: Essential 14, Core 24, Deep 29, including cover/final. No historical quota retained.
- Effective embedded `screens` equal canonical JSON exactly. Defaults RU/dark/Essential; `contentMode: explanatory`.
- Maintained build and deterministic audit: 69 checks, zero warnings/failures. Book-local `build-sol.mjs` calls the maintained builder and hides only repeated source footers; source maps and Sources dialog remain intact. No shared shell edits.
- Offline Chrome file loading at 320×568, 390×844, 1024×768, 1440×900. Every screen traversed in both languages and themes at every viewport; all three mode counts checked. No remote runtime requests, JS exceptions or horizontal overflow. Embedded fonts loaded.
- Checked icon-only single header row with accessible labels, Sources/Contents dialogs, language and saved screen ID, keyboard focus toggle, visible Next in focus, desktop rail and home href. Representative screenshots in `qa/`; 320px dense-screen screenshot visually inspected.
- Browser processes: each run used `/usr/bin/timeout 30`, its own mkdtemp profile and detached process group; finally killed that group and removed that profile. No server was started.
- Physical iPhone/PWA displacement, production integration and touch gesture checks were not performed here. Existing shared shell behavior is not certified by this local test.

Commands: `python3 author-sol.py`; `node build-sol.mjs`; maintained `audit_story_html.mjs … --min-screens 29 --require-bilingual`; `node browser-qa-sol.mjs <width>`.

Final local scroll check, 2026-10-31: every body’s last paragraph was reachable by vertical scrolling at all four widths in both languages/themes. Screenshots were recaptured after the transition finished. Four refreshed browser reports record `bodyScrollReachable: true`.


## Parent correction — 2026-10-31

Applied KAH-01, KAH-02. Only embedded data and derived reading estimates were refreshed; outer reader code/styles are byte-identical. Original independent review remains unchanged. Publisher validation is required before acceptance.

Focused parent regression passed: exact changed copies, body-tail reachability, no horizontal overflow, no runtime exceptions and no remote requests at 320/390/768/1440 px across RU/EN and both themes. Meadows also exposes the distinct archive link and exact scoped note in Sources. Combined report: 88 assertions; owned Chrome process/profile cleaned. Not a physical iPhone/PWA or independent content certification.
