"""Capture the sitemap audit without changing application files.

Use --route KEY --all-widths --out NEW_DIRECTORY for implementation review.
Missing candidates get reference evidence, never a fabricated similarity score.
"""
import argparse, concurrent.futures, datetime, importlib.util, json, subprocess, sys, shutil, hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
spec=importlib.util.spec_from_file_location('bhr_tiled',ROOT/'capture-normalized.py')
tile=importlib.util.module_from_spec(spec);spec.loader.exec_module(tile)
skill=tile.module
VIEWPORTS={'wide':(1920,1080),'desktop':(1440,900),'tablet':(768,1024),'mobile':(390,844)}
P=argparse.ArgumentParser();P.add_argument('--route',action='append');P.add_argument('--all-widths',action='store_true');P.add_argument('--out',type=Path,default=ROOT/'baseline');P.add_argument('--workers',type=int,default=3);P.add_argument('--resume',action='store_true');P.add_argument('--viewport',action='append',choices=list(VIEWPORTS));P.add_argument('--reference-cache',type=Path);args=P.parse_args()
routes=json.loads((ROOT/'routes.json').read_text())
if args.route:routes=[r for r in routes if r['key'] in args.route or r['route'] in args.route]
if not routes:P.error('No scoped route matches --route')
if args.out.resolve()==(ROOT/'baseline').resolve() and not args.resume and any((ROOT/'baseline').glob('*/capture.json')):
 P.error('Planning baseline is preserved. Use --out NEW_DIRECTORY, or --resume to fill unfinished routes without replacing completed captures.')
INVENTORY=r'''() => {
 const clean=e=>(e?.innerText||e?.textContent||'').trim().replace(/\s+/g,' ');
 const box=e=>{let r=e.getBoundingClientRect();return{x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height}};
 const visible=e=>{let s=getComputedStyle(e),r=e.getBoundingClientRect();return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'};
 const detail=e=>{let s=getComputedStyle(e);return{tag:e.tagName,cls:typeof e.className==='string'?e.className:'',text:clean(e),html:e.innerHTML,box:box(e),font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,color:s.color,background:s.backgroundColor}};
 return {
  viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio,scale:visualViewport.scale,scrollHeight:document.documentElement.scrollHeight},
  headings:[...document.querySelectorAll('h1,h2,h3,h4')].filter(visible).map(detail),
  articles:[...document.querySelectorAll('article')].filter(visible).map(e=>({cls:e.className,headings:[...e.querySelectorAll('h1,h2,h3,h4')].map(clean),text:clean(e),box:box(e),images:[...e.querySelectorAll('img')].map(i=>i.currentSrc||i.src),links:[...e.querySelectorAll('a[href]')].map(a=>({text:clean(a),href:a.getAttribute('href')}))})),
  images:[...document.images].filter(visible).map(e=>({src:e.currentSrc||e.src,alt:e.alt,natural:[e.naturalWidth,e.naturalHeight],box:box(e),fit:getComputedStyle(e).objectFit,clip:getComputedStyle(e).clipPath})),
  forms:[...document.forms].map(f=>({id:f.id,action:f.action,method:f.method,headings:[...f.querySelectorAll('h1,h2,h3,h4')].map(clean),box:box(f),fields:[...f.elements].filter(e=>e.type!=='hidden').map(e=>({tag:e.tagName,name:e.name,type:e.type,required:e.required,validation:e.dataset.validation||null,requiredClass:!!e.closest('.required'),value:['radio','checkbox'].includes(e.type)?e.value:null,disabled:e.disabled,placeholder:e.getAttribute('placeholder'),accept:e.accept||null,min:e.min||null,max:e.max||null,checked:!!e.checked,label:clean(e.closest('label'))||clean(document.querySelector(`label[for="${CSS.escape(e.id)}"]`))||clean(e.parentElement).slice(0,260),options:e.options?[...e.options].map(o=>({text:o.text,value:o.value})):null}))})),
  disclosures:[...document.querySelectorAll('details,summary,.Faq.Item')].map(e=>({tag:e.tagName,cls:e.className,text:clean(e),open:e.open||false})),
  media:[...document.querySelectorAll('video,iframe')].map(e=>({tag:e.tagName,src:e.src||e.querySelector('source')?.src||e.dataset.src,title:e.title,box:box(e)})),
  canon:document.querySelector('link[rel=canonical]')?.href||null
 };
}'''

