#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ['finding_id', 'claim', 'label', 'confidence', 'source_url', 'source_title', 'publisher', 'source_type',
          'published_at', 'accessed_at', 'supporting_note', 'independence_note', 'contradictions', 'file_sha256', 'analyst_notes']


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


def init(path: Path, force: bool) -> None:
    if path.exists() and not force: raise FileExistsError(f'{path} already exists; use --force to overwrite')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f: csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def add(path: Path, args) -> None:
    if not path.exists(): init(path, False)
    row = {field: '' for field in FIELDS}
    row.update({
        'finding_id': args.finding_id, 'claim': args.claim, 'label': args.label, 'confidence': args.confidence,
        'source_url': args.source_url, 'source_title': args.source_title, 'publisher': args.publisher,
        'source_type': args.source_type, 'published_at': args.published_at,
        'accessed_at': args.accessed_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'supporting_note': args.supporting_note, 'independence_note': args.independence_note,
        'contradictions': args.contradictions, 'analyst_notes': args.notes,
        'file_sha256': sha256_file(args.file) if args.file else '',
    })
    with path.open('a', encoding='utf-8', newline='') as f: csv.DictWriter(f, fieldnames=FIELDS).writerow(row)


def summary(path: Path) -> None:
    with path.open(encoding='utf-8', newline='') as f: rows = list(csv.DictReader(f))
    from collections import Counter
    print(f'Rows: {len(rows)}')
    print('Confidence:', dict(Counter(r['confidence'] or 'unset' for r in rows)))
    print('Labels:', dict(Counter(r['label'] or 'unset' for r in rows)))
    missing = sum(not r['source_url'] and not r['file_sha256'] for r in rows)
    print(f'Rows without URL or file hash: {missing}')


def main() -> int:
    ap = argparse.ArgumentParser(description='Create and maintain a CSV evidence ledger.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('init'); p.add_argument('path'); p.add_argument('--force', action='store_true')
    p = sub.add_parser('add'); p.add_argument('path'); p.add_argument('--finding-id', default='')
    p.add_argument('--claim', required=True); p.add_argument('--label', default='single-source lead')
    p.add_argument('--confidence', choices=['high', 'medium', 'low', ''], default='low')
    p.add_argument('--source-url', default=''); p.add_argument('--source-title', default=''); p.add_argument('--publisher', default='')
    p.add_argument('--source-type', choices=['primary-authoritative', 'primary', 'secondary-high-quality', 'secondary-aggregate', 'community', ''], default='')
    p.add_argument('--published-at', default=''); p.add_argument('--accessed-at', default='')
    p.add_argument('--supporting-note', default=''); p.add_argument('--independence-note', default='')
    p.add_argument('--contradictions', default=''); p.add_argument('--notes', default=''); p.add_argument('--file')
    p = sub.add_parser('summary'); p.add_argument('path')
    args = ap.parse_args(); path = Path(args.path)
    try:
        if args.cmd == 'init': init(path, args.force)
        elif args.cmd == 'add': add(path, args)
        else: summary(path)
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}'); return 1

if __name__ == '__main__':
    raise SystemExit(main())
