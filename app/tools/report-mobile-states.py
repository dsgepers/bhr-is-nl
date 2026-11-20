"""Compare native menu/sticky frames with the same visual-diff implementation."""
import importlib.util,json,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20';sp=importlib.util.spec_from_file_location('state_diff',Path.home()/'.codex/skills/visual-diff/scripts/compare_page.py');skill=importlib.util.module_from_spec(sp);sys.modules[sp.name]=skill;sp.loader.exec_module(skill)
rows=[]
for mode,refphase,phase,w,h in [('phone','final-3','accepted-states',390,844),('tablet','final-3-tablet','accepted-tablet-states',768,1024)]:
 for state in ['closed','menu','about','industries','scrolled']:
  ref=BASE/refphase/'states'/('reference-'+state+'.png');cand=BASE/phase/'states'/('candidate-'+state+'.png');out=BASE/'accepted-report/states'/mode/state;out.mkdir(parents=True,exist_ok=True)
  for path in [ref.with_suffix('.json'),cand.with_suffix('.json')]:
   v=json.loads(path.read_text())['viewport'];assert v['dpr']==1 and v['scale']==1 and v['width']==w,v
  diff=skill.compare_images(ref,cand,skill.ViewportSpec(state,w,h,1),out,SimpleNamespace(background='#ffffff',threshold=5,zoom_rect=[],color_pick=[],color_pick_rect=[]));rows.append({'mode':mode,'state':state,'diff':diff,'strict':'PASS'if diff['mismatchPercent']<=.5 and diff['ssimEstimate']>=.985 else'OPEN','intentionalDifference':'Readable Industries label replaces source encoding defect; no mask.'});print(mode,state,round(diff['mismatchPercent'],3),round(diff['ssimEstimate'],5),flush=True)
(BASE/'accepted-report/states/report.json').write_text(json.dumps(rows,indent=2)+'\n')
