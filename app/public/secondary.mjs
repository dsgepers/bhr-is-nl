import {siteUrl} from './paths.mjs';
import {selectedProjectGroup,projectGalleryIndex} from './secondary-behavior.mjs';
import {searchPages,cookiePreferences,stepTarget} from './behavior.mjs';
const all=(selector,root=document)=>[...root.querySelectorAll(selector)];
const filters=all('[data-project-filter]');
function syncProjects(){
 const selected=selectedProjectGroup(location.search);
 filters.forEach(input=>{input.checked=input.value===selected});
 all('[data-project-group]').forEach(group=>{group.hidden=selected!==null&&group.dataset.projectGroup!==selected});
 all('[data-project-reset]').forEach(button=>{button.hidden=selected===null});
 const empty=document.querySelector('[data-project-empty]');if(empty)empty.hidden=selected!=='3';
}
filters.forEach(input=>input.addEventListener('change',()=>{const url=new URL(location.href);url.searchParams.set('filter_projectgroup[]',input.value);history.pushState({},'',url);syncProjects()}));
all('[data-project-reset]').forEach(button=>button.addEventListener('click',()=>{const url=new URL(location.href);url.searchParams.delete('filter_projectgroup[]');history.pushState({},'',url);syncProjects()}));
window.addEventListener('popstate',syncProjects);syncProjects();
const sticky=document.querySelector('[data-project-sticky]'),hero=document.querySelector('.secondary-hero');
if(sticky&&hero){const sync=()=>{sticky.hidden=scrollY<hero.offsetHeight};window.addEventListener('scroll',sync,{passive:true});sync()}
all('[data-project-gallery]').forEach(gallery=>{
 const slides=all('.secondary-project-slide',gallery),thumbs=all('[data-project-thumb]',gallery);let index=0;
 const show=next=>{index=projectGalleryIndex(next,0,slides.length);slides.forEach((slide,i)=>slide.classList.toggle('is-hidden',i!==index));thumbs.forEach((thumb,i)=>thumb.setAttribute('aria-pressed',String(i===index)));gallery.dataset.projectIndex=String(index)};
 gallery.querySelector('[data-project-prev]')?.addEventListener('click',()=>show(projectGalleryIndex(index,-1,slides.length)));
 gallery.querySelector('[data-project-next]')?.addEventListener('click',()=>show(projectGalleryIndex(index,1,slides.length)));
 thumbs.forEach((thumb,i)=>thumb.addEventListener('click',()=>show(i)));show(0);
});
// These forms deliberately never enter site.mjs's .static-form delivery scanner.
all('[data-local-only-form]').forEach(form=>{
 const steps=all('[data-step]',form),status=form.querySelector('.form-status');let step=0;
 const show=next=>{step=stepTarget(next,0,steps.length);steps.forEach((s,i)=>{s.hidden=i!==step});form.querySelector('.prev-step').hidden=step===0;form.querySelector('.next-step').hidden=step===steps.length-1;form.querySelector('.wizard-submit').hidden=step!==steps.length-1;steps[step].querySelector('input,select,textarea')?.focus()};
 const validStep=()=>{const bad=all('input,select,textarea',steps[step]).find(i=>!i.checkValidity());if(bad){bad.reportValidity();return false}return true};
 if(steps.length){form.noValidate=true;form.querySelector('.next-step').addEventListener('click',()=>{if(validStep())show(step+1)});form.querySelector('.prev-step').addEventListener('click',()=>show(step-1));form.addEventListener('keydown',event=>{if(event.key==='Enter'&&event.target.tagName!=='BUTTON'&&event.target.tagName!=='TEXTAREA'&&step<steps.length-1){event.preventDefault();if(validStep())show(step+1)}})}
 form.addEventListener('submit',event=>{event.preventDefault();status.textContent='';if(steps.length){const invalid=steps.findIndex(s=>all('input,select,textarea',s).some(i=>!i.checkValidity()));if(invalid>=0){show(invalid);validStep();return}}else if(!form.reportValidity())return;status.textContent='Dit formulier is nog niet aangesloten.'});
 form.addEventListener('input',()=>{status.textContent=''});form.querySelector('button[type="submit"]').disabled=false;
});
const searchForm=document.querySelector('[data-secondary-search]'),results=document.querySelector('[data-secondary-results]');
if(searchForm&&results){
 const input=searchForm.querySelector('input');let sequence=0,index;
 const render=async query=>{const ticket=++sequence;results.replaceChildren();if(!query.trim())return;index??=fetch(siteUrl('/search-index.json')).then(r=>{if(!r.ok)throw new Error('Search index unavailable');return r.json()});const pending=index;let pages;try{pages=await pending}catch{if(index===pending)index=undefined;if(ticket===sequence)results.textContent='Zoeken is tijdelijk niet beschikbaar.';return}if(ticket!==sequence)return;const matches=searchPages(pages,query);if(!matches.length){results.textContent='Geen resultaten gevonden.';return}for(const page of matches){const article=document.createElement('article'),heading=document.createElement('h2'),anchor=document.createElement('a'),description=document.createElement('p');anchor.href=page.url;anchor.textContent=page.title;heading.append(anchor);description.textContent=(page.text||'').slice(0,240);article.append(heading,description);results.append(article)}};
 const sync=()=>{const params=new URLSearchParams(location.search);input.value=params.get('search')??params.get('q')??'';render(input.value)};
 searchForm.addEventListener('submit',event=>{event.preventDefault();const url=new URL(location.href);url.searchParams.delete('q');input.value?url.searchParams.set('search',input.value):url.searchParams.delete('search');history.pushState({},'',url);render(input.value)});
 searchForm.querySelector('[data-search-clear]').addEventListener('click',()=>{input.value='';searchForm.requestSubmit();input.focus()});window.addEventListener('popstate',sync);sync();
}
const cookieForm=document.querySelector('[data-secondary-cookies]');
if(cookieForm){
 const key='bhr-cookie-consent',inputs=all('input[name]',cookieForm);let saved;try{saved=localStorage.getItem(key)}catch{}
 const common=cookiePreferences(saved);let details={};try{details=JSON.parse(saved)||{}}catch{}
 inputs.forEach(input=>{input.checked=input.name==='necessary'||(input.name==='analytics'?common.analytics:Object.hasOwn(details,input.name)?details[input.name]===true:common.marketing)});
 const save=acceptAll=>{const preferences={necessary:true};inputs.forEach(input=>{if(acceptAll)input.checked=true;preferences[input.name]=input.checked});preferences.marketing=['socialMedia','personalized','content','advertising'].some(k=>preferences[k]);try{localStorage.setItem(key,JSON.stringify(preferences))}catch{}cookieForm.querySelector('[role="status"]').textContent='Uw voorkeuren zijn opgeslagen.';const banner=document.querySelector('#cookie-layer');if(banner)banner.hidden=true};
 cookieForm.addEventListener('submit',event=>{event.preventDefault();save(false)});all('[data-cookie-all]',cookieForm).forEach(button=>button.addEventListener('click',()=>save(true)));
}
const jobSticky=document.querySelector('[data-job-sticky]');
if(jobSticky){const title=document.querySelector('.secondary-job-title');const sync=()=>{jobSticky.hidden=scrollY<(title?.offsetHeight||500);if(!jobSticky.hidden)document.documentElement.style.setProperty('--secondary-job-sticky-height',`${jobSticky.offsetHeight}px`)};window.addEventListener('scroll',sync,{passive:true});window.addEventListener('resize',sync);document.fonts.ready.then(sync);sync()}

