import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {layout} from '../components.mjs';

test('every page exposes media-guarded mobile styles and one deferred mobile enhancement',()=>{
 const html=layout('Mobile check','<h1>Mobile check</h1>','home');
 assert.match(html,/<link rel="stylesheet" href="\/mobile-parity\.css" media="\(max-width: 1199px\)">/);
 assert.match(html,/<script type="module" src="\/mobile\.mjs"><\/script>/);
 assert.equal([...html.matchAll(/src="\/mobile\.mjs"/g)].length,1);
 assert.ok(html.indexOf('/mobile-parity.css')>html.indexOf('/responsive.css'));
});

test('mobile assets are packaged on every generated route with a content version',()=>{
 const pages=JSON.parse(fs.readFileSync(new URL('../dist/search-index.json',import.meta.url)));
 for(const {url} of pages){
  const html=fs.readFileSync(new URL(`../dist${url==='/'?'':url}/index.html`,import.meta.url),'utf8');
  for(const name of ['mobile-parity.css','mobile.mjs'])assert.ok(html.includes(`/${name}?v=`),`${url}: ${name}`);
 }
});
