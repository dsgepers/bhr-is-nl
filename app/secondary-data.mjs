import fs from 'node:fs';
const json=name=>JSON.parse(fs.readFileSync(new URL(name,import.meta.url),'utf8'));
export function validateSecondaryContent(entries){
 const result={};
 for(const [route,spec] of entries){
  if(Object.hasOwn(result,route))throw new Error(`Duplicate secondary route: ${route}`);
  if(!route.startsWith('/')||spec.route!==route)throw new Error(`Invalid secondary route: ${route}`);
  result[route]=spec;
 }
 return result;
}
export const secondaryContent=validateSecondaryContent(Object.entries(json('./secondary-content.json')));
const assets=json('./assets-manifest.json');
export function secondaryMedia(url){
 const asset=Object.hasOwn(assets,url)?assets[url]:null;
 if(!asset)throw new Error(`Unknown exact secondary media URL: ${url}`);
 return typeof asset==='string'?asset:asset.path;
}
