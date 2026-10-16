#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

FIELDS = ['finding_id', 'claim', 'label', 'confidence', 'source_url', 'source_title', 'publisher', 'source_type',
          'published_at', 'accessed_at', 'supporting_note', 'independence_note', 'contradictions', 'file_sha256', 'analyst_notes']
CONFIDENCES = ['high', 'medium', 'low', '']
SOURCE_TYPES = ['primary-authoritative', 'primary', 'secondary-high-quality', 'secondary-aggregate', 'community', '']
DEFAULTS = {
    'finding_id': '', 'label': 'single-source lead', 'confidence': 'low',
    'source_url': '', 'source_title': '', 'publisher': '', 'source_type': '',
    'published_at': '', 'accessed_at': '', 'supporting_note': '',
    'independence_note': '', 'contradictions': '', 'notes': '', 'file': None,
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()


@contextmanager
def ledger_lock(path: Path):
    """Fail fast if another cooperating writer owns this ledger's sidecar lock."""
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f'{path.name}.lock')
    owner = f'{os.getpid()} {uuid.uuid4().hex}\n'
    try:
        handle = lock_path.open('x', encoding='ascii')
    except FileExistsError as exc:
        raise RuntimeError(
            f'Ledger is locked: {lock_path}. Another writer may be active. '
            'If a writer crashed, remove this lock only after confirming no writer is active.'
        ) from exc
    identity = os.fstat(handle.fileno())
    try:
        with handle:
            handle.write(owner)
            handle.flush()
        yield path
    finally:
        # A conflicting caller never enters this block. Do not remove a lock
        # recreated by someone else after this process's lock was removed.
        try:
            current = lock_path.lstat()
            if ((current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino)
                    and lock_path.read_text(encoding='ascii') == owner):
                lock_path.unlink()
        except FileNotFoundError:
            pass


def _init_unlocked(path: Path, force: bool) -> None:
    if path.exists() and not force: raise FileExistsError(f'{path} already exists; use --force to overwrite')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f: csv.DictWriter(f, fieldnames=FIELDS).writeheader()


def init(path: Path, force: bool) -> None:
    with ledger_lock(path) as locked_path:
        _init_unlocked(locked_path, force)


def prepare_row(values: dict) -> dict:
    """Apply the same fields, defaults and choice validation to both add modes."""
    if not isinstance(values, dict):
        raise ValueError('each finding must be a JSON object')
    unknown = values.keys() - DEFAULTS.keys() - {'claim'}
    if unknown:
        raise ValueError(f'unknown fields: {", ".join(sorted(unknown))}')
    if 'claim' not in values:
        raise ValueError('claim is required')
    data = DEFAULTS | values
    for field, value in data.items():
        if field == 'file' and value is None:
            continue
        if not isinstance(value, str):
            raise ValueError(f'{field} must be a string')
    if data['confidence'] not in CONFIDENCES:
        raise ValueError(f'confidence must be one of {CONFIDENCES}')
    if data['source_type'] not in SOURCE_TYPES:
        raise ValueError(f'source_type must be one of {SOURCE_TYPES}')
    row = {field: '' for field in FIELDS}
    row.update({
        **{field: data[field] for field in FIELDS if field in data},
        'accessed_at': data['accessed_at'] or datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        'analyst_notes': data['notes'],
        'file_sha256': sha256_file(data['file']) if data['file'] else '',
    })
    return row


def add(path: Path, args) -> None:
    row = prepare_row({field: getattr(args, field) for field in (*DEFAULTS, 'claim')})
    with ledger_lock(path) as locked_path:
        if not locked_path.exists(): _init_unlocked(locked_path, False)
        with locked_path.open('a', encoding='utf-8', newline='') as f:
            csv.DictWriter(f, fieldnames=FIELDS).writerow(row)


def read_batch(handle) -> list[dict]:
    rows = []
    for line_number, line in enumerate(handle, start=1):
        if not line.strip():
            continue
        try:
            rows.append(prepare_row(json.loads(line)))
        except (ValueError, TypeError, OSError) as exc:
            raise ValueError(f'line {line_number}: {exc}') from exc
    return rows


def append_batch(path: Path, rows: list[dict]) -> None:
    """Commit a fully validated batch in one replacement, preserving existing rows."""
    if not rows:
        return
    with ledger_lock(path) as locked_path:
        _append_batch_unlocked(locked_path, rows)


def _append_batch_unlocked(path: Path, rows: list[dict]) -> None:
    existing = path.read_bytes() if path.exists() else b''
    if path.exists():
        reader = csv.reader(io.StringIO(existing.decode('utf-8-sig'), newline=''))
        if next(reader, None) != FIELDS:
            raise ValueError('existing ledger has an unexpected CSV header')
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=FIELDS)
    if not existing:
        writer.writeheader()
    writer.writerows(rows)
    if existing and not existing.endswith((b'\n', b'\r')):
        existing += b'\r\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f'.{path.name}.', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(existing)
            handle.write(buffer.getvalue().encode('utf-8'))
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            temporary.chmod(stat.S_IMODE(path.stat().st_mode))
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def add_batch(path: Path, input_path: str) -> int:
    if input_path == '-':
        rows = read_batch(sys.stdin)
    else:
        with Path(input_path).open(encoding='utf-8-sig') as handle:
            rows = read_batch(handle)
    append_batch(path, rows)
    return len(rows)


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
    p.add_argument('--confidence', choices=CONFIDENCES, default='low')
    p.add_argument('--source-url', default=''); p.add_argument('--source-title', default=''); p.add_argument('--publisher', default='')
    p.add_argument('--source-type', choices=SOURCE_TYPES, default='')
    p.add_argument('--published-at', default=''); p.add_argument('--accessed-at', default='')
    p.add_argument('--supporting-note', default=''); p.add_argument('--independence-note', default='')
    p.add_argument('--contradictions', default=''); p.add_argument('--notes', default=''); p.add_argument('--file')
    p = sub.add_parser('add-batch', help='append JSONL findings after validating the entire batch')
    p.add_argument('path')
    p.add_argument('--input', required=True,
                   help='JSONL file or - for stdin; keys match add options with underscores (e.g. finding_id, notes, file)')
    p = sub.add_parser('summary'); p.add_argument('path')
    args = ap.parse_args(); path = Path(args.path)
    try:
        if args.cmd == 'init': init(path, args.force)
        elif args.cmd == 'add': add(path, args)
        elif args.cmd == 'add-batch': print(f'Added {add_batch(path, args.input)} findings.')
        else: summary(path)
        return 0
    except Exception as exc:
        print(f'ERROR: {exc}'); return 1

if __name__ == '__main__':
    raise SystemExit(main())
