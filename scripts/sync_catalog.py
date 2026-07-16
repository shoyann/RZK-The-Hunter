#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

from cataloglib import parse_readme

DEFAULT_URL = 'https://raw.githubusercontent.com/jivoi/awesome-osint/master/README.md'
DEFAULT_REPO = 'https://github.com/jivoi/awesome-osint'


def fetch(url: str, timeout: int) -> str:
    req = Request(url, headers={'User-Agent': 'awesome-osint-operator/1.0'})
    with urlopen(req, timeout=timeout) as response:
        content_type = response.headers.get('Content-Type', '')
        if 'text' not in content_type and 'markdown' not in content_type and 'octet-stream' not in content_type:
            raise RuntimeError(f'Unexpected content type: {content_type}')
        data = response.read(5_000_000)
    return data.decode('utf-8')


def write_csv(catalog: dict, path: Path) -> None:
    fields = ['id', 'name', 'url', 'domain', 'category', 'subcategory', 'description', 'tags', 'risk_tier',
              'pii_sensitive', 'breach_or_credentials', 'dark_web', 'malware', 'biometric', 'source_line']
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i in catalog['tools']:
            w.writerow({'id': i['id'], 'name': i['name'], 'url': i['url'], 'domain': i['domain'],
                        'category': i['category'], 'subcategory': i['subcategory'], 'description': i['description'],
                        'tags': '|'.join(i['tags']), 'risk_tier': i['risk_tier'], **i['risk_flags'],
                        'source_line': i['source_line']})


def write_taxonomy(catalog: dict, path: Path) -> None:
    counts = Counter(t['category'] for t in catalog['tools'])
    order = []
    for tool in catalog['tools']:
        if tool['category'] not in order:
            order.append(tool['category'])
    guarded = {c['name'] for c in catalog['categories'] if c['default_risk'] == 'guarded'}
    lines = [
        '# Catalog Taxonomy', '',
        f"- Source tools: **{catalog['stats']['tools']:,}**",
        f"- Categories: **{catalog['stats']['categories']}**",
        f"- Risk tiers: `{catalog['stats']['risk_tiers']}`", '',
        '| Category | Tools | Default handling |', '|---|---:|---|',
    ]
    for category in order:
        safe = category.replace('|', '\\|')
        lines.append(f"| {safe} | {counts[category]} | {'Guarded' if category in guarded else 'Standard'} |")
    lines += ['', 'Risk tiers are heuristic triage metadata, not legal judgments. Review `safety-policy.md` before use.']
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def update_attribution(package_root: Path, generated: str, digest: str) -> None:
    path = package_root / 'ATTRIBUTION.md'
    if path.exists():
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'(?m)^- Snapshot retrieved: .*$', f'- Snapshot retrieved: {generated}', text)
        text = re.sub(r'(?m)^- Snapshot SHA-256: `[^`]+`$', f'- Snapshot SHA-256: `{digest}`', text)
        path.write_text(text, encoding='utf-8')

    readme = package_root / 'README.md'
    if readme.exists():
        text = readme.read_text(encoding='utf-8')
        text = re.sub(r'快照获取时间：`[^`]+`，SHA-256：`[^`]+`。',
                      f'快照获取时间：`{generated}`，SHA-256：`{digest}`。', text)
        readme.write_text(text, encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser(description='Refresh and parse the upstream Awesome OSINT README.')
    ap.add_argument('--url', default=DEFAULT_URL)
    ap.add_argument('--from-file', help='Use a local README instead of downloading')
    ap.add_argument('--output-dir', default=str(Path(__file__).resolve().parents[1] / 'references'))
    ap.add_argument('--timeout', type=int, default=30)
    ap.add_argument('--no-attribution-update', action='store_true')
    args = ap.parse_args()

    try:
        text = Path(args.from_file).read_text(encoding='utf-8') if args.from_file else fetch(args.url, args.timeout)
        generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        catalog = parse_readme(text, generated, args.url, DEFAULT_REPO)
        out = Path(args.output_dir)
        (out / 'source').mkdir(parents=True, exist_ok=True)
        (out / 'source' / 'awesome-osint-README.md').write_text(text, encoding='utf-8')
        (out / 'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        write_csv(catalog, out / 'catalog.csv')
        write_taxonomy(catalog, out / 'taxonomy.md')
        if not args.no_attribution_update:
            update_attribution(out.parent, generated, catalog['source']['snapshot_sha256'])
        print(f"Updated {catalog['stats']['tools']} tools across {catalog['stats']['categories']} categories.")
        print(f"Risk tiers: {catalog['stats']['risk_tiers']}")
        print(f"Snapshot SHA-256: {catalog['source']['snapshot_sha256']}")
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
