from pathlib import Path
import shutil
H=Path(__file__).resolve().parent.parent
R=H/'root-review'
for name in ['qa/content-verification.json','qa/structural-audit.json','verify.mjs']:
    q=R/('input-'+name.replace('/','-'))
    if not q.exists():shutil.copyfile(H/name,q)
changes={
 'ru':[
  ('агуары, красные волки романа,','агуары, красные волки,'),
  ('Паганель нашёл нарду, из которого в романе делают грубую муку и хлеб.','Паганель нашёл нарду; из него приготовили грубую муку и хлеб.'),
  (' Доказательства самого захвата у них ещё не было.',''),
  ('Он надеялся, что одиночество и раскаяние ещё переменят этого человека, но доказать будущее не мог.','Он надеялся, что размышления и раскаяние ещё переменят этого человека.'),
  ('После разговора с невестой свадьбу сыграли','После короткого разговора майора с невестой свадьбу сыграли')],
 'en':[
  ("Aguaras, the novel's red wolves,",'Aguaras, red wolves,'),
  ('Paganel found nardoo, used in the novel to make rough flour and bread.','Paganel found nardoo; they made coarse flour and bread from it.'),
  (' They still had no evidence of the capture itself.',''),
  ('He hoped solitude and repentance might yet change the man, but could not prove the future.','He hoped reflection and repentance might yet change the man.'),
  ('After a conversation with the bride, the wedding took place','After a brief conversation between the major and the bride, the wedding took place')]
}
for lang, edits in changes.items():
    p=H/f'draft-{lang}.md';s=p.read_text()
    for before,after in edits:
        assert s.count(before)==1,(lang,before)
        s=s.replace(before,after)
    p.write_text(s)
print('Four paired paragraphs repaired; acceptance remains pending.')
