import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';

export const minimumSimilarity=90;
export const requiredWidths=[1440,768,390];
const appRoot=fileURLToPath(new URL('../',import.meta.url));
const projectRoot=path.dirname(appRoot);
const normalize=pathname=>pathname.replace(/\/+$/,'')||'/';

function matchesCapture(record,route,original){
 if(record.operation!=='web_site_capture')return false;
 try{
  const url=new URL(record.result.url);
  const hosts=original?['bhr-is.nl','www.bhr-is.nl']:['127.0.0.1','localhost','[::1]'];
  return hosts.includes(url.hostname)&&normalize(url.pathname)===normalize(route)&&!url.search;
 }catch{return false;}
}

// Evidence is supplied in journal order. Only the most recent capture for this
// exact route may count; another page's score and older passes are irrelevant.
export function reviewPage(route,evidence){
 const result={route,minimumSimilarity,status:'blocked',similarity:null,widths:[]};
 const original=evidence.findLast(row=>matchesCapture(row,route,true));
 const rebuilt=evidence.findLast(row=>matchesCapture(row,route,false));
 if(!original)return {...result,reason:'Missing original page screenshot capture.'};
 if(!rebuilt)return {...result,reason:'Missing rebuilt page screenshot capture.'};
 if(original.artifactError||rebuilt.artifactError)return {...result,reason:original.artifactError||rebuilt.artifactError};
 for(const width of requiredWidths){
  const before=original.result.screenshots?.find(shot=>shot.css_width===width);
  const after=rebuilt.result.screenshots?.find(shot=>shot.css_width===width);
  if(!before?.sha256||!after?.sha256)return {...result,reason:`Missing screenshot pair at ${width}px.`};
  const fullPage=shot=>shot.cut===false&&shot.width===width&&Number.isSafeInteger(shot.height)&&shot.height>0;
  if(!fullPage(before)||!fullPage(after))return {...result,reason:`Missing complete, uncropped page screenshots at ${width}px.`};
  const comparison=evidence.findLast(row=>row.operation==='web_pixels_compare'&&row.params?.before_sha256===before.sha256&&row.params?.after_sha256===after.sha256);
  const metrics=comparison?.result;
  const valid=value=>typeof value==='number'&&Number.isFinite(value)&&value>=0&&value<=1;
  if(!metrics?.comparable||!valid(metrics.layout_similarity)||!valid(metrics.perceptual_similarity))return {...result,reason:`Missing valid measured comparison at ${width}px.`};
  const sameSize=(size,shot)=>size?.width===shot.width&&size?.height===shot.height;
  if(!sameSize(metrics.sizes?.before,before)||!sameSize(metrics.sizes?.after,after)||metrics.width!==width||metrics.height!==Math.min(before.height,after.height))return {...result,reason:`Comparison does not cover the full screenshot overlap at ${width}px.`};
  // The pixel comparator measures the shared area. Count any unmatched page
  // height as different, so an extra or missing section cannot disappear.
  const coverage=Math.min(before.height,after.height)/Math.max(before.height,after.height);
  const similarity=50*(metrics.layout_similarity+metrics.perceptual_similarity)*coverage;
  result.widths.push({width,similarity,coverage,passed:similarity>=minimumSimilarity,evidenceId:comparison.id});
 }
 result.similarity=Math.min(...result.widths.map(row=>row.similarity));
 result.status=result.widths.every(row=>row.passed)?'passed':'failed';
 result.reason=result.status==='passed'?'All required widths meet 90%.':'At least one required width is below 90%.';
 return result;
}

export function parseJournal(text){
 // Concurrent tool calls can append adjacent objects with no newline. Count
 // complete JSON objects while respecting braces and escapes inside strings.
 const events=[];
 let start=-1,depth=0,inString=false,escaped=false;
 for(let i=0;i<text.length;i++){
  const char=text[i];
  if(start<0){
   if(/\s/.test(char))continue;
   if(char!=='{')throw Error('Invalid Craft journal: expected a JSON object.');
   start=i;
  }
  if(inString){
   if(escaped)escaped=false;
   else if(char==='\\')escaped=true;
   else if(char==='"')inString=false;
  }else if(char==='"')inString=true;
  else if(char==='{')depth++;
  else if(char==='}'&&--depth===0){events.push(JSON.parse(text.slice(start,i+1)));start=-1;}
 }
 if(start>=0)throw Error('Incomplete Craft journal JSON object; retry after the tool finishes.');
 return events;
}

