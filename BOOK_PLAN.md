# Library expansion plan

The active expansion queue contains 25 books. All counts are cumulative `Essential / Core / Deep`, include the cover and final screens, and use the approved **Maximum** density. Deeper screens must add a distinct mechanism, case, caveat, application or synthesis; counts are a fidelity contract, not permission to pad.

| Section | Book | Counts | Collection | Source boundary |
| --- | --- | ---: | --- | --- |
| Risk and decisions | Nassim Nicholas Taleb — *Antifragile* | 36 / 90 / 144 | Taleb | Source-backed synthesis; local file is a condensation, not the full book |
| Risk and decisions | Nassim Nicholas Taleb — *Skin in the Game* | 30 / 72 / 112 | Taleb | Full lawful EPUB supplied by maintainer |
| Human and behavior | Robert Sapolsky — *Behave* | 36 / 90 / 144 | Sapolsky | Source-backed synthesis unless a lawful edition is supplied |
| Human and behavior | Robert Sapolsky — *Determined* | 36 / 90 / 144 | Sapolsky | Source-backed synthesis unless a lawful edition is supplied |
| Health and protocols | Robert Sapolsky — *Why Zebras Don’t Get Ulcers* | 36 / 90 / 144 | Sapolsky | Full lawful EPUB; health claims need independent corroboration |
| Human and behavior | Will Storr — *Selfie* | 30 / 72 / 112 | — | Full lawful EPUB supplied by maintainer |
| Systems and work | Greg McKeown — *Essentialism* | 30 / 72 / 112 | Practices | Full lawful EPUB supplied by maintainer |
| History, power and strategy | Sun Tzu — *The Art of War* | 22 / 46 / 70 | Practices | Public-domain primary text plus scholarship; local file is only a condensation |
| Health and protocols | Andrew Huberman — *Protocols* | 36 / 90 / 144 | Practices | Official book and episode materials plus independent health evidence; explicit limitations |
| Systems and work | Oliver Burkeman — *Four Thousand Weeks* | 30 / 72 / 112 | Practices | Full lawful EPUB supplied by maintainer |
| Consciousness and calm | Mark Williams & Danny Penman — *Mindfulness* | 30 / 72 / 112 | Practices | Full lawful EPUB supplied by maintainer |
| Consciousness and calm | William B. Irvine — *A Guide to the Good Life* | 30 / 72 / 112 | Practices | Full lawful RU and EN EPUB editions supplied by maintainer |
| Consciousness and calm | Robert Pirsig — *Zen and the Art of Motorcycle Maintenance* | 36 / 90 / 144 | — | Full lawful EPUB supplied by maintainer |
| Consciousness and calm | David R. Hawkins — *Letting Go: The Pathway of Surrender* | 36 / 90 / 144 | Practices | Full lawful RU EPUB supplied by maintainer; spiritual and clinical claims need explicit evidence boundaries |
| Health and protocols | Bessel van der Kolk — *The Body Keeps the Score* | 36 / 90 / 144 | Practices | Full lawful RU EPUB supplied by maintainer; treatment and neuroscience claims need current independent corroboration |
| Health and protocols | Moshe Feldenkrais — *Awareness Through Movement* | 36 / 90 / 144 | Practices | Full local RU EPUB and PDF; the twelve lessons must remain practices, not medical prescriptions |
| Health and protocols | Moshe Feldenkrais — *The Potent Self* | 36 / 90 / 144 | Practices | Distinct complete English edition is lawfully borrowable through Open Library; full-text build requires an active loan or a supplied purchased EPUB |
| Systems and work | Jake Knapp & John Zeratsky — *Make Time* | 30 / 72 / 112 | Practices | Full lawful EPUB supplied by maintainer |
| Fiction and adventure | Robert Louis Stevenson — *Treasure Island* | 24 / 60 / 96 | For my son · 14+ | Public-domain text; no ending in Essential, full plot only in Deep |
| Fiction and adventure | Arthur Conan Doyle — *The Lost World* | 36 / 90 / 144 | For my son · 14+ | Public-domain text; no ending in Essential, full plot only in Deep |
| Fiction and adventure | J. R. R. Tolkien — *The Hobbit* | 36 / 90 / 144 | For my son · 14+ | Copyright-safe analytical digest; no ending in Essential, full plot only in Deep |
| Fiction and adventure | Ursula K. Le Guin — *A Wizard of Earthsea* | 36 / 90 / 144 | For my son · 14+ | Copyright-safe analytical digest; no ending in Essential, full plot only in Deep |
| Fiction and adventure | Terry Pratchett — *The Wee Free Men* | 24 / 60 / 96 | For my son · 14+ | Copyright-safe analytical digest; no ending in Essential, full plot only in Deep |
| Fiction and adventure | Douglas Adams — *The Hitchhiker’s Guide to the Galaxy* | 24 / 60 / 96 | For my son · 14+ | Copyright-safe analytical digest; no ending in Essential, full plot only in Deep |
| Fiction and adventure | Andy Weir — *Project Hail Mary* | 24 / 60 / 96 | For my son · 14+ | Copyright-safe analytical digest; no ending in Essential, full plot only in Deep |

## Execution status — 2026-10-31

The catalogue currently registers **22 books / 2,553 screens**, including **18 of the 25 expansion titles** and four pre-existing readers. Registration is local until the associated PR is merged and its production deployment verified.

- Ready for release: *Mindfulness* and *Behave* after cold-review corrections and standalone matrices of 3,424 and 6,480 visits respectively.
- In repair/review: *Antifragile*, *Determined*, *Zen and the Art of Motorcycle Maintenance*.
- Collectors restarted under the approved analytical-digest source boundary: *The Wee Free Men*, *The Hitchhiker’s Guide to the Galaxy*, *Project Hail Mary*. Missing a full EPUB alone is not a blocker; each package still needs enough lawful, claim-level evidence for 24 / 60 / 96 distinct screens and a cold review before publication.
- Source-blocked: *The Potent Self*. An active controlled loan or supplied purchased EPUB is still needed for the planned fidelity build.

## Source-access notes

| Requested book | Status | Next action |
| --- | --- | --- |
| Moshe Feldenkrais — *The Potent Self* | Found online as a distinct 1985 Harper & Row edition, 240 pages, ISBN 0062503200, with controlled digital borrowing at Open Library (`OL20945624M`, Internet Archive item `potentselfguidet0000feld`). | Borrow it through the maintainer’s Open Library account or supply a purchased EPUB before a fidelity-based collector run. |
| Moshe Feldenkrais — *The Elusive Obvious* | Natural methodological companion; current 2019 North Atlantic Books edition is available in paperback and ebook, ISBN 9781623173340 / 9781623173357. No lawful open full text was found. | Purchase or supply the ebook if this title is preferred over *The Potent Self*. |

## Quality gates

- Complete claim or plot map before screen writing.
- Essential remains a complete argument or spoiler-safe story invitation.
- RU and EN preserve the same claims, quantities, qualifications and screen IDs.
- Every factual screen has source IDs and a provenance type: book, corroboration or synthesis.
- Health books distinguish evidence strength, outdated claims and non-medical guidance.
- Fiction uses the agreed spoiler policy: Essential avoids the ending; Deep may contain the full plot and ending.
- Build from schema-v2 `story-data.json`; run the deterministic audit and real-browser QA before catalogue integration.
