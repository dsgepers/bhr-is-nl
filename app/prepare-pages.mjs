import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {siteUrl,siteMarkup} from './public/paths.mjs';

// Run on a fresh build; only published files are changed.
export function preparePages(dist,basePath=''){
 const base=basePath.replace(/\/$/,'');
 if(base&&!/^\/(?:[A-Za-z0-9_.-]+\/)*[A-Za-z0-9_.-]+$/.test(base))throw Error('Invalid Pages base path');
 const rewrite=value=>typeof value==='string'?siteUrl(value,base):Array.isArray(value)?value.map(rewrite):value&&typeof value==='object'?Object.fromEntries(Object.entries(value).map(([key,item])=>[key,rewrite(item)])):value;
 for(const file of fs.readdirSync(dist,{recursive:true})){
  const target=path.join(dist,file);
  if(!/\.(html|css|json)$/.test(file))continue;
  let content=fs.readFileSync(target,'utf8');
  if(file.endsWith('.html'))content=siteMarkup(content,base);
  if(/\.(html|css)$/.test(file))content=content.replace(/url\((['"]?)(\/[^)'"\s]*)\1\)/g,(_,quote,url)=>`url(${quote}${siteUrl(url,base)}${quote})`);
  else content=JSON.stringify(rewrite(JSON.parse(content)));
  fs.writeFileSync(target,content);
 }
 fs.writeFileSync(path.join(dist,'.nojekyll'),'');
 console.log(`Prepared GitHub Pages output at ${base||'/'}.`);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 preparePages(fileURLToPath(new URL('./dist/',import.meta.url)),process.env.PAGES_BASE_PATH||'');
}
