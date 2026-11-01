from pathlib import Path
import json, shutil

H = Path(__file__).resolve().parent.parent
R = H / 'root-review'
for name in ['write-map.py', 'review-package.mjs', 'chapter-scene-map.md', 'sources.md', 'QA.md']:
    dest = R / ('input-' + name)
    if not dest.exists():
        shutil.copyfile(H / name, dest)

def edit(name, before, after):
    p = H / name
    s = p.read_text()
    assert s.count(before) == 1, (name, before[:70])
    p.write_text(s.replace(before, after))

def chapter(lang, index, replacement):
    p = H / ('draft-' + lang + '.md')
    parts = p.read_text().split('\n## ')
    heading, old = parts[index + 1].split('\n\n', 1)
    first = old.strip().split('\n\n')[0]
    parts[index + 1] = heading + '\n\n' + first + '\n\n' + replacement.strip() + '\n'
    p.write_text('\n## '.join(parts))

chapter('ru', 16, '''Следом шли новые схватки. Однажды в загон по очереди впустили трёх собак, в другой раз — пойманного взрослого волка. Потом против Белого Клыка выставили сразу двух псов. Он убил обоих, но и сам едва остался жив. Осенью, с первым снегом и льдом на реке, Смит увёз его пароходом в Доусон. Клетка стояла на палубе; пассажиры смотрели, совали палки, смеялись. В городе за показ «Бойцового Волка» брали золотым песком. Стоило ему улечься, как острая палка снова поднимала его на ноги: зрителям полагалось получить зрелище за свои деньги.

Для боёв его теперь выводили в лес за несколько миль от Доусона. Обычно уходили ночью, подальше от конной полиции, и ждали до рассвета, когда собирались зрители и приводили противника. Обычная собака ещё щетинилась и рычала, когда он уже успевал ударить; люди научились удерживать его до настоящего начала схватки. Равных ему находилось всё меньше. Стали привозить пойманных волков, а однажды — взрослую рысь. Она была такой же быстрой и, кроме зубов, пускала в ход когти. Он выжил и после неё. Но победа опять возвращала его в клетку. Когда Смит, избив его, уходил, вслед ему ещё долго неслось рычание. Последнего звука отнять у Белого Клыка он не мог.

После рыси бои прекратились совсем: больше не находилось животных, которых считали достойными противниками. До весны Белый Клык оставался выставочным зверем за решёткой. Затем приехал игрок Тим Кинэн и привёз первого в Клондайке бульдога — Чероки. Вокруг будущего боя целую неделю шли разговоры. Белый Клык ничего о них не знал. Когда цепь сняли в очередной раз, перед ним стоял низенький незнакомый пёс.''')
chapter('en', 16, '''More contests followed. One day three dogs were sent into the pen in succession; another day it was a newly captured adult wolf. Then they set two dogs against White Fang together. He killed both, but almost died himself. In autumn, with the first snow and drifting ice on the river, Smith took him by steamer to Dawson. His cage stood on deck; passengers watched, poked sticks and laughed. In town they paid gold dust to see the Fighting Wolf. Whenever he lay down, a sharp stick brought him to his feet again: the spectators must get a performance for their money.

For fights they now led him into the woods several miles outside Dawson. Usually they left at night, out of the mounted police's way, and waited until daylight brought the audience and an opponent. An ordinary dog would still be bristling and growling when he had already struck; men learned to hold him until the contest actually began. Equals became harder to find. They brought captured wolves, and once an adult female lynx. She was as quick as he was and used her claws as well as teeth. He survived her too. But victory returned him to the cage again. When Smith withdrew after beating him, a growl followed long after. He could not take that final sound from White Fang.

After the lynx, fighting stopped altogether: no animal considered a worthy opponent could be found. Until spring White Fang remained an exhibit behind bars. Then the gambler Tim Keenan arrived with Cherokee, the first bulldog in the Klondike. For a week the coming match was the subject of conversation. White Fang knew nothing of it. When the chain was removed once more, a short unfamiliar dog stood before him.''')
edit('draft-ru.md', 'Резкое слово и удар Скотта заставили терпеть прикосновения', 'Резкое слово и лёгкий шлепок Скотта заставили терпеть прикосновения')
edit('draft-en.md', "Scott's sharp word and cuff compelled him", "Scott's sharp word and light cuff compelled him")
edit('draft-ru.md', 'тыкать носом к убитым птицам и бить.', 'тыкать носом к убитым птицам и шлёпать.')
edit('draft-ru.md', 'Скотт включил свет, спустился с отцом и узнал Джима Холла. Тот был мёртв.', 'Скотт включил свет и спустился с отцом. Судья узнал Джима Холла. Тот был мёртв.')
edit('draft-en.md', 'Scott switched on the light, descended with his father and recognised Jim Hall. He was dead.', 'Scott switched on the light and descended with his father. The judge identified Jim Hall, who lay dead.')
edit('assemble.py', "('i-3',832,1214,[1,2,3,2,2,1]", "('i-3',832,1214,[1,2,3,1,1,1]")
edit('assemble.py', "('iv-3',4799,4975,[1,3,1],['За дверью — противник','Победа до утра','Низенький пёс'],['An opponent beyond the door','Victory until morning','The short dog'])", "('iv-3',4799,4975,[1,1,3,1],['За дверью — противник','Осенний пароход','Ночью за город','Низенький пёс'],['An opponent beyond the door','The autumn steamer','Into the woods at night','The short dog'])")
edit('assemble.py', "if key=='iv-3' and j==3:", "if key=='iv-3' and j==4:")
edit('review-package.mjs', 'ps.length===85', 'ps.length===86')
edit('review-package.mjs', "r.at(-2).id==='iv-3-p3'", "r.at(-2).id==='iv-3-p4'")
edit('review-package.mjs', "shortRouteStop:'iv-3-p3'", "shortRouteStop:'iv-3-p4'")

ledger = json.loads((R / 'reading-ledger.json').read_text())
old = json.loads((R / 'input-story-data.json').read_text())
ledger['originalDeepReadPairIds'] = [s['id'] for s in old['screens']]
ledger['deepReadPairIds'] = []
ledger['originalAll88PairsRead'] = True
ledger['allCurrentPairsRead'] = False
ledger['primaryRangesActuallyRead'] = [[832,1214],[1780,1843],[2400,2592],[3416,3589],[4799,5850],[5940,6148],[6380,6621],[6700,7519]]
ledger['readEvidenceNote'] = 'Root read all original88 RU/EN pairs and the complete map/Sources. Changed final pairs and shorter final routes require fresh reading. Primary ranges are selected direct reading, not complete continuous novel reading by root.'
(R / 'reading-ledger.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
print('Root repairs applied; no acceptance granted.')
