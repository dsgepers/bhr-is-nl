import {siteUrl} from './paths.mjs';
import {searchPages,stepTarget,formSubmitSettings,validateFormSubmit,bindFormStatusReset,cookiePreferences,birthDateValue,carouselTarget} from './behavior.mjs';
import {arrowIcon} from './icons.mjs';
const $=(q,root=document)=>root.querySelector(q),$$=(q,root=document)=>[...root.querySelectorAll(q)];
const safeStore={get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}}};
const cookieLayer=$('#cookie-layer');
if(safeStore.get('bhr-cookie-consent')||location.pathname.includes('cookie-instellingen'))cookieLayer.hidden=true;
$$('[data-consent]').forEach(b=>b.addEventListener('click',()=>{safeStore.set('bhr-cookie-consent',b.dataset.consent);cookieLayer.hidden=true}));
const savedPreferences=cookiePreferences(safeStore.get('bhr-cookie-consent'));$$('.cookie-options input[name]').forEach(input=>{input.checked=savedPreferences[input.name]===true});
$('.cookie-options')?.addEventListener('submit',e=>{e.preventDefault();safeStore.set('bhr-cookie-consent',JSON.stringify(Object.fromEntries(new FormData(e.currentTarget))));const p=document.createElement('p');p.setAttribute('role','status');p.textContent='Uw voorkeuren zijn opgeslagen.';e.currentTarget.append(p)});
$$('.dropdown-toggle').forEach(b=>b.addEventListener('click',()=>{const open=b.closest('.dropdown').classList.toggle('open');b.setAttribute('aria-expanded',open)}));
$('.mobile-toggle')?.addEventListener('click',e=>{const open=$('.site-header').classList.toggle('menu-open');e.currentTarget.setAttribute('aria-expanded',open);e.currentTarget.setAttribute('aria-label',open?'Menu sluiten':'Menu openen')});
document.addEventListener('click',e=>{$$('.dropdown.open').forEach(d=>{if(!d.contains(e.target)){d.classList.remove('open');$('.dropdown-toggle',d).setAttribute('aria-expanded','false')}})});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){
 $$('.dropdown.open').forEach(d=>{d.classList.remove('open');$('.dropdown-toggle',d).setAttribute('aria-expanded','false')});
 const header=$('.site-header'),toggle=$('.mobile-toggle');
 if(header.classList.contains('menu-open')){header.classList.remove('menu-open');toggle?.setAttribute('aria-expanded','false');toggle?.setAttribute('aria-label','Menu openen');toggle?.focus()}
}});
const header=$('.site-header');
document.addEventListener('click',event=>{
 if(event.target.closest('[data-history-back]')){event.preventDefault();window.history.back()}
});
const simpleHeader=header.classList.contains('simple-header'),simpleLogo=simpleHeader?$('.brand img',header):null;
const syncHeader=()=>{
 const scrolled=simpleHeader?window.scrollY>=10:window.scrollY>20;
 header.classList.toggle('is-scrolled',scrolled);
 if(simpleLogo){const source=siteUrl(`/assets/images/bhr-brand${scrolled?'':'-white'}.svg`);if(simpleLogo.getAttribute('src')!==source)simpleLogo.src=source}
};
window.addEventListener('scroll',syncHeader,{passive:true});syncHeader();
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
 const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-visible');reveal.unobserve(entry.target)}}),{threshold:.12});
 $$('.intro-layout>div,.section-heading>div,.industry-copy,.how-row,.about-copy,.title-copy,.article-copy').forEach(element=>{element.classList.add('reveal-ready');reveal.observe(element)});
}
$('[data-scroll]')?.addEventListener('click',e=>document.getElementById(e.currentTarget.dataset.scroll)?.scrollIntoView({behavior:'smooth'}));
const slides=$$('.slide');let currentSlide=0;function showSlide(i){currentSlide=i;slides.forEach((s,n)=>{s.classList.toggle('active',n===i);s.inert=n!==i;s.setAttribute('aria-hidden',n!==i)});$$('[data-goto-slide]').forEach((b,n)=>b.setAttribute('aria-pressed',n===i));}
if(slides.length)showSlide(0);
$$('[data-goto-slide]').forEach(b=>b.addEventListener('click',()=>showSlide(Number(b.dataset.gotoSlide))));
if(slides.length&&!matchMedia('(prefers-reduced-motion: reduce)').matches)setInterval(()=>{if(!document.hidden)showSlide((currentSlide+1)%slides.length)},6000);
const searchDialog=$('.search-dialog');$('.search-open')?.addEventListener('click',e=>{if(searchDialog?.showModal){e.preventDefault();searchDialog.showModal();$('input',searchDialog).focus()}});
$$('.dialog-close').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
$$('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close()}}));
let searchIndex;async function find(form,query){const result=form.parentElement.querySelector('.search-results');try{searchIndex??=await fetch(siteUrl('/search-index.json')).then(r=>{if(!r.ok)throw Error();return r.json()});const matches=searchPages(searchIndex,query);result.replaceChildren();const label=document.createElement('p');label.textContent=matches.length?`${matches.length} resultaten voor “${query}”`:`Geen resultaten voor “${query}”.`;result.append(label);matches.forEach(p=>{const article=document.createElement('article'),h=document.createElement('h3'),a=document.createElement('a');a.href=p.url;a.textContent=p.title;h.append(a);article.append(h);result.append(article)})}catch{result.textContent='Zoeken is tijdelijk niet beschikbaar. Probeer het opnieuw.'}}
$$('.site-search').forEach(form=>{form.addEventListener('submit',e=>{e.preventDefault();const q=new FormData(form).get('q').trim();if(q)find(form,q)});if(!form.closest('dialog')){const q=new URLSearchParams(location.search).get('q');if(q){$('input',form).value=q;find(form,q)}}});
$('.filters')?.addEventListener('submit',e=>{e.preventDefault();const chosen=new FormData(e.currentTarget).getAll('categorie');let visible=0;$$('.project-card').forEach(p=>{p.hidden=chosen.length>0&&!chosen.includes(p.dataset.category);if(!p.hidden)visible++});$$('[data-project-category]').forEach(section=>{section.hidden=$$('.project-card',section).every(p=>p.hidden)});$('.results-empty').hidden=visible>0;const url=new URL(location.href);url.searchParams.delete('categorie');chosen.forEach(v=>url.searchParams.append('categorie',v));history.replaceState(null,'',url)});
if($('.filters')){const params=new URLSearchParams(location.search).getAll('categorie');$$('.filters input').forEach(i=>i.checked=params.includes(i.value));if(params.length)$('.filters').dispatchEvent(new Event('submit',{cancelable:true}))}
$('a[href="#meer-expertises"]')?.addEventListener('click',e=>{e.preventDefault();const open=$('.service-grid').classList.toggle('show-all');e.currentTarget.innerHTML=`<span class="arrow">${arrowIcon(open)}</span>${open?'Toon minder':'Toon meer'}`});
$$('.lightbox-open').forEach(a=>a.addEventListener('click',e=>{const d=$('.lightbox');if(d?.showModal){e.preventDefault();$('img',d).src=a.href;$('img',d).alt=$('img',a)?.alt||'Vergrote afbeelding';d.showModal()}}));
const formSiteRoot=new URL('.',import.meta.url);
$$('[data-form-submit]').forEach(form=>{
 const settings=formSubmitSettings(form.dataset.formSubmit,formSiteRoot);
 form.action=settings.action;
 $('[name="subject"]',form).value=settings.subject;
 $('[name="redirect"]',form).value=settings.next;
 $('[name="pagina"]',form).value=location.href;
 let step=0;const steps=$$('[data-step]',form);
 function change(direction){if(direction>0){const inputs=$$('input,select,textarea',steps[step]);const bad=inputs.find(i=>!i.checkValidity());if(bad){bad.reportValidity();return}}step=stepTarget(step,direction,steps.length);steps.forEach((s,i)=>{s.hidden=i!==step});$$('[data-step-label]',form).forEach((l,i)=>{l.classList.toggle('current',i===step);l.setAttribute('aria-current',i===step?'step':'false')});$('.prev-step',form).hidden=step===0;$('.next-step',form).hidden=step===steps.length-1;$('.wizard-submit',form).hidden=step!==steps.length-1;$('input,select,textarea',steps[step])?.focus()}
 bindFormStatusReset(form,$('.form-status',form));
 $('.next-step',form)?.addEventListener('click',()=>change(1));$('.prev-step',form)?.addEventListener('click',()=>change(-1));
 form.addEventListener('keydown',e=>{if(e.key==='Enter'&&steps.length&&e.target.tagName!=='TEXTAREA'&&e.target.tagName!=='BUTTON'&&step<steps.length-1){e.preventDefault();change(1)}});
 // A wizard validates visible controls as it advances and validates every step at final submission.
 if(steps.length)form.noValidate=true;
 form.addEventListener('submit',e=>{
  const status=$('.form-status',form);status.textContent='';
  if(steps.length){
   const invalid=steps.findIndex(s=>$$('input,select,textarea',s).some(i=>!i.checkValidity()));
   if(invalid>=0){e.preventDefault();step=invalid;change(0);$$('input,select,textarea',steps[step]).find(i=>!i.checkValidity())?.reportValidity();return}
  }else if(!form.reportValidity()){e.preventDefault();return}
  const result=validateFormSubmit(new FormData(form));
  if(!result.ok){
   e.preventDefault();status.textContent=result.reason==='files'?'Uw documenten zijn samen te groot. Kies bestanden van maximaal 4 MB.':'Uw bericht is niet verzonden. Probeer het opnieuw.';return;
  }
  // Let the browser POST the complete form; the configured provider handles the redirect.
  $('button[type="submit"]',form).disabled=true;
  status.textContent='Uw bericht wordt verzonden…';
 });
 const enable=()=>{$('button[type="submit"]',form).disabled=false;$('.form-status',form).textContent=''};
 window.addEventListener('pageshow',enable);enable();
});

// Scoped parity controls use the same form delivery contract as the other pages.
$$('.parity-form').forEach(form=>{
 const day=$('[name="birth_day"]',form),month=$('[name="birth_month"]',form),year=$('[name="birth_year"]',form);
 if(day&&month&&year){
  const syncDate=()=>{const value=birthDateValue(day.value,month.value,year.value);$('[name="birthdate"]',form).value=value||'';day.setCustomValidity(value?'':'Kies een geldige geboortedatum.');};
  [day,month,year].forEach(input=>input.addEventListener('change',syncDate));
  form.addEventListener('submit',syncDate,true);form.addEventListener('reset',()=>{day.setCustomValidity('');});
 }
 $('input[type="file"]',form)?.addEventListener('change',e=>{const label=$('[data-file-name]',form);if(label)label.textContent=e.target.files?.[0]?.name||'Selecteer een bestand';});
});
$$('[data-carousel]').forEach(root=>{
 const track=$('[data-carousel-track]',root),items=[...track.children],viewport=track.parentElement;
 if(!items.length)return;
 const loop=root.dataset.carousel==='partners',motion=matchMedia('(prefers-reduced-motion: reduce)');
 let position=0,start=null,timer=null,wrapTimer=null,hovered=false,focused=false;
 if(loop){
  const clone=item=>{const copy=item.cloneNode(true);copy.removeAttribute('data-partner');copy.setAttribute('aria-hidden','true');copy.inert=true;return copy;};
  track.prepend(...items.map(clone));track.append(...items.map(clone));
 }
 const paint=(index,step,animate)=>{
  track.style.transition=animate?'':'none';track.style.transform=`translateX(${-index*step}px)`;
  if(!animate){void track.offsetWidth;track.style.transition='';}
 };
 const update=(direction,animate=true)=>{
  const gap=parseFloat(getComputedStyle(track).gap)||0,step=items[0].getBoundingClientRect().width+gap;
  const visible=Math.max(1,Math.floor((viewport.getBoundingClientRect().width+gap)/step)),previous=position;
  if(wrapTimer){clearTimeout(wrapTimer);wrapTimer=null;paint((loop?items.length:0)+position,step,false);}
  position=carouselTarget(position,direction,loop?items.length:Math.max(1,items.length-visible+1),loop);
  let visual=(loop?items.length:0)+position;
  const wrapped=loop&&((direction>0&&previous===items.length-1&&position===0)||(direction<0&&previous===0&&position===items.length-1));
  if(wrapped)visual=direction>0?2*items.length:items.length-1;
  paint(visual,step,animate&&!motion.matches);
  const photo=$('.parity-step-photo,.secondary-steps-layout>.secondary-photo',root),photoSource=items[position].dataset.stepImage;
  if(photo&&photoSource){photo.src=photoSource;photo.alt=$('h3',items[position])?.textContent||photo.alt;}
  if(wrapped)wrapTimer=setTimeout(()=>{paint(items.length+position,step,false);wrapTimer=null;},motion.matches?0:360);
  const status=$('[data-carousel-status]',root);
  if(status){
   const shown=Array.from({length:Math.min(visible,items.length)},(_,i)=>(position+i)%items.length+1);
   status.textContent=loop?(position+visible>items.length?`Partners ${shown.join(', ')} van ${items.length}`:`Partners ${position+1} tot ${position+visible} van ${items.length}`):`Stap ${position+1} van ${items.length}`;
  }
  const progress=$('.parity-progress',root);if(progress)progress.style.setProperty('--progress',`${(position+1)/items.length*100}%`);
  $$('[data-carousel-direction]',root).forEach(button=>button.disabled=!loop&&(Number(button.dataset.carouselDirection)<0?position===0:position>=items.length-visible));
 };
 const pause=()=>{clearInterval(timer);timer=null;};
 const resume=()=>{pause();if(loop&&!motion.matches&&!hovered&&!focused&&!document.hidden)timer=setInterval(()=>update(1),5000);};
 $$('[data-carousel-direction]',root).forEach(button=>button.addEventListener('click',()=>update(Number(button.dataset.carouselDirection))));
 viewport.addEventListener('pointerdown',e=>{if(e.target.closest('button,a,input,select,textarea'))return;start=e.clientX;pause();viewport.setPointerCapture(e.pointerId);});
 viewport.addEventListener('pointerup',e=>{if(start!==null&&Math.abs(e.clientX-start)>35)update(e.clientX<start?1:-1);start=null;resume();});
 viewport.addEventListener('pointercancel',()=>{start=null;resume();});
 root.addEventListener('mouseenter',()=>{hovered=true;pause();});root.addEventListener('mouseleave',()=>{hovered=false;resume();});
 root.addEventListener('focusin',()=>{focused=true;pause();});root.addEventListener('focusout',e=>{if(!root.contains(e.relatedTarget)){focused=false;resume();}});
 motion.addEventListener('change',resume);document.addEventListener('visibilitychange',resume);
 window.addEventListener('resize',()=>update(0,false));update(0,false);resume();
});
