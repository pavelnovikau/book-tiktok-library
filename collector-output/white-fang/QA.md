# White Fang — implementation QA

**Parent status, 2026-10-31:** independent cold review completed, all required findings repaired, fresh audit and targeted browser checks passed. Ready for catalogue integration; not published. Collector-stage notes/fingerprints are retained below, with the final repair record at the end.


2026-10-31. **Candidate for parent cold editorial review; not independently reviewed, integrated, published, or deployed.**

## Deliverable

Exactly four canonical files: `story-data.json`, `white-fang.html`, `sources.md`, `QA.md`. Reader defaults: **RU / dark / Essential**. Audience: **teen-14-plus**. One original abstract vector cover, embedded in the JSON/HTML. No publisher art, film stills, source-book file, or copied modern translation. Final HTML: **402,053 bytes**.

| Mode | Screens, cumulative | RU words | EN words | RU estimate | EN estimate |
|---|---:|---:|---:|---:|---:|
| Essential | 24 | 1,245 | 1,475 | 7 min | 7 min |
| Core | 60 | 3,128 | 3,699 | 18 min | 17 min |
| Deep | 96 | 5,059 | 5,926 | 29 min | 27 min |

Word totals above use the builder's counter: title + cover subtitle + body, excluding section labels and reader chrome. Reading estimates use its default 180 RU / 220 EN words per minute, rounded up; they are reading estimates, not tested completion times. The auditor separately counts title + body (5,051 RU / 5,916 EN), omitting the 8/10-word cover subtitle.

Body-only totals: **4,464 RU / 5,212 EN**. For the 94 ordinary screens (cover/final excluded), RU bodies have **41–52 words, mean 46.69**; EN **50–63, mean 54.50**. All are within the 35–75 target. Level distribution is **24 / 36 / 36**; cover and final are level 1. Non-cover provenance: **58 book / 1 corroboration / 36 synthesis**. All factual screens carry source IDs; per-screen evidence locators and distinct cognitive jobs are in JSON. The spoiler-warning screen has no factual source claim.

## Evidence and editorial boundary

**Six sources**, including the complete lawfully accessible English Gutenberg #910 edition and selected passages of London's own essay. Actual book reading was **selective close reading across all five parts**, not a continuous full-book read. Full access does not imply full reading. Exact coverage, excluded discovery sources, references and interpretation limits are recorded in `sources.md`. The two independent scholarly sources were used only through explicitly labelled publisher/indexed abstracts; neither full article/chapter was read. No scientific validation of canine cognition or training is claimed.

The claim/plot/theme map and source ledger were written before the screen corpus. This is an original analytical companion, not a chapter-by-chapter text replacement. RU is newly written analytical copy, paired with EN; no published Russian translation was used. Part/chapter locators follow the consulted English edition and no page numbers or dialogue are invented.

Essential remains a coherent invitation and explanation of hunger, learning, exclusion, power, spectacle and critical reading. Core adds early/middle evidence and qualifications. Both stop before the decisive IV.IV turn. Deep adds eight early close readings plus 28 late screens: `deep-spoiler-warning` at absolute screen 67 precedes all IV.IV–V.V disclosures. Every late section is labelled Deep/spoilers; late titles avoid disclosing outcomes. The level-1 closing screens stay spoiler-safe in every mode. Global Sources and method notes contain no late character, rescue, final setting, verdict, survival, or family outcome. External full-text links are optional and explicitly warned as potentially revealing plot.

Violence, killing, abuse and organised fighting are acknowledged without reproducing graphic detail. Racial hierarchy, physiognomy, inherited-memory and sex-based explanations are identified as narration requiring critical distance. Human morality is not derived from canine biology; literary cause is distinguished from ethical permission and from real-world handling advice.

## Maintained build and deterministic audit

Built directly from schema v2 with the current shared builder and template, including the maintained `reader-header.html`. No shell fork, injected private UI patch, shared-template edit, root-reader change, catalogue change, git action, PR, deployment or LOG update was performed.

```sh
node skills/book-tiktok/scripts/build_story.mjs collector-output/white-fang/story-data.json --out collector-output/white-fang/white-fang.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/white-fang/white-fang.html --min-screens 96 --require-bilingual
```

Final deterministic result: **68 passes, 0 warnings, 0 failures**. Exact nested counts, bilingual corpus, stable unique IDs, source references, provenance, embedded media/fonts and offline runtime invariants passed.

## Collector-stage real-browser matrix (before parent repairs)

Installed Google Chrome in real headless mode, automated directly through CDP, loading the local `file://` HTML. No preview tools or content server. Network was put offline for page QA. No external HTTP request, runtime exception or unexplained error was observed in the final runs.

Every viewport tested both RU/EN and dark/light and traversed all three modes: 24 + 60 + 96 = **180 screen visits per combination**. Final matrix: **16 combinations / 2,880 visits**. The full matrix was rerun after the final provenance corrections.

| Viewport | Combinations | Visits | Document X/Y overflow | Slide X overflow | Header rows |
|---|---:|---:|---:|---:|---:|
| 320 × 568 | 4 | 720 | 0 / 0 px | 0 px | 1 |
| 390 × 844 | 4 | 720 | 0 / 0 px | 0 px | 1 |
| 1024 × 768 | 4 | 720 | 0 / 0 px | 0 px | 1 |
| 1440 × 900 | 4 | 720 | 0 / 0 px | 0 px | 1 |

