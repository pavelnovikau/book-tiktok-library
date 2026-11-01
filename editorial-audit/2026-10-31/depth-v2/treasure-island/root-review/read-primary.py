from pathlib import Path
import sys
p=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/treasure-island/primary.txt')
lines=p.read_text().splitlines();start,end=map(int,sys.argv[1:3])
for i in range(start-1,min(end,len(lines))):print(f"L{i+1}: {lines[i]}")
