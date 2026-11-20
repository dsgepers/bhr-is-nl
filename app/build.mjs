import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {home,services,projects,branches,standard,faq,image,origin,media,pageContent,observedPage,pageImage} from './data.mjs';
import {esc,link,img,eyebrow,inline,layout,homepage,titleSection,articleSections,serviceCards,projectCards,industry,about,vacancy,cta,branchCards,partners,faqSection,contactForm,quoteForm,processSection} from './components.mjs';
import {expertiseIndex,servicePage,standardPage,aboutPage,careersPage,contactPage,appointmentPage,vacancyPage,projectListing,pageCta,partnersPage} from './inner-pages.mjs';
import {secondaryContent} from './secondary-data.mjs';
import {secondaryPage,secondaryOptions} from './secondary-pages.mjs';
const root=path.dirname(fileURLToPath(import.meta.url)),dist=path.join(root,'dist');
fs.mkdirSync(dist,{recursive:true});fs.cpSync(path.join(root,'public'),dist,{recursive:true});
const pages=[],emitted=new Set();
const assetVersions=new Map();
function versionSliderAssets(html,allowed=null){
 return html.replace(/\b(href|src)="(\/[^"?]+\.(?:css|mjs))"/g,(original,attribute,url)=>{
  if(allowed&&!allowed.has(url))return original;
  if(!assetVersions.has(url))assetVersions.set(url,createHash('sha256').update(fs.readFileSync(path.join(root,'public',url))).digest('hex').slice(0,12));
  return `${attribute}="${url}?v=${assetVersions.get(url)}"`;
 });
}
function add(url,title,body,cls='secondary',simple=false){if(emitted.has(url))throw new Error(`Duplicate route: ${url}`);emitted.add(url);let meta={};if(Object.hasOwn(secondaryContent,url)){const o=secondaryOptions(url);title=o.title;body=secondaryPage(url);cls=o.classes;simple=o.simple;meta={documentTitle:o.documentTitle,canonical:o.canonical};}pages.push({url,title,text:body.replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').slice(0,12000)});const folder=path.join(dist,url);fs.mkdirSync(folder,{recursive:true});let html=layout(title,body,cls,simple,meta);if(body.includes('data-step-image='))html=versionSliderAssets(html);html=versionSliderAssets(html,new Set(['/mobile-parity.css','/mobile.mjs']));fs.writeFileSync(path.join(folder,'index.html'),html);}
add('/','BHR Industrial Automations & Paneelbouw',homepage(),'home');
add('/expertises','Onze expertises',expertiseIndex(),'secondary reference-page expertise-index parity-page parity-expertises');
for(const p of services)add(p.url,p.title,servicePage(p));
for(const p of standard){const key=p.url.includes('proces-productie')?'proces-productie':p.url==='/service-en-onderhoud'?'service-en-onderhoud':null;add(p.url,p.title,standardPage(p,key?{parity:key}:{}),'secondary reference-page'+(key?' parity-page parity-'+key:''));}
const machine=standard[0];add('/voor-machinebouwers/voor-machinebouwers',machine.title,standardPage(machine,{parity:'machinebouwers'}),'secondary reference-page parity-page parity-machinebouwers');
add('/over-ons','Over BHR',aboutPage());
add('/over-ons/partners','Partners',partnersPage(),'secondary reference-page parity-page parity-partners');
add('/over-ons/werken-bij','Werken bij',careersPage(),'secondary reference-page parity-page parity-werken-bij');
add('/vacature','Vacatures',vacancyPage());

add('/projecten','Projecten',projectListing());
for(const p of projects)add(p.url,p.title,titleSection(p,false)+articleSections(p));
for(const b of branches){const p=observedPage({...b,heading:`Betrouwbare paneelbouw en automatisering voor ${b.title.toLowerCase()}`,intro:'BHR Industrial Solutions brengt paneelbouw, besturing en software samen. Onze oplossingen laten machines en processen betrouwbaar presteren, met aandacht voor veiligheid, onderhoud en uitbreiding.',img:image('Paneelbouw'),sections:[`Geïntegreerde besturing en automatisering voor ${b.title.toLowerCase()}`,`Paneelbouw en besturingskasten voor ${b.title.toLowerCase()}`,`De betrouwbare partner voor ${b.title.toLowerCase()}`]});add(p.url,b.title,titleSection(p)+articleSections(p)+processSection(p)+serviceCards(true)+partners()+(p.faq?.length?faqSection(false,p):'')+cta());}

add('/contact','Contact',contactPage());
add('/afspraak-maken','Afspraak maken',appointmentPage(),'secondary appointment-page',true);
add('/veelgestelde-vragen','Veelgestelde vragen',titleSection({title:'Veelgestelde vragen'},false)+faqSection(true));
add('/zoeken','Zoeken',titleSection({title:'Zoeken'},false)+`<section class="text-section"><div class="container"><form class="site-search" action="/zoeken"><label>Waar bent u naar op zoek?<input type="search" name="q" placeholder="Zoekterm" required></label><button class="button">Zoeken</button></form><div class="search-results" aria-live="polite"></div></div></section>`);
add('/cookie-instellingen','Cookie-instellingen',titleSection({title:'Cookie-instellingen'},false)+`<section class="text-section"><div class="container"><h2>Uw cookievoorkeuren</h2><p>U kunt uw toestemming op elk moment aanpassen.</p><form class="cookie-options"><label><input type="checkbox" checked disabled> Noodzakelijke cookies</label><label><input name="analytics" type="checkbox"> Ervaring en meting</label><label><input name="marketing" type="checkbox"> Marketing</label><button class="button">Voorkeuren opslaan</button></form></div></section>`);
// The original privacy/footer links are placeholders; preserve them while supplying dedicated form destinations.
for(const [url,title] of [['/privacyverklaring','Privacyverklaring'],['/algemene-voorwaarden','Algemene voorwaarden']])add(url,title,titleSection({title},false)+`<section class="text-section"><div class="container"><p>Voor informatie over ${title.toLowerCase()} kunt u contact opnemen met BHR Industrial Solutions.</p>${link('Stuur een e-mail','mailto:info@bhr-is.nl')}</div></section>`);
add('/bedankt','Bedankt',titleSection({title:'Bedankt voor uw bericht',intro:'Uw bericht is verzonden. Wij nemen zo spoedig mogelijk contact met u op.'},false));
for(const [route,p] of Object.entries(secondaryContent))if(!emitted.has(route))add(route,p.title,'');
fs.writeFileSync(path.join(dist,'search-index.json'),JSON.stringify(pages));
fs.writeFileSync(path.join(dist,'404.html'),layout('Pagina niet gevonden',titleSection({title:'Pagina niet gevonden',intro:'Deze pagina is niet beschikbaar.'},false)+`<section class="text-section"><div class="container">${link('Naar de homepage','/')}</div></section>`,'secondary'));
fs.writeFileSync(path.join(dist,'sitemap.xml'),`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${pages.map(p=>`<url><loc>${origin}${p.url}</loc></url>`).join('')}</urlset>`);
fs.writeFileSync(path.join(dist,'robots.txt'),'User-agent: *\nAllow: /\n');
console.log(`Built ${pages.length} static pages into dist.`);
