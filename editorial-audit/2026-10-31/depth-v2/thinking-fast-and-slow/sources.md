# Thinking, Fast and Slow — sources and evidence boundary

Candidate for the expanded nonfiction pilot. Work began 2026-10-31; finished local checks 2026-11-01 Europe/Warsaw. Status: ready for independent check, **not** editorial acceptance or permission to publish.

The current collector, old ready manifest, reviews and parent repair record remain immutable comparison inputs. Both depth corrections and the later root-personal-review mandate in BRIEF.md were read. This directory alone is writable for this implementation.

## Identity and actual reading

Primary evidence is the user-owned expanded directory EPUB `Думай медленно Решай быстро 1.epub`, read in place under the supplied Apple Books root. OPF title: `Думай медленно… Решай быстро`; creator: `Даниэль Канеман` (whitespace normalized); 117 spine entries. `content.opf` and the actual `content0.html` copyright page verify Daniel Kahneman 2011, translation by Школа перевода Баканова 2013, AST Publishers 2014. Two previously rejected 5.2k/5.7k-word condensations were not used or reintroduced.

The introduction and its five-part roadmap (`content0–2`), supporting sections for every retained mechanism/experiment, and the entire conclusion (`content101` from “Выводы”, then `content102–103`) were read. This is mapped selective reading, not a continuous cover-to-cover reading of all 117 entries. The following are actual substantive reads, not an inventory claim:

- Complete spine texts read (41): `content0.html`, `content1.html`, `content2.html`, `content3.html`, `content5.html`, `content7.html`, `content20.html`, `content23.html`, `content25.html`, `content28.html`, `content29.html`, `content32.html`, `content38.html`, `content39.html`, `content42.html`, `content47.html`, `content50.html`, `content54.html`, `content55.html`, `content56.html`, `content57.html`, `content58.html`, `content59.html`, `content60.html`, `content61.html`, `content66.html`, `content67.html`, `content68.html`, `content69.html`, `content72.html`, `content76.html`, `content78.html`, `content82.html`, `content84.html`, `content92.html`, `content94.html`, `content95.html`, `content98.html`, `content100.html`, `content102.html`, `content103.html`.
- Complete bounded supporting sections:
  - `content52.html`: Chapter 21 opening “Интуиция и формулы – кто кого?” through end of this spine file; preceding Chapter 20 material excluded.
  - `content65.html`: “«Прижизненный эпикриз» – частичное решение проблемы” through the next discussion heading; later Bernoulli opening excluded.
  - `content71.html`: Full token-market / mug-market / seller–chooser–buyer comparison, from “Мы с Кнетчем и Талером разработали эксперимент” through file end. Earlier wine/ticket discussion not relied upon.
  - `content85.html`: “Политика рисков” through “Разговоры о политике рисков”; later mental-accounting chapter excluded.
  - `content101.html`: “Выводы” through file end, including the conclusion’s two-selves discussion. Earlier Chapter 38 material excluded.

The original EPUB remains read-only. Its prose, complete chapters and private extractions were not copied into this directory or the public repository. `read-source.py` reads selected sections in memory only. `coverage-map.json` records source locators and candidate IDs, not primary-text extracts. Appendices A/B, the complete notes and acknowledgments were not substantively read for this pilot; their existence was checked in the spine/heading inventory. Retained examples are supported by the main text rather than reconstructed from the appendices or memory.

EN is an original translation of the new RU condensation. There was no full English edition or line-by-line comparison with the published English original. RU/EN meaning, numbers, conditions and paragraph ordering were checked during authorship. This does not certify the official Russian translation against English.

## Public sources and their roles

