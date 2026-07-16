from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

SKIP_TOP = {'📖 Table of Contents', 'Contributing', 'Credits', 'License'}
GUARDED_CATEGORIES = {
    'Data Breach Search Engines', 'Dark Web Search Engines', 'Pastebins',
    'Social Media Tools', 'Major Social Networks',
    'Real-Time Search, Social Media Search, and General Social Media Tools',
    'Username Check', 'People Investigations', 'Email Search / Email Check',
    'Phone Number Research', 'Vehicle / Automobile Research',
    'Domain and IP Research', 'Threat Intelligence', 'Threat Actor Search',
}
RESTRICTED_PATTERNS = [
    r'\bdox(?:bin|xing)?\b', r'password breach', r'credential',
    r'infostealer', r'stealer logs?', r'breach data', r'leak database',
    r'darknet-exposed', r'malware samples?', r'download confirmed malware',
    r'adult content', r'face search', r'facial recognition', r'face recognition', r'by face',
    r'search(?:ing)?.*people.*photo', r'people.*by photo', r'find.*by face',
    r'real[- ]time.*phone', r'live location',
]
CATEGORY_TAGS = {
    'General Search': ['search', 'discovery'], 'Google Dorks Tools': ['search-operators', 'query-building'],
    'Main National Search Engines': ['regional-search', 'search'], 'Meta Search': ['metasearch', 'search'],
    'Privacy Focused Search Engines': ['privacy', 'search'], 'Data Breach Search Engines': ['breach-exposure', 'defensive'],
    'Speciality Search Engines': ['specialized-search'], 'Dark Web Search Engines': ['dark-web', 'high-risk'],
    'Visual Search and Clustering Search Engines': ['visual-search', 'clustering'], 'Similar Sites Search': ['related-sites'],
    'Document and Slides Search': ['documents', 'pdf', 'slides'], 'Threat Actor Search': ['threat-actor', 'cti'],
    'Live Cyber Threat Maps': ['threat-map', 'cti'], 'File Search': ['file-search', 'open-directories'],
    'Pastebins': ['paste-sites', 'high-risk'], 'Code Search': ['code-search', 'repositories'],
    'Major Social Networks': ['social-media'], 'Real-Time Search, Social Media Search, and General Social Media Tools': ['social-media', 'realtime-search'],
    'Social Media Tools': ['social-media'], 'Blog Search': ['blogs', 'search'],
    'Forums and Discussion Boards Search': ['forums', 'communities'], 'Username Check': ['username', 'account-discovery'],
    'People Investigations': ['people', 'public-records', 'pii-sensitive'], 'Email Search / Email Check': ['email', 'pii-sensitive'],
    'Phone Number Research': ['phone', 'pii-sensitive'], 'Vehicle / Automobile Research': ['vehicle', 'public-records'],
    'Expert Search': ['experts', 'people'], 'Company Research': ['company', 'business'],
    'Job Search Resources': ['jobs', 'employment'], 'Q&A Sites': ['qa', 'communities'],
    'Domain and IP Research': ['domain', 'dns', 'ip', 'infrastructure'], 'Keywords Discovery and Research': ['keywords', 'search'],
    'Web History and Website Capture': ['web-archive', 'preservation'], 'Language Tools': ['translation', 'language'],
    'Image Search': ['image', 'reverse-image'], 'Image Analysis': ['image', 'metadata', 'forensics'],
    'Video Search and Other Video Tools': ['video', 'verification'], 'Academic Resources and Grey Literature': ['academic', 'grey-literature'],
    'Geospatial Research and Mapping Tools': ['geospatial', 'maps', 'geolocation'], 'News': ['news', 'media'],
    'News Digest and Discovery Tools': ['news', 'discovery'], 'Fact Checking': ['fact-checking', 'verification'],
    'Data and Statistics': ['data', 'statistics'], 'Web Monitoring': ['monitoring', 'alerts'],
    'Browsers': ['browser', 'opsec'], 'Offline Browsing': ['archiving', 'offline'],
    'VPN Services': ['privacy', 'network'], 'Infographics and Data Visualization': ['visualization', 'reporting'],
    'Social Network Analysis': ['network-analysis', 'graph'], 'Privacy and Encryption Tools': ['privacy', 'encryption', 'opsec'],
    'DNS': ['dns', 'infrastructure'], 'Maritime': ['maritime', 'geospatial'], 'Other Tools': ['misc'],
    'Threat Intelligence': ['cti', 'ioc'], 'Gaming Platforms': ['gaming', 'social-media'],
    'Music Streaming Services': ['music', 'social-media'], 'OSINT Videos': ['training', 'video'],
    'OSINT Blogs': ['training', 'blogs'], 'OSINT RSS Feeds': ['training', 'rss'],
    'Other Resources': ['training', 'resources'], 'Related Awesome Lists': ['resources', 'catalogs'],
}
KEYWORD_TAGS = [
    ('api', r'\bapi\b'), ('cli', r'\bcli\b|command[- ]line'), ('open-source', r'open[- ]source|github\.com|gitlab\.com'),
    ('free', r'\bfree\b|no[- ]signup|no registration|without registration'), ('paid', r'\bpaid\b|premium|subscription|credits?'),
    ('registration', r'registration required|account required|sign[- ]?up'), ('whois', r'\bwhois\b|\brdap\b'),
    ('certificate', r'certificate transparency|ssl|tls|crt\.sh'), ('asn-bgp', r'\basn\b|\bbgp\b'),
    ('exif', r'\bexif\b|metadata'), ('archive', r'archive|wayback|historical'),
    ('reverse-search', r'reverse image|reverse search'), ('malware', r'\bmalware\b|yara'),
    ('cve', r'\bcve\b|vulnerabilit'), ('ioc', r'\bioc\b|indicator of compromise'),
    ('rss', r'\brss\b|feed'), ('mapping', r'\bmap\b|mapping|geograph|satellite'),
]

