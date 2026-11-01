from pathlib import Path
import json
P=Path(__file__).parent
d=json.loads((P/'story-data.json').read_text()); scenes=json.loads((P/'scene-map.json').read_text()); chapters=json.loads((P/'witness-chapter-ranges.json').read_text())
s='# Chapter and scene map\n\nWorking review document: contains full-story spoilers. Every narrative paragraph was written in the connected RU draft, translated as a matching EN paragraph, then assigned a scene ID. Horne locators identify parts/chapters and 1-based physical lines in the exact hashed witness, never printed pages.\n\n'
s+='Essential: cover + narrative paragraphs 1–24 + final (26 screens). A continuous opening ending after Robert’s rescue, the Portuguese misunderstanding and the introduction of Thalcave/Thaouka. Captain Grant is still missing.\n\nCore: cover + paragraphs 1–67 + final (69 screens). The continuous opening through the South American journey and the Australian journey to the Snowy camp, before exposure. It stops honestly with an unresolved search.\n\nDeep: cover + all 113 narrative paragraphs + an inline late-story warning before paragraph 68 + final (116 screens). The three-part journey, betrayal, New Zealand, wrong order, real reunion/message solution, Ayrton disposition and homecoming are retained. Entry to Deep always requires session consent, including saved IDs.\n\n'
s+='| Draft paragraph | Scene ID | Level | RU / EN title | Primary locator |\n|---|---|---:|---|---|\n'
for m in scenes:
 s+=f"| {m['paragraph']} | `{m['id']}` | {m['level']} | {m['title']['ru']} / {m['title']['en']} | Horne {', '.join(m['chapters'])}; L{m['startLine']}–{m['endLine']} |\n"
