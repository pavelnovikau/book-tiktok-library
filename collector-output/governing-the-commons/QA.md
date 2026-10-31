# Governing the Commons — implementation QA

Status: **ready-for-independent-check**, not independent editorial PASS and not publication approval. Date: 2026-10-31.

## Content and edition

- Target: Elinor Ostrom, *Governing the Commons: The Evolution of Institutions for Collective Action*, Cambridge University Press, 1990, DOI 10.1017/CBO9780511807763.
- New approved queued title; no pre-existing assigned collector delivery/root reader at intake. Old pairs read: 0. New screen pairs read: **33 RU/EN**, including cover/final. The connected draft precedes segmentation and its full prose reconstructs exactly from the Deep body.
- Read each resulting language sequence at Essential, Core and Deep; source notes/method are bilingual. Matched all effective HTML screen bodies, titles, levels, source IDs, method and source notes against authoring JSON. This is an implementation self-check, not independent review or certified translation.
- Counts derived from content: **14 / 24 / 33**, cover/final included. No historical count or screen quota applied. Levels: 14 / 10 / 9.
- Approximate title/subtitle/body words using builder's counter: RU 599 / 939 / 1,275; EN 679 / 1,056 / 1,420. Deep average: about 39 RU / 43 EN words per screen. Reading estimates: RU **4 / 6 / 8 min**; EN **4 / 5 / 7 min**. Standard minutes override fixes Russian `4 минуты`; no settings feature was added.
- All retained concepts/cases map to primary locations in `governing-the-commons-evidence-sol.json` and `sources.md`. Ten reader sources; one additional later-lecture draft checked only to police the 1990 boundary.

## Structure, parity and offline

Maintained tools:

```text
node skills/book-tiktok/scripts/build_story.mjs collector-output/governing-the-commons/story-data.json --out collector-output/governing-the-commons/governing-the-commons.html
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/governing-the-commons/governing-the-commons.html --min-screens 33 --require-bilingual
```

The descriptive HTML uses the maintained current shell. A book-scoped post-build style, `#governing-the-commons-dialog-only-sources`, hides `.source-label` so reading screens have no research footer; maps and the Sources dialog remain. Reapply that presentation at a rebuild, or use the publisher's latest equivalent. This does not change `contentMode: explanatory` or copy/implement the unmerged settings feature in PR 29.

Deterministic audit: **69 structural assertions, 0 failures, 0 warnings**. See `governing-the-commons-structure-sol.json` for the exact artifact hashes. The audit is not a fidelity verdict.

- JSON and effective embedded HTML corpus/source/method parity verified.
- Exact nested Essential ⊂ Core ⊂ Deep membership verified.
- Fresh profile defaults RU / dark / Essential; saved settings respected thereafter.
- Embedded Geist, Geist Mono and typographic SVG cover; no remote runtime dependency.
- Sources in the accessible dialog; per-screen provenance retained in data, hidden in reading presentation.
- Current compact icon-only header with localized labels/tooltips and `href="./"` library contract. Actual root-library navigation awaits publisher integration.

## Real Chrome checks

File opened directly with Chrome network emulation set offline; no HTTP content server. Four viewport runs: **320×568, 390×844, 1024×768, 1440×900**. Each traversed all three modes in RU and EN and both dark/light themes: **284 screen visits per run**. Two additional 390×844 runs emulated iPhone browser and standalone state, also with all 284 visits. Total in the final six reports: **1,704 screen visits**.

Every final browser report records the current HTML and story-data SHA-256. All six hashes were checked against the final files.

Verified programmatically:

- Exact visible counts, expected screen titles and every body against embedded data.
- No horizontal document/body overflow; vertically overflowing text reaches its end.
- Embedded fonts ready and cover decoded.
- Sources and Chapters dialogs open/close; labels localize.
- Position, mode and theme preserved across language switch; saved Continue resumes; Start over and final restart work.
- Real CDP keyboard inputs for navigation/focus; pointer tap toggles focus; horizontal pointer swipe pages; vertical pointer movement is ignored as a tap/page swipe.
- Focus hides header, counter, Back and rail while retaining Next.
- All top controls remain in one icon-only row; desktop rail appears at desktop widths.
- In emulated iPhone browser mode the install guide/trigger appear; in emulated standalone mode both are suppressed. A simulated 47px safe-top variable keeps controls below it.
- Zero captured Runtime exceptions and zero HTTP(S) runtime resource requests in all six runs.

Visually inspected final 320px dense reading, 390px cover, and 1440px cover/dense reading. Long text at 320px scrolls behind the maintained footer; the final paragraph is reachable. The two capture timings used before the final reports were corrected to wait for the shell's entry animation, rather than mistake intermediate opacity for unreadable final text.

Evidence: `governing-the-commons-browser-sol-<width>-<no|browser|standalone>.json`; corresponding `-cover.png`/`-dense.png` for the four ordinary viewport runs. Screenshots of resumed Deep are QA states; fresh default was asserted separately.

Each Chrome instance ran under `timeout 30` with its own `mktemp -d` profile. The runner terminated its process group and remaining processes bearing that unique profile path, then removed that profile in `finally`. Owned Chrome/profile residue count after QA: zero. No server was started. Official source downloads/OCR files were also removed from their separate owned temporary directory.

## Limits and handoff

The complete 1990 edition was not acquired/read continuously. Official first-ten-page text and original chapter openings were combined with identified earlier/contemporaneous/later author material; detailed contents/index verify book connections. The 1988 case procedures and 1992 principles are not certified word-identical to the 1990 body. The reader discloses this boundary. Full irrigation procedures, complete basin histories and every qualification/comparison in unconsulted chapter bodies are not reconstructed.

No physical iPhone/iPad, installed PWA, touch hardware or production/root integration was tested. Pointer and iOS/safe-area emulations are not those tests. Independent content check and publisher integration remain pending; publisher applies the latest maintained shell. No Git, PR, deployment, external messages, shared-shell/installed-skill/root/catalogue/index or shared-log changes were performed.


## Parent correction of independent findings — 2026-10-31

GTC-001: parent checked the publisher’s exposed/indexed opening of original 1990 chapter 6, printed p.182, DOI10.1017/CBO9780511807763.008: each individual system lies within a single country. The book’s sample is not confined to one country. Corrected only the RU scope sentence; EN and all other prose are unchanged. Direct non-abs page timed out; the Cambridge /abs publisher record exposed the actual paragraph through search. This is targeted primary-opening access, not the full chapter or book.

Parent focused regression passed: exact corrected copies and complete scroll-tail reachability at 320/390/768/1440 px across RU/EN and both themes; no horizontal overflow, runtime exception or remote request. Combined 128 assertions in publisher-findings/parent-ostrom-earthsea-toc-history-browser.json. Existing outer runtime/consent code is unchanged. Owned Chrome process/profile removed. Not physical iPhone/PWA testing or independent content acceptance.