const bannerButtons=all('[data-banner-index]');
if(bannerButtons.length){const pictures=all('.secondary-hero-image');bannerButtons.forEach((button,index)=>button.addEventListener('click',()=>{pictures.forEach((picture,i)=>picture.classList.toggle('is-hidden',i!==index));bannerButtons.forEach((control,i)=>control.setAttribute('aria-pressed',String(i===index)))}))}

all('[data-secondary-timeline]').forEach(timeline=>{
 const track=timeline.querySelector('[data-timeline-track]'),years=all('[data-timeline-index]',timeline);
 const previous=timeline.querySelector('[data-timeline-prev]'),next=timeline.querySelector('[data-timeline-next]');let index=0;
 const show=target=>{index=projectGalleryIndex(target,0,years.length);const first=track.firstElementChild,step=first.getBoundingClientRect().width+parseFloat(getComputedStyle(track).gap||0);track.style.transform=`translateX(${-index*step}px)`;years.forEach((year,i)=>year.setAttribute('aria-pressed',String(i===index)));previous.disabled=index===0;next.disabled=index===years.length-1};
 years.forEach((year,i)=>year.addEventListener('click',()=>show(i)));
 previous.addEventListener('click',()=>show(index-1));next.addEventListener('click',()=>show(index+1));window.addEventListener('resize',()=>show(index));show(0);
});

all('[data-job-share]').forEach(share=>{
 share.addEventListener('mouseenter',()=>{share.open=true});share.addEventListener('mouseleave',()=>{share.open=false});
 share.addEventListener('keydown',event=>{if(event.key==='Escape'){share.open=false;share.querySelector('summary').focus();event.stopPropagation()}});
});
