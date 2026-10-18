import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build', ROOT / 'tools/build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class BuildTests(unittest.TestCase):
    def setUp(self):
        self.site = json.loads((ROOT / 'data/site.json').read_text())
        self.release = json.loads((ROOT / 'data/release.json').read_text())

    def test_draft_has_no_download_and_noindex(self):
        page = build.render(self.site, self.release)
        self.assertIn('noindex,nofollow', page)
        self.assertIn('APK пока недоступен', page)
        self.assertNotIn('>Скачать для Android', page)
        self.assertNotIn('{{', page)

    def test_unapproved_release_cannot_produce_production(self):
        with self.assertRaisesRegex(ValueError, 'Publication blocked'):
            build.render(self.site, self.release, production=True)

    def test_code_only_feature_is_rejected(self):
        self.site['features'] = [{'title':'Feature from development', 'description':'Unverified'}]
        with self.assertRaisesRegex(ValueError, 'not verified'):
            build.render(self.site, self.release)

    def test_development_screenshot_is_rejected(self):
        self.site['screenshots'] = [{'src':'assets/brand/originals/mascot_calm.webp'}]
        with self.assertRaisesRegex(ValueError, 'not approved'):
            build.render(self.site, self.release)

    def test_https_only(self):
        for url in ['http://example.com/a.apk','javascript:alert(1)','https://user:password@example.com/a.apk']:
            with self.subTest(url=url), self.assertRaises(ValueError): build.https(url)

    def test_asset_path_safety(self):
        for path in ['../../secret', 'assets/../README.md', '/etc/passwd', 'assets/missing.png']:
            with self.subTest(path=path), self.assertRaises(ValueError): build.asset(path)

    def test_content_is_escaped(self):
        self.site['faq'][0]['answer'] = '<script>alert("bad")</script>'
        page = build.render(self.site, self.release)
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<script>alert(', page)

    def test_build_is_repeatable_and_excludes_private_files(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'_site'
            build.build(output)
            first = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            build.build(output)
            second = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            self.assertEqual(first, second)
            self.assertFalse((output/'docs').exists())
            self.assertFalse((output/'project_specs').exists())
            self.assertFalse((output/'data').exists())
            self.assertEqual((ROOT/'privacy.html').read_bytes(), (output/'privacy.html').read_bytes())
            self.assertEqual((ROOT/'CNAME').read_bytes(), (output/'CNAME').read_bytes())

    def test_verified_metadata_requires_checksum_and_proof(self):
        self.release.update(status='verified', approved_for_distribution=True, approval_reference='TEST fixture, never an actual authorization')
        with self.assertRaisesRegex(ValueError, 'Missing verified release field'):
            build.render(self.site, self.release)

    def test_verified_status_cannot_bypass_owner_approval(self):
        self.release['status'] = 'verified'
        with self.assertRaisesRegex(ValueError, 'Owner approval'):
            build.render(self.site, self.release)

    def ready_fixture(self):
        # Test-only proof records; no real APK is approved or added to project data.
        self.release.update(status='verified',version='TEST-ONLY',date='2026-10-18',url='https://example.com/test-only.apk',size_bytes=1,sha256='a'*64,min_android='TEST',source_commit='a'*40,verification_note='TEST ONLY',approved_for_distribution=True,approval_reference='TEST ONLY')
        self.site['features']=[dict(title='TEST',description='TEST ONLY',verified_version='TEST-ONLY',evidence='TEST ONLY')]
        self.site['screenshots']=[dict(src='assets/brand/originals/mascot_calm.webp',width=440,height=512,alt='TEST ONLY',caption='TEST ONLY',verified_version='TEST-ONLY',evidence='TEST ONLY',approved_for_publication=True)]

    def test_apk_approval_cannot_authorize_website_indexing(self):
        self.ready_fixture()
        for publication in [None,{},dict(approved=False,approval_reference='TEST'),dict(approved=True,approval_reference='')]:
            with self.subTest(publication=publication),self.assertRaisesRegex(ValueError,'Separate website publication approval'):
                build.render(self.site,self.release,production=True,publication=publication)

    def test_website_approval_cannot_bypass_apk_gate(self):
        with self.assertRaisesRegex(ValueError,'Publication blocked'):
            build.render(self.site,self.release,production=True,publication=dict(approved=True,approval_reference='TEST ONLY'))

    def test_preview_keeps_noindex_even_if_publication_is_authorized(self):
        self.ready_fixture();publication=dict(approved=True,approval_reference='TEST ONLY')
        self.assertIn('noindex,nofollow',build.render(self.site,self.release,publication=publication))
        self.assertIn('content="index,follow"',build.render(self.site,self.release,production=True,publication=publication))

    def test_structured_data_roundtrips_html_sensitive_names_safely(self):
        import re
        self.site['name']='</script><img src=x onerror=alert(1)>'
        page=build.render(self.site,self.release)
        block=re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S).group(1)
        self.assertEqual(self.site['name'],json.loads(block)['name'])
        self.assertNotIn('</script>',block)

    def test_support_and_domain_cannot_inject_attributes(self):
        self.site['support'] = 'x@y.com" onclick="alert(1)'
        with self.assertRaises(ValueError): build.render(self.site, self.release)

if __name__ == '__main__': unittest.main()
