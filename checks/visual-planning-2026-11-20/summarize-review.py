"""Build per-page acceptance records from actual visual-diff reports; no averages."""
import argparse,json,html
from pathlib import Path
P=argparse.ArgumentParser();P.add_argument('run',type=Path);args=P.parse_args();root=Path(__file__).resolve().parents[2];run=args.run.resolve();routes=json.loads((root/'checks/visual-planning-2026-11-20/routes.json').read_text());plans=json.loads((root/'checks/visual-planning-2026-11-20/plan-index.json').read_text());views=['wide','desktop','tablet','mobile'];records=[];missing=[]
for route in routes:
 p=run/route['key'];file=p/'report.json'
 if not file.exists():missing.append(route['route']);continue
 report=json.loads(file.read_text());capture=json.loads((p/'capture.json').read_text());row={'route':route['route'],'key':route['key'],'reference':route['reference'],'candidate':route['candidate'],'candidateBuildHash':capture.get('candidateBuildHash'),'candidateRevisionChanged':capture.get('candidateRevisionChanged'),'views':[]};md=[f"# Implementation review: {route['route']}",f"\nReference: {route['reference']}  \nCandidate: {route['candidate']}", '\n1920px is primary. Every width has its own gate; no scores are averaged.', '\n| Width | Source / candidate height | Δheight | Mismatch | SSIM | Strict | Close clone |','|---|---:|---:|---:|---:|---|---|']
 for label in views:
  v=next((v for v in report['viewports']if v['label']==label),None)
  if not v:missing.append(route['route']+':'+label);continue
  d=v['diff'];delta=d['candidateSize']['height']-d['referenceSize']['height'];failed=[]
  if d['mismatchPercent']>.5:failed.append('pixel')
  if d['ssimEstimate']<.985:failed.append('ssim')
  if abs(delta)>2:failed.append('height')
  if capture.get('candidateRevisionChanged'):failed.append('revision')
  vp=v['reference'].get('viewport',{});cv=v['candidate'].get('viewport',{})
  if not all(x.get('dpr')==1 and x.get('scale')==1 for x in [vp,cv]):failed.append('zoom/DPR')
  strict=not failed;close=d['mismatchPercent']<5 and d['ssimEstimate']>.93
  row['views'].append({'label':label,'width':v['width'],'height':v['height'],'sourceHeight':d['referenceSize']['height'],'candidateHeight':d['candidateSize']['height'],'heightDelta':delta,'mismatchPercent':d['mismatchPercent'],'ssimEstimate':d['ssimEstimate'],'strict':strict,'closeClone':close,'failed':failed})
  md.append(f"| {v['width']}×{v['height']} | {d['referenceSize']['height']} / {d['candidateSize']['height']} | {delta:+} | {d['mismatchPercent']:.3f}% | {d['ssimEstimate']:.5f} | {'PASS'if strict else'OPEN: '+', '.join(failed)} | {'yes'if close else'no'} |")
 md+=['\nStrict: mismatch≤0.5%, SSIM≥0.985, |Δheight|≤2px, DPR1/scale1, stable candidate revision. Close clone is a separate <5% mismatch/SSIM>0.93 classification.', '\n## Evidence','\n[Interactive comparison](report.html) · [Raw metrics](report.json)']
 for v in row['views']:md.append(f"\n{v['label']}: [unmasked pair]({v['label']}-side-by-side-unmasked.png), [heatmap]({v['label']}-heatmap.png), [overlay]({v['label']}-overlay.png)")
 md+=['\nCookies are dismissed; the pointer is parked away; fonts and finite transitions settle. First original partner/banner frames are held. Tiling retains the original header and suppresses repeated floating chrome; vacancy sidebars are captured once in their original document position. No screenshot masks. Separate scrolled states are reviewed in the sibling states directory.','\nA failed width remains open. This record does not assert Craft’s independent likeness score.']
 (p/'review.md').write_text('\n'.join(md)+'\n');records.append(row)
summary={'pages':len(records),'views':sum(len(r['views'])for r in records),'missing':missing,'strictPasses':sum(v['strict']for r in records for v in r['views']),'strictOpen':sum(not v['strict']for r in records for v in r['views']),'byViewport':{l:{'strictPass':sum(v['strict']for r in records for v in r['views']if v['label']==l),'strictOpen':sum(not v['strict']for r in records for v in r['views']if v['label']==l),'closeClone':sum(v['closeClone']for r in records for v in r['views']if v['label']==l)}for l in views},'records':records}
(run/'acceptance.json').write_text(json.dumps(summary,indent=2)+'\n');(run/'open-gates.json').write_text(json.dumps([{'route':r['route'],**v}for r in records for v in r['views']if not v['strict']],indent=2)+'\n')
md=['# BHR remaining-page visual review','\n64 scoped routes;1920px primary. Source and candidate use the same viewport, DPR1 and scale1. Separate acceptance per page and width.','\n| Page |1920|1440|768|390|','|---|---|---|---|---|'];ht=[]
for r in records:
 cells=[]
 for v in r['views']:cells.append(f"{'PASS'if v['strict']else'OPEN'} {v['mismatchPercent']:.2f}% / {v['ssimEstimate']:.4f} / {v['heightDelta']:+}px")
 md.append(f"| [{r['route']}]({r['key']}/review.md) | "+' | '.join(cells)+' |');ht.append('<tr><th><a href="'+html.escape(r['key'])+'/report.html">'+html.escape(r['route'])+'</a></th>'+''.join('<td>'+html.escape(s)+'</td>'for s in cells)+'</tr>')
md+=['\nCells: strict gate, mismatch, SSIM, height delta. Open gates are not passes. See acceptance.json for all individual values, source/candidate dimensions, classification, and failed criteria.','\nFinal source/content and functional review notes are maintained in docs/superpowers/execution/2026-11-20-remaining-progress.md.']
(run/'README.md').write_text('\n'.join(md)+'\n');(run/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>BHR visual review</title><style>body{font:14px system-ui;background:#f0f6fa;color:#13284b;padding:30px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:10px;border:1px solid #d9e3ea;text-align:left}td{white-space:nowrap}h1{font-size:25px}a{color:#067da9}</style><h1>BHR:64-page visual review</h1><p>1920px primary. Individual strict gates at four widths. Each cell shows gate, mismatch, SSIM and height delta. An open gate remains open.</p><table><thead><tr><th>Page</th><th>1920×1080</th><th>1440×900</th><th>768×1024</th><th>390×844</th></tr></thead><tbody>'+''.join(ht)+'</tbody></table>')
print(json.dumps({k:v for k,v in summary.items()if k!='records'}));raise SystemExit(bool(missing))