CHINESE_EXPANSIONS = {
    '域名': 'domain dns whois rdap certificate ip infrastructure',
    '网站': 'website domain web archive search', '证书': 'certificate ssl tls transparency',
    '历史': 'history archive wayback historical', '用户名': 'username nickname handle social account',
    '账号': 'account username social profile', '社交': 'social media network profile',
    '人物': 'people public records biography', '邮箱': 'email mail breach validation',
    '邮件': 'email mail', '电话': 'phone number', '手机': 'phone mobile number',
    '公司': 'company business registry corporate', '企业': 'company business registry corporate',
    '图片': 'image reverse image metadata exif', '照片': 'image photo reverse metadata exif',
    '视频': 'video keyframe verification', '地理': 'geospatial map geolocation location',
    '定位': 'geolocation location map', '地图': 'map geospatial satellite',
    '新闻': 'news media', '核查': 'fact checking verification', '事实': 'fact checking verification',
    '威胁': 'threat intelligence cti ioc', '漏洞': 'cve vulnerability threat',
    '恶意软件': 'malware threat intelligence', '文档': 'document pdf slides',
    '监控': 'monitoring alerts rss change detection', '代码': 'code search repository github',
}

def clean_heading(raw: str) -> str:
    return re.sub(r'^\[↑\]\([^)]*\)\s*', '', raw).strip()

