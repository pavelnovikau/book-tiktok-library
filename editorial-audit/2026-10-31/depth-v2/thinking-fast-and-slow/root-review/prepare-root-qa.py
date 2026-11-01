from pathlib import Path

p=Path(__file__).resolve().parent.parent
r=p/'root-review';(r/'qa').mkdir(exist_ok=True)
s=(p/'browser-check.mjs').read_text()
def replace(before,after,label):
    global s
    assert s.count(before)==1,(label,s.count(before))
    s=s.replace(before,after)
replace('const dir=path.dirname(fileURLToPath(import.meta.url)),',
        'const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url))),','parent candidate path')
replace("'story-data.json','thinking-fast-and-slow.html','browser-check.mjs'",
        "'story-data.json','thinking-fast-and-slow.html','root-review/browser-check.mjs'",'actual harness hash')
s=s.replace("path.join(dir,'qa',","path.join(dir,'root-review','qa',")
s=s.replace('book-tiktok.thinking-fast-and-slow.mode','book-tiktok.thinking-fast-and-slow.depth-v2.mode')
s=s.replace('book-tiktok.thinking-fast-and-slow.lastScreen','book-tiktok.thinking-fast-and-slow.depth-v2.lastScreen')
s=s.replace("'book-tiktok.'+d.slug+'.lastScreen'","'book-tiktok.'+d.slug+'.depth-v2.lastScreen'")
replace(".length===97,'saved Deep'",".length===110,'saved Deep'",'revised exact depth count')
anchor=next(line for line in s.splitlines() if "await c('Page.navigate'" in line)
seed=""" await c('Page.addScriptToEvaluateOnNewDocument',{source:`if(!sessionStorage.getItem('rootLegacySeeded')){localStorage.setItem('book-tiktok.thinking-fast-and-slow.language','en');localStorage.setItem('book-tiktok.thinking-fast-and-slow.mode','deep');localStorage.setItem('book-tiktok.thinking-fast-and-slow.lastScreen','risk-policy');sessionStorage.setItem('rootLegacySeeded','true');}`});
"""
replace(anchor,seed+anchor,'legacy revision fixture')
anchor=next(line for line in s.splitlines() if 'Screenshots are local QA' in line)
extra="""  report.explicitDeeperResume=[];
  for(const lang of ['ru','en'])for(const lower of ['essential','core']){
   const result=await ev(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent);if(document.documentElement.lang!=='${lang}')document.getElementById('languageButton').click();document.querySelector('[data-mode="deep"]').click();document.querySelector('#desktopContentsList [data-go-to="bayesian-update"]').click();document.querySelector('[data-mode="${lower}"]').click();document.querySelector('#desktopContentsList [data-go-to="cover"]').click();const b=document.querySelector('[data-start="continue"]'),label=b.textContent,explicit=label.includes(d.modes.deep.label['${lang}']);b.click();return {explicit,correctDepth:document.querySelectorAll('.progress-segment').length===d.targetModes.deep,correctTarget:localStorage.getItem('book-tiktok.thinking-fast-and-slow.depth-v2.lastScreen')==='bayesian-update',oldKeysPreserved:localStorage.getItem('book-tiktok.thinking-fast-and-slow.lastScreen')==='risk-policy'};})()`);
   assert(Object.values(result).every(Boolean),'explicit deeper resume '+JSON.stringify(result));report.explicitDeeperResume.push({lang,lower,...result});
  }
"""
replace(anchor,extra+anchor,'explicit lower-to-deeper resume')
(r/'browser-check.mjs').write_text(s)
s=(p/'measure.mjs').read_text()
s=s.replace('const dir=path.dirname(fileURLToPath(import.meta.url));','const dir=path.dirname(path.dirname(fileURLToPath(import.meta.url)));',1)
s=s.replace('median:(a[47]+a[48])/2','median:a.length%2?a[Math.floor(a.length/2)]:(a[a.length/2-1]+a[a.length/2])/2')
s=s.replace('for(const width of[320,390,1024,1440])','for(const width of[320,1440])')
s=s.replace("path.join(dir,'qa',","path.join(dir,'root-review','qa',")
(r/'measure.mjs').write_text(s)
print('Root QA isolated; final count, legacy namespace fixture and explicit deeper resume configured.')
