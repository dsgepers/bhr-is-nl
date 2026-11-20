import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const paths = new URL('../public/paths.mjs', import.meta.url);
test('Pages path helpers are available',()=>assert.ok(fs.existsSync(paths),'Pages path helpers missing'));
test('repository URLs preserve anchors, query strings and external links',async()=>{
 const {siteUrl,siteMarkup,routePath}=await import(paths);
 assert.equal(siteUrl('/contact?q=a#form','/bhr-is-nl'),'/bhr-is-nl/contact?q=a#form');
 assert.equal(siteUrl('/','/bhr-is-nl'),'/bhr-is-nl/');
 for(const url of ['#form','mailto:info@bhr-is.nl','https://example.com/a','//example.com/a','./icons.mjs'])assert.equal(siteUrl(url,'/bhr-is-nl'),url);
 assert.equal(siteUrl('/contact',''),'/contact');
 assert.equal(siteUrl('/bhr-is-nl/contact','/bhr-is-nl'),'/bhr-is-nl/contact');
 assert.equal(siteMarkup('<a href="/"><img src="/assets/a.svg"></a>','/bhr-is-nl'),'<a href="/bhr-is-nl/"><img src="/bhr-is-nl/assets/a.svg"></a>');
 assert.equal(routePath('/bhr-is-nl/','/bhr-is-nl'),'/');
 assert.equal(routePath('/bhr-is-nl/contact/','/bhr-is-nl'),'/contact');
 assert.equal(routePath('/contact/',''),'/contact');
});

test('Pages preparation prefixes HTML, CSS and JSON values while retaining mobile route keys',async()=>{
 const {preparePages}=await import('../prepare-pages.mjs');
 const {mkdtempSync,rmSync,writeFileSync,readFileSync}=fs;
 const {tmpdir}=await import('node:os');
 const path=await import('node:path');
 const dir=mkdtempSync(path.join(tmpdir(),'bhr-pages-'));
 try{
  writeFileSync(path.join(dir,'index.html'),'<a href="/contact"><img src="/assets/a.svg"></a><div style="background:url(/assets/inline.svg)"></div><form action="https://api.web3forms.com/submit"></form>');
  writeFileSync(path.join(dir,'theme.css'),"a{background:url('/assets/a.svg')}b{mask:url(/assets/b.svg)}");
  writeFileSync(path.join(dir,'mobile-data.json'),JSON.stringify({'/':[{from:'/assets/a.svg',to:'/assets/b.svg'}],'/contact':[]}));
  preparePages(dir,'/bhr-is-nl');
  assert.match(readFileSync(path.join(dir,'index.html'),'utf8'),/href="\/bhr-is-nl\/contact"/);
  assert.match(readFileSync(path.join(dir,'index.html'),'utf8'),/url\(\/bhr-is-nl\/assets\/inline.svg\)/);
  assert.match(readFileSync(path.join(dir,'index.html'),'utf8'),/https:\/\/api.web3forms.com\/submit/);
  assert.match(readFileSync(path.join(dir,'theme.css'),'utf8'),/url\('\/bhr-is-nl\/assets\/a.svg'\)/);
  assert.match(readFileSync(path.join(dir,'theme.css'),'utf8'),/url\(\/bhr-is-nl\/assets\/b.svg\)/);
  const data=JSON.parse(readFileSync(path.join(dir,'mobile-data.json'),'utf8'));
  assert.equal(data['/'][0].from,'/bhr-is-nl/assets/a.svg');
  assert.equal(data['/'][0].to,'/bhr-is-nl/assets/b.svg');
  assert.ok(data['/contact']);
  assert.ok(fs.existsSync(path.join(dir,'.nojekyll')));
 }finally{rmSync(dir,{recursive:true,force:true})}
});
