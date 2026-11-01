# White Fang depth-v2 — QA and handoff

Status: `ready-for-root-personal-check`. `publicationAllowed=false`; `rootPersonalAcceptance=false`.

Candidate only; defaults RU / dark / Essential / Sans. One standalone offline HTML, no content server or runtime network dependencies. One primary source, no external image dependency. The typographic cover uses the embedded fonts.

| Cumulative route | All screens | Narrative paragraphs | RU narrative words | EN narrative words | Body reading RU / EN |
|---|---:|---:|---:|---:|---|
| Essential / Главное | 32 | 30 | 2,878 | 3,578 | 15.99 / 16.26min |
| Core / Подробнее | 50 | 48 | 4,556 | 5,676 | 25.31 / 25.80min |
| Deep / Глубоко | 88 | 85 | 8,123 | 10,009 | 45.13 / 45.50min |

Counts include cover/final; Deep also contains one warning. All 25 source chapters are represented in the full route. Short routes stop at Cherokee’s arrival; the fight’s outcome and later resolution are only in Deep after consent. Complete coverage/omissions are in chapter-scene-map.md.

Framing body words, separately: RU67/67/98, EN80/80/114. Title/subtitle words: RU91/139/241, EN116/183/323. Framing plus headings take about0.88/1.14/1.88 RU minutes and0.89/1.20/1.99 EN minutes. Section labels are counted separately in metrics.json (including their own minute totals) and excluded by the maintained reading-time calculation. Builder totals including titles/subtitles/body are RU3036/4762/8462 and EN3774/5939/10446; interface estimates are RU17/27/48 and EN18/27/48 minutes. UI controls, Sources and Settings are not narrative reading time. Narrative density is81–109 RU and94–136 EN words per paragraph. Counts describe the result, not its quality.

`review-package.mjs` verified all85 complete RU/EN paragraphs against both connected drafts, canonical JSON and the actual embedded HTML corpus, plus actual paragraph counts on all88 pairs, nested IDs, shared short stopping point, warning position and true last scene. `qa/structural-parity.json` binds the inputs. All85 narrative units have primary source1; cover/warning/final are explicitly framing.

Maintained deterministic audit, final artifact: **69 passes, no warnings/failures** (`qa/audit-final.json`). Command:

```
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs white-fang.html --min-screens 88 --require-bilingual
```

The minimum is the count derived from the finished draft, not a target used to produce it. Builder and shared skill files remained read-only; build-record.json records their exact hashes and the book-local patches.

Browser QA used actual offline `file://` loads in headless Chrome, with the network emulated offline and runtime request/exception collection. Each phase owns a unique `mkdtemp` profile and detached process group, runs Chrome under `timeout 30`, and removes its entire group/profile in `finally`, including failure. Final `qa/cleanup.json` verifies no owned Chrome instance or profile remains. No content server, publication or shared browser tab was used.

- Four matrices:320×568,390×844,1024×768,1440×900; RU/EN × dark/light × Sans/Serif × all three complete routes. **5,440 rendered screen instances**, exact paragraph/title/route/progress checks, no horizontal overflow, no academic footnotes in narrative mode, depth-filtered Sources/contents. Exact candidate hashes are in every final browser report.
- Additional tail pass: **2,720 actual last-character visibility checks** across all85 narrative paragraphs, four dimensions, two languages, two themes and two fonts. Dense EN bottom scrolling and RU Serif text were also visually inspected.
- Font inspection uses Chrome’s actual platform-font records on real paragraphs: embedded Geist Sans, Latin Geist Serif and Cyrillic Source Serif4 as appropriate. Settings discloses the Cyrillic fallback. All licenses/fonts travel in the HTML.
- **152 saved Deep entry paths**: every level3 ID × RU/EN × both lower modes. Each requires fresh consent, preserves content on cancel and resumes the exact target after confirmation.
- Four real downgrade paths revoke consent; cover depth controls, final entry, stale contents/desktop-rail references, actual reload after acceptance, saved Deep mode, invalid old IDs, safe progress resume and BFCache restoration were checked. Contents, cover/Continue, Sources and shared final remain generic before consent. Consent is never stored and is revoked by lowering depth or document replacement.
- Legacy short-reader keys cannot reopen this candidate. Global light/Serif preferences survive while old progress stays untouched. Language, Settings and focus preserve reading state; restart clears the saved position. Buttons, Arrow/Page/Space keys and horizontal pointer paging work; vertical pointer motion does not page.
- Native Settings Tab stays inside the modal over12 steps; Escape closes and returns focus to the gear. A30px top /12px side inset emulation keeps all five icon controls inside one row. Desktop rail remains scrollable and its active chapter visible after phone-to-desktop resize. These asynchronous checks sample after a Chrome paint; unpainted timing samples were not treated as final evidence.
- iPhone user-agent and standalone emulation checked the localized install guide, its focus-mode suppression and its absence in standalone. **No physical iPhone, Safari or installed-PWA claim.**

Final browser reports: `browser-320.json`, `browser-390.json`, `browser-1024.json`, `browser-1440.json`, `browser-tails.json`, `browser-consent.json`, `browser-entries.json`, `browser-controls.json`, `browser-ios.json` in qa/. All completed with zero runtime exceptions or remote runtime requests.

Reproduce within this directory: `python3 assemble.py`; `node build-candidate.mjs`; `node review-package.mjs`; `python3 write-map.py`; then the audit and `node browser-check.mjs <phase>`. Root should review the exact hashes in ready.json. Rebuilding may change those hashes and requires renewed verification.

Remaining required work belongs to root: complete personal reading of both final languages and every route, coverage/omission comparison and primary checks, then an explicit acceptance decision. This package is not published and structural/browser success is not editorial acceptance. Only this new book-local directory was written; historical collectors, ready/reviews, root HTML/catalogue, global ledger, shared/installed files and other candidates were untouched by this implementation.
