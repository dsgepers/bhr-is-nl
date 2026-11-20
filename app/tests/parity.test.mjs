import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import * as behavior from '../public/behavior.mjs';

const page=route=>fs.readFileSync(new URL(`../dist/${route}/index.html`,import.meta.url),'utf8');
const inOrder=(html,labels)=>{let at=-1;for(const text of labels){const next=html.indexOf(text,at+1);assert.ok(next>at,`Missing or misplaced: ${text}`);at=next}};

test('expertises exposes its complete service overview before the process and recommendations',()=>{
 const html=page('expertises');
 inOrder(html,['Onze expertises','Inbedrijfstelling','Industriële automatisering','Hoe BHR werkt','Complete oplossingen voor elke installatie','Slimme automatisering in de praktijk','Direct een offerte aanvragen?']);
 assert.ok(html.includes('437_dsc02673.webp'),'the process photo must be packaged');
 assert.ok(html.includes('data-carousel="steps"'),'the process controls must have a track');
 assert.ok(html.includes('Wij denken mee vanaf het begin. Met onze ervaring'),'the process cards must include their explanatory copy');
});
test('nested machine-builders route preserves original photos and the distinct lead band',()=>{
 const html=page('voor-machinebouwers/voor-machinebouwers');
 assert.ok(html.includes('parity-lead'),'the lead is distinct from the hero');
 for(const name of ['851_dsc01712','783_dsc01720','779_dsc02362','777_dsc00987','775_dsc02204','781_dsc02826'])assert.ok(html.includes(name),name);
 inOrder(html,['Seriematige paneelbouw','Efficiënte techniek','De kwaliteit van het proces','BHR Industrial Solutions: een partner','Samen bouwen','Kunnen we u helpen']);
});
test('process page retains specific photos and places its callout before the last article',()=>{
 const html=page('voor-machinebouwers/proces-productie');
 for(const name of ['848_dsc01159','771_dsc01350','773_dsc02153','769_dsc02091'])assert.ok(html.includes(name),name);
 inOrder(html,['Waarom kiezen voor BHR','Wat kunnen wij voor','BHR Industrial Solutions: partner','Wij helpen u graag verder']);
});
test('service renders the photographic testimonial and an explicit two-field contact form',()=>{
 const html=page('service-en-onderhoud');
 assert.ok(html.includes('451_dsc02462.webp'));
 assert.ok(html.includes('parity-testimonial'));
 const form=html.match(/<form[^>]*data-form-kind="quick"[\s\S]*?<\/form>/)?.[0];
 assert.ok(form,'quick contact is an explicit variant');
 assert.ok(form.includes('name="company"')&&form.includes('name="email"'));
 assert.ok(!form.includes('name="phone"')&&!form.includes('name="message"'));
});
test('partners uses its original hero and eight logical logos in a controlled strip',()=>{
 const html=page('over-ons/partners');
 assert.ok(html.includes('866_dsc02204.webp'));
 assert.ok(html.includes('data-carousel="partners"'));
 assert.equal([...html.matchAll(/data-partner=/g)].length,8);
 inOrder(html,['Partners van BHR','Onze samenwerkingen','Klaar om uw project','Samenwerken doen we graag!']);
});
test('careers preserves distinct fact photos and offers the captured application choices',()=>{
 const html=page('over-ons/werken-bij');
 for(const name of ['857_dsc02261','787_dsc02462','785_dsc00930','816_dsc01886','819_dsc02091','820_dsc02701','822_dsc02552','824_dsc01048','1120_dsc02091'])assert.ok(html.includes(name),name);
 inOrder(html,['Uitgelichte vacatures','Dit is BHR','Wat ons drijft','Maak vandaag nog kennis','Bouw mee aan jouw toekomst','Sollicitatieformulier']);
 for(const name of ['birth_day','birth_month','birth_year'])assert.ok(html.includes(`name="${name}"`),name);
 assert.ok(html.includes('Junior E-Plan Engineer')&&html.includes('Monteur Paneelbouw'));
});
test('split date values serialize real calendar dates and reject impossible or partial dates',()=>{
 assert.equal(behavior.birthDateValue?.('29','2','2000'),'2000-02-29');
 for(const date of [['29','2','2001'],['31','4','2000'],['','2','2000'],['0','1','2000']])assert.equal(behavior.birthDateValue?.(...date),null);
});
test('parity styling is opt-in and leaves the homepage and other templates on their original styles',()=>{
 for(const route of ['expertises','voor-machinebouwers/voor-machinebouwers','voor-machinebouwers/proces-productie','service-en-onderhoud','over-ons/partners','over-ons/werken-bij'])assert.ok(page(route).includes('/parity.css'),route);
 for(const route of ['','expertises/paneelbouw'])assert.ok(!page(route).includes('/parity.css'),route);
});

