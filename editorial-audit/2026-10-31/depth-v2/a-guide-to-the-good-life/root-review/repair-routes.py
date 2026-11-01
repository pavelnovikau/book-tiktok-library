from pathlib import Path
H=Path(__file__).resolve().parent.parent
changes={
 'ru':[
  ('У Сенеки и Музония Ирвин встретил','У Сенеки и Музония Руфа Ирвин встретил'),
  ('Музоний идёт дальше и предлагает добровольно','Стоик Музоний Руф идёт дальше и предлагает добровольно'),
  ('Для Марка человек разумен и общественен','Для Марка Аврелия человек разумен и общественен'),
  ('### Ответ без ответного унижения','### Юмор или молчание в ответ'),
  ('Игнорирование способно лишить обидчика награды — видимого смятения.','Игнорирование способно лишить обидчика награды — видимого смятения. По Ирвину, насмешка и показное равнодушие могут уязвить обидчика сильнее прямой ответной брани.')
 ],
 'en':[
  ('In Seneca and Musonius, Irvine instead found','In Seneca and Musonius Rufus, Irvine instead found'),
  ('Musonius goes further, proposing the voluntary','The Stoic Musonius Rufus goes further, proposing the voluntary'),
  ('For Marcus, humans are rational and social','For Marcus Aurelius, humans are rational and social'),
  ('### A response without a counterinsult','### Replying with humor or silence'),
  ('Ignoring an affront can deprive the offender of a reward: visible distress.',"Ignoring an affront can deprive the offender of a reward: visible distress. In Irvine's account, humor and conspicuous indifference can wound the offender more than a direct counterinsult.")
 ]
}
for lang,pairs in changes.items():
 p=H/f'draft.{lang}.md';s=p.read_text()
 for a,b in pairs:assert s.count(a)==1,(lang,a);s=s.replace(a,b)
 p.write_text(s)
print('Three first-use names clarified; humor/nonresponse indirect sting restored from the actual primary passage. Counts remain derived.')
