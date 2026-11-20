"""Compare device-correct cached frames with the installed visual-diff metrics.

No alignment, page masks, averaging, or rescaling enters acceptance metrics.
Desktop compares the immutable local before frame, not the public website.
"""
import argparse,base64,hashlib,html,importlib.util,json,sys
from pathlib import Path
from types import SimpleNamespace
from PIL import Image,ImageChops,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20'
p=argparse.ArgumentParser();p.add_argument('--mode',default='mobile');p.add_argument('--candidate-phase',default='final');p.add_argument('--reference-phase',default='baseline');p.add_argument('--output',default='report');p.add_argument('--route',action='append');args=p.parse_args()
sp=importlib.util.spec_from_file_location('mobile_diff',Path.home()/'.codex/skills/visual-diff/scripts/compare_page.py');skill=importlib.util.module_from_spec(sp);sys.modules[sp.name]=skill;sp.loader.exec_module(skill)
out=BASE/args.output/args.mode;out.mkdir(parents=True,exist_ok=True);desktop=args.mode in ['desktop','laptop'];refrole='candidate'if desktop else'reference'
routes=json.loads((BASE/'routes.json').read_text());routes=[r for r in routes if not args.route or r['route']in args.route]
if args.mode!='mobile'and not args.route:routes=[r for r in routes if(BASE/args.reference_phase/r['key']/args.mode/(refrole+'.json')).exists()]
rows=[];sheets=[]
for r in routes:
 refdir=BASE/args.reference_phase/r['key']/args.mode;canddir=BASE/args.candidate_phase/r['key']/args.mode;ref=refdir/(refrole+'.png');cand=canddir/'candidate.png'
 if not(refdir/(refrole+'.json')).exists()or not(canddir/'candidate.json').exists():
  rows.append({**r,'status':'MISSING CAPTURE'});continue
 rd=json.loads((refdir/(refrole+'.json')).read_text());cd=json.loads((canddir/'candidate.json').read_text())
 if rd.get('status',200)>=400:
  rows.append({**r,'status':'REFERENCE UNAVAILABLE','httpStatus':rd['status']});continue
 capture=json.loads((canddir/'capture.json').read_text());dest=out/r['key'];dest.mkdir(exist_ok=True)
 ri=Image.open(ref).convert('RGB');ci=Image.open(cand).convert('RGB');equal=ri.size==ci.size and ImageChops.difference(ri,ci).getbbox()is None
 if desktop and equal:
  diff={'mismatchPercent':0,'ssimEstimate':1,'sameSize':True,'referenceSize':{'width':ri.width,'height':ri.height},'candidateSize':{'width':ci.width,'height':ci.height}}
 else:
  diff=skill.compare_images(ref,cand,skill.ViewportSpec(args.mode,rd['viewport']['width'],rd['viewport'].get('viewportHeight',844),1),dest,SimpleNamespace(background='#ffffff',threshold=0 if desktop else 5,zoom_rect=[],color_pick=[],color_pick_rect=[]))
 heightDelta=ci.height-ri.height
 zoom=all(abs(rd['viewport'][x]-cd['viewport'][x])<.001 for x in ['dpr','scale'])
 failures=[]
 if capture['revisionChanged']:failures.append('candidate revision changed during capture')
 if not zoom:failures.append('zoom/DPR differs')
 if desktop:
  if not equal:failures.append('desktop pixels changed')
 else:
  if diff['mismatchPercent']>.5:failures.append('mismatch > 0.5%')
  if diff['ssimEstimate']<.985:failures.append('SSIM < 0.985')
  if abs(heightDelta)>2:failures.append('|height delta| > 2px')
 row={**r,'status':'OPEN'if failures else'PASS','classification':'close clone'if not desktop and diff['mismatchPercent']<5 and diff['ssimEstimate']>.93 else None,'failures':failures,'heightDelta':heightDelta,'diff':diff,'reference':str(ref),'candidate':str(cand),'revision':capture['revisionAfter'],'sameZoom':zoom,'normalization':'DPR1/scale1; denied cookies; lazy images; settled fonts/finite transitions; first hero/partner item; viewport tiles with one header; sticky sidebars static; no masks'};rows.append(row)
 for kind,im in [('reference',ri),('candidate',ci)]:
  thumb=im.copy();thumb.thumbnail((195,14000));thumb.save(dest/(kind+'.jpg'),quality=65)
 # All routes are available for direct contact-sheet inspection; never metric-scaled.
 sheet=Image.new('RGB',(410,46+max(round(ri.height*195/ri.width),round(ci.height*195/ci.width))),'white');draw=ImageDraw.Draw(sheet);draw.text((5,5),r['route'],fill='black');draw.text((5,24),f'{diff["mismatchPercent"]:.2f}% | SSIM {diff["ssimEstimate"]:.4f} | dh {heightDelta}',fill='black')
 for x,im in [(0,ri),(205,ci)]:
  im=im.resize((195,round(im.height*195/im.width)));sheet.paste(im,(x,46))
 sheets.append((r['key'],sheet));print(args.mode,r['route'],row['status'],round(diff['mismatchPercent'],3),round(diff['ssimEstimate'],5),heightDelta,flush=True)
