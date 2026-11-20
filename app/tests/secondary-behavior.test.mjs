import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

test('project selection reads the source query and rejects unknown groups',async()=>{
 const file=new URL('../public/secondary-behavior.mjs',import.meta.url);assert.ok(fs.existsSync(file),'secondary behavior exists');
 const {selectedProjectGroup}=await import(file);
 assert.equal(selectedProjectGroup('?filter_projectgroup%5B%5D=2'),'2');
 assert.equal(selectedProjectGroup('?filter_projectgroup%5B%5D=3'),'3');
 assert.equal(selectedProjectGroup('?filter_projectgroup%5B%5D=99'),null);
 assert.equal(selectedProjectGroup(''),null);
});
test('project galleries clamp at both ends including empty galleries',async()=>{
 const file=new URL('../public/secondary-behavior.mjs',import.meta.url);assert.ok(fs.existsSync(file),'secondary behavior exists');
 const {projectGalleryIndex}=await import(file);let i=0;
 const sequence=[i];for(let n=0;n<6;n++){i=projectGalleryIndex(i,1,5);sequence.push(i)}
 assert.deepEqual(sequence,[0,1,2,3,4,4,4]);assert.equal(projectGalleryIndex(0,-1,5),0);assert.equal(projectGalleryIndex(3,1,0),0);
});
