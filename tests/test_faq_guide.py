import copy
import json
from pathlib import Path
import unittest
import test_build

ROOT=Path(__file__).resolve().parents[1]
build=test_build.build
class FaqGuideTests(unittest.TestCase):
    def setUp(self):
        self.site=json.loads((ROOT/'data/site.json').read_text());self.release=json.loads((ROOT/'data/release.json').read_text())
    def test_categories_ids_questions_and_sources_match_reviewed_matrix(self):
        coverage=json.loads((ROOT/'docs/verification/faq-feature-coverage.json').read_text())
        self.assertEqual(8,len(self.site['faq_categories']));self.assertEqual(33,len(self.site['faq']))
        self.assertEqual({q['id']:q['answer'] for q in self.site['faq']},{q['id']:q['answer'] for q in coverage['topics']})
        for topic in coverage['topics']:
            self.assertTrue(topic['sources'] or topic['website_source'])
            for source in topic['sources']:
                self.assertEqual(coverage['android_snapshot'],source['commit']);self.assertGreater(source['line'],0)
    def test_anchor_and_details_semantics_no_js_dependency(self):
        page=build.render(self.site,self.release)
        self.assertEqual(33,page.count('<details'))
        for category in self.site['faq_categories']:
            self.assertIn('href="#faq-'+category['id']+'"',page)
            self.assertIn('id="faq-'+category['id']+'" tabindex="-1"',page)
        self.assertIn('Справочник по текущей разработке',page)
        self.assertNotIn('downloadUrl',page);self.assertIn('noindex,nofollow',page)
    def test_invalid_duplicate_or_empty_categories_rejected(self):
        changes=[lambda s:s['faq_categories'].append(s['faq_categories'][0]),lambda s:s['faq'][0].update(category='missing'),lambda s:s['faq'][0].update(id=s['faq'][1]['id']),lambda s:s['faq_categories'].append(dict(id='empty',title='Empty')),lambda s:s['faq_categories'][0].update(id='bad" onclick=')]
        for change in changes:
            site=copy.deepcopy(self.site);change(site)
            with self.assertRaises(ValueError):build.render(site,self.release)
    def test_category_and_answer_escaping_and_legacy_fallback(self):
        self.site['faq_categories'][0]['title']='<script>bad</script>'
        self.site['faq'][0]['answer']='<img src=x onerror=bad>'
        page=build.render(self.site,self.release)
        self.assertIn('&lt;script&gt;',page);self.assertIn('&lt;img',page)
        del self.site['faq_categories']
        self.assertEqual(33,build.render(self.site,self.release).count('<details'))
    def test_future_verified_fixture_preserves_question_category(self):
        f=test_build.BuildTests();f.setUp();f.ready_fixture()
        page=build.render(f.site,f.release)
        self.assertEqual(8,page.count('class="faq-group"'))
        self.assertIn('Где скачать приложение?',page)
