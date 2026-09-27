"""Regenerate static search metadata and sitemap after adding or editing pages."""
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Switch to https://yangboye.com after the certificate is issued and HTTPS is verified.
BASE = 'http://yangboye.com'
START, END = '<!-- search-metadata:start -->', '<!-- search-metadata:end -->'


def page_url(name):
    return BASE + '/' + (name[:-10] if name.endswith('index.html') else name)


def update():
    urls = []
    for path in sorted([*ROOT.glob('*.html'), *(ROOT / 'zh').glob('*.html')]):
        if path.name == 'highlight-template.html':
            continue
        name = path.relative_to(ROOT).as_posix()
        zh = name.startswith('zh/')
        source = path.read_text(encoding='utf-8')
        if path.name == 'index.html':
            title = '叶洋波 Yangbo Ye | 复旦大学 · 极端天气气候研究' if zh else 'Yangbo Ye (叶洋波) | Fudan University · Weather and Climate Extremes'
            description = ('叶洋波（Yangbo Ye）的个人学术主页。复旦大学大气与海洋科学系博士后，研究极端天气气候事件、事件归因、影响归因及空间复合型极端事件。'
                           if zh else 'Academic homepage of Yangbo Ye (叶洋波), a postdoctoral researcher at Fudan University studying weather and climate extremes, event attribution, impact attribution, and spatially compound events.')
            source, count = re.subn(r'<title>.*?</title>', '<title>' + escape(title) + '</title>', source, count=1, flags=re.S)
            assert count == 1
            source, count = re.subn(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + escape(description, quote=True) + '">', source, count=1)
            assert count == 1
        source = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', source, flags=re.S)
        source = re.sub(r'<link rel="alternate" hreflang="(?:en|zh-CN)" href="[^"]*">', '', source)
        canonical = page_url(name)
        meta = f'<link rel="canonical" href="{canonical}">\n'
        for lang, target in [('en', path.name), ('zh-CN', 'zh/' + path.name)]:
            meta += f'<link rel="alternate" hreflang="{lang}" href="{page_url(target)}">\n'
        if path.name == 'research.html':
            meta += '<meta name="robots" content="noindex,follow">\n'
        else:
            urls.append(canonical)
        if path.name == 'index.html':
            person = {'@type': 'Person', '@id': BASE + '/#yangbo-ye',
                      'name': '叶洋波' if zh else 'Yangbo Ye',
                      'alternateName': ['Yangbo Ye', 'Yang-Bo Ye'] if zh else ['叶洋波', 'Yang-Bo Ye'],
                      'url': BASE + '/', 'image': BASE + '/assets/yangbo-ye.jpg',
                      'jobTitle': '博士后' if zh else 'Postdoctoral Researcher',
                      'worksFor': {'@type': 'CollegeOrUniversity', 'name': '复旦大学' if zh else 'Fudan University'},
                      'sameAs': ['https://orcid.org/0009-0002-9135-1086',
                                 'https://scholar.google.com/citations?user=EZSfJd0AAAAJ',
                                 'https://www.researchgate.net/profile/Yangbo-Ye']}
            profile = {'@context': 'https://schema.org', '@type': 'ProfilePage', 'url': canonical,
                       'inLanguage': 'zh-CN' if zh else 'en', 'mainEntity': person}
            meta += '<script type="application/ld+json">' + json.dumps(profile, ensure_ascii=False) + '</script>\n'
        source = source.replace('</head>', START + '\n' + meta + END + '\n</head>', 1)
        path.write_text(source, encoding='utf-8')
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    sitemap = ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
    for url in urls:
        entry = ET.SubElement(sitemap, 'url')
        ET.SubElement(entry, 'loc').text = url
    ET.indent(sitemap, space='  ')
    ET.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + '/sitemap.xml\n', encoding='utf-8')
    print(f'Updated search metadata and sitemap: {len(urls)} indexable pages, {BASE}')


if __name__ == '__main__':
    update()
