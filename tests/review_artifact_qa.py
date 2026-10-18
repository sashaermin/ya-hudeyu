#!/usr/bin/env python3
"""Verify a downloaded CI review bundle, then render that archive on loopback."""
import argparse
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path, PurePosixPath
import stat
import tempfile
import threading
import urllib.request
import zipfile

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run(archive, checkpoint, output, executable, local=False):
    manifest = json.loads(archive.with_suffix('.manifest.json').read_text())
    expected = json.loads((ROOT / 'docs/verification/release-candidate.json').read_text())
    assert manifest['source_commit'] == checkpoint
    if not local:
        assert manifest['source_worktree_dirty'] is False
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert digest == manifest['sha256'] == expected['archive_sha256']
    assert archive.stat().st_size == manifest['size_bytes']
    result = dict(source_commit=checkpoint, archive_sha256=digest,
                  source_worktree_dirty=manifest['source_worktree_dirty'],
                  archive_files_verified=0, rendered=[], page_errors=[],
                  scope='Local archive rehearsal only' if local else 'Downloaded CI archive on loopback; no hosted preview or production deployment')
    with tempfile.TemporaryDirectory() as directory:
        with zipfile.ZipFile(archive) as bundle:
            records = {item['path']: item for item in manifest['files']}
            assert len(records) == len(manifest['files']) == len(bundle.namelist())
            assert set(records) == set(bundle.namelist())
            for entry in bundle.infolist():
                name = PurePosixPath(entry.filename)
                assert not name.is_absolute() and '..' not in name.parts
                assert not stat.S_ISLNK(entry.external_attr >> 16)
                content = bundle.read(entry)
                assert len(content) == records[entry.filename]['size_bytes']
                assert hashlib.sha256(content).hexdigest() == records[entry.filename]['sha256']
                result['archive_files_verified'] += 1
            bundle.extractall(directory)
        handler = functools.partial(QuietHandler, directory=directory)
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}/'
        try:
            with urllib.request.urlopen(base + 'privacy.html') as response:
                assert response.status == 200
                assert response.read() == (ROOT / 'privacy.html').read_bytes()
            with sync_playwright() as p:
                browser = p.chromium.launch(executable_path=executable, args=['--no-sandbox'])
                result['browser_version'] = browser.version
                for width in (390, 1440):
                    for theme in ('light', 'dark'):
                        context = browser.new_context(viewport={'width': width, 'height': 900}, color_scheme=theme)
                        page = context.new_page()
                        page.on('pageerror', lambda error: result['page_errors'].append(str(error)))
                        response = page.goto(base)
                        assert response.status == 200
                        assert hashlib.sha256(response.body()).hexdigest() == expected['site_index_sha256']
                        page.evaluate('document.fonts.ready')
                        assert 'Я ХУдЕЮ' in page.title()
                        assert 'большим' in page.locator('h1').inner_text()
                        assert 'скоро для android' in page.locator('.release-status').inner_text().casefold()
                        assert page.locator('html').get_attribute('data-theme') == theme
                        assert page.locator('meta[name=robots]').get_attribute('content') == 'noindex,nofollow'
                        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                        assert page.locator('.hero-cat').evaluate('el => el.complete && el.naturalWidth > 0')
                        for href in page.locator('a[href]').evaluate_all('els => els.map(el => el.getAttribute("href"))'):
                            assert href.startswith(('#', 'mailto:')) or href == 'privacy.html', href
                        if width == 390:
                            page.locator('#menu-toggle').click()
                            assert page.locator('#menu-toggle').get_attribute('aria-expanded') == 'true'
                            page.keyboard.press('Escape')
                        page.locator('summary').first.click()
                        assert page.locator('details').first.get_attribute('open') is not None
                        result['rendered'].append(dict(width=width, theme=theme, status='PASS', coming_soon=True, apk_download=False, noindex=True))
                        context.close()
                browser.close()
        finally:
            server.shutdown(); thread.join(); server.server_close()
    assert not result['page_errors'], result['page_errors']
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not local and os.environ.get('GITHUB_ACTIONS') == 'true':
        print(f'::notice title=Website review archive verified::source {checkpoint}; archive_sha256 {digest}; files {result["archive_files_verified"]}; rendered 4; noindex=true; APK=false; page_errors=0')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--executable', default='/usr/bin/chromium')
    parser.add_argument('--local-rehearsal', action='store_true', help='Allow dirty local manifest; never report remote verification')
    parser.add_argument('--output', type=Path, default=ROOT / '.test-results/review-artifact.json')
    args = parser.parse_args()
    run(args.archive, args.checkpoint, args.output, args.executable, args.local_rehearsal)
