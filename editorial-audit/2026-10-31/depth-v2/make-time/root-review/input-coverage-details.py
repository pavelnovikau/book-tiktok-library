from pathlib import Path
import json
p=Path(__file__).resolve().parent
notes='''Record the choice in a convenient daily ritual; a visible note can remind you.
Repeat unfinished, continuing, skill-building, or enjoyable Highlights rather than demand novelty.
List and rank current life areas; circle the first; revise ranking when conditions change.
Batch accumulated minor work occasionally; avoid making cleanup the daily default.
Store possibilities separately from the decision and calendar; JZ and Michelle’s boat work anchors the procedure.
Two columns, one main project, reserved blank space, secondary project and sink; rewrite after several days.
Repeat one project across consecutive days to reduce startup; Jake’s slow first writing days are retained.
Choose duration and start time, then account for prerequisites such as leaving work for groceries.
Reserve one or two hours proactively, leave availability, and treat the reservation seriously; Graham is named.
Move, shorten, or cluster appointments with participants; power differs between manager and intern.
Cancel an occasional excessive commitment honestly; this is temporary relief rather than lasting unreliability.
Give an honest refusal; Kristen’s sincere helpful ending must not become a false future promise.
Plan the day, compare it with reality, revise the drawing; Sarah Cooper and Newport retain their distinct roles.
JZ’s light, coffee ritual and activity require an earlier evening and sufficient sleep; not everyone follows it.
Jake rests first, disconnects for writing, then winds down and meets his personal bedtime.
Choose a stopping boundary rather than await an empty inbox; recognise displaced Highlights and preserve tomorrow’s energy.
Remove endless apps, ordinary mail and browser; retain tools; temporarily restore access for a specific task.
Log out and decline remembered sessions; JZ adds complicated password-manager credentials as friction.
Disable most alerts but retain useful reminders and one urgent SMS route; review after a short trial.
Move icons from the home screen to create a pause after habitual unlocking.
Use a wristwatch to check time without opening a phone’s opportunities for distraction.
Chris leaves devices at work; people who must be reachable can instead put the phone away at home.
Preserve the overnight break from streams; JZ prepares a closed-tab, logged-out computer the previous evening.
Identify the particular service drawing regretful habitual returns, then match its strength with a barrier.
Choose news frequency and purpose; JZ’s weekly magazine, podcast and targeted research are personal choices.
Close apps and tabs, hide tempting bookmarks, use a calm start page to prepare the next opening.
Decline flight Wi-Fi and switch off the seat screen; retain the source note’s exception for children.
Use blockers or a router timer; Jake’s nine-thirty cutoff removes repeated decisions from tired evenings.
Chrissa cancels home broadband, retains tethering; a friend changing the password supplies a temporary trial.
Track consequences beyond initial action: Jake’s tweet leads to checking, browsing and renewed context loading.
Recognise easy completions that displace the selected Highlight; the same activity can be appropriate elsewhere.
Define purpose, time budget and entry route; JZ bypasses Twitter feed, Jake uses a stricter blocker.
Preserve enjoyable sport-related occasions while dropping continual coverage; JZ keeps shared Packers games and rare visits.
Try end-of-day email to protect better hours and reduce unnecessary commitments and elaborate replies.
Reserve a bounded mail session followed by an unavoidable transition; knowing it is scheduled supports waiting.
JZ aims for weekly clearing, handling genuinely urgent messages meanwhile and preserving a faster alternate channel.
Treat arrival like asynchronous paper mail rather than a live conversation demanding immediate response.
Reply at the slowest rate consequences permit; do not translate physical politeness into universal instant availability.
An explicit notice is optional; colleagues sometimes infer the pattern. Sales/support can require fast replies.
Separate phone sending from receiving through a dedicated account and forwarding; Taylor and Rizwan have distinct contributions.
Create deliberate holiday unavailability where possible through expectations, removed mail and leaving the laptop.
Choose blocking windows after assessing real deadlines; Jake’s ten-thirty and three-o’clock checks reflect time zones.
Replace repetitive television news with selected reading; its inefficiency belongs to the authors’ argument.
Move the television so conversation becomes easier; Cindy and Steve’s household retains occasional watching.
A projector adds setup before viewing; it is an optional friction device, not a prescribed purchase.
Choose individual films/episodes instead of automatically entering an endless subscription catalogue.
Try a television-free month and then decide how much viewing to restore; Jake’s Swiss move provides a real case.
Close a door or signal concentration through headphones, including silent ones, where a room is unavailable.
Create an external commitment; Friday sprint interviews and JZ’s race give an otherwise optional task a deadline.
Divide the Highlight into concrete verb-led actions; holiday planning example and Allen attribution are retained.
Reserve liked music for a particular activity, building a cue instead of prescribing a genre.
Make time visible with a shrinking dial; Jake’s playtime timer is a specific family practice.
Prefer robust simple tools; JZ’s Mori failure shows setup, compatibility, access and discontinued-support costs.
Begin on paper to avoid online options and predetermined software formats while finding an idea.
Write distracting questions down for later rather than research each immediately.
One attentive breath reconnects bodily sensation and the chosen task.
Allow a quiet boring interval instead of automatically filling it with a feed.
When stuck, stay with the problem, move to paper or walk rather than take an unrelated digital escape.
If tactics fail, rest or reduce intensity; where a day off is impossible, use real breaks or a pleasant Highlight.
Wholehearted involvement sometimes differs from rest; monk attribution, Jake’s play and JZ’s sailing remain conditional.
Accept modest regular movement and less-than-perfect days; Jake’s basketball injury versus stroller run anchors the shift.
Build walking into travel, including partial routes; JZ’s commute also becomes time for thinking.
Select useful inconveniences such as stairs or cooking; the authors retain disagreement over luggage wheels.
Brief intense routines are one option. The textual interval description and JZ’s three-by-three remain; missing movement image is not guessed.
Arrange simple recognisable food in advance; Pollan attribution and the authors’ different preparation habits remain.
Put salad on the plate first and arrange the rest around it; no exact nutritional ratio is invented.
JZ describes personal fasting and Kevin’s sixteen-hour arrangement; broad disease/longevity promises are not endorsed.
Jake carries chosen snacks and responds to hunger rather than boredom; he does not adopt JZ’s fasting preference.
Change the usual dessert rather than ban treats; Jake’s drive with Holly and the caffeine qualification remain.
The delayed first cup is an author trial, not a universal hormonal prescription; Ryan’s individual differences remain.
Anticipate a habitual energy dip instead of waiting for complete exhaustion; exact half-hour lead is compressed.
JZ pairs coffee with a fifteen-minute rest; his response is personal, not a promised cognitive effect.
Smaller portions such as green tea are an option rather than a compulsory drink substitution.
Align a helpful cup with starting the Highlight while remembering its later sleep cost.
Find an earlier last cup by observing sleep onset; Camille Fleming’s role and Ryan’s nonuniversal window are retained.
Separate caffeine from an automatic sugar serving; no complete sugar ban is claimed.
Change surroundings through woods, park or outdoor break; Jake’s lawyer father and later running are retained.
Start with brief guided meditation in a convenient setting; Holly, Headspace and Jake’s observations remain personal.
Sometimes leave headphones off to allow quiet; their other helpful functions are not cancelled.
Choose a real break rather than another feed; JZ’s logout cue and Jake’s complete-film alternative explain the distinction.
Choose a person whose voice contact usually helps and notice energy afterward; phone contact is included.
Eat without screens for attention, rest and conversation; the shift between Jake’s and Holly’s family customs is retained.
Remove devices and charging from the bedroom; paper/quiet reader and a separate alarm preserve useful functions.
Dim the evening gradually, use night mode and remove screens; mask and gradual morning light are optional supports.
Rest ten to twenty minutes without requiring sleep; office embarrassment/time limits and weekend options remain.
The book and Kristen prefer steadier rhythms; real sleep debt is acknowledged, not replaced by a blanket deprivation rule.
Caregiving can make routines unavailable; preserve small opportunities for food, rest and sleep to sustain care itself.'''.splitlines()
assert len(notes)==87,len(notes)
x=json.loads((p/'coverage-map.json').read_text())
for t,note in zip(x['tactics'],notes):
 t['retainedMechanism']=note
 t['compressionRationale']='Explains the mechanism in connected prose; repeated exhortations and secondary ornament do not need separate screens.'
 if t['tactic'] in [14,15]:t['compressionRationale']='Keeps the actual author-specific transition and limits, but omits a complete hour-by-hour illustrated diary.'
 if t['tactic'] in [25,33,43]:t['compressionRationale']='Keeps consumption purpose and a real choice; omits dated audience statistics and most rhetorical comparison.'
 if t['tactic']==64:t['compressionRationale']='Owned text lacks exact illustrated twelve-movement sequence; the concrete gap is stated rather than repaired from outside memory.'
 if t['tactic'] in range(70,77):t['compressionRationale']='Grouped by timing and sleep consequences; not all biochemical explanation, dose equivalences or asserted numerical effects are repeated.'
 if t['tactic']==78:t['compressionRationale']='The guided practice and actual case are enough here; cortical-thickness/GRE effect claims and 400-day streak are not necessary to the practical argument.'
 if t['tactic']==86:t['compressionRationale']='Preserves rhythm reasoning and sleep-debt qualification without presenting it as independently updated clinical advice.'
(P:=p/'coverage-map.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
md=(p/'coverage-map.md').read_text();md+='\n## What each numbered tactic actually contributes\n\n'
for t in x['tactics']:md+=f"{t['tactic']}. {t['retainedMechanism']} Compression: {t['compressionRationale']}\n\n"
(p/'coverage-map.md').write_text(md)
