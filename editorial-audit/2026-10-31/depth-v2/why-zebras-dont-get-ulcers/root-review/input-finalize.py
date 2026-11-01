"""Book-local handoff manifest. Does not grant editorial acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SLUG = "why-zebras-dont-get-ulcers"
METRICS = json.loads((ROOT / "qa/metrics-and-integrity.json").read_text())
AUDIT = json.loads((ROOT / "qa/structural-audit.json").read_text())
DATA = json.loads((ROOT / "story-data.json").read_text())
MAP = json.loads((ROOT / "coverage-map.json").read_text())
LEDGER = json.loads((ROOT / "source-reading-ledger.json").read_text())
PRIOR = json.loads((ROOT / "prior-comparison.json").read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


assert not AUDIT["failures"] and not AUDIT["warnings"]
assert len(METRICS["browserReports"]) == 5
assert len(METRICS["primarySourceLedger"]) == 18
assert all(x["unchanged"] for x in METRICS["immutableInputs"])
for name, digest in METRICS["inputHashes"].items():
    assert sha(ROOT / name) == digest, name
for report in METRICS["browserReports"] + [METRICS["preferenceReport"]]:
    assert sha(ROOT / report["file"]) == report["sha256"], report["file"]

mode_rows = []
word_rows = []
for mode in ("essential", "core", "deep"):
    m = METRICS["modes"][mode]
    mode_rows.append(f"| {mode.title()} | {m['screens']} | {m['ru']['bodyWords']:,} | {m['en']['bodyWords']:,} | {m['ru']['bodyMinutes']:.2f} / {m['ru']['uiMinutes']} | {m['en']['bodyMinutes']:.2f} / {m['en']['uiMinutes']} |")
    for lang in ("ru", "en"):
        x = m[lang]
        word_rows.append(f"| {mode.title()} / {lang.upper()} | {x['bodyWords']:,} | {x['headingWords']} | {x['coverWords']} | {x['uiEstimateWords']:,} | {x['sectionLabelWords']} |")

case_count = sum(len(ch["cases"]) for ch in MAP["chapters"])
views = sum(r["views"] for r in METRICS["browserReports"])
qa = f"""# Candidate QA and reading limits

Status: **ready-for-root-personal-check**. `rootPersonalAcceptance=false`; `publicationAllowed=false`.

## Exact content and reading counts

{len(DATA['screens'])} total bilingual screens: one cover and {len(DATA['screens']) - 1} reading fragments, including the shared final. Every reading fragment has two corresponding paragraphs. **212 RU and 212 EN draft paragraphs** match the structured data and embedded HTML exactly, in order. All six route exports also match exactly.

| Mode | Screens incl. cover/final | RU body words | EN body words | RU body minutes / reader estimate | EN body minutes / reader estimate |
|---|---:|---:|---:|---|---|
{chr(10).join(mode_rows)}

Body time uses **180 RU / 220 EN words per minute**. The unrounded body minutes above are estimates, not tested reading speed. Rounded-up body times are RU **26/48/74** and EN **22/42/64** minutes. The reader's more conservative labels include cover, title and subtitle text: RU **27/50/77**; EN **23/44/67**. Russian minute declension is correct for the actual labels.

Words use the maintained builder's Unicode lexical-token regex. Body excludes the cover, headings, subtitles, section labels, permanent interface, Sources and method notes; it includes the final. The builder's estimate text is **body + reading headings + cover**, not a count of every UI string.

| Mode / language | Body | Reading headings | Entire cover text | Builder estimate text | Repeated section labels, excluded |
|---|---:|---:|---:|---:|---:|
{chr(10).join(word_rows)}

Reading-screen density: RU {METRICS['density']['ru']['min']}–{METRICS['density']['ru']['max']} body words, median {METRICS['density']['ru']['median']}; EN {METRICS['density']['en']['min']}–{METRICS['density']['en']['max']}, median {METRICS['density']['en']['median']}. Longer phone screens scroll vertically; all paragraph tails were reached in browser traversal.

## Why this volume

The 13,197-word RU body is justified by the retained causal argument across all 18 chapters: communication/feedback, distinct organ costs, development/reproduction, immune timing and cancer limits, pain/memory/sleep/aging, experimental appraisal/control, depression/personality, reward/addiction and the social-scale account of inequality and resources. The map contains {case_count} grouped cases, experiments or author illustrations with setup/result/limits. This is not {case_count} independent scientific replications.

