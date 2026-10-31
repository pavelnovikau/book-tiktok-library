# Flowers for Algernon — implementation QA

Status: **ready-for-independent-check**. Implementation self-check only; no independent editorial approval or publication is implied.

- Target: Daniel Keyes, 1966 novel. `contentMode: narrative`.
- Canonical pairs read: **34 RU/EN pairs**, including cover and shared final; resulting nested sequences reread for continuity. The actual effective HTML corpus was read, not only authoring data.
- Exact cumulative counts including cover/final: **14 Essential / 22 Core / 34 Deep** (levels 14 / 8 / 12). Counts follow the prose; no quota was inherited from another book.
- Reading estimates: RU **4 / 7 / 10 minutes**; EN **4 / 6 / 10 minutes**. Maintained builder word totals (including titles/cover) are in `evidence/build-result.json`.
- Body density, RU: 39–60 words, median 48.5; EN: 44–68 words, median 54.5.
- Sources: **22 scoped entries**, not 22 full editions. Three are author pages/interview; the primary novel passages were consulted as quotations within guides. Full source boundary: `sources.md` and `evidence/source-review.md`.
- Maintained builder and template used. Only this generated reader receives the local cover and Deep-consent corrections in `evidence/build-local.mjs`; shared shell/Global Settings work is untouched.
- Final HTML SHA-256: `77dab3112a1a907fd0856acaf73ac3fc38a98fa4ee84a248f38d1f6ce48c4f97`.
- Story data SHA-256: `e879a91a337e47d6019e6b58a0e16b318ed057f0096f4f76f1b786b7d316886f`.

## Checks run on this exact build

1. Maintained v2 audit: **69 passes, 0 warnings, 0 failures** (`evidence/structural-audit.txt`).
2. Exact embedded-screen/source/method parity with canonical data; count assertions and unique screen IDs (`evidence/integrity.json`).
3. Chrome file:// navigation with network offline: **1,120 screen visits** across all three modes, both languages and both themes at **320×568, 390×844, 1024×768 and 1440×900**. No horizontal overflow, incorrect titles/counters or inline provenance in narrative mode. Both embedded fonts loaded. Chapter rail, compact icon controls, localized labels, Sources and Contents checked. Results: `evidence/browser-320.json`, `browser-390.json`, `browser-1024.json`, `browser-1440.json`.
4. Deep warning from cover and contents; cancel and Escape preserve mode/position. Reload with saved Deep ID starts safely in Essential and uses a generic resume label. Continue requires new document-local consent, then restores the saved ID. Language/theme preserve position; final restart clears progress. Keyboard, horizontal swipe, vertical gesture and real text taps into/out of focus checked (`evidence/browser-behavior.json`).
5. iPhone browser emulation: install guide, six icon controls in one row below an emulated 24px status inset, then standalone suppression. This is **not physical iOS/Safari testing** (`evidence/browser-ios.json`).
6. **0 runtime exceptions, 0 HTTP runtime requests**. No server was started. Each Chrome launch used `/usr/bin/timeout 30`, its own `mktemp -d` profile and owned-process-group cleanup. Profiles removed; no owned Chrome process remained.
7. Visual inspection: 320 RU/dark cover, 320 EN/light dense prose, 1440 RU/dark cover and 1440 EN/light prose. Screenshots are in `evidence/`. No horizontal clipping; dense prose is readable and Next remains available. No list/image/comparison screens were fabricated for test coverage.

The browser harness initially needed to wait for the maintained header MutationObserver, await native Escape closure and measure hidden-parent geometry correctly. These were test corrections, not shared UI changes. An undefined cover-size token was replaced with the maintained `--text-4xl`; grammatical minute labels were supplied via local data.

## Reproduction (owned package only)

```sh
python3 collector-output/flowers-for-algernon/evidence/author.py
node collector-output/flowers-for-algernon/evidence/build-local.mjs
node skills/book-tiktok/scripts/audit_story_html.mjs collector-output/flowers-for-algernon/flowers-for-algernon.html --min-screens 34 --require-bilingual
node collector-output/flowers-for-algernon/evidence/browser-qa.mjs 320
```

Other browser phases: `390`, `1024`, `1440`, `behavior`, `ios`. Do not rebuild directly and omit the book-local guard: use `build-local.mjs`.

## Remaining limits

Independent content/source review is pending, especially the guide-mediated primary boundary. Complete-novel voice, unretained scenes and a named Russian translation are not certified. Physical Safari/iPhone is untested. Publisher catalogue integration and production behavior were not tested by this worker. Root readers, catalogue, index, shared UI/skills, logs, Git/PR, deployment and external messages are outside this implementation and were not changed/sent by it.


## Parent local corrections — 2026-10-31

FFA-01: reproduced the actual RU/EN downgrade leak using the unchanged independent reviewer proof. A shallow mode selection now revokes document-local consent, clears obsolete pending action and closes an obsolete warning; existing central hidden-ID, saved Continue and mode-selection guards remain. No late prose or neutral resume labels changed. FFA-02: parent directly read Ullyatt’s selected Report15 discussion and reproduced novel conversation (Heinemann1989 pp.153–154), plus SparkNotes Report15 Summary. Nemur, not Burt, supplies the contingency answer; the two minimum corrections remove the wrong Burt attribution. Burt’s separate laboratory tour remains distinct. New sources23/24 support the corrected mapping; conflicting guide11 no longer maps to warren-visit and its global note discloses the attribution limit without revealing the answer. No full primary edition, full article reading or official translation certification.

Original independent review remains unchanged. Focused regression and localized publisher acceptance are recorded separately; no self-issued independent PASS.

Parent regression completed: **164 assertions passed** across RU320/dark, EN390/light, RU1440/light and EN768/dark. Exact corrected Warren body/tail, true downgrade to Core and Essential, shallow title concealment, neutral saved destination, native Cancel/Escape, cover and Contents Deep requests, exact accepted resume, and fresh reload consent passed. Zero runtime exceptions/external requests; owned timeout30 Chrome/process group/profile cleaned. Existing evidence/author.py is a pre-correction preparation generator; current story-data.json is the maintained build input and the exact local guard delta is recorded in the parent closure. Older1120-visit checks remain historical; they are not re-labelled as a new post-correction matrix.
