"""Check bilingual navigation, articles, language pairs and local resources."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent
NAV = ('index.html', 'highlights.html', 'publications.html', 'cv.html', 'contact.html')
ARTICLES = ('meiyu-2020.html', 'southwest-rainfall-2020.html', 'compound-2020.html', 'north-china-heat-2023.html', 'cold-2023.html', 'school-heat-2024.html')
FILES = (*NAV, 'research.html', 'highlight-template.html', *ARTICLES)
PAGES = (*FILES, *(f'zh/{name}' for name in FILES))


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.current, self.nav = [], set(), [], []
        self.in_nav = False
        self.headings = 0
        self.language = None
        self.switches = []
        self.alternates = {}
        self.cards = []
        self.card = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article' and 'highlight-card' in attrs.get('class', '').split():
            self.card = {'links': [], 'images': [], 'tone': attrs.get('data-tone')}
            self.cards.append(self.card)
        if self.card is not None:
            if tag == 'a':
                self.card['links'].append(attrs.get('href'))
            if tag == 'img':
                self.card['images'].append(attrs)
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'a' and 'language-switch' in attrs.get('class', '').split():
            self.switches.append(attrs.get('href'))
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs.get('hreflang')] = attrs.get('href')
        if tag == 'nav':
            self.in_nav = True
        if tag == 'h1':
            self.headings += 1
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, 'Duplicate id'
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'a' and self.in_nav:
            self.nav.append(attrs.get('href'))
        if attrs.get('aria-current') == 'page':
            self.current.append(attrs.get('href'))

    def handle_endtag(self, tag):
        if tag == 'article':
            self.card = None
        if tag == 'nav':
            self.in_nav = False


pages = {name: Page((ROOT / name).read_text(encoding='utf-8')) for name in PAGES}
for name, page in pages.items():
    chinese = name.startswith('zh/')
    basename = Path(name).name
    assert page.headings == 1, (name, 'Expected one main heading')
    expected_current = [] if basename == 'research.html' else [basename if basename in NAV else 'highlights.html']
    assert page.current == expected_current, (name, 'Wrong active page')
    assert page.nav == list(NAV), (name, 'Navigation must link to all main pages')
    assert page.language == ('zh-CN' if chinese else 'en'), (name, 'Wrong document language')
    counterpart = ('../' if chinese else 'zh/') + basename
    assert page.switches == [counterpart], (name, 'Language switch must retain current page')
    assert page.alternates == {'en': ('../' if chinese else '') + basename, 'zh-CN': ('' if chinese else 'zh/') + basename}, (name, 'Wrong language metadata')
    for link in page.links:
        assert link and link != '#', (name, 'Empty link')
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        target_path = ((ROOT / name).parent / unquote(url.path)).resolve() if url.path else (ROOT / name)
        target = target_path.relative_to(ROOT).as_posix()
        assert target_path.is_file(), (name, 'Missing file', target)
        if url.fragment:
            assert target in pages and unquote(url.fragment) in pages[target].ids, (name, 'Missing anchor', link)
for prefix in ('', 'zh/'):
    assert 'highlights.html' in pages[prefix + 'index.html'].links
    assert 'highlights.html' in pages[prefix + 'highlight-template.html'].links
    for article in ARTICLES:
        assert article in pages[prefix + 'highlights.html'].links
        assert 'highlights.html' in pages[prefix + article].links
    for name, expected in [('index.html', list(reversed(ARTICLES))[:4]), ('highlights.html', list(reversed(ARTICLES)))]:
        cards = pages[prefix + name].cards
        assert len(cards) == len(expected), (prefix + name, 'Wrong number of highlight cards')
        for card, article in zip(cards, expected):
            assert card['links'] == [article] * 3, (prefix + name, 'Wrong article order or card link')
            assert card['tone'] == str(ARTICLES.index(article) % 5 + 1), 'Wrong blue palette cycle'
            assert len(card['images']) == 1 and card['images'][0].get('alt'), 'Missing representative image'
            assert all(card['images'][0].get(attr) for attr in ('width', 'height')), 'Missing image dimensions'
    assert 'meiyu-2020.html' in pages[prefix + 'southwest-rainfall-2020.html'].links
    assert all(article in pages[prefix + 'compound-2020.html'].links for article in ARTICLES[:2])
print(f'PASS: {len(pages)} pages, bilingual navigation, language pairs, article paths, assets and anchors.')
