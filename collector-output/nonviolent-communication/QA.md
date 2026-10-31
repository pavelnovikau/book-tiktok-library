# Nonviolent Communication — local implementation QA

Status: **ready-for-independent-check**. These are implementation checks and the writer’s own source review, not independent editorial approval or publication.

## Final corpus

- New approved work: no prior collector, root reader or catalogue record existed for this slug. Old pairs read: **0**; newly authored/read RU/EN pairs: **30**.
- `contentMode: explanatory`; default **RU / dark / Essential**.
- Exact cumulative `targetModes`: **16 / 26 / 30**, including cover and shared final. Levels: 16 + 10 + 4. Counts follow the prose; no historical quota, padding or approval gate.
- Maintained-builder word totals including titles: Essential **753 RU / 869 EN**, Core **1,281 / 1,467**, Deep **1,489 / 1,704**. Estimated minutes: RU **5 / 8 / 9**, EN **4 / 7 / 8**.
- Body density: RU 38–66 words, median 44; EN 42–72, median 52. Paragraph prose only; no comparison/list/image screens require separate treatment. No external media.
- Eleven sources, with evidence locators on every screen and a detailed map in `sources.md`. Primary book passages, additional Rosenberg works and Myra Walden’s official CNVC cross-check are distinguished. No full-edition or official-translation fidelity certificate.

## Build and structure

Run `node collector-output/nonviolent-communication/build-local.mjs` from the repository root. This delegates to the maintained `skills/book-tiktok/scripts/build_story.mjs`; it never copies another reader.

The book-local wrapper preserves explanatory semantics and source maps, hides per-screen provenance chrome in favor of the Sources dialog, and removes the generic seven-node analytical cover placeholder. Its small CSS block lives only in this collector and survives rebuilding through the wrapper. Shared builder/template/header files were read, not edited. It preserves the maintained icon header, focus mode, saved progress and iOS guide.

`node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/nonviolent-communication/nonviolent-communication.html --min-screens 30 --require-bilingual` passed **69 checks, zero warnings and zero failures**. Exact JSON/embedded screen, source, method and count parity passed; valid source IDs, stable paired IDs, one cover and one final, strict nested growth and slug-specific storage were checked. See `qa/structure.json` and `qa/corpus-check.json`.

## Actual Chrome checks

`browser-qa.mjs` opens this collector’s standalone `file://` HTML with network offline. Each invocation uses `timeout 30`, a unique `mktemp -d` profile and its own detached process group, then closes the browser, kills the owned group and removes the profile in `finally`. No server was started. Seven final successful reports record the exact tested authoring/HTML SHA-256 hashes; all match this package.

The matrix ran **320×568, 390×844, 1024×768 and 1440×900**, each in **RU/EN × dark/light**. Every nested mode was traversed through real UI handlers: **1,152 screen visits across 16 viewport/language/theme combinations**. Each visit checked rendered title/body against canonical data, exact counter, nonempty content, vertical scroll reachability where needed, zero horizontal overflow, compact single-row icon controls, localized accessible labels and hidden reading-screen source labels. Desktop rail synchronization and active-item visibility passed. Embedded Geist and Geist Mono loaded offline. External HTTP runtime requests: **0**. Reader exceptions/console errors in final runs: **0**.

390px and 1440px interaction runs each passed **22 checks**, including arrows/Page/Space, language/theme position preservation, Sources and Contents dialogs, hidden-target depth raising, F/Escape and pointer focus, retained Next, vertical-gesture exclusion, horizontal swipe, Continue/Start over, final restart and a 47px top-safe-area override.

The 320px iPhone-UA run checked automatic installation guidance, EN localization/manual reopening, six icons in one row, 47px header inset, and hiding the guide/trigger with `navigator.standalone`. This is **Chrome emulation**, not a physical iPhone/Safari/PWA production test.

Representative screenshots were visually inspected: 320px RU dark cover and dense principal case, 1440px EN light cover, and 320px iOS safe-area header. Long prose remains scrollable above the fixed Next controls. Final screenshots and seven reports are under `qa/`. A process/profile check found no owned Chrome processes or `nvc-chrome-*` profiles left behind.

## Editorial self-check and remaining scope

Read all 30 RU/EN pairs as written and compared the effective embedded corpus with the canonical JSON. Read Essential, Core and Deep in order. Corrected an initial EN sock-pair overinterpretation, the implication that an alternative income had already been obtained, an overbroad comparison in Phil’s complaint, and an Essential reference to a case only present in Core. No new anecdote, invented dialogue, therapeutic claim or fabricated page/quotation is retained.

The specific source-sufficiency and edition boundaries are in `sources.md` and the Sources dialog. Continuous complete chapters 4–8, full mediation/counseling procedures and the protective-force school case are not reconstructed. A concise central method and checked cases are offered, not exhaustive coverage of every chapter. This nonfiction has no existing book-specific ending-spoiler promise or consent gate to migrate.

Publisher work remains: independent reading of every revised pair and supporting passages; review of the declared source scope; root reader/catalogue integration; production saved-progress/mobile checks and any release action. No Git/PR/deploy, external message, catalogue/index/root-reader/shared-shell/shared-log edit or subagent was used by this worker.


## Parent meaning corrections — 2026-10-31

Parent applied required independent meaning findings NVC-01, NVC-02 in RU and EN. Changed pairs: two-punishment-questions, reflection-request. Embedded data/derived reading estimates refreshed without replacing outer reader code or styles. This is a localized closure awaiting publisher validation, not a new independent PASS.
