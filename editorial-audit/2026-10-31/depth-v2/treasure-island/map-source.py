from pathlib import Path
import json,hashlib,re,datetime
here=Path(__file__).parent
src=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-1-private/treasure-island/primary.txt')
starts=[147,350,593,809,1016,1225,1465,1687,1894,2116,2318,2535,2748,2930,3124,3386,3569,3743,3925,4143,4360,4600,4808,4976,5174,5358,5640,5861,6151,6382,6642,6877,7106,7327,7513]
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV','XXV','XXVI','XXVII','XXVIII','XXIX','XXX','XXXI','XXXII','XXXIII','XXXIV']
beats='''Bones arrives, one-legged watcher/nightmares, inn tyranny, Livesey confronts knife
Black Dog confronts Bones, fight/notched sign, stroke/bloodletting and warning
Rum plea, Flint/chest disclosure, father dies, Pew coerces Jim, black spot/Bones dies
Neighbours refuse, mother insists on debt only, chest/foreign coins, packet, faint/bridge
Pew demands papers not money, warnings/quarrel, horse accident, revenue officers, Jim keeps packet
Library/pie, Bones ledger, treasure map and notes, expedition, warning about Trelawney
Delay/map dreams, revealing Bristol letter, mother/new helper, jealousy/farewell, port
Friendly Silver, Black Dog escapes, staged pursuit/Morgan, unpaid-score laughter, renewed trust
Smollett objections, map secrecy, arms/berths moved, Jim dislikes captain
Departure song, Arrow drinking/disappearance, Silver at sea, parrot tales, apple barrel
Silver recruits Dick, past/savings claims, Hands wants revolt, delay/murder plan, rum/land cry
Copied chart/no crosses, Silver friendly, report/council, seven reliable against nineteen
Gloomy island, towing/discipline failing, leave, shore parties 6/13, Jim impulsively runs
Exploration, overheard Tom refusal, Alan cry, crutch/knife murder, Jim flees
Wild Ben, cheese, marooning/Flint history, reward/passage, hints/boat, gun/flag
DOCTOR takes over; water problem, spring/fort reconnaissance, stores trips, Gray defects
DOCTOR overloaded boat/current, Trelawney misses Hands, swamping not direct hit, supplies lost
DOCTOR stockade race, Redruth death, flag/cannonade/short rations, Jim returns
JIM resumes; Ben will meet gentleman alone, white rock, camp/sand/smoke, cheese, truce flag
Silver offer and Smollett terms, unknown night attack, pipe scene, no help rising, rage
Posts abandoned except Gray, defence, rush, Jim falls/Gray kills Anderson, losses
Hunter death/Smollett recovery prospect, doctor leaves, Jim deserts, coracle, cable plan
Difficult boat, cable danger/slack, drunken quarrel/wrestle, cutting, tide to sea/sleep
Cliffs/sea lions via boy perception, balancing/paddling/thirst, erratic ship, leap/coracle lost
Two watchmen, O'Brien dead/Hands alive, wrecked cabin, water/food/flag, bargain/dressing
Dead/body-spirit conversation, secret dirk, shared pilotage, attack/wet priming, grounding/climb/involuntary shots
Hands shot/drowned, shallow wound release, O'Brien overboard, sails/escape, return/parrot/capture
Six pirates/no prisoners, Silver's account, Jim's boast not fact, Morgan threat, reciprocal bargain/map mystery
Bible black spot, rules/charges/rebuttal, chart wins command, Dick joke, Jim sympathy
Doctor treats pirates, parole, escape refused, ship location, warning/limited promise
Breakfast double bargain, rope/two boats, bearings, skeleton pointer/Allardyce guess
Ghost song/last words, echo argument, Ben dead-or-alive joke, Dick fever, empty old pit
Silver changes sides, hidden shots/Merry killed, Ben's prior work disclosed, rescue timing, cave/supper
Gold labour/coins, remaining men's appeal/shot, supplies/marooning, port/Silver escape, five return/shares/nightmare'''.splitlines()
omissions='''Repeated drinking incidents, extended physical description and much of song are shortened
Tattoo inventory and medical dialogue shortened; bloodletting retained as fictional period treatment
Full rum monologue and intervening household routine compressed
Detailed chest inventory and exact coin values shortened; debt-count delay retained
Individual fugitives and customs pursuit detail shortened
Ledger entries/coordinates and exact map bearings omitted, not replaced
Letter reproduced indirectly, Blandly purchase gossip and sexist speculation omitted
Most nautical teaching detail and several exchanges omitted
Full berth plan and arguments shortened
Most parrot geography and tall age claims only attributed to Silver; no factual validation
Savings sums and long rhetoric compressed; no savings lesson inferred
Formal deck toasts and manoeuvre commands condensed
Geography and navigation compressed; numbers retained
Botanical names condensed; broken back not asserted as certain
Ben's pious self-account compressed; no secret exposed early
Five journeys grouped around cargo/rescue sequence; no Jim omniscience
Exact heading typo resolved by title/order (witness prints XXVII here); no claim shell hit boat
Captain's harsh extra-mouth remark omitted, Redruth relational scene retained
Watch assignments and tactical arithmetic compressed
Night raid remains Jim's suspicion, not newly witnessed scene
No added duel choreography; Hunter later fate stays after boundary
No claim Jim's desertion was a sanctioned mission
Exact song lyrics and minute course changes compressed
No scientific guarantee about sea lions copied from narrator
Food list and vessel geometry shortened
One pistol reprimed/other reloaded, two involuntary discharges retained; no deliberate execution
Wound is skin pinch; no invented deep injury or bandage cure
Jim boasts beyond facts; no killing O'Brien assigned to Jim in narration
Full repetitive rebuttal compressed, comic Bible effect retained
Medical diagnosis/air theory remains doctor's belief, no contemporary clinical claim
Flint killing details are pirates' reconstruction, identity a guess
Superstitious echo argument stays weak in Jim's eyes, not proof of life
Detailed oar work and exact sea mileage shortened; relocation/rescue timing intact
Exact meal inventory and racialized port categories omitted; Silver's future not certified'''.splitlines()
assert len(beats)==len(omissions)==34
chapters=[{'chapter':roman[i],'logicalNumber':i+1,'sourceLines':[starts[i],starts[i+1]-1],'focalizer':'Livesey' if i+1 in (16,17,18) else 'Jim Hawkins','retained':beats[i],'compressedOrOmitted':omissions[i]} for i in range(34)]
obj={'work':'Robert Louis Stevenson, Treasure Island','sourceSha256':hashlib.sha256(src.read_bytes()).hexdigest(),'source':str(src),'chapters':chapters,'containsFullPlotSpoilers':True,'segmentationPending':True}
(here/'chapter-map.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
ranges=[(147,808),(809,1464),(1465,2115),(2116,2747),(2748,3385),(3386,3924),(3925,4599),(4600,5173),(5174,5860),(5861,6381),(6382,6876),(6877,7512)]
ledger={'schemaVersion':1,'work':obj['work'],'witness':{'path':str(src),'bytes':len(src.read_bytes()),'sha256':obj['sourceSha256'],'totalLines':7863,'novelNarrativeLines':[147,7512],'metadata':'Gutenberg #120; header says English, illustrator Louis Rhead, updated September 4 2026. Electronic witness, not certified collation with an 1883 printing.','headingAnomaly':'At L3569 header is XXVII, followed by The Jolly-boat’s Last Trip. Continuous order and contents identify logical XVII. Later XXVII is correct.'},'readBy':'implementation worker personally in this turn, no child readers','scope':'All narrative paragraphs in continuous source order, I–XXXIV including ending. Metadata/contents checked. License/footer not claimed as narrative reading.','method':'Twelve bounded sed outputs, each returned without truncation and read before drafting. File acquisition alone was not counted as reading.','readingLedger':[{'order':i+1,'lines':[a,b],'displayedAndRead':True,'nextStartsAt':b+1 if i<11 else None} for i,(a,b) in enumerate(ranges)],'coverageGaps':[],'limits':['Original RU/EN condensation; neither language is a certified published translation.','No print-edition variant collation, no historical geography or medical/scientific validation.','Full primary remains at supplied private path outside the public library repository.'],'criticalRechecks':{'BenJoke':{'chapter':'XXXII','lines':[6985,7018],'finding':'Recognition of Ben plus nobody minds Ben dead or alive restores courage. No proof of Ben being alive.'},'BenFear':{'chapter':'XXXIV','lines':[7373,7382],'finding':'Ben fears his old quartermaster; no revenge motive supplied.'},'SilverEscape':{'chapter':'XXXIV','lines':[7465,7473],'finding':'Ben connives at escape and claims life-saving reason; story attributes that reason to Ben.'},'Hands':{'chapter':'XXVI–XXVII','lines':[5575,5695],'finding':'One priming changed, other gun reloaded; thrown dirk, involuntary shots, shot/drowned, skin pinch release.'},'TreasureChronology':{'chapter':'XXXIII','lines':[7180,7250],'finding':'Ben moved treasure two months before arrival. Doctor learns after assault, bargains next morning after ship disappears; rescue follows discovering Jim captive.'}}}
(here/'source-coverage.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
