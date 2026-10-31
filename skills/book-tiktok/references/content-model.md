# Content model

Use this reference when researching, outlining, translating, or checking fidelity to a book.

## Evidence ladder

Prefer evidence in this order:

1. Text supplied by the user or a lawfully accessible public-domain/licensed edition.
2. Official publisher description, table of contents, notes, excerpt, and the author’s own long-form interviews or lectures.
3. Primary historical, scientific, economic, or technical sources needed to verify the book’s factual scaffolding.
4. Substantial independent reviews that describe the argument, cases, disagreements, and omissions.
5. Tertiary summaries only for discovery; do not let them determine the final thesis map.

For a copyrighted book, never search for or reproduce an unauthorized full text. A public synthesis can still be faithful when its evidence boundary is explicit. Record what was actually consulted.

## Claim map before screens

Answer these questions in working notes before layout:

- What desire, tension, or question makes the book worth reading?
- What does the author say conventional accounts get wrong or miss?
- What is the shortest accurate statement of the thesis?
- Through what causal chain does it operate?
- Which people, events, experiments, datasets, or cases carry the argument?
- What changes because of the argument—politically, economically, socially, organizationally, or personally?
- Which qualifications and counterexamples prevent a simplistic reading?
- Which claims belong to the author, which are independent corroboration, and which are the digest’s inference?
- What compact mental model should remain after the last screen?

Use a light DPST reading arc when it fits: the reader’s desire or question → the problem in the conventional account → the book’s solution or model → the transformation in understanding. Do not force a product-pitch rhythm onto a book whose argument needs a different sequence.

If sources disagree, represent the disagreement instead of silently choosing the most dramatic version. Do not start screen writing until the claim map forms a coherent causal sequence.

## Source ledger

Keep a source ledger while researching. For each source record:

- direct URL, title, author/publisher, role, and access date;
- which claims it supports or challenges;
- whether it exposes the book’s own argument, provides primary factual scaffolding, or adds independent criticism;
- useful passages in paraphrase, with short quotations only when necessary and within copyright limits;
- uncertainties, disagreements, and claims still unsupported.

The final artifact needs only concise bilingual source notes. The fuller ledger is working evidence and should not contain copied copyrighted chapters.

## Provenance types

Every non-cover screen uses one provenance type in the v2 data contract:

- `book` — the author’s thesis, mechanism, evidence, example, or qualification;
- `corroboration` — primary or independent evidence that supports, narrows, or disputes the book;
- `synthesis` — the digest’s inference, analogy, application, or compact mental model.

Provenance is not a confidence score. A `book` screen can report a contested claim, and a `synthesis` screen can be strongly reasoned; the label tells the reader whose move it is.

## Screen-count agreement

Before any research beyond identifying the exact book and making a preliminary density estimate, the user must either provide an Essential/Core/Deep triple or choose among three proposed profiles. Offer exact cumulative counts plus approximate time, recommend one, and wait for the choice. If the user supplies only a Deep total, propose and confirm the nested split. Counts include the level-1 cover and final screens. Do not hide the decision inside the implementation.

Use nested depths rather than three unrelated summaries. These bands help form the three options:

- **Compact:** roughly 16–24 Essential, 30–48 Core, 45–64 Deep.
- **Standard:** roughly 20–30 Essential, 42–68 Core, 64–90 Deep.
- **Dense:** roughly 24–36 Essential, 56–90 Core, 90–130+ Deep.

The proposed counts should follow the book, but the selected counts belong to the brief after the user chooses. A short, single-idea book may need fewer screens; a systems book, history, handbook, or multi-domain argument may need more than 100. If the claim map later shows that the selected count would require padding or omit a major mechanism, return to the user with evidence and a revised three-option proposal rather than silently changing the target.

Essential must remain a complete argument by itself: question, thesis, main mechanism, decisive evidence, consequence, qualification, and final model. Core inserts the book’s important actors, evidence, cases, and objections. Deep adds secondary mechanisms, applications, contested interpretations, source-sensitive detail, and bounded modern relevance.

Useful screen jobs include:

- framing question or desire;
- thesis or misconception correction;
- causal step;
- chronology pivot;
- person or institution;
- quantitative anchor;
- case study or worked example;
- distributional consequence;
- political, organizational, or cultural aftereffect;
- counterexample or caveat;
- analogy with an explicit limit;
- application;
- synthesis.

Each screen should be understandable alone and necessary in sequence. A strong title carries the claim; the body earns it. If two titles make the same claim, merge or differentiate the screens.

## Density and rhythm

- Target roughly 35–75 body words per ordinary screen. Let lists, worked examples, and evidence screens run longer when the cognitive job genuinely requires it.
- Alternate abstraction with evidence: thesis → mechanism → case → consequence → qualification.
- Use numbers only when they sharpen scale or causality. State whether a figure is nominal, estimated, or a modern equivalent.
- Use short quotations sparingly and within copyright limits. Paraphrase the argument instead of assembling a quote collage.
- Do not turn a historical analogy into identity. State what maps to the present and what does not.
- End with the book’s durable mental model, not a generic motivational conclusion.

## RU/EN parity

- Store one stable ID, level, provenance type, source list, and image assignment per screen; store RU and EN copy beneath it.
- Translate meaning and cadence, not word order. Proper names, dates, quantities, and causal qualifiers must remain aligned.
- Localize all interface text, accessibility labels, captions, source notes, method text, and document title.
- In a Russian-led artifact, Russian is the saved default and the button shows `EN`; the English view shows `RU`.
- A language switch must preserve the current screen, selected depth, theme, and saved progress.
- Large word-count skew between translations is a review signal: check for missing evidence or qualifications rather than mechanically equalizing length.

## Source disclosure

Give sources short numeric IDs and attach them to the screens they support. The Sources dialog should contain title, direct URL, role, and a brief note describing what that source supports.

Include a concise method note with three distinctions:

- this is an analytical digest, not copied book text;
- factual claims are sourced and evidence gaps remain explicit;
- corroboration, present-day analogies, and synthesis are distinguished from the author’s own claims.
