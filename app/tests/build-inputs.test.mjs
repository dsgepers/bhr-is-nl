import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

test('page image selection works from source data without local reference captures',()=>{
 const app=fileURLToPath(new URL('../',import.meta.url));
 const clean=fs.mkdtempSync(path.join(os.tmpdir(),'bhr-build-inputs-'));
 try{
  // Isolate the data module with its distributable JSON inputs, without captures.
  for(const file of fs.readdirSync(app).filter(file=>file.endsWith('.json')||file==='data.mjs')){
   fs.copyFileSync(path.join(app,file),path.join(clean,file));
  }
  const result=spawnSync(process.execPath,['--input-type=module','-e',`
   import assert from 'node:assert/strict';
   import {pageImage} from './data.mjs';
   assert.equal(pageImage('/expertises/software-engineering','Software die begint bij het complete proces','/assets/fallback.webp'),'/assets/images/585_dsc02701.webp');
   assert.equal(pageImage('/missing','Unknown','/assets/fallback.webp'),'/assets/fallback.webp');
  `],{cwd:clean,encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
 }finally{fs.rmSync(clean,{recursive:true,force:true})}
});
