#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from cataloglib import (add_json_arguments, load_catalog, positive_int, project_tool,
                        score_tool, validate_json_arguments)

# Each stage is: title, search query, allowed categories, preferred catalog names.
# Preferred names are anchors, not endorsements. They still require current verification.
PROFILES = {
    'domain': [
        ('Identity and registration', 'RDAP WHOIS domain registration registrar',
         ['Domain and IP Research', 'DNS'], ['Icann Lookup', 'Whois Arin Online', 'digga']),
        ('DNS and certificates', 'DNS certificate transparency subdomain SSL TLS',
         ['Domain and IP Research', 'DNS', 'Speciality Search Engines'], ['CRT Certificate Search', 'DNSDumpster', 'DNSViz']),
        ('Infrastructure', 'IP ASN BGP hosting internet asset',
         ['Domain and IP Research', 'Speciality Search Engines'], ['BGP.tools', 'BGP.he.net', 'Censys', 'Shodan']),
        ('History', 'Wayback archive website history capture',
         ['Web History and Website Capture'], ['Wayback Machine', 'Archive.is']),
        ('Reputation', 'domain reputation phishing abuse threat intelligence',
         ['Domain and IP Research', 'Threat Intelligence', 'Speciality Search Engines'], ['Cisco Talos Intelligence', 'Abuseipdb', 'OTX AlienVault']),
    ],
    'company': [
        ('Official identity', 'company registry filings legal entity corporate registration',
         ['Company Research'], ['OpenCorporates', 'EDGAR U.S. Securities and Exchange Commission Filings']),
        ('Ownership and risk', 'company ownership subsidiaries sanctions offshore',
         ['Company Research', 'Document and Slides Search'], ['OpenSanctions', 'OCCRP Aleph', 'Offshore Leak Database']),
        ('Documents and history', 'annual report documents archive company website',
         ['Document and Slides Search', 'Web History and Website Capture'], ['DocumentCloud', 'Wayback Machine']),
        ('Reporting and data', 'company news data statistics',
         ['News', 'Data and Statistics'], ['Reuters', 'AP', 'BBC News']),
    ],
    'username': [
        ('Candidate discovery', 'username check account discovery social media',
         ['Username Check'], ['WhatsMyName', 'Sherlock', 'Maigret']),
        ('Platform verification', 'social media profile search',
         ['Social Media Tools', 'Major Social Networks'], []),
        ('Web and archive', 'username web search archive history',
         ['General Search', 'Web History and Website Capture'], ['Google Search', 'Bing', 'Wayback Machine']),
    ],
    'people': [
        ('Official public records', 'people public records professional biography official',
         ['People Investigations', 'Expert Search'], []),
        ('Organizations and work', 'company professional employment publications',
         ['Company Research', 'Academic Resources and Grey Literature'], ['OpenCorporates', 'Google Scholar']),
        ('News and archives', 'person news archive history',
         ['News', 'Web History and Website Capture'], ['Reuters', 'AP', 'Wayback Machine']),
    ],
    'email': [
        ('Defensive exposure', 'email breach exposure notification defensive',
         ['Email Search / Email Check', 'Data Breach Search Engines'], ['Have I Been Pwned']),
        ('Domain and authenticity', 'email domain MX SPF DKIM DMARC reputation',
         ['Email Search / Email Check', 'Domain and IP Research', 'DNS'], ['MXToolbox', 'DNSai']),
    ],
    'image': [
        ('Reverse search', 'reverse image search visual similarity',
         ['Image Search'], ['Google Lens', 'TinEye', 'Bing Images', 'Yandex Images']),
        ('Metadata and forensics', 'image EXIF metadata forensic analysis',
         ['Image Analysis'], ['ExifTool', 'Jeffreys Image Metadata Viewer', 'JIMPL']),
        ('Geolocation', 'image geolocation maps satellite street view',
         ['Geospatial Research and Mapping Tools'], ['Google Earth Pro', 'Google Maps', 'Mapillary', 'SunCalc']),
        ('Provenance', 'image archive earliest publication verification',
         ['Web History and Website Capture', 'Fact Checking'], ['Wayback Machine', 'Archive.is', 'Verification Handbook']),
    ],
    'news': [
        ('Discovery', 'news search local media',
         ['News', 'News Digest and Discovery Tools'], ['Reuters', 'AP', 'BBC News', 'Google News']),
        ('Primary documents', 'documents official records PDF',
         ['Document and Slides Search'], ['DocumentCloud', 'RECAP Archive']),
        ('Verification', 'fact checking verification source',
         ['Fact Checking'], ['Verification Handbook', 'Full Fact', 'Fact Check', 'Snopes']),
        ('Archive', 'website archive historical capture',
         ['Web History and Website Capture'], ['Wayback Machine', 'Archive.is']),
    ],
    'threat': [
        ('IOC enrichment', 'threat intelligence IOC IP domain hash CVE',
         ['Threat Intelligence', 'Speciality Search Engines'], ['OTX AlienVault', 'Cisco Talos Intelligence', 'Abuseipdb']),
        ('Actor context', 'threat actor APT tactics techniques',
         ['Threat Actor Search'], ['MISP Galaxy', 'Malpedia', 'APT Groups and Operations']),
        ('Infrastructure', 'passive DNS ASN BGP certificate domain',
         ['Domain and IP Research', 'DNS', 'Speciality Search Engines'], ['BGP.tools', 'CRT Certificate Search', 'Censys']),
        ('Monitoring', 'threat monitoring RSS alerts',
         ['Web Monitoring', 'OSINT RSS Feeds'], ['Google Alerts', 'Feedly']),
    ],
    'monitoring': [
        ('Official feeds', 'RSS official feed alerts',
         ['Web Monitoring', 'OSINT RSS Feeds'], ['Feedly', 'Google Alerts']),
        ('Change detection', 'website change detection archive',
         ['Web Monitoring', 'Web History and Website Capture'], ['ChangeDetection.io', 'visualping', 'Wayback Machine']),
        ('News discovery', 'news alert discovery',
         ['News Digest and Discovery Tools', 'News'], ['Google News', 'Reuters', 'AP']),
    ],
}