s+='\nThese source ranges are review locators, not claims that every word of every mapped chapter survives in the condensation. All chapters were actually read; editorial retention and primary reading are separate. See edition-omission-map.md.\n'
(P/'chapter-scene-map.md').write_text(s)
notes={
'1.1':'Retains capture, bottle and damaged papers. Omits most shark anatomy, tail-cutting detail and general claims about shark behavior.',
'1.2':'Retains three copies, lost longitude, latitude and confident Patagonia conjecture. Omits repeated full reconstructions; guessed date is not made a wreck fact.',
'1.3':'Retains arrival, children’s ages and Mary wanting handwriting; condenses repeated questions.',
'1.4':'Retains Mary’s care, Grant’s colony plan, refusal, children’s proposals and Helena’s offer. Compresses Scottish party politics.',
'1.5':'Retains preparation, Robert’s service, Mangles, major and cathedral. Omits ship dimensions and most machinery/provision totals.',
'1.6':'Retains Mary’s nautical familiarity, Robert aloft, telescope fall and wrong names. Shortens the scholar’s titles.',
'1.7':'Retains ship identification, failed route-change request and purpose of search. Omits the detailed Tibetan scientific commission.',
'1.8':'Retains successive landing excuses, rain and voluntary decision to stay. Omits wine statistics and secondary expedition names.',
'1.9':'Retains maps/language study, growing attachment, straits and Southern Cross. Omits the long Patagonian-height dispute and detailed historical geography.',
'1.10':'Retains failed coast search, river-bottle hypothesis, land/sea split and farewells. Omits hypothetical military rescue logistics.',
'1.11':'Retains mule caravan, ponchos, Robert, naming rivers and armchair joke. Omits lengthy food/tack/travel custom explanations.',
'1.12':'Retains blocked Antuco, dismissal of guide, ascent, exhaustion and hut. Omits precise altitude/physiology calculations.',
'1.13':'Retains volcano/fuel, guanaco rush, failed supper, foreboding and earthquake descent. Food explanation remains Paganel’s claim.',
'1.14':'Retains repeated search, Glenarvan’s delay, condor and external shot/rescue. Omits anatomical size claims and exaggerated general zoology.',
'1.15':'Retains Thalcave, Portuguese discovery, language repair, supplies and recovery. Omits racial/physiognomic judgments.',
'1.16':'Retains Thaouka, route on sand and uncertain captive report. Omits extensive Pampas classifications and weather discussion.',
'1.17':'Retains drought, north-wind quarrel and dry Salinas. Condenses gaucho controversy without turning stereotypes into reference facts.',
'1.18':'Retains split, father’s soft voice/song, horse sensing water, enclosure and hunting. Omits most game taxonomy and exact distances.',
'1.19':'Retains night siege, ammunition/fire depletion, adult disagreement, Robert’s decoy ride and dawn reunion. No modern pack-behavior assertion.',
'1.20':'Retains refreshed party and empty region leading to Tandil. Omits flamingo/Chateaubriand experiment and rhetorical advice.',
'1.21':'Retains sergeant’s family comedy, war explanation and Guinnard false trail. Compresses his biography and individual children’s names.',
'1.22':'Retains delay, wet plain, horns, rain, flood and horse losses. Condenses repeated ground/weather stages.',
'1.23':'Retains ombu household, saved food/powder, lens and world-parallel question. Omits many birds, architectural measurements and supply calculations.',
'1.24':'Retains Australia reading, tree feast and Noah argument. Omits the embedded happy-man’s-shirt tale and racialized jaguar food ranking.',
'1.25':'Retains storm, fire, caimans, waterspout and drifting tree. Omits lightning statistics and weather-science assertions.',
'1.26':'Retains Thalcave reunion, coast vigil/sleeping Paganel, signals and farewell gifts/refusal. No promised future reunion.',
'2.1':'Retains family reunion, Mary/John, breakfast and major’s renewed map scrutiny. Compresses repeated expedition recap.',
'2.2':'Retains prepared cabin, writing and Tristan negative search. Omits demographic/racial hierarchy and precise island statistics.',
'2.3':'Retains coal, solitude disagreement, Viot and negative search. Uses Amsterdam group rather than silently resolving Horne’s island-name confusion.',
'2.4':'Retains tentative date revision and rifle/telescope wager with frog joke. Omits long navigator list.',
'2.5':'Retains barometer, screw failure, command conflict, sail struggle and oil/bar passage. Omits machinery/weather calculations; no seamanship instruction.',
'2.6':'Retains repair need, failed search, mill and OMoore hospitality. Omits narrator’s general guarantee that hard work produces settler success.',
'2.7':'Retains Ayrton’s conditional testimony, children’s memories, authentic papers and crossing proposal. Omits conflicting exact June dates.',
'2.8':'Retains John joins, wagon, Ayrton’s ship inspection and literal orders to Tom. Omits minute wagon measurements.',
'2.9':'Retains dinner statistics/comedy and Paganel’s regeneration claim as his claim. Omits long supposedly scientific catalogue.',
'2.10':'Retains stockkeeper, Christmas and Wimerra damage. Compresses herd totals, economics and long river-crossing procedure.',
'2.11':'Retains smith wrist marks, trefoil, Carisbrook and railway crime, including dead keeper. Compresses rescue statistics; no native guilt inferred.',
'2.12':'Retains Toline’s label, school/family, friendship, Bible prize, geography satire, corrective gift and unknown departure motive.',
'2.13':'Retains watchfulness, eucalyptus, Seymour gang warning and postponed ship order. Omits newspaper date corruption and long botanical explanation.',
'2.14':'Retains Mozart, Pattersons, hospitality and John saving Robert. Omits most station economics and banker-father improvement speech.',
'2.15':'Retains inn, Alps/hail, horse deaths, Snowy bog and luminous mushrooms. Compresses inconsistent day-by-day dates.',
'2.16':'Retains surviving branded horse, wagon/river problem and messenger debate. Major’s reasons are revealed in chronological reconstruction from his later account.',
'2.17':'Retains overheard plot, shot/exposure, Mary’s loss of hope, messenger lot and distracted writing. No premature revelation of actual wrong country.',
'2.18':'Retains wounded Mulrady, care, stolen letter, piracy scheme and burned bridge. Compresses repeated watch reports.',
'2.19':'Retains failed canoe, falling water, broken raft/lost stores, litter, hardship, Delegete and Eden telegram. Food is narrative, not survival guidance.',
'3.1':'Retains Mary/John pledge, Halley negotiation and last coast search. Omits minor bargaining repetitions.',
'3.2':'Retains slow crossing and Paganel’s preoccupation. Omits detailed Tasman voyage/history and ancient-continent reasoning.',
'3.3':'Retains drunken crew, John’s watch, no charts and takeover discussion. Omits most historical martyr narrative and repeated generalizations.',
'3.4':'Retains Glenarvan looking for Duncan, reef maneuvers, wreck, cargo panic and morning abandonment. Condenses repeated ship handling.',
'3.5':'Retains raft necessity and Paganel’s fears as his fears. Omits long purported biological/religious explanation of cannibalism and illustrative anecdotes.',
'3.6':'Retains raft delay, ruined empty yawl, anchor/night, severed cable and landing. Halley’s death remains inferred, not witnessed.',
'3.7':'Retains rain cave, land-seizure resistance and limits of current news. Omits exact historical troop/statistical claims and racial taxonomy.',
'3.8':'Retains scrub, Waipa, bird interest, fog camp and capture. Omits detailed kiwi/tui natural history and named route inventories.',
'3.9':'Retains captivity, upstream canoe, defeated warriors, exchange hope and Taupo. Omits tattoo classification and bodily hierarchy.',
'3.10':'Retains grief, sacred house, hidden revolver, exchange, KaraTete’s assault, Glenarvan’s shot, taboo and missing pair. No private motives invented.',
'3.11':'Retains expanded death sentence, priest dead, forced funeral witness, killings and tomb. Reduces graphic cannibalism detail; no ethnographic certification.',
'3.12':'Retains condemned night, major’s caution, scraping, hand recognition, Robert’s explanation, rope and interrupted escape. No invented shared escape with Paganel.',
'3.13':'Retains taboo refuge, Paganel’s partial account, tomb stores, failed ridge and hot ground. Omits Bible gunwad/Psalm consolation and full food catalogue.',
'3.14':'Retains vent plan, eruption greater than hoped, damage/deaths, retreating guards and night escape. No scientific feasibility claim.',
'3.15':'Retains arduous volcanic/kauri journey, uncertain moa sighting, Mary/John restraint, Lottin chase and Duncan mistaken for enemy. Omits naming a mountain after Glenarvan.',
'3.16':'Retains actual order, Tom’s literal execution, Ayrton locked up and Paganel gun mishap/undressing refusal. Selected French XVII cross-check.',
'3.17':'Retains refusal, authority limit, coal/return decision, Helena interviews and crew anger. Private conversation content remains unknown.',
'3.18':'Retains island bargain/limited knowledge, actual mutiny, prior landing, plot confession and third reading. No exact contradictory date copied.',
'3.19':'Retains island selection/lights, children’s future conversation, mistaken hallucination and dawn recognition. No pre-consent title leak.',
'3.20':'Retains reunion, engagement blessing, survival story, real cry, message solution/double island name and Ayrton disposition. Omits exact wreck date/longitude and recipe detail.',
'3.21':'Retains homecoming, marriage, Robert’s sea future, colonial ambition and Arabella/tattoo ending. No sequel fate imported.'}
a='# Edition and omission map\n\nFull-story spoilers. Main retained arc follows the Horne-edited 66-chapter witness. The original French work has 70 chapters; only four selective French checks are claimed. This table does not certify what the uncollated French-only material contains.\n\n'
a+='The final volume follows developed scenes, not a quota: the first part gives the rescue party time to form, lose Robert, live with Thalcave, lose its false trail and cross the flood; the second develops sea travel, farm trust, the wagon journey, Toline, music, horse losses, betrayal and the stolen order; the third retains the long wrong-ship escape, war/captivity, two rescues, the order’s cause, Ayrton’s limited knowledge, the children’s night and the full message/return. Rough planning range was 12–18k RU narrative words. Final exact counts are in metrics.json. It is a large condensation, not a substitute for every travel chapter or every argument in the original.\n\n'
a+='| Horne chapter | Actual witness range | Candidate paragraphs | Retention and real omissions |\n|---|---|---|---|\n'
count={}
for c in chapters:
 part=c['part'];count[part]=count.get(part,0)+1;code=f'{part}.{count[part]}'
 match=[str(m['paragraph']) for m in scenes if code in m['chapters']]
 assert match and code in notes
 a+=f"| {code} | L{c['startLine']}–{c['endLine']} | {', '.join(match)} | {notes[code]} |\n"
