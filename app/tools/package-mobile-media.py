"""Package original device derivatives and authored route/image mapping."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,concurrent.futures,hashlib,json,re,urllib.request
P=argparse.ArgumentParser();P.add_argument('--device',choices=['mobile','tablet'],default='mobile');args=P.parse_args()
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20/baseline'
manifest=json.loads((ROOT/'app/assets-manifest.json').read_text());routes=json.loads((BASE.parent/'routes.json').read_text());needed=set();source={}
def photo(url):return re.sub(r'^\d+_','',url.split('/')[-1])
for route in routes:
 path=BASE/route['key']/args.device/'reference.html'
 if not path.exists():continue
 soup=BeautifulSoup(path.read_text(),'html.parser');images=[]
 for image in soup.select('img[src]'):
  url=image['src']
  if url.startswith('https://www.bhr-is.nl/media/images/'):
   images.append({'url':url,'alt':image.get('alt','')})
   if url not in manifest:needed.add(url)
 source[route['route']]=images
def download(url):
 name=args.device+'-'+hashlib.sha256(url.encode()).hexdigest()[:10]+'-'+url.split('/')[-1];file=ROOT/'app/public/assets/images'/name
 if not file.exists():
  request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(request,timeout=30)as response:data=response.read()
  assert len(data)>100,(url,len(data));file.write_bytes(data)
 data=file.read_bytes();return url,{'path':'/assets/images/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'secondaryOnly':True,'role':'original '+args.device+' derivative'}
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 for url,asset in pool.map(download,sorted(needed)):manifest[url]=asset
reverse={v['path']:k for k,v in manifest.items()};mapping={}
for route in routes:
 if route['route']not in source:continue
 html=ROOT/'app/dist'/route['route'].strip('/')/'index.html';soup=BeautifulSoup(html.read_text(),'html.parser');images=source[route['route']];rows=[]
 for image in soup.select('img[src]'):
  current=image['src'];origin=reverse.get(current)
  if not origin:continue
  exact=[im for im in images if image.get('alt') and im['alt']==image['alt']]
  candidates=[im for im in exact if photo(im['url'])==photo(origin)] or (exact if len(exact)==1 else [im for im in images if photo(im['url'])==photo(origin)])
  if not candidates:continue
  chosen=candidates[0];target=manifest[chosen['url']]['path']
  if target!=current:
   row={'from':current,'to':target,'alt':image.get('alt',''),'source':chosen['url']}
   if row not in rows:rows.append(row)
 if rows:mapping[route['route']]=rows
(ROOT/'app/assets-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(ROOT/('app/public/'+('mobile'if args.device=='mobile'else'tablet')+'-data.json')).write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n')
print('Packaged',len(needed),'original '+args.device+' derivatives;',sum(len(r)for r in mapping.values()),'image replacements across',len(mapping),'routes')