1. [Macmillan: Thinking, Fast and Slow](https://us.macmillan.com/books/9780374533557/thinkingfastandslow/) identifies the original and provides an official English introduction excerpt. The page and available excerpt were consulted; neither proves later chapter content. Source 1 in the reader means the **private primary book**; its public URL is an identification link. Source 2 means the publisher/excerpt only.
2. [Doyen et al. (2012), Behavioral Priming](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0029081): abstract and introductory method discussion consulted. The walking-speed replication raises procedure/expectation concerns. That social-priming episode is omitted; this does not refute semantic priming generally or validate anchoring.
3. [Hagger et al. (2016), registered ego-depletion replication](https://journals.sagepub.com/doi/10.1177/1745691616652873): abstract and protocol introduction consulted. Its small estimate spans zero. Ego depletion is not retold as established fact. This protocol is not a final verdict on every self-control study.
4. [Killingsworth, Kahneman & Mellers (2023), income and emotional well-being](https://pubmed.ncbi.nlm.nih.gov/36857342/): abstract consulted. Its group-dependent relationship qualifies carrying the historical income threshold into present advice; that threshold is omitted. The direct PNAS page returned 403; PubMed supplied the primary abstract.

All five source records remain globally accessible in the HTML Sources dialog. The three later papers have role `reference` and qualify scope; they are not substituted for the book or cited as support for every retained experiment. No contemporary systematic review or consensus certificate is claimed. In particular, the book's associative explanation of anchoring and its assertiveness/list-length results remain **reported 2011 book accounts**, with their stated experimental conditions; this implementation has not independently revalidated them. Statistical identities such as set inclusion and two-toss arithmetic are distinguished from empirical generalizations.

## The retained argument

The book first asks how automatic impressions and effortful checking interact. The statistics section tests plausible stories against sample size, base rates and logical constraints. The expertise section then asks whether confident predictions were learnable, stable and better than consistent rules, before returning to the author's own planning failure. Prospect theory shifts from beliefs about the world to evaluations of gains, losses and chances; framing shows that preferences may depend on representation. The last part asks whether choosing a remembered episode expresses the well-being of the person who lived through its moments. The conclusion revisits two selves, ideal agents/real people, and two systems in reverse order, without promising immunity.

This is the fullest **retained** explanatory account in this candidate, not an assertion that every chapter and experiment survives. The 38-chapter map below exposes substantial omissions rather than counting a name as coverage. Deep preserves all 64 authored units; Essential and Core are nested coherent routes. The additional depth develops actual cases, alternative explanations and limits, not a new coaching framework.

## Chapter/argument coverage

| Chapter in verified RU edition | Coverage | Candidate unit IDs | Substance and deliberate omissions |
|---|---|---|---|
| 1. Действующие лица | Развёрнуто | two-systems; the-gorilla | Системы как обозначения режимов; восприятие и внимание. Зрительные иллюзии главы не развёрнуты. |
| 2. Внимание и усилия | Развёрнуто | attention-and-effort | Преобразование цифр, зрачки, дополнительная задача, предел внимания. |
| 3. Ленивый контролёр | Выборочно | bat-and-ball | Проверяемая арифметическая подсказка. Истощение самоконтроля и другие тесты не пересказаны. |
| 4. Ассоциативный механизм | Опущено как самостоятельная глава | — | Социальный прайминг не пересказан; ассоциативная память объясняется в связи с WYSIATI и экспертизой. |
| 5. Когнитивная лёгкость | Выборочно | cognitive-ease | Лёгкость обработки, знакомость, иллюзия известности и истины по content12–13. Опыт с именами в книге отделён от отчёта об исследованиях Джакоби; настроение и отдельные шрифтовые опыты не развёрнуты. |
| 6. Нормы, неожиданности и причины | Опущено | — | Специальные примеры нормы и причинной связности не включены. |
| 7. Механизм поспешных выводов | Выборочно | a-complete-looking-story | WYSIATI и одностороннее судебное изложение; отдельная серия опытов об ореоле не пересказана. |
| 8. Как выносятся суждения | Опущено как самостоятельная глава | — | Базовые оценки, прототипы и сопоставление интенсивностей не имеют отдельного объяснительного блока. |
| 9. Ответ на более лёгкий вопрос | Развёрнуто | the-easier-question | Подстановка и реальный рассказ автора о финансисте/Ford; без новых инвестиционных аналогий. |
| 10. Закон малых чисел | Развёрнуто | small-samples; law-of-small-numbers | Оба края распределения рака почки, размер выборки, шары. История малых школ не включена. |
| 11. Эффект привязки | Развёрнуто | the-wheel; two-kinds-of-anchors | 10/65 → 25/45, недостаточная корректировка и избирательная активация. Судейские и торговые примеры не включены. |
| 12. Наука доступности | Развёрнуто | easy-to-recall; six-or-twelve | K из введения; 6/12 примеров и объяснение трудности музыкой. Не все перечисленные в книге модераторы удержаны. |
| 13. Доступность, эмоции, риск | Развёрнуто выборочно | affect-and-public-risk | Оценка преимуществ/рисков технологий, каскад, позиции Словика и Санстейна и двойственная позиция автора. Исторические экологические споры и частоты смертности не переносятся как современные факты. |
| 14. Специальность Тома В. | Выборочно | base-rates; bayesian-update | Стив из введения и байесовское соединение 3% с отношением правдоподобий 4. Полный портрет/ранжирование Тома В. не удержаны. |
| 15. Линда: лучше меньше | Развёрнуто | linda; linda-and-language | Включение множеств, различие правдоподобия и вероятности, влияние представления и возражения. Посуда, бейсбольные карточки и прочие дополнительные задачи опущены. |
| 16. Причины побеждают статистику | Выборочно | causal-base-rates | Две математически одинаковые задачи о такси, статистические/причинные базовые частоты и авторская граница применения групповых суждений. Опыты обучения психологии не включены. |
| 17. Регрессия к среднему | Развёрнуто | flight-instructors; coins-and-golf | Инструкторы, монеты, гольф, отбор экстремумов, обратное во времени сравнение. История Гальтона не включена. |
| 18. Как справляться с интуитивными предсказаниями | Опущено как самостоятельная глава | — | Прогноз с регрессией показан через гольф в главе 17. Четырёхшаговая процедура Джули и отдельные прогнозы главы 18 не пересказаны. |
| 19. Иллюзия понимания | Выборочно | after-the-result | Записанные прогнозы поездки Никсона и ретроспекция, оценка по результату. Истории успеха компаний не удержаны. |
| 20. Иллюзия значимости | Выборочно | the-record-of-skill | 25 консультантов × 8 лет, 28 сравнений, устойчивость умения. Другие отборочные/политические случаи не включены. |
| 21. Интуиция и формулы — кто кого? | Развёрнуто | formulas-and-judgment; rules-and-exceptions; interview-in-parts; hiring-procedure | Мил, ограниченность/постоянство формул, сломанная нога, Доуз, армейское интервью и процедура найма. Бордо, Апгар и отдельный раздел неприятия алгоритмов опущены. |
| 22. Интуиция экспертов: когда стоит ей доверять? | Развёрнуто | kleins-objection; when-intuition-learns; learning-from-feedback | Кляйн, пожар, план по распознаванию, регулярность среды, практика, обратная связь, границы по задачам. Не универсальное требование определённого числа часов. |
| 23. Взгляд извне | Развёрнуто | curriculum-project; outside-view | История учебника с исходными прогнозами и исходом, сравнение классов, три шага внешнего взгляда, стимулы к неточным планам. |
| 24. Двигатель капитализма | Выборочно | optimism-and-enterprise; premortem | История мотеля, различие готовности рисковать и оптимистичного прогноза, польза и цена оптимизма, открытый вопрос поддержки и процедура Кляйна. Исход мотеля не придуман; исторические уровни выживания бизнеса и прочие исследования главы не развёрнуты. |
| 25. Ошибки Бернулли | Развёрнуто | money-and-utility; reference-point | Деньги/полезность и Джек/Джилл. История психофизики, страхование груза и петербургский парадокс не включены. |
| 26. Теория перспектив | Развёрнуто | two-gifts; diminishing-sensitivity; losses-and-gains; limits-of-prospect-theory | Смена точки отсчёта, отражение предпочтений, потери/приобретения, неполнота модели: разочарование и сожаление. Теорема Рабина не доказывается. |
| 27. Эффект владения | Развёрнуто выборочно | a-mug-of-ones-own; goods-for-trade | Жетоны/кружки, третья группа и три цены, товары для себя/обмена, опыт торговцев и методические границы. Вино, билеты, нейроснимки и бедность не пересказаны. |
| 28. Неудачи | Опущено | — | Негативность, цели, справедливость, статус-кво и право собственности не имеют отдельного блока. |
| 29. Четырёхчастная схема | Развёрнуто | probability-weights; fourfold-pattern; lawsuit-negotiations | Вероятность/вес, возможность/определённость, все четыре сочетания и переговоры. Парадокс Алле и полная таблица весов не воспроизводятся. |
| 30. Редкие события | Выборочно | description-and-experience | Выбор по описанию/опыту, кнопки, неполнота интерпретации. Прочие примеры яркости и формата частот опущены. |
| 31. Политика рисков | Развёрнуто | sam-and-tosses; risk-policy | Сэм, два броска со всеми исходами, серия и три самостоятельные оговорки. Не советы о текущих финансовых продуктах или частоте проверки портфеля. |
| 32. Ведение счетов | Выборочно | mental-accounts-and-sunk-costs | Полезность счетов для самоконтроля, задача Талера о билетах, невозвратные затраты, учебник и конфликт интересов руководителя/фирмы. Налоговые рекомендации, отдельные случаи сожаления и диспозиционный эффект не развёрнуты. |
| 33. Инверсии | Выборочно | joint-and-separate-evaluation | Раздельная/совместная оценка двух экспериментальных сценариев ограбления; одинаковая травма, разная компенсация и явный принцип сравнения. Ставки, словари и другие межкатегориальные задачи опущены. |
| 34. Рамки и реальность | Развёрнуто выборочно | same-outcomes-new-frame; behind-the-frame | Полные A/B и A′/B′, эквивалентность, отсутствие готового независимого предпочтения. Топливо, медицинский выбор, налоги и другие хорошие рамки не пересказаны. |
| 35. Два «я» | Развёрнуто | two-selves; pain-and-memory; the-cold-hand; time-and-stories | Два вида полезности, текущие/поздние оценки, два профиля боли, холодная рука с условным 80%, длительность. Не медицинская инструкция. |
| 36. Жизнь как история | Опущено как самостоятельная глава | — | Джен, опера, отпуск без памяти и специальные задачи о жизни как истории не пересказаны. |
| 37. Ощущение благополучия | Развёрнуто выборочно | day-reconstruction; two-wellbeing-questions | Выборка переживаний, реконструкция дня, U-индекс, различие двух оценок. Порог дохода и ранжирование групп/занятий не перенесены как современная норма. |
| 38. Оценка жизни | Выборочно | focusing-illusion | Реальные ответы и прогнозы студентов Калифорнии/Среднего Запада, фокусировка. Клинические примеры адаптации, семейные опросы и покупки не развёрнуты. |

Introduction: `the-question`, with the source roadmap read in full. Conclusion: `both-selves`, `econs-and-humans`, `limits-of-correction`, `final`, supported by all three conclusion sections. Chapter boundaries in this EPUB often cross spine files; a filename is a locator, not an assertion that the whole numbered chapter was read.

## Experiment and procedure map by exact candidate unit

The separate [coverage-map.md](coverage-map.md) and [coverage-map.json](coverage-map.json) list all 64 units, all 110 screen IDs, book chapters and exact primary content filenames. A complete case may span two adjacent phone screens. Every screen preserves source 1 and `claimType: book`; no unmarked digest inference or invented example is introduced.

## Mandatory old corrections

KAH-01: `same-outcomes-new-frame` keeps A: 200 saved; B: 1/3 all 600 saved and 2/3 none; A′: 400 deaths; B′: 1/3 no deaths and 2/3 all 600 deaths. Equivalence can be inspected. Direct source: `content92.html`, actually read in full.

KAH-02: `risk-policy` keeps the independent-games condition, protection of overall well-being, **and** the separate exclusion of long-shot lotteries. `sam-and-tosses` also retains a possible loss in the two-toss bundle; it promises no certain gain. Direct source: `content84.html`, read in full, with the risk-policy section of `content85.html`. The wording is the author's proposal under these conditions, not current financial guidance.

No full-book translation endorsement, present-science endorsement, clinical recommendation or investment recommendation is claimed. The root must personally read/assess the candidate and key primary passages before any replacement publication; an external review or these local checks cannot supply that acceptance alone.

## Parent additions and actual source checking

The original writer scope above is preserved as its own reading claim. Root subsequently read all97 original RU/EN pairs and both complete maps, composed six additional connected bilingual units, and checked their actual primary text in memory. New retained units use content12 P008–018/content13; content33–34; content40 P008–032; content62 P013–019/content63; content85 P013–027/content62 P007; and content88 P008–017. The root also read content58,94,95 and84 throughout, selected28/71/98 passages, and content60/55. The primary reading ledger distinguishes these ranges from full-volume reading.

The medical passage restores the author's own conditional contrast between accumulated pain and memory; an unmarked absolute editorial veto was removed. Book-era study context is explicit. Historical empirical reports remain reports of the book, not current clinical/financial advice or a contemporary consensus certificate. Root read the Doyen abstract, Hagger's indexed publisher abstract and the2023 joint income reanalysis abstract for the narrow source-note qualifications; neither full research paper nor all later studies were reviewed. Root's final personal acceptance is still pending until route reading and checks finish.

Root subsequently read the complete electronic conclusion witnesses content101 P001–019, content102 P001–012 and content103 P001–013. All current 110 RU/EN pairs and the cumulative Essential27/Core74 routes were personally read. The pain-profile case now appears in Essential so that the experience/memory distinction is demonstrated before the closing discussion. These are additional selected primary checks, not continuous full-book reading.
