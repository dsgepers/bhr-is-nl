"""Device-correct BHR visual audit. Source snapshots are evidence, never product code."""
import argparse,concurrent.futures,hashlib,importlib.util,json,sys,time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'checks/mobile-parity-2026-11-20'
BASE.mkdir(parents=True,exist_ok=True)
if not (BASE/'routes.json').exists():
 pages=json.loads((ROOT/'app/dist/search-index.json').read_text());(BASE/'routes.json').write_text(json.dumps([{'route':p['url'],'key':p['url'].strip('/').replace('/','--')or'home','title':p['title']}for p in pages],indent=2)+'\n')
P=argparse.ArgumentParser();P.add_argument('--phase',default='baseline');P.add_argument('--mode',default='mobile',choices=['mobile','phone-small','phone-large','tablet','desktop','laptop']);P.add_argument('--role',default='both',choices=['both','reference','candidate']);P.add_argument('--route',action='append');P.add_argument('--workers',type=int,default=3);P.add_argument('--skip-complete',action='store_true');args=P.parse_args()
PROFILES={'mobile':(390,844,'mobile'),'phone-small':(360,800,'mobile'),'phone-large':(430,932,'mobile'),'tablet':(768,1024,'tablet'),'desktop':(1920,1080,'desktop'),'laptop':(1440,900,'desktop')}
PHONE_UA='Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36'
TABLET_UA='Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
spec=importlib.util.spec_from_file_location('bhr_tiled',ROOT/'checks/visual-planning-2026-11-20/capture-normalized.py');tiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(tiler);skill=tiler.module
INVENTORY=r'''() => {
 const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'};
 const detail=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {tag:e.tagName,cls:typeof e.className==='string'?e.className:'',id:e.id,text:e.innerText?.trim().slice(0,600),box:{x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height},font:s.fontFamily,size:s.fontSize,lineHeight:s.lineHeight,weight:s.fontWeight,color:s.color,background:s.backgroundColor,padding:s.padding,margin:s.margin,display:s.display,gap:s.gap,direction:s.flexDirection,grid:s.gridTemplateColumns,position:s.position,z:s.zIndex,clip:s.clipPath,fit:s.objectFit}};
 const headings=[...document.querySelectorAll('h1,h2,h3,h4')].filter(visible);
 const containers=new Set(headings.map(e=>e.closest('section,article,.Block,.Element,.Textblock')||e.parentElement));
 return {viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale,viewportHeight:innerHeight,screenWidth:screen.width,touch:navigator.maxTouchPoints,ua:navigator.userAgent,height:document.documentElement.scrollHeight,scrollWidth:document.documentElement.scrollWidth},styles:[...document.styleSheets].map(e=>e.href),headings:headings.map(detail),blocks:[...containers].map(detail),images:[...document.images].filter(visible).map(e=>({...detail(e),src:e.currentSrc||e.src,alt:e.alt,naturalWidth:e.naturalWidth})),forms:[...document.forms].map(f=>({...detail(f),fields:[...f.elements].filter(visible).map(detail)})),header:document.querySelector('.mobile-header,header')?detail(document.querySelector('.mobile-header')||document.querySelector('header')):null,footer:document.querySelector('footer')?detail(document.querySelector('footer')):null,articles:[...document.querySelectorAll('article')].filter(visible).map(detail)};
}'''

def revision():
 h=hashlib.sha256()
 for f in sorted((ROOT/'app/dist').rglob('*')):
  if f.is_file()and f.suffix in ['.html','.css','.mjs']:
   h.update(str(f.relative_to(ROOT/'app/dist')).encode());h.update(f.read_bytes())
 return h.hexdigest()

