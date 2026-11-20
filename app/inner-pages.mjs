import {parityPage} from './parity-pages.mjs';
import {projects,pageContent,observedPage,pageImage,image} from './data.mjs';
import {esc,link,img,eyebrow,inline,titleSection,articleSections,serviceCards,projectCards,industry,vacancy,cta,partners,faqSection,contactForm,quoteForm} from './components.mjs';

const action=(text,url,outline=false)=>({text,url,outline});
const talk=action('Praat met een expert','/afspraak-maken');
const contact=action('Neem contact op','/contact');

// Document images use the panoramic 1920 × 700 format. Keep this separate
// from the 940 × 740 image/text blocks used farther down these pages.
function documentHeader(page) {
 const p=observedPage(page);
 return `<section class="document-hero"><div class="document-banner">${img(p.img,p.title)}</div><div class="document-intro"><div class="container document-intro-layout"><h1>${esc(p.heading||p.title)}</h1><div class="document-intro-copy">${p.intro?`<p>${esc(p.intro)}</p>`:''}${p.actions?.length?`<nav>${p.actions.map(a=>link(esc(a.text),a.url,a.outline?'button outline white':'button')).join('')}</nav>`:''}</div></div></div></section>`;
}

export function pageCta(title,actions=[talk,action('Onze expertises','/expertises',true)],label='Ontdek jouw mogelijkheden') {
 return `<section class="cta"><div class="container">${eyebrow(label)}<h2>${esc(title)}</h2><nav>${actions.map(a=>link(esc(a.text),a.url,a.outline?'button outline':'button')).join('')}</nav></div></section>`;
}

export function servicePage(page) {
 const p=observedPage(page);
 const quoteTarget=['paneelbouw','retrofit'].includes(p.slug)?'#offerte':'/contact';
 const hero=titleSection({...p,actions:[action(p.slug==='software-engineering'?'Vraag een offerte aan':'Offerte aanvragen',quoteTarget),action('Neem contact op','/contact',true)]});
 const articles=articleSections({...p,articleData:p.articleData?.map((s,i)=>s.title==='Onze paneelbouw'?{...s,projects:projects.filter(p=>['bouwen-afdelingsinstallatie','cummins','retrofit-oplossingen-in-bestaande-machineframe'].includes(p.slug))}:s)});
 const titles={
  'software-engineering':'Wil je een offerte aanvragen voor Paneelbouw?',
  'hardware-engineering':'Maak een afspraak met BHR voor Hardware Engineering',
  'paneelbouw':'Vraag vandaag nog je offerte aan voor paneelbouw op maat',
  'elektrocomponenten':'Wil je een offerte aanvragen?',
  'industriele-automatisering':'Maak een afspraak met BHR voor Industriële automatisering'
 };
 const end=pageCta(titles[p.slug]||'Wat kunnen wij voor jouw proces betekenen?',titles[p.slug]?[action('Praat met een expert','/contact'),action('Onze expertises','/expertises',true)]:undefined);
 const questions=p.faq?.length?faqSection(false,p):'';
 if(p.slug==='paneelbouw')return hero+articles+end+questions+quoteForm('compact');
 if(p.slug==='retrofit')return hero+articles+quoteForm('compact')+end;
 return hero+articles+questions+end;
}

export function standardPage(page,options={}) {
 if(options.parity)return parityPage(options.parity);
 const p=observedPage(page),service=p.url==='/service-en-onderhoud',process=p.url.includes('proces-productie');
 const hero=documentHeader({...p,actions:service?[action('Plan uw serviceafspraak','/afspraak-maken')]:process?[action('Offerte aanvraag','/expertises#offerte'),action('Praat met een expert','/afspraak-maken',true)]:[]});
 const articles=process?
  articleSections({...p,articleData:p.articleData.slice(0,2)})+cta()+articleSections({...p,lead:[],articleOffset:2,articleData:p.articleData.slice(2)}):
  articleSections(p)+(service?faqSection(false,p):'')+cta();
 const form=service?quickContact():contactForm(process?'Wij helpen u graag verder':'Kunnen we u helpen met uw proces?').replace('Contactformulier','Neem contact met ons op');
 return hero+articles+form;
}

export function expertiseIndex(){return parityPage('expertises');}
export function partnersPage(){return parityPage('partners');}

const values=[
 ['G','Garantie','Wij zorgen dat installaties werken en blijven werken. Onze oplossingen zijn first-time-right, veilig en duurzaam.'],
 ['R','Resultaat','Problemen bestaan niet, uitdagingen wel. We denken in mogelijkheden en verbeteren continu onze eigen processen door slimmer te werken'],
 ['E','Efficientie','Met één aanspreekpunt en korte lijnen maken we complexe projecten overzichtelijk. We werken samen met jou als één team samen.'],
 ['A','Ambitie','Wij herkennen ons in jouw ambitie. We laten je machines en productielijnen beter presteren, met snelle doorlooptijden en slimme retrofit-oplossingen.'],
 ['T','Trots','We werken netjes, georganiseerd en met oog voor detail. Van schone kasten tot strakke installaties. Wij zijn trots op ons werk en laten dat zien.']
];

