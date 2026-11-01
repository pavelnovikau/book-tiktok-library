"""Book-local segmentation of the completed original bilingual prose.

No source-text extraction or shared asset mutation is performed here.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
SLUG = "why-zebras-dont-get-ulcers"
ESSENTIAL = {1, 2, 5, 6, 7, 11, 15, 19, 22, 26, 27, 31, 36, 38, 40,
             44, 46, 50, 52, 56, 60, 63, 64, 67, 69, 74, 78, 81, 85,
             86, 88, 89, 95, 104, 105, 106}
DEEP_ONLY = {3, 4, 8, 12, 14, 18, 20, 23, 25, 28, 30, 34, 37, 41, 43,
             45, 47, 49, 51, 53, 54, 57, 61, 66, 72, 75, 76, 80, 82, 87,
             91, 93, 96, 97, 99, 101, 103}
assert not (ESSENTIAL & DEEP_ONLY)
CHAPTER_LAST = [5, 9, 14, 18, 23, 30, 35, 45, 49, 55, 59, 62, 68, 76,
                80, 85, 95, 106]


def read_draft(lang):
    units = []
    text = (ROOT / f"draft-{lang}.md").read_text()
    for block in re.split(r"(?m)^## ", text)[1:]:
        title, body = block.split("\n", 1)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        assert len(paragraphs) == 2, (lang, title, len(paragraphs))
        units.append({"title": title.strip(), "paragraphs": paragraphs})
    return units


def section(chapter):
    if chapter <= 2:
        return {"ru": "Мобилизация", "en": "Mobilization"}
    if chapter <= 5:
        return {"ru": "Органы и энергия", "en": "Organs and energy"}
    if chapter <= 7:
        return {"ru": "Развитие и размножение", "en": "Development and reproduction"}
    if chapter <= 9:
        return {"ru": "Защита и боль", "en": "Defense and pain"}
    if chapter <= 12:
        return {"ru": "Память, сон, возраст", "en": "Memory, sleep, aging"}
    if chapter <= 15:
        return {"ru": "Оценка и уязвимость", "en": "Appraisal and vulnerability"}
    if chapter <= 17:
        return {"ru": "Вознаграждение и общество", "en": "Reward and society"}
    return {"ru": "Условия совладания", "en": "Conditions for coping"}


drafts = {lang: read_draft(lang) for lang in ("ru", "en")}
assert len(drafts["ru"]) == len(drafts["en"]) == CHAPTER_LAST[-1]
unit_count = len(drafts["ru"])
data = {
    "schemaVersion": 2,
    "slug": SLUG,
    "title": {"ru": "Почему у зебр не бывает инфаркта", "en": "Why Zebras Don't Get Ulcers"},
    "description": {
        "ru": "Роберт Сапольски: как полезная мобилизация становится хронической нагрузкой — от гормонов и органов до памяти, иерархии и неравенства.",
        "en": "Robert Sapolsky on how useful mobilization becomes a chronic burden, from hormones and organs to memory, hierarchy, and inequality.",
    },
    "defaultLanguage": "ru", "defaultTheme": "dark", "defaultMode": "essential",
    "contentMode": "explanatory",
    "methodNote": {
        "ru": "Оригинальное сокращённое изложение. Полностью прочитаны оба предисловия и основной текст всех 18 глав пользовательского русского EPUB Piter, ISBN 978-5-4461-1081-0; примечания прочитаны выборочно. Научная рамка — третье английское издание, а не обновление науки к дате русского файла 2021 года. Английский текст переводит это изложение и не сверен с опубликованным английским оригиналом. Пять современных проверок отдельно обозначены рядом с соответствующими тезисами. Главы и реальные опыты сохранены с условиями и ограничениями; часть примеров и подробностей опущена. Это не полный текст книги и не клиническое руководство.",
        "en": "An original condensed account. Both prefaces and the complete main text of all 18 chapters were read in the user's Russian Piter EPUB, ISBN 978-5-4461-1081-0; notes were consulted selectively. Its scientific framework is the third English edition, not an update to the Russian file's 2021 date. The English translates this condensation and was not collated against the published English original. Five contemporary checks are explicitly distinguished beside the relevant claims. Chapters and actual experiments retain their conditions and limits; some examples and details are omitted. This is neither the complete book nor a clinical guide.",
    },
    "sources": [
        {"id": 1, "role": "book", "title": "Robert M. Sapolsky — Why Zebras Don't Get Ulcers / Piter RU, ISBN 978-5-4461-1081-0",
         "url": "https://www.piter.com/product/pochemu-u-zebr-ne-byvaet-infarkta-psihologiya-stressa",
         "note": {"ru": "Первичный источник — личный полный русский EPUB: 18 глав и предисловия прочитаны целиком, примечания выборочно. Ссылка подтверждает издание; аннотация не заменяет книгу.", "en": "Primary evidence is the personally owned full Russian EPUB: all 18 main chapter bodies and prefaces were read; notes selectively. The link identifies the edition; its blurb is not the book evidence."}},
        {"id": 2, "role": "reference", "title": "NIDDK — Symptoms & Causes of Peptic Ulcers",
         "url": "https://www.niddk.nih.gov/health-information/digestive-diseases/peptic-ulcers-stomach-ulcers/symptoms-causes",
         "note": {"ru": "Только явно современное уточнение в рассуждении о язве. Проверено 2026-11-01.", "en": "Only the explicitly contemporary qualification in the ulcer discussion. Checked 2026-11-01."}},
        {"id": 3, "role": "reference", "title": "National Cancer Institute — Stress and Cancer",
         "url": "https://www.cancer.gov/about-cancer/coping/feelings/stress-fact-sheet",
         "note": {"ru": "Только явно современное уточнение о возникновении, прогрессировании и выживаемости. Проверено 2026-11-01.", "en": "Only the explicitly contemporary qualification concerning onset, progression, and survival. Checked 2026-11-01."}},
        {"id": 4, "role": "reference", "title": "NIMH — Depression",
         "url": "https://www.nimh.nih.gov/health/publications/depression",
         "note": {"ru": "Только современное уточнение многофакторности депрессии. Проверено 2026-11-01; терапевтический обзор не составлялся.", "en": "Only a contemporary qualification on depression's multiple contributing factors. Checked 2026-11-01; no treatment review was undertaken."}},
        {"id": 5, "role": "primary", "title": "Border et al. (2019) — No Support for Historical Candidate Gene or Candidate Gene-by-Interaction Hypotheses for Major Depression Across Multiple Large Samples",
         "url": "https://pubmed.ncbi.nlm.nih.gov/30845820/",
         "note": {"ru": "Прочитана полная аннотация первичного исследования, не полная статья. Узкое уточнение ранней гипотезы о генах-кандидатах; не отрицание роли наследственности и среды. Проверено 2026-11-01.", "en": "The full abstract of the primary study was read, not the full paper. A narrow qualification of early candidate-gene hypotheses, not a rejection of inherited or environmental influences. Checked 2026-11-01."}},
        {"id": 6, "role": "reference", "title": "NIDDK — Type 2 Diabetes",
         "url": "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes/type-2-diabetes",
         "note": {"ru": "Только современное уточнение: инсулин может применяться и при втором типе. Прочитаны соответствующие разделы этой страницы и обзор типов диабета NIDDK. Проверено 2026-11-01.", "en": "Only a contemporary qualification: insulin can also be used in type 2. Relevant sections here and NIDDK's overview of diabetes types were read. Checked 2026-11-01."}},
    ],
    "media": {},
    "screens": [{
        "id": "cover", "level": 1, "type": "cover", "sources": [],
        "copy": {
            "ru": {"section": "Роберт Сапольски", "title": "Почему у зебр не бывает инфаркта", "subtitle": "Психология стресса",
                   "body": "<p>Тело готовится бежать, пока человек лежит без сна. Сапольски прослеживает, как такая подготовка помогает пережить опасность и почему её затянувшаяся работа меняет органы, память и отношения. От нервов и гормонов этот путь ведёт к устройству общества.</p>", "visualAlt": "Типографическая обложка"},
            "en": {"section": "Robert Sapolsky", "title": "Why Zebras Don't Get Ulcers", "subtitle": "The physiology and psychology of stress",
                   "body": "<p>The body prepares to run while a person lies awake. Sapolsky follows how this preparation helps meet danger, and why its prolonged activity changes organs, memory, and relationships. From nerves and hormones, the argument leads to the organization of society.</p>", "visualAlt": "Typographic cover"},
        },
    }],
}

for number in range(1, unit_count + 1):
    chapter = next(i for i, last in enumerate(CHAPTER_LAST, 1) if number <= last)
    labels = section(chapter)
    sources = [1]
    if number in {17: 6, 22: 2, 44: 3, 69: 4, 76: 5}:
        sources.append({17: 6, 22: 2, 44: 3, 69: 4, 76: 5}[number])
    screen = {
        "id": "final" if number == unit_count else f"unit-{number:03d}",
        "level": 1 if number in ESSENTIAL else 3 if number in DEEP_ONLY else 2,
        "claimType": "book", "sources": sources,
        "bookLocation": {
            "chapter": chapter,
            "epubFile": f"OEBPS/Text/978544611081-{chapter + 1}.xhtml",
            "readingLedgerFile": f"{chapter + 5:03d}-978544611081-{chapter + 1}.txt",
            "draftUnit": number,
        },
        "copy": {},
    }
    if number == unit_count:
        screen["final"] = True
    for lang in ("ru", "en"):
        unit = drafts[lang][number - 1]
        screen["copy"][lang] = {
            "section": labels[lang], "title": unit["title"],
            "body": "".join(f"<p>{html.escape(p, quote=False)}</p>" for p in unit["paragraphs"]),
        }
    data["screens"].append(screen)

data["targetModes"] = {mode: sum(s["level"] <= level for s in data["screens"])
                       for mode, level in (("essential", 1), ("core", 2), ("deep", 3))}
(ROOT / "story-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
(ROOT / "routes").mkdir(exist_ok=True)
for mode, level in (("essential", 1), ("core", 2), ("deep", 3)):
    for lang in ("ru", "en"):
        result = ["# " + data["title"][lang], "", f"{mode.title()} · RU/EN paired original condensation", ""]
        for s in data["screens"]:
            if s["level"] <= level:
                result += ["## " + s["copy"][lang]["title"], ""]
                result += [html.unescape(p) + "\n" for p in re.findall(r"<p>(.*?)</p>", s["copy"][lang]["body"])]
        (ROOT / "routes" / f"{mode}.{lang}.md").write_text("\n".join(result).rstrip() + "\n")

print(json.dumps({"targetModes": data["targetModes"], "draftUnits": unit_count,
                  "paragraphsPerLanguage": unit_count * 2, "sourceCount": len(data["sources"])}, indent=2))
