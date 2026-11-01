# Essentialism — implementation self-checks

These are technical and writer self-checks. Literary/meaning acceptance is pending root's personal reading. No self-PASS of that acceptance is asserted. rootPersonalAcceptance=false; publicationAllowed=false.

The maintained structural audit reports69 checks passed,0 warnings,0 failures (qa/schema-audit.json). The candidate-specific verifier checks every authored field against the HTML embedding, all125 paired paragraphs against the connected drafts, all six ordered route files, exact counts/times, valid source ranges and continuous displayed-source coverage. It confirms the supplied source file hash is unchanged and no runtime HTTP dependency is present. Evidence: qa/deterministic.json and metrics.json. Word count and these checks do not prove explanatory completeness.

Real offline file:// Chrome matrices cover320×568,390×844,1024×768 and1440×900; RU/EN; dark/light; Sans/Serif; Essential/Core/Deep. Each matrix visits2,256 views, total9,024, checking ordered IDs, rendered titles/body paragraphs, exact cumulative counts, horizontal bounds and last-body-line reachability. Zero collected runtime exceptions and zero runtime HTTP requests. The Sources dialog exposes chapter/file/paragraph locators. No content server, shared browser tab or other reader was used.

Each viewport also runs20 interaction assertions, a real native radio keyboard sequence (four arrows and Space), four explicit deeper-resume combinations (RU/EN from Essential/Core), three invalid/stale saved-state cases, four actual platform-font checks and global-preference reload. The first cold Serif selection occurs BEFORE inactive faces are preloaded. At320, both Serif faces are initially unloaded; scroll90px is preserved at90px after selection while the scroll range changes650→626px. This tests a meaningful nonzero position rather than an already-zero sample. At desktop, nonzero scrolling is tested only where content actually overflows.

Theme changes preserve screen/depth/exact current scroll. Language changes preserve stable screen/depth and proportional position across reflow. Settings opens without an incidental theme toggle. Its native radio arrows/Space do not advance the book. Both dialogs open/close; the Sources location map is present. Focus mode hides the header, retains Next and exits via Escape. Keyboard paging, Previous, horizontal swipe and vertical-gesture isolation are exercised. Final restart clears saved screen and lastMode. Header controls remain in one labeled icon-only row inside the viewport; desktop rail is visible.

Old `book-tiktok.essentialism.*` language/mode/lastScreen keys are seeded with EN/Deep/final and remain unread by the new document. A fresh load is RU/dark/Sans/Essential with no Continue. Candidate progress uses only `book-tiktok.essentialism.depth-v2.*`. Invalid language/depth safely falls back; invalid or stale content ID (including cover as a saved body target) resets to the Essential cover. Valid remembered deeper routes do not raise mode on arrival: Continue explicitly names «Глубоко» / Deep before entry, then the click intentionally restores the destination. Global theme/font remain under `bookLibrary.preferences.v1`.

Actual Chrome platform-font records verify embedded Geist for Sans, Source Serif4 for Russian Serif and Geist Serif for English Serif. The localized Settings note identifies Cyrillic fallback; synthetic Serif weights/italics stay disabled. All fonts/licenses are embedded. The shared Settings/header modules and installed skill remain unedited. Book-local adjustments live in build.mjs: new namespace/invalid-state handling, explicit-depth Continue, proportional language scroll, source-map exposure, typographic cover and Smartcat violet focus token. Per-screen research chrome is hidden while contentMode stays explanatory and sources remain global.

Owned Chrome: every launch is wrapped by `/usr/bin/timeout 30`, gets a unique mktemp profile and a detached owned process group. finally/exit/signal cleanup terminates that group and any remaining processes with this exact owned profile, then removes only that profile. All four final reports confirm profileRemoved=true and remainingOwnedPids=[]. No other's process was cleaned up. A first harness attempt had a JavaScript evaluate-wrapper syntax error; it cleaned up and was corrected before the successful final matrices. There was no reader defect from that attempt.

Visual inspection: the writer opened all eight320/1440 screenshots—cover, dense Russian Serif/light text, English selection procedure/dark text and final bottom. Header is compact, text measure/rail are usable, scrolling is necessary on dense phone views and the final line is reachable. The cover screenshots deliberately show the user-selected Deep route from the screenshot phase; initial fresh Essential is separately asserted in each report. Other matrix layouts were checked by DOM geometry, not individually screenshot-reviewed.

Material limits: this is desktop Chrome with mobile sizes, not a physical Safari/iPhone/PWA test. No actual mobile Safari, installation lifecycle, VoiceOver, browser-denied storage or multi-document hosted preference test is claimed. No images exist in this candidate. No independent current-science or official-English-edition collation was performed. All content/meaning acceptance remains with root.

Reproduce from this directory (read-only installed dependency required):

```
node build.mjs
node /Users/pn/.codex/skills/book-tiktok/scripts/audit_story_html.mjs essentialism.html --min-screens 125 --require-bilingual
node verify.mjs
node browser-check.mjs 320
node browser-check.mjs 390
node browser-check.mjs 1024
node browser-check.mjs 1440
python3 document.py
python3 seal.py
```

The source-reading display script is deliberately separate: it records a new display when explicitly run and is not part of rebuilding the candidate.
