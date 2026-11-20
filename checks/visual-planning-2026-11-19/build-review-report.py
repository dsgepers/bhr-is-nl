"""Index the completed captures and make a compact in-conversation review gallery."""
from pathlib import Path
from PIL import Image
import html
import json

BASE=Path(__file__).resolve().parent
PROJECT=BASE.parent.parent
KEYS=['expertises','machinebouwers','proces-productie','service-en-onderhoud','partners','werken-bij']
LABELS=['Expertises','Machinebouwers','Proces & productie','Service & onderhoud','Partners','Werken bij']
VPS={'desktop':(1440,900),'tablet':(768,1024),'mobile':(390,844)}
summary=[]
for key,label in zip(KEYS,LABELS):
    report=json.loads((BASE/key/'report.json').read_text())
    entry={'key':key,'label':label,'reference':report['referenceUrl'],'candidate':report['candidateUrl'],'viewports':[]}
    for view in report['viewports']:
        d=view['diff']
        assert view['zoomDiagnostics']['sameZoom'], (key,view['label'],'zoom mismatch')
        assert d['referenceSize']['width']==view['width']==d['candidateSize']['width']
        entry['viewports'].append({'label':view['label'],'width':view['width'],'height':view['height'],'mismatchPercent':d['mismatchPercent'],'ssimEstimate':d['ssimEstimate'],'referenceSize':d['referenceSize'],'candidateSize':d['candidateSize'],'sameZoom':True})
        for name in ['reference','candidate','heatmap']:
            source=Image.open(BASE/key/f"{view['label']}-{name}.png").convert('RGB')
            source.crop((0,0,view['width'],min(view['height'],source.height))).save(BASE/key/f"{view['label']}-{name}-top.jpg",quality=88)
        for name in ['side-by-side','heatmap','overlay']:
            source=Image.open(BASE/key/f"{view['label']}-{name}.png").convert('RGB')
            source.thumbnail((1200,2400));source.save(BASE/key/f"{view['label']}-{name}-review.jpg",quality=86)
    summary.append(entry)
