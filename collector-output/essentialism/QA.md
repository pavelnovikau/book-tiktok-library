# essentialism — repair QA, 2026-10-31

Status: local checks complete; **ready for independent editorial check**, not publication approval. Old green reviews do not certify this repair.

- Source: Greg McKeown, Эссенциализм. Путь к простоте, МИФ 2015, И. Айзятулова, ISBN 9785000573471; original 2014.
- Before: 112 RU/EN pairs; after: 36 RU/EN pairs. Depths: {'essential': 18, 'core': 28, 'deep': 36}.
- Defaults: RU / dark / Essential. `contentMode: explanatory`.
- Every retained/replaced RU/EN pair reread for meaning, qualifications and sequence; source scope in `sources.md` and audit report.
- Maintained local `build_story.mjs`; maintained `audit_story_html.mjs --require-bilingual`: zero failures/warnings (raw result private).
- File-URL Chromium traversal: 320×568, 390×844, 1440×900, both themes, both languages, all three modes: **984 rendered screen checks**, no horizontal overflow, no title/count mismatches, no runtime exceptions, no HTTP(S) runtime requests. Sources and Contents open/close; embedded corpus matches authoring JSON apart from computed mode times.
- Unique temporary Chrome profile, hard `timeout 30`, owned process group killed and profile removed in finally. No server started.
- No shared shell, root reader, catalogue, publication or Git action.

Changes: Rebuilt all 36 bilingual pairs into connected, shorter prose (18 Essential / 28 Core / 36 Deep). Replaced administrative titles with readable ideas/cases, removed independent-study detours and all writer-created exercises, kept concrete author cases and actual procedures. Preserved the four-burner qualification, the risk that a better opportunity never comes, unfinished digital-access goal, reverse pilot, four editing moves, Herbie’s fictional origin, leadership appendix and family-centered conclusion. Default changed to Essential; contentMode is explanatory. Two sources remain because only the edition and its publisher identity support the delivered account; old six-source quota has no role.

Limits: This is a checked condensation of the represented main argument, not exhaustive coverage of every case or independent validation of Essentialism. Full EPUB and extracts are private outside the repository. Physical iPhone/PWA behavior and stale saved-ID migration require publisher regression checks.

Publisher: root integration, catalogue counts/times, shared mobile/PWA/focus and retained/deleted-ID saved-progress regression remain yours. Tests above are local browser checks, not physical iPhone/PWA or assistive-technology testing.
