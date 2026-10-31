# Solaris — implementation QA, 2026-10-31

Status: **ready-for-independent-check**. This is collector self-QA, not independent editorial approval, whole-book certification or publication. Current source scope and the retained causal links are in `sources.md`; the old audit is unchanged.

## Result

The former analytical 112-pair package was rebuilt as connected fiction. `narrative-draft.md` precedes segmentation. Exact nested counts, including cover/final: **10 Essential / 16 Core / 32 Deep**; level additions **10 / 6 / 16**. Defaults: **RU / dark / Essential / Sans**. `contentMode: narrative`; all 29 story paragraphs have source maps, with no per-screen academic chrome. Sources remains accessible globally.

| Mode | Screens | RU words | EN words | RU / EN estimated minutes |
| --- | ---: | ---: | ---: | ---: |
| Essential | 10 | 450 | 543 | 3 / 3 |
| Core | 16 | 753 | 907 | 5 / 5 |
| Deep | 32 | 1,516 | 1,825 | 9 / 9 |

Builder words include titles/subtitle/body. Estimates use 180 RU / 220 EN words per minute and exclude reflection/source reading. Ordinary narrative bodies: **35–58 RU** words, mean **47.66**; **40–67 EN**, mean **56.90**. Their totals are 1,382 RU / 1,650 EN. The 23 source entries include limited primary reading, accountable guides and bounded critical excerpts; they do not imply 23 complete works were read.

## Reproduction

Only run these Solaris-scoped commands; the maintained accepted installed skill is read-only:

```sh
python3 collector-output/solaris/segment.py
node /Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs collector-output/solaris/story-data.json --out collector-output/solaris/solaris.html
python3 collector-output/solaris/guard_reader.py
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs collector-output/solaris/solaris.html --min-screens 32 --require-bilingual
node collector-output/solaris/qa-solaris.mjs 320
node collector-output/solaris/qa-solaris.mjs 390
node collector-output/solaris/qa-solaris.mjs 1024
node collector-output/solaris/qa-solaris.mjs 1440
node collector-output/solaris/qa-solaris.mjs interactions
node collector-output/solaris/qa-solaris.mjs ios
node collector-output/solaris/qa-solaris.mjs visual
```

Structure: **69 passes, zero failures**. One expected warning names empty source lists on `deep-warning` and `final`: these are navigation/consent framing and make no external plot claim. No fake source was added merely to silence the warning. Exact metadata, bilingual fields, unique IDs, counts and narrative presentation pass. Final effective HTML equals canonical authoring JSON except builder-generated `modes`; source/media maps match. The original baseline ZIP was checked to contain all four old Solaris files.

## Local spoiler guard

`guard_reader.py` installs package-local **SOLARIS_VOLATILE_CONSENT_V1** after the maintained build and fails if expected shell anchors drift. It edits only this generated reader. Do not rebuild or transplant the collector without preserving this guard.

- Selecting Deep, a saved level-3 resume, or a hidden level-3 ID requires an explicit localized dialog. Cancellation/Escape leaves the current mode and position untouched. Pre-consent contents contain no late titles.
- Consent exists only in the runtime closure. It is never stored. Reload and BFCache restoration revoke it; leaving Deep revokes it too. A stored Deep preference opens a safe Essential cover until a new opt-in.
- The maintained generic labels remain intact: `Продолжить Deep — спойлеры финала` / `Continue Deep — ending spoilers`. They do not interpolate a late screen title. A saved late ID is restored only after fresh consent; removed old IDs fall back safely.
- The Deep warning precedes the late narrative. Cover, shallow contents, shared final and global source/method notes remain safe. Optional external sources are marked as containing spoilers.

## Offline browser matrix

Preview was attempted as requested. It rejected `file://` with **Invalid preview URL (unsupported-protocol: file:)**. Fallback: actual Google Chrome headless/new via CDP, opening this HTML directly. No content server, preview proxy or remote page runtime was used. HTTP(S) runtime requests were blocked and CDP emulated offline networking.

Each viewport traversed every screen in all depths, both languages, both themes and **both reading fonts**: `(10 + 16 + 32) x 2 x 2 x 2 = 464` visits. Final total: **1,856** visits. Each viewport also exercised **48 Sources/Contents dialog cases**. Reports are `qa/320.json`, `390.json`, `1024.json`, `1440.json`.

| Viewport | Visits | Scrollable visits | Horizontal overflow | Runtime errors | External requests |
| --- | ---: | ---: | ---: | ---: | ---: |
| 320 x 568 | 464 | 38 | 0 | 0 | 0 |
| 390 x 844 | 464 | 24 | 0 | 0 | 0 |
| 1024 x 768 | 464 | 24 | 0 | 0 | 0 |
| 1440 x 900 | 464 | 0 | 0 | 0 | 0 |

Checked actual localized body/title, active stable ID, counter, filtered contents, child width containment, reachable scroll bottoms, cover-copy children and decoded embedded SVG. Desktop rail stays present and synchronized. Consent child/footer containment was checked before accepting on all configurations. Sources contains all 23 entries. Geist Sans, Geist Mono, Geist Serif and Source Serif 4 load from embedded data. Serif mode uses the maintained Cyrillic fallback disclosure; UI controls remain Sans. Reader prose has no lists/comparison component requiring additional component QA.

`qa/interactions.json`: **25 checks**, including native ArrowRight/Space, Next, F/Escape, native mouse drag, native touch swipe, native text-tap focus toggle, synthetic vertical-pointer discrimination, Settings controls, exact stable-position preservation, RU/EN generic resume, cancel/reload/depth/BFCache consent paths, removed legacy IDs and restart. Initial CDP pointer dispatch stalled before a compositor frame; bringing the owned page to front and capturing a frame resolved it. The final native pointer and touch checks pass. Synthetic vertical discrimination is not claimed as physical touch-scroll verification.

`qa/ios.json`: iPhone Safari UA and mobile metrics at 320/390; six icon controls share one row (y=23, rightmost edges 308/378). Install guide is localized/scrollable and hides in emulated standalone. The old S1 heading-focus clipping was not reproduced with this maintained shell: initial guide scrollTop=0 and title is below the dialog top. This is **Chrome emulation, not physical Safari or an installed iPhone PWA test**.

Visually inspected the saved phone/desktop cover and letter, dark RU oxygen/ending/shared-final/consent, generic saved resume and iPhone guide. Representative PNGs are in `qa/`. Small-phone covers intentionally scroll; reading paragraphs and Next remain reachable.

Every browser phase used its own `mkdtemp` profile and detached process group under `timeout 30`. Success and failure paths kill only that group and remove that profile. All final reports assert cleanup; final process/profile checks found no owned leftovers. No server was started.

## Handoff limits

Independent review must read the actual 32 pairs and check the mapped actions, not infer fidelity from this structural/browser pass. Full-edition/translation-line fidelity, physical Safari, oceanic intention and a promised reunion are not certified. Original audits/reviews are immutable; root readers/catalogue/shared shell/installed skill/Git/PR/deploy remain outside this worker's work. Hashed handoff: `../../editorial-audit/2026-10-31/ready/solaris.json`.
