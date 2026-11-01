from pathlib import Path
import json,re,html

H=Path(__file__).resolve().parent.parent
data=json.loads((H/'story-data.json').read_text())
replacement={
 'ru': 'В авторской рабочей модели сильный стресс меняет работу медиаторных систем, но одновременно запускает восстановление. Истощение запасов норадреналина в мозге сопровождается усилением его синтеза. Глюкокортикоиды участвуют и в регуляции выработки транспортера серотонина — белка, возвращающего медиатор из синапса. Разные варианты соответствующего гена, предполагалось, по-разному отвечают на этот сигнал. Так пережитое событие, гормональная реакция и наследственность соединялись в объяснение того, почему одни люди восстанавливаются, а у других нарушение закрепляется. Гены в этой гипотезе задавали уязвимость, а не неизбежную судьбу.',
 'en': "In Sapolsky's proposed working model, severe stress changes transmitter systems but also initiates recovery. Depletion of brain norepinephrine stores is accompanied by increased synthesis. Glucocorticoids also participate in regulating production of the serotonin transporter, the protein returning the transmitter from the synapse. Different variants of the corresponding gene were proposed to respond differently to this signal. Experience, hormonal responses, and inheritance thus entered an explanation for why some people recover while dysfunction persists in others. Genes in this hypothesis conferred vulnerability rather than inevitable fate."
}
for lang in ['ru','en']:
    file=H/f'draft-{lang}.md';text=file.read_text()
    body=next(s for s in data['screens'] if s['id']=='unit-076')['copy'][lang]['body']
    old=html.unescape(re.findall(r'<p>(.*?)</p>',body,re.S)[0])
    assert text.count(old)==1,(lang,'gene paragraph')
    text=text.replace(old,replacement[lang])
    old,new={
      'ru':('Самозаражение Маршалла вызвало гастрит; это не следует пересказывать как создание им у себя доказанной язвы.','После самозаражения у Маршалла развился гастрит, а не подтверждённая язва.'),
      'en':("Marshall's self-infection produced gastritis; it should not be retold as his creating a confirmed ulcer in himself.","Marshall's self-infection produced gastritis, rather than a confirmed ulcer.")
    }[lang]
    assert text.count(old)==1,(lang,'gastritis sentence')
    file.write_text(text.replace(old,new))
print('Restored the historical recovery mechanism in unit-076 and removed the editorial instruction in unit-022, RU/EN. Rebuild and personal rereading still required.')
