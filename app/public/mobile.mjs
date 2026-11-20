// Authored mobile UI. The desktop branch adds no nodes, classes or styles.
const mobileViewport=matchMedia('(max-width: 1199px)');
let teardown;
let mediaData,tabletData,contentData,headingData;
const phoneIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><rect x="8" y="2" width="14" height="26" rx="3"/><path d="M12 5h6M14 24h2"/></svg>';
const arrowIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><path d="M3 15h24M19 7l8 8-8 8"/></svg>';
const brandMarkup=()=>'<a class="mobile-brand" href="/" aria-label="BHR homepage"><img src="/assets/images/bhr-brand-white.svg" alt="BHR"><span>Your system<br><span class="mobile-brand-integrator">inte<span class="accent">great</span>or</span></span></a>';
function enhanceMobile(){
 const body=document.body,original=document.querySelector('.site-header');
 if(!original)return()=>{};
 const simple=original.classList.contains('simple-header');
 const header=document.createElement('header');header.className='mobile-header'+(simple?' mobile-simple-header':'');
 const phone=`<a class="mobile-circle mobile-phone" href="tel:+31162238834" aria-label="Bel BHR">${phoneIcon}</a>`;
 const toggle='<button type="button" class="mobile-circle mobile-menu-icon" data-mobile-open aria-label="Menu openen" aria-controls="mobile-navigation" aria-expanded="false"><span></span><span class="visually-hidden">Menu</span></button>';
 header.innerHTML=`<div class="mobile-header-inner">${simple?`<a data-mobile-back-link class="mobile-back-link" href="${original.querySelector('.back')?.getAttribute('href')||'/'}" aria-label="Terug">${arrowIcon}<span>Terug</span></a>`:''}${brandMarkup()}<div class="mobile-header-actions">${phone}${simple?'':'<a class="mobile-circle mobile-search" href="/zoeken" aria-label="Zoeken"><svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="m18 18 9 9"/></svg></a>'+toggle+'<a class="mobile-tablet-appointment" href="/afspraak-maken">Afspraak maken</a>'}</div></div>`;
 let drawer,opener,arrangePanels,isOpen=false,storedY=0,savedBody,active=true;
 const previousRoute=body.getAttribute('data-mobile-route');body.dataset.mobileRoute=location.pathname.replace(/\/+$/,'')||'/';
 const phoneViewport=matchMedia('(max-width: 767px)'),changedImages=new Map();
 let phoneGeneration=0;
 const phoneNodes=[],phoneRestorers=[];
 const clearPhoneContent=()=>{phoneNodes.splice(0).forEach(n=>n.remove());phoneRestorers.splice(0).reverse().forEach(fn=>fn());body.classList.remove('mobile-legacy-content')};
 const restoreImages=()=>{for(const [image,src]of changedImages)image.setAttribute('src',src);changedImages.clear()};
 const applyDeviceMedia=async()=>{
  const generation=++phoneGeneration,phone=phoneViewport.matches;
  restoreImages();if(!phone)clearPhoneContent();
  try{
   if(phone)mediaData??=fetch('/mobile-data.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{mediaData=null;return {}});
   else tabletData??=fetch('/tablet-data.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{tabletData=null;return {}});
   const data=await(phone?mediaData:tabletData);if(generation!==phoneGeneration||!active||phone!==phoneViewport.matches||!body.classList.contains('mobile-ready'))return;
   const rows=data[location.pathname.replace(/\/+$/,'')||'/']||[];
   for(const image of document.images){
    const src=image.getAttribute('src');const row=rows.find(r=>r.from===src&&r.alt===image.alt);
    if(row){if(!changedImages.has(image))changedImages.set(image,src);image.src=row.to;}
   }
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
   headingData??=fetch('/mobile-headings.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{headingData=null;return {}});
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
   contentData??=fetch('/mobile-content.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{contentData=null;return {}});
   const record=(await contentData)[body.dataset.mobileRoute];if(!record||generation!==phoneGeneration||!active||!phoneViewport.matches)return;
   const section=document.querySelector('.branch-section'),grid=section.querySelector('.branch-grid');if(!grid)return;
   const element=(tag,cls,text)=>{const e=document.createElement(tag);e.className=cls;if(text)e.textContent=text;return e};
   const window=element('div','mobile-branch-window');window.tabIndex=0;window.setAttribute('aria-label','Branches');const track=element('div','mobile-branch-track');window.append(track);
   for(const item of record.branches){const article=element('article',''),a=element('a','');a.href=item.href;const im=element('img','');im.src=item.image;im.alt=item.title;a.append(im);const h=element('h3',''),title=element('a','',item.title);title.href=item.href;h.append(title);const more=element('a','button outline','Afspraak maken');more.href=item.href;article.append(a,h,more);track.append(article)}
   add(grid.parentElement,window);const controls=element('nav','mobile-branch-controls');controls.setAttribute('aria-label','Branches bladeren');
   for(const [label,direction]of [['Vorige branche',-1],['Volgende branche',1]]){const button=element('button','',direction<0?'←':'→');button.type='button';button.setAttribute('aria-label',label);button.addEventListener('click',()=>window.scrollBy({left:direction*(window.clientWidth+20)/1.2,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'}));controls.append(button)}add(grid.parentElement,controls);
   if(record.region){const r=record.region,region=element('section','mobile-region');const container=element('div','container'),eye=element('div','eyebrow',r.eyebrow),h=element('h2','',r.title),p=element('p','',r.intro),list=element('ul','check-list');for(const text of r.locations)list.append(element('li','',text));const cta=element('a','button',r.cta);cta.href=r.href;const im=element('img','');im.src=r.image;im.alt='Werkgebied BHR in Zuid-Nederland';container.append(eye,h,p,list,cta,im);region.append(container);const why=[...document.querySelectorAll('.article-section')].find(e=>e.querySelector('h2')?.textContent.startsWith('Waarom kiezen'))||document.querySelector('.quote-section');why?.before(region);phoneNodes.push(region)}
   const wizard=document.querySelector('.quote-section .wizard');if(record.quoteTitle&&wizard){const title=element('h3','mobile-quote-title',record.quoteTitle);wizard.prepend(title);phoneNodes.push(title)}
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
  drawer.innerHTML=`<div class="mobile-drawer-inner"><div class="mobile-drawer-top">${brandMarkup()}<div class="mobile-header-actions">${phone}<button type="button" class="mobile-circle mobile-close-icon" data-mobile-close aria-label="Menu sluiten"><span></span></button></div></div><nav class="mobile-drawer-nav" aria-label="Mobiele hoofdnavigatie"><button type="button" class="mobile-back" data-mobile-back hidden aria-label="Terug naar hoofdmenu">${arrowIcon}</button><h2 class="mobile-submenu-title" hidden></h2><div data-mobile-panel="root"><a href="/">Home</a><a href="/expertises">Onze expertises</a><button type="button" data-mobile-submenu="industries">Industrieën<span>${arrowIcon}</span></button><button type="button" data-mobile-submenu="about">Over BHR<span>${arrowIcon}</span></button><a href="/service-en-onderhoud">Service en onderhoud</a><a href="/projecten">Projecten</a><a href="/contact">Contact</a></div><div data-mobile-panel="industries" hidden><a href="/voor-machinebouwers/voor-machinebouwers">Voor machinebouwers</a><a href="/voor-machinebouwers/proces-productie">Voor proces en productie</a></div><div data-mobile-panel="about" hidden><a href="/over-ons/partners">Partners</a><a href="/over-ons/werken-bij">Werken bij</a></div><nav class="mobile-drawer-aux" aria-label="Meer over BHR"><a href="/over-ons/werken-bij">Werken bij</a><a href="/nieuws">Blogs</a></nav></nav><div class="mobile-drawer-bottom"><a class="mobile-appointment" href="/afspraak-maken">Afspraak maken</a><nav class="mobile-socials" aria-label="Sociale media">${social}</nav></div></div>`;
  arrangePanels=()=>{
   const nav=drawer.querySelector('.mobile-drawer-nav');
   for(const name of ['industries','about']){const panel=drawer.querySelector(`[data-mobile-panel="${name}"]`);if(innerWidth>=768)drawer.querySelector(`[data-mobile-submenu="${name}"]`).after(panel);else nav.insertBefore(panel,drawer.querySelector('.mobile-drawer-aux'))}
   showPanel();if(isOpen)drawer.querySelector('[data-mobile-close]').focus({preventScroll:true});
  };
  arrangePanels();phoneViewport.addEventListener('change',arrangePanels);
  body.append(drawer);opener=header.querySelector('[data-mobile-open]');
  drawer.querySelectorAll('.mobile-socials a').forEach((a,i)=>{a.replaceChildren(Object.assign(document.createElement('img'),{src:`/assets/images/${['facebook','linkedin','instagram'][i]}.svg`,alt:''}))});
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
 if(footerLogo)footerLogo.src='/assets/images/bhr-brand-white.svg';
 const footerSocial=document.querySelector('.site-footer>.container>.social-links')?.cloneNode(true);
 if(footerSocial){
  footerSocial.classList.add('mobile-footer-socials');
  footerSocial.querySelectorAll('a').forEach((a,i)=>a.replaceChildren(Object.assign(document.createElement('img'),{src:`/assets/images/${['facebook','linkedin','instagram'][i]}.svg`,alt:''})));
  document.querySelector('.footer-info')?.append(footerSocial);
 }
 body.prepend(header);body.classList.add('mobile-ready');
 phoneViewport.addEventListener('change',applyDeviceMedia);applyDeviceMedia();
 const updateHeader=()=>{
  const dark=scrollY>20||innerWidth>=768;header.classList.toggle('mobile-header-scrolled',dark);
  header.querySelector('.mobile-brand img').src=`/assets/images/bhr-brand${dark?'':'-white'}.svg`;
 };
 addEventListener('scroll',updateHeader,{passive:true});addEventListener('resize',updateHeader);updateHeader();
 return()=>{active=false;close();restoreScroll();restoreImages();clearPhoneContent();if(previousRoute===null)body.removeAttribute('data-mobile-route');else body.setAttribute('data-mobile-route',previousRoute);phoneViewport.removeEventListener('change',applyDeviceMedia);if(arrangePanels)phoneViewport.removeEventListener('change',arrangePanels);removeEventListener('scroll',updateHeader);removeEventListener('resize',updateHeader);if(footerLogo)footerLogo.setAttribute('src',footerLogoSource);footerSocial?.remove();header.remove();drawer?.remove();body.classList.remove('mobile-ready')};
}
function syncMobile(){if(mobileViewport.matches){if(!teardown)teardown=enhanceMobile()}else if(teardown){teardown();teardown=null;}}
mobileViewport.addEventListener('change',syncMobile);syncMobile();
