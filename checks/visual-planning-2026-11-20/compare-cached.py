"""Invoke visual-diff on PNGs with their actual measured DOM sidecars attached."""
import importlib.util,json,sys
from pathlib import Path
sp=importlib.util.spec_from_file_location('bhr_cached_diff',Path.home()/'.codex/skills/visual-diff/scripts/compare_page.py')
skill=importlib.util.module_from_spec(sp);sys.modules[sp.name]=skill;sp.loader.exec_module(skill)
original=skill.image_only_capture
def capture(spec,role,source_dir,out_dir,url):
 result=original(spec,role,source_dir,out_dir,url)
 sidecar=Path(source_dir)/f'{spec.label}-{role}-dom.json'
 if not sidecar.exists():raise RuntimeError(f'Cannot validate cached capture without actual DOM metadata: {sidecar}')
 result['domSummary']=json.loads(sidecar.read_text());result['domAudit']=str(sidecar.resolve())
 return result
skill.image_only_capture=capture
if __name__=='__main__':raise SystemExit(skill.main())
