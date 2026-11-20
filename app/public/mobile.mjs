import {siteUrl,siteMarkup,routePath} from './paths.mjs';
// Authored mobile UI. The desktop branch adds no nodes, classes or styles.
const mobileViewport=matchMedia('(max-width: 1199px)');
let teardown;
let mediaData,tabletData,contentData,headingData;
const phoneIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><rect x="8" y="2" width="14" height="26" rx="3"/><path d="M12 5h6M14 24h2"/></svg>';
const arrowIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><path d="M3 15h24M19 7l8 8-8 8"/></svg>';
const brandMarkup=()=>'<a class="mobile-brand" href="/" aria-label="BHR homepage"><img src="/assets/images/bhr-brand-white.svg" alt="BHR"><span>Your system<br><span class="mobile-brand-integrator">inte<span class="accent">great</span>or</span></span></a>';
function enhanceMobile(){
 const body=document.body,original=document.querySelector('.site-header'),cleanup=[];
 if(!original)return()=>{};
 const simple=original.classList.contains('simple-header');
 const header=document.createElement('header');header.className='mobile-header'+(simple?' mobile-simple-header':'');
 const phone=`<a class="mobile-circle mobile-phone" href="tel:+31162238834" aria-label="Bel BHR">${phoneIcon}</a>`;
 const toggle='<button type="button" class="mobile-circle mobile-menu-icon" data-mobile-open aria-label="Menu openen" aria-controls="mobile-navigation" aria-expanded="false"><span></span><span class="visually-hidden">Menu</span></button>';
 header.innerHTML=siteMarkup(`<div class="mobile-header-inner">${simple?`<button type="button" data-mobile-back-link data-history-back class="mobile-back-link" aria-label="Terug">${arrowIcon}<span>Terug</span></button>`:''}${brandMarkup()}<div class="mobile-header-actions">${phone}${simple?'':'<a class="mobile-circle mobile-search" href="/zoeken" aria-label="Zoeken"><svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="m18 18 9 9"/></svg></a>'+toggle+'<a class="mobile-tablet-appointment" href="/afspraak-maken">Afspraak maken</a>'}</div></div>`);
 let drawer,opener,arrangePanels,isOpen=false,storedY=0,savedBody,active=true;
 const previousRoute=body.getAttribute('data-mobile-route');body.dataset.mobileRoute=routePath(location.pathname);
 const phoneViewport=matchMedia('(max-width: 767px)'),changedImages=new Map();
 let phoneGeneration=0;
 const phoneNodes=[],phoneRestorers=[];
 const clearPhoneContent=()=>{phoneNodes.splice(0).forEach(n=>n.remove());phoneRestorers.splice(0).reverse().forEach(fn=>fn());body.classList.remove('mobile-legacy-content')};
 const restoreImages=()=>{for(const [image,src]of changedImages)image.setAttribute('src',src);changedImages.clear()};
 const applyDeviceMedia=async()=>{
  const generation=++phoneGeneration,phone=phoneViewport.matches;
  restoreImages();if(!phone)clearPhoneContent();
  try{
   if(phone)mediaData??=fetch(siteUrl('/mobile-data.json'),{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{mediaData=null;return {}});
   else tabletData??=fetch(siteUrl('/tablet-data.json'),{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{tabletData=null;return {}});
   const data=await(phone?mediaData:tabletData);if(generation!==phoneGeneration||!active||phone!==phoneViewport.matches||!body.classList.contains('mobile-ready'))return;
   const rows=data[routePath(location.pathname)]||[];
   await Promise.all([...document.images].map(async image=>{
    const src=image.getAttribute('src'),row=rows.find(r=>r.from===src&&r.alt===image.alt);if(!row)return;
    const loaded=await new Promise(resolve=>{const probe=new Image();probe.onload=()=>resolve(probe.naturalWidth>0);probe.onerror=()=>resolve(false);probe.src=row.to});
    if(!loaded||generation!==phoneGeneration||!active||phone!==phoneViewport.matches||image.getAttribute('src')!==src)return;
    if(!changedImages.has(image))changedImages.set(image,src);image.src=row.to;
   }));
   if(phone)applyPhoneContent(generation);
  }catch{}
 };
 const applyPhoneContent=async(generation)=>{
  if(!active||!phoneViewport.matches)return;
  clearPhoneContent();
  const add=(parent,node)=>{parent?.append(node);phoneNodes.push(node)};
  document.querySelectorAll('.parity-projects,.projects-section').forEach(section=>{
   const original=section.querySelector('.parity-section-title>.inline-link,.section-heading>.inline-link'),grid=section.querySelector('.parity-project-grid,.project-grid');
   if(original&&grid){const clone=original.cloneNode(true);clone.classList.add('mobile-project-more');add(grid.parentElement,clone)}
  });
  const expertise=document.querySelector('.home .expertise-section'),expertiseLink=expertise?.querySelector('.section-heading>.inline-link');if(expertiseLink){const clone=expertiseLink.cloneNode(true);clone.classList.add('mobile-expertise-more');add(expertise.querySelector('.service-grid').parentElement,clone)}
  try{
   headingData??=fetch(siteUrl('/mobile-headings.json'),{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{headingData=null;return {}});
   const records=(await headingData)[body.dataset.mobileRoute]||[];if(generation!==phoneGeneration||!active||!phoneViewport.matches)return;
   const normalize=text=>text.replace(/\s+/g,' ').trim();
   for(const heading of document.querySelectorAll('#page-content h1,#page-content h2,#page-content h3,#page-content h4')){
    const record=records.find(r=>normalize(r.text)===normalize(heading.innerText));if(!record)continue;
    const original=[...heading.childNodes];heading.replaceChildren(...original.map(n=>n.cloneNode(true)));heading.querySelectorAll('br').forEach(br=>br.replaceWith(document.createTextNode(' ')));
    const full=heading.textContent,words=[...full.matchAll(/\S+/g)],breaks=[];let count=0;
    for(const part of record.parts.slice(0,-1)){count+=part.match(/\S+/g)?.length||0;if(words[count-1])breaks.push(words[count-1].index+words[count-1][0].length)}
    for(const offset of breaks.reverse()){
     const walker=document.createTreeWalker(heading,NodeFilter.SHOW_TEXT);let node,total=0;
     while(node=walker.nextNode()){if(total+node.length>=offset){const range=document.createRange();range.setStart(node,offset-total);range.collapse(true);range.insertNode(document.createElement('br'));break}total+=node.length}
    }
    phoneRestorers.push(()=>heading.replaceChildren(...original));
   }
  }catch{}
  if(!document.querySelector('.branch-section'))return;
  try{
   contentData??=fetch(siteUrl('/mobile-content.json'),{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{contentData=null;return {}});
   const record=(await contentData)[body.dataset.mobileRoute];if(!record||generation!==phoneGeneration||!active||!phoneViewport.matches)return;
   const section=document.querySelector('.branch-section'),grid=section.querySelector('.branch-grid');if(!grid)return;
   const element=(tag,cls,text)=>{const e=document.createElement(tag);e.className=cls;if(text)e.textContent=text;return e};
   const window=element('div','mobile-branch-window');window.tabIndex=0;window.setAttribute('aria-label','Branches');const track=element('div','mobile-branch-track');window.append(track);
   for(const item of record.branches){const article=element('article',''),a=element('a','');a.href=item.href;const im=element('img','');im.src=item.image;im.alt=item.title;a.append(im);const h=element('h3',''),title=element('a','',item.title);title.href=item.href;h.append(title);const more=element('a','button outline','Afspraak maken');more.href=item.href;article.append(a,h,more);track.append(article)}
   add(grid.parentElement,window);const controls=element('nav','mobile-branch-controls');controls.setAttribute('aria-label','Branches bladeren');
   for(const [label,direction]of [['Vorige branche',-1],['Volgende branche',1]]){const button=element('button','',direction<0?'←':'→');button.type='button';button.setAttribute('aria-label',label);button.addEventListener('click',()=>window.scrollBy({left:direction*(window.clientWidth+20)/1.2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));controls.append(button)}add(grid.parentElement,controls);
   if(record.region){const r=record.region,region=element('section','mobile-region');const container=element('div','container'),eye=element('div','eyebrow',r.eyebrow),h=element('h2','',r.title),p=element('p','',r.intro),list=element('ul','check-list');for(const text of r.locations)list.append(element('li','',text));const cta=element('a','button',r.cta);cta.href=r.href;const im=element('img','');im.src=r.image;im.alt='Werkgebied BHR in Zuid-Nederland';container.append(eye,h,p,list,cta,im);region.append(container);const why=[...document.querySelectorAll('.article-section')].find(e=>e.querySelector('h2')?.textContent.startsWith('Waarom kiezen'))||document.querySelector('.quote-section');why?.before(region);phoneNodes.push(region)}
   const wizard=document.querySelector('.quote-section .wizard');if(record.quoteTitle&&wizard){const title=element('h3','mobile-quote-title',record.quoteTitle);wizard.prepend(title);phoneNodes.push(title);if(record.quoteIntro){const intro=element('p','mobile-quote-intro',record.quoteIntro);title.after(intro);phoneNodes.push(intro)}}
   const lead=document.querySelector('.page-lead');if(record.lead&&lead){const parent=lead.querySelector('.container'),original=[...parent.childNodes],title=element('h2','',record.lead.title),p=element('p','',record.lead.text);parent.replaceChildren(title,p);phoneRestorers.push(()=>parent.replaceChildren(...original))}
   body.classList.add('mobile-legacy-content');
  }catch{}
 };
 const restoreScroll=()=>{
  if(!savedBody)return;
  for(const [key,value]of Object.entries(savedBody))body.style[key]=value;
  savedBody=null;scrollTo(0,storedY);
 };
 const showPanel=(name='root')=>{
  if(!drawer)return;
  const tablet=innerWidth>=768;if(tablet&&name===drawer.dataset.panel&&name!=='root')name='root';
  drawer.querySelectorAll('[data-mobile-panel]').forEach(p=>p.hidden=tablet&&p.dataset.mobilePanel==='root'?false:p.dataset.mobilePanel!==name);
  drawer.querySelectorAll('[data-mobile-submenu]').forEach(button=>button.setAttribute('aria-expanded',String(button.dataset.mobileSubmenu===name)));
  drawer.querySelector('[data-mobile-back]').hidden=name==='root';
  drawer.querySelector('.mobile-submenu-title').hidden=name==='root';
  drawer.querySelector('.mobile-submenu-title').textContent=name==='about'?'Over BHR':name==='industries'?'Industrieën':'';
  drawer.dataset.panel=name;
  if(name!=='root'&&!tablet)drawer.querySelector('[data-mobile-back]').focus({preventScroll:true});
 };
 const close=()=>{
  if(!isOpen)return;isOpen=false;drawer.close();opener?.setAttribute('aria-expanded','false');restoreScroll();opener?.focus({preventScroll:true});
 };
 if(!simple){
  drawer=document.createElement('dialog');drawer.className='mobile-drawer';drawer.id='mobile-navigation';drawer.setAttribute('aria-label','Hoofdnavigatie');
  const social=document.querySelector('.social-links')?.innerHTML||'';
  drawer.innerHTML=siteMarkup(`<div class="mobile-drawer-inner"><div class="mobile-drawer-top">${brandMarkup()}<div class="mobile-header-actions">${phone}<button type="button" class="mobile-circle mobile-close-icon" data-mobile-close aria-label="Menu sluiten"><span></span></button></div></div><nav class="mobile-drawer-nav" aria-label="Mobiele hoofdnavigatie"><button type="button" class="mobile-back" data-mobile-back hidden aria-label="Terug naar hoofdmenu">${arrowIcon}</button><h2 class="mobile-submenu-title" hidden></h2><div data-mobile-panel="root"><a href="/">Home</a><a href="/expertises">Onze expertises</a><button type="button" data-mobile-submenu="industries">Industrieën<span>${arrowIcon}</span></button><button type="button" data-mobile-submenu="about">Over BHR<span>${arrowIcon}</span></button><a href="/service-en-onderhoud">Service en onderhoud</a><a href="/projecten">Projecten</a><a href="/contact">Contact</a></div><div data-mobile-panel="industries" hidden><a href="/voor-machinebouwers/voor-machinebouwers">Voor machinebouwers</a><a href="/voor-machinebouwers/proces-productie">Voor proces en productie</a></div><div data-mobile-panel="about" hidden><a href="/over-ons/partners">Partners</a><a href="/over-ons/werken-bij">Werken bij</a></div><nav class="mobile-drawer-aux" aria-label="Meer over BHR"><a href="/over-ons/werken-bij">Werken bij</a><a href="/nieuws">Blogs</a></nav></nav><div class="mobile-drawer-bottom"><a class="mobile-appointment" href="/afspraak-maken">Afspraak maken</a><nav class="mobile-socials" aria-label="Sociale media">${social}</nav></div></div>`);
  arrangePanels=()=>{
   const nav=drawer.querySelector('.mobile-drawer-nav');
   for(const name of ['industries','about']){const panel=drawer.querySelector(`[data-mobile-panel="${name}"]`);if(innerWidth>=768)drawer.querySelector(`[data-mobile-submenu="${name}"]`).after(panel);else nav.insertBefore(panel,drawer.querySelector('.mobile-drawer-aux'))}
   showPanel();if(isOpen)drawer.querySelector('[data-mobile-close]').focus({preventScroll:true});
  };
  arrangePanels();phoneViewport.addEventListener('change',arrangePanels);
  body.append(drawer);opener=header.querySelector('[data-mobile-open]');
  drawer.querySelectorAll('.mobile-socials a').forEach((a,i)=>{a.replaceChildren(Object.assign(document.createElement('img'),{src:siteUrl(`/assets/images/${['facebook','linkedin','instagram'][i]}.svg`),alt:''}))});
  opener.addEventListener('click',()=>{
   if(isOpen){close();return;}storedY=scrollY;savedBody=Object.fromEntries(['overflow','position','top','width'].map(k=>[k,body.style[k]]));
   body.style.overflow='hidden';body.style.position='fixed';body.style.top=`${-storedY}px`;body.style.width='100%';
   showPanel();drawer.showModal();isOpen=true;opener.setAttribute('aria-expanded','true');drawer.querySelector('[data-mobile-close]').focus({preventScroll:true});
  });
  drawer.addEventListener('cancel',e=>{e.preventDefault();close()});
  drawer.addEventListener('keydown',e=>{
   if(e.key!=='Tab')return;
   const focusable=[...drawer.querySelectorAll('a[href],button:not([disabled]),[tabindex="0"]')].filter(el=>el.getClientRects().length&&!el.closest('[hidden]'));
   const first=focusable[0],last=focusable.at(-1);
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus()}
   else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}
  });
  drawer.addEventListener('click',e=>{
   if(e.target===drawer||e.target.closest('[data-mobile-close]')){close();return;}
   const next=e.target.closest('[data-mobile-submenu]');if(next){showPanel(next.dataset.mobileSubmenu);return;}
   if(e.target.closest('[data-mobile-back]')){const panel=drawer.dataset.panel;showPanel();drawer.querySelector(`[data-mobile-submenu="${panel}"]`)?.focus({preventScroll:true});}
   if(e.target.closest('a[href]'))close();
  });
 }
 const footerLogo=document.querySelector('.footer-logo .brand img'),footerLogoSource=footerLogo?.getAttribute('src');
 if(footerLogo)footerLogo.src=siteUrl('/assets/images/bhr-brand-white.svg');
 const footerSocial=document.querySelector('.site-footer>.container>.social-links')?.cloneNode(true);
 if(footerSocial){
  footerSocial.classList.add('mobile-footer-socials');
  footerSocial.querySelectorAll('a').forEach((a,i)=>a.replaceChildren(Object.assign(document.createElement('img'),{src:siteUrl(`/assets/images/${['facebook','linkedin','instagram'][i]}.svg`),alt:''})));
  document.querySelector('.footer-info')?.append(footerSocial);
 }
 const skip=body.querySelector(':scope>.skip-link');if(skip)skip.after(header);else body.prepend(header);body.classList.add('mobile-ready');
 const revealFocus=()=>{
  const target=document.activeElement;if(!active||!target||header.contains(target)||drawer?.contains(target)||target.closest('#cookie-layer,.skip-link,[data-job-sticky],[data-project-sticky]'))return;
  let top=header.getBoundingClientRect().bottom;
  for(const bar of document.querySelectorAll('[data-job-sticky],[data-project-sticky]')){const r=bar.getBoundingClientRect();if(!bar.hidden&&r.width&&r.top<top+5)top=Math.max(top,r.bottom)}
  const r=target.getBoundingClientRect();if(r.height&&r.top<top+12)scrollBy(0,r.top-top-12);
 };
 const onFocus=()=>requestAnimationFrame(()=>{revealFocus();requestAnimationFrame(revealFocus)});
 document.addEventListener('focusin',onFocus);cleanup.push(()=>document.removeEventListener('focusin',onFocus));
 // A consent panel is modal before enhancement as well as after a stored choice.
 const consent=document.querySelector('#cookie-layer'),inertBefore=new Map();let consentOpen=false,consentReturn;
 const syncConsent=()=>{
  let saved;try{saved=localStorage.getItem('bhr-cookie-consent')}catch{}
  const open=Boolean(consent&&!consent.hidden&&!saved&&!location.pathname.includes('cookie-instellingen'));if(open===consentOpen)return;
  consentOpen=open;
  if(open){consentReturn=document.activeElement;for(const node of body.children){if(node===consent||node.tagName==='SCRIPT')continue;inertBefore.set(node,node.inert);node.inert=true}consent.querySelector('button,a[href]')?.focus({preventScroll:true})}
  else{for(const [node,value]of inertBefore)node.inert=value;inertBefore.clear();if(active)(consentReturn&&consentReturn!==body&&consentReturn.isConnected?consentReturn:header.querySelector('a'))?.focus({preventScroll:true})}
 };
 const consentKeys=event=>{if(!consentOpen||event.key!=='Tab')return;const controls=[...consent.querySelectorAll('a[href],button')].filter(e=>e.getClientRects().length);if(event.shiftKey&&document.activeElement===controls[0]){event.preventDefault();controls.at(-1)?.focus()}else if(!event.shiftKey&&document.activeElement===controls.at(-1)){event.preventDefault();controls[0]?.focus()}};
 const consentObserver=new MutationObserver(syncConsent);if(consent)consentObserver.observe(consent,{attributes:true,attributeFilter:['hidden']});document.addEventListener('keydown',consentKeys);syncConsent();
 cleanup.push(()=>{consentObserver.disconnect();document.removeEventListener('keydown',consentKeys);for(const [node,value]of inertBefore)node.inert=value;inertBefore.clear()});
 // The editorial process variant is a separate three-step mobile composition.
 // Preserve the original desktop carousel and its closed-over item inventory.
 for(const section of document.querySelectorAll('.secondary-cards-process')){
  if(section.querySelector('h2')?.textContent.trim()!=='Hoe BHR werkt')continue;
  const items=[...section.querySelectorAll('.secondary-card-grid>article')].filter(a=>/^Stap \d/.test(a.querySelector('h4')?.textContent||''));if(!items.length)continue;
  const layout=document.createElement('div');layout.className='mobile-process';
  const photo=items[0].querySelector('img').cloneNode(true);photo.className='mobile-process-photo';
  const window=document.createElement('div');window.className='mobile-process-window';window.tabIndex=0;window.setAttribute('aria-label','Stappen van BHR');
  const track=document.createElement('div');track.className='mobile-process-track';window.append(track);
  items.forEach(item=>{const card=item.querySelector('.secondary-card-copy').cloneNode(true);card.className='mobile-process-card';card.querySelectorAll('nav:empty').forEach(e=>e.remove());track.append(card)});
  const controls=document.createElement('nav');controls.className='mobile-process-controls';controls.setAttribute('aria-label','Stappen bladeren');
  const step=()=>track.firstElementChild.getBoundingClientRect().width+20;let index=0;
  const paint=()=>{index=Math.max(0,Math.min(items.length-1,Math.round(window.scrollLeft/step())));const im=items[index].querySelector('img');photo.src=im.src;photo.alt=im.alt;controls.querySelectorAll('button').forEach((button,i)=>button.disabled=i===0?index===0:index===items.length-1)};
  for(const [label,direction]of [['Vorige stap',-1],['Volgende stap',1]]){const button=document.createElement('button');button.type='button';button.textContent=direction<0?'←':'→';button.setAttribute('aria-label',label);button.addEventListener('click',()=>window.scrollTo({left:(index+direction)*step(),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));controls.append(button)}
  window.addEventListener('scroll',paint,{passive:true});layout.append(photo,window,controls);section.querySelector('.secondary-container').append(layout);section.classList.add('mobile-process-enhanced');paint();cleanup.push(()=>{section.classList.remove('mobile-process-enhanced');layout.remove()});
 }
 // Native pointer gestures feed existing controls, preserving their image/state logic.
 for(const timeline of document.querySelectorAll('[data-secondary-timeline]')){
  const window=timeline.querySelector('.secondary-timeline-window');let start;
  const down=event=>{if(event.target.closest('button,a,input'))return;start={x:event.clientX,y:event.clientY};window.setPointerCapture(event.pointerId)};
  const up=event=>{if(start){const dx=event.clientX-start.x,dy=event.clientY-start.y;if(Math.abs(dx)>35&&Math.abs(dx)>Math.abs(dy))timeline.querySelector(dx<0?'[data-timeline-next]':'[data-timeline-prev]')?.click()}start=null};
  const cancel=()=>{start=null};window.addEventListener('pointerdown',down);window.addEventListener('pointerup',up);window.addEventListener('pointercancel',cancel);cleanup.push(()=>{window.removeEventListener('pointerdown',down);window.removeEventListener('pointerup',up);window.removeEventListener('pointercancel',cancel)});
 }
 const search=document.querySelector('[data-secondary-search]');if(search){const input=search.querySelector('input'),sync=()=>search.classList.toggle('mobile-search-populated',Boolean(input.value));input.addEventListener('input',sync);search.addEventListener('submit',sync);search.querySelector('[data-search-clear]').addEventListener('click',sync);sync();cleanup.push(()=>{input.removeEventListener('input',sync);search.removeEventListener('submit',sync);search.querySelector('[data-search-clear]').removeEventListener('click',sync);search.classList.remove('mobile-search-populated')})}

 phoneViewport.addEventListener('change',applyDeviceMedia);applyDeviceMedia();
 const updateHeader=()=>{
  const dark=body.classList.contains('thank-you-page')||(simple?scrollY>=10:scrollY>20)||innerWidth>=768;header.classList.toggle('mobile-header-scrolled',dark);
  header.querySelector('.mobile-brand img').src=siteUrl(`/assets/images/bhr-brand${dark?'':'-white'}.svg`);
 };
 addEventListener('scroll',updateHeader,{passive:true});addEventListener('resize',updateHeader);updateHeader();
 return()=>{const restoreNavigation=header.contains(document.activeElement)||drawer?.contains(document.activeElement);active=false;close();cleanup.forEach(fn=>fn());restoreScroll();restoreImages();clearPhoneContent();if(previousRoute===null)body.removeAttribute('data-mobile-route');else body.setAttribute('data-mobile-route',previousRoute);phoneViewport.removeEventListener('change',applyDeviceMedia);if(arrangePanels)phoneViewport.removeEventListener('change',arrangePanels);removeEventListener('scroll',updateHeader);removeEventListener('resize',updateHeader);if(footerLogo)footerLogo.setAttribute('src',footerLogoSource);footerSocial?.remove();header.remove();drawer?.remove();body.classList.remove('mobile-ready');if(restoreNavigation)original.querySelector('a[href],button')?.focus({preventScroll:true})};
}
function syncMobile(){if(mobileViewport.matches){if(!teardown)teardown=enhanceMobile()}else if(teardown){teardown();teardown=null;}}
mobileViewport.addEventListener('change',syncMobile);syncMobile();
