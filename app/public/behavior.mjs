import {formDefinitions} from './config.js';
export function searchPages(pages,query){const n=x=>String(x).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const terms=n(query).trim().split(/\s+/).filter(Boolean);return terms.length?pages.filter(p=>terms.every(t=>n(`${p.title} ${p.text||''}`).includes(t))):[];}
export function stepTarget(current,direction,total){return Math.max(0,Math.min(total-1,current+direction));}
export function formSubmitSettings(kind,siteRoot){
 if(!Object.hasOwn(formDefinitions,kind))throw Error(`Unknown form: ${kind}`);
 const definition=formDefinitions[kind];
 return {action:'https://api.web3forms.com/submit',subject:definition.subject,next:new URL(definition.next.slice(1),siteRoot).href};
}
export function validateFormSubmit(data){
 if(data.get('botcheck'))return {ok:false,reason:'honeypot'};
 const files=[...data.values()].filter(value=>typeof File!=='undefined'&&value instanceof File&&value.size);
 if(files.reduce((total,file)=>total+file.size,0)>4*1024*1024)return {ok:false,reason:'files'};
 return {ok:true};
}

export function bindFormStatusReset(form,status){
 const clear=()=>{status.textContent=''};
 form.addEventListener('invalid',clear,true);
 form.addEventListener('input',clear);
 form.addEventListener('change',clear);
}
export function cookiePreferences(saved){
 if(saved==='accepted')return {analytics:true,marketing:true};
 let value={};try{value=JSON.parse(saved)||{}}catch{}
 const enabled=key=>value[key]===true||value[key]==='on';
 return {analytics:enabled('analytics'),marketing:enabled('marketing')};
}

// Calendar validation is shared by the split birth-date controls and submission.
export function birthDateValue(day,month,year){
 if(!/^\d+$/.test(String(day))||!/^\d+$/.test(String(month))||!/^\d{4}$/.test(String(year)))return null;
 const d=Number(day),m=Number(month),y=Number(year),date=new Date(Date.UTC(y,m-1,d));
 if(y<1900||m<1||m>12||d<1||date.getUTCFullYear()!==y||date.getUTCMonth()!==m-1||date.getUTCDate()!==d)return null;
 return `${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
}

export function carouselTarget(current,direction,total,loop=false){
 if(total<1)return 0;
 return loop?((current+direction)%total+total)%total:stepTarget(current,direction,total);
}
