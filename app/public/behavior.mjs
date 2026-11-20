export function searchPages(pages,query){const n=x=>String(x).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const terms=n(query).trim().split(/\s+/).filter(Boolean);return terms.length?pages.filter(p=>terms.every(t=>n(`${p.title} ${p.text||''}`).includes(t))):[];}
export function stepTarget(current,direction,total){return Math.max(0,Math.min(total-1,current+direction));}
export async function submitStaticForm(data,config={},fetcher=fetch){
 const key=String(config.formKeys?.[data.get('subject')]||config.staticFormsKey||'').trim();
 if(!key)return {ok:false,reason:'unconfigured'};
 if(String(data.get('honeypot')||'').trim())return {ok:false,reason:'honeypot'};
 const files=[...data.values()].filter(v=>typeof File!=='undefined'&&v instanceof File&&v.size);
 if(files.reduce((total,file)=>total+file.size,0)>4*1024*1024)return {ok:false,reason:'files'};
 data.set('apiKey',key);
 try{
  const response=await fetcher(config.staticFormsEndpoint||'https://api.staticforms.dev/submit',{
   method:'POST',body:data,headers:{Accept:'application/json'},signal:AbortSignal.timeout(20000)
  });
  const result=await response.json();
  return response.ok&&result.success===true?{ok:true}:{ok:false,reason:'delivery'};
 }catch{return {ok:false,reason:'delivery'}}
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
