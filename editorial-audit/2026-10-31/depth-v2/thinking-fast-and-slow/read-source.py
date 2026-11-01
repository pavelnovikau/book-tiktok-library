"""Read selected owned-EPUB sections in memory only; never persist extracted text."""
import os,unicodedata,sys,re
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['head','script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','h4','div','li','br'] and not self.skip:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['head','script','style']:self.skip-=1
  if t in ['p','h1','h2','h3','h4','li'] and not self.skip:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
r='/Users/pn/Library/Mobile Documents/iCloud~com~apple~iBooks/Documents'
p=next(os.path.join(r,x) for x in os.listdir(r) if unicodedata.normalize('NFC',x)=='Думай медленно Решай быстро 1.epub')
for arg in sys.argv[1:]:
 bits=arg.split('@');i=int(bits[0]);q=Text();q.feed(open(f'{p}/content{i}.html').read());t=''.join(q.out);t=re.sub(r'\n\s*\n+','\n',t);
 if len(bits)>1:t=t[t.index(bits[1]):]
 if len(bits)>2:t=t[:t.index(bits[2])]
 print(f'\n=== content{i}.html; '+ ('full file' if len(bits)==1 else 'section '+bits[1])+ ' ===\n'+t)