def parse_readme(text: str, generated_at: str, source_url: str, repository: str, license_name: str = 'CC BY-SA 4.0') -> dict:
    items, current = [], []
    for line_no, line in enumerate(text.splitlines(), 1):
        hm = re.match(r'^(#{2,4})\s+(.+?)\s*$', line)
        if hm:
            level, title = len(hm.group(1)), clean_heading(hm.group(2))
            if level == 2: current = [title]
            elif level == 3: current = current[:1] + [title]
            elif level == 4: current = current[:2] + [title]
            continue
        m = re.match(r'^\s*[*-]\s+\[([^\]]+)\]\(([^)]+)\)(?:\s*-\s*(.*))?\s*$', line)
        vals = None
        if m:
            vals = m.groups()
        else:
            mm = re.match(r'^\s*[*-]\s+\[([^\]]+)\]\s+(https?://\S+)(?:\s+-\s+(.*))?\s*$', line)
            if mm: vals = mm.groups()
        if not vals or not current or current[0] in SKIP_TOP:
            continue
        name, url, desc = vals[0].strip(), vals[1].strip(), (vals[2] or '').strip()
        url = re.sub(r'\s+[\"\'].*$', '', url).strip()
        top, sub = current[0], current[1] if len(current) > 1 else ''
        searchable = f'{name} {desc} {top} {sub} {url}'.lower()
        flags = {
            'pii_sensitive': top in {'People Investigations', 'Email Search / Email Check', 'Phone Number Research', 'Username Check'} or bool(re.search(r'people|email|phone|username|face', searchable)),
            'breach_or_credentials': bool(re.search(r'breach|credential|password|leak|infostealer|stealer log', searchable)),
            'dark_web': top == 'Dark Web Search Engines' or bool(re.search(r'dark web|darknet|\.onion|tor hidden', searchable)),
            'malware': bool(re.search(r'malware|yara|virus|ransomware', searchable)),
            'biometric': bool(re.search(r'face search|facial|reverse face|search.*face', searchable)),
        }
        reasons = [pat for pat in RESTRICTED_PATTERNS if re.search(pat, searchable)]
        risk = 'restricted' if reasons else ('guarded' if top in GUARDED_CATEGORIES or any(flags.values()) else 'low')
        tags = list(CATEGORY_TAGS.get(top, []))
        if sub: tags.append(re.sub(r'[^a-z0-9]+', '-', sub.lower()).strip('-'))
        for tag, pat in KEYWORD_TAGS:
            if re.search(pat, searchable): tags.append(tag)
        tags = sorted(set(filter(None, tags)))
        parsed = urlparse(url if '://' in url else 'https://' + url.lstrip('/'))
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-') or 'tool'
        item_id = f"{slug[:60]}-{hashlib.sha1(f'{name}|{url}|{top}|{sub}'.encode()).hexdigest()[:8]}"
        items.append({
            'id': item_id, 'name': name, 'url': url, 'domain': parsed.netloc.lower().removeprefix('www.'),
            'category': top, 'subcategory': sub, 'description': desc, 'tags': tags, 'risk_tier': risk,
            'risk_flags': flags, 'risk_reasons': reasons,
            'signals': {'open_source': 'open-source' in tags, 'free_signal': 'free' in tags, 'paid_signal': 'paid' in tags,
                        'registration_signal': 'registration' in tags, 'api_signal': 'api' in tags, 'cli_signal': 'cli' in tags},
            'source_line': line_no,
        })
    seen, deduped = set(), []
    for item in items:
        key = (item['name'].casefold(), item['url'].casefold(), item['category'], item['subcategory'])
        if key not in seen:
            seen.add(key); deduped.append(item)
    items = deduped
    from collections import Counter
    cc, rc = Counter(i['category'] for i in items), Counter(i['risk_tier'] for i in items)
    order = []
    for i in items:
        if i['category'] not in order: order.append(i['category'])
    return {
        'schema_version': '1.0.0', 'generated_at': generated_at,
        'source': {'name': 'jivoi/awesome-osint', 'repository': repository, 'readme': source_url,
                   'license': license_name, 'retrieved_at': generated_at,
                   'snapshot_sha256': hashlib.sha256(text.encode()).hexdigest()},
        'stats': {'tools': len(items), 'categories': len(cc), 'risk_tiers': dict(sorted(rc.items()))},
        'categories': [{'name': c, 'count': cc[c], 'default_risk': 'guarded' if c in GUARDED_CATEGORIES else 'low'} for c in order],
        'tools': items,
    }

def load_catalog(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))

def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text.casefold())
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r'[^a-z0-9\u4e00-\u9fff]+', ' ', text).strip()

def expand_query(query: str) -> str:
    extra = [v for k, v in CHINESE_EXPANSIONS.items() if k in query]
    return query + (' ' + ' '.join(extra) if extra else '')

def score_tool(tool: dict, query: str) -> float:
    q = normalize(expand_query(query))
    tokens = [t for t in q.split() if len(t) > 1]
    if not tokens: return 0.0
    fields = {
        'name': normalize(tool.get('name', '')),
        'category': normalize(tool.get('category', '') + ' ' + tool.get('subcategory', '')),
        'description': normalize(tool.get('description', '')),
        'tags': normalize(' '.join(tool.get('tags', []))),
        'domain': normalize(tool.get('domain', '')),
    }
    weights = {'name': 8, 'category': 6, 'description': 3, 'tags': 4, 'domain': 2}
    score = 0.0
    for token in tokens:
        for field, text in fields.items():
            if token in text:
                score += weights[field]
                if text.startswith(token): score += 0.5
    phrase = normalize(query)
    if phrase and phrase in fields['name']: score += 12
    if phrase and phrase in fields['description']: score += 5
    if tool.get('risk_tier') == 'low': score += 0.4
    return score