The old root's 144 screens contain 6,252 RU body words; the distinct 51-screen collector contains 2,247. The new candidate has fewer screens than that root but much more explanatory room. Counts were derived after the completed exposition and selection of cumulative routes; the 12–18k planning range was neither a filler target nor an acceptance test. Omissions remain substantial and explicit in `sources.md` and the map. This volume does not establish fidelity or root acceptance.

## Source and editorial checks

Both prefaces and all 18 main bodies were read completely in bounded chunks. Hashes and continuous read ranges are recorded in `source-reading-ledger.json`; integrity checks confirm all 18 main-body ranges are covered and all private source hashes remain unchanged. Notes were selective: chapter 1 notes 1–14, chapter 4 notes 52–53 and chapter 10 note 280. **All notes read: false.** English translates the new condensation; published-English collation was not done.

The complete RU exposition was written before the corresponding EN. Worker continuity inspection retained standalone entry points for shorter modes: Selye is introduced on first use, allostatic load is glossed where it first reaches those routes, and no hidden Deep fragment is required to decode those terms. Actual cases demonstrate shorter-mode claims. The original full prose, route membership, source map, omissions and final text remain for root's own complete review. This is an implementation check, not independent editorial acceptance.

The rat-care passages remain distinct. MRI volume is not counted as dead neurons; an unlocated twin-study setup is not attributed to this edition. Cancer onset/progression/survival and distress are separate. Historical receptor models and endocrine hypotheses stay historical. Five narrow current qualifications are labeled explicitly and mapped to official sources or the original research abstract. The full modern medical literature was not reviewed.

## Structural and browser results

The maintained deterministic audit completed **{AUDIT['passes']} passes, zero warnings and zero failures**. `contentMode=explanatory`; fresh default RU / dark / Essential / Sans. The standalone HTML is {AUDIT['bytes']:,} bytes and needs no runtime files or network. It embeds the maintained Geist Sans/Mono/Serif and Source Serif 4 fallback with licenses. Six sources remain accessible globally with their roles.

Five isolated real-Chrome runs covered **320×568, 390×844, 1024×768, 1440×900**, plus 320×568 with emulated iPhone user agent/safe areas. At each viewport the harness visited all three modes in RU/EN, dark/light and Sans/Serif: **{views:,} screen visits in 120 route/configuration traversals** across the final five reports. Each visit checked the actual title and every paragraph against data, mode count, bounds and reachable paragraph tail. There were zero runtime exceptions and zero remote runtime requests.

Interactions checked language/position preservation, Settings, source/contents dialogs, fonts, focus mode, buttons/keys, horizontal swipe versus vertical scroll, desktop rail, final restart, Continue and Start over. All visible top controls fit one labeled icon-only row at 320 px. The iPhone emulation additionally checked a 44 px safe top inset, mobile touch swipe, localized install guide and standalone hiding of its guide/trigger. **This is Chrome emulation, not physical iPhone/Safari or PWA installation certification.**

Actual platform-font records show embedded Geist for Sans, Source Serif 4 for Russian Serif and Geist Serif for English Serif. Serif controls stay Sans and the Settings fallback note remains visible. Visual inspection covered the final-build 320 px RU Serif nurse case, 1440 px resumed cover, 390 px RU final, 1024 px EN immune-mechanism screen and the emulated-iPhone nurse screen. Screenshots' older `quantitative` filename labels refer to that immune-mechanism screen; no unimplemented chart/list/image type is claimed.

The focused preference supplement proves a new document was loaded using `performance.timeOrigin`: global light/Serif, EN and the expanded-book position survive a real same-file reload and Continue. A separately identified synthetic storage event refreshes dark/Sans without paging. Cross-file `file://` preference sharing is browser-dependent and was not certified. No hosted app server was started.

## Progress and preferences

Book progress uses **`book-tiktok.{SLUG}.depth-v2.`**. The harness seeded the old slug's EN/Deep/last-screen keys and verified the candidate still starts freshly in RU/Essential. Old short/other-sequence progress does not silently resume here. A remembered deeper screen is offered with an explicit deeper-mode Continue label in both languages before the reader changes depth. Continue, Start over and final restart were exercised.

Global theme/font use the maintained `bookLibrary.preferences.v1` key. The candidate-local build changes only typographic cover decoration, its progress namespace, explicit deeper Continue copy and RU time inflection. The installed builder, shell, fonts and shared Settings assets were read-only.

