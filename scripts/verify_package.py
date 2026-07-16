#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors = []
    manifest = ROOT / 'manifest.txt'
    if not manifest.exists():
        errors.append('manifest.txt missing')
    else:
        for rel in manifest.read_text(encoding='utf-8').splitlines():
            if rel.strip() and not (ROOT / rel).exists():
                errors.append(f'manifest entry missing: {rel}')

    skill = ROOT / 'SKILL.md'
    if not skill.exists() or not skill.read_text(encoding='utf-8').startswith('---\n'):
        errors.append('SKILL.md frontmatter missing')

    try:
        catalog = json.loads((ROOT / 'references/catalog.json').read_text(encoding='utf-8'))
        if catalog['stats']['tools'] < 1000:
            errors.append('catalog unexpectedly small')
        ids = [t['id'] for t in catalog['tools']]
        if len(ids) != len(set(ids)):
            errors.append('duplicate tool IDs')
        if any(' ' in t['url'] for t in catalog['tools']):
            errors.append('catalog contains URL with spaces')
        source = (ROOT / 'references/source/awesome-osint-README.md').read_bytes()
        actual = hashlib.sha256(source).hexdigest()
        expected = catalog['source']['snapshot_sha256']
        if actual != expected:
            errors.append('source snapshot hash mismatch')
        attribution = (ROOT / 'ATTRIBUTION.md').read_text(encoding='utf-8')
        if expected not in attribution:
            errors.append('ATTRIBUTION.md snapshot hash is stale')
    except Exception as exc:
        errors.append(f'catalog error: {exc}')

    for script in (ROOT / 'scripts').glob('*.py'):
        try:
            py_compile.compile(str(script), doraise=True)
        except Exception as exc:
            errors.append(f'{script.name}: {exc}')

    if errors:
        print('FAILED')
        for error in errors:
            print('-', error)
        return 1
    print('OK — package structure, catalog, snapshot hash, attribution, URLs, and Python scripts verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
