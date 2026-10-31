// Bounded integration checks. They exercise public reader controls and the
// existing book-local guards, without substituting consent implementations.
import fs from 'node:fs';
import path from 'node:path';
export async function runRelease09QA({phase,books,navigate,evaluate,command,assert,catalogue,outputDir}) {
  const checks=[];
  const dialogSelector='dialog[open]:not(#settingsDialog):not(#contentsDialog):not(#sourcesDialog)';
  const acceptSelector='#duneSpoilerAccept,#deepConfirm,#spoilerAccept,#solarisSpoilerAccept,[data-ending-accept],#deepConsentAccept,#weeSpoilerAccept,[data-spoiler-accept],#endingAccept';
  const cancelSelector='#duneSpoilerCancel,#deepCancel,#spoilerCancel,#solarisSpoilerCancel,[data-ending-cancel],#deepConsentCancel,#weeSpoilerCancel,[data-spoiler-cancel],#endingCancel';
  async function decide(accept) {
    const id=await evaluate(`(()=>{const d=document.querySelector(${JSON.stringify(dialogSelector)});if(!d)throw Error('No actual consent dialog');const c=d.querySelector('input[type=checkbox]');if(${accept}&&c&&!c.checked)c.click();const b=d.querySelector(${JSON.stringify(accept?acceptSelector:cancelSelector)});if(!b||b.disabled)throw Error('Missing/enabled consent action');const id=d.id;b.click();return id;})()`);
    await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))');
    return id;
  }
  async function open(book) { await navigate(book,"document.querySelector('[data-start]')"); }
  if(phase==='release09-guards') {
    for(const book of books) {
      const slug=book.slice(0,-5), record=catalogue.books.find(b=>b.slug===slug);
      if(record.spoilerPolicy!=='full-plot-in-deep') continue;
      for(const language of ['ru','en']) {
        await open(book);
        const late=await evaluate(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),s=d.screens.find(s=>s.level===3);localStorage.setItem('book-tiktok.${slug}.language','${language}');localStorage.setItem('book-tiktok.${slug}.mode','deep');localStorage.setItem('book-tiktok.${slug}.lastScreen',s.id);return {id:s.id,title:s.copy['${language}'].title};})()`);
        await open(book);
        assert(await evaluate(`!!document.querySelector('[data-mode=essential][aria-pressed=true]')&&!document.body.innerText.includes(${JSON.stringify(late.title)})`),`${slug}/${language}: saved ending hidden`);
        await evaluate("document.querySelector('[data-start=continue]').click()");
        if(slug==='i-robot') assert(await evaluate("deepConfirm.disabled&&!deepAcknowledgment.checked"),'I Robot explicit unchecked acknowledgment');
        const modal=await decide(false);
        assert(await evaluate("!!document.querySelector('.cover-layout')&&!document.querySelector('[data-mode=deep][aria-pressed=true]')"),'cancel kept shallow cover');
        await evaluate("document.querySelector('[data-start=continue]').click()");
        await command('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
        await command('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
        assert(await evaluate(`!document.querySelector(${JSON.stringify(dialogSelector)})&&!document.querySelector('[data-mode=deep][aria-pressed=true]')`),'native Escape kept shallow state');
        await evaluate("document.querySelector('[data-start=continue]').click()");await decide(true);
        assert(await evaluate(`document.querySelector('#story h1').textContent===${JSON.stringify(late.title)}`),'saved Deep restored exact target');
        // A consented late ID must again be guarded after *each* shallower depth.
        for(const mode of ['core','essential']) {
          await evaluate(`document.querySelector('[data-mode=${mode}]').click();(document.querySelector('[data-start=continue]')||document.querySelector('[data-mode=deep]')).click()`);
          assert(await evaluate(`!!document.querySelector(${JSON.stringify(dialogSelector)})&&!document.querySelector('[data-mode=deep][aria-pressed=true]')`),`${slug}/${language}/${mode}: downgrade revoked consent`);
          await decide(false);
          await evaluate("document.querySelector('[data-mode=deep]').click()");await decide(true);
        }
        await evaluate("document.querySelector('[data-mode=essential]').click();document.querySelector('[data-mode=deep]').click()");
        assert(await evaluate(`!!document.querySelector(${JSON.stringify(dialogSelector)})`),'picker requires renewed consent');await decide(false);
        // Retarget an actually bound Contents control to a normally withheld
        // ID. Newly injected controls have no listener in these readers.
        await evaluate(`(()=>{const button=contentsList.querySelector('[data-go-to]');button.dataset.goTo='${late.id}';button.click();})()`);
        assert(await evaluate(`!!document.querySelector(${JSON.stringify(dialogSelector)})&&!document.querySelector('[data-mode=deep][aria-pressed=true]')`),'hidden ID is guarded');await decide(false);
        await evaluate("document.querySelector('[data-mode=deep]').click()");await decide(true);
        if(slug==='the-neverending-story') {
          const ids=await evaluate("[...contentsList.querySelectorAll('[data-go-to]')].map(n=>n.dataset.goTo)");assert(ids.indexOf('the-price')+1===ids.indexOf('acharis'),'NES Deep warning before Acharis');
        }
        await evaluate(`localStorage.setItem('book-tiktok.${slug}.lastScreen',${JSON.stringify(late.id)});localStorage.setItem('book-tiktok.${slug}.mode','deep')`);
        await open(book);
        assert(await evaluate("!!document.querySelector('[data-mode=essential][aria-pressed=true]')"),'reload revokes');
        await evaluate("document.querySelector('[data-start=continue]').click()");await decide(false);
        checks.push({slug,language,modal,neutralSavedDeep:true,cancel:true,nativeEscape:true,explicitAcknowledgment:slug==='i-robot',resumeExact:true,bothDowngradesRevoke:true,pickerRenews:true,hiddenIdGuard:true,reloadRevokes:true});
      }
    }
  }
  if(phase==='release09-metadata') {
    for(const [slug,id] of [['skin-in-the-game','green-lumber'],['mindfulness','one-minute-return']])for(const language of ['ru','en']) {
      await open(slug+'.html');await evaluate(`localStorage.setItem('book-tiktok.${slug}.language','${language}');localStorage.setItem('book-tiktok.${slug}.mode','essential');localStorage.setItem('book-tiktok.${slug}.lastScreen','${id}')`);await open(slug+'.html');
      const label=await evaluate("document.querySelector('[data-start=continue]').textContent");assert(label.includes(language==='ru'?'Глубоко':'Deep'),`${slug}: destination mode label`);
      assert(await evaluate("!!document.querySelector('[data-mode=essential][aria-pressed=true]')"),'cover remains Essential');
      await evaluate("document.querySelector('[data-start=continue]').click()");
      assert(await evaluate(`localStorage.getItem('book-tiktok.${slug}.mode')==='deep'&&document.querySelector('#story h1').textContent===JSON.parse(document.getElementById('book-tiktok-data').textContent).screens.find(s=>s.id==='${id}').copy['${language}'].title`),'valid target resumes at advertised mode');
      await evaluate(`localStorage.setItem('book-tiktok.${slug}.mode','essential');localStorage.setItem('book-tiktok.${slug}.lastScreen','${id}')`);await open(slug+'.html');await evaluate("document.querySelector('[data-start=begin]').click()");
      assert(await evaluate(`!!document.querySelector('[data-mode=essential][aria-pressed=true]')&&localStorage.getItem('book-tiktok.${slug}.lastScreen')!=='${id}'`),'Start over honors Essential');checks.push({slug,language,label,explicitDestination:true,exactTarget:true,startOverEssential:true});
    }
    await navigate('?q='+encodeURIComponent('Сознавание через движение'),"document.querySelectorAll('.book').length===1");assert(await evaluate("!!document.querySelector('[data-book=awareness-through-movement]')"),'CM02 alias');checks.push({finding:'CM-02',aliasSearch:true});
    await open('the-giver.html');assert(await evaluate("JSON.parse(document.getElementById('book-tiktok-data').textContent).description.en.includes('first novel in Lois Lowry’s Giver Quartet')"),'CM01 reader metadata');checks.push({finding:'CM-01',readerMetadata:true});
    await open('the-potent-self.html');assert(await evaluate("[...document.querySelectorAll('[data-mode=essential]')].every(n=>n.textContent.includes('4 минуты'))"),'TPS generated RU duration');checks.push({finding:'TPS2-L10N-001',derivedLabel:true});
  }
  if(phase==='release09-corrections') {
    for(const [book,id] of [['flowers-for-algernon.html','warren-visit'],['the-wee-free-men.html','eggs-in-the-henhouse']])for(const language of ['ru','en']) {
      await open(book);await evaluate(`if(document.documentElement.lang!=='${language}')languageButton.click();document.querySelector('[data-mode=deep]').click()`);await decide(true);
      const result=await evaluate(`(()=>{contentsList.querySelector('[data-go-to=${id}]').click();const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),s=d.screens.find(s=>s.id==='${id}'),body=document.querySelector('.story-slide').innerHTML;return {title:document.querySelector('#story h1').textContent===s.copy['${language}'].title,body:body.includes(s.copy['${language}'].body),text:document.querySelector('.story-slide').innerText};})()`);
      assert(result.title&&result.body,book+' exact corrected copy');checks.push({book,id,language,...result});
    }
    // Removed and cover IDs must not leave a false Resume or inherit Deep.
    for(const book of books)for(const id of ['cover','not-a-current-screen']) {
      const slug=book.slice(0,-5);await open(book);await evaluate(`localStorage.setItem('book-tiktok.${slug}.lastScreen','${id}');localStorage.setItem('book-tiktok.${slug}.mode','core');localStorage.setItem('book-tiktok.${slug}.language','en')`);await open(book);
      assert(await evaluate(`!localStorage.getItem('book-tiktok.${slug}.lastScreen')&&!document.querySelector('[data-start=continue]')&&!!document.querySelector('[data-mode=essential][aria-pressed=true]')&&document.documentElement.lang==='en'`),`${book}/${id} invalid progress`);checks.push({book,id,safeEssentialCover:true,languagePreserved:true});
    }
    // The old analytical revision must not be mistaken for reviewed prose,
    // even if an old ID happens to collide with a current ID.
    await open('i-robot.html');await evaluate("localStorage.removeItem('book-tiktok.i-robot.narrativeRevision');const d=JSON.parse(document.getElementById('book-tiktok-data').textContent);localStorage.setItem('book-tiktok.i-robot.lastScreen',d.screens.find(s=>s.type!=='cover'&&s.level===1).id);localStorage.setItem('book-tiktok.i-robot.mode','deep')");await open('i-robot.html');assert(await evaluate("!localStorage.getItem('book-tiktok.i-robot.lastScreen')&&!document.querySelector('[data-start=continue]')&&!!document.querySelector('[data-mode=essential][aria-pressed=true]')"),'I Robot old analytical revision invalidated');checks.push({slug:'i-robot',oldAnalyticalRevisionInvalidated:true});
  }
  if(phase==='release09-tail') {
    for(const book of books)for(const [language,theme,width] of [['ru','dark',320],['en','light',320],['ru','light',390],['en','dark',1440]]) {
      await command('Emulation.setDeviceMetricsOverride',{width,height:width===320?568:width===390?844:900,deviceScaleFactor:1,mobile:width<900});
      await open(book);await evaluate(`if(document.documentElement.lang!=='${language}')languageButton.click();BookSettings.set('theme','${theme}');document.querySelector('[data-mode=deep]').click()`);
      if(await evaluate(`!!document.querySelector(${JSON.stringify(dialogSelector)})`))await decide(true);
      const longest=await evaluate(`(()=>{const d=JSON.parse(document.getElementById('book-tiktok-data').textContent),s=d.screens.filter(s=>s.type!=='cover'&&!s.final).sort((a,b)=>b.copy['${language}'].body.length-a.copy['${language}'].body.length)[0];contentsList.querySelector('[data-go-to="'+s.id+'"]').click();return {id:s.id,title:s.copy['${language}'].title};})()`);
      for(const font of ['sans','serif']) {
        await evaluate(`BookSettings.set('readingFont','${font}');document.fonts.ready.then(()=>true)`);await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve(true))))');
        const result=await evaluate(`(()=>{const scroll=document.querySelector('.slide-scroll');scroll.scrollTop=scroll.scrollHeight;const tail=[...scroll.querySelectorAll('p,li,blockquote')].filter(n=>getComputedStyle(n).display!=='none').at(-1);return {overflow:scroll.scrollWidth>scroll.clientWidth+1||document.documentElement.scrollWidth>innerWidth+1,tailReachable:tail.getBoundingClientRect().bottom<=scroll.getBoundingClientRect().bottom+1,sameScreen:document.querySelector('#story h1').textContent===${JSON.stringify(longest.title)}};})()`);
        assert(!result.overflow&&result.tailReachable&&result.sameScreen,`${book}/${language}/${font}/${width} dense tail ${JSON.stringify(result)}`);checks.push({book,language,theme,width,font,id:longest.id,...result});
        if(book==='flowers-for-algernon.html'&&font==='serif') {const shot=await command('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(outputDir,`release09-dense-${language}-${width}.png`),Buffer.from(shot.data,'base64'));}
      }
    }
  }
  return {checks,physicalIPhone:false,scope:'Focused release09 integration controls; immutable independent literary reviews remain separate.'};
}
