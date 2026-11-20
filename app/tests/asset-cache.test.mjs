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

test('form delivery modules and recipient settings bypass stale cached versions',()=>{
 for(const [file,dependency] of [['site.mjs','behavior.mjs'],['behavior.mjs','config.js']]){
  const source=fs.readFileSync(new URL(`../dist/${file}`,import.meta.url),'utf8');
  const match=source.match(new RegExp(`from ['"]\\./${dependency.replace('.', '\\.')}\\?v=([a-f0-9]+)['"]`));
  assert.ok(match,`${file} must version ${dependency}`);
  const actual=createHash('sha256').update(fs.readFileSync(new URL(`../dist/${dependency}`,import.meta.url))).digest('hex').slice(0,12);
  assert.equal(match[1],actual);
 }
 for(const route of ['contact','nieuws','test','over-ons/werken-bij']){
  const html=fs.readFileSync(new URL(`../dist/${route}/index.html`,import.meta.url),'utf8');
  assert.match(html,/src="\/site\.mjs\?v=[a-f0-9]+"/);
 }
});
