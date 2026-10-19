#!/usr/bin/env python3
"""Read-only HTTPS and browser QA of the recorded production release.

Run on the existing GitHub runner with its normal TLS trust. Never deploy,
change trust stores, disable certificate checks, or infer a new release.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

import browser_qa
import uiux_qa
import gallery_loading_qa
import faq_qa
import download_live_qa

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://yahudeyu-app.ru/'
PRIVATE = ['AGENTS.md', 'AGENT_HANDOFF.md', 'AGENT_DEVELOPMENT_PROTOCOL.md',
           'docs/FIRST_RELEASE.md', 'data/publication.json', 'data/release.json',
           'project_specs/WEBSITE_MASTER_TZ_2026-10-18.md',
           '.github/workflows/website-checks.yml', 'tools/build.py',
           'tests/test_build.py', '.git/config', 'README.md',
           'docs/UI_UX_REQUIREMENTS_AUDIT.md',
           'project_specs/UIUX_PRODUCTION_AUTHORIZATION_2026-10-18.md',
           'gallery-loading-fixture', 'gallery-qa-fixture',
           'docs/BETA_REVIEW.md', 'docs/FAQ_GUIDE.md', 'data/site.json',
           'templates/download.html', 'tools/beta_release.py', 'tests/beta_fixture.py',
           'fixture/', 'download/fixture/',
           'project_specs/PHASE2_FAQ_BETA_PRODUCTION_AUTHORIZATION_2026-10-20.md']


def fetch(path):
    request = urllib.request.Request(BASE + path, headers={'Cache-Control': 'no-cache'})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            assert response.url.startswith(BASE), response.url
            body = response.read()
            return dict(path=path, status=response.status,
                        sha256=hashlib.sha256(body).hexdigest())
    except urllib.error.HTTPError as error:
        return dict(path=path, status=error.code)


def run(executable, output, manifest_path=None, detailed_ui=False, expanded=False):
    manifest = json.loads((manifest_path or ROOT/'docs/verification/uiux-production-release.json').read_text())
    records = manifest['files']
    expected_commit = manifest['prepared_production_commit']
    result = dict(checked_at=datetime.now(timezone.utc).isoformat(), base=BASE,
                  production_commit=expected_commit, read_only=True,
                  tls_verification=True, custom_ca_changes=False, status='RUNNING')
    output.mkdir(parents=True, exist_ok=True)
    try:
        with ThreadPoolExecutor(max_workers=6) as pool:
            result['http'] = list(pool.map(fetch, [''] + [r['path'] for r in records] + PRIVATE))
        by_path = {r['path']: r for r in result['http']}
        for record in records:
            actual = by_path[record['path']]
            assert actual['status'] == 200, actual
            assert actual['sha256'] == record['sha256'], actual
        assert by_path['']['sha256'] == by_path['index.html']['sha256']
        for path in PRIVATE:
            assert by_path[path]['status'] == 404, by_path[path]
        with urllib.request.urlopen(BASE, timeout=30) as response:
            page = response.read().decode()
            assert 'content="noindex,nofollow"' in page
            assert 'Скоро для Android' in page
            assert 'downloadUrl' not in page
        with urllib.request.urlopen(BASE+'robots.txt', timeout=30) as response:
            assert response.read() == b'User-agent: *\nDisallow: /\n'
        axe = str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js') if detailed_ui else None
        browser_qa.run(BASE, output, axe, executable=executable)
        browser = json.loads((output/'browser-results.json').read_text())
        assert len(browser['matrix']) == 16
        assert not browser['page_errors'] and not browser['failed_requests']
        if detailed_ui:
            uiux_qa.run(BASE, output/'uiux', executable=executable)
            gallery_loading_qa.run(BASE, output/'gallery', executable=executable)
            ui = json.loads((output/'uiux/uiux-results.json').read_text())
            gallery = json.loads((output/'gallery/gallery-loading-results.json').read_text())
            result['uiux'] = dict(privacy_matrix=len(ui['privacy_matrix']), nojs_cases=len(ui['nojs']),
                                  legal_text_unchanged=ui['legal_content_unchanged'],
                                  keyboard_focus=ui['focus'], gallery_theme_cases=len(gallery),
                                  axe_runs=len(browser['axe'])+len(ui['privacy_axe'])+len(gallery)*2,
                                  axe_violations=0, gallery_scope='Browser-only mascot fixtures with actual deployed JS/assets, not published Android screenshots')
        if expanded:
            faq_qa.run(BASE,output/'expanded/faq','chromium',executable)
            faq=json.loads((output/'expanded/faq/faq-results.json').read_text())
            download=download_live_qa.run(BASE,output/'expanded/download',executable)
            # Exact approved Phase2 content still marked as development, not released APK features.
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b=p.chromium.launch(executable_path=executable,args=['--no-sandbox'])
                pg=b.new_page();pg.goto(BASE)
                assert pg.locator('.intent-card').count()==5
                assert pg.locator('.journey-list li').count()==4
                assert pg.locator('.motivation img').get_attribute('src')=='assets/brand/originals/mascot_hint.webp'
                assert pg.locator('.faq-categories a').count()==8 and pg.locator('.faq-group details').count()==33
                assert 'Справочник по текущей разработке.' in pg.locator('.faq-development-note').inner_text()
                assert 'TEST ONLY' not in pg.content() and 'ТЕСТОВЫЙ МАКЕТ' not in pg.content()
                b.close()
            result['expanded']=dict(faq_layouts=len(faq['matrix']),faq_categories=8,faq_questions=33,faq_nojs=len(faq['nojs']),
                download_layouts=len(download['matrix']),download_nojs=len(download['nojs']),
                axe_runs=len(faq['axe'])+len(download['axe']),axe_violations=0,
                development_intent_cards=5,journey_steps=4,download_unavailable=True,no_fixture_publication=True)
        result.update(status='PASS', public_files_verified=len(records),
                      private_paths_404=len(PRIVATE), browser_version=browser['browser_version'],
                      matrix_runs=16, interactions=browser['interactions'],
                      noindex=True, apk_download=False)
    except Exception as error:
        result.update(status='FAIL', error=str(error))
        raise
    finally:
        (output/'production-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        if detailed_ui:
            print('::notice title=Production UI UX verified::' + json.dumps(dict(production_commit=expected_commit, **result['uiux']), ensure_ascii=False))
        if expanded:
            print('::notice title=Production expanded release verified::'+json.dumps(dict(production_commit=expected_commit,**result['expanded']),ensure_ascii=False))
        print(f'::notice title=Production website verified::commit {expected_commit}; '
              f'public_files {len(records)}; internal_404 {len(PRIVATE)}; '
              'browser_matrix 16; noindex=true; APK=false; TLS=true; page_errors=0')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--executable', required=True)
    parser.add_argument('--output', type=Path, default=ROOT/'.test-results/production')
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--uiux', action='store_true', help='Also verify audited privacy/navigation and browser-only gallery loading fixtures')
    parser.add_argument('--expanded', action='store_true', help='Read-only Phase2/categorized FAQ/unavailable download QA')
    args = parser.parse_args()
    run(args.executable, args.output, args.manifest, args.uiux, args.expanded)
