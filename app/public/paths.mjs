// This module lives at the published site root, including on project Pages sites.
const basePath=new URL('.',import.meta.url).pathname.replace(/\/$/,'');
export function siteUrl(value,base=basePath){
 if(!value.startsWith('/')||value.startsWith('//')||!base)return value;
 if(value===base||value.startsWith(base+'/'))return value;
 return base+value;
}
export function siteMarkup(html,base=basePath){
 return html.replace(/\b(href|src|action|data-step-image)="(\/[^\"]*)"/g,(_,attr,url)=>`${attr}="${siteUrl(url,base)}"`);
}
export function routePath(pathname,base=basePath){
 const local=base&&(pathname===base||pathname.startsWith(base+'/'))?pathname.slice(base.length):pathname;
 return local.replace(/\/+$/,'')||'/';
}
