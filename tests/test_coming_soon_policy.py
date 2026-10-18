"""Approved coming-soon publication gates and independent indexing control."""
import json
from pathlib import Path
import unittest
import test_build

ROOT = Path(__file__).resolve().parents[1]
build = test_build.build

class ComingSoonPolicyTests(unittest.TestCase):
    def setUp(self):
        self.site = json.loads((ROOT / 'data/site.json').read_text())
        self.release = json.loads((ROOT / 'data/release.json').read_text())
        self.publication = dict(approved=True, approval_reference='TEST ONLY', release_mode='coming-soon')

    def test_explicit_coming_soon_website_approval_does_not_enable_apk(self):
        page = build.render(self.site, self.release, production=True, publication=self.publication)
        self.assertIn('content="index,follow"', page)
        self.assertIn('Скоро для Android', page)
        self.assertNotIn('>Скачать для Android', page)
        self.assertNotIn('downloadUrl', page)
        self.assertIn('noindex,nofollow', build.render(self.site, self.release, publication=self.publication))

    def test_mode_cannot_replace_real_site_approval(self):
        for approval, reference in [(False, 'TEST'), ('true', 'TEST'), (True, ''), (True, ' '), (True, None)]:
            with self.subTest(approval=approval, reference=reference), self.assertRaisesRegex(ValueError, 'Separate website publication approval'):
                build.render(self.site, self.release, production=True, publication=dict(approved=approval, approval_reference=reference, release_mode='coming-soon'))

    def test_unknown_mode_is_not_a_gate_bypass(self):
        self.publication['release_mode'] = 'ignore-release-gates'
        with self.assertRaisesRegex(ValueError, 'Unknown website release mode'):
            build.render(self.site, self.release, production=True, publication=self.publication)

    def test_coming_soon_cannot_carry_unverified_app_content(self):
        for key, value in [('features', [dict(title='Unverified')]), ('screenshots', [dict(src='unverified')])]:
            site = dict(self.site, **{key: value})
            with self.subTest(key=key), self.assertRaises(ValueError):
                build.render(site, self.release, production=True, publication=self.publication)

    def test_ready_apk_cannot_use_coming_soon_to_avoid_full_release_requirements(self):
        fixture = test_build.BuildTests()
        fixture.setUp(); fixture.ready_fixture()
        with self.assertRaisesRegex(ValueError, 'must not contain an APK'):
            build.render(fixture.site, fixture.release, production=True, publication=self.publication)

    def test_production_can_preserve_noindex_without_bypassing_site_approval(self):
        self.publication['indexing_approved'] = False
        page = build.render(self.site, self.release, production=True, publication=self.publication)
        self.assertIn('content="noindex,nofollow"', page)
        self.assertNotIn('downloadUrl', page)
        self.publication['approved'] = False
        with self.assertRaisesRegex(ValueError, 'Separate website publication approval'):
            build.render(self.site, self.release, production=True, publication=self.publication)

    def test_indexing_flag_requires_true_boolean_and_never_indexes_draft(self):
        for flag in [False, None, 'true', 1]:
            with self.subTest(flag=flag):
                pub = dict(self.publication, indexing_approved=flag)
                self.assertIn('content="noindex,nofollow"', build.render(self.site, self.release, True, pub))
        pub = dict(self.publication, indexing_approved=True)
        self.assertIn('content="index,follow"', build.render(self.site, self.release, True, pub))
        self.assertIn('content="noindex,nofollow"', build.render(self.site, self.release, False, pub))