Per visit: exact expected title/counter, reachable stable ID, document width/height, slide scroll width, rail presence and active-entry synchronisation/containment. Covers additionally checked layout and each cover child's left/right containment inside the slide, rather than trusting document overflow alone. Embedded cover decoded; Geist and Geist Mono passed font checks. All visible top controls had a localised aria-label and tooltip, contained an SVG and no visible text; the home target is `./`.

**Intentional vertical reading scroll remains** on smaller viewports, as required by the shared reading shell. Maximum observed vertical scroll range (including cover): 410 px at 320, 145 px at 390, 275 px at 1024, zero at 1440. This is contained slide scrolling, not document or horizontal overflow. The last content/provenance element was tested reachable by scrolling to the bottom in each interaction viewport. This QA does not claim that every mobile card fits without vertical scrolling.

## Targeted interaction QA

Repeated at all four viewports, starting RU/dark and switching to EN/light:

- Native pointer tap on cover text enters focus; the cover's Next remains available. Native Next enters the reading sequence and preserves focus. Escape exits after Next. F works while Next retains focus; Escape restores the shell.
- Native Space on focused Next advances exactly one screen; on language/theme it activates the control while preserving position; on Chapters/Sources it opens the corresponding native dialog without paging; on Home it does not page. Space with body focus advances. Back returns correctly.
- Native horizontal pointer swipe pages without being read as a focus tap. Vertical movement does not page or toggle focus. An existing text selection prevents a text tap from entering focus. F inside an open source dialog is ignored.
- Chapters navigates by stable ID; desktop rail stays active and in view. Sources and Contents open/close, including Escape. Reader position survives language/theme changes.
- Reload offers Continue and Start over. Continue restores the saved Deep ID, EN and light theme. When the saved ID is hidden by Essential, Continue raises depth to Deep and reaches that ID. Start over goes to the first ordinary screen. Final Restart clears saved progress and returns to the cover.

At 320 × 568 under iPhone Safari user-agent emulation: the install guide opens once in browser mode, includes the inability of a site to remove Safari chrome itself, Share / Add to Home Screen and relaunching from Home Screen rather than Telegram. It localises to EN, opens manually from the icon in the same header row, closes and stays suppressed in focus. Exiting focus restores the trigger; reload does not reopen the once-seen guide. With `navigator.standalone = true`, both guide and trigger remain absent.

**Platform limit:** those were iOS browser/standalone signals emulated in Chrome, not a physical iPhone, Safari engine, or an actually installed Home Screen application. No fullscreen capability is claimed for an ordinary Safari tab.

Six representative screenshots were visually inspected: 320 RU/dark cover, 390 EN/light comparison, 1024 RU/light cover, 1440 EN/dark cover, 320 RU/light three-question list and 1440 RU/dark late prose. Header row, text measure, scrolling, cover containment, source labels and rail were checked. No independent editorial review is claimed.

## Collector-stage cleanup and fingerprints

Every manually launched Chrome used `timeout 30`, a unique temporary profile and a separately allocated CDP port. Each owned process group and remaining descendants were terminated in `finally`, and its profile removed, also on failures. No Vite/HMR/content server was started. Scratch scripts, source download, reports and screenshots were outside the repo and removed after extracting this report. Only the four canonical files remain in the owned directory.

| File | SHA-256 |
|---|---|
| `collector-output/white-fang/story-data.json` | `5df731b8e91c535a435eee103cf36232faa1974b03f121d26df53caa38dd54de` |
| `collector-output/white-fang/white-fang.html` | `7d4b62f7f04b471fe41d266f9a4baf1491c687b61d888cdc073c30ce5711ff9b` |
| `skills/book-tiktok/scripts/build_story.mjs` | `f0a5e65358aa159f9cc64266ff9629cc80fbe392a3f52025a25ce909f6c08c3b` |
| `skills/book-tiktok/assets/standalone-template.html` | `690b5beae668868566c7680ebfed5f59736b49506bdee09b4046247a8d13e724` |
| `skills/book-tiktok/assets/reader-header.html` | `0947f8417d61e5d8944e9ec010defef2bba747e5dc8583436ce4cf2729881623` |

These fingerprints identify the final candidate and the exact maintained assets used. Parent owns independent cold review and integration.

## Independent cold review and parent repairs — 2026-10-31

Fresh independent review read all 96 RU/EN pairs and returned READY WITH FIXES. Parent applied both required findings: neutralized the three Deep titles exposed through Continue, and corrected maternal-cost so feeding the surviving wolf cub is distinguished from the lynx losing her entire litter. The latter was checked against primary II.5. Counts and source-access limits are unchanged.

The Continue regression passed 96 lower-depth/saved-Deep combinations, plus 16 maternal-body states. After the generic source-role wording update, targeted final-build QA passed 64 changed-screen states and 16 source-panel states across 320/390/1024/1440, RU/EN and both themes. Continue retains its saved target and raises depth; text bottoms stay reachable. Exact raw source-role labels were separately checked. No runtime errors, external requests or horizontal overflow. These are targeted post-repair checks; the 2,880-visit collector matrix was not repeated.

Current SHA-256: JSON `986d6b1c943f04dd9d051c38fa41eadaccf609df83e2ffab5de5bd2a9f95d869`; HTML `9d48a54e8f33c75fcef2bc7551d82b3a1bbc7566f851e221396d3e0d238edb56`; shared template `373caac52171dd92c0de3048dd6d59b08a627c7fcd0b998f8aceda6f345d69f1`. Earlier fingerprints and broad matrices above identify the collector stage, not a claim of repeating that entire matrix after these localized repairs.

Ready for parent catalogue integration. No publication is claimed. Owned Chrome processes/profiles were cleaned; no server was started.
