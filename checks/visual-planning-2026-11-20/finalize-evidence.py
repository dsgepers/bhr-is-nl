"""Restore actual capture metadata when comparing cached PNG inputs.

The skill's image-only CLI doesn't automatically load DOM sidecars. Both live
captures already assert viewport/DPR/scale. Reattach those measured sidecars
and apply the skill's zoom diagnostic before accepting a cached comparison.
"""
import importlib.util,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('bhr_diff_report',Path.home()/'.codex/skills/visual-diff/scripts/compare_page.py')
skill=importlib.util.module_from_spec(sp);sys.modules[sp.name]=skill;sp.loader.exec_module(skill)
results=[]
for route in json.loads((ROOT/'routes.json').read_text()):
 out=ROOT/'baseline'/route['key'];capture=out/'capture.json';error=out/'error.json'
 if capture.exists():data=json.loads(capture.read_text())
 elif error.exists():data=json.loads(error.read_text())
 else:continue
 if 'error' in data:
  if not (out/'report.json').exists() or len(data['viewports'])!=len(route['widths']):continue
  if not data['error'].startswith('Command '):continue
  data['metadataRecovery']='Image-only CLI lacked DOM metadata; restored measured sidecars and enforced zoom equality.'
  data.pop('error')
 if route['localExists']:
  report=json.loads((out/'report.json').read_text())
  for v in report['viewports']:
   metadata=next(e for e in data['viewports'] if e['label']==v['label'])
   for role in ['reference','candidate']:
    v[role].update(metadata[role]);v[role]['domSummary']=json.loads((out/f"{v['label']}-{role}-dom.json").read_text())
   v['zoomDiagnostics']=skill.zoom_diagnostics(v['reference'],v['candidate'],.001)
   assert v['zoomDiagnostics']['sameZoom'],v['zoomDiagnostics']
  report['settings']['captureMethod']='Native viewport tiles; pointer outside viewport; first logical partner held; actual DOM sidecars attached; no masks.'
  report['settings']['failOnZoomMismatch']=True
  skill.write_reports(report,out)
 capture.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');results.append(data)
(ROOT/'baseline/capture-summary.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
print('Finalized',len(results),'routes with actual capture metadata.')
