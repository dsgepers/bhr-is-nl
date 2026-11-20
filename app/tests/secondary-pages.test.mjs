import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {layout} from '../components.mjs';

const protectedHashes=JSON.parse(fs.readFileSync(new URL('./fixtures/secondary-protected-hashes.json',import.meta.url)));
test('secondary foundation exposes strict dispatch and media lookup',async()=>{
 const target=new URL('../secondary-pages.mjs',import.meta.url);
 assert.ok(fs.existsSync(target),'secondary route renderer must exist');
 const {secondaryPage,secondaryOptions}=await import(target);
 const {secondaryMedia,validateSecondaryContent}=await import('../secondary-data.mjs');
 assert.throws(()=>secondaryPage('/unknown-secondary-route'),/Unknown/);
 assert.throws(()=>secondaryOptions('/unknown-secondary-route'),/Unknown/);
 assert.throws(()=>secondaryMedia('https://www.bhr-is.nl/media/images/other/437_dsc02673.webp'),/exact|Unknown/);
 assert.throws(()=>secondaryMedia('toString'),/exact|Unknown/);
 assert.throws(()=>secondaryOptions('constructor'),/Unknown/);
 assert.throws(()=>validateSecondaryContent([['/one',{route:'/one'}],['/one',{route:'/one'}]]),/Duplicate/);
});
test('secondary layout loads scoped assets, exact metadata and support links',()=>{
 const html=layout('Example','<h1>Example</h1>','secondary parity-page secondary-parity',true,{documentTitle:'Exact title',canonical:'https://www.bhr-is.nl/example'});
 assert.ok(html.includes('<title>Exact title</title>'));
 assert.ok(html.includes('rel="canonical" href="https://www.bhr-is.nl/example"'));
 assert.ok(html.indexOf('/secondary-parity.css')>html.indexOf('/parity.css'));
 assert.ok(html.includes('src="/secondary.mjs"'));
 assert.ok(html.includes('href="/pagina-niet-gevonden"'));
 assert.ok(html.includes('href="/privacy"'));
 const old=layout('Old','<h1>Old</h1>','secondary parity-page');
 assert.ok(!old.includes('/secondary.mjs')&&!old.includes('/secondary-parity.css'));
 assert.ok(old.includes('href="/privacyverklaring"'));
});
// Expertises was explicitly updated for step-specific photos after the parity phase;
// only its baseline was refreshed. The other eleven retain their original hashes.
test('all twelve protected HTML outputs retain their approved hashes',()=>{
 for(const [route,expected] of Object.entries(protectedHashes)){
  const html=fs.readFileSync(new URL(`../dist${route==='/'?'':route}/index.html`,import.meta.url));
  assert.equal(createHash('sha256').update(html).digest('hex'),expected,route);
 }
});

const expected=JSON.parse(fs.readFileSync(new URL('./fixtures/secondary-pages.json',import.meta.url)));
const {readBody,assertInOrder}=await import('./secondary-helpers.mjs');
for(const [route,reference] of Object.entries(expected))test(`${route} source composition`,()=>{
 const html=readBody(route);assertInOrder(html,reference.headings);
 for(const src of reference.images)assert.ok(html.includes(src),`${route}: missing original ${src}`);
});
test('about restores the visible banner slogan even though the CMS used a div',()=>{
 const html=readBody('/over-ons');assert.match(html,/<h1>Over ons<\/h1>/);assert.ok(html.includes('Your system inte'));
 assert.ok(html.includes('data-banner-index="0"')&&html.includes('data-banner-index="1"'));
});
test('FAQ answers preserve the verified besturingskasten link instead of the broken CMS token',()=>{
 const html=readBody('/veelgestelde-vragen');assert.ok(html.includes('href="/expertises/paneelbouw">elektrische besturingskasten</a>'));
 assert.ok(!html.includes('%7B1%3ADocument%3A16%7D'));
});
test('source layouts retain alternating article columns and static branch overviews',async()=>{
 const {secondaryPage}=await import('../secondary-pages.mjs');
 const content=JSON.parse(fs.readFileSync(new URL('../secondary-content.json',import.meta.url)));
 const layouts=JSON.parse(fs.readFileSync(new URL('./fixtures/secondary-layouts.json',import.meta.url)));
 for(const [route,expected] of Object.entries(layouts)){
  for(const index of expected.reverseArticles)assert.equal(content[route].blocks[index].reverse,true,route+' block '+index+' must put its photo on the right');
  for(const index of expected.staticBranches){assert.equal(content[route].blocks[index].carousel,false,route+' needs a wrapping grid');assert.ok(secondaryPage(route).includes('secondary-cards-static'));}
 }
});

test('partner sliders begin with original Siemens and Eplan items rather than cloned tail items',()=>{
 const content=JSON.parse(fs.readFileSync(new URL('../secondary-content.json',import.meta.url)));
 for(const [route,s]of Object.entries(content))for(const b of s.blocks||[])if(b.kind==='partners'){assert.match(b.items[0].image.src,/44_partner2/,route);assert.match(b.items[1].image.src,/45_partner3/,route);}
});
test('vacancy process cards retain the source recruiting explanations',()=>{
 for(const route of ['/vacature/monteur-paneelbouw','/vacature/junior-e-plan-engineer']){
  const html=readBody(route);for(const text of ['Onze recruiters bekijken uw sollicitatie zorgvuldig.','Zien we een mogelijke match?','Zijn we allebei enthousiast?','Is het een match? Dan ontvangt u een aanbod'])assert.ok(html.includes(text),route+': '+text);
 }
});
test('Etten-Leur preserves its article within the location content column',()=>{
 const html=readBody('/locaties/betrouwbare-paneelbouw-voor-industriele-installaties-in-etten-leur');assert.ok(html.includes('secondary-narrow-article'));
});
test('featured vacancy sections retain introductory text and the vacancy listing link',()=>{
 const about=readBody('/over-ons');assert.ok(about.includes('Binnen een hecht team')||about.includes('binnen een hecht team'));
 for(const route of ['/over-ons','/de-mensen-achter-de-techniek'])assert.ok(readBody(route).includes('Bekijk alle vacatures'),route);
});
test('branch slider headers keep their source label and right-hand navigation',()=>{
 const html=readBody('/expertises/cybersecurity');assert.ok(html.includes('Onze branches'));
 assert.match(html,/secondary-cards-intro[\s\S]*?Al onze diensten/);
});
test('industry FAQ sections retain their link to the full question overview',()=>{
 assert.ok(readBody('/branches/productie-industrie').includes('Bekijk meer veelgestelde vragen'));
});
test('job descriptions retain separate source text groups and their paragraph boundaries',()=>{
 for(const route of ['/vacature/monteur-paneelbouw','/vacature/junior-e-plan-engineer'])assert.equal((readBody(route).match(/class="secondary-job-text"/g)||[]).length,2,route);
});
test('source inline article actions keep their compact treatment',()=>{
 assert.match(readBody('/de-mensen-achter-de-techniek'),/class="button inline"[^>]*>Over BHR/);
});
test('Dongen article descriptions keep the source paragraph indentation',()=>{
 assert.equal((readBody('/paneelbouwer-dongen').match(/class="secondary-indent"/g)||[]).length,3);
});
