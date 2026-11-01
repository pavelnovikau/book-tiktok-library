from pathlib import Path
p=Path(__file__).parent/'four-thousand-weeks.html';t=p.read_text()
def replace(old,new):
 global t
 assert t.count(old)==1,(old[:80],t.count(old));t=t.replace(old,new)
replace('const storagePrefix = `book-tiktok.${data.slug}.`;','const storagePrefix = data.progressNamespace;')
old="const primaryLabel = resumeHasEnding ? (state.language === 'ru' ? 'Продолжить Deep — спойлеры финала' : 'Continue Deep — ending spoilers') : remembered ? text().continuePrefix + copyOf(remembered).title + text().continueSuffix : text().start;"
new="""const resumeMode = remembered && remembered.level > levels[state.mode] ? requiredMode(remembered.level) : null;
        const primaryLabel = resumeMode
          ? (state.language === 'ru' ? 'Продолжить · ' : 'Continue in ') + modeLabel(resumeMode) + ': ' + copyOf(remembered).title
          : remembered ? text().continuePrefix + copyOf(remembered).title + text().continueSuffix : text().start;"""
replace(old,new)
replace("start: 'Начать просмотр'","start: 'Начать чтение'")
replace("coverTop: 'СИСТЕМА / ИДЕЯ / СЛЕДСТВИЕ', coverBottom: 'ОДНА МОДЕЛЬ, КОТОРУЮ СТОИТ УНЕСТИ'","coverTop: 'КОНЕЧНОСТЬ / ВЫБОР / ВРЕМЯ', coverBottom: 'ЖИЗНЬ БЕЗ ОБЕЩАНИЯ УСПЕТЬ ВСЁ'")
replace("coverTop: 'SYSTEM / IDEA / CONSEQUENCE', coverBottom: 'ONE MODEL TO CARRY FORWARD'","coverTop: 'FINITUDE / CHOICE / TIME', coverBottom: 'LIFE WITHOUT FINISHING EVERYTHING'")
replace('<div class="cover-line"><span class="cover-node">01</span><span class="cover-node">02</span><span class="cover-node">03</span><span class="cover-node is-focus">04</span><span class="cover-node">05</span><span class="cover-node">06</span><span class="cover-node">07</span></div>','<p class="hero-number">4000</p>')
p.write_text(t)
print('Local namespace, explicit deeper-resume label and book-specific typographic cover applied; installed shell unchanged.')
