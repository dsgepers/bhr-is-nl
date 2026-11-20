import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';

const root=path.resolve(import.meta.dirname,'..');
test('Agro retains its captured questions and application process',()=>{
 const page=fs.readFileSync(path.join(root,'dist/branches/agro/index.html'),'utf8');
 assert.equal([...page.matchAll(/<details>/g)].length,4);
 for(const title of ['Uw sollicitatie','Telefonisch contact','Kennismakingsgesprek','Aan de slag'])assert.ok(page.includes(`<h3>${title}</h3>`));
});
test('About and Vacatures retain available original content and photos',()=>{
 const about=fs.readFileSync(path.join(root,'dist/over-ons/index.html'),'utf8');
 assert.ok(about.replace(/<[^>]*>/g,'').replace(/\s+/g,' ').includes('Bij Aqualab Zuid werken wij inmiddels meer dan drie jaar samen met BHR Industrial Solutions B.V.'));
 const vacancy=fs.readFileSync(path.join(root,'dist/vacature/index.html'),'utf8');
 assert.ok(vacancy.includes('<h1>Bouw mee aan jouw toekomst in de techniek</h1>'));
 const partners=fs.readFileSync(path.join(root,'dist/over-ons/partners/index.html'),'utf8');
 assert.ok(partners.includes('src="/assets/images/866_dsc02204.webp"'));
});
test('Paneelbouw project recommendations retain working links and no markup text',()=>{
 const page=fs.readFileSync(path.join(root,'dist/expertises/paneelbouw/index.html'),'utf8');
 assert.ok(!page.includes('###'));
 for(const route of ['/projecten/bouwen-afdelingsinstallatie','/projecten/cummins','/projecten/retrofit-oplossingen-in-bestaande-machineframe'])assert.ok(page.includes(`href="${route}"`));
});
test('form templates let Web3Forms use the visitor email as the reply address',()=>{
 const page=fs.readFileSync(path.join(root,'dist/contact/index.html'),'utf8');
 assert.ok(!page.includes('name="replyTo" value="@"'));
 assert.ok(page.includes('name="email"'));
});
test('inner pages retain their individual original copy, lists and FAQ answers',()=>{
 const page=fs.readFileSync(path.join(root,'dist/expertises/software-engineering/index.html'),'utf8');
 assert.ok(page.includes('We starten niet in de code, maar bij jouw proces.'));
 assert.ok(page.replace(/<[^>]*>/g,'').includes('Strakke kasten met logische signaalstructuur'));
 assert.ok(page.includes('Wat doet een software engineer in industriële automatisering?'));
 const questions=fs.readFileSync(path.join(root,'dist/veelgestelde-vragen/index.html'),'utf8');
 assert.equal([...questions.matchAll(/<details>/g)].length,20);
 const hardware=fs.readFileSync(path.join(root,'dist/expertises/hardware-engineering/index.html'),'utf8');
 assert.ok(hardware.includes('<h1>Hardware engineering als basis voor betrouwbare productie</h1>'));
});
test('every generated image, font and background is available without the original server',()=>{
 const files=fs.readdirSync(path.join(root,'dist'),{recursive:true}).filter(f=>/\.(html|css)$/.test(f));
 let assets=0;
 for(const file of files){
  const content=fs.readFileSync(path.join(root,'dist',file),'utf8');
  const refs=[...content.matchAll(/(?:src|href)="([^"]+)"|url\(['"]?([^)'"\s]+)['"]?\)/g)].map(m=>m[1]||m[2]);
  for(const ref of refs.filter(r=>/\.(webp|png|jpe?g|svg|ico|woff2?)(?:\?|$)/i.test(r))){
   assert.ok(!/^https?:/.test(ref),`${file} depends on remote asset ${ref}`);
   assert.ok(fs.existsSync(path.join(root,'dist',ref.replace(/^\//,''))),`${file} is missing ${ref}`);assets++;
  }
 }
 assert.ok(assets>100,'all pages should contain their local media');
 const manifest=JSON.parse(fs.readFileSync(path.join(root,'assets-manifest.json')));
 for(const asset of Object.values(manifest)){
  const bytes=fs.readFileSync(path.join(root,'public',asset.path));
  assert.equal(createHash('sha256').update(bytes).digest('hex'),asset.sha256);
 }
});

test('forms cannot submit before client validation and sending handlers are ready',()=>{
 for(const route of ['contact','expertises','expertises/paneelbouw','over-ons/werken-bij']){
  const page=fs.readFileSync(path.join(root,'dist',route,'index.html'),'utf8');
  const forms=[...page.matchAll(/<form class="static-form[\s\S]*?<\/form>/g)].map(m=>m[0]);
  assert.ok(forms.length,`${route} must contain the expected form`);
  for(const form of forms){
   const buttons=[...form.matchAll(/<button[^>]*type="submit"[^>]*>/g)].map(m=>m[0]);
   assert.ok(buttons.length);
   assert.ok(buttons.every(button=>/\sdisabled(?:[\s=>])/.test(button)),`${route} can send a native POST before redirect configuration`);
   assert.match(form,/<noscript>[\s\S]*href="mailto:info@bhr-is.nl"[\s\S]*<\/noscript>/);
  }
 }
});
