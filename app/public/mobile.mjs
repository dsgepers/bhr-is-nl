// Authored mobile UI. The desktop branch adds no nodes, classes or styles.
const mobileViewport=matchMedia('(max-width: 1199px)');
let teardown;
let mediaData;
const phoneIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><rect x="8" y="2" width="14" height="26" rx="3"/><path d="M12 5h6M14 24h2"/></svg>';
const arrowIcon='<svg viewBox="0 0 30 30" aria-hidden="true"><path d="M3 15h24M19 7l8 8-8 8"/></svg>';
const brandMarkup=()=>'<a class="mobile-brand" href="/" aria-label="BHR homepage"><img src="/assets/images/bhr-brand-white.svg" alt="BHR"><span>Your system<br>inte<span class="accent">great</span>or</span></a>';
function enhanceMobile(){
 const body=document.body,original=document.querySelector('.site-header');
 if(!original)return()=>{};
 const simple=original.classList.contains('simple-header');
 const header=document.createElement('header');header.className='mobile-header'+(simple?' mobile-simple-header':'');
 const phone=`<a class="mobile-circle mobile-phone" href="tel:+31162238834" aria-label="Bel BHR">${phoneIcon}</a>`;
 const toggle='<button type="button" class="mobile-circle mobile-menu-icon" data-mobile-open aria-label="Menu openen" aria-controls="mobile-navigation" aria-expanded="false"><span></span><span class="visually-hidden">Menu</span></button>';
 header.innerHTML=`<div class="mobile-header-inner">${simple?`<a data-mobile-back-link class="mobile-back-link" href="${original.querySelector('.back')?.getAttribute('href')||'/'}" aria-label="Terug">${arrowIcon}<span>Terug</span></a>`:''}${brandMarkup()}<div class="mobile-header-actions">${phone}${simple?'':'<a class="mobile-circle mobile-search" href="/zoeken" aria-label="Zoeken"><svg viewBox="0 0 30 30" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="m18 18 9 9"/></svg></a>'+toggle+'<a class="mobile-tablet-appointment" href="/afspraak-maken">Afspraak maken</a>'}</div></div>`;
 let drawer,opener,isOpen=false,storedY=0,savedBody;
 const phoneViewport=matchMedia('(max-width: 767px)'),changedImages=new Map();
 const restoreImages=()=>{for(const [image,src]of changedImages)image.setAttribute('src',src);changedImages.clear()};
 const applyPhoneMedia=async()=>{
  if(!phoneViewport.matches){restoreImages();return;}
  try{
   mediaData??=fetch('/mobile-data.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error();return r.json()}).catch(()=>{mediaData=null;return {}});
   const data=await mediaData;if(!phoneViewport.matches||!body.classList.contains('mobile-ready'))return;
   const rows=data[location.pathname.replace(/\/+$/,'')||'/']||[];
   for(const image of document.images){
    const src=image.getAttribute('src');const row=rows.find(r=>r.from===src&&r.alt===image.alt);
    if(row){changedImages.set(image,src);image.src=row.to;}
   }
  }catch{}
 };
 const restoreScroll=()=>{
  if(!savedBody)return;
  for(const [key,value]of Object.entries(savedBody))body.style[key]=value;
  savedBody=null;scrollTo(0,storedY);
 };
 const showPanel=(name='root')=>{
  if(!drawer)return;
  drawer.querySelectorAll('[data-mobile-panel]').forEach(p=>p.hidden=p.dataset.mobilePanel!==name);
  drawer.querySelector('[data-mobile-back]').hidden=name==='root';
  drawer.querySelector('.mobile-submenu-title').hidden=name==='root';
  drawer.querySelector('.mobile-submenu-title').textContent=name==='about'?'Over BHR':name==='industries'?'Industrieën':'';
  drawer.dataset.panel=name;
  if(name!=='root')drawer.querySelector('[data-mobile-back]').focus({preventScroll:true});
 };
 const close=()=>{
  if(!isOpen)return;isOpen=false;drawer.close();opener?.setAttribute('aria-expanded','false');restoreScroll();opener?.focus({preventScroll:true});
 };
 if(!simple){
  drawer=document.createElement('dialog');drawer.className='mobile-drawer';drawer.id='mobile-navigation';drawer.setAttribute('aria-label','Hoofdnavigatie');
  const social=document.querySelector('.social-links')?.innerHTML||'';
  drawer.innerHTML=`<div class="mobile-drawer-inner"><div class="mobile-drawer-top">${brandMarkup()}<div class="mobile-header-actions">${phone}<button type="button" class="mobile-circle mobile-close-icon" data-mobile-close aria-label="Menu sluiten"><span></span></button></div></div><nav class="mobile-drawer-nav" aria-label="Mobiele hoofdnavigatie"><button type="button" class="mobile-back" data-mobile-back hidden aria-label="Terug naar hoofdmenu">${arrowIcon}</button><h2 class="mobile-submenu-title" hidden></h2><div data-mobile-panel="root"><a href="/">Home</a><a href="/expertises">Onze expertises</a><button type="button" data-mobile-submenu="industries">Industrieën<span>${arrowIcon}</span></button><button type="button" data-mobile-submenu="about">Over BHR<span>${arrowIcon}</span></button><a href="/service-en-onderhoud">Service en onderhoud</a><a href="/projecten">Projecten</a><a href="/contact">Contact</a></div><div data-mobile-panel="industries" hidden><a href="/voor-machinebouwers/voor-machinebouwers">Voor machinebouwers</a><a href="/voor-machinebouwers/proces-productie">Voor proces en productie</a></div><div data-mobile-panel="about" hidden><a href="/over-ons/partners">Partners</a><a href="/over-ons/werken-bij">Werken bij</a></div></nav><div class="mobile-drawer-bottom"><a class="mobile-appointment" href="/afspraak-maken">Afspraak maken</a><nav class="mobile-socials" aria-label="Sociale media">${social}</nav></div></div>`;
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
 body.prepend(header);body.classList.add('mobile-ready');
 phoneViewport.addEventListener('change',applyPhoneMedia);applyPhoneMedia();
 const updateHeader=()=>{
  const dark=scrollY>20||innerWidth>=768;header.classList.toggle('mobile-header-scrolled',dark);
  header.querySelector('.mobile-brand img').src=`/assets/images/bhr-brand${dark?'':'-white'}.svg`;
 };
 addEventListener('scroll',updateHeader,{passive:true});addEventListener('resize',updateHeader);updateHeader();
 return()=>{close();restoreScroll();restoreImages();phoneViewport.removeEventListener('change',applyPhoneMedia);removeEventListener('scroll',updateHeader);removeEventListener('resize',updateHeader);header.remove();drawer?.remove();body.classList.remove('mobile-ready')};
}
function syncMobile(){if(mobileViewport.matches){if(!teardown)teardown=enhanceMobile()}else if(teardown){teardown();teardown=null;}}
mobileViewport.addEventListener('change',syncMobile);syncMobile();