function readEvidence(){
 const base=path.join(projectRoot,'investigation.cany');
 const journal=path.join(base,'journal');
 if(!fs.existsSync(journal))return [];
 const records=[];
 for(const name of fs.readdirSync(journal).filter(name=>name.endsWith('.jsonl')).sort()){
  const events=parseJournal(fs.readFileSync(path.join(journal,name),'utf8'));
  for(const event of events){
   if(!event.ok||!event.evidence_id||!['web_site_capture','web_pixels_compare'].includes(event.tool))continue;
   const id=event.evidence_id;
   const record=JSON.parse(fs.readFileSync(path.join(base,'evidence',id.slice(3,5),`${id}.json`),'utf8'));
   if(record.operation==='web_site_capture'){
    try{
     for(const shot of record.result.screenshots||[]){
      const file=path.join(record.result.output_directory,shot.file);
      const hash=createHash('sha256').update(fs.readFileSync(file)).digest('hex');
      if(hash!==shot.sha256)throw Error('Screenshot bytes no longer match their recorded evidence.');
      if(matchesCapture(record,new URL(record.result.url).pathname,false)){
       const html=path.join(appRoot,'dist',new URL(record.result.url).pathname,'index.html');
       if(fs.statSync(file).mtimeMs<fs.statSync(html).mtimeMs)throw Error('Rebuilt screenshot predates the current build; capture this page again.');
      }
     }
    }catch(error){record.artifactError=`Unavailable or stale screenshot evidence: ${error.message}`;}
   }
   records.push(record);
  }
 }
 return records;
}

function main(){
 const pages=JSON.parse(fs.readFileSync(path.join(appRoot,'dist/search-index.json'),'utf8')).filter(page=>page.url!=='/');
 if(!pages.length)throw Error('Build the site before checking its subpages.');
 const copy=JSON.parse(fs.readFileSync(path.join(appRoot,'page-content.json'),'utf8'));
 const evidence=readEvidence();
 // Keep build order and examine every page even when an earlier page is blocked.
 const results=[];
 for(const [index,page] of pages.entries()){
  const result={order:index+1,title:page.title,hasOriginalCopy:!!copy[page.url],...reviewPage(page.url,evidence)};
  results.push(result);
  console.log(`${index+1}/${pages.length} ${result.status.toUpperCase()} ${page.url}: ${result.reason}`);
 }
 const counts=Object.fromEntries(['passed','failed','blocked'].map(status=>[status,results.filter(row=>row.status===status).length]));
 const report={generatedAt:new Date().toISOString(),minimumSimilarity,requiredWidths,scoreRule:'Every full-page width must reach 90%; score averages measured layout/detail, penalizes unmatched height, and uses the lowest width without rounding.',passed:counts.passed===results.length,counts,pages:results};
 const qa=path.join(appRoot,'qa');
 fs.mkdirSync(qa,{recursive:true});
 fs.writeFileSync(path.join(qa,'subpage-likeness.json'),JSON.stringify(report,null,2)+'\n');
 const lines=results.map(row=>`${row.order}. ${row.route} — ${row.status.toUpperCase()}${row.similarity===null?'':` (${row.similarity.toFixed(2)}%)`}: ${row.reason}`);
 fs.writeFileSync(path.join(qa,'subpage-likeness.txt'),[`Subpage likeness review: minimum ${minimumSimilarity}% on every page at ${requiredWidths.join('/')}px.`,`Checked ${results.length} subpages individually: ${counts.passed} passed, ${counts.failed} below target, ${counts.blocked} blocked.`,`Missing evidence is unverified and cannot pass. The homepage score applies only to the homepage.`,...lines].join('\n')+'\n');
 console.log(`Subpage likeness: ${counts.passed}/${results.length} passed; ${counts.failed} failed; ${counts.blocked} blocked. Reports: qa/subpage-likeness.json and qa/subpage-likeness.txt`);
 if(!report.passed)process.exitCode=1;
}

if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main();