RISK_ORDER = {'low': 0, 'guarded': 1, 'restricted': 2}


def stage_id(title: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', title.casefold()).strip('-')


def main() -> int:
    ap = argparse.ArgumentParser(
        description='Select implementation tools after choosing an evidence-changing action.',
        epilog='Workflow bundles are suggestions, not action order. See references/adaptive-investigation-strategy.md.')
    ap.add_argument('--workflow', required=True, choices=sorted(PROFILES))
    stage_args = ap.add_mutually_exclusive_group()
    stage_args.add_argument('--stage', help='Select one stage by slug or full title; default: first stage only')
    stage_args.add_argument('--all-stages', action='store_true', help='Explicitly select tools for every workflow stage')
    stage_args.add_argument('--list-stages', action='store_true', help='List stage slugs and queries without selecting tools')
    ap.add_argument('--per-stage', type=positive_int, default=2,
                    help='Maximum tools per selected stage; first is primary, second is backup (default: 2)')
    ap.add_argument('--catalog', default=str(Path(__file__).resolve().parents[1] / 'references' / 'catalog.json'))
    ap.add_argument('--max-risk', choices=['low', 'guarded'], default='guarded')
    add_json_arguments(ap)
    args = ap.parse_args()
    validate_json_arguments(ap, args)
    stages = PROFILES[args.workflow]
    if args.list_stages:
        if args.fields is not None or args.full:
            ap.error('--fields and --full apply to tool results, not --list-stages')
        if args.json:
            print(json.dumps([{'stage_id': stage_id(title), 'stage': title, 'query': query}
                              for title, query, _, _ in stages], ensure_ascii=False, separators=(',', ':')))
        else:
            print(f'Workflow: {args.workflow}')
            for title, query, _, _ in stages:
                print(f'{stage_id(title)}\t{title}\n  {query}')
        return 0
    if args.stage is not None:
        requested = args.stage.strip().casefold()
        stages = [stage for stage in stages
                  if requested in (stage_id(stage[0]), stage[0].casefold())]
        if not stages:
            ap.error(f'unknown stage {args.stage!r} for {args.workflow}; use --list-stages')
    elif not args.all_stages:
        stages = stages[:1]
        notice = (f'Selected first stage only: {stage_id(stages[0][0])}. '
                  'Use --stage for another evidence need, or --all-stages for the full bundle.')
        print(notice, file=sys.stderr if args.json else sys.stdout)
    catalog = load_catalog(args.catalog)
    output = []
    used_domains = set()
    for stage, query, categories, preferred in stages:
        preferred_rank = {name.casefold(): len(preferred) - idx for idx, name in enumerate(preferred)}
        candidates = []
        for tool in catalog['tools']:
            if RISK_ORDER[tool['risk_tier']] > RISK_ORDER[args.max_risk]:
                continue
            if tool['category'] not in categories:
                continue
            score = score_tool(tool, query)
            bonus = 100 * preferred_rank.get(tool['name'].casefold(), 0)
            if score > 0 or bonus:
                candidates.append((score + bonus, tool))
        candidates.sort(key=lambda x: (-x[0], x[1]['risk_tier'], x[1]['name'].casefold()))
        selected = []
        for score, tool in candidates:
            if tool['domain'] in used_domains and len(candidates) > args.per_stage:
                continue
            selected.append({'score': round(score, 2), **tool})
            used_domains.add(tool['domain'])
            if len(selected) >= args.per_stage:
                break
        output.append({'stage': stage, 'query': query, 'tools': selected})
    if args.json:
        output = [{**stage, 'tools': [project_tool(tool, args.fields, args.full) for tool in stage['tools']]}
                  for stage in output]
        print(json.dumps(output, ensure_ascii=False, indent=2 if args.full else None,
                         separators=None if args.full else (',', ':')))
        return 0
    print(f'Workflow: {args.workflow}\n')
    for stage in output:
        print(f"## {stage['stage']}")
        if not stage['tools']:
            print('- No suitable catalog match; use authoritative manual sources.')
        for t in stage['tools']:
            note = t['description'] or ', '.join(t['tags'][:4])
            print(f"- {t['name']} [{t['risk_tier']}] — {note}\n  {t['url']}")
        print()
    print('Preferred names are starting anchors, not endorsements. Verify current status and use primary sources for findings.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
