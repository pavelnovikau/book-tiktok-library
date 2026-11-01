"""Read private witness in bounded Unicode-character ranges; never copies text to disk.

Ranges are 0-based, half-open. A successful display is recorded as dispatched;
the finished reading ledger separately confirms actual reading, not mere inventory.
"""
from pathlib import Path
import sys, json, hashlib, datetime

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-10-private/a-guide-to-the-good-life-source')
number = int(sys.argv[1])
f = next(SOURCE.glob(f'{number:03d}-*.txt'))
raw = f.read_bytes()
s = raw.decode('utf-8')
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = min(int(sys.argv[3]), len(s)) if len(sys.argv) > 3 else len(s)
assert 0 <= start < end <= len(s)
assert end - start <= 35000, 'Use bounded chunks'
event = dict(file=f.name, sha256=hashlib.sha256(raw).hexdigest(), start=start, end=end,
             totalCharacters=len(s), rangeConvention='Unicode characters; 0-based half-open',
             displayedAtUtc=datetime.datetime.now(datetime.timezone.utc).isoformat())
print(json.dumps(event, ensure_ascii=False))
print(s[start:end])
with (HERE/'reading-dispatch.jsonl').open('a') as out:
    out.write(json.dumps(event, ensure_ascii=False)+'\n')
