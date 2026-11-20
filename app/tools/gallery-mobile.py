"""Build a small inline gallery; complete per-page evidence stays in report.html."""
import base64,html,json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'checks/mobile-parity-2026-11-20';REPORT=BASE/'accepted-report/mobile';out=BASE/'gallery';out.mkdir(exist_ok=True)
data=json.loads((REPORT/'report.json').read_text());keys=['expertises','contact','afspraak-maken','home','projecten','expertises--paneelbouw','over-ons','vacature--monteur-paneelbouw'];frames=[]
for key in keys:
 r=next(r for r in data['rows']if r['key']==key);d=r['diff'];paths=[]
 for role in ['reference','candidate']:
  source=Path(r[role]);image=Image.open(source).convert('RGB');image.thumbnail((330,15000));path=out/(key+'-'+role+'.jpg');image.save(path,quality=72);paths.append(str(path))
 heat=Image.open(d['heatmapImage']).convert('RGB');heat.thumbnail((330,15000));heatpath=out/(key+'-heatmap.jpg');heat.save(heatpath,quality=72)
 frames.append({'label':r['route'],'paths':paths,'heat':str(heatpath),'metrics':f'{r["status"]} · mismatch {d["mismatchPercent"]:.2f}% · SSIM {d["ssimEstimate"]:.4f} · height Δ {r["heightDelta"]:+d}px'})
for mode,ref,cand in [('Phone menu',BASE/'final-3/states/reference-menu.png',BASE/'accepted-states/states/candidate-menu.png'),('Tablet menu',BASE/'final-3-tablet/states/reference-menu.png',BASE/'accepted-tablet-states/states/candidate-menu.png')]:
 paths=[]
 for role,source in [('reference',ref),('candidate',cand)]:
  im=Image.open(source).convert('RGB');im.thumbnail((380,1200));path=out/(mode.split()[0]+'-'+role+'.jpg');im.save(path,quality=80);paths.append(str(path))
 frames.append({'label':mode,'paths':paths,'heat':None,'metrics':'Native menu state · no masks. The source’s encoded Industries label is deliberately corrected locally.'})
options=''.join(f'<option value="{i}">{html.escape(f["label"])}</option>'for i,f in enumerate(frames));panels=[]
for i,f in enumerate(frames):
 panels.append(f'<section data-panel="{i}"{ " hidden"if i else""}><p class="metrics">{html.escape(f["metrics"])}</p><div class="pair">'+''.join(f'<figure><figcaption>{label}</figcaption><div class="scroll"><img src="{path}" alt="{label} — {html.escape(f["label"])}"></div></figure>'for label,path in zip(['Live reference','Local'],f['paths']))+'</div>'+ (f'<div class="heat" hidden><div class="scroll"><img src="{f["heat"]}" alt="Difference heatmap"></div></div>'if f['heat']else'')+'</section>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:none;color:var(--foreground);font-family:var(--font-sans)}*{box-sizing:border-box}header{display:flex;align-items:end;gap:16px;flex-wrap:wrap}label{display:grid;gap:6px;flex:1;min-width:180px}select,button{font:inherit;color:var(--foreground);background:var(--secondary);border:1px solid var(--border);border-radius:var(--radius);padding:10px 12px}button{cursor:pointer}p{line-height:1.5}.metrics{font-family:var(--font-mono);font-size:12px;color:var(--muted-foreground);margin:14px 0}.pair{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px}figure{margin:0;min-width:0;background:var(--card);border-radius:var(--radius);padding:16px}figcaption{font-size:13px;margin-bottom:10px}.scroll{height:650px;overflow:auto;scrollbar-width:thin}img{display:block;width:100%;height:auto}.heat{max-width:380px;margin:auto}.note{font-size:12px;color:var(--muted-foreground);margin-bottom:0}[hidden]{display:none!important}@media(max-width:480px){figure{padding:6px}.pair{gap:6px}.scroll{height:500px}}
</style><header><label>Compare page or menu<select id="page">'''+options+'''</select></label><button id="view" type="button">Show heatmap</button></header>'''+''.join(panels)+'''<p class="note">390×844 phone captures, DPR1 and scale1. Scroll either image to compare the full page. OPEN means the strict visual target is not met. These reduced previews do not replace the full PNGs and per-page reports.</p><script>
const select=document.querySelector('#page'),button=document.querySelector('#view');let heat=false;
function show(){document.querySelectorAll('[data-panel]').forEach(p=>p.hidden=p.dataset.panel!==select.value);const p=document.querySelector('[data-panel="'+select.value+'"]');button.disabled=!p.querySelector('.heat');p.querySelector('.pair').hidden=heat&&!button.disabled;if(p.querySelector('.heat'))p.querySelector('.heat').hidden=!heat;button.textContent=heat?'Show page pair':'Show heatmap'}
select.addEventListener('change',()=>{heat=false;show()});button.addEventListener('click',()=>{heat=!heat;show()});document.querySelectorAll('.pair').forEach(pair=>{const panes=pair.querySelectorAll('.scroll');let busy=false;panes.forEach((pane,i)=>pane.addEventListener('scroll',()=>{if(busy)return;busy=true;panes[1-i].scrollTop=pane.scrollTop;requestAnimationFrame(()=>busy=false)}))});show();
</script></html>'''
(out/'gallery.html').write_text(page)
standalone=re.sub(r'src="([^"]+)"',lambda m:'src="data:image/jpeg;base64,'+base64.b64encode(Path(m.group(1)).read_bytes()).decode()+'"',page)
(out/'gallery-standalone.html').write_text(standalone);print(out/'gallery.html')