a+='\n## Sensitive mechanisms to compare directly\n\n- I.II: known latitude versus inferred country and date.\n- I.XIV–XVI: external shot, Robert alive, Thalcave and language failure.\n- I.XIX: adults dispute decoy sacrifice; Robert takes Thaouka, morning reunion.\n- I.XXI–XXVI: Guinnard, ombu/Australia reading before fire, farewell.\n- II.VII–VIII: authentic papers do not make the wreck testimony true; orders to Tom.\n- II.XII: Bible prize versus corrective Richardson gift and its abandonment.\n- II.XV–XVIII: trefoil, poison, Major’s overhearing, shot and stolen order.\n- III.X–XIV: Glenarvan fires; exchange collapses; Robert’s tunnel; Paganel’s refuge and vent.\n- III.XV–XVIII: mistaken pirate fear, original letter, imprisonment, limited confession.\n- III.XIX–XXI: night voice, three survivors, message names, marooning and tattoo comedy.\n\nAll primary ranges were read by the implementation writer. Root still must read both complete resulting languages and every route, compare this coverage, and directly check the mechanisms above on exact candidate hashes. No root review is claimed here.\n'
(P/'edition-omission-map.md').write_text(a)
# Short-route review copies; Deep is the complete connected draft, with an inline warning in the reader.
routes=P/'routes';routes.mkdir(exist_ok=True)
for lang in ('ru','en'):
 for mode,lv in [('essential',1),('core',2)]:
  body=f'# {d["title"][lang]} — {mode}\n\n'+('Незавершённый маршрут. Развязка здесь не раскрывается.\n\n' if lang=='ru' else 'An intentionally unfinished route. The ending is not revealed here.\n\n')
  for screen in d['screens']:
   if screen['level']<=lv and screen.get('draftParagraph'):
    cp=screen['copy'][lang];body+='## '+cp['title']+'\n\n'+cp['body'][3:-4]+'\n\n'
  (routes/f'{mode}-{lang}.md').write_text(body)
print('maps: 66 chapters, 113 scenes; 4 short-route review copies')
