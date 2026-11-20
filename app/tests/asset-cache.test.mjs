import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';

test('process-slider pages cannot reuse CSS or modules cached before their latest build',()=>{
 for(const route of ['expertises','afspraak-maken']){
  const html=fs.readFileSync(new URL(`../dist/${route}/index.html`,import.meta.url),'utf8');
  const assets=[...html.matchAll(/(?:src|href)="(\/[^"?]+\.(?:css|mjs))(\?[^" ]*)?"/g)];
  assert.ok(assets.some(([,path])=>path==='/site.mjs'),route);
  for(const [,path,query=''] of assets){
   const version=new URLSearchParams(query.slice(1)).get('v');
   assert.ok(version,`${route}: ${path} must bypass stale cached assets`);
   const file=fs.readFileSync(new URL(`../dist${path}`,import.meta.url));
   assert.equal(version,createHash('sha256').update(file).digest('hex').slice(0,12),`${route}: ${path} must identify its current bytes`);
  }
 }
});
