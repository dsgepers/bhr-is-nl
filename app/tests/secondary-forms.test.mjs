import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=route=>fs.readFileSync(new URL(`../dist${route}/index.html`,import.meta.url),'utf8');
const fixture=JSON.parse(fs.readFileSync(new URL('./fixtures/secondary-pages.json',import.meta.url)));
const decode=s=>s.replaceAll('&quot;','"').replaceAll('&amp;','&').replaceAll('&#39;',"'");
test('standalone quote retains every captured option including empty prompts',()=>{
 const html=read('/offerteaanvraag');
 const expected=fixture['/offerteaanvraag'].fields.filter(f=>f.tag==='SELECT');
 assert.equal(expected.length,7);
 for(const [i,field] of expected.entries()){
  const select=html.match(new RegExp(`<select name="\\$specificatie_${i}"[^>]*>[\\s\\S]*?<\\/select>`))?.[0];assert.ok(select);
  const options=[...select.matchAll(/<option[^>]*>([\s\S]*?)<\/option>/g)].map(m=>decode(m[1]));
  assert.deepEqual(options,field.options.map(o=>o.text),field.label);
  assert.equal(/ required/.test(select),field.semanticRequired);
 }
 assert.ok(html.includes('name="subject" value="Offerteaanvraag BHR"'));
});
test('newsletter and alternate quote now use their own Web3Forms purposes',()=>{
 for(const [route,kind] of [['/nieuws','newsletter'],['/test','quote']]){
  const html=read(route),form=html.match(new RegExp(`<form[^>]*data-form-submit="${kind}"[\\s\\S]*?<\\/form>`))?.[0];
  assert.ok(form,route);assert.match(form,/action="https:\/\/api.web3forms.com\/submit"/);
  assert.ok(!form.includes('data-local-only-form'));
  assert.match(form,/<button[^>]*type="submit"[^>]*disabled/);
 }
});
test('vacancy applications keep delivery names, correct job choice and truthful upload limit',()=>{
 for(const [route,title] of [['/vacature/junior-e-plan-engineer','Junior E-Plan Engineer'],['/vacature/monteur-paneelbouw','Monteur Paneelbouw']]){
  const html=read(route);
  for(const name of ['firstname','lastname','email','phone','birth_day','birth_month','birth_year','birthdate','bewaren','vacature','attachment','privacy'])assert.ok(html.includes(`name="${name}"`),name);
  assert.ok(html.includes('name="subject" value="Sollicitatieformulier"'));
  assert.ok(html.includes(`name="vacature" value="${title}"`));assert.ok(!html.includes('<select name="vacature"'));assert.ok(html.includes('4MB')&&!html.includes('10MB'));
  assert.equal([...html.matchAll(/<aside class="secondary-employee"/g)].length,1,'the application must not invent a second employee card');
  assert.ok(html.includes('href="#form_2"')&&html.includes('id="form_2"'));
 }
});