Every manually launched Chrome used its own `mktemp -d` profile and `/usr/bin/timeout 30`, a dedicated process group/port, and cleanup in `finally`. All six final browser/preference reports confirm **profile removed and zero remaining owned PIDs**. No Chrome, HMR connection or profile owned by these runs remains.

## Integrity and remaining gate

`qa/metrics-and-integrity.json` binds the current drafts/data/HTML, browser inputs, actual source ranges and protected inputs. Root HTML, old collector, accepted-pilot review/build files and installed shared assets match the recorded protected hashes. No Git/PR/deploy, catalogue/global-ledger write or publication occurred.

Root must personally read the complete resulting RU/EN prose and all cumulative routes, compare coverage and omissions with the work, directly check critical source passages, and record acceptance against exact hashes. Structural/browser passes and this worker's map cannot grant that acceptance. `ready.json` binds the deliverables and retains both acceptance/publication flags as false.
"""
(ROOT / "QA.md").write_text(qa)

handoff = f"""# Root handoff — Why Zebras Don't Get Ulcers

**Candidate only: ready-for-root-personal-check. No publication approval.**

Open `{SLUG}.html` directly. Fresh defaults are RU / dark / Essential; global theme/font preferences persist. Modes are **37/70/107 screens**. Deep has **13,197 RU / 13,960 EN body words**; its reader estimates are **77 / 67 minutes** including headings/cover. Exact shorter-mode counts/times are in `QA.md` and `ready.json`.

Read the complete `draft-ru.md` and `draft-en.md`, then each exact cumulative export:

- `routes/essential.ru.md`, `routes/essential.en.md`
- `routes/core.ru.md`, `routes/core.en.md`
- `routes/deep.ru.md`, `routes/deep.en.md`

Use `coverage-map.md` / `.json` for all 18 chapters and {case_count} grouped cases, `sources.md` for edition/omissions/modern qualifications, and `source-reading-ledger.json` for private-source hashes/ranges. `read-source.py FILE START END` displays a bounded primary passage without copying it into this directory. Its optional `ack` operation updates this worker ledger; a root personal-reading record should remain a separate root record.

Pay particular attention to the GH/sedated-mother/active-licking contrast versus separate later-life care observations; types of diabetes; acute immune redistribution versus suppression; cancer endpoints and support-trial replication; brain-volume causal alternatives; both historical receptor hypotheses; control/selection in executive monkeys; reward/appetite versus withdrawal; the nonlinear-averaging inequality objection and competing public-resource paths; selected healthy-aging cohorts and withdrawal of useful support.

The old root is 144 pairs while the collector is 51; `prior-comparison.json` records both. They remain untouched. Main-text reading covers all chapters, but most notes, the published EN original and most underlying research papers were not read. No physical Safari claim is made.

