# Editorial repair — direct user instructions, 2026-10-31

The previous assignment was wrong. Technical passes and previous cold reviews do not establish fidelity: they accepted an analytical companion where the user requested an engaging condensed book. Audit the actual published content and draft packages from scratch.

The user has now authorized ten Sol max workers and one publisher, including immediate publication of verified corrections. This supersedes the temporary all-agent/publication stop. Latest steering explicitly asks to fill the ten worker slots: continue repair/review, actively resolve source gaps, and begin already approved queued works under this corrected brief. Do not invent new titles or replace agreed ones without the user's choice. Work one book at a time and retain a reviewable record of every change.

## The requested reading experience

**Fiction:** tell the author's story in concise, engaging original prose. Preserve characters, their relationships, motives actually established in the text, events, causality, atmosphere, humour, uncertainty and suspense. Scenes and concrete events must carry the reading. Titles may name a scene, place, action or question. Do not replace adventures with lessons about competence, leadership, responsibility, psychology or the reader's life. Do not add exercises, modern analogies, invented dialogue, invented scenes or invented motives. Do not claim to know a definitive authorial intention that the evidence does not establish. A chapter-by-chapter administrative synopsis also needs rewriting if it is dull or disconnected.

**Nonfiction:** convey the author's actual main ideas, reasoning and examples in an engaging concise sequence. Keep qualifications, uncertainty, disagreement and attribution. The author's real cases can supply narrative; invented anecdotes cannot. Remove the digest writer's lessons, prescriptions and analogies when they substitute for the book. Independent scientific checks may qualify a factual claim, but must not silently replace the author's argument. Practical books retain actual procedures; a philosophical novel retains both its narrative and its philosophical argument in their original relationship. Hermes/Nous is an original research brief, not an authored book: label and audit it accordingly.

Write good connected text first; divide it into short mobile screens afterwards. Existing screen totals are historical, not a reason to pad. Set `targetModes` to the justified final nested counts and record the change. Every depth must read coherently. Preserve current spoiler promises: decisive fictional endings remain in Deep after a clear warning. Do not leak them in covers, resume labels, global source notes or Essential/Core contents.

## Evidence and audit

- Read every RU/EN screen in the assigned current delivery and draft. For a published book, inspect the root HTML's effective embedded corpus, not just collector JSON. Note meaningful divergence.
- Identify the exact work and edition. Inspect `sources.md` and actual evidence. A fetched complete book and continuous reading are different claims. Check whether a local EPUB is a full edition, condensation or summary before relying on it.
- Use user-supplied owned editions read-only or lawfully accessible full text. Apple Books root: `/Users/pn/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents`; EPUBs are usually expanded directories. Scope searches to assigned titles. Do not expose unrelated filenames or place private/full copyrighted text in this public Git repository.
- If only excerpts/reviews are accessible, say exactly what can and cannot be verified. Do not reconstruct unsupported plot details or certify whole-book fidelity from a blurb. Search lawful author/publisher/library material proactively. If the remaining evidence cannot support a faithful rewrite, deliver a precise source gap rather than new fabrication.
- Complete book text is preferred, not a universal prerequisite for a concise source-supported condensation. A substantial official chapter guide, actual author material and verified primary passages may jointly support the retained story or argument. Assess support for the particular retained actions, motives and causal claims; do not automatically reject a book solely because the whole edition was not downloaded/read continuously. Never fill an essential missing link from memory, claim full-text reading that did not happen, or relabel criticism as the author's own words. A blurb or unverified generic recap alone remains insufficient.
- Record concrete defects by stable screen ID, with the problematic wording, expected correction and a primary-text location or direct supporting URL. Distinguish a factual error, unsupported specificity, unwanted interpretation, omission, broken narrative and translation mismatch.
- Mechanical provenance counts and lexical searches are triage only. They cannot prove a passage false or the rewrite faithful. Previous 68-pass audits measure structure and UI, not editorial success.

## Deliverables and ownership

Each worker owns only its assigned collector folders and its own reports under `editorial-audit/2026-10-31/books/`. Save per-book reports as you finish, including how many pairs were actually read, evidence scope, specific findings, KEEP/EDIT/REBUILD/SOURCE-GAP verdict, changes and remaining limits. Do not claim the whole assignment finished while books remain unread.

For a justified rewrite, update the four canonical collector files (story-data.json, descriptive HTML, sources.md, QA.md). Preserve the old version in the existing external baseline, never delete unrelated files. For fiction set `contentMode: "narrative"`; for nonfiction `contentMode: "explanatory"`. Use maintained build tools, not a copied reader. Parent is updating shared skill/shell; do not edit shared files or synchronize the installed skill.

After content and local checks pass, write `editorial-audit/2026-10-31/ready/<slug>.json` containing slug, deliverable paths and SHA-256 hashes, counts, report path, source scope, exact changes and unresolved issues. Set `status: "ready-for-independent-check"`, never self-certify publication. A source gap is not ready. The publisher owns root readers, books.json, index.html, release docs and Git/PR/deploy actions. Workers must not touch those files, run sync across readers, commit, push, publish, contact external people or spawn agents.

Independent content review reads every changed pair, the resulting narrative/argument sequence and supporting primary passages. The publisher can rely on a completed independent PASS when the reviewed authoring/HTML hashes still match; it need not repeat that entire review. It checks integration, saved progress, spoiler behaviour and actual production, and directly validates any small post-review corrections against the finding and source. Publish only corrections that satisfy this brief and relevant structural/mobile/offline checks. Passing legacy QA alone is insufficient. Keep untouched books' audit status honest. Publish approved ready books incrementally without waiting for all forty. Never deploy the entire collector tree.

## Shared safeguards

Default RU/dark/Essential; bilingual parity; offline standalone HTML; Flexoki dark/light; one compact icon-only header. Keep the homepage statistics strip (explicit user choice). Equalize homepage tabs. Investigate the reported iPhone/PWA header displacement rather than assuming its cause. Keep sources available through the Sources dialog; reading screens should not look like a research report.

No invented quotations or page references. Preserve book-specific spoiler consent and saved-progress protections. If Chrome is used, use a unique temporary profile, a bounded lifetime and owned-process cleanup; do not leave servers or browser profiles behind.

Baseline: `/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/baseline.zip` and `baseline-manifest.json`. Inventory includes 31 published works, nine structured unpublished packages and the source-only Project Hail Mary folder (41 records). Baseline creation does not imply editorial verification.
