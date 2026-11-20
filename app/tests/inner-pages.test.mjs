import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const page = route => fs.readFileSync(new URL(`../dist/${route}/index.html`, import.meta.url), 'utf8').split('<div id="page-content">')[1].split('<footer')[0];

// Expectations come from the saved public-page evidence, independently of the renderer.
test('About follows the live section order and includes the five value descriptions', () => {
 const html = page('over-ons');
 const headings = [...html.matchAll(/<h2[^>]*>([\s\S]*?)<\/h2>/g)].map(m => m[1].replace(/<[^>]+>/g, '').replaceAll('&#39;', "'").replace(/\s+/g,' ').trim());
 const partners = headings.indexOf('Onze samenwerkingen in slimme automatisering');
 const values = headings.indexOf('What makes BHR your system integreator?');
 const review = headings.findIndex(h => h.startsWith("''Het bedrijf"));
 assert.ok(partners < values && values < review, 'partners and values must precede the testimonial');
 assert.ok(html.includes('Wij zorgen dat installaties werken en blijven werken.'));
 assert.ok(html.includes('Wij herkennen ons in jouw ambitie.'));
});

test('Careers puts the location after the facts and restores its missing values block', () => {
 const html = page('over-ons/werken-bij');
 assert.ok(html.indexOf('Dit is BHR') < html.indexOf('Maak vandaag nog kennis met BHR'));
 assert.ok(html.includes('Wat ons drijft'));
 assert.ok(html.includes('Altijd bouwen aan slimmere oplossingen'));
 assert.ok(html.includes('Vooruit door leren en verbeteren'));
 assert.equal([...html.matchAll(/<h2[^>]*>Maak vandaag nog kennis met BHR<\/h2>/g)].length, 1);
});

test('Project articles preserve their lead list without injecting sales buttons', () => {
 const html = page('projecten/bierskid-besturing-zonder-plc');
 assert.ok(html.includes('<li>hogere bedrijfszekerheid,</li>'));
 assert.ok(html.includes('<li>eenvoud in onderhoud,</li>'));
 assert.ok(!html.includes('Praat met een expert'));
});

test('Service and careers primary actions point to the actions on the live pages', () => {
 const service = page('service-en-onderhoud');
 assert.match(service, /href="\/afspraak-maken"[^>]*>Plan uw serviceafspraak<\/a>/);
 const careers = page('over-ons/werken-bij');
 assert.match(careers, /href="\/vacature"[^>]*>Bekijk onze vacatures<\/a>/);
 assert.ok(!service.includes('Offerte aanvragen'));
});

test('Paneelbouw recommendations render as project cards and software has no invented quote section', () => {
 const paneelbouw = page('expertises/paneelbouw');
 const cards = [...paneelbouw.matchAll(/<article class="project-card"[\s\S]*?<\/article>/g)];
 assert.equal(cards.length, 3);
 assert.ok(cards.some(([card]) => card.includes('/projecten/cummins')));
 const software = page('expertises/software-engineering');
 assert.ok(!software.includes('Bespreek uw vraag met onze specialisten.'));
 assert.match(software, /Wil je een offerte aanvragen voor Paneelbouw\?/);
});

test('Process and production places its expert callout before the final partner article', () => {
 const html = page('voor-machinebouwers/proces-productie').replaceAll('\u00a0',' ');
 const cta=html.indexOf('class="parity-cta"');assert.ok(cta>0&&cta<html.indexOf('BHR Industrial Solutions: partner voor uw proces en productiviteit'));
 const hero = html.split('</section>')[0];
 assert.match(hero, /href="\/expertises#offerte"[^>]*>Offerte aanvraag<\/a>/);
 assert.match(hero, /href="\/afspraak-maken"[^>]*>Praat met een expert<\/a>/);
 assert.equal((html.match(/Wij helpen u graag verder/g) || []).length, 1);
 assert.equal((html.match(/Voor bedrijven in de industrie ontwerpen/g) || []).length, 1, 'the lead belongs before the first article only');
});

test('Document routes preserve panoramic imagery while parity routes overlay their heading', () => {
 for (const route of ['expertises','voor-machinebouwers','voor-machinebouwers/proces-productie','service-en-onderhoud']) {
  const html = page(route);
  assert.match(html, /class="parity-hero/);assert.match(html, /parity-hero-image/);
 }
});
