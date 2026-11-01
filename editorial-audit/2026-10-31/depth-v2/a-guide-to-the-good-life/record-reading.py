from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
P=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-10-private/a-guide-to-the-good-life-source')
hash=lambda b:hashlib.sha256(b).hexdigest()
files=[]
main=[8,10,11,12,14,15,16,17,18,20,21,22,23,24,25,26,27,28,29,30,32,33,34,35]
notes=[85]+list(range(329,342))
for f in sorted(P.glob('*.txt')):
 raw=f.read_bytes();text=raw.decode();num=int(f.name[:3]) if f.name[:3].isdigit() else None
 role='extraction-index' if num is None else 'main-text' if num in main else 'endnote' if 36<=num<=354 else 'index' if num==356 else 'bibliography' if num==355 else 'front-matter'
 scope='read-complete' if num in main or num in notes or num in [3,5] else 'structure-consulted-first-36-lines' if num is None else 'hashed-only-not-substantively-read'
 files.append(dict(file=f.name,sha256=hash(raw),bytes=len(raw),characters=len(text),lines=len(text.splitlines()),role=role,readingStatus=scope))
(D/'source-hashes.json').write_text(json.dumps(dict(privateSourceDirectory=str(P),hashAlgorithm='SHA-256 on raw UTF-8 bytes',fileCount=len(files),totalCharacters=sum(f['characters'] for f in files),files=files),ensure_ascii=False,indent=2)+'\n')
events=[json.loads(x) for x in (D/'reading-dispatch.jsonl').read_text().splitlines()]
reading=[]
for n in main:
 f=next(P.glob(f'{n:03d}-*.txt'));s=f.read_text();ev=[e for e in events if e['file']==f.name];end=0
 for e in ev:assert e['start']==end;end=e['end']
 assert end==len(s),(f.name,end,len(s))
 reading.append(dict(file=f.name,sha256=hash(f.read_bytes()),characterRanges=[[e['start'],e['end']] for e in ev],displayedAtUtc=[e['displayedAtUtc'] for e in ev],actuallyReadAllDisplayedRanges=True,scope='continuous complete introduction/chapter/reading program',chapter='Introduction' if n==8 else 'Reading program' if n==35 else main.index(n)))
ru=Path('/Users/pn/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/Радость жизни.epub')
additional=[]
for rel in ['OEBPS/info.xhtml','OEBPS/pre.xhtml']:
 f=ru/rel;raw=f.read_bytes();additional.append(dict(privateEdition=str(ru),file=rel,sha256=hash(raw),byteRange=[0,len(raw)],scope='complete HTML text read via HTMLParser; not the rest of the translation'))
en=Path('/Users/pn/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents/A Guide to the Good Life The Ancient Art of Stoic Joy.epub')
raw=(en/'content.opf').read_bytes();additional.append(dict(privateEdition=str(en),file='content.opf',sha256=hash(raw),scope='metadata title/creator/date/identifiers/publisher and spine count inspected',spineEntries=357))
report=dict(schemaVersion=1,atUtc=datetime.datetime.now(datetime.timezone.utc).isoformat(),slug='a-guide-to-the-good-life',
 rangeConvention='Unicode-character offsets; 0-based half-open unless explicitly byteRange. Not print pages.',
 mainTextReadCompletelyInNumericSpineOrder=True,completeRussianTranslationCollation=False,allNotesOrIndexRead=False,rawExtractsCopiedIntoCandidate=False,
 fullMainTextFiles=reading,mainTextCharacters=sum(next(x for x in files if x['file']==r['file'])['characters'] for r in reading),
 consultedEndnotes=[dict(file=next(P.glob(f'{n:03d}-*.txt')).name,sha256=hash(next(P.glob(f'{n:03d}-*.txt')).read_bytes()),characterRange=[0,len(next(P.glob(f'{n:03d}-*.txt')).read_text())]) for n in notes],
 additionalPrimary=additional,frontMatterRead=['003-part0002.txt','005-part0004.txt'],
 limitations=['All 357 extracted text entries plus INDEX.txt were inventoried and hashed; hashing is not reading.','319 part0035_split entries are endnotes, not substantive chapters; 356-part0037.txt is the index.','Selected endnotes establish the book’s citation path, not independent reading or validation of the works cited.','Raw private sources remain outside the candidate.','No web acquisition or contemporary medical-efficacy review was conducted.','Authoring/route review by the implementer is not root personal acceptance.'])
(D/'reading-ledger.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['mainTextCharacters','mainTextReadCompletelyInNumericSpineOrder']}),len(files))