(out/'report.json').write_text(json.dumps({'mode':args.mode,'candidatePhase':args.candidate_phase,'referencePhase':args.reference_phase,'rows':rows},ensure_ascii=False,indent=2)+'\n')
md=[f'# BHR {args.mode} visual comparison','',f'Candidate: `{args.candidate_phase}`. Reference: `{args.reference_phase}`. '+('Immutable local desktop before/after.'if desktop else'Live device theme. Strict gates are independent for each page.'),'','No masks or alignment. Pixel threshold '+('0'if desktop else'5')+'. SSIM is the installed skill’s global estimate.','', '| Page | Status | Mismatch | SSIM | Height delta |','|---|---|---:|---:|---:|']
for r in rows:
 d=r.get('diff',{});md.append(f'| `{r["route"]}` | {r["status"]} | {d.get("mismatchPercent", "—")} | {d.get("ssimEstimate", "—")} | {r.get("heightDelta", "—")} |')
(out/'report.md').write_text('\n'.join(md)+'\n')
for start in range(0,len(sheets),6):
 group=sheets[start:start+6];canvas=Image.new('RGB',(410*len(group),max(im.height for _,im in group)),'#ddd')
 for i,(_,im)in enumerate(group):canvas.paste(im,(410*i,0))
 canvas.save(out/f'contact-sheet-{start//6+1:02}.jpg',quality=70)
# A local full report retains each page and its diagnostic PNGs.
body=[]
for r in rows:
 d=r.get('diff',{});key=r['key'];body.append(f'<details><summary>{html.escape(r["route"])} — {r["status"]} · {d.get("mismatchPercent","—")}% · SSIM {d.get("ssimEstimate","—")} · Δh {r.get("heightDelta","—")}</summary>')
 if 'diff'in r:body.append(f'<div class="pair"><a href="{r["reference"]}"><img loading="lazy" src="{key}/reference.jpg" alt="Reference"></a><a href="{r["candidate"]}"><img loading="lazy" src="{key}/candidate.jpg" alt="Candidate"></a></div><p>'+html.escape('; '.join(r['failures'])or'All applicable gates pass')+'</p>')
 body.append('</details>')
(out/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>BHR visual comparison</title><style>body{font:16px/1.5 system-ui;max-width:1000px;margin:auto;padding:24px}summary{cursor:pointer;padding:12px;border-bottom:1px solid #ddd}.pair{display:flex;gap:20px;align-items:flex-start}.pair a{width:50%}.pair img{width:100%;height:auto}</style><h1>BHR '+args.mode+' comparison</h1><p>Left: reference. Right: local. Every route has an independent gate; OPEN means the strict target is not met.</p>'+''.join(body)+'</html>')
