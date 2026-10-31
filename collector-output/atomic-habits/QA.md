# Local QA — Atomic Habits

2026-10-31. Implementation self-check; ready for independent content check, not independent PASS or publication.

- Previous assigned collector/root edition: absent at intake; old pairs read 0. New authoring pairs reviewed: 24 RU/EN (48 copies). Read the whole resulting explanatory sequence at each nested depth.
- Exact counts: 13/20/24, including cover and final, derived after prose. Defaults RU/dark/Essential; `contentMode: explanatory`.
- Canonical `screens` equal effective embedded HTML `screens` exactly. Maintained audit: 69 checks, zero failures/warnings. Sources dialog retains all 18 source records and honest scope.
- `build-sol.mjs` invokes the maintained builder, then applies book-local CSS hiding only repetitive source footers. No shared shell or root changes. No copied reader corpus.
- Offline Chrome at 320×568, 390×844, 1024×768 and 1440×900; every screen in RU/EN and light/dark, all mode counts. Embedded fonts loaded, no external runtime requests, exceptions or horizontal overflow.
- Tested dialogs, language/position preservation, stored screen ID, keyboard focus toggle, visible Next in focus, desktop rail, home href, one icon-only header row with labels. Screenshots saved in `qa/`; representative mobile/desktop frames inspected.
- Each browser invocation: timeout 30, unique mkdtemp profile, owned detached process-group kill and profile removal in finally. No server started.
- Not verified: a physical iPhone/PWA, touch gestures, deployed/root-reader integration. Local structure/automation does not prove editorial fidelity.

Reproduce: `python3 author-sol.py`; `node build-sol.mjs`; maintained `audit_story_html.mjs … --min-screens 24 --require-bilingual`; `node browser-qa-sol.mjs <width>`.

Final local scroll check, 2026-10-31: every body’s last paragraph was reachable by vertical scrolling at all four widths in both languages/themes. Screenshots were recaptured after the transition finished. Four refreshed browser reports record `bodyScrollReachable: true`.