export function team(title='Samen maken we het verschil',label='Ons gedreven team') {
 return `<section class="text-section team-section"><div class="container">${eyebrow(label)}<h2>${title}</h2><article class="team-card">${img('/media/images/employee/1/1/1147_dsc02542.webp','Henk Rutten','team-portrait')}<h3>Henk Rutten</h3><p>Directeur</p></article></div></section>`;
}

export function aboutPage() {
 const sections=pageContent['/over-ons'].sections;
 const mission=pageImage('/over-ons',sections[0].title,image('Slimme oplossingen <br><span>en</span> first- time-right'));
 return `<section class="about-hero" style="--about-image:url('${image('Homepage')}')" aria-label="BHR in beeld"><button class="scroll-down" data-scroll="missie">Scroll down<span>↓</span></button></section>`+
  `<section class="article-section" id="missie"><div class="container split">${img(mission,sections[0].title)}<div class="article-copy">${eyebrow('Onze missie en visie')}<h1>${esc(sections[0].title)}</h1><p>${esc(sections[0].content[0])}</p>${link('Neem contact op','/contact')}</div></div></section>`+
  industry()+partners()+`<section class="text-section values-section pale"><div class="container"><h2>What makes BHR your system integreator?</h2><div class="values-grid">${values.map(([letter,title,text])=>`<article><div class="value-letter">${letter}</div><h3>${title}</h3><p>${esc(text)}</p></article>`).join('')}</div></div></section>`+
  articleSections({title:'Review',articleData:[{...sections[2],eyebrow:'Review',img:pageImage('/over-ons',sections[2].title,image('Paneelbouw'))}]})+
  vacancy()+team()+pageCta('Bouw mee aan jouw toekomst in de techniek',[contact,action('Solliciteer nu','/over-ons/werken-bij#contactformulier',true)],'Werken bij BHR');
}

export function careersPage(){return parityPage('werken-bij');}

export function contactPage() {
 const p=observedPage({url:'/contact',title:'Contact'});
 return `<section class="page-title contact-title"><div class="container"><div class="title-copy"><h1>${esc(p.heading)}</h1><p>${esc(p.intro)}</p><div class="contact-details"><div><strong>Adres</strong>Zandeweg 5F<br>5107NM Dongen<br>Nederland</div><div><strong>Telefoonnummer</strong>${link('+31 (0)162 - 23 88 34','tel:+31162238834','')}</div><div><strong>E-mail</strong>${link('Stuur een e-mail','mailto:info@bhr-is.nl','')}</div></div></div>${img(p.img,'Contact')}</div></section>`+
  contactForm()+team('Gedreven en betrokken','Persoonlijke aandacht, professionele expertise');
}

export function appointmentPage() {
 return titleSection({url:'/afspraak-maken',title:'Afspraak maken',introList:['Vertalen we uw wensen naar een helder vertrekpunt','Maakt u kennis met onze experts','Leggen we onze werkwijze en aanpak uit'],actions:[]},false)+contactForm('Vul het afspraakformulier in');
}

export function vacancyPage() {
 return titleSection({url:'/vacature',title:'Vacatures',actions:[]},false)+`<section class="text-section vacancy-list"><div class="container"><p>Momenteel zijn er geen items aanwezig.</p></div></section>`;
}

export function projectListing() {
 const card=p=>`<article class="project-card" data-category="${p.category}"><a href="${p.url}">${img(pageImage(p.url,p.title,p.img),p.title)}</a>${eyebrow(p.category)}<h3>${link(p.title,p.url,'')}</h3><p>${esc(p.intro.length>240?p.intro.slice(0,237)+'…':p.intro)}</p>${inline('Meer over dit project',p.url)}</article>`;
 return titleSection({title:'Projecten',heading:'Projecten waar we trots op zijn',intro:'Ontdek onze gerealiseerde projecten binnen automatisering, paneelbouw en machine-integratie. Stuk voor stuk slimme oplossingen.'},false)+
  `<section class="project-listing"><div class="container"><form class="filters">${['Automatisering','Integratie','Paneelbouw'].map(t=>`<label><input type="checkbox" name="categorie" value="${t}">${t}</label>`).join('')}<button class="button" type="submit">Filter</button></form><p class="results-empty" hidden>Er zijn geen projecten gevonden.</p>${['Automatisering','Paneelbouw'].map(c=>`<section class="project-category" data-project-category="${c}"><h2>${c}</h2><div class="project-grid">${projects.filter(p=>p.category===c).map(card).join('')}</div></section>`).join('')}</div></section>`+
  `<section class="text-section pale"><div class="container"><h2>Van technisch innovatie naar concrete oplossingen</h2><p>Bij BHR Industrial Solutions vertalen we technische innovatie naar concrete oplossingen die werken. Onze kracht ligt in samenwerking. We denken mee, schakelen snel en werken met vakmanschap en trots aan elk project.</p></div></section>`+cta();
}

function quickContact() {
 // Reuse the configured delivery and validation behavior, with the two fields on this live page.
 return contactForm('Snel contact').replace(/<aside>[\s\S]*?<\/aside>/,'').replace(/<label>Naam<input[^>]+><\/label>/,'').replace(/<label>Telefoonnummer<input[^>]+><\/label>/,'').replace(/<label class="full">Bericht<textarea[\s\S]*?<\/label>/,'').replace('class="form-section pale"','class="form-section pale quick-contact"');
}
