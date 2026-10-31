# The Art of War — editorial repair, group 10

Verdict: **REBUILD**. Collector package rebuilt; ready for independent editorial check. Publication is not certified.

## What was actually read

All 70 existing RU/EN screen pairs, including covers, subtitles, final screen, and source/method copy. Authoring JSON, collector embedded corpus and root published embedded corpus were compared: all 70 pairs were identical. Runtime code was inspected for corpus transformations: filtering and rendering, no later prose substitution. Root HTML was read only. Built metadata differed from authoring through computed modes; this did not alter the text.

Primary work: Sunzi, *The Art of War*, Lionel Giles translation (1910), basic text without the later commentary, Project Gutenberg #17405. The full thirteen chapters were continuously read for this repair in three consecutive windows, with no omitted intervening text. The text contains roughly 61,000 characters including contents. Public-domain source: https://www.gutenberg.org/cache/epub/17405/pg17405-images.html . This supports a digest of this translation, not certification against Classical Chinese, all manuscript variants or every later commentator. The owner's Russian EPUB was identified but not used as a substitute or claimed read. Earlier secondary-source reading claims are not inherited as this worker's reading.

## Concrete findings in the delivered text

| Existing stable ID | Wording / defect | Expected correction and primary anchor |
| --- | --- | --- |
| `cover` | “трактат об ответственности за конфликт” gives a modern moral thesis priority over conquest. | Introduce the actual strategic problem: victory while preserving one's own state and strength; I.1–2, II, III.1–7. |
| `whole-book-map` | “Это карта нашего чтения” interrupts the opening after several scholarly screens. | Remove the administrative map; move directly from the stakes into assessment, I.3–26. |
| `assessment-before-action` | “не разрешение манипулировать людьми в обычных отношениях” inserts a recurring contemporary lesson. | Give the chapter's deception argument in its military setting, I.18–25, without a lesson about relationships. |
| `depletion` | “не между трудолюбием и ленью” answers an objection the book never raises. | Restore the causal sequence: prolonged operations, exhaustion, other rulers exploiting weakness; II.2–7. |
| `siege-emotion` | “уже понесённые затраты … создают эмоциональное давление” supplies a modern causal diagnosis. | Report what the source establishes: months of preparation, an irritated general, failed assault and casualties; III.4–5. |
| `organization-at-scale` | “структуры восприятия” and “инфраструктура связи” turn concrete military organization into abstract management prose. | Restore divisions, signals, drums and banners; V.1–4, VII.23–26. |
| `water-with-conditions` | “не исчезает ответственность за результат” replaces the water image with a leadership lesson. | Explain water taking its course from ground and an army adapting to its opponent; VI.25–34. |
| `speed-has-a-bill` | “критика изолированной метрики” names a modern lesson instead of the army's predicament. | Recount baggage versus speed, forced march, strong ahead and weary behind; VII.6–11. |
| `no-exit-modern-limit` | Removing resources from a workplace is an invented modern example. | Delete the example. Preserve the actual coercion of the army, XI.23–25,35–40,50–59. |
| `bounded-modern-example` | “Допустим, организация выбирает большой запуск” is entirely the digest writer's scenario. | Delete; no counterpart in I–XIII. |
| `five-reading-questions` / `final` | Five questions and “Наш итог” replace the ending with the compiler's framework. | Finish with intelligence and the book's relation of preparation, preservation and victory; XIII.1–27, with I–XII in context. |
| `uncertain-author`, `manuscript-witness`, `layers-of-reading`, `modern-reception`, `dated-hypotheses` | Long scholarly preface and postscript displace the argument; not factual errors merely because they are secondary. | Remove as reading screens. Keep edition/translation boundary in Sources. No modern scholarly hypothesis is needed to retell the base text. |

No decisive RU/EN factual disagreement was found in the 70 old pairs. The main defect was the same in both languages: commentary, generalized vocabulary, repeated caveats, and invented modern applications taking the place of the connected treatise. This is a reading-experience finding, not a lexical score.

## Result and self-check

All 36 new pairs were authored and substantively reread in order. Rebuilt all body copy and cover/final copy; retained useful IDs where the concept survives. Essential follows every chapter's central argument; Core adds mechanisms and examples; Deep adds six subordinate passages. Counts changed **22/46/70 → 15/30/36**, with no quota padding. `contentMode: explanatory`; fresh-session default RU/dark/Essential. Every body screen is an attributed account of the book, not a compiler “Synthesis”. No scenes, dialogue, quotations, motives, modern anecdotes, or print page numbers were invented. The five spies, harsh coercion and deception remain rather than being sanitized into humane leadership.

Sources were narrowed to the actually read full primary translation. New per-screen locators refer to its chapter/paragraph numbering. Claims about the ancient text are not claims that its numerical or medical assertions are validated modern facts. No full source text or private extraction was put in the repository.

Maintained `build_story.mjs` rebuilt only this collector HTML. Browser check used an owned Chrome process, unique temporary profile and 30-second bound; no server, no network, cleanup after completion. Eight viewport/language/theme combinations: 320×568 and 1440×900, RU/EN, dark/light; all 36 screens rendered without horizontal overflow or runtime exceptions; 15/30/36 contents counts, source dialog and Home href checked. Embedded revised screens equal authoring JSON. Browser JSON/screenshots are private outside the repository. This is a structural/display check, not an independent editorial verdict. A first screenshot was captured mid-transition; no display claim relies on that low-opacity frame.

## Publisher attention

Do not copy collector HTML blindly over the maintained root shell. Integrate the revised corpus through maintained tools and retain current icon header, focus behavior and saved-progress protections. Update root/catalogue counts, times and description from the revised corpus. Old progress IDs that were removed need the maintained fallback; retained IDs now contain rewritten copy. No book-specific spoiler consent exists or is needed. Root readers/catalogue/shared shell were not edited. No Git, PR, deployment or external messaging was performed.
