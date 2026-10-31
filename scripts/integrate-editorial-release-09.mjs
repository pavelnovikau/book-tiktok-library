// Reproduce root integration from the nine immutable, sealed source snapshots.
// Run from repository root, before sync:readers and the prepared metadata helper.
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const audit = 'editorial-audit/2026-10-31';
const findings = `${audit}/publisher-findings`;
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const sha = p => hash(fs.readFileSync(p));
const queue = json(`${findings}/parent-release09-queue.json`);
const seal = json(`${findings}/release-09-intake-seal.json`);
assert.equal(sha(`${findings}/parent-release09-queue.json`), seal.queueSha256);
assert.equal(queue.candidates.length, 9);
const catalogue = json('books.json');
const definitions = {
  dune: { author: {ru:'Фрэнк Герберт',en:'Frank Herbert'}, genres:['science-fiction','adventure'], tags:['science-fiction','environment','power','adventure'], motif:'desert-cycle',tone:'orange',mark:'ARRAKIS' },
  'the-potent-self': { subjects:['health-body','psychology-relationships'],tags:['somatics','movement','learning','body-awareness'],motif:'unforced-motion',tone:'cyan',mark:'ACTION' },
  solaris: { genres:['science-fiction'],tags:['science-fiction','memory','uncertainty','identity'],motif:'ocean-station',tone:'blue',mark:'OCEAN' },
  'flowers-for-algernon': { genres:['science-fiction','life-people'],tags:['science-fiction','memory','identity','care'],motif:'maze-trace',tone:'green',mark:'CHARLIE' },
  'the-neverending-story': { author:{ru:'Михаэль Энде',en:'Michael Ende'}, genres:['fantasy','adventure'],tags:['fantasy','adventure','identity','home'],motif:'twin-serpents',tone:'magenta',mark:'FANTASTICA' }
};
const storyTags = {
  'i-robot':['science-fiction','uncertainty','trust','care'],
  'the-wee-free-men':['fantasy','adventure','coming-of-age','care'],
  'the-hitchhikers-guide-to-the-galaxy':['science-fiction','adventure','uncertainty']
};
const entries = [];
for (const input of queue.candidates) {
  const {slug} = input;
  for (const key of ['ready','review','originalReview','closure']) if(input[key]) assert.equal(sha(input[key]),input[key+'Sha256'], input[key]);
  const path = `collector-output/${slug}`;
  const source = json(`${path}/story-data.json`);
  const raw = fs.readFileSync(`${path}/${slug}.html`, 'utf8');
  const data = JSON.parse(raw.match(/<script id="book-tiktok-data" type="application\/json">\s*([\s\S]*?)<\/script>/)[1]);
  for(const [key,value] of Object.entries(source)) if(!['media','modes'].includes(key)) assert.deepEqual(data[key],value,slug+'/'+key);
  const counts = Object.fromEntries([['essential',1],['core',2],['deep',3]].map(([m,l])=>[m,data.screens.filter(s=>s.level<=l).length]));
  if(input.counts) assert.deepEqual(counts,input.counts);
  if(source.targetModes) assert.deepEqual(counts,source.targetModes);
  const minutes = Object.fromEntries(['ru','en'].map(lang=>[lang,Object.fromEntries(Object.entries(data.modes).map(([m,v])=>[m,Number.parseInt(v.minutes[lang])]))]));
  if(input.review) {
    const review=json(input.review); assert.equal(review.verdict,'PASS');
    assert(JSON.stringify(review).includes(sha(`${path}/story-data.json`)));
    assert(JSON.stringify(review).includes(sha(`${path}/${slug}.html`)));
  }
  if(input.kind!=='metadata-only-correction') {
    let html = raw;
    // Existing book-local guards remain untouched. Unknown/cover IDs have no
    // valid reading destination; preserve language and return to Essential.
    const state = /      const state = \{[\s\S]*?\n      \};/;
    assert.equal((html.match(new RegExp(state.source,'g'))||[]).length,1);
    html=html.replace(state, block=>`      const release09SavedId = stored('lastScreen', '');\n      const release09InvalidSavedId = Boolean(release09SavedId && !data.screens.some(screen => screen.id === release09SavedId && screen.type !== 'cover'));\n      if (release09InvalidSavedId) removeStored('lastScreen');\n\n${block}\n      if (release09InvalidSavedId) { state.mode = 'essential'; save('mode', state.mode); }`);
    fs.writeFileSync(`${slug}.html`,html);
  }
  let book=catalogue.books.find(b=>b.slug===slug);
  if(!book) {
    const d=definitions[slug];assert(d,slug);const fiction=Boolean(d.genres);
    book={slug,file:slug+'.html',workTypes:[fiction?'fiction':'nonfiction'],genres:d.genres||[],subjects:d.subjects||[],section:fiction?'fiction-adventure':'body-mind',tags:d.tags,collections:[],audience:source.audience||'general',author:source.author||d.author,cover:{type:'typographic',mark:d.mark,motif:d.motif,tone:d.tone}};
    // Use the catalogue's existing health/body legacy section.
    if(!fiction) book.section='health-protocols';
    assert(catalogue.sections.some(s=>s.id===book.section),book.section);
    catalogue.books.push(book);
  }
  if(input.kind!=='metadata-only-correction') {
    Object.assign(book,{title:source.title,description:source.description,screenCount:counts.deep,readingMinutes:minutes.ru,spoilerPolicy:source.spoilerPolicy});
    if(storyTags[slug]) book.tags=storyTags[slug];
    if(slug==='the-wee-free-men') book.cover.mark='CHALK';
  }
  entries.push({...input,counts,reviewPath:input.review||input.originalReview,readyPath:input.ready,parentClosure:input.closure,originalVerdict:input.review?json(input.review).verdict:input.originalReview?json(input.originalReview).verdict:'metadata-only',decision:input.review?'accepted-matching-independent-PASS':input.kind==='metadata-only-correction'?'accepted-bounded-metadata-correction':'accepted-bounded-publisher-closure',sourceJsonSha256:sha(`${path}/story-data.json`),sourceHtmlSha256:sha(`${path}/${slug}.html`),sourceCount:data.sources.length,sourceScope:data.methodNote,contentMode:data.contentMode,readingMinutesByLanguage:minutes,checkedScreens:input.closure?(json(input.closure).changedScreens||[]):[]});
}
fs.writeFileSync('books.json',JSON.stringify(catalogue,null,2)+'\n');
assert.equal(catalogue.books.length,58); assert.equal(catalogue.books.reduce((n,b)=>n+b.screenCount,0),2188);
const receipt={release:'09',state:'sealed-integration-in-progress',baseMain:queue.expectedBaseMain,sealedAt:seal.atUtc,acceptedCandidates:entries,mainReaders:8,acceptedPairs:entries.filter(e=>e.kind!=='metadata-only-correction').reduce((n,e)=>n+e.counts.deep,0),metadataOnlyPairsUnchanged:27,catalogueBooks:58,catalogueScreens:2188,publicAllowlistAssets:69,productionVerified:false,excluded:['mans-search-for-meaning','ubik','the-martian-chronicles','the-two-captains','moondust'],limits:['Exact retained passages and identified guides only; no whole-edition or published-Russian-translation certificate.','All original independent verdicts and parent/root snapshots remain immutable.','No physical iPhone/Safari/PWA certificate.']};
assert.equal(receipt.acceptedPairs,286);
fs.writeFileSync(`${findings}/release-09.json`,JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({books:58,screens:2188,mainReaders:8,mainPairs:286,metadataOnly:27}));