(BASE/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
lines=['# Six-page visual baseline','', 'Captured live references and the existing local build on 2026-11-19. Planning evidence; no application changes.','', 'Settings: Chromium, DPR 1, light scheme, nl-NL, Europe/Amsterdam; desktop 1440×900, tablet 768×1024, phone 390×844. Cookie consent dismissed. No content masks. Native viewport tiles preserve layered heroes, with repeated sticky headers suppressed after the first tile. Full document height is retained; horizontal off-canvas carousel overflow is excluded from screenshot width and retained in DOM diagnostics.','', 'Animations/carousels can vary. Metrics diagnose differences; they are not a likeness percentage or an acceptance result. Each full-page report includes side-by-side, heatmap, overlay, computed DOM, rendered text/HTML and image inventory.','', '| Page | Viewport | Pixel mismatch | SSIM estimate | Live dimensions | Local dimensions |','| --- | --- | ---: | ---: | --- | --- |']
for e in summary:
    for v in e['viewports']:
        r=v['referenceSize'];c=v['candidateSize'];lines.append(f"| [{e['label']}]({e['key']}/report.md) | {v['label']} | {v['mismatchPercent']:.2f}% | {v['ssimEstimate']:.4f} | {r['width']}×{r['height']} | {c['width']}×{c['height']} |")
lines+=['','All 18 comparisons have matched DPR/zoom diagnostics. Proposed future near-exact target: <=0.5% mismatch, >=0.985 SSIM, height delta <=2px, and manual review of every section and state. No current page passes this target.','', '## Reports and screenshots','']
for e in summary:
    k=e['key'];lines.append(f"- {e['label']}: [live page]({e['reference']}), [report]({k}/report.html), [desktop comparison]({k}/desktop-side-by-side.png), [heatmap]({k}/desktop-heatmap.png), [overlay]({k}/desktop-overlay.png). Tablet and phone versions are beside them.")
lines+=['','## Assets and functional baseline','','`asset-audit.json` records 59 unique-per-page source image references: 37 exact manifest entries, 10 other derivatives of the same photo, and 12 missing image sources. Exact derivatives must be packaged during implementation. Counts include the same asset when used on different pages.','','Existing checks passed: 33 tests; 44 routes, 2116 local links and 532 image/script references verified. These checks establish functionality, not visual parity.','','## Reproduce','','From the project root, serve the current build with `python -m http.server 4173 --bind 127.0.0.1 --directory app/dist`. In another terminal run:','','```bash','python checks/visual-planning-2026-11-19/run-comparisons.py --out checks/visual-review-<run-id>','# Add --route expertises (or another page key) for a single page.','```','','The helper uses `/tmp/bhr-visual-diff-venv/bin/python` by default. For a persistent Python environment with `playwright`, `pillow` and `numpy`, set `VISUAL_DIFF_PYTHON`; install its Playwright Chromium browser. The skill is loaded from `~/.codex/skills/visual-diff/scripts/compare_page.py`. No application dependencies were installed.','','Self-healing: added the repo-local capture adapter, runner and report builder. The global visual-diff skill was not modified. The stale shared-preview screenshots and superseded standard full-page captures are not part of this baseline.','','See [plan index](../../docs/superpowers/plans/2026-11-19-bhr-visual-parity.md) and [review record](review.md).']
(BASE/'README.md').write_text('\n'.join(lines)+'\n')
options=''.join(f'<option value="{e["key"]}">{html.escape(e["label"])}</option>' for e in summary)
cards=[]
for e in summary:
    for v in e['viewports']:
        vp=v['label'];k=e['key'];r=v['referenceSize'];c=v['candidateSize']
        imgs=''.join(f'<figure><figcaption>{label}</figcaption><img src="{html.escape(str(BASE/k/f"{vp}-{name}-top.jpg"))}" alt="{html.escape(e["label"])} {label}, {vp}"></figure>' for name,label in [('reference','Live reference'),('candidate','Current local')])
        cards.append(f'<article class="evidence" data-page="{k}" data-vp="{vp}" hidden><p class="metrics">Mismatch <strong>{v["mismatchPercent"]:.2f}%</strong> · SSIM {v["ssimEstimate"]:.4f}<br>Live {r["width"]}×{r["height"]} · Local {c["width"]}×{c["height"]}</p><div class="pair">{imgs}</div><details><summary>Show heatmap of this first screen</summary><img class="heat" src="{html.escape(str(BASE/k/f"{vp}-heatmap-top.jpg"))}" alt="Difference heatmap"></details></article>')
body='''<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;color:var(--foreground);font-family:var(--font-sans,system-ui);font-size:14px}*{box-sizing:border-box}label{display:inline-flex;gap:8px;align-items:center;margin:0 12px 10px 0}select{font:inherit;padding:7px;border-radius:var(--radius,6px);color:var(--foreground);background:var(--card);border:1px solid var(--border)}.muted{color:var(--muted-foreground);font-size:12px;line-height:1.5}.chart{margin:12px 0 18px}.row{display:grid;grid-template-columns:150px 1fr 58px;gap:8px;align-items:center;margin:7px 0;font-size:12px}.track{height:8px;background:var(--secondary);border-radius:4px;overflow:hidden}.bar{height:100%;background:var(--chart-1);border-radius:4px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0;min-width:0}figcaption{font-weight:600;margin:0 0 8px}img{display:block;width:100%;height:auto;border:1px solid var(--border);border-radius:var(--radius,6px)}.metrics{font-size:13px;line-height:1.6}.heat{max-height:650px;object-fit:contain;object-position:top}details{margin-top:12px}summary{cursor:pointer;color:var(--primary);margin-bottom:10px}[hidden]{display:none!important}@media(max-width:480px){.row{grid-template-columns:115px 1fr 48px}.pair{gap:8px}}
</style></head><body><label>Page <select id="page">OPTIONS</select></label><label>Width <select id="vp"><option value="desktop">Desktop · 1440px</option><option value="tablet">Tablet · 768px</option><option value="mobile">Phone · 390px</option></select></label><p class="muted">Full-page pixel mismatch by page. Lower is better. These are baseline diagnostics, not likeness scores. Screenshots below show the first screen; complete page comparisons are saved with the plans.</p><div class="chart" id="chart"></div>CARDS<script>const data=DATA;const p=document.getElementById('page'),v=document.getElementById('vp');function update(){document.querySelectorAll('.evidence').forEach(e=>e.hidden=e.dataset.page!==p.value||e.dataset.vp!==v.value);document.getElementById('chart').innerHTML=data.map(e=>{const x=e.viewports.find(x=>x.label===v.value);return '<div class="row"><span>'+e.label+'</span><div class="track"><div class="bar" style="width:'+x.mismatchPercent+'%"></div></div><span>'+x.mismatchPercent.toFixed(1)+'%</span></div>'}).join('')}p.onchange=v.onchange=update;update();</script></body></html>'''
body=body.replace('OPTIONS',options).replace('CARDS',''.join(cards)).replace('DATA',json.dumps(summary,ensure_ascii=False))
(BASE/'comparison-gallery.html').write_text(body)
print('Built index, summary, thumbnails and comparison-gallery.html for',len(summary),'pages /',sum(len(e['viewports']) for e in summary),'comparisons')
