from pathlib import Path
import json
H=Path(__file__).resolve().parent.parent
replacements={
 'ru':[
  ('Это проверка предложенной философии на повседневном поведении, а не новое универсальное расписание, придуманное поверх книги.','Это проверка предложенной философии на повседневном поведении.'),
  (' Раздел нельзя честно превратить ни в современное руководство по сексуальному здоровью, ни в утверждение, что стоики вообще отвергали близость.',''),
  (' Сохранить авторский тезис важно; превратить его в установленный вывод о ненужности защиты от дискриминации было бы уже другим утверждением.',''),
  ('Это существенная часть его защиты стоицизма, а не случайная реплика, которую можно убрать без потери аргумента. Но книга здесь опирается преимущественно на вторичные полемические источники: пересказ не превращает их в современную проверку лечения или доказательство превосходства стоицизма над профессиональной помощью.','В этой полемике Ирвин опирается преимущественно на вторичные источники. Их изложение не является современной проверкой лечения или доказательством превосходства стоицизма над профессиональной помощью.'),
  ('Сохранить его значение — значит понять, что автор защищает возможность пересборки, не приписывая древним знание эволюции.','Автор защищает возможность пересборки, не приписывая древним знание эволюции.'),
  (' Это пересказ рассказанного им обмена, а не дополнительный придуманный разговор.','')
 ],
 'en':[
  ('This tests the proposed philosophy in everyday conduct, rather than supplying a new universal timetable invented on top of the book.','This tests the proposed philosophy in everyday conduct.'),
  (' The section cannot honestly become either a modern sexual-health guide or a claim that the Stoics rejected intimacy altogether.',''),
  (" Retaining the author's thesis matters; turning it into an established finding that protection from discrimination is unnecessary would make another claim.",''),
  ("This is a substantial part of his defense of Stoicism, rather than an incidental remark removable without loss to the argument. But the book relies here chiefly on secondary polemical sources: this account does not turn them into a current treatment review or proof of Stoicism's superiority to professional help.","In this polemic Irvine relies chiefly on secondary sources. Their discussion is not a present-day treatment review or evidence of Stoicism's superiority to professional care."),
  ('Preserving its meaning means recognizing that he defends the possibility of reconstruction without attributing knowledge of evolution to the ancients.','Irvine defends the possibility of reconstruction without attributing knowledge of evolution to the ancients.'),
  (' This paraphrases an exchange he reports, rather than adding an invented conversation.','')
 ]
}
for lang,pairs in replacements.items():
 p=H/f'draft.{lang}.md';s=p.read_text()
 for old,new in pairs:assert s.count(old)==1,(lang,old);s=s.replace(old,new)
 p.write_text(s)
config={'virtue-and-roman-emphasis':[10518,21000]}
(H/'root-review/primary-locator-repairs.json').write_text(json.dumps(config,indent=2)+'\n')
p=H/'map-coverage.py';s=p.read_text();needle="m['keyPrimaryPassagesForRoot']=keys"
assert s.count(needle)==1
replacement="""repair_file=D/'root-review/primary-locator-repairs.json'
if repair_file.exists():
 for k in keys:
  repaired=json.loads(repair_file.read_text()).get(k['label'])
  if repaired:k['characterRange']=repaired;k['locatorNote']='Expanded after actual root reading to include both Greek virtue and Roman tranquility emphasis.'
m['keyPrimaryPassagesForRoot']=keys"""
p.write_text(s.replace(needle,replacement))
print('Repaired six paired prose fragments and one primary locator; acceptance remains pending.')
