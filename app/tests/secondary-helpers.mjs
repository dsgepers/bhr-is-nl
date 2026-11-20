import fs from 'node:fs';
import assert from 'node:assert/strict';
export const readBody=route=>fs.readFileSync(new URL(`../dist${route==='/'?'':route}/index.html`,import.meta.url),'utf8').split('<div id="page-content">')[1].split('</div><footer')[0];
export const plainText=html=>html.replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/&#39;/g,"'").replace(/&quot;/g,'"').replace(/\s+/g,' ').trim();
export function assertInOrder(html,texts){let pos=-1;const text=plainText(html);for(const label of texts){const next=text.indexOf(label,pos+1);assert.ok(next>pos,`Missing or misplaced: ${label}`);pos=next}}
