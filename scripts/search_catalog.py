#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from cataloglib import load_catalog, score_tool

RISK_ORDER = {'low': 0, 'guarded': 1, 'restricted': 2}


def clip(text: str, width: int = 88) -> str:
    text = ' '.join(text.split())
    return text if len(text) <= width else text[:width - 1] + '…'


def main() -> int:
    ap = argparse.ArgumentParser(description='Search the structured Awesome OSINT catalog.')
    ap.add_argument('query')
    ap.add_argument('--catalog', default=str(Path(__file__).resolve().parents[1] / 'references' / 'catalog.json'))
    ap.add_argument('--top', type=int, default=10)
    ap.add_argument('--category', action='append', help='Exact category filter; repeatable')
    ap.add_argument('--max-risk', choices=['low', 'guarded', 'restricted'], default='guarded')
    ap.add_argument('--include-restricted', action='store_true', help='Equivalent to --max-risk restricted; use only for authorized defensive triage')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    max_risk = 'restricted' if args.include_restricted else args.max_risk
    catalog = load_catalog(args.catalog)
    rows = []
    for tool in catalog['tools']:
        if RISK_ORDER[tool['risk_tier']] > RISK_ORDER[max_risk]: continue
        if args.category and tool['category'] not in args.category: continue
        score = score_tool(tool, args.query)
        if score > 0: rows.append((score, tool))
    rows.sort(key=lambda x: (-x[0], x[1]['risk_tier'], x[1]['name'].casefold()))
    rows = rows[:max(1, args.top)]

    if args.json:
        print(json.dumps([{'score': round(s, 2), **t} for s, t in rows], ensure_ascii=False, indent=2))
        return 0
    if not rows:
        print('No matching tools. Try broader terms or a category filter.')
        return 1
    print(f"{'SCORE':>5}  {'RISK':<10} {'NAME':<30} {'CATEGORY':<28} DESCRIPTION")
    print('-' * 118)
    for score, t in rows:
        print(f"{score:5.1f}  {t['risk_tier']:<10} {clip(t['name'], 30):<30} {clip(t['category'], 28):<28} {clip(t['description'])}")
        print(f"       {t['url']}")
    print('\nCatalog entries are leads. Verify current availability, terms, and facts independently.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
