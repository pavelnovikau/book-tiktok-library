# The Left Hand of Darkness — implementation QA, 2026-10-31

Status: ready-for-independent-check; no independent editorial PASS or publication claim.

Rebuilt the 144-pair analytical package as 35 narrative RU/EN pairs. Exact modes 11/15/35; contentMode narrative. All 144 old pairs were read during this rescue, and their HTML embedded screen corpus was compared with JSON: identical. No published root reader exists for this slug. All 35 replacement pairs were read in both languages. Cover artwork retained; its technical caption replaced with Smartcat credit, neutral accessible description. No hand-edited shared shell or discarded book-specific custom code.

Maintained build_story.mjs and audit_story_html.mjs used. Final audit: 69 passes, zero failures/warnings, --min-screens 35 --require-bilingual. Two authoring/setup corrections occurred before final verification: Python 3.9 file parser required splitting one very long UTF-8 line; media credit is required by builder and was restored as localized Smartcat credit. The audit run against the old corpus during that failed first authoring attempt is **not** validation of the replacement. All final checks below were rerun against the final 35-pair artifact.

Four independent Chrome file:// runs at 320×568, 390×844, 1024×768, 1440×900; each visited all 11+15+35 screens in RU/EN and light/dark, 976 screen visits total. All exact titles, counts and current IDs agreed, no horizontal overflow. Checked fresh RU/dark/Essential, embedded offline fonts, Sources/Contents dialogs, mode-filtered contents, one-row icon header, language/theme position preservation, F/Escape focus, navigation, generic saved-Deep label and cover on reload. No runtime exceptions or HTTP runtime requests. Receipts: .rescue-qa-{320,390,1024,1440}.json. 320 cover and concluding-screen screenshots visually inspected. Chrome timeout 30 seconds, unique mktemp profile per run, owned process-group kill and profileRemoved true in all final receipts; no server started.

Spoilers: original full-plot-in-Deep promise preserved, including the foretelling answer. No prior book-local separate consent implementation was present; none removed. Sources dialog method accurately discloses limited reading and warns external pages may reveal plot. Narrative source-label chrome hidden. Fictional uncertainty about Estraven's final act preserved. No physical iPhone/Safari, swipe gesture or separate safe-area test claimed. Independence and content sufficiency review remain pending.


## Parent meaning corrections — 2026-10-31

Parent applied required independent meaning findings LHD-SR-001, LHD-SR-002, LHD-SR-003, LHD-SR-004 in RU and EN. Changed pairs: arrest, the-prison-truck, pulefen, waking-in-the-tent. Embedded data/derived reading estimates refreshed without replacing outer reader code or styles. This is a localized closure awaiting publisher validation, not a new independent PASS.