def run(route):
 out=BASE/args.phase/route['key']/args.mode;out.mkdir(parents=True,exist_ok=True)
 roles=['reference','candidate']if args.role=='both'else[args.role]
 if args.skip_complete and all((out/(r+'.json')).exists()for r in roles):return {'route':route['route'],'skipped':True}
 w,h,device=PROFILES[args.mode];result={'route':route['route'],'mode':args.mode,'revisionBefore':revision(),'views':{}}
 try:
  with sync_playwright()as p:
   b=p.chromium.launch()
   for role in roles:
    settings={'viewport':{'width':w,'height':h},'screen':{'width':w,'height':h},'device_scale_factor':1,'locale':'nl-NL','timezone_id':'Europe/Amsterdam','color_scheme':'light','reduced_motion':'reduce','is_mobile':device=='mobile','has_touch':device!='desktop'}
    if device!='desktop':settings['user_agent']=PHONE_UA if device=='mobile'else TABLET_UA
    c=b.new_context(**settings)
    c.route('**/*',lambda r:r.abort()if r.request.method not in ['GET','HEAD','OPTIONS']else r.continue_())
    if role=='reference':c.add_cookies([{'name':'device','value':device,'domain':'www.bhr-is.nl','path':'/'},{'name':'cookieconsent_status','value':'deny','domain':'www.bhr-is.nl','path':'/'}])
    else:c.add_init_script("localStorage.setItem('bhr-cookie-consent','denied')")
    page=c.new_page();url=('https://www.bhr-is.nl'if role=='reference'else'http://localhost:4173')+route['route']
    response=page.goto(url,wait_until='domcontentloaded',timeout=45000);page.wait_for_timeout(1000);page.evaluate('document.fonts.ready')
    if response.status>=400:
     result['views'][role]={'status':response.status,'url':page.url};(out/(role+'.json')).write_text(json.dumps(result['views'][role],indent=2));c.close();continue
    page.evaluate("document.querySelector('.cc-deny')?.click();document.documentElement.style.scrollBehavior='auto'")
    # Load lazy media and finite entrance effects before measuring document geometry.
    total=page.evaluate('document.documentElement.scrollHeight')
    for y in range(0,total,max(h-100,500)):
     page.evaluate('(y)=>scrollTo(0,y)',y);page.wait_for_timeout(45)
    page.evaluate('scrollTo(0,0)');page.wait_for_timeout(200)
    page.screenshot(path=str(out/(role+'.png')),full_page=True,scale='css')
    inventory=page.evaluate(INVENTORY);inventory['status']=response.status;inventory['url']=page.url
    assert inventory['viewport']['dpr']==1 and inventory['viewport']['scale']==1,inventory['viewport']
    if inventory['viewport']['width']!=w:
     inventory['viewportWarning']='Layout overflow changes innerWidth at the requested device viewport'
     if args.phase!='baseline':raise RuntimeError(str(inventory['viewport']))
    if role=='reference':assert any('corporate-'+device in(s or'')for s in inventory['styles']),inventory['styles']
    (out/(role+'.json')).write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
    if role=='reference':(out/'reference.html').write_text(page.content())
    result['views'][role]={'status':response.status,'url':page.url,'viewport':inventory['viewport']};c.close()
   b.close()
  result['revisionAfter']=revision();result['revisionChanged']=result['revisionBefore']!=result['revisionAfter'];(out/'capture.json').write_text(json.dumps(result,indent=2)+'\n');print(args.phase,args.mode,route['route'],'OK',flush=True)
 except Exception as e:
  result['error']=str(e);(out/'error.json').write_text(json.dumps(result,indent=2));print(args.phase,args.mode,route['route'],'ERROR',str(e)[:180],flush=True)
 return result

routes=json.loads((BASE/'routes.json').read_text())
if args.route:routes=[r for r in routes if r['route']in args.route or r['key']in args.route]
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)as pool:results=list(pool.map(run,routes))
(BASE/(args.phase+'-'+args.mode+'-'+args.role+'-summary.json')).write_text(json.dumps(results,indent=2)+'\n')
raise SystemExit(any('error'in r for r in results))
