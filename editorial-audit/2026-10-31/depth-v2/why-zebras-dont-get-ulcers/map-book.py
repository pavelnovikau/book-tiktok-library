"""Generate a review map; inspect the private primary text read-only.

Only locations, hashes and original paraphrase enter this directory.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "story-data.json").read_text())
LEDGER = json.loads((ROOT / "source-reading-ledger.json").read_text())
PRIVATE = Path(LEDGER["sourceRoot"])
ROOT_ANCHOR_FILE = ROOT / "root-review/map-anchor-repairs.json"
ROOT_ANCHORS = json.loads(ROOT_ANCHOR_FILE.read_text())["cases"] if ROOT_ANCHOR_FILE.exists() else {}


def case(units, name, kind, needles, setup, result, limit):
    return dict(units=units, name=name, kind=kind, find=needles,
                setup=setup, resultOrFunction=result, qualification=limit)


CHAPTERS = [
    dict(chapter=1, label="Anticipation, allostasis, and the price of mobilization",
         argument="A response useful during an immediate physical emergency can be initiated by anticipated events. Damage often comes from its persistent operation, failed shutoff, or mismatched recovery, rather than a stock of stress hormones running out.",
         mechanisms=["Resource redistribution temporarily postpones digestion, growth and reproduction.", "Allostasis coordinates changing settings and behavior; a missing response can also be dangerous.", "Disease risk runs through intermediate vulnerabilities and interacting causes."],
         cases=[
             case([1,2],"Opening insomnia and the zebra/lion comparison","author illustration",["Два часа"],"Someone anticipates an important day, then worries about sleeplessness and bodily symptoms; a chase requires immediate physical expenditure.","Anticipation can recruit real bodily preparation before physical damage occurs.","The zebra is a comparison, not a claim that other animals never experience chronic stress or ulcers."),
             case([4,5],"Selye's extract and saline groups","reported experiment",["Селье"],"Rats receiving ovarian extract and saline controls both experience injections and difficult handling; other stressors are then varied.","The recurring pattern supports a shared response component; it does not establish the extract as its cause.","Sapolsky rejects Selye's simple exhaustion explanation while retaining the discovery's importance.")],
         omissions="Historical population-mortality estimates and extended comparisons with conquered infectious disease are not reproduced as contemporary epidemiology; the adaptive-versus-chronic distinction is retained."),
    dict(chapter=2, label="Neural and endocrine communication",
         argument="The brain's appraisal reaches organs through identifiable neural and chemical routes, with different speeds, receptors and feedback. There is no single fixed hormonal signature of every stressor.",
         mechanisms=["Sympathetic signaling, norepinephrine and adrenal-medullary epinephrine provide a rapid route.", "Hypothalamic CRH → pituitary ACTH → adrenal-cortical glucocorticoids; feedback limits secretion.", "Pituitary stimulation and inhibition, tissue sensitivity, timing, species and context complicate a simple command model."],
         cases=[
             case([8],"Discovery of hypothalamic releasing signals","research history",["Шалли","Гиймен","Гиллемин"],"Changes after pituitary isolation and brain injury suggest upstream instructions; investigators purify tiny active fractions from large amounts of animal tissue.","Chemical instructions from hypothalamus to pituitary give an experimentally grounded route from brain to endocrine organs.","The historical master-gland label is revised, not merely repeated."),
             case([9],"Tending and befriending","author's discussion of a hypothesis",["Тейлор"],"Shelley Taylor's proposal expands the behavioral picture beyond obligatory fighting or fleeing.","Bonding and care can be part of responses to threat.","Counterexamples in both sexes prevent a universal male/female binary; rats and humans also differ in acute growth-hormone responses.")],
         omissions="Full lists of every gland, purification detail and sex-difference study are compressed. The actual HPA sequence, feedback and variation remain explicit."),
    dict(chapter=3, label="Cardiovascular adaptation and vulnerability",
         argument="The same circulatory preparation that supplies working muscles can repeatedly burden vessels and a vulnerable heart. Chronic disease formation, an acute trigger and the interpretation of social experiments are separate questions.",
         mechanisms=["Rate, contraction force, venous return, vascular redistribution and water retention work together.", "Vessel remodeling raises resistance and reinforces pressure; inflammation, lipids and clotting interact.", "Atherosclerotic vulnerability, ischemia and arrhythmia are not interchangeable endpoints."],
         cases=[
             case([12],"Kaplan's reorganized primate groups","reported animal experiment",["Каплан"],"Social groups are repeatedly reorganized, altering rank stability; diet and sympathetic blockade are considered.","Which rank bears the physiological cost depends on stability and interaction conditions.","Not proof that one human job title inevitably causes plaques; diet and experimental context matter."),
             case([13],"Excitement acting on an already vulnerable heart","author's clinical/observational discussion",["ишеми"],"Short episodes of arousal occur against prior vascular or cardiac vulnerability.","A trigger can matter without explaining the whole disease's origin.","The old discussion of fear, joy and sudden death does not establish every historical death account's autonomic cause."),
             case([14],"Hormone therapy and the WHI result","book-era clinical evidence",["2002","женского здоровья"],"Observational and animal expectations concerning estrogen are set beside a randomized hormone-therapy result.","A plausible protective pathway does not settle the result of a particular formulation and clinical intervention.","The passage is a book-era lesson about the evidence, not a current treatment recommendation.")],
         omissions="Voodoo-death anecdotes, most dramatic mortality figures, and the CRP/egg rhetoric are omitted. No historical hormone regimen is turned into clinical advice."),
    dict(chapter=4, label="Fuel storage, mobilization and cumulative burden",
         argument="Insulin supports storage; emergency signals mobilize and redistribute fuel. Repeated reversal has costs and can aggravate metabolic vulnerability, while combined modest disturbances can matter across systems.",
         mechanisms=["Glycogen, triglycerides and protein connect circulating nutrients with reserves.", "Stress restricts storage, promotes glucose production and changes insulin effectiveness in different tissues.", "Type 1 autoimmune insulin deficiency differs from type 2 resistance and compensatory secretion; later beta-cell decline is not conversion into autoimmune type 1."],
         cases=[
             case([15,16,17],"The author's savings-account explanation","author's explanatory analogy",["инсулин"],"The body stores nutrients after feeding and releases them for immediate demand.","Repeated withdrawals and redeposits themselves use energy and can compromise long-term tissue maintenance.","This is the author's analogy for actual biochemical transformations, not a new financial application framework."),
             case([18],"Seeman's older-adult biomarker study","reported observational study",["Симен"],"Older participants are compared using multiple physiological measures, including values below individual disease thresholds.","A combined burden can be informative when no single dramatic abnormality captures the pattern.","Allostatic load is not one hormone, one universal test, or a diagnosis from subjective worry.")],
         omissions="Outdated diabetes-prevalence figures, detailed adipocyte-count claims and full biomarker scoring instructions are omitted. Distinct diabetes mechanisms are retained."),
    dict(chapter=5, label="Appetite, fat distribution, gut and ulcer defenses",
         argument="Timing explains opposite appetite responses, while different gut regions and mucosal defenses respond differently. Infection changes the ulcer explanation without answering why every infected person has the same outcome.",
         mechanisms=["Fast CRH-related appetite suppression can precede slower, longer glucocorticoid effects.", "Visceral fat, insulin and reward-related eating complicate a simple calories-versus-willpower account.", "Upper-tract inhibition, colonic activity and visceral sensitivity differ.", "Mucus, flow, repair, acid rebound and ischemia/reperfusion provide distinct ulcer pathways."],
         cases=[
             case([19,20],"Epel's stress-and-eating comparison","reported human experiment",["Эпель"],"Food intake after experimental stress is compared with glucocorticoid responsiveness and calmer conditions.","Stronger responders ate more, especially sweet foods, in the stress condition; baseline intake need not show the same difference.","Timing, restrained eating and the surrounding food environment matter; the result does not classify moral strength."),
             case([20],"Comfort-food feedback","reported experimental interpretation",["Даллман"],"Energy-dense food and insulin-related conditions are considered alongside HPA activity.","A short-term reduction in one stress signal need not mean a favorable overall metabolic outcome.","The mechanism is not an instruction to use food as treatment."),
             case([22,23],"Warren, Marshall and the ulcer explanation","research/clinical history",["Маршалл"],"Bacterial evidence and antimicrobial treatment challenge a purely psychological explanation of recurring peptic disease.","Infection and host defenses can interact; Marshall's self-exposure produced gastritis, not a demonstrated self-created ulcer.","Current NIDDK common-cause information is labeled separately; no historical percentage is silently made contemporary.")],
         omissions="Detailed IBS subtype catalogues, all dietary examples and old infection prevalence estimates are compressed or omitted. No individual gastrointestinal diagnosis is offered."),
    dict(chapter=6, label="Development, active contact and growth",
         argument="Developing organisms carry their early conditions into later regulation, but early effects are not destiny. Severe deprivation, active tactile interaction, ordinary family imperfections and species differences must remain distinct.",
         mechanisms=["Prenatal conditions can alter later metabolic fit and HPA-feedback sensitivity.", "Growth requires coordinated GH, somatomedin and other signals; acute metabolic GH action differs from long-term growth action.", "Bones continue remodeling after childhood; strong glucocorticoid exposure and everyday stress are different evidence conditions."],
         cases=[
             case([24],"Dutch hunger winter and Barker's question","historical cohort/research interpretation",["голод","Баркер"],"Prenatal famine exposure is considered by developmental timing and later conditions.","The book develops a mismatch hypothesis between early scarcity and later abundance.","Birth weight is an imperfect proxy; pregnancy and postnatal conditions are not easily separated in humans."),
             case([25],"Prenatal animal exposure and feedback receptors","reported animal experiments",["рецептор"],"Pregnant animals encounter stress or glucocorticoid exposure; later behavior, endocrine recovery and metabolism are compared in offspring.","A developmental change may alter later response shutoff rather than only current arousal.","Repeated maternal physiology can create intergenerational similarities without demonstrating inherited DNA change."),
             case([27],"The nurse's three-week holiday","reported clinical case",["отпуск"],"A child with severe growth failure improves, worsens during the nurse's absence and improves again after her return, with similar food intake.","Stimulated GH response and measured growth track changes in a significant relationship.","One case; the table measures stimulated hormone and growth over time, not a continuous basal love-dependent hormone level."),
             case([28],"Separated rat pups, sedated mother and simulated licking","reported animal experiment",["вылизыв"],"GH falls after separation; contact with a sedated mother is compared with active licking-like stimulation.","Active tactile interaction restores the measurement where passive maternal presence does not.","This chapter-6 result is not an invented reunion-care explanation of chapter-18 aging results; human transfer is bounded."),
             case([28,29],"Premature-infant touch and Harlow's surrogates","separate reported studies",["Харлоу","недоношен"],"Hospital tactile-stimulation studies and macaque milk-versus-soft-surrogate comparisons ask different questions.","Sensory interaction and attachment cannot be reduced to nutrition alone.","Hospital conditions and animal experiments remain distinct; the cruelty of isolation experiments is acknowledged.")],
         omissions="Initiation-ritual correlations, the Barrie/Peter Pan anecdote and most hormone quantities are omitted. The nurse's table is explained without reproducing it. No parenting protocol is invented."),
    dict(chapter=7, label="Reproductive suppression and resilience",
         argument="Threat and energetic conditions can act at several reproductive levels, yet basic reproduction is often more resilient than a simple shutdown story suggests. Hormones, desire, sexual coordination and fertility outcomes are not one measure.",
         mechanisms=["Hypothalamic releasing signals, pituitary LH/FSH and gonadal response form distinct sites of inhibition.", "Opioids, prolactin and glucocorticoids participate; erectile parasympathetic/vascular coordination differs from ejaculation and libido.", "Energy availability and signal duration alter cycles; outcome-to-distress reverse causality complicates infertility research."],
         cases=[
             case([33],"Feeding patterns and lactational signals","author's comparative example",["Калахари"],"Different feeding patterns change the persistence of prolactin-related signals.","Signal timing matters alongside its peak, illustrating interaction between behavior and endocrine regulation.","Not a contraception method or an inference that menstruation proves ovulation."),
             case([34],"Mating-season and hyena exceptions","comparative animal cases",["гиен"],"Reproductive behavior continues under unusually stressful social or seasonal conditions.","The cost and regulation of reproduction depend on ecology and behavior.","The author's possible rewiring explanation is not a demonstrated universal human mechanism."),
             case([35],"Distress surrounding infertility treatment","book-era human evidence discussion",["бесплоди"],"Distress is measured among people whose failures, treatment demands and relationship strain can themselves create stress.","The association does not by itself establish distress as the initiating cause; basic reproductive resilience remains part of the chapter.","No promise that calmness ensures pregnancy and no blame for the outcome.")],
         omissions="The rodent Bruce effect, detailed implantation/pregnancy-loss discussion, full desire-lever experiments and numerical fertility comparisons are omitted. Severe human historical circumstances are not normalized."),
    dict(chapter=8, label="Immune timing, clinical illness, cancer and mistaken normality",
         argument="The immune system is regulated in both directions. Acute mobilization, later restraint, persistent suppression and inadequate restraint differ. A plausible immune pathway is insufficient evidence for infection, spontaneous cancer or survival claims.",
         mechanisms=["Innate/acquired functions, cytokines and neural/endocrine access are reciprocal.", "Cell migration means lower blood counts can coexist with increased defense at a target site.", "Immune activation → endocrine restraint limits self-damage; onset, progression and recurrence are different outcomes.", "Selection of the reference population can create a fictitious anatomical abnormality."],
         cases=[
             case([37],"Ader and Cohen's conditioned immune response","reported animal experiment",["Адер"],"A flavor is paired with an immunosuppressive drug and later presented separately; lupus-prone mice make the functional direction important.","The learned cue suppresses immune activity; in the reported autoimmune mouse model the suppression can prolong life, while inhibition can harm defense against infection.","Not proof of unrestricted conscious control or a general cure."),
             case([38,39],"Dhabhar's migrating cells and Munck's immune brake","separate reported animal experiments",["Дабхар","Манк","Мунк"],"Acute stress is assessed across compartments; another line restrains glucocorticoid feedback during immune challenge.","Redistribution differs from depletion; keeping the glucocorticoid brake low increases autoimmune risk in the reported rats.","One blood sample and a maxim of more immunity are insufficient descriptions."),
             case([40,41],"Cohen's rhinovirus volunteers and social isolation","human challenge study plus distinct animal evidence",["Коэн"],"Virus exposure is standardized after prior stress assessment; separate primate work concerns social conditions and infection course.","A clinical cold after comparable exposure is stronger evidence than a lab marker alone; multiple social-to-health routes remain plausible.","Human stress histories were not randomized; isolated primate conditions cannot stand for every human network."),
             case([42],"Transplanted tumors in animals","reported animal model",["опухол"],"Stressed animals already receive tumor cells or a virus-related tumor challenge.","The model can inform growth/progression mechanisms.","It does not directly show spontaneous human cancer onset from stress."),
             case([43,44],"Spiegel's support groups, a later trial and Siegel's promises","book-era clinical trials and critique",["Шпигел","Шпигель","Зигел"],"A randomized metastatic-breast-cancer support intervention reports a survival difference; a later study does not reproduce survival benefit.","Support's distress benefit can stand without a demonstrated survival mechanism; possible contamination is an explanation to test.","Not a resolved replication story, a personality cure or a reason to blame a patient. NCI's present qualification is separate."),
             case([45],"Which infant thymus counted as normal?","historical selection error",["тимус"],"Chronically ill autopsy cases define a shrunken reference; sudden-death infants look enlarged by comparison.","A mistaken normal range contributed to unnecessary irradiation and later harm.","The retained point is reference-group selection, not a current account of SIDS causation.")],
         omissions="Most historical HIV/latent-virus treatment detail, every immune pathway and all cancer studies are omitted. No historical treatment regimen or deterministic bereavement mortality claim is retained."),
    dict(chapter=9, label="Pain signaling, modulation and chronic amplification",
         argument="Pain reflects signaling and context-sensitive neural processing. Urgent threat can suppress it, whereas persistent anxiety can amplify it; neither change makes injury or suffering unreal.",
         mechanisms=["Spinal inhibitory circuits and descending control modulate transmission.", "Endogenous opioid action explains some stress/placebo analgesia; antagonist effects do not make all analgesia opioid.", "Sensitization, anticipation and visceral exceptions complicate a uniform acute-stress analgesia rule."],
         cases=[
             case([46],"Beecher's wounded soldiers and civilians","reported clinical comparison",["Бичер"],"Morphine need is compared in soldiers and civilians with roughly comparable injuries but different meanings of injury.","Relief from combat can alter the affective context of a wound.","Not randomized proof that attitude determines every patient's pain."),
             case([47,48],"Spinal gating and opioid-blockade evidence","reported mechanisms/experiments",["налоксон","опиат"],"Touch-related input and descending pathways affect relay; antagonists test opioid involvement in selected analgesic responses.","Transmission is actively regulated; some endogenous relief has an identifiable chemical route.","Modulation is not tissue healing; not all pain relief uses the same route."),
             case([48,49],"The author's daughter's painful ear and anticipation","author's family anecdote and mechanism",["доч"],"A change in painful circumstances produces relief before an antibiotic could explain it.","Time course can distinguish immediate modulation from slower treatment action.","The anecdote is not evidence that the underlying infection was unreal or that chronic pain requires no care.")],
         omissions="Most opening literary examples and detailed imaging/hypnosis protocols are omitted. Old fibromyalgia hormone hypotheses are not offered as a diagnostic test."),
    dict(chapter=10, label="Memory systems and the dose/context of arousal",
         argument="Encoding, consolidation, retrieval and different memory systems respond differently. Arousal can enhance selected emotional material while prolonged exposure disrupts hippocampal function; human volume differences need causal alternatives.",
         mechanisms=["Explicit contextual memory differs from procedural learning.", "Different receptor sensitivities and amygdala–hippocampus interactions help explain nonlinearity.", "Synaptic plasticity, dendrites, neurogenesis and energetic vulnerability are distinct experimental endpoints.", "MRI volume does not count dead neurons or establish direction of causality."],
         cases=[
             case([51],"H.M. learns a skill without remembering the sessions","reported neurological case",["инициалами","Г. M."],"A patient with profound explicit-memory difficulty nevertheless improves a practiced procedure.","Memory is not one storage function; performance and conscious recollection can dissociate.","The case does not imply that all stress effects on memory are identical to a surgical lesion."),
             case([52],"Cahill and McGaugh's hospital stories and propranolol","reported human experiments",["Кахилл","Кэхилл","Макгоу"],"A neutral hospital visit is compared with an emotionally arousing accident story; blockade is tested.","The emotional segment has selective retention benefit, which the blocker removes without erasing all neutral memory.","Vividness is not global accuracy; a drug's experimental use is not a prescribing recommendation."),
             case([54,55],"Cushing's recovery and the PTSD vulnerability alternative","book-era human evidence",["Кушинг"],"Volume and function are considered after correction of hormone excess; the book also raises the possibility that smaller volume preceded PTSD without detailing the design of that study.","Some differences can precede symptoms or be reversible; consequence is not the only model.","Human scans, rodent cell changes and severe hormone exposure cannot be equated.")],
         omissions="The deliberately fanciful opening Coke celebration is not retold as a real memoir. Historical stroke/spinal-injury drug discussions and every plasticity experiment are omitted."),
    dict(chapter=11, label="Sleep as an active process and a two-way loop",
         argument="Sleep loss increases stress and arousal disrupts sleep, including its organization. Sleep also serves active neural functions; anticipation and recovery intervals matter.",
         mechanisms=["NREM/REM organization differs; replay and consolidation can affect later learning.", "CRH/arousal and fragmented restorative sleep reinforce a loop without making a single bad night fatal.", "Circadian endocrine preparation can precede an expected wake time."],
         cases=[
             case([56],"The new father and spilled cranberry juice","author's family episode",["клюкв"],"Confidence about organized care gives way to repeated waking; the child finally sleeps while the father keeps anticipating another interruption.","A concrete scene introduces both directions of the sleep–stress relationship.","No invented dialogue is supplied; the event is paraphrased."),
             case([57],"Sleeping rats and reversal learning","reported animal research",["Макнотон","Макноутон","Хэйрстон","Хэрстон"],"Neural replay and a task whose old response must later be reversed are considered.","An apparent later advantage after sleep loss can result from less consolidation of the old habit, not improved learning overall.","Sleep-deprivation procedure effects and particular task demands matter."),
             case([58],"Airline staff with five versus fifteen recovery days","reported observational comparison",["Бристольск"],"Flight-related conditions are compared with different intervals for recovery.","Recovery opportunity is associated with memory-related differences.","An observational workplace comparison does not demonstrate irreversible neuron loss."),
             case([59],"Expected waking at six or nine","reported human experiment",["Борн"],"Participants expect different wake times; hormonal activity is measured before actual waking.","Preparation shifts before the scheduled event, illustrating anticipatory regulation.","Not a general ability to command hormone rhythms or guarantee punctual waking.")],
         omissions="Historical insomnia prevalence and nightly-hour statistics are omitted. No sleep schedule or medical protocol is prescribed."),
    dict(chapter=12, label="Aging, reserve and the feedback-cascade hypothesis",
         argument="Aging differences can appear mainly under challenge or during delayed recovery. A glucocorticoid–hippocampal feedback loop is an investigable hypothesis with substantial individual variation, not a universal aging clock.",
         mechanisms=["Reduced maximum reserve can coexist with ordinary resting function.", "Feedback challenge distinguishes peak output from response shutoff.", "Hippocampal impairment and prolonged glucocorticoid exposure can reinforce one another in models."],
         cases=[
             case([60],"Timed versus unhurried cognitive performance","reported aging comparison",["интеллект","тест"],"Performance under added time pressure is set beside less-demanding conditions.","Loss of reserve differs from a universal inability to do the task.","Averages and distributions must remain distinct."),
             case([61],"Postreproductive salmon and adrenal intervention","comparative species case/experiment",["лосос"],"Rapid postreproductive deterioration and adrenal involvement are examined in an extreme life history.","Endocrine regulation can strongly affect a particular species' life cycle.","Not a human adrenal-removal or longevity proposal."),
             case([62],"Feedback testing and the cascade","reported experimental hypothesis",["дексаметазон"],"An external glucocorticoid signal should suppress upstream secretion; old and impaired animals vary in recovery.","A failing controller can prolong the signal that further burdens the controller.","Human generalization and inevitable decline remain unresolved; chapter 18 returns to preserved function.")],
         omissions="Fixed-heartbeat/rate-of-living simplifications and most cultural old-age vignettes are omitted. Their absence is not a claim that this chapter establishes a single alternative theory."),
    dict(chapter=13, label="Appraisal, outlets, predictability and control",
         argument="Holding physical exposure similar while changing information or available action reveals how psychological organization changes a response. Benefits depend on timing, accuracy, stakes and genuine possibilities.",
         mechanisms=["Outlets, familiar support, predictive signals and perceived control alter commands from brain to body.", "A warning also defines safe intervals; an indefinite warning may prolong anticipation.", "Relative improvement and expectations matter, but illustrative numbers are not experimental results.", "Impossible responsibility can convert control into guilt; experimental selection can distort an executive-stress story."],
         cases=[
             case([63],"Mason's appraisal claim and the anesthetized incision","author's scientific disagreement",["Мейсон","Мэйсон"],"Psychological interpretation is important, but a physical incision still recruits a response under anesthesia.","Neither purely physical dose nor conscious appraisal explains every response.","Appraisal is not denial of physical stressors."),
             case([64],"Weiss's shocks with a gnawing block","reported animal experiment",["Вайс"],"Comparable shock exposure is paired with an available gnawing outlet.","Animals with an outlet show less physiological damage, including ulceration.","Displaced aggression is a separate harmful-to-others outlet, not a coping prescription."),
             case([65,66],"Warning signals and the changing-shock illustration","experiment plus author's hypothetical example",["предсказуем","двадцать пять","25 удар"],"Warnings distinguish threat from safe periods; a numerical improvement/worsening scenario explains reference history.","Information and direction of change alter the meaning of the same present burden.","The changing-number scenario is explicitly an illustration, not a claimed performed trial."),
             case([67,68],"Control levers, a human noise button and executive monkeys","separate reported experiments and design critique",["Брэйди"],"Controllable exposure is contrasted with lacking control; Brady's fast learners were selected into the executive condition.","Perceived action can help, while nonrandom assignment complicates claims that responsibility causes ulcers.","No general law that either bosses or subordinates always suffer most; unavoidable outcomes require different control claims.")],
         omissions="All warning intervals, every parachute-habituation result and detailed occupational survey statistics are compressed. The limits of prediction/control remain beside their benefits."),
    dict(chapter=14, label="Depression across biological and psychological levels",
         argument="Major depression involves anhedonia and widespread function changes. Stress links experience, cognition and biology without yielding one universal transmitter, hormone profile or gene explanation.",
         mechanisms=["Rapid monoamine action versus delayed clinical effects motivates receptor/network alternatives, not a proven simple deficiency.", "Cytokines, thyroid/sex hormones and susceptible circuits illustrate multiple entrances.", "Elevated HPA activity and failed feedback occur in a subset; recurrent episodes can become less tied to an external trigger.", "Generalized ineffective-action learning models part of depression without reproducing the human illness."],
         cases=[
             case([70],"The apparently shortened hospital corridor","author's reported personal acquaintance",["коридор"],"A recovering patient walks more but invents a reconstruction of the corridor to preserve the belief that he is deteriorating.","Interpretation can absorb contrary evidence in depression.","The account is the author's case, not a new invented patient or a universal description."),
             case([71,72,73],"Drug timing and heterogeneous biological pathways","book-era research discussion",["моноамин"],"Biochemical onset, symptom time course and distinct endocrine/immune findings are compared.","Treatment mechanism does not automatically reveal origin; one biological pattern cannot represent all depression.","Old experimental hormonal approaches are not presented as current standards or individual advice."),
             case([74],"Seligman and Maier's controllable versus uncontrollable exposure","reported animal experiments/model",["Селигман","Майер"],"Prior uncontrollable shocks are followed by a situation in which escape is possible, with controllable-exposure comparison animals.","Some animals fail to use the new option; prior experience generalizes beyond the original event.","Models initiative and expectations, not guilt, language and the entire human disorder."),
             case([75],"Hiroto's noise and unsolvable tasks","reported human experimental model",["Хирото"],"Participants face controllable or uncontrollable noise and insoluble problems before later tasks.","Apparent futility can carry into a new solvable setting.","A brief induced pattern is not a diagnosis of major depression."),
             case([76],"Early candidate-gene excitement and later large-sample testing","historical hypothesis plus separate modern primary abstract",["Каспи","серотонин"],"The book's early susceptibility hypothesis is distinguished from Border et al.'s later preregistered large-sample analyses.","The later abstract reports no support for the historical candidate-gene hypotheses tested.","Only the abstract was read; this does not refute all heredity, environment or possible gene–environment relations.")],
         omissions="Detailed drug lists/doses, old DHEA/antiglucocorticoid optimism, all genetic calculations and the full Freudian history are omitted or briefly attributed. No current treatment review is claimed."),
    dict(chapter=15, label="Temperament, learned threat, hostility and apparent calm",
         argument="Within the same rank, threat discrimination, social relationships and response style can change exposure and recovery. Personality labels become misleading when circular or used as diagnoses.",
         mechanisms=["Amygdala-linked learning can recruit autonomic responses before conscious contextual recognition.", "Stress effects on threat-related and contextual-memory circuits can diverge in animal work.", "The broad Type A bundle differs from hostility; subjective report, facial expression and physiological arousal can disagree."],
         cases=[
             case([77],"Two same-rank baboon response styles","author's field observations",["Гэри","Гари","Кеннет"],"Baboons differ in responding to real versus neutral challenges, winning versus losing and affiliative opportunities.","Rank alone does not exhaust variation; real interactions and style both matter.","These are baboons, not invented human managers or two guaranteed mortality outcomes."),
             case([78],"Recognizing the threatening intonation too late","author illustration and animal mechanisms",["интонаци"],"The author's example involves a trauma-related intonation; neural threat processing can precede explicit recognition.","Autonomic alarm and coherent conscious recollection need not match.","The generic illustration is not recast as a newly documented individual case or one diagnostic biomarker."),
             case([79],"Type A's failed broad replication and hostility refinement","book-era human evidence",["Фридман"],"A broad hurried/competitive bundle is contrasted with narrower component analyses and different provocation tasks.","Hostility and social threat interpretation need not mean ambition or working quickly.","Disagreement about underlying insecurity remains; no personality-to-disease certainty."),
             case([80],"Suppressed expression and repressive style","reported human studies and alternative explanations",["Гросс","репрессор","репрессив"],"Emotional-film expression suppression and low-reported-anxiety/high-arousal participants probe different aspects of apparent calm.","Outward expression and internal autonomic cost can diverge.","Social desirability and measurement alternatives remain; calm conscientious people are not assigned a hidden illness.")],
         omissions="The upholstery-discovery joke is not converted into a literal instant discovery. Most personality scales and psychogenic-miscarriage speculation are omitted; circular blame remains rejected."),
    dict(chapter=16, label="Enjoyable challenge, reward and addiction",
         argument="Bounded voluntary uncertainty can be enjoyable, while prolonged involuntary threat is different. Anticipation and effort can diverge from pleasure, especially when addiction shifts behavior toward avoiding distress.",
         mechanisms=["Ventral tegmental–accumbens pathways participate in anticipation and motivated work, not all pleasure.", "Cue learning and uncertain delivery alter dopaminergic activity.", "Tolerance/opponent adaptation and withdrawal change the goal toward relief; stress, cues and context can reinstate seeking."],
         cases=[
             case([81],"Piazza and Le Moal's glucocorticoid self-administration","reported animal experiments",["Пьяцца"],"Rats work a lever for glucocorticoid injections; amount and duration affect reward-path dopamine.","Moderate brief elevation can enhance dopamine activity, whereas the author contrasts prolonged strong exposure with dopamine reduction and dysphoria.","The book-era animal finding is not a human stimulant recommendation or a claim that all dopamine pathways behave identically."),
             case([82],"Blakemore's tickling machine","reported human experiment",["Блейкмор","Блэйкмор","Блэкмор"],"A device changes the timing or direction of self-generated touch.","Unexpected sensory consequences make otherwise predictable self-touch more ticklish.","The bounded safe setup is not equivalent to real chronic danger."),
             case([83],"Schultz's cue, lever sequence and reward","reported animal experiments",["Шульц"],"After learning, animals respond to a cue and perform an action sequence before reward, sometimes with uncertain delivery.","Activation moves toward anticipation and effort rather than remaining only at consumption.","Dopamine is not equated with a complete measure of pleasure."),
             case([84,85],"Self-administration, extinction and reinstatement","reported animal models",["физраствор","солев","возобнов"],"A previously reinforced lever stops delivering drug; context, a prime or stress later restores seeking.","Visible extinction need not erase learned vulnerability; relief from distress differs from initial euphoria.","Early-life vulnerability, immediate arousal and established withdrawal are not one mechanism; human addiction exceeds the model.")],
         omissions="Most sensation-seeking subtype hypotheses and exact reward-magnitude rhetoric are omitted. The Russian thousandfold claim is not promoted to a factual universal effect."),
    dict(chapter=17, label="Hierarchy, socioeconomic gradients and inequality",
         argument="Status affects physiology through particular social arrangements, not an invariant low-rank law. Human gradients require material constraints, autonomy, relative position, cohesion and public investment to be considered together.",
         mechanisms=["Stable versus contested rank and species-specific reproductive roles alter who bears costs.", "Income, education, housing, working conditions and resources are intertwined.", "Subjective status supplements material position; nonlinear individual income–health curves are an alternative to a contextual inequality effect.", "Trust/reciprocity and unequal investment in common services are distinct proposed social pathways."],
         cases=[
             case([86,87],"Subordinate baboons versus costly dominance in other species","comparative field and group evidence",["мангуст","собак","игрун"],"Different species and changing hierarchies allocate reproductive competition, threats and escape options differently.","Rank's endocrine meaning depends on ecology and actual interactions.","No biological formula for every human hierarchy."),
             case([88,90],"Whitehall and the gradient above destitution","reported human observational program",["Уайтхолл","Whitehall","Мармот"],"British civil servants are compared across occupational grades with relatively shared medical access.","A graded relation extends beyond hunger versus sufficiency; access and measured habits do not exhaust the book's explanation.","An unexplained remainder is not automatically a pure cortisol effect; selection and confounding remain."),
             case([89],"Diuretics and unavailable toilet breaks","author's concrete social/clinical example",["мочегон"],"Low-paid workers have medication but lack enough permission to use a toilet during work.","Formal access fails to remove an organizational obstacle to adherence.","The example explains constraints rather than prescribing or changing medication."),
             case([91,92,93],"Adler's ladder, Wilkinson's inequality comparison and nonlinear averaging","reported studies and analytical objection",["Адлер","Уилкинсон"],"Perceived position, societies with similar means and different distributions, and curved income–health relations are compared.","Relative status and distribution raise questions beyond individual income.","Ecological associations do not establish all individual or contextual causal pathways; arithmetic can explain part of an apparent relation."),
             case([94,95],"Kawachi's social capital and the public-services alternative","competing social hypotheses",["Кавачи","Линч","Эванс"],"Trust/reciprocity and unequal reliance on public systems offer different routes from distribution to health.","The author expands the problem to social resources and who can buy private substitutes.","Neither route is a completed randomized proof; cohesion can also constrain outsiders.")],
         omissions="Historical country rankings, every SES dataset and exact regression shares are omitted. No new claim that meditation or a mindset change cures poverty substitutes for the social argument."),
    dict(chapter=18, label="Preserved function, available control and flexible coping",
         argument="Variation in aging and coping leaves room for change, but no one method fits every situation. Control, support and action help through real conditions; their loss or misapplication can reverse a short-term benefit.",
         mechanisms=["Preserved-function subgroups challenge an inevitable cascade.", "Control of manageable procedures differs from responsibility for an impossible outcome.", "Benefits during an activity, after it and over a clinical follow-up are distinct; choice and selection matter.", "Problem-focused action before an outcome and reappraisal after an irreversible event require different strategies."],
         cases=[
             case([96],"Meaney's preserved-memory old rats and separate early-care findings","reported animal research",["Мини"],"Old rats are separated by memory performance; early handling and natural maternal-care findings are described separately.","Not every animal follows the entire cascade; early conditions can be associated with favorable later regulation.","No invented claim that separation causes extra reunion care that in turn causes the aging benefit."),
             case([97],"Vaillant's selected healthy Harvard men","reported longitudinal observational cohort",["Вайлант"],"Two hundred selected healthy male students are followed; later outcomes are related to pre-fifty characteristics.","Successful aging is real and heterogeneous, with potentially informative correlates.","Selection, the origins of optimism/relationships and adversity-related confounding prevent a guaranteed recipe."),
             case([98,99],"Nursing-home choices, student visits and their withdrawal","reported interventions",["посещени","комнатные растения"],"Residents receive decisions or predictable/self-scheduled visits; study support later ends.","Modest usable control can improve experience; abrupt loss can leave people worse than at baseline.","An intervention includes its ending; not power over aging itself."),
             case([98],"Patient-controlled analgesia","reported clinical organization",["анальгези","обезболива"],"A clinically controlled delivery system changes access to relief.","Availability of limited action can change helplessness and demand.","Not unmonitored personal dosing or unrestricted drug supply."),
             case([99],"Parents during remission and after relapse","reported human observations",["ремисси"],"Current endocrine burden is compared across coping styles and later recurrence.","A style relieving the present may have a different cost when circumstances change.","Lower hormone now is not a permanently superior personality or a rule to deny medical facts."),
             case([100,101,102,103],"Exercise, meditation, support and religious participation","author's differentiated evidence discussion",["медитац","Торесен","Слоан"],"Voluntary activity, in-session relaxation, existing social groups and chosen belief communities involve different exposures and selection.","Benefit depends on autonomy, duration, quality and what the practice means in the person's life.","No commercial school's supremacy, required religiosity, universal crowd benefit or present-day treatment standard."),
             case([104,105,106],"John Henry effort, an exam and irreversible loss","reported human concept plus author's explanatory examples",["генриизм","Генри"],"Intense striving under limited opportunity is set beside tasks whose controllability changes with time.","Flexibility and structural resources matter; doubling effort does not always solve the obstacle.","No blame for illness or universal relaxation lesson; the shared ending preserves the social and medical limits.")],
         omissions="The literal 80/20 rhetoric, speculative calm-with-arousal paragraph, most historical exercise schedules and drug details are omitted. The exam and bereavement examples are the author's, not invented coaching exercises."),
]


def anchor(text, needles, end):
    hits = [(text.casefold().find(n.casefold()), n) for n in needles]
    hits = [(p, n) for p, n in hits if 0 <= p < end]
    if not hits:
        return {"scope": "chapter main body", "start": 0, "end": end,
                "preciseNeedleUnresolved": needles}
    position, needle = min(hits)
    start = text.rfind("\n", 0, position) + 1
    finish = text.find("\n", position)
    if finish < 0:
        finish = end
    finish = min(finish, end)
    return {"scope": "containing source paragraph", "needle": needle,
            "start": start, "end": finish, "firstLine": text[:start].count("\n") + 1,
            "lastLine": text[:finish].count("\n") + 1,
            "sha256": hashlib.sha256(text[start:finish].encode()).hexdigest()}


for ch in CHAPTERS:
    number = ch["chapter"]
    file = f"{number + 5:03d}-978544611081-{number + 1}.txt"
    source = next(x for x in LEDGER["files"] if x["file"] == file)
    text = (PRIVATE / file).read_text()
    units = [s for s in DATA["screens"] if s.get("bookLocation", {}).get("chapter") == number]
    ch["source"] = {"file": file, "epubFile": f"OEBPS/Text/978544611081-{number + 1}.xhtml",
                    "sha256": source["sha256"], "mainBodyStart": 0,
                    "mainBodyEnd": source["mainBodyEnd"], "completeMainBodyRead": True}
    ch["screenIds"] = [s["id"] for s in units]
    ch["modeCoverage"] = {m: [s["id"] for s in units if s["level"] <= l]
                          for m, l in [("essential", 1), ("core", 2), ("deep", 3)]}
    for c in ch["cases"]:
        c["screenIds"] = [next(s["id"] for s in units if s["bookLocation"]["draftUnit"] == n)
                          for n in c.pop("units")]
        c["sourceAnchor"] = anchor(text, c.pop("find"), source["mainBodyEnd"])
        if c["name"] in ROOT_ANCHORS:
            anchors = []
            for start, finish in ROOT_ANCHORS[c["name"]]:
                assert 0 <= start < finish <= source["mainBodyEnd"]
                anchors.append({"scope": "root-selected source passage; entry/context, not full-literature certification",
                                "start": start, "end": finish,
                                "firstLine": text[:start].count("\n") + 1,
                                "lastLine": text[:finish].count("\n") + 1,
                                "sha256": hashlib.sha256(text[start:finish].encode()).hexdigest()})
            c["sourceAnchor"] = anchors[0]
            c["sourceAnchors"] = anchors
            c["anchorReview"] = "Corrected after direct personal root reading; all ranges are recorded separately."

payload = {
    "book": DATA["title"], "slug": DATA["slug"],
    "scope": "All 18 complete main chapter bodies plus both prefaces read; notes selective. Map contains original paraphrase and source locations, no extracted primary prose.",
    "rootPersonalAcceptance": False, "publicationAllowed": False,
    "argumentSpine": [
        "Anticipation recruits a protective response; prolonged activity, failed shutoff and deferred repair create costs.",
        "Neural/endocrine communication, receptors and feedback explain how appraisal reaches distinct organs.",
        "Circulation, energy, appetite, gut, development, reproduction and immunity demonstrate different costs and conditions.",
        "Pain, memory, sleep and aging introduce active processing, timing, reciprocal loops and preserved function.",
        "Experiments vary information, outlets and control while holding physical exposure similar.",
        "Depression, temperament and reward explain heterogeneous vulnerability, learned expectations and persistent seeking.",
        "Hierarchy, material resources, inequality and public systems determine who encounters chronic demands and recovery options.",
        "Flexible coping fits actual controllability; individual strategies and changes in social conditions remain necessary at different scales."
    ],
    "chapters": CHAPTERS,
    "criticalDistinctions": [
        {"name": "Rat-care correction", "screens": ["unit-028", "unit-096"], "rule": "Chapter-6 separation/sedated mother/active licking concerns GH. Chapter-18 early handling and natural maternal care are separately reported later-life findings. No invented mediation through reunion care."},
        {"name": "Diabetes distinction", "screens": ["unit-017"], "rule": "Later beta-cell decline in type 2 is not conversion to autoimmune type 1."},
        {"name": "Immune location and timing", "screens": ["unit-038","unit-039","unit-040"], "rule": "Blood redistribution, immune function and clinical cold are distinct endpoints."},
        {"name": "Cancer endpoints", "screens": ["unit-042","unit-043","unit-044"], "rule": "Implanted tumor progression, spontaneous human onset, distress and survival are not interchangeable."},
        {"name": "Brain volume", "screens": ["unit-054","unit-055","unit-062"], "rule": "MRI volume is not a neuron-death count; vulnerability and consequence can coexist."},
        {"name": "Appraisal and control", "screens": ["unit-063","unit-066","unit-068"], "rule": "Physical stress remains real; the changing-shock example is hypothetical; executive-monkey assignment was selected."},
        {"name": "Book-era versus modern", "screens": ["unit-017","unit-022","unit-044","unit-069","unit-076"], "rule": "Only explicitly marked narrow contemporary qualifications; the rest conveys the author's edition-era argument."},
        {"name": "Social scale", "screens": ["unit-089","unit-093","unit-094","unit-095","unit-104"], "rule": "Material constraints and competing inequality pathways survive; no generic calm-down solution replaces them."},
    ],
    "meaningfulLimits": [
        "Whole main-text reading does not imply all notes or every cited scientific article were read.",
        "English is an original translation of this condensation, not collation with the published English book.",
        "Many supporting studies and humor, figures, bibliographic notes and historical numerical detail are omitted.",
        "No claim of present clinical consensus, independent scientific replication or root's editorial acceptance."
    ],
}
assert len(CHAPTERS) == 18
assert sum(len(c["screenIds"]) for c in CHAPTERS) == len(DATA["screens"]) - 1
(ROOT / "coverage-map.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
lines = ["# Whole-book chapter, argument and case map", "", payload["scope"], "",
         "Root personal acceptance: pending. Publication: prohibited for this candidate.", "",
         "## Causal spine", ""]
lines += [f"{i}. {s}" for i, s in enumerate(payload["argumentSpine"], 1)]
lines += ["", "## Chapter coverage", "", "All chapter locations refer to the private user-owned RU edition; offsets are zero-based Unicode characters, end-exclusive. Anchors locate entry paragraphs for rereading; the surrounding discussion may be needed for the entire comparison. No print page numbers are asserted.", ""]
for ch in CHAPTERS:
    src = ch["source"]
    lines += [f"### {ch['chapter']}. {ch['label']}", "", ch["argument"], "",
              f"Primary: `{src['file']}`, main body `[0,{src['mainBodyEnd']})`, SHA-256 `{src['sha256']}`. Full body read.", "",
              "Mechanisms: " + " ".join(ch["mechanisms"]), "",
              "Screens: " + ", ".join(f"`{x}`" for x in ch["screenIds"]) + ".", "",
              "| Retained case / kind | Setup and result | Limits | Screens / source location |",
              "|---|---|---|---|"]
    for c in ch["cases"]:
        a=c["sourceAnchor"]
        loc="; ".join(f"chars [{x['start']},{x['end']})" for x in c.get("sourceAnchors", [a]))
        if "preciseNeedleUnresolved" in a:
            loc+="; chapter-wide location, precise anchor unresolved"
        lines.append(f"| {c['name']} — {c['kind']} | {c['setup']} {c['resultOrFunction']} | {c['qualification']} | {', '.join(c['screenIds'])}; {loc} |")
    lines += ["", "Deliberate omissions: " + ch["omissions"], ""]
lines += ["## Critical distinctions", ""]
lines += [f"- **{c['name']}** ({', '.join(c['screens'])}): {c['rule']}" for c in payload["criticalDistinctions"]]
lines += ["", "## Reading limits", ""] + ["- " + x for x in payload["meaningfulLimits"]]
(ROOT / "coverage-map.md").write_text("\n".join(lines).rstrip() + "\n")
unresolved=[{"chapter":ch["chapter"],"case":c["name"],"needles":c["sourceAnchor"]["preciseNeedleUnresolved"]}
            for ch in CHAPTERS for c in ch["cases"] if "preciseNeedleUnresolved" in c["sourceAnchor"]]
print(json.dumps({"chapters":len(CHAPTERS),"mappedScreens":sum(len(c["screenIds"]) for c in CHAPTERS),
                  "retainedCaseRecords":sum(len(c["cases"]) for c in CHAPTERS),"unresolvedAnchors":unresolved},ensure_ascii=False,indent=2))