def capture(browser,url,label,role,out):
 width,height=VIEWPORTS[label]
 context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,color_scheme='light',locale='nl-NL',timezone_id='Europe/Amsterdam',reduced_motion='reduce')
 context.route('**/*',lambda r:r.abort() if r.request.method not in ['GET','HEAD','OPTIONS'] else r.continue_())
 page=context.new_page()
 try:
  response=page.goto(url,wait_until='domcontentloaded',timeout=45000)
  if response and response.status>=400:raise RuntimeError(f'{role} unavailable: HTTP {response.status} at {url}')
  page.wait_for_timeout(900)
  page.evaluate("""() => {document.querySelector('button.cc-allow')?.click();if(location.hostname==='127.0.0.1'){localStorage.setItem('bhr-cookie-consent','accepted');const e=document.querySelector('#cookie-layer');if(e)e.hidden=true;}document.documentElement.style.scrollBehavior='auto'}""")
  page.mouse.move(-20,-20)
  page.evaluate('document.fonts.ready')
  total=page.evaluate('document.documentElement.scrollHeight')
  for y in range(0,total,max(height-100,400)):
   page.evaluate('(y)=>scrollTo(0,y)',y);page.wait_for_timeout(90)
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(350)
  page.screenshot(path=str(out/f'{label}-{role}.png'),full_page=True,scale='css',animations='allow')
  inventory=page.evaluate(INVENTORY)
  vp=inventory['viewport']
  assert vp['width']==width and vp['height']==height and vp['dpr']==1 and vp['scale']==1,vp
  dom=skill.collect_dom_audit(page);content=skill.collect_page_content(page);html=content.pop('html',None)
  (out/f'{label}-{role}-dom.json').write_text(json.dumps(dom,indent=2,ensure_ascii=False))
  (out/f'{label}-{role}-content.json').write_text(json.dumps(content,indent=2,ensure_ascii=False))
  (out/f'{label}-{role}-inventory.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False))
  (out/f'{label}-{role}-text.txt').write_text(content.get('text',''))
  if html:(out/f'{label}-{role}.html').write_text(html)
  return {'status':response.status if response else None,'final_url':page.url,'title':page.title(),'viewport':vp,'domAudit':str(out/f'{label}-{role}-dom.json'),'inventory':str(out/f'{label}-{role}-inventory.json')}
 finally:context.close()

def run(route):
 out=(args.out/route['key']).resolve();out.mkdir(parents=True,exist_ok=True)
 if args.resume and (out/'capture.json').exists():return {'key':route['key'],'resumed':True}
 # Route inventory records the planning gap; recheck after implementation so
 # newly created pages are reported as real candidates rather than still absent.
 actual_local=(PROJECT/'app/dist'/route['route'].strip('/')/'index.html').exists()
 def revision():
  paths=[PROJECT/'app/dist'/route['route'].strip('/')/'index.html']+[PROJECT/'app/dist'/name for name in ['theme.css','responsive.css','inner-pages.css','parity.css','secondary-parity.css','site.mjs','secondary.mjs','secondary-behavior.mjs','behavior.mjs']]
  digest=hashlib.sha256()
  for path in paths:
   if path.exists():digest.update(path.name.encode());digest.update(path.read_bytes())
  return digest.hexdigest()
 result={**route,'planningLocalExists':route['localExists'],'localExists':actual_local,'capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidateBuildHash':revision(),'viewports':[]}
 widths=args.viewport or (list(VIEWPORTS) if args.all_widths else route['widths'])
 result['planningWidths']=route['widths'];result['widths']=widths
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch()
   for label in widths:
    if args.reference_cache:
     cache=args.reference_cache/route['key']
     inventory=json.loads((cache/f'{label}-reference-inventory.json').read_text())
     vp=inventory['viewport'];width,height=VIEWPORTS[label]
     assert vp['width']==width and vp['height']==height and vp['dpr']==1 and vp['scale']==1,vp
     for source in cache.glob(f'{label}-reference*'):
      if source.is_file():shutil.copy2(source,out/source.name)
     reference={'status':200,'final_url':route['reference'],'viewport':vp,'domAudit':str(out/f'{label}-reference-dom.json'),'inventory':str(out/f'{label}-reference-inventory.json'),'cacheSource':str(cache)}
    else:reference=capture(browser,route['reference'],label,'reference',out)
    view={'label':label,'reference':reference}
    local=PROJECT/'app/dist'/route['route'].strip('/')/'index.html'
    if local.exists():view['candidate']=capture(browser,route['candidate'],label,'candidate',out)
    else:view['candidate']=None
    result['viewports'].append(view)
   browser.close()
  if all(v['candidate'] is not None for v in result['viewports']):
   # Attach measured DOM metadata before the image-only CLI evaluates zoom.
   cmd=[sys.executable,str(ROOT/'compare-cached.py'),'--reference',route['reference'],'--candidate',route['candidate'],'--reference-image-dir',str(out),'--candidate-image-dir',str(out),'--out',str(out),'--fail-on-zoom-mismatch']
   for label in widths:cmd+=['--viewport',f'{label}:{VIEWPORTS[label][0]}x{VIEWPORTS[label][1]}']
   with (out/'comparison.log').open('w') as log:subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=True)
   report=json.loads((out/'report.json').read_text())
   for v in report['viewports']:
    capture_view=next(i for i in result['viewports'] if i['label']==v['label'])
    for role in ['reference','candidate']:
     v[role].update(capture_view[role]);v[role]['domSummary']=json.loads((out/f"{v['label']}-{role}-dom.json").read_text())
    v['zoomDiagnostics']=skill.zoom_diagnostics(v['reference'],v['candidate'],.001)
    assert not v['zoomDiagnostics']['warnings'],v['zoomDiagnostics']
   skill.write_reports(report,out)
  result['candidateRevisionChanged']=result['candidateBuildHash']!=revision()
  (out/'capture.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
  print(route['key'],'captured',len(widths),'widths','comparison' if actual_local else 'MISSING LOCAL',flush=True)
 except Exception as e:
  result['error']=str(e);(out/'error.json').write_text(json.dumps(result,indent=2));print(route['key'],'ERROR',str(e)[:180],flush=True)
 return result

with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:results=list(pool.map(run,routes))
args.out.mkdir(parents=True,exist_ok=True);(args.out/'capture-summary.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
raise SystemExit(any('error' in r for r in results))
