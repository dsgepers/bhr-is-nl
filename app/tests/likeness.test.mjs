import {test} from 'node:test';
import assert from 'node:assert/strict';
import {reviewPage,parseJournal} from '../tools/check-subpage-likeness.mjs';

// Only measured Craft evidence may supply a score. High scores on a different
// route, or on two widths, must never make an unchecked page appear to pass.
const route='/expertises/software-engineering';
function evidence(path=route,scores=[0.90,0.90,0.90]){
 const widths=[1440,768,390];
 return [
  {id:'original',operation:'web_site_capture',result:{url:`https://www.bhr-is.nl${path}`,screenshots:widths.map(width=>({css_width:width,width,height:1000,cut:false,sha256:`original-${width}`}))}},
  {id:'rebuilt',operation:'web_site_capture',result:{url:`http://127.0.0.1:8080${path}`,screenshots:widths.map(width=>({css_width:width,width,height:1000,cut:false,sha256:`rebuilt-${width}`}))}},
  ...widths.map((width,i)=>({id:`comparison-${width}`,operation:'web_pixels_compare',params:{before_sha256:`original-${width}`,after_sha256:`rebuilt-${width}`},result:{comparable:true,width,height:1000,sizes:{before:{width,height:1000},after:{width,height:1000}},layout_similarity:scores[i],perceptual_similarity:scores[i]}}))
 ];
}

test('missing subpage screenshots remain blocked with no invented score',()=>{
 const result=reviewPage(route,[]);
 assert.equal(result.status,'blocked');
 assert.equal(result.similarity,null);
 assert.match(result.reason,/original.*capture/i);
});

test('homepage evidence cannot satisfy a subpage likeness requirement',()=>{
 assert.equal(reviewPage(route,evidence('/',[1,1,1])).status,'blocked');
});

test('90% passes only when all required widths have measured comparisons',()=>{
 const result=reviewPage(route,evidence());
 assert.equal(result.status,'passed');
 assert.equal(result.similarity,90);
 assert.deepEqual(result.widths.map(row=>row.width),[1440,768,390]);
 const incomplete=evidence().filter(row=>row.id!=='comparison-390');
 assert.equal(reviewPage(route,incomplete).status,'blocked');
});

test('a sub-90% result fails even when the other widths score 100%',()=>{
 const result=reviewPage(route,evidence(route,[1,1,0.8999]));
 assert.equal(result.status,'failed');
 assert.ok(result.similarity<90);
});

test('comparisons must reference the screenshots of the same original and rebuilt page',()=>{
 const rows=evidence();
 rows[2].params.after_sha256='different-screenshot';
 assert.equal(reviewPage(route,rows).status,'blocked');
});

test('invalid or incomparable pixel results cannot pass',()=>{
 for(const invalid of [null,undefined,NaN,Infinity,-1,1.01,'0.99']){
  const rows=evidence();
  rows[2].result.perceptual_similarity=invalid;
  assert.equal(reviewPage(route,rows).status,'blocked');
 }
 const rows=evidence();
 rows[2].result.comparable=false;
 assert.equal(reviewPage(route,rows).status,'blocked');
});

test('an older high-scoring capture cannot override a newer failing capture',()=>{
 const older=evidence(route,[1,1,1]),newer=evidence(route,[0.80,0.80,0.80]);
 for(const capture of newer.filter(row=>row.operation==='web_site_capture')){
  for(const shot of capture.result.screenshots)shot.sha256+='-new';
 }
 for(const comparison of newer.filter(row=>row.operation==='web_pixels_compare')){
  comparison.params.before_sha256+='-new';
  comparison.params.after_sha256+='-new';
 }
 assert.equal(reviewPage(route,[...older,...newer]).status,'failed');
});

test('Craft journal events may be concatenated without line separators',()=>{
 const text='{"caller":"mcp","params":{"text":"braces }{ and \\\"quotes\\\""}}{"caller":"ui","ok":true}\n';
 assert.deepEqual(parseJournal(text),[{caller:'mcp',params:{text:'braces }{ and "quotes"'}},{caller:'ui',ok:true}]);
 assert.throws(()=>parseJournal('{"caller":"unfinished"'),/journal|JSON/i);
});

test('truncated original or rebuilt page captures cannot pass as full-page checks',()=>{
 for(const captureIndex of [0,1]){
  const rows=evidence();
  rows[captureIndex].result.screenshots[0].cut=true;
  assert.equal(reviewPage(route,rows).status,'blocked');
 }
});

test('comparisons of cropped areas cannot stand in for the whole screenshots',()=>{
 const rows=evidence();
 rows[2].result.height=500;
 assert.equal(reviewPage(route,rows).status,'blocked');
});

test('unmatched page height reduces the score rather than disappearing from the check',()=>{
 const rows=evidence(route,[1,1,1]);
 rows[1].result.screenshots[0].height=2000;
 rows[2].result.sizes.after.height=2000;
 const result=reviewPage(route,rows);
 assert.equal(result.status,'failed');
 assert.equal(result.similarity,50);
});
