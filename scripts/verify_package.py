#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import py_compile
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$")


def verify_versions(errors: list[str]) -> None:
    version_file = ROOT / 'VERSION'
    if not version_file.exists():
        errors.append('VERSION missing')
        return

    version = version_file.read_text(encoding='utf-8').strip()
    if not SEMVER_RE.fullmatch(version):
        errors.append(f'VERSION is not valid SemVer: {version!r}')
        return

    try:
        metadata = json.loads((ROOT / 'skill.json').read_text(encoding='utf-8'))
        metadata_version = str(metadata.get('version', '')).strip()
        if metadata_version != version:
            errors.append(f'skill.json version mismatch: {metadata_version!r} != {version!r}')
    except Exception as exc:
        errors.append(f'skill.json version check failed: {exc}')

    try:
        skill_text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        match = re.search(r'(?m)^version:\s*([^\s]+)\s*$', skill_text)
        skill_version = match.group(1) if match else None
        if skill_version != version:
            errors.append(f'SKILL.md version mismatch: {skill_version!r} != {version!r}')
    except Exception as exc:
        errors.append(f'SKILL.md version check failed: {exc}')

    try:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        expected = f'Release: `v{version}`'
        if expected not in readme:
            errors.append(f'README.md release marker mismatch: expected {expected!r}')
    except Exception as exc:
        errors.append(f'README.md version check failed: {exc}')

    try:
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        if f'## {version}' not in changelog:
            errors.append(f'CHANGELOG.md missing release heading: ## {version}')
    except Exception as exc:
        errors.append(f'CHANGELOG.md version check failed: {exc}')


def verify_wanted_person_mode(errors: list[str]) -> None:
    """Prevent the guarded wanted-person workflow from drifting out of core routing."""
    workflow_rel = 'workflows/wanted-person-location-intelligence.md'
    workflow = ROOT / workflow_rel
    if not workflow.exists():
        errors.append(f'wanted-person workflow missing: {workflow_rel}')
        return

    try:
        manifest_entries = {
            rel.strip()
            for rel in (ROOT / 'manifest.txt').read_text(encoding='utf-8').splitlines()
            if rel.strip()
        }
        if workflow_rel not in manifest_entries:
            errors.append(f'manifest.txt missing wanted-person workflow: {workflow_rel}')
    except Exception as exc:
        errors.append(f'wanted-person manifest check failed: {exc}')

    try:
        skill_text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        if workflow_rel not in skill_text:
            errors.append('SKILL.md does not route to the wanted-person workflow')
        if 'active official wanted/fugitive' not in skill_text:
            errors.append('SKILL.md missing official wanted/fugitive activation language')
    except Exception as exc:
        errors.append(f'wanted-person SKILL.md check failed: {exc}')

    try:
        metadata = json.loads((ROOT / 'skill.json').read_text(encoding='utf-8'))
        capabilities = set(metadata.get('capabilities', []))
        required = {
            'official-wanted-person-status-gating',
            'official-wanted-person-location-intelligence',
            'freshness-labelled-location-inference',
        }
        missing = sorted(required - capabilities)
        if missing:
            errors.append(f'skill.json missing wanted-person capabilities: {missing}')
    except Exception as exc:
        errors.append(f'wanted-person skill.json check failed: {exc}')

    try:
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        if 'guarded official wanted/fugitive-person location intelligence' not in readme:
            errors.append('README.md missing wanted/fugitive capability declaration')
    except Exception as exc:
        errors.append(f'wanted-person README check failed: {exc}')

    try:
        safety = (ROOT / 'references/safety-policy.md').read_text(encoding='utf-8')
        if 'Official wanted/fugitive-person exception' not in safety:
            errors.append('safety-policy.md missing wanted/fugitive exception gate')
    except Exception as exc:
        errors.append(f'wanted-person safety-policy check failed: {exc}')

    try:
        people = (ROOT / 'workflows/people-public-interest.md').read_text(encoding='utf-8')
        if workflow_rel.split('/', 1)[1] not in people:
            errors.append('people-public-interest.md does not hand off verified wanted cases')
    except Exception as exc:
        errors.append(f'wanted-person people workflow check failed: {exc}')


def main() -> int:
    errors: list[str] = []
    manifest = ROOT / 'manifest.txt'
    if not manifest.exists():
        errors.append('manifest.txt missing')
    else:
        entries = [rel.strip() for rel in manifest.read_text(encoding='utf-8').splitlines() if rel.strip()]
        if len(entries) != len(set(entries)):
            errors.append('manifest.txt contains duplicate entries')
        for rel in entries:
            if not (ROOT / rel).exists():
                errors.append(f'manifest entry missing: {rel}')

    skill = ROOT / 'SKILL.md'
    if not skill.exists() or not skill.read_text(encoding='utf-8').startswith('---\n'):
        errors.append('SKILL.md frontmatter missing')

    verify_versions(errors)
    verify_wanted_person_mode(errors)

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
    print('OK — package structure, versions, wanted-person routing, catalog, snapshot hash, attribution, URLs, and Python scripts verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
