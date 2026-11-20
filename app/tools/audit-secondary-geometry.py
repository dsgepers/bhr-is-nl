"""Fast geometry diagnostics against frozen source inventories; not a visual gate."""
import argparse,asyncio,json,re
from pathlib import Path
from playwright.async_api import async_playwright
P=argparse.ArgumentParser();P.add_argument('--reference',type=Path,required=True);P.add_argument('--out',type=Path,required=True);P.add_argument('--viewport',action='append',default=[]);P.add_argument('--route',action='append',default=[]);args=P.parse_args()
ROOT=Path(__file__).resolve().parents[2];routes=json.loads((ROOT/'checks/visual-planning-2026-11-20/routes.json').read_text());VIEWPORTS={'wide':(1920,1080),'desktop':(1440,900),'tablet':(768,1024),'mobile':(390,844)}
if args.route:routes=[r for r in routes if r['key']in args.route or r['route']in args.route]
normalize=lambda t:re.sub(r'\s+',' ',t).strip()
async def main():
 async with async_playwright()as p:
  browser=await p.chromium.launch();sem=asyncio.Semaphore(4)
  async def one(route,label):
   async with sem:
    w,h=VIEWPORTS[label];context=await browser.new_context(viewport={'width':w,'height':h},reduced_motion='reduce');page=await context.new_page();await page.add_init_script("localStorage.setItem('bhr-cookie-consent','accepted')");await page.goto(route['candidate']);await page.evaluate('document.fonts.ready');await page.evaluate('Promise.all([...document.images].map(e=>e.decode().catch(()=>{})))');await page.wait_for_timeout(30)
    candidate=await page.evaluate("""()=>({height:document.documentElement.scrollHeight,headings:[...document.querySelectorAll('h1,h2,h3,h4')].filter(e=>!e.closest('footer')&&e.getBoundingClientRect().height>0).map(e=>{let r=e.getBoundingClientRect();return {text:e.innerText.trim().replace(/\\s+/g,' '),box:{x:r.x,y:r.y+scrollY,width:r.width,height:r.height}}})})""");await context.close()
    source=json.loads((args.reference/route['key']/f'{label}-reference-inventory.json').read_text());differences=[]
    for h in source['headings']:
     if h['box']['y']<0:continue
     matches=[c for c in candidate['headings']if normalize(c['text'])==normalize(h['text'])];c=min(matches,key=lambda c:abs(c['box']['y']-h['box']['y'])+abs(c['box']['x']-h['box']['x']))if matches else None
     if c:
      delta={k:round(c['box'][k]-h['box'][k],3)for k in ['x','y','width','height']}
      if any(abs(v)>2 for v in delta.values()):differences.append({'text':h['text'][:90],'delta':delta,'reference':h['box'],'candidate':c['box']})
    return {'key':route['key'],'route':route['route'],'viewport':label,'heightDelta':candidate['height']-source['viewport']['scrollHeight'],'differences':differences}
  results=await asyncio.gather(*(one(r,l)for r in routes for l in (args.viewport or VIEWPORTS)));await browser.close();args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n');print(f'{len(results)} geometry diagnostics saved')
asyncio.run(main())
