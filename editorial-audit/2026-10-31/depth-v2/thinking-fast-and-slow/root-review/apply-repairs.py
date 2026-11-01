# coding: utf-8
from pathlib import Path
import json, re, shutil

base=Path(__file__).resolve().parent.parent
review=base/'root-review'
original=json.loads((review/'input-story-data.json').read_text())
additions=json.loads((review/'additions.json').read_text())
for name in ['sources.md','QA.md','coverage-map.json','browser-check.mjs','qa/metrics-and-integrity.json']:
    target=review/('input-'+name.replace('/','-'))
    if not target.exists(): shutil.copyfile(base/name,target)

def change(text,before,after,label):
    assert text.count(before)==1,(label,text.count(before))
    return text.replace(before,after)

# These paragraphs were composed as connected RU/EN prose before segmentation.
for lang in ['ru','en']:
    path=base/f'draft.{lang}.md'
    text=path.read_text()
    for item in additions:
        title=next(s for s in original['screens'] if s['id']==item['after'])['copy'][lang]['title']
        pattern=r'^### '+re.escape(title)+r'\n[\s\S]*?(?=^### |^## |\Z)'
        matches=list(re.finditer(pattern,text,re.M));assert len(matches)==1,item['id']
        block='### '+item[lang]['title']+'\n\n'+'\n\n'.join(item[lang]['paras'])+'\n\n'
        end=matches[0].end();text=text[:end].rstrip()+'\n\n'+block+text[end:]
    if lang=='ru':
        text=change(text,'Рассуждение о WYSIATI объясняет, почему ответа иногда слишком много по сравнению с имеющимися знаниями. Другой механизм объясняет, откуда берётся его содержание.',
                    'Быстрое впечатление может казаться достаточным основанием для ответа. Но как именно возникает содержание этого ответа?', 'standalone shorter-mode bridge')
        text=change(text,'### Как соединить две информации','### Как соединить два вида сведений','natural RU title')
        text=change(text,'### Реальная процедура из книги','### Как устроить собеседование','reader-facing heading')
        text=change(text,'Но по книге продавцы называют в среднем 7,12 доллара,','Но книга приводит такие оценки: продавцы называют 7,12 доллара,','no unsupported statistic type')
        text=change(text,'В исследовании Канемана и Дона Редельмейера пациенты во время колоноскопии',
                    'В исследовании начала 1990-х годов Канемана и Дона Редельмейера пациенты во время колоноскопии','historical clinical context')
        text=change(text,'Делать отсюда рекомендацию продлевать болезненные процедуры нельзя: именно дополнительная боль создаёт противоречие, которое автор исследует.',
                    'В обсуждении медицинского примера сам автор различает две цели. Если нужно смягчить воспоминание, важны пик и постепенное ослабление боли в конце. Если нужно уменьшить суммарно прожитую боль, большую роль получает сокращение длительности, даже когда конец запомнится хуже. Канеман спрашивает, какой цели дать приоритет. Его предположение о том, что многие предпочтут лучшие воспоминания, не выдано за результат опроса. Конфликт двух оценок остаётся предметом вопроса, а не исчезает за готовым правилом.', 'restore author clinical dilemma')
    else:
        text=change(text,"WYSIATI helps explain why an answer sometimes exceeds the available knowledge. Another mechanism explains where its content comes from.",
                    "An immediate impression can seem sufficient to answer a question. But where does that answer's content come from?", 'standalone EN bridge')
        text=change(text,'### An actual procedure from the book','### Structuring an interview','reader-facing EN heading')
        text=change(text,'Yet the book reports average valuations of $7.12','Yet the book reports valuations of $7.12','no unsupported EN statistic type')
        text=change(text,"In Kahneman and Don Redelmeier's study, patients undergoing colonoscopy", "In Kahneman and Don Redelmeier's early-1990s study, patients undergoing colonoscopy", 'historical EN clinical context')
        text=change(text,'It cannot justify recommending longer painful procedures: the additional pain is precisely what creates the contradiction under investigation.',
                    'Discussing the medical example, the author distinguishes two objectives. To soften memory, the peak and a gradual reduction of pain at the end matter. To reduce accumulated experienced pain, shortening duration matters more, even if the ending is remembered less favorably. Kahneman asks which objective should take priority. His expectation that many would favor better memories is not presented as a survey result. The conflict between evaluations remains a question rather than disappearing behind a ready rule.', 'restore EN author dilemma')
    path.write_text(text)

path=base/'prepare-candidate.py';text=path.read_text()
text=change(text,'ru,en=parse(\'ru\'),parse(\'en\');assert len(ru)==len(en)==58',
            'ru,en=parse(\'ru\'),parse(\'en\');assert len(ru)==len(en)','derive authoring count')
text=change(text,'assert len(config)==58',
'''# Parent's source-checked additions follow their connected prose anchors.
additions=json.loads((P/'root-review/additions.json').read_text())
original_ids=[row[0] for row in config]
for item in additions:
 position=next(i for i,row in enumerate(config) if row[0]==item['after'])+1
 config.insert(position,(item['id'],item['level'],item['chapter'],item['files']))
assert [row[0] for row in config if row[0] in original_ids]==original_ids
assert len(config)==len(ru)==len(en)''','match expanded metadata and prose')
text=change(text,"sid=uid if gidx==0 else uid+'-continued';ids.append(sid)",
            "sid=uid if gidx==0 else uid+'-continued' if gidx==1 else uid+'-continued-'+str(gidx+1);ids.append(sid)", 'unique natural paragraph groups')
text=text.replace('не перенесён в пилот как','не перенесён в это изложение как')
text=text.replace('not carried over as a universal contemporary rule','not carried over as a universal contemporary rule')
path.write_text(text)
print(json.dumps({'newConnectedUnits':len(additions),'oldUnitOrderPreserved':True,'rootSourceChecksRequiredForAllNewUnits':True}))