Acceptance must bind the exact candidate hashes in `ready.json`. Root's personal review of all complete text, routes, primary mechanisms and meaningful omissions is still required. Any content change requires updated parity/counts/hashes and appropriate QA. There is no delegated authority to publish from this package.
"""
(ROOT / "HANDOFF.md").write_text(handoff)

critical = ["draft-ru.md", "draft-en.md", "story-data.json", SLUG + ".html",
            "coverage-map.md", "coverage-map.json", "sources.md", "QA.md",
            "source-reading-ledger.json", "web-reading-ledger.json",
            "editorial-report.md", "HANDOFF.md", "qa/metrics-and-integrity.json"]
files = {str(p.relative_to(ROOT)): {"sha256": sha(p), "bytes": p.stat().st_size}
         for p in sorted(ROOT.rglob("*")) if p.is_file() and p.name != "ready.json"}
ready = {
    "manifestVersion": 1, "slug": SLUG, "title": DATA["title"],
    "bookAuthor": "Robert M. Sapolsky", "artifactOwner": "Pavel Novikau / Smartcat",
    "createdAtUtc": datetime.now(timezone.utc).isoformat(),
    "status": "ready-for-root-personal-check", "rootPersonalAcceptance": False,
    "publicationAllowed": False, "rootPersonalReviewRecord": None,
    "artifactDirectory": str(ROOT), "standaloneHtml": str(ROOT / (SLUG + ".html")),
    "contentMode": DATA["contentMode"],
    "defaults": {"language": "ru", "theme": "dark", "mode": "essential", "readingFont": "sans"},
    "modeCountsIncludingCoverAndFinal": DATA["targetModes"],
    "readingRatesWordsPerMinute": METRICS["rates"], "wordMethod": METRICS["wordMethod"],
    "modes": METRICS["modes"], "density": METRICS["density"],
    "draftParagraphs": METRICS["draftParity"], "routeParagraphs": METRICS["routeParity"],
    "sourceCount": len(DATA["sources"]), "sources": [{"id": s["id"], "role": s["role"], "url": s["url"]} for s in DATA["sources"]],
    "sourceScope": {
        "primaryEdition": "User-owned full RU Piter EPUB, ISBN 978-5-4461-1081-0, 2021; third-English-edition framework, not a 2021 science update",
        "privateArchive": LEDGER["sourceRoot"], "completeMainChaptersRead": 18,
        "completeMainBodyCharacters": LEDGER["completeMainBodyCharacters"],
        "prefacesRead": LEDGER["prefacesRead"], "allNotesRead": False,
        "notesConsulted": LEDGER["notesConsulted"],
        "englishPublishedEditionCollated": False,
        "contemporaryQualificationScreens": ["unit-017","unit-022","unit-044","unit-069","unit-076"],
        "modernResearchReadingLimit": "Border et al. full abstract, not full paper; other checks are narrow official-page sections, not a literature review",
        "sourceProseCopiedIntoPackage": False,
    },
    "coverage": {"chapters": 18, "readingFragments": 106, "groupedCaseRecords": case_count,
                 "map": "coverage-map.json", "omissionAndEditionTable": "sources.md",
                 "volumeRationale": "13,197 RU body words preserve the 18-chapter causal chain, actual cases, opposing explanations and social-scale argument. The planning range and screen totals are not quotas or acceptance evidence. Significant exclusions are explicit."},
    "state": {"progressNamespace": f"book-tiktok.{SLUG}.depth-v2.",
              "legacyProgressIsolationVerified": True, "explicitDeeperContinueVerified": True,
              "sharedPreferencesKey": "bookLibrary.preferences.v1",
              "sameFilePreferenceReloadVerified": True,
              "crossFileFileUrlSharingCertified": False},
    "qa": {"structuralPasses": AUDIT["passes"], "warnings": [], "failures": [],
           "exactDraftDataHtmlParagraphParity": True, "exactAllRouteParagraphParity": True,
           "browserReports": METRICS["browserReports"], "preferenceReport": METRICS["preferenceReport"],
           "finalBrowserScreenVisits": views, "remoteRuntimeRequests": 0, "runtimeExceptions": 0,
           "standaloneOffline": True, "physicalSafariTested": False,
           "iosScope": "Chrome user-agent, safe-area/touch and standalone emulation only",
           "allOwnedChromeProfilesAndProcessesCleaned": True,
           "protectedInputsUnchanged": True},
    "legacyComparison": {"currentRootPairsRead": 144, "collectorPairsRead": 51,
                         "effectiveCorporaEqual": False, "bothUnchanged": True,
                         "details": "prior-comparison.json"},
    "readingLimits": MAP["meaningfulLimits"] + [
        "Most cited original scientific papers were not read; book reports are attributed to the edition.",
        "Shorter routes intentionally omit additional experiments; their exact text and chapter coverage are provided for personal review.",
        "Browser QA is not editorial acceptance or physical Safari certification.",
    ],
    "rootReviewRequired": [
        "Personally read every complete resulting RU and EN text, cover and final.",
        "Personally read each cumulative Essential/Core/Deep route in RU and EN.",
        "Compare the actual chapter/argument/case map and significant omissions with the retained reading experience.",
        "Directly check critical primary passages, experimental setups/results, qualifications and animal-to-human boundaries.",
        "Check current qualifications, translation parity and progress behavior; record personal acceptance against exact reviewed hashes before publication.",
    ],
    "publicationPerformed": False, "gitPrDeployPerformed": False,
    "writesConfinedToArtifactDirectory": True,
    "contentHashes": {name: files[name]["sha256"] for name in critical},
    "files": files,
    "manifestHashNote": "All package files except ready.json itself are bound above; the manifest cannot contain its own SHA-256.",
}
(ROOT / "ready.json").write_text(json.dumps(ready, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": ready["status"], "rootPersonalAcceptance": False,
                  "publicationAllowed": False, "modeCounts": DATA["targetModes"],
                  "ruDeepBodyWords": METRICS["modes"]["deep"]["ru"]["bodyWords"],
                  "boundFiles": len(files), "htmlSha256": files[SLUG + ".html"]["sha256"]}, indent=2))
