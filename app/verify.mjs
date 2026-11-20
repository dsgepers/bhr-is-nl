import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';

const base=(process.env.PAGES_BASE_PATH||'').replace(/\/$/,'');
const localPath=value=>{
 assert.ok(!base||value===base||value.startsWith(base+'/'),`URL escapes Pages base: ${value}`);
 return base?value.slice(base.length)||'/':value;
};
const dist=new URL('./dist/',import.meta.url),root=fileURLToPath(dist);
const htmlFiles=fs.readdirSync(dist,{recursive:true}).filter(file=>file.endsWith('.html'));
let links=0,assets=0;
for(const file of htmlFiles){
 const html=fs.readFileSync(new URL(file,dist),'utf8');
 const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(new Set(ids).size,ids.length,`${file}: duplicate element IDs`);
 assert.equal([...html.matchAll(/<h1(?:\s[^>]*)?>/g)].length,1,`${file}: expected one main heading`);
 for(const match of html.matchAll(/\b(href|src)="([^"]+)"/g)){
  const [,attribute,value]=match;
  if(/^(?:https?:|mailto:|tel:|data:|\/\/)/.test(value)){
   if(attribute==='src')throw Error(`${file}: external asset ${value}`);
   continue;
  }
  if(value==='#')continue;
  const url=new URL(value,'https://local.invalid'+base+'/'+file.replace(/index\.html$/,''));
  let local=path.join(root,decodeURIComponent(localPath(url.pathname)));
  if(fs.existsSync(local)&&fs.statSync(local).isDirectory())local=path.join(local,'index.html');
  assert.ok(fs.existsSync(local),`${file}: missing destination ${value}`);
  if(url.hash){
   const target=fs.readFileSync(local,'utf8');
   assert.ok(target.includes(`id="${decodeURIComponent(url.hash.slice(1))}"`),`${file}: missing anchor ${value}`);
  }
  attribute==='href'?links++:assets++;
 }
}
const pages=JSON.parse(fs.readFileSync(new URL('search-index.json',dist)));
assert.equal(new Set(pages.map(p=>p.url)).size,pages.length,'duplicate routes');
for(const page of pages)assert.ok(fs.existsSync(path.join(root,localPath(page.url),'index.html')),`missing page ${page.url}`);
console.log(`Verified ${pages.length} routes, ${links} local links and ${assets} image/script references.`);
