from pathlib import Path
import json,hashlib,re,datetime
P=Path(__file__).resolve().parent
D=json.loads((P/'story-data.json').read_text());C=json.loads((P/'coverage-map.json').read_text());M=json.loads((P/'qa/metrics-and-integrity.json').read_text())
full=[0,1,2,3,5,7,20,23,25,28,29,32,38,39,42,47,50,54,55,56,57,58,59,60,61,66,67,68,69,72,76,78,82,84,92,94,95,98,100,102,103]
sections={52:'Chapter 21 opening “Интуиция и формулы – кто кого?” through end of this spine file; preceding Chapter 20 material excluded.',65:'“«Прижизненный эпикриз» – частичное решение проблемы” through the next discussion heading; later Bernoulli opening excluded.',71:'Full token-market / mug-market / seller–chooser–buyer comparison, from “Мы с Кнетчем и Талером разработали эксперимент” through file end. Earlier wine/ticket discussion not relied upon.',85:'“Политика рисков” through “Разговоры о политике рисков”; later mental-accounting chapter excluded.',101:'“Выводы” through file end, including the conclusion’s two-selves discussion. Earlier Chapter 38 material excluded.'}
C['readingScope']={'edition':'Owned full expanded Russian EPUB, AST 2014; Bakanov translation school 2013; original 2011','spineEntries':117,'verifiedMetadata':['title','creator','copyright page','five-part map','introduction','conclusion','appendix/note headings'],'completeSpineTextsRead':[f'content{i}.html' for i in full],'completeBoundedSectionsRead':{f'content{i}.html':v for i,v in sections.items()},'continuousWholeBookReading':False,'fullEnglishCollation':False,'privateExtractsPersisted':False,'note':'Complete supporting sections were read for every retained mechanism/case. Whole files listed here were actually read, in some cases in overlapping calls after output truncation. An inventory, download or heading scan is not counted as substantive reading.'}
(P/'coverage-map.json').write_text(json.dumps(C,ensure_ascii=False,indent=2)+'\n')
rows=[
(1,'Действующие лица','Развёрнуто','two-systems; the-gorilla','Системы как обозначения режимов; восприятие и внимание. Зрительные иллюзии главы не развёрнуты.'),
(2,'Внимание и усилия','Развёрнуто','attention-and-effort','Преобразование цифр, зрачки, дополнительная задача, предел внимания.'),
(3,'Ленивый контролёр','Выборочно','bat-and-ball','Проверяемая арифметическая подсказка. Истощение самоконтроля и другие тесты не пересказаны.'),
(4,'Ассоциативный механизм','Опущено как самостоятельная глава','—','Социальный прайминг не пересказан; ассоциативная память объясняется в связи с WYSIATI и экспертизой.'),
(5,'Когнитивная лёгкость','Опущено','—','Повторение, знакомость, иллюзии истины, шрифтовые и настроенческие опыты не развёрнуты.'),
(6,'Нормы, неожиданности и причины','Опущено','—','Специальные примеры нормы и причинной связности не включены.'),
(7,'Механизм поспешных выводов','Выборочно','a-complete-looking-story','WYSIATI и одностороннее судебное изложение; отдельная серия опытов об ореоле не пересказана.'),
(8,'Как выносятся суждения','Опущено как самостоятельная глава','—','Базовые оценки, прототипы и сопоставление интенсивностей не имеют отдельного объяснительного блока.'),
(9,'Ответ на более лёгкий вопрос','Развёрнуто','the-easier-question','Подстановка и реальный рассказ автора о финансисте/Ford; без новых инвестиционных аналогий.'),
(10,'Закон малых чисел','Развёрнуто','small-samples; law-of-small-numbers','Оба края распределения рака почки, размер выборки, шары. История малых школ не включена.'),
(11,'Эффект привязки','Развёрнуто','the-wheel; two-kinds-of-anchors','10/65 → 25/45, недостаточная корректировка и избирательная активация. Судейские и торговые примеры не включены.'),
(12,'Наука доступности','Развёрнуто','easy-to-recall; six-or-twelve','K из введения; 6/12 примеров и объяснение трудности музыкой. Не все перечисленные в книге модераторы удержаны.'),
(13,'Доступность, эмоции, риск','Опущено','—','Каскады доступности, общественные риски и спор экспертов с публикой не пересказаны.'),
(14,'Специальность Тома В.','Выборочно','base-rates; bayesian-update','Стив из введения и байесовское соединение 3% с отношением правдоподобий 4. Полный портрет/ранжирование Тома В. не удержаны.'),
(15,'Линда: лучше меньше','Развёрнуто','linda; linda-and-language','Включение множеств, различие правдоподобия и вероятности, влияние представления и возражения. Посуда, бейсбольные карточки и прочие дополнительные задачи опущены.'),
(16,'Причины побеждают статистику','Опущено','—','Каузальные базовые частоты, такси, обучение психологии не пересказаны.'),
(17,'Регрессия к среднему','Развёрнуто','flight-instructors; coins-and-golf','Инструкторы, монеты, гольф, отбор экстремумов, обратное во времени сравнение. История Гальтона не включена.'),
(18,'Как справляться с интуитивными предсказаниями','Опущено как самостоятельная глава','—','Прогноз с регрессией показан через гольф в главе 17. Четырёхшаговая процедура Джули и отдельные прогнозы главы 18 не пересказаны.'),
(19,'Иллюзия понимания','Выборочно','after-the-result','Записанные прогнозы поездки Никсона и ретроспекция, оценка по результату. Истории успеха компаний не удержаны.'),
(20,'Иллюзия значимости','Выборочно','the-record-of-skill','25 консультантов × 8 лет, 28 сравнений, устойчивость умения. Другие отборочные/политические случаи не включены.'),
(21,'Интуиция и формулы — кто кого?','Развёрнуто','formulas-and-judgment; rules-and-exceptions; interview-in-parts; hiring-procedure','Мил, ограниченность/постоянство формул, сломанная нога, Доуз, армейское интервью и процедура найма. Бордо, Апгар и отдельный раздел неприятия алгоритмов опущены.'),
(22,'Интуиция экспертов: когда стоит ей доверять?','Развёрнуто','kleins-objection; when-intuition-learns; learning-from-feedback','Кляйн, пожар, план по распознаванию, регулярность среды, практика, обратная связь, границы по задачам. Не универсальное требование определённого числа часов.'),
(23,'Взгляд извне','Развёрнуто','curriculum-project; outside-view','История учебника с исходными прогнозами и исходом, сравнение классов, три шага внешнего взгляда, стимулы к неточным планам.'),
(24,'Двигатель капитализма','Выборочно','premortem','Сохранён полный смысл процедуры Кляйна и её ограниченность. Предпринимательский оптимизм, конкуренция и прочие случаи главы не развёрнуты.'),
(25,'Ошибки Бернулли','Развёрнуто','money-and-utility; reference-point','Деньги/полезность и Джек/Джилл. История психофизики, страхование груза и петербургский парадокс не включены.'),
(26,'Теория перспектив','Развёрнуто','two-gifts; diminishing-sensitivity; losses-and-gains; limits-of-prospect-theory','Смена точки отсчёта, отражение предпочтений, потери/приобретения, неполнота модели: разочарование и сожаление. Теорема Рабина не доказывается.'),
(27,'Эффект владения','Развёрнуто выборочно','a-mug-of-ones-own; goods-for-trade','Жетоны/кружки, третья группа и три цены, товары для себя/обмена, опыт торговцев и методические границы. Вино, билеты, нейроснимки и бедность не пересказаны.'),
(28,'Неудачи','Опущено','—','Негативность, цели, справедливость, статус-кво и право собственности не имеют отдельного блока.'),
(29,'Четырёхчастная схема','Развёрнуто','probability-weights; fourfold-pattern; lawsuit-negotiations','Вероятность/вес, возможность/определённость, все четыре сочетания и переговоры. Парадокс Алле и полная таблица весов не воспроизводятся.'),
(30,'Редкие события','Выборочно','description-and-experience','Выбор по описанию/опыту, кнопки, неполнота интерпретации. Прочие примеры яркости и формата частот опущены.'),
(31,'Политика рисков','Развёрнуто','sam-and-tosses; risk-policy','Сэм, два броска со всеми исходами, серия и три самостоятельные оговорки. Не советы о текущих финансовых продуктах или частоте проверки портфеля.'),
(32,'Ведение счетов','Опущено','—','Мысленные счета, невозвратные затраты и отдельные ситуации сожаления не пересказаны. Разочарование/сожаление выше — ограничения модели из главы 26.'),
(33,'Инверсии','Опущено','—','Совместная/раздельная оценка и судебные инверсии этой главы не развёрнуты.'),
(34,'Рамки и реальность','Развёрнуто выборочно','same-outcomes-new-frame; behind-the-frame','Полные A/B и A′/B′, эквивалентность, отсутствие готового независимого предпочтения. Топливо, медицинский выбор, налоги и другие хорошие рамки не пересказаны.'),
(35,'Два «я»','Развёрнуто','two-selves; pain-and-memory; the-cold-hand; time-and-stories','Два вида полезности, текущие/поздние оценки, два профиля боли, холодная рука с условным 80%, длительность. Не медицинская инструкция.'),
(36,'Жизнь как история','Опущено как самостоятельная глава','—','Джен, опера, отпуск без памяти и специальные задачи о жизни как истории не пересказаны.'),
(37,'Ощущение благополучия','Развёрнуто выборочно','day-reconstruction; two-wellbeing-questions','Выборка переживаний, реконструкция дня, U-индекс, различие двух оценок. Порог дохода и ранжирование групп/занятий не перенесены как современная норма.'),
(38,'Оценка жизни','Выборочно','focusing-illusion','Реальные ответы и прогнозы студентов Калифорнии/Среднего Запада, фокусировка. Клинические примеры адаптации, семейные опросы и покупки не развёрнуты.')]
source='''# Thinking, Fast and Slow — sources and evidence boundary

Candidate for the expanded nonfiction pilot. Work began 2026-10-31; finished local checks 2026-11-01 Europe/Warsaw. Status: ready for independent check, **not** editorial acceptance or permission to publish.

The current collector, old ready manifest, reviews and parent repair record remain immutable comparison inputs. Both depth corrections and the later root-personal-review mandate in BRIEF.md were read. This directory alone is writable for this implementation.

## Identity and actual reading

Primary evidence is the user-owned expanded directory EPUB `Думай медленно Решай быстро 1.epub`, read in place under the supplied Apple Books root. OPF title: `Думай медленно… Решай быстро`; creator: `Даниэль Канеман` (whitespace normalized); 117 spine entries. `content.opf` and the actual `content0.html` copyright page verify Daniel Kahneman 2011, translation by Школа перевода Баканова 2013, AST Publishers 2014. Two previously rejected 5.2k/5.7k-word condensations were not used or reintroduced.

The introduction and its five-part roadmap (`content0–2`), supporting sections for every retained mechanism/experiment, and the entire conclusion (`content101` from “Выводы”, then `content102–103`) were read. This is mapped selective reading, not a continuous cover-to-cover reading of all 117 entries. The following are actual substantive reads, not an inventory claim:

'''
source+=f'- Complete spine texts read ({len(full)}): '+', '.join(f'`content{i}.html`' for i in full)+'.\n'
source+='- Complete bounded supporting sections:\n'+''.join(f'  - `content{i}.html`: {v}\n' for i,v in sections.items())
source+='''
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

This is the fullest **retained** explanatory account in this candidate, not an assertion that every chapter and experiment survives. The 38-chapter map below exposes substantial omissions rather than counting a name as coverage. Deep preserves all 58 authored units; Essential and Core are nested coherent routes. The additional depth develops actual cases, alternative explanations and limits, not a new coaching framework.

## Chapter/argument coverage

| Chapter in verified RU edition | Coverage | Candidate unit IDs | Substance and deliberate omissions |
|---|---|---|---|
'''
source+=''.join(f'| {n}. {t} | {st} | {ids} | {note} |\n' for n,t,st,ids,note in rows)
source+='''
Introduction: `the-question`, with the source roadmap read in full. Conclusion: `both-selves`, `econs-and-humans`, `limits-of-correction`, `final`, supported by all three conclusion sections. Chapter boundaries in this EPUB often cross spine files; a filename is a locator, not an assertion that the whole numbered chapter was read.

## Experiment and procedure map by exact candidate unit

The separate [coverage-map.md](coverage-map.md) and [coverage-map.json](coverage-map.json) list all 58 units, all 97 screen IDs, book chapters and exact primary content filenames. A complete case may span two adjacent phone screens. Every screen preserves source 1 and `claimType: book`; no unmarked digest inference or invented example is introduced.

## Mandatory old corrections

KAH-01: `same-outcomes-new-frame` keeps A: 200 saved; B: 1/3 all 600 saved and 2/3 none; A′: 400 deaths; B′: 1/3 no deaths and 2/3 all 600 deaths. Equivalence can be inspected. Direct source: `content92.html`, actually read in full.

KAH-02: `risk-policy` keeps the independent-games condition, protection of overall well-being, **and** the separate exclusion of long-shot lotteries. `sam-and-tosses` also retains a possible loss in the two-toss bundle; it promises no certain gain. Direct source: `content84.html`, read in full, with the risk-policy section of `content85.html`. The wording is the author's proposal under these conditions, not current financial guidance.

No full-book translation endorsement, present-science endorsement, clinical recommendation or investment recommendation is claimed. The root must personally read/assess the candidate and key primary passages before any replacement publication; an external review or these local checks cannot supply that acceptance alone.
'''
(P/'sources.md').write_text(source)
coverage='# Thinking, Fast and Slow — retained argument and source map\n\nImplementation map, not an independent verdict. Files are relative to the verified private EPUB; no primary text is reproduced. Paragraphs were authored before screen segmentation. Each added screen stays in its unit’s depth so the unit’s qualifications cannot disappear alone.\n\n| Unit | Level | RU / EN title | Primary chapter and spine locations | Screen IDs |\n|---|---|---|---|---|\n'
coverage+=''.join(f'| {x["unit"]} | {x["level"]} | {x["ruTitle"]} / {x["enTitle"]} | {x["chapter"]}: '+', '.join(f'`{f}`' for f in x['primaryFiles'])+' | '+', '.join(f'`{f}`' for f in x['screenIds'])+' |\n' for x in C['units'])
coverage+='\nThe complete chapter/omission map and honest reading boundary are in sources.md. Plain connected drafts: draft.ru.md and draft.en.md. Segmented route exports: essential/core/deep.ru/en.md. Root review must inspect the complete prose, every route, key mechanisms and meaningful omissions, not infer explanatory quality from this map.\n'
(P/'coverage-map.md').write_text(coverage)
metrics='| Depth | Screens | RU body words | RU at 180 wpm | EN body words | EN at 220 wpm | Reader UI minutes RU / EN |\n|---|---:|---:|---:|---:|---:|---|\n'
for mode,m in M['modes'].items():metrics+=f'| {mode.title()} | {m["screens"]} | {m["ru"]["bodyWords"]:,} | {m["ru"]["bodyMinutes"]:.2f} min | {m["en"]["bodyWords"]:,} | {m["en"]["bodyMinutes"]:.2f} min | {m["ru"]["uiMinutes"]} / {m["en"]["uiMinutes"]} |\n'
qa='''# Local QA — expanded Thinking, Fast and Slow pilot

2026-11-01 Europe/Warsaw. Implementation checks only. Status: **ready-for-independent-check**, never self-PASS. Publication and root editorial acceptance remain open.

## Resulting scope and counts

The connected RU manuscript was written first, then translated into EN, before phone segmentation. There are 58 authoring units and 154 paired paragraphs, segmented into 97 bilingual screens. Every current collector screen ID (29/29, including cover/final) still exists; this preserves the slug and semantic resume anchors. The new authoring corpus is independent of the 29-screen collector. Its old HTML embedded screens match its old JSON; no root `<slug>.html` or exact catalogue slug entry exists at the inspected library root.

'''+metrics+'''
Body counts use the installed builder’s Unicode lexical-word regex, excluding cover, headings, subtitles, method/source notes and UI, but including the shared final. Full UI estimates include cover and headings; that explains the larger estimates shown on the cover. They are estimates, not timed reader measurements. Exact machine metrics and density are in `qa/metrics-and-integrity.json`.

The 8,311-word RU body lies within the authorized 8–12k planning range; there is no length deviation to justify. It is about four times the old ~2,040-word body. Quantity itself does not certify completeness. Deep contains every draft paragraph once; Core contains 5,873 RU words, and Essential 2,292. Both shorter routes remain explanatory rather than lists of conclusions.

During route review, “third principle” was changed to “another principle” so Essential does not depend on a missing second principle. The anchor case and probability weights were promoted into Essential so the shared closing discussion introduces no unexplained mechanism. This derived 25/68/97 rather than preserving the preliminary 22-screen short route. No padding or independent prose was generated from a screen target.

## Structural and offline checks

- Maintained installed builder: `/Users/pn/.codex/skills/book-tiktok/scripts/build_story.mjs`, read-only. No copied reader shell, runtime-logic patch, installed-skill edit, shared synchronization, content server or preview tool. Candidate-local CSS hides the unrelated generic seven-node “one model to take away” cover; the actual bilingual title/copy supplies a typographic cover. Header, Settings, Sources and state logic remain the maintained implementation.
- Deterministic audit: 69 checks, zero failures/warnings (`qa/structural.json`). This is a structural result only.
- Effective embedded screens and source records equal canonical JSON. `contentMode: explanatory`; RU/dark/Essential on fresh storage, Sans initially. Five global Sources records with honest book/publisher/reference roles. No remote runtime dependency; all fonts/licenses embedded.
- Offline `file://` Chromium traversal at 320×568, 390×844, 1024×768 and 1440×900, both languages, both themes, Sans and Serif, **each complete depth route**: 24 routes and 1,520 rendered visits per viewport. Titles and body paragraphs compared with data, exact counts/order checked, document/slide overflow checked and each body tail reached by scrolling. Zero unexplained runtime exceptions or remote requests.
- Settings gear opens without toggling theme; radio controls change actual theme/font; book ID, depth, counter and reading scroll preserved. Source and Contents dialogs, labels, icon-only one-row header, home link, rail and rail active ID checked.
- Actual platform-font records confirm embedded Geist for Sans in RU/EN, Source Serif 4 for RU Serif and Geist Serif for EN Serif. The localized fallback note remains visible. Not merely checking a CSS family declaration.
- Keyboard next/back, buttons, horizontal pointer swipe, vertical gesture discrimination, focus entry/exit, paging in focus, final restart, saved EN/Deep ID after reload, Continue and Start over checked. All 29 old stable IDs remain available in the new corpus.
- Additional iPhone-UA runs at 320 and 390 with actual CDP safe-area override (44 top/34 bottom): six controls in one row below the inset; guide automatic/open/close and EN manual localization; CDP touch swipe; emulated `navigator.standalone` hides guide/trigger. These are Chrome emulations, **not physical iPhone Safari/PWA tests**.
- Visually inspected final 320 light/RU Serif dense prose, desktop dark/EN quantitative case, and iPhone dark cover. Long phone prose intentionally scrolls vertically. No list/image layouts were added; no images are required by this text-led pilot.

Each run used `/usr/bin/timeout 30`, `/usr/bin/mktemp -d`, an isolated process group and `finally` cleanup, including the failed harness run. Reports confirm profile removal and zero surviving owned PIDs. Browser reports bind the exact candidate JSON/HTML/harness hashes. No other active browser instance was terminated.

## Harness corrections, not hidden product failures

The first screenshots were captured during the entrance opacity transition; screenshot timing was corrected and the final matrix recaptured after 350 ms. One initial iPhone check expected the pre-swipe saved ID after deliberately advancing with a touch swipe. The reader correctly saved the advanced screen; the harness now restores its intended fixture before testing reload. The original failed report is retained as `qa/browser-ios-390-harness-before-reset.json`; final iOS reports have zero failures and completed cleanup. No product shell/content workaround was made for either harness issue. A separate final visual finding removed the unrelated generic cover decoration through candidate-only CSS; the full final matrix was rerun.

## Editorial self-check and required next review

All 58 RU/EN units were authored/compared in meaning, all resulting screen pairs inspected through their data/rendering, and the three nested sequences checked for dependencies. This is the writer’s review. The source ledger separately identifies complete support sections, partial chapter coverage and omitted chapters; it does not claim a continuous full-book read. EN has not been collated with the complete English volume.

KAH-01 was checked against full `content92`: every branch of A/B and A′/B′ remains. KAH-02 was checked against full `content84`: independence, overall well-being and the long-shot exclusion are three distinct conditions. Two-toss outcomes preserve the possibility of loss. Controls, hash counts and lexical matching cannot establish any of these source meanings by themselves.

The next reviewer must read all 97 RU/EN pairs and all six language/depth routes; assess whether a reader understands **why** each mechanism works and how the five parts connect; inspect the 38-chapter omissions and experiment map; directly check key primary sections, the critical probability/risk qualifications, and any other disputed specificity. Under the latest BRIEF, the root personally performs and records final acceptance with exact hashes. A delegated PASS, word count or local technical check alone is insufficient.

Remaining boundaries: no continuous whole-volume reading, full English collation, exhaustive research-status review, physical iPhone/PWA test, production integration or external publication. Three later primary abstracts/method introductions qualify specific scope in Sources rather than silently rewrite the 2011 argument. No medical, financial, scientific or full-translation endorsement is claimed.

## Ownership and reproduction

Only this NEW candidate directory was written. Current collector, old ready manifest, reviews, books.json and prior records match intake hashes. No Git/PR/deploy/status/log/shared-shell action occurred. Root public readers were not created or changed.

Rebuild: `python3 prepare-candidate.py`; then `node build.mjs`, which invokes the maintained installed builder and applies only the documented local cover CSS. Audit command is recorded in `qa/structural.json`. Browser runs: `node browser-check.mjs 320` (likewise 390/1024/1440), and `node browser-check.mjs 320 --ios` / `390 --ios`. `node measure.mjs` checks embedding and hashes and writes the exact per-depth metrics. Do not use the later readiness manifest as editorial approval.
'''
(P/'QA.md').write_text(qa)
report='''# Expanded nonfiction pilot — implementation handoff

Status: ready-for-independent-check. No self-PASS, root acceptance or publication.

The previous 29-screen/~2,040-RU-word corpus was factually scoped but too compressed to establish explanatory depth. Both user corrections were applied by writing a new connected RU manuscript, translating it faithfully, then deriving nested phone beats. The candidate has 58 argument units and 97 RU/EN screen pairs. The 38-chapter map exposes whole omitted chapters as well as developed mechanisms; no label is treated as explanatory coverage.

'''+metrics+'''
The new sequence develops attention and effort, substitution/WYSIATI, small samples, availability, representativeness/base rates, anchoring/regression, hindsight and skill measurement, formulas/interviews, Klein’s expertise conditions, outside view/premortem, reference points/losses/probability weights/framing, and experienced/remembered well-being. Concrete studies carry the explanations and the author’s qualifications remain attached. Later research notes stay in global Sources; the 2011 book is not silently rewritten.

Read-only source scope: verified full AST 2014 owned Russian EPUB (2013 translation, original 2011), 117 entries, introduction/part map, complete supporting sections for every retained case and the entire conclusion. The exact complete-file/bounded-section list is in sources.md/coverage-map.json. This is not a continuous whole-volume reading or a comparison with the full English original. The full private text was not copied into the repository.

All 29 old stable IDs are retained. Local structural checks and six browser matrices are complete, including actual embedded-font rendering, fresh defaults, state, offline behavior, touch/safe-area emulation and owned-process cleanup. They establish implementation behavior rather than explanatory quality or source fidelity. QA.md records both resolved harness issues and the tests’ boundaries.

Important deliberate omissions include dedicated cognitive-ease, norm/cause, risk-cascade, causal-base-rate, Chapter 18 correction-procedure, negativity/fairness, mental-accounting, reversal and life-as-story chapters; several additional experiments inside covered chapters are omitted. Their absence is explicit, not passed off as full chapter coverage. The root must judge whether the retained arc now sustains the intended substantial condensation.

Next: root personally reads RU/EN and all nested routes, compares the complete chapter/argument map, checks key primary mechanisms and both repaired critical examples, and records acceptance/rejection against candidate hashes. Any independent reviewer is supporting evidence, never a replacement for root acceptance. Existing collector/ready/reviews/catalogue remain untouched and hash-identical. No publication, commit, PR or deployment occurred.
'''
(P/'implementation.md').write_text(report)
print('Wrote source/coverage/QA/implementation records; substantive full-file reads:',len(full),'bounded sections:',len(sections))
