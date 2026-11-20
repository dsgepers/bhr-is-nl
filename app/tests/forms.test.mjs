import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as forms from '../public/behavior.mjs';

const data=()=>{const value=new FormData();value.set('email','test@example.invalid');value.set('$specificatie_0','Machinebouw');return value;};
test('appointment uses Web3Forms with redirects on the actual published origin and repository root',()=>{
 for(const root of ['https://example.com/','https://dsgepers.github.io/bhr-is-nl/','http://localhost:4173/']){
  const result=forms.formSubmitSettings('appointment',root);
  assert.equal(result.action,'https://api.web3forms.com/submit');
  assert.equal(result.next,new URL('bedankt/afspraak/',root).href);
  assert.equal(result.subject,'Afspraakaanvraag BHR');
 }
 assert.throws(()=>forms.formSubmitSettings('unknown','https://example.com/'),/Unknown/);
});
test('all form purposes have distinct thank-you destinations',()=>{
 const kinds=['contact','quick','appointment','quote','application','newsletter'];
 const settings=kinds.map(kind=>forms.formSubmitSettings(kind,'https://example.com/'));
 assert.equal(new Set(settings.map(s=>s.next)).size,kinds.length);
 for(const setting of settings)assert.match(setting.next,/^https:\/\/example.com\/bedankt\//);
});
test('native delivery preserves visitor fields and accepts a CV up to the existing 4 MB limit',()=>{
 const value=data();value.set('attachment',new File([new Uint8Array(4*1024*1024)],'cv.pdf',{type:'application/pdf'}));
 assert.deepEqual(forms.validateFormSubmit(value),{ok:true});
 assert.equal(value.get('email'),'test@example.invalid');assert.equal(value.get('$specificatie_0'),'Machinebouw');
 assert.equal(value.get('attachment').name,'cv.pdf');
});
test('oversized combined attachments and honeypot entries block native delivery',()=>{
 const value=data();value.set('attachment',new File([new Uint8Array(4*1024*1024)],'cv.pdf'));
 value.set('extra',new File(['x'],'extra.pdf'));
 assert.deepEqual(forms.validateFormSubmit(value),{ok:false,reason:'files'});
 for(const field of ['botcheck']){
  const bot=data();bot.set(field,'on');
  assert.deepEqual(forms.validateFormSubmit(bot),{ok:false,reason:'honeypot'});
 }
});
test('every enquiry form emits its provider fields and has a thank-you page',()=>{
 const kinds=new Set();
 for(const file of fs.readdirSync(new URL('../dist/',import.meta.url),{recursive:true}).filter(f=>f.endsWith('.html'))){
  const html=fs.readFileSync(new URL(`../dist/${file}`,import.meta.url),'utf8');
  assert.ok(!html.includes('api.staticforms.dev'),file);
  assert.ok(!html.includes('data-local-only-form'),file);
  for(const [markup,kind] of [...html.matchAll(/<form[^>]*data-form-submit="([^"]+)"[\s\S]*?<\/form>/g)].map(m=>[m[0],m[1]])){
   kinds.add(kind);
   assert.match(markup,/action="https:\/\/api.web3forms.com\/submit"/);
   for(const field of ['access_key','subject','redirect','botcheck','email'])assert.ok(markup.includes(`name="${field}"`),`${file}: ${field}`);
   assert.ok(markup.includes('name="access_key" value="87d4dc81-dc01-415e-8050-426d0824b6a0"'));
   for(const field of ['_next','_subject','_honey','_template'])assert.ok(!markup.includes(`name="${field}"`));
   assert.match(markup,/method="post"/);assert.match(markup,/enctype="multipart\/form-data"/);
   assert.ok(!markup.includes('name="apiKey"')&&!markup.includes('name="_captcha"'));
   const next=new URL(forms.formSubmitSettings(kind,'https://example.com/').next).pathname;
   const thanks=fs.readFileSync(new URL(`../dist${next}index.html`,import.meta.url),'utf8');
   assert.match(thanks,/<h1>/);assert.match(thanks,/name="robots" content="noindex,follow"/);
  }
 }
 // New pages may reuse a form (for example, the style-guide preview).
 // Validate every instance above and require all six purposes without fixing the total.
 assert.equal(kinds.size,6);
});
test('editing a form or failing browser validation clears an earlier status',()=>{
 const form=new EventTarget(),status={textContent:''};forms.bindFormStatusReset(form,status);
 for(const event of ['input','change','invalid']){status.textContent='Uw bericht wordt verzonden…';form.dispatchEvent(new Event(event));assert.equal(status.textContent,'');}
});
