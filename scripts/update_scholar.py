"""Refresh the two static publication cards from the public Scholar profile.

No dependencies or browser-side requests. A failed fetch/parse leaves files intact.
"""
import argparse
from datetime import datetime, timedelta, timezone
from html import escape, unescape
import json
import math
from pathlib import Path
import re
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://scholar.google.com/citations?user=EZSfJd0AAAAJ&hl=en'
START, END = '<!-- scholar-stats:start -->', '<!-- scholar-stats:end -->'


def parse_profile(source):
    def text(fragment):
        return unescape(re.sub(r'<[^>]+>', '', fragment)).strip()

    def cells(fragment, css_class):
        return [text(x) for x in re.findall(
            rf'<(?:td|th|span)\b[^>]*class="{css_class}"[^>]*>(.*?)</(?:td|th|span)>',
            fragment, re.S)]

    table = re.search(r'<table\b[^>]*id="gsc_rsb_st"[^>]*>(.*?)</table>', source, re.S)
    name = re.search(r'<div\b[^>]*id="gsc_prf_in"[^>]*>(.*?)</div>', source, re.S)
    if not table or not name or text(name[1]) != 'Yang-Bo Ye':
        raise ValueError('Expected public Scholar profile was not returned.')
    values = cells(table[1], 'gsc_rsb_std')
    headers = cells(table[1], 'gsc_rsb_sth')
    years, counts = cells(source, 'gsc_g_t'), cells(source, 'gsc_g_al')
    if len(values) != 6 or len(headers) != 3 or not re.fullmatch(r'Since 20\d{2}', headers[2]):
        raise ValueError('Scholar metric table changed or is incomplete.')
    if not years or len(years) != len(counts):
        raise ValueError('Scholar annual citation chart is incomplete.')
    numbers = values + years + counts
    if any(not re.fullmatch(r'\d+(?:,\d{3})*', n) for n in numbers):
        raise ValueError('Non-numeric Scholar data; keeping the previous snapshot.')
    values = [int(n.replace(',', '')) for n in values]
    annual = [{'year': int(y), 'citations': int(c.replace(',', ''))} for y, c in zip(years, counts)]
    if [a['year'] for a in annual] != sorted(set(a['year'] for a in annual)):
        raise ValueError('Duplicate or unordered citation years.')
    if any(values[i + 1] > values[i] for i in (0, 2, 4)):
        raise ValueError('Recent metrics cannot exceed all-time metrics.')
    return {'source': URL, 'updated': datetime.now(timezone(timedelta(hours=8))).date().isoformat(),
            'since': int(headers[2][-4:]), 'citations': values[:2],
            'h_index': values[2:4], 'i10_index': values[4:], 'annual': annual}


def render_card(data, zh=False):
    title = '引用情况' if zh else 'Cited by'
    labels = ('引用次数', 'h-index', 'i10-index') if zh else ('Citations', 'h-index', 'i10-index')
    since = f'{data["since"]} 年以来' if zh else f'Since {data["since"]}'
    rows = ''.join(f'<tr><th scope="row">{label}</th><td>{data[key][0]:,}</td><td>{data[key][1]:,}</td></tr>'
                   for label, key in zip(labels, ('citations', 'h_index', 'i10_index')))
    # Show the latest seven years, matching the compact Scholar chart.
    annual = data['annual'][-7:]
    peak = max(a['citations'] for a in annual)
    step = max(1, math.ceil(peak / 4 / 10) * 10)
    ceiling = step * 4
    svg = '<svg class="citation-chart" viewBox="0 0 300 190" role="img" aria-labelledby="citation-chart-title"><title id="citation-chart-title">'
    svg += ('年度引用次数：' if zh else 'Citations per year: ')
    svg += escape('; '.join(f'{a["year"]}: {a["citations"]}' for a in annual)) + '</title>'
    for i in range(5):
        y = 152 - i * 32
        svg += f'<line x1="6" y1="{y}" x2="266" y2="{y}" class="citation-grid"/><text x="298" y="{y + 4}" text-anchor="end" class="citation-axis">{step * i}</text>'
    slot = 260 / len(annual)
    for i, item in enumerate(annual):
        x, height = 6 + (i + .5) * slot, item['citations'] / ceiling * 128
        svg += f'<rect x="{x - slot * .28:.2f}" y="{152 - height:.2f}" width="{slot * .56:.2f}" height="{height:.2f}" rx="2" class="citation-bar"><title>{item["year"]}: {item["citations"]}</title></rect>'
        svg += f'<text x="{x:.2f}" y="{145 - height:.2f}" text-anchor="middle" class="citation-value">{item["citations"]}</text><text x="{x:.2f}" y="173" text-anchor="middle" class="citation-axis">{item["year"]}</text>'
    svg += '</svg>'
    updated = '更新于' if zh else 'Updated'
    link = '查看 Google Scholar →' if zh else 'View Google Scholar →'
    return f'''<aside class="scholar-card" aria-labelledby="scholar-title">
<p class="eyebrow" lang="en">Google Scholar</p><h2 id="scholar-title">{title}</h2>
<table class="scholar-metrics"><caption class="sr-only">{title}</caption><thead><tr><th scope="col"><span class="sr-only">{'指标' if zh else 'Metric'}</span></th><th scope="col">{'全部' if zh else 'All'}</th><th scope="col">{since}</th></tr></thead><tbody>{rows}</tbody></table>
{svg}
<p class="scholar-updated">{updated} <time datetime="{data['updated']}">{data['updated']}</time></p>
<a class="scholar-profile" href="{escape(URL, quote=True)}">{link}</a>
</aside>'''


def save_snapshot(data, root=ROOT):
    # Prepare both pages first, so missing markers cannot leave a half-updated site.
    outputs = {}
    for filename, zh in [('publications.html', False), ('zh/publications.html', True)]:
        path = root / filename
        source = path.read_text(encoding='utf-8')
        if source.count(START) != 1 or source.count(END) != 1 or source.index(START) > source.index(END):
            raise ValueError(f'Missing or duplicate Scholar markers in {filename}')
        before, rest = source.split(START)
        _, after = rest.split(END)
        outputs[path] = before + START + '\n' + render_card(data, zh) + '\n' + END + after
    outputs[root / 'assets/scholar/stats.json'] = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--html', type=Path, help='Use a previously fetched profile HTML (offline check).')
    args = parser.parse_args()
    try:
        if args.html:
            source = args.html.read_text(encoding='utf-8')
        else:
            with urlopen(URL, timeout=30) as response:
                source = response.read().decode(response.headers.get_content_charset() or 'utf-8')
        data = parse_profile(source)
        save_snapshot(data)
        print(f'Scholar updated: {data["citations"][0]} citations, {data["updated"]}')
    except Exception as error:
        raise SystemExit(f'Scholar update failed: {error}')
