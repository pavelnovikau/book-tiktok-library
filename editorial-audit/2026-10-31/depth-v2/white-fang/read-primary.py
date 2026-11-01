from pathlib import Path
import hashlib,sys,json,datetime
here=Path(__file__).resolve().parent
src=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/white-fang/primary.txt')
b=src.read_bytes();sha=hashlib.sha256(b).hexdigest()
assert sha=='3c7226d00fd9b169f0016635d0e461501620f343220ee18db7ca9f083f4ad3f4'
lines=b.splitlines(keepends=True); a,z=map(int,sys.argv[1:3]); chunk=b''.join(lines[a-1:z])
assert 1<=a<=z<=len(lines);assert len(chunk)<=47000
record={'sourceSha256':sha,'startLine':a,'endLine':z,'rangeSha256':hashlib.sha256(chunk).hexdigest(),'bytes':len(chunk),'presentedAtUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'activity':'complete source range presented for direct reading; no indexing or download counted'}
with (here/'reading-ranges.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
print(json.dumps(record));print(chunk.decode())
