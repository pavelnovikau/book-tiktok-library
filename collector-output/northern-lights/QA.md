# Northern Lights — implementation QA

Status: **ready for independent check**. These are implementation checks, not independent editorial approval or a certificate of whole-book fidelity.

## Artifact and scope

- Four canonical files: `story-data.json`, `northern-lights.html`, `sources.md`, `QA.md`.
- First novel only, Philip Pullman’s *Northern Lights* / *The Golden Compass*; no adaptations or sequels.
- Narrative, RU/dark/Essential by default. Exact cumulative counts **17 / 22 / 43**, levels 17 + 5 + 21. Counts include cover and shared final.
- Five sources, no distributed source text or borrowed cover art. All 41 story scenes use original prose. Typographic cover, embedded Geist/Geist Mono, warm Flexoki light/dark and book-local violet primary action.
- Approximate reading time: RU **5 / 6 / 11 minutes**; EN **5 / 5 / 11 minutes**. Builder word totals (including titles/framing): RU **737 / 919 / 1853**; EN **886 / 1093 / 2224**.
- Story body density: RU mean **40.7**, range **21–64** words; EN mean **48.4**, range **22–80**. Counts were derived after prose, not used as quotas.

## Repeatable build and checks

Run only these scoped commands from the repository root:

```sh
python3 collector-output/northern-lights/segment-manuscript.py
node collector-output/northern-lights/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/northern-lights/northern-lights.html --min-screens 43 --require-bilingual
node collector-output/northern-lights/qa/check-corpus.mjs
node collector-output/northern-lights/qa/browser.mjs mobile
node collector-output/northern-lights/qa/browser.mjs desktop
node collector-output/northern-lights/qa/browser.mjs behaviour
node collector-output/northern-lights/qa/browser.mjs ios
```

The local wrapper invokes the maintained builder; it does not copy another reader. It adds this novel’s volatile Deep consent, neutral locked titles, safe generic Deep Continue label and a text-only narrative cover. It writes only this collector. It does not integrate PR29 settings or modify shared fonts/UI. Build input hashes are in `qa/build.json`.

## Actual results

- Maintained structural audit: **69 checks**, zero warnings/failures. This does not measure literary fidelity.
- Effective embedded HTML corpus equals canonical JSON for screens, source map, method note, counts and policy. Segmenting the 16 connected manuscript paragraphs preserves every story sentence in order in both languages. See `qa/corpus-parity.json`.
- Every one of 43 new RU/EN pairs was read; the 17/22/43 sequences were checked continuously. After narrowing three source/causal formulations and the cover, the changed pairs and shallower sequences were reread. The author’s evidence review is recorded separately from automated tests.
- Real Chromium file navigation, offline **before** load, at **320×568, 390×844, 1024×768 and 1440×900**; both themes, both languages, all three modes, every screen: **1,312 rendered screen checks**, zero horizontal overflow. Mobile and desktop receipts each record 656 traversals.
- Embedded fonts load offline; zero HTTP(S) runtime requests; zero runtime/console exceptions across all four phases. Media/image decoding is not applicable: no raster media is included.
- Header is one compact icon-only row with localized labels/tooltips. Five normal controls fit at 320px; six fit in iPhone browser emulation with the install trigger. A simulated 24px safe-area inset keeps controls below the status area. Desktop rail is present, scrollable, and follows current IDs.
- Buttons, ArrowRight/PageUp, horizontal swipe, vertical non-navigation gesture, tap/keyboard focus toggle, Next in focus, both dialogs, exact counters, language/theme/position preservation, saved progress, Continue, Start over and final restart were exercised.
- Deep picker, direct hidden chapter and saved Deep Continue all require consent. Cancel leaves shallow content intact. Downgrade and reload revoke consent. Shallow contents use neutral locked Deep labels. The remembered ending screen title is not exposed on the cover. Common final and global source/method notes remain spoiler-safe.
- Visually inspected fresh 320px cover (start control visible), dense English prose on light at 320px, desktop rail/prose at 1440px, shared final at 390px, and 320px iPhone safe-area emulation. Screenshots are in `qa/`.
- iPhone browser guide auto-open, manual trigger, English localization and emulated standalone suppression were checked. This is **Chromium emulation**, not physical Safari or a real installed PWA.

All final browser receipts bind to HTML SHA-256 `2be07fd4627e846d6b51314e77aaf6775ae17c9026488638af55fc59d6efd43f`. Every phase launched Chrome through `timeout 30` with its own `mktemp -d` profile and killed its owned process group and removed its profile in cleanup. **No server was started.**

## Limits and ownership

No full primary novel or published Russian translation was read continuously. The final action chain is guide-backed, with checked primary hinges; see `sources.md` and `source-evidence-map.json`. Independent review remains necessary.

`href="./"` is preserved for the publisher’s root-level integration; this collector does not publish a root reader or catalogue entry. Actual library navigation after integration belongs to the publisher. Root/catalogue/index, shared shell/settings/fonts, installed skills, logs and Git/PR/deploy were not edited or invoked. No subagents or external messages.


## Parent local correction — 2026-10-31

NL-001: parent directly read Helen Mason/ZigZag official guide, printed79/PDF84, chapter18 Fog and Ice, declarative summary. The discussion ends with tiredness; the cliff-ghast attack occurs later. Both copies now say Later/Позже without inventing an interruption. No added sleep scene or reordering, new source, level or count. This is guide-supported chronology, not a claim of continuous primary chapter18 reading.

Only embedded data/derived mode estimates and the matching connected manuscript(s) were refreshed. Outer code/styles and bespoke spoiler guards are byte-identical. Older segmentation generators are pre-correction preparation artifacts; the updated story-data.json is the maintained builder input. Original independent review remains unchanged; localized publisher validation is pending, not self-issued PASS.

Parent focused regression completed: 176 assertions across the four corrected readers, RU/EN and 320/390/768/1440 widths with light/dark representative cases. Exact changed copy, scroll tails, no horizontal overflow/runtime/network requests, saved-Deep warning, cancel and accepted restore passed. Ender uses browser confirm; the harness explicitly accepts/dismisses it. Failed harness diagnostic retained separately; no product-runtime correction was needed. Owned Chrome/profile cleaned. Per-reader structural result remains 69 passes. Not physical iPhone/PWA or new independent literary approval.
