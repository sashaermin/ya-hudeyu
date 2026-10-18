"""Phase2 intent must never masquerade as verified public APK capabilities."""
import copy
import unittest
import test_build
build=test_build.build

class Phase2Tests(unittest.TestCase):
    def setUp(self):
        fixture=test_build.BuildTests();fixture.setUp();self.site=fixture.site;self.release=fixture.release

    def test_intent_content_and_original_mascot_render_without_release_claims(self):
        page=build.render(self.site,self.release)
        self.assertEqual(5,len(self.site['planned_areas']))
        self.assertEqual(5,page.count('class="intent-card '))
        for text in ['будущий опыт','В разработке','Публичного выпуска пока нет','id="journey"','mascot_hint.webp','id="download"','noindex,nofollow']:
            self.assertIn(text,page)
        self.assertNotIn('downloadUrl',page)
        self.assertNotIn('softwareVersion',page)
        self.assertEqual([],self.site['features'])
        self.assertEqual([],self.site['screenshots'])
        self.assertFalse(self.release['approved_for_distribution'])

    def test_planned_areas_cannot_satisfy_full_release_gate(self):
        with self.assertRaisesRegex(ValueError,'Publication blocked'):
            build.render(self.site,self.release,production=True,publication=dict(approved=True,approval_reference='TEST ONLY',release_mode='full'))

    def test_development_status_and_source_proof_required(self):
        for change in [dict(status='released'),dict(source_commit=''),dict(source_path=''),dict(id='unsupported')]:
            site=copy.deepcopy(self.site);site['planned_areas'][0].update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):build.render(site,self.release)

    def test_project_copy_is_escaped(self):
        self.site['planned_areas'][0]['heading']='<script>alert(1)</script>'
        page=build.render(self.site,self.release)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;',page)
        self.assertNotIn('<script>alert(1)</script>',page)
