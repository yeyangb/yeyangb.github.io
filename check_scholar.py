"""Offline checks for citation parsing, failure preservation and bilingual links."""
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from scripts.update_scholar import START, END, ROOT, parse_profile, render_card, save_snapshot

# Minimal public-profile markup, including zero citations and formatted numbers.
sample = '''<div id="gsc_prf_in">Yang-Bo Ye</div><table id="gsc_rsb_st">
<th class="gsc_rsb_sth"></th><th class="gsc_rsb_sth">All</th><th class="gsc_rsb_sth">Since 2022</th>
<td class="gsc_rsb_std">1,345</td><td class="gsc_rsb_std">341</td>
<td class="gsc_rsb_std">7</td><td class="gsc_rsb_std">7</td>
<td class="gsc_rsb_std">6</td><td class="gsc_rsb_std">6</td></table>
<span class="gsc_g_t" style="right:30px">2025</span><span class="gsc_g_t">2026</span>
<span class="gsc_g_al">0</span><span class="gsc_g_al">106</span>'''
data = parse_profile(sample)
assert data['citations'] == [1345, 341] and data['since'] == 2022
assert data['annual'] == [{'year': 2025, 'citations': 0}, {'year': 2026, 'citations': 106}]
for bad in ('<html>Captcha / access denied</html>', sample.replace('Yang-Bo Ye', 'Other Author'),
            sample.replace('>106<', '>unavailable<'), sample.replace('>2026<', '>2025<'),
            sample.replace('>341<', '>2,000<'), sample.replace('<span class="gsc_g_al">0</span>', '')):
    try:
        parse_profile(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid Scholar response was accepted')

with TemporaryDirectory() as directory:
    root = Path(directory)
    (root / 'zh').mkdir()
    original = f'<main>{START}old snapshot{END}</main>'
    (root / 'publications.html').write_text(original, encoding='utf-8')
    (root / 'zh/publications.html').write_text('missing markers', encoding='utf-8')
    try:
        save_snapshot(data, root)
    except ValueError:
        pass
    else:
        raise AssertionError('Missing page marker was accepted')
    assert (root / 'publications.html').read_text(encoding='utf-8') == original
    assert not (root / 'assets/scholar/stats.json').exists()
    (root / 'zh/publications.html').write_text(original, encoding='utf-8')
    save_snapshot(data, root)
    assert json.loads((root / 'assets/scholar/stats.json').read_text(encoding='utf-8')) == data
    assert '2022 年以来' in (root / 'zh/publications.html').read_text(encoding='utf-8')

links = {'paper-autumn-heat-2026': 'school-heat-2024.html', 'paper-cold-2023': 'cold-2023.html',
         'paper-heat-2023': 'north-china-heat-2023.html', 'paper-compound-2020': 'compound-2020.html',
         'paper-rain-2020': 'southwest-rainfall-2020.html', 'paper-conditional-2020': 'meiyu-2020.html'}
snapshot = json.loads((ROOT / 'assets/scholar/stats.json').read_text(encoding='utf-8'))
for filename, zh in [('publications.html', False), ('zh/publications.html', True)]:
    source = (ROOT / filename).read_text(encoding='utf-8')
    assert source.count('class="publication-highlight"') == 6
    for ident, target in links.items():
        article = re.search(rf'<article\b[^>]*id="{ident}".*?</article>', source, re.S)[0]
        assert f'href="{target}"' in article
    assert render_card(snapshot, zh) in source, 'Card and stored citation snapshot differ'
print('Scholar checks passed: parsing, failed-update preservation, both cards and 12 article links.')
