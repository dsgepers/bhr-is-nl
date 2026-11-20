from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw
import json,urllib.parse as U
ROOT=Path(__file__).resolve().parent;routes=json.loads((ROOT/'routes.json').read_text());manifest=json.loads((ROOT.parent.parent/'app/assets-manifest.json').read_text());catalog=[];assets={};out=ROOT/'inspection';out.mkdir(exist_ok=True)
seo={'/betrouwbare-paneelbouw-etten-leur','/bordenbouw-op-maat','/bordenbouwer','/industriele-bordenbouw','/paneelbouw-automatisering-tilburg','/paneelbouw-automatisering-voor-machineparken-in-tilburg','/paneelbouw-oosterhout','/paneelbouwer-dongen','/paneelbrouwer-breda'}
def family(r):
 if r=='/projecten':return 'project-listing'
 if r.startswith('/projecten/'):return 'project-detail'
 if r in ['/contact','/afspraak-maken']:return 'contact' if r=='/contact' else 'appointment'
 if r.startswith('/expertises/'):return 'expertise'
 if r.startswith('/branches/'):return 'branch'
 if r.startswith('/locaties/'):return 'location-detail'
 if r=='/locaties':return 'location-listing'
 if r in seo:return 'seo'
 if r in ['/over-ons','/de-mensen-achter-de-techniek','/certificering','/referentie']:return 'company'
 if r in ['/offerteaanvraag','/test']:return 'quote'
 if r=='/nieuws':return 'news'
 if r=='/vacature':return 'vacancy-listing'
 if r.startswith('/vacature/'):return 'vacancy-detail'
 if r in ['/voor-machinebouwers','/werken-bij']:return 'alias'
 return 'utility'
for n,r in enumerate(routes,1):
 p=ROOT/'baseline'/r['key'];cap=json.loads((p/'capture.json').read_text());inv=json.loads((p/'wide-reference-inventory.json').read_text());content=json.loads((p/'wide-reference-content.json').read_text());soup=BeautifulSoup((p/'wide-reference.html').read_text(),'html.parser')
 for vp in r['widths']:
  for role in ['reference','candidate']:
   ip=p/f'{vp}-{role}-inventory.json';hp=p/f'{vp}-{role}.html'
   if not ip.exists() or not hp.exists():continue
   ii=json.loads(ip.read_text());ss=BeautifulSoup(hp.read_text(),'html.parser')
   for fi,form in enumerate(ii['forms']):
    sf=ss.find_all('form')[fi]
    for f in form['fields']:
     if not f.get('name'):continue
     node=sf.find(attrs={'name':f['name']})
     if not node:continue
     f['validation']=node.get('data-validation');f['requiredClass']=any('required' in (a.get('class') or []) for a in [node,*list(node.parents)[:4]]);f['semanticRequired']=bool(f.get('required') or f['validation']=='Y' or f['requiredClass']);f['value']=node.get('value') if f.get('type') in ['radio','checkbox'] else None
   ip.write_text(json.dumps(ii,indent=2,ensure_ascii=False)+'\n')
 inv=json.loads((p/'wide-reference-inventory.json').read_text());heading=[h['text'] for h in inv['headings']];image_urls=list(dict.fromkeys(i['src'] for i in inv['images']));metrics=[]
 if (p/'report.json').exists():
  report=json.loads((p/'report.json').read_text());metrics=[{'viewport':v['label'],'mismatch':v['diff']['mismatchPercent'],'ssim':v['diff']['ssimEstimate'],'referenceSize':v['diff']['referenceSize'],'candidateSize':v['diff']['candidateSize'],'heightDelta':v['diff']['candidateSize']['height']-v['diff']['referenceSize']['height']} for v in report['viewports']]
 projects=[]
 for a in soup.select('article.Project.Item'):
  h=a.find(['h1','h2','h3']);slides=a.select('.projectSlider>div[id]');projects.append({'title':h.get_text(' ',strip=True) if h else '', 'images':list(dict.fromkeys(i.get('src') for i in a.select('.projectSlider img'))),'originalSlides':[{ 'id':e.get('id'),'src':e.find('img').get('src') if e.find('img') else None} for e in slides]})
 data={**r,'number':n,'family':family(r['route']),'title':next((h['text'] for h in inv['headings'] if h['tag']=='H1'),content['title']),'headings':heading,'hero':next((i for i in inv['images'] if i['box']['width']>1000 and i['box']['y']<500),None),'images':image_urls,'articles':inv['articles'],'forms':inv['forms'],'media':inv['media'],'canonical':inv['canon'],'metrics':metrics,'status':cap['viewports'][0]['reference']['status'],'finalUrl':cap['viewports'][0]['reference']['final_url'],'projects':projects,'simpleHeader':bool(soup.select('header.Header-simple')),'bodyText':content.get('text','')}
 catalog.append(data)
 for u in image_urls:
  entry=assets.setdefault(u,{'url':u,'pages':[],'exactPackaged':u in manifest,'packagedPath':manifest.get(u,{}).get('path'),'plannedPath':'/assets/images/'+U.urlsplit(u).path.rsplit('/',1)[-1]});entry['pages'].append(r['route'])
 # Primary previews for direct full-page composition inspection; one pair/row.
 thumb=[]
 for role in ['reference','candidate']:
  f=p/f'wide-{role}.png'
  if f.exists():
   im=Image.open(f).convert('RGB');im.thumbnail((230,2600));thumb.append(im)
  else:thumb.append(None)
 height=max(im.height for im in thumb if im is not None)+35;sheet=Image.new('RGB',(460,height),'white');d=ImageDraw.Draw(sheet);d.text((4,4),str(n)+' '+r['route'][:66],fill='black')
 for i,im in enumerate(thumb):
  if im:sheet.paste(im,(i*230,30))
  else:d.text((234,40),'NO LOCAL ROUTE',fill='red')
 sheet.save(out/f'{n:02d}-{r["key"]}.jpg',quality=84)
(ROOT/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n');(ROOT/'asset-audit.json').write_text(json.dumps(list(assets.values()),indent=2,ensure_ascii=False)+'\n')
# Eight pages per sheet, scaled equally to retain source/candidate height contrast.
for batch in range(0,len(catalog),8):
 pairs=[]
 for row in catalog[batch:batch+8]:
  im=Image.open(out/f'{row["number"]:02d}-{row["key"]}.jpg');im.thumbnail((360,1800));pairs.append(im)
 heights=[max(pairs[i].height,pairs[i+1].height if i+1<len(pairs) else 0) for i in range(0,len(pairs),2)];atlas=Image.new('RGB',(720,sum(heights)+30*len(heights)),'#ddd');y=0
 for row,h in enumerate(heights):
  for col in [0,1]:
   idx=row*2+col
   if idx<len(pairs):atlas.paste(pairs[idx],(col*360,y))
  y+=h+30
 atlas.save(out/f'atlas-{batch//8+1:02d}.jpg',quality=86)
print('Catalog:',len(catalog),'pages; photos:',len(assets),'; missing exact media:',sum(not a['exactPackaged'] for a in assets.values()))