test('quote decisions preserve the captured products, prompts and optional steps',()=>{
 const html=page('expertises');
 const expected=[
  ['Agrarisch','Chemie','Bouw','Industrie','Recycling','Food','Overig'],
  ['','Wandmontage','Staand op de vloer','Ingebouwd','Retrofit','Speciaal','Overig'],
  ['','Kunststof','Plaatstaal','RVS','Weet ik nog niet','Overig'],
  ['','Eenvoudig zonder PLC','Eenvoudig met PLC','Relatief eenvoudig met PLC','Relatief eenvoudig zonder PLC','Complex','Weet ik niet','Overig'],
  ['','Nee','Ja, 7"','Ja, 10"','Ja, 12"','Groter dan 12"'],
  ['','Klein: 30x30cm','Klein-middel: 50x50cm','Middel: 120x120cm','Middel-groot: 60x220cm','Groot: 120x220cm','Weet ik niet','Overig'],
  ['','Nederland','Europa','Amerika','Overig'],
 ];
 const decode=s=>s.replace(/&quot;/g,'"').replace(/&amp;/g,'&');
 for(let i=0;i<7;i++){
  const select=html.match(new RegExp(`<select name="\\$specificatie_${i}"[^>]*>[\\s\\S]*?<\\/select>`))?.[0];assert.ok(select,`decision ${i+1}`);
  const values=[...select.matchAll(/<option(?: value="([^"]*)")?>([^<]*)<\/option>/g)].map(m=>m[1]!==undefined?decode(m[1]):decode(m[2]));
  assert.deepEqual(values,expected[i],`available choices for decision ${i+1}`);
  assert.equal(/<select[^>]*\brequired\b/.test(select),[true,true,true,false,false,true,false][i]);
 }
});
test('careers calls to action reach the article and application on this page',()=>{
 const html=page('over-ons/werken-bij');
 assert.match(html,/<a[^>]*href="#werken-bij"[^>]*>Lees verder<\/a>/);
 assert.match(html,/<a[^>]*href="#contactformulier"[^>]*>Solliciteer nu<\/a>/);
 assert.ok(html.includes('parity-location'));
});
test('parity form requirements match their visible contact and application fields',()=>{
 for(const route of ['voor-machinebouwers/voor-machinebouwers','voor-machinebouwers/proces-productie','over-ons/partners']){
  const textarea=page(route).match(/<textarea[^>]*name="message"[^>]*>/)?.[0];assert.ok(textarea);assert.ok(!textarea.includes('required'),`${route}: message is optional`);
 }
 const job=page('over-ons/werken-bij');
 for(const name of ['cv','bewaren','vacature'])assert.match(job,new RegExp(`<(?:input|select)[^>]*name="${name}"[^>]*\\brequired\\b`),`${name} is required`);
});
test('a looping carousel wraps both ways without changing bounded step navigation',()=>{
 assert.equal(behavior.carouselTarget?.(7,1,8,true),0);
 assert.equal(behavior.carouselTarget?.(0,-1,8,true),7);
 assert.equal(behavior.carouselTarget?.(2,1,3,false),2);
 assert.equal(behavior.carouselTarget?.(0,-1,3,false),0);
});
