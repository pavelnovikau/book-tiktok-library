from pathlib import Path

H=Path(__file__).resolve().parent.parent
changes={
 'ru':[
  ('Такой вывод не следует из описанных механизмов и исследований.','Из возможного влияния психики на течение болезни не следует ответственность больного за отсутствие исцеления.'),
  ('Крыса, привыкшая получать вещество нажатием рычага,','Крыса, привыкшая получать наркотическое вещество нажатием рычага,'),
  ('Роберт Эванс, Джон Линч и Джордж Каплан предлагают иной, материальный путь.','Роберт Эванс, Джон Линч и Джордж Каплан описывают, как распределение доходов может менять общественные услуги.')
 ],
 'en':[
  ('That conclusion does not follow from the mechanisms and studies described.',"Possible psychological effects on a disease's course do not make patients responsible for failure to recover."),
  ('A rat accustomed to obtaining a drug through lever pressing','A rat accustomed to obtaining an addictive drug through lever pressing'),
  ('Robert Evans, John Lynch, and George Kaplan propose another, material pathway.','Robert Evans, John Lynch, and George Kaplan describe a material pathway connecting income distribution to public services.')
 ]
}
for lang,items in changes.items():
 p=H/f'draft-{lang}.md';s=p.read_text()
 for a,b in items:
  assert s.count(a)==1,(lang,a)
  s=s.replace(a,b)
 p.write_text(s)
print('Clarified the cancer inference, addictive-drug referent and public-services opening in both languages; no route counts changed.')
