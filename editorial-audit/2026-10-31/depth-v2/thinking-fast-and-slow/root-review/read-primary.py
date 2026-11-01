"""Read the owned book in memory; P means nonempty extracted line in one spine file."""
from pathlib import Path
from html.parser import HTMLParser
import unicodedata, re, sys
class Text(HTMLParser):
    def __init__(self): super().__init__(); self.out=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in ['head','script','style']: self.skip+=1
        if t in ['p','h1','h2','h3','h4','div','li','br'] and not self.skip: self.out.append('\n')
    def handle_endtag(self,t):
        if t in ['head','script','style']: self.skip-=1
        if t in ['p','h1','h2','h3','h4','li'] and not self.skip: self.out.append('\n')
    def handle_data(self,d):
        if not self.skip: self.out.append(d)
base=Path('/Users/pn/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents')
book=next(f for f in base.iterdir() if unicodedata.normalize('NFC',f.name)=='Думай медленно Решай быстро 1.epub')
def lines(n):
    parser=Text();parser.feed((book/f'content{n}.html').read_text())
    return [re.sub(r'\s+',' ',x).strip() for x in ''.join(parser.out).splitlines() if x.strip()]
if __name__=='__main__':
    n=int(sys.argv[1]);rows=lines(n)
    if len(sys.argv)==2: print(f'content{n}.html: {len(rows)} extracted nonempty lines; {sum(len(s) for s in rows)} chars')
    else:
        a,b=map(int,sys.argv[2:4]);print(f'content{n}.html; P{a:03d}–P{min(b,len(rows)):03d}; electronic extraction, not printed pages')
        for i in range(a-1,min(b,len(rows))): print(f'P{i+1:03d}: {rows[i]}')
