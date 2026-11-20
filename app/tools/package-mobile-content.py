"""Package measured mobile content metadata from the device-correct audit.

Only original copy, heading break positions and original media references enter
product JSON; source templates, stylesheets and scripts remain evidence only.
"""
import json,re
from pathlib import Path
from bs4 import BeautifulSoup,NavigableString
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20/baseline'
visibilityPath=BASE.parent/'heading-breaks.json'
if not visibilityPath.exists():raise SystemExit('Run audit-mobile-heading-breaks.py before packaging phone headings')
visibility=json.loads(visibilityPath.read_text())
manifest=json.loads((ROOT/'app/assets-manifest.json').read_text());routes=json.loads((BASE.parent/'routes.json').read_text());headings={};legacy={}
for row in routes:
 path=BASE/row['key']/'mobile/reference.html'
 if not path.exists():continue
 soup=BeautifulSoup(path.read_text(),'html.parser');records=[]
 for heading in soup.select('.maincontainer h1,.maincontainer h2,.maincontainer h3,.maincontainer h4,.maincontainer div.h1'):
  values=[]
  def walk(node):
   if isinstance(node,NavigableString):values.append(str(node))
   elif node.name=='br':values.append('\nBR\n')
   else:
    for child in node.children:walk(child)
  walk(heading);parts=[re.sub(r'\s+',' ',v).strip()for v in ''.join(values).split('\nBR\n')];parts=[p for p in parts if p];text=' '.join(parts);record={'text':text,'parts':parts}
  if text and record not in records:records.append(record)
 for observed in visibility.get(row['route'],[]):
  for i,record in enumerate(records):
   if record['text']==observed['text']:records[i]={'text':observed['text'],'parts':observed['parts']}
 headings[row['route']]=records
 if row['route']not in ['/expertises/paneelbouw','/expertises/retrofit']:continue
 record={'branches':[]};seen=set()
 quote=next((r['text']for r in records if r['text'].startswith('Bereken direct de investering')),None)
 if quote:
  record['quoteTitle']=quote
  title=next((h for h in soup.select('h3')if h.get_text(' ',strip=True)==quote),None)
  intro=title.parent.select_one('.Intro')if title else None
  if intro:record['quoteIntro']=intro.get_text(' ',strip=True)
 lead=soup.select_one('.maincolumn>.inner>.Heading')
 if lead:record['lead']={'title':lead.select_one('.left .h1').get_text(' ',strip=True),'text':lead.select_one('.Content').get_text(' ',strip=True)}
 for article in soup.select('article.Branche'):
  image=article.find('img');anchor=article.find('a',href=True);title=article.find(['h2','h3'])
  if image and anchor and title and anchor['href']not in seen:
   record['branches'].append({'title':title.get_text(' ',strip=True),'href':anchor['href'],'image':manifest[image['src']]['path']});seen.add(anchor['href'])
 region=soup.select_one('.LocationOverview')
 if region:record['region']={'eyebrow':region.get('data-subtitle'),'title':region.get('data-title'),'intro':region.get('data-introduction'),'href':region.get('data-url'),'cta':region.select_one('.Heading nav .title').get_text(' ',strip=True),'image':'/assets/images/map.png','locations':[e.get_text(' ',strip=True)for e in region.select('.Heading ul li .title')]}
 legacy[row['route']]=record
for name,value in [('mobile-content.json',legacy),('mobile-headings.json',headings)]:
 (ROOT/'app/public'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
print('Packaged',sum(map(len,headings.values())),'heading records and',len(legacy),'legacy phone compositions')
