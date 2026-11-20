import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as forms from '../public/behavior.mjs';

const data=()=>{const value=new FormData();value.set('subject','Offerteaanvraag BHR');value.set('email','test@example.invalid');value.set('$specificatie_0','Machinebouw');return value;};
test('forms keep visitor details and make no request until a key is supplied',async()=>{
 const value=data();let called=false;
 const result=await forms.submitStaticForm(value,{},async()=>{called=true;throw Error('Unexpected delivery')});
 assert.equal(called,false);assert.equal(result.reason,'unconfigured');
 assert.equal(value.get('email'),'test@example.invalid');
});
test('configured forms send all fields and use the form-specific key',async()=>{
 const value=data();let delivered;
 const result=await forms.submitStaticForm(value,{staticFormsKey:'shared-key',formKeys:{'Offerteaanvraag BHR':'quote-key'}},async(url,options)=>{
  delivered={url,options};return {ok:true,json:async()=>({success:true})};
 });
 assert.equal(result.ok,true);assert.equal(delivered.url,'https://api.staticforms.dev/submit');
 assert.equal(delivered.options.method,'POST');
 assert.equal(delivered.options.body.get('apiKey'),'quote-key');
 assert.equal(delivered.options.body.get('$specificatie_0'),'Machinebouw');
 assert.equal(delivered.options.body.get('email'),'test@example.invalid');
});
test('service rejection and network failure never report success',async()=>{
 for(const fetcher of [async()=>({ok:false,json:async()=>({success:false})}),async()=>({ok:true,json:async()=>({success:false})}),async()=>{throw Error('Offline')}]){
  const value=data(),result=await forms.submitStaticForm(value,{staticFormsKey:'test-key'},fetcher);
  assert.equal(result.ok,false);assert.equal(result.reason,'delivery');assert.equal(value.get('email'),'test@example.invalid');
 }
});
test('oversized attachments and honeypot entries are blocked before delivery',async()=>{
 let called=false;const fetcher=async()=>{called=true;throw Error('Unexpected delivery')};
 const value=data();value.set('cv',new File([new Uint8Array(4*1024*1024+1)],'cv.pdf',{type:'application/pdf'}));
 assert.equal((await forms.submitStaticForm(value,{staticFormsKey:'test-key'},fetcher)).reason,'files');
 const bot=data();bot.set('honeypot','Spam');
 assert.equal((await forms.submitStaticForm(bot,{staticFormsKey:'test-key'},fetcher)).reason,'honeypot');
 assert.equal(called,false);
});

test('editing a form or failing browser validation clears an earlier success message',()=>{
 const form=new EventTarget(),status={textContent:''};
 forms.bindFormStatusReset(form,status);
 for(const event of ['input','change','invalid']){
  status.textContent='Bedankt voor uw bericht.';
  form.dispatchEvent(new Event(event));
  assert.equal(status.textContent,'',`${event} must clear the prior submission result`);
 }
});
