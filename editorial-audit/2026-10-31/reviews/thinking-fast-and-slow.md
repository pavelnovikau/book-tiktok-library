# Thinking, Fast and Slow — independent content review

REQUIRES-FIXES: two local content corrections, not a rebuild or whole-volume source gap. Read all 29/29 RU/EN pairs, all titles/cover/final, method and source notes, and all six connected routes (14/24/29 in each language). Canonical prose and effective embedded HTML agree.

## Evidence actually read

Independently identified the entitled expanded Russian EPUB named in sources.md: title/creator OPF metadata, original 2011 copyright, Bakanov translation school 2013, AST 2014, 117 spine entries, five-part/appendix/conclusion structure. Read selected claim-supporting passages from all five parts, introduction and conclusion, using the precise content filenames in the source map. The two rejected short condensations are not treated as evidence. The official [Macmillan English introduction](https://us.macmillan.com/books/9780374533557/thinkingfastandslow/) was also read; it supports the introduction/base-rate and framing of the work, not the private edition’s later chapter passages.

No continuous full-volume reading or full-English collation is claimed. EN was checked against the RU condensation and retained primary meaning. The public identification URL is not a claim that the whole English volume was accessed. No private extraction was written to the repo.

## Required corrections

KAH-01 — medium, `same-outcomes-new-frame`, all depths and both languages. RU: “Одной группе предлагают гарантированно спасти 200 человек или рискнуть ради спасения всех. Другой те же последствия описывают через гарантированную смерть 400 человек и риск, при котором могут умереть все или никто.” EN: “One group chooses between certainly saving 200 and a gamble that could save everyone. Another receives equivalent outcomes described as 400 certain deaths versus a gamble in which everyone or no one could die.”

The gamble probabilities are missing, as is the first gamble’s zero-survivor branch. The next paragraph asserts equivalence that these abbreviated choices do not establish. Restore the two distributions: 1/3 all 600 saved and 2/3 none saved; equivalently 1/3 no deaths and 2/3 all 600 dead. Keep the certain 200 saved/400 dead alternatives. This makes the framing contrast inspectable without turning the screen into a lecture. Primary: owned RU edition, `content92.html`, epidemic problem, programs A/B and A′/B′. The JSON gives minimal replacement wording in both languages.

KAH-02 — medium, `risk-policy`, Deep RU/EN. RU: “потенциальная потеря не должна угрожать благополучию, ставки не должны складываться в одну и ту же опасность, а риски должны быть достаточно независимыми”. EN: “a possible loss must not threaten overall well-being, the bets must not all expose the person to the same danger, and risks must be sufficiently independent”.

Two clauses repeat the independence restriction; the author’s separate third restriction is absent. Replace the repeated clause with his exclusion of long-shot gambles/lotteries with small winning chances. Keep independence and no threat to overall well-being. The final warning about unfavorable or ruinous bets does not cover this distinct condition. Primary: owned RU edition, `content84.html`, advice to Sam after the coin-toss series, the three caveats and final low-chance-lottery bullet. This preserves the real procedure rather than deleting all guidance.

## Findings on the rest of the arc

Systems 1/2 remain descriptive characters, not anatomy or a fast-bad/slow-good rule. The bat-and-ball arithmetic, WYSIATI, kidney-cancer extremes, 10/65 wheel, six/twelve assertiveness examples, base rates, fictional Linda and flight-instructor regression keep distinct mechanisms. Hindsight and outcome evaluation are linked in the actual source; the RU connection is supportable rather than an invented causal theory.

Expert intuition retains environmental regularity, opportunity to learn and feedback. The army interview keeps separate ratings and the surprising usefulness of intuition after structured data; the hiring procedure is the author’s. Outside view does not become arbitrary averaging. Klein’s premortem keeps its timing, 5–10 minutes and limited promise.

Reference dependence, diminishing sensitivity, loss aversion, use versus trading goods, probability weighting and prospect theory’s blind spots are present. Descriptive preference effects are not presented as rationality or current investing advice. Pain/memory distinctions remain descriptive; no new clinical recommendation to prolong pain appears. California connects focusing back to available information. The final has no immunity promise.

Essential traverses all five parts with coherent transitions; Core supplies experiments/procedures, Deep adds logical and theoretical limits. KAH-01 weakens the same example in every route; KAH-02 affects Deep only. Apart from these local omissions, no broken dependency or meaningful bilingual mismatch was found. Omitting priming/ego-depletion does not validate them; this review makes no replication or current-science certificate. Other omissions are judged against the promised central arc, not exhaustive chapter coverage.

No optional style/date demands. Fresh deterministic audit: 69 checks passed, zero warnings/failures; this is a structural result only. Publication acceptance should wait for KAH-01 and KAH-02, corrected RU/EN/embedded parity and new hashes.

## Integrity and exact hashes

All four canonical files, source map, implementation report and ready manifest were unchanged. Every package file captured before review also remained unchanged. Ready deliverable/report/source-map hashes matched. No collector, ready, root reader, shared shell, Git, PR, deployment or external messaging changes.

| File | SHA-256 before | SHA-256 after |
|---|---|---|
| `collector-output/thinking-fast-and-slow/story-data.json` | `22835bb177a6cbd38f82cb0c1a9c5f37d19442f785b43328acd8730a21d3d926` | `22835bb177a6cbd38f82cb0c1a9c5f37d19442f785b43328acd8730a21d3d926` |
| `collector-output/thinking-fast-and-slow/thinking-fast-and-slow.html` | `29b4959427656a8f6402b5e6b197bea422a3e1ce952ab5e66ecad71abb1d09da` | `29b4959427656a8f6402b5e6b197bea422a3e1ce952ab5e66ecad71abb1d09da` |
| `collector-output/thinking-fast-and-slow/sources.md` | `48c119934bf5d9cc9901d432012629e4f4a47d4fcd82162f8a5911c6f6dd30c6` | `48c119934bf5d9cc9901d432012629e4f4a47d4fcd82162f8a5911c6f6dd30c6` |
| `collector-output/thinking-fast-and-slow/QA.md` | `28f8ca0e1157f5fa3bea312bc5641bb3ac07418c2290e8497eca7d90bdea9014` | `28f8ca0e1157f5fa3bea312bc5641bb3ac07418c2290e8497eca7d90bdea9014` |
| `collector-output/thinking-fast-and-slow/evidence-map.sol.json` | `25fe8a0642a36e49f9f7c0ae91721b4fdd1e069bb8647f1b0604c4bb9c9d6454` | `25fe8a0642a36e49f9f7c0ae91721b4fdd1e069bb8647f1b0604c4bb9c9d6454` |
| `editorial-audit/2026-10-31/ready/thinking-fast-and-slow.json` | `1f2f6b3e1c0bb2e46a8054dc1d478ab16186093ba7e6115da7fea2612dcf7250` | `1f2f6b3e1c0bb2e46a8054dc1d478ab16186093ba7e6115da7fea2612dcf7250` |
| `editorial-audit/2026-10-31/books/thinking-fast-and-slow.sol-implementation.md` | `2fd700884e990d37dee3ea9caca0553d76c007fd124f4d92b17070b5b212af60` | `2fd700884e990d37dee3ea9caca0553d76c007fd124f4d92b17070b5b212af60` |

The JSON records exact route IDs, source-boundary decisions, findings and fresh embedding/count checks. The deterministic audit was rerun as a structural check only; no new browser matrix was run.
