"""Convert public, read-only page evidence to content data; never imports code."""
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
pages = {}
def clean(text):
    return re.sub(r'【\d+†([^】†]+)(?:†[^】]+)?】', r'\1', text).replace('\xa0', ' ').strip()

for file in sorted((root / 'reference').glob('public-pages-*.txt')):
    for source in file.read_text().split('-' * 80):
        match = re.search(r'"ref_id":\s*"(https://(?:www\.)?bhr-is.nl[^\"]*)"', source)
        if not match or 'Total lines:' not in source:
            continue
        url = urlsplit(match.group(1)).path or '/'
        lines = re.findall(r'^L\d+: ?(.*)$', source, re.M)
        h1 = next((i for i, line in enumerate(lines) if line.startswith('# ')), None)
        result = {'source': match.group(1), 'sections': [], 'faq': []}
        if h1 is not None:
            i = h1 + 1
            heading = [clean(lines[h1][2:])]
            while i < len(lines) and 0 < len(clean(lines[i])) < 80 and not lines[i].startswith(('【', '#')):
                heading.append(clean(lines[i])); i += 1
            result['heading'] = ' '.join(heading).replace('- ', '-')
            while i < len(lines) and not lines[i].strip(): i += 1
            if i < len(lines) and not lines[i].startswith(('【', '#', '[')):
                result['intro'] = clean(lines[i])
        for i, line in enumerate(lines):
            if not line.startswith('## '): continue
            title = clean(line[3:])
            j = i + 1
            content = []
            while j < len(lines):
                row = lines[j]
                if row.startswith('#') or '†Image:' in row or clean(row).startswith('Your system inte'): break
                if clean(row) in ['Onze branches', 'FAQ', 'Ontdek jouw mogelijkheden', 'Hoe wij jou van dienst zijn', 'Vakmanschap van begin tot eind', 'Partners', 'Contactformulier', 'Werken bij BHR', 'Ruimte om te groeien']: break
                if row.strip() and not re.fullmatch(r'(?:【[^】]+】\s*)+', row.strip()) and not row.strip().startswith('[Input]'):
                    content.append(clean(row))
                j += 1
            if 'Veelgestelde vragen' in title or title == 'Vind je antwoorden':
                for row in content:
                    if row.startswith('* '):
                        result['faq'].append([row[2:].strip(), ''])
                    elif result['faq']:
                        result['faq'][-1][1] += (' ' if result['faq'][-1][1] else '') + row
                result['faqTitle'] = title
            elif re.match(r'In welke branches|Panelenbouw die', title):
                result['branchAt'] = len(result['sections'])
                result['branchTitle'] = title
                result['branchIntro'] = ' '.join(content)
            elif content and not re.match(r'Onze expertises|Onze samenwerkingen|Hoe BHR werkt|What makes|Uitgelichte vacatures|Dit is BHR|Wat ons drijft|Vind je antwoorden|Gedreven en betrokken|Samen maken we het verschil', title):
                result['sections'].append({'title': title, 'content': content})
        if h1 is not None:
            first = next((i for i in range(h1 + 1, len(lines)) if lines[i].startswith('## ')), len(lines))
            lead = []
            for row in lines[h1 + 1:first]:
                if len(clean(row)) > 100 and not row.strip().startswith(('【', '#')) and clean(row) != result.get('intro'):
                    lead.append(clean(row))
            result['lead'] = lead
        pages[url] = result
(root / 'page-content.json').write_text(json.dumps(pages, ensure_ascii=False, indent=2) + '\n')
print(f'Extracted individual content for {len(pages)} pages, {sum(len(p["sections"]) for p in pages.values())} sections.')
