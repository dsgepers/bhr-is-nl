"""Reuse only completed captures proved to match the unchanged final build."""
import hashlib,json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[2];base=root/'checks/visual-review-remaining-2026-11-20-final-a';out=root/'checks/visual-review-remaining-2026-11-20-final';workspace=root/'.superpowers/sdd/2026-11-20-bhr-remaining-pages';reserved=set(json.loads((workspace/'final-batch-1-keys.json').read_text()));log=[]
for source in sorted(base.glob('*/capture.json')):
 capture=json.loads(source.read_text());key=capture['key'];target=out/key
 # The running first batch owns its queued paths. Job candidates need the new
 # symmetric sidebar-normalization helper, even if their product hash matches.
 if key in reserved or key.startswith('vacature--')or target.exists()or capture.get('candidateRevisionChanged'):continue
 paths=[root/'app/dist'/capture['route'].strip('/')/'index.html']+[root/'app/dist'/n for n in ['theme.css','responsive.css','inner-pages.css','parity.css','secondary-parity.css','site.mjs','secondary.mjs','secondary-behavior.mjs','behavior.mjs']];digest=hashlib.sha256()
 for p in paths:
  if p.exists():digest.update(p.name.encode());digest.update(p.read_bytes())
 if capture.get('candidateBuildHash')!=digest.hexdigest():continue
 if {v['label']for v in capture['viewports']}!={'wide','desktop','tablet','mobile'}:continue
 for v in capture['viewports']:
  for role in ['reference','candidate']:
   vp=v[role]['viewport'];assert vp['dpr']==1 and vp['scale']==1
 if not(source.parent/'report.json').exists():continue
 shutil.copytree(source.parent,target)
 old=str(source.parent.resolve());new=str(target.resolve())
 for file in target.iterdir():
  if file.suffix in ['.json','.md','.html','.log','.txt']:
   text=file.read_text();file.write_text(text.replace(old,new))
 copied=json.loads((target/'capture.json').read_text());copied['reusedExactCandidateFrom']=old;copied['verifiedCurrentBuildHash']=digest.hexdigest();(target/'capture.json').write_text(json.dumps(copied,indent=2)+'\n')
 hashes={}
 for label in ['wide','desktop','tablet','mobile']:
  for role in ['reference','candidate']:
   name=f'{label}-{role}.png';a=hashlib.sha256((source.parent/name).read_bytes()).hexdigest();b=hashlib.sha256((target/name).read_bytes()).hexdigest();assert a==b;hashes[name]=a
 log.append({'key':key,'capturedAt':capture['capturedAt'],'buildHash':digest.hexdigest(),'pngHashes':hashes})
with(workspace/'exact-capture-reuse.jsonl').open('a')as f:
 for item in log:f.write(json.dumps(item)+'\n')
print('Reused exact current-revision captures',len(log))
