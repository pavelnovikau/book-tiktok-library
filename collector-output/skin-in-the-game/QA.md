# Skin in the Game — repair checks, 2026-10-31

Status: ready for independent editorial check, not publication approval. The earlier green review is superseded.

## Substantive self-check

Read all 112 original RU/EN pairs in the collector and compared them with the effective embedded root corpus: identical screens. Rewrote the sequence to 53 pairs and checked the resulting RU/EN meaning, cases and the Essential/Core/Deep paths. New cumulative counts: 19 / 37 / 53. Level increments: 19 / 18 / 16. `contentMode: explanatory`; defaults RU / dark / Essential. Fifty old IDs are retained; three are new. Detailed omissions and access limits are in sources.md and the per-book audit report.

Removed the invented launch-team example, digest exercises, later ergodicity literature and reviewer commentary from the book-reading sequence. Replaced generic headings and repeated disclaimers with connected author-grounded cases. Corrected the ethics-of-disagreement meaning. No invented scenes, dialogue, quotations, page references, contemporary application or academic theorem has been added.

## Structural and browser checks

Maintained build tool: `skills/book-tiktok/scripts/build_story.mjs`; maintained auditor: `skills/book-tiktok/scripts/audit_story_html.mjs`. Collector HTML rebuilt from JSON. Audit: 69 passes, no warnings/failures; 53 screens, cumulative 19/37/53; 2,501 RU / 2,889 EN words under the auditor's counting convention (builder includes cover subtitle: 2,505 / 2,894). These counts measure size, not fidelity.

Real Google Chrome via local file, with fresh isolated profiles, `timeout 30`, explicit process-group cleanup and immediate profile deletion. At 320×568 and 1440×900: every visible screen in every depth × RU/EN × dark/light, 436 renders per viewport, 872 total. Expected localized titles, no document horizontal overflow, header controls in bounds, sources open and contain edition, embedded fonts loaded; zero runtime exceptions or HTTP(S) runtime requests. Actual text tap entered focus mode at both sizes. Inspected the mobile EN/light disagreement screenshot: coherent paragraph, all controls in a compact row, no clipped text. Screenshots/private reports are outside repo.

These checks do not cover physical iPhone Safari, installed PWA behaviour, or the publisher's later maintained-shell integration. No root reader, catalogue, shared script or deployment was changed. The final wording-only Sources note was rebuilt after the browser matrix; the structural audit was rerun on that output.

## Publisher attention

Integrate JSON with the maintained shell; do not use this worker as publication approval. Update root metadata to 53 screens and justified counts/time estimates. Reader body still carries the shared nonfiction Book argument / Sources footer; no EPUB paragraph is appended. Existing progress uses stable IDs: retained IDs have revised wording, removed IDs must safely return to the cover rather than reuse an old numerical offset. Recheck resume and Sources after live integration. No fiction spoiler-consent behaviour applies to this book.
