from pathlib import Path
import json,re,hashlib,datetime
b=Path(__file__).parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=Path('/Users/pn/smartcat/_artifacts/book-tiktok-editorial-audit-20261031/group-8-private/selfie-edition.json');p=json.loads(source.read_text());by={a['file']:a for a in p}
# The six endnotes actually displayed, not a claim to have read all endmatter.
notes=[45,111,113,131,141,223]
ledger=json.loads((b/'reading-ledger.json').read_text())
ledger['selectiveNotes']={'file':'OPS/ch2.xhtml','paragraphs':[{'paragraph':n,'sha256':hashlib.sha256(by['OPS/ch2.xhtml']['paragraphs'][n-1].encode()).hexdigest()} for n in notes],'displayedReadingAcknowledged':True,'scope':'Origins of Gazzaniga account; Vasco archival sources and tape; translation of song-title note; Austen Heinz reconstruction sources. Not full note reading.'}
ledger['completeMainSpineVerified']=True
main=[a for a in p if re.match(r'OPS/ch1-(?:[3-9]|1\d|2[01])\.xhtml$',a['file'])]
seen={(r['file'],r['p']) for c in ledger['chunks'] for r in c['paragraphHashes']}
assert all((a['file'],n) in seen for a in main for n in range(1,len(a['paragraphs'])+1))
assert len(ledger['chunks'])==30 and all(c['displayedReadingAcknowledged'] for c in ledger['chunks'])
ledger['mainSpineParagraphs']=sum(len(a['paragraphs']) for a in main)
ledger['mainSpineWordsReported']=sum(a['words'] for a in main)
ledger['notReadContinuously']=['OPS/ch2.xhtml except six listed paragraphs; image binaries unavailable']
(b/'reading-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
# Each file is represented, but read coverage is not a claim of exhaustive retelling.
omit={
3:'P020\u2013023 detailed epidemiology and drug-prescription discussion; P032/P044 detailed gender/appearance statistics; P049 numerical supporting surveys. Retain multifactor warning, OConnor entrapment, Flett no demonstrated increase, Meredith loop. No self-harm methods or romanticisation from P007\u2013018.',
4:'P030/P069\u2013085 individual weapons, injury and revenge details; P039\u2013040 sweeping species/racial generalisations; P055 numerical gossip proportions; P106 self-punishment detail. Keep gang recruitment, public humiliation, group-relative altruism, conversion as testimony and interpreter cases.',
5:'P003\u2013004 extended free-will/Sapolsky debate omitted; no universal consensus inferred. P008\u2013016 conversion limits retained, including later violence in bounded description.',
6:'P007\u2013011 detailed neural counts and hereditary percentages; P016 youth-memory example; P025\u2013028 catalogue of philosophers/contests condensed. P031 historical selectivity retained. Do not reproduce apparent chronology typo in P046.',
7:'P004 employment/family discrimination anecdote, detailed literary genealogy P008\u201315 and specific suicide examples P020\u201328 shortened or omitted. Retain Kim competing perspectives, collective pressure and urban-change qualifications; P031\u201334 inward transition.',
8:'P006\u2013010 atmospheric/ritual detail condensed; P014\u2013015 communion exchange omitted; P028 voice-frequency study and P046 shock experiment omitted; P047\u201350 health-correlation specifics condensed; P095\u201397 broad interreligious hierarchy not asserted. Martin/Pluscarden are developed, not merely named.',
9:'P008\u2013009 speculative intimate childhood reconstruction of Freud omitted. P010\u201319 Oedipus influence and risk of generalising from self retained as Storr\u2019s account, not direct causal diagnosis. P022\u201326 Perls visit condensed without invented dialogue.',
10:'P017 healer violence details, P030 nun counts, P043\u201344 individual group testimonies, P048 sexual display, P050 Natalie Wood assault, P052 celebrity/scandal roll call condensed/omitted. Retain Smiles/mind-cure contrast, Great Compression, Rogers compassion versus limitless theory, Shaw and Perls/Schutz methods and costs.',
11:'P017 explicit sexual questionnaire content omitted; retain stated willingness versus observed acts. P070 teenage restaurant rejection not fully developed; P110\u2013111 names, methods of deaths and Manson cameo omitted. No direct causal verdict on Esalen. Goat/role/shared-sketch arc, Hood and social-pain dispute retained.',
12:'P009\u2013012 luggage refusal and last insult condensed into ending of course; P016 detailed est expansion and P017 list of conference speakers condensed. P014\u201322 dissent/Marin/Wolfe/Vasco transition represented.',
13:'P009\u201311 full Atlas reception/affair detail condensed; P018 erroneous almost30-years arithmetic not repeated. P023 names/fitness statistics, P040 fringe sexual-policy interests and P041 imagined-artery episode omitted. Legal budget manoeuvre, social-vaccine promise and political-personal contradictions developed.',
14:'P004\u201310 parade of supporters/ribbons compressed. P020\u201322 programme/legal percentages not repeated. P051\u201353 sexuality disclosure omitted: not required to explain data manipulation; proposed causal account of crisis remains someone\u2019s conjecture. P055\u201378 tapes, dissent, institutional diplomacy and interviews developed.',
15:'P008\u201310 Barrowford case omitted, since anecdotal inspection is not experimental proof. P012\u201320 family/travel romance condensed. P025\u201333 review and narcissism correction developed. P035\u201344 generation dispute and Brummelman limits retained. P049\u201360 financial figures/Clinton negotiation scene compressed, not recast as monocausal economics.',
16:'P001 contemporaneous Apple tax dispute not independently updated and omitted in specifics; P003 Netflix/team culture, P005\u201307 Rand revival/Trump labels condensed. Retain risk transfer and digital transition; no current legal or clinical claim.',
17:'P006 detailed UI demonstration condensed; P013\u201317 laboratory/Jobs details shortened. P018\u201324 Brand/WELL/GBN history represented. P031 unrelated hostel scandals omitted; P077\u201381 ghost anecdote omitted. Jeremy labour/drone and mission-versus-profit reasoning developed.',
18:'P001\u201343 hostel conversation condensed, sexual description and ghost story omitted. P044\u201357 Faber plans attributed, not realised capabilities. P058\u201373 electoral specifics condensed; no full election theory. P074 secondhand twins/termination story omitted as weak indirect evidence; P075\u201386 Kate\u2019s direct robot/jobs/religion objections retained. P095\u2013117 selfie rituals, injury details and funeral anecdote selectively shortened.',
19:'P003\u2013004 operational self-harm description omitted, motive/control retained. P009 seduction technique omitted, manipulation mechanism retained. P023 bodily/diet detail compressed. P037\u201341 statistical series shortened; P043 specific campus incidents omitted rather than generalised into proof about a generation.',
20:'P004\u201310 spectacular biological design futures identified as aspirations, not capabilities; clinical product not endorsed. P018\u201335 Heinz dispute, sister\u2019s diagnostic correction and multifactor context developed; no method details from P022\u201323. P039\u201357 Big Five qualifications retained; predictive percentages, deterministic alcoholism/wealth claims P051\u201352 not repeated.',
21:'P001 autobiographical/ancestral rhetoric compressed; P003\u201309 Nettle conversation retains unresolved success/happiness tradeoff. P016\u201322 repeated socioeconomic inventories and totalising metaphors condensed. P023\u201328 responsibility, projects/environment fully represented in original exposition; P030\u201339 actual final reportage scene retained.'}
roles=[
'Debbie\u2019s role ideal becomes a judgment against the whole person; her account prompts investigation, not a single-cause conclusion.',
'OConnor distinguishes depression, socially prescribed perfectionism and entrapment, opening a psychological mechanism with stated uncertainty.',
'Flett locates possible change in public environment and self-presentation; Meredith is participant and producer of comparison.',
'The psychological mechanism needs a cultural explanation of the particular ideal; author selects a limited historical line.',
'Pridmore\u2019s childhood rupture and institutions supply the reported route to gang belonging, without diagnosing him.',
'Club humiliation shows why reputational stakes can outweigh physical danger; explanation does not excuse violence.',
'Primate alliances frame hierarchy; gossip transfers reputational information and teaches approved conduct.',
'Infant cooperation and gang service expose the boundary between group-relative selflessness and universal harmlessness.',
'Christian conversion supplies a new narrative and affiliation; later aggression limits total-transformation claims.',
'Gazzaniga and choice blindness separate a convincing reason from access to causes; this connects personal narrative to culture.',
'Body shame makes cultural evaluation emotionally tangible; Himba task redesign challenges hidden universal assumptions.',
'Neural development and gene/environment interaction prevent simple personal percentages or blank-slate claims.',
'Greek ecology and polis status explain the proposed emergence of a perfectible individual, with male-freedom and historical-inference limits.',
'McAdams narrative identity and Epley self-favouring motives explain appropriation of available heroic stories.',
'Confucian exemplarity offers a contrasting ideal; group tendencies cannot identify a particular individual.',
'Fish/context and within-country studies show that attention and causal blame can privilege person or setting.',
'Kim\u2019s literary perspectives and collective pressure block a simplistic claim that the East solves perfectionism.',
'Pluscarden connects Christian inward discipline to a lived setting and the author\u2019s Catholic memories.',
'Henrich prestige learning adds living exemplars to cultural stories; celebrity influence can exceed competence.',
'Martin overturns Storr\u2019s assumption that repetition lacks a project: vanity and spiritual struggle provide direction.',
'Freud secularises the suspect inner world; Perls becomes the bridge towards a good-self reversal.',
'Smiles\u2019s labour differs from mind-cure belief; shifting causation inward offers hope and risks blaming the sufferer.',
'Great Compression changes economic security and standards of likeability, also generating revolt against conformity.',
'Rogers relationship and unconditional regard are separated from a theory of a perfect core; Coulson is retrospective testimony.',
'Esalen embodies the human-potential promise; false ten-percent claim is identified, author enters the course.',
'Shaw\u2019s bodily practice turns into a guided causal story; Storr\u2019s tears do not verify her explanation.',
'Perls/Schutz encounters expose the contradiction between liberation and authority, plus refusal of responsibility for harm.',
'Hood, Sartre, Snyder and arousal study challenge a pure good core while preserving evidence type and limits.',
'Goat, objectionable role and skit develop Storr\u2019s ambivalent experience: shared action helps, character persists.',
'Williams rejection research explains vulnerability; neural overlap disputed and Esalen tragedies not assigned one cause.',
'Maslow/Rogers doubts and tyranny conference trace movement critique before its political institutionalisation.',
'Rand, Branden and Greenspan carry different branches of the independent ideal; original achievement-based esteem distinguished.',
'Rand\u2019s rejection and Collective\u2019s loyalty show need for recognition within an individualist doctrine; unfair racism comparison rejected.',
'Neoliberal reforms change conditions of getting along/ahead and make entrepreneurial personality a requirement.',
'Vasco\u2019s personal liberation, continued temper and employee objection connect compassion to accountability.',
'The social-vaccine proposal wins state support through responsibility and savings, while testimony is not causal evidence.',
'University prestige converts ridicule into public legitimacy; dissident\u2019s book reveals discrepancy.',
'Archive tape restores scope and direction-of-causation questions; exact words can mislead by selective context.',
'Smelser institutional diplomacy and Mecca publicity strategy explain failure of correction without omniscient motive attribution.',
'Baumeister changes his own prior belief; review distinguishes self-report from independently assessed outcomes.',
'Noise/provocation results correct high-esteem hypothesis to narcissism; sociometer is a model, not a call for humiliation.',
'Generation dispute remains live within the book; parental overvaluation differs from warmth, no Vasco natural experiment.',
'Economic crisis and benefits of trade remain together; risk transfer explains limits of blaming individual losers.',
'Engelbart\u2019s demo and project combine personal augmentation with collaboration; no sole-inventor claim.',
'Encounter programme adds to already multiple lab problems; networked collaboration contrasts with isolated power.',
'Brand/WELL/GBN/Wired connect counterculture and market ideals; Long Boom was a scenario.',
'Social platforms quantify reputation and compare identities; this is the book-period interpretation, not current-platform validation.',
'Jeremy\u2019s drone and exhausting labour develop the founder ideal and simultaneous mission/profit requirement.',
'Shannin/Berkeley/Steph show enterprise as expression and competing social visions; narrator\u2019s discomfort remains visible.',
'Faber\u2019s plans confront Kate\u2019s jobs/religious-outsider objection; desirable innovation has external consequences.',
'Cramer/control narratives and social-news loops explain part of2016 with author bias and not-all-voters qualifications.',
'CJ\u2019s presentation/NPI result introduces an explicitly extreme, possibly performed case rather than clinical or generational diagnosis.',
'Protection, overvaluation and isolation in CJ\u2019s account complicate privilege; no single-family causal proof.',
'Admiration, romantic manipulation and Perry breakup distinguish superiority from dignity; narrator retains sympathy.',
'Fox pool anecdote shows imagined audience; causal-depression uncertainty and positive generational shifts retained.',
'Heinz\u2019s technical work and speculative perfectibility open the final reported case with reconstruction sources explicit.',
'Sweet Peach becomes a misleading headline; Hutchinson\u2019s real objection and later support both retained.',
'Business stress, depression and public attack interact; sister disputes unverified diagnosis and refuses single blame.',
'Little\u2019s misheard graduation lesson introduces stable trait differences and limits of assessment.',
'Traits select/evoke environments; stability allows change, parenting is not deterministic design.',
'Storr revises his earlier illusion claim: stable dispositions coexist with contextual roles, distinct from divine perfection.',
'Acceptance limits self-blame but requires mitigation, apology and obligations; no Perls-style license.',
'Achievable meaningful projects and suitable environments redirect effort without promising a different essence.',
'Actual fogbound launch preserves affection and wonder alongside critique, closing on imperfect social humans.'
]
assert len(roles)==64
m=json.loads((b/'coverage-map.json').read_text())
for u,role in zip(m['units'],roles):u['argumentativeJob']=role
m['wholeMainSpine']=[{'file':a['file'],'checkedRange':{'start':1,'end':len(a['paragraphs'])},'readingComplete':True,'units':[u['unit'] for u in m['units'] if any(l['file']==a['file'] for l in u['primaryLocators'])],'omissions':omit[int(a['file'].split('-')[1].split('.')[0])]}for a in main]
counts=json.loads((b/'metrics.json').read_text())['modes']['deep']['languages']
m['depthDecision']={'ruMainBodyWords':counts['ru']['mainBodyWords'],'enMainBodyWords':counts['en']['mainBodyWords'],'orientation':'12\u201318k RU was a planning range, not a minimum. Result is 10.3% below its lower edge; not padded to reach it. Full chapter spine read and each major reporting arc developed. Omitted long biographical byways, repeated numerical series, lurid detail, secondary campus incidents and tangential scandals, itemised by exact source ranges. A root reviewer may still request restoration.','notWholeBook':'Condensation, not exhaustive reproduction. Full reading does not establish complete retention, English collation or scientific validation.'}
(b/'coverage-map.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
md=['# Selfie \u2014 whole-spine coverage and omissions','Implementation-agent map. Root acceptance is pending. Locators are exact inclusive 1-based paragraph-array positions, not print pages. Main paragraphs were displayed and read continuously; hashes and acknowledgements are in reading-ledger.json.','## Whole main spine','| File | Checked whole range | Retained units | Deliberate compression / omissions |','|---|---|---|---|']
for a in m['wholeMainSpine']:md.append(f"| {a['file']} | P001\u2013P{a['checkedRange']['end']:03d} | {', '.join(map(str,a['units']))} | {a['omissions']} |")
md+=['','## Developed argument, interviews and transitions','Each unit contains three connected paragraphs in each language. Screens were derived afterwards, generally two passages per unit. Level1 appears in every route; level2 adds Core; level3 adds Deep. Shorter routes do not assume that an omitted encounter has been read.','| Unit / depth | RU / EN | Source locations | Argumentative transition / reporting function | Screens |','|---|---|---|---|---|']
for u in m['units']:
 loc='; '.join(f"{l['file']} P{l['start']:03d}\u2013{l['end']:03d}"for l in u['primaryLocators'])
 md.append(f"| {u['unit']} / {u['level']} | {u['titles']['ru']} / {u['titles']['en']} | {loc} | {u['argumentativeJob']} | {', '.join(u['screens'])} |")
md+=['','## Length and evidence boundary',m['depthDecision']['orientation'],m['depthDecision']['notWholeBook'],'','No operational self-harm detail, invented clinical interpretation, dialogue, exercise or corporate lesson has been added. Austen\u2019s sister\u2019s account is attributed; CJ is not a diagnosis or a typical millennial. Self-esteem is distinguished from narcissism. The late stable-traits revision is retained alongside the early authentic-core critique.','Missing images/diagrams cannot be assessed from the text-only extraction. Metadata supplies Russian title and copyright, not a translator credit. Endnotes were consulted selectively (six specified paragraphs); methodology and acknowledgements were read in full.']
(b/'coverage-map.md').write_text('\n\n'.join(md[:3])+'\n\n'+'\n'.join(md[3:])+'\n')
record={'reviewKind':'Implementation self-check, not independent or root acceptance','primary':{'path':str(source),'sha256':h(source),'continuousMainAndMethod':True,'mainParagraphs':ledger['mainSpineParagraphs'],'mainWordsReported':ledger['mainSpineWordsReported'],'notesSelective':notes},'authorMethod':{'locators':['OPS/ch1-2.xhtml P014','OPS/ch1-6.xhtml P031','OPS/ch1-23.xhtml P001\u2013007'],'limits':['Group means cannot describe a specific individual.','Historical chain is selected, simplified and incomplete.','Journalist uses many secondary sources and expert interviews.','Specialists read manuscript in whole or part, not necessarily every claim independently.','Social psychology disputed, own bias/fallibility acknowledged.','Names sometimes changed; interviews edited; hybrid quotations omit ellipses.','No independent present scientific validation performed here.']},'translation':{'English':'Original English rendering of this original Russian exposition, not official English text; no full official collation','names':'Austen Heinz, Peter Marin, Uichol Kim, Dianne Tice rendered in English; underlying narrative scope stays Russian-source based.','metadata':'No translation identity inferred from Russian language or prior ledger. Copyright2017/2019 and exact title actually displayed.'},'scope':['No private primary paragraphs or extraction copied into deliverable.','No edits to root readers, prior collector/ready/reviews, catalogue or global state.','Only new owned candidate; installed skill read-only.','No Git, PR, deploy, external messages, agents or runtime content server.'],'rootPersonalAcceptance':False,'publicationAllowed':False}
(b/'source-method.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
(b/'sources.md').write_text('''# Selfie \u2014 sources and method

Primary evidence is the owner-supplied read-only Russian extraction. SHA256 ec92b521a877c1385bc3d0f3a81c834ce5574f9f51da6852b0efe6f936d11766. Actual metadata: Will Storr, the full Russian title, copyright2017, Individuum Print2019. The provided metadata records do not carry translator/ISBN fields; the old ledger\u2019s claim was not inferred or independently confirmed here.

All main paragraphs OPS/ch1-3.xhtml through ch1-21.xhtml were displayed continuously in30 bounded chunks (including continuations), followed by acknowledgements and complete methodology OPS/ch1-23.xhtml. Exact ranges and paragraph/range hashes are in reading-ledger.json. OPS/ch1-22.xhtml acknowledgements also read. Six exact note paragraphs were displayed selectively; the whole note apparatus was not read continuously.

The single public source link in the reader is a bibliographic pointer retained from the earlier source package. It was not fetched for this implementation and is not evidence of a public full text. No web source or later scientific review substitutes for the author\u2019s argument.

Storr\u2019s own method uses secondary literature, expert interviews and specialist review of all or part of the manuscript. He acknowledges bias, error and disputes in social psychology; he says some names were changed and interview quotations edited or combined. Reported case histories and selected historical chains are not universal experimental demonstrations. Current scientific validity was not independently certified. English is an original rendering of the Russian-source exposition, without full official-English collation.

No image binaries were supplied in the26-record extraction. Illustrations/diagrams and their relationship to passages could not be checked; do not read their absence here as proof that the edition has none. No book cover or substitute diagram was invented. Reader cover is typographic.

Detailed retained interviews, reasoning, transitions and real omissions are in coverage-map.md/.json. Main-body length is measured separately from headings, cover framing, Sources and navigation. Root must personally read every final RU/EN route, compare the map and omissions, and inspect actual critical primary passages before publication. This implementation grants no acceptance.
''')
print({'mainParagraphs':ledger['mainSpineParagraphs'],'mainWordsReported':ledger['mainSpineWordsReported'],'mapUnits':len(m['units'])})
