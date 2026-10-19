"""Preliminary images are integrity checked and cannot inherit release approval."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import preview_gallery as gallery
import build

class Tags(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

class PreviewGalleryTests(unittest.TestCase):
    def setUp(self):self.config=json.loads((ROOT/'data/android_preview.json').read_text())
    def test_all_eleven_integrity_portrait_and_metadata(self):
        self.assertTrue(gallery.validate(self.config,ROOT))
        self.assertEqual([i['id'] for i in self.config['items']],gallery.ORDER)
        paths=[i[k] for i in self.config['items'] for k in ('src','full')]
        self.assertEqual(len(set(paths)),22)
        self.assertEqual(set(paths),{p.relative_to(ROOT).as_posix() for p in (ROOT/'assets/previews').iterdir()})
        self.assertLess(sum((ROOT/p).stat().st_size for p in paths),1200000)
        for path in paths:
            data=(ROOT/path).read_bytes();self.assertEqual(data[:4],b'RIFF');self.assertEqual(data[8:12],b'WEBP')
            for marker in (b'EXIF',b'XMP ',b'ICCP'):self.assertNotIn(marker,data)
    def test_visible_categories_captions_and_edited_disclaimer(self):
        text=gallery.render(self.config);tags=Tags(text).tags
        figures=[a for t,a in tags if t=='figure'];self.assertEqual(len(figures),11)
        grouped=[i['id'] for key,_ in gallery.CATEGORIES for i in self.config['items'] if i['category']==key]
        self.assertEqual([a['data-preview-id'] for a in figures],grouped)
        for key,title in gallery.CATEGORIES:
            self.assertIn('href="#preview-'+key+'"',text);self.assertIn(title,text)
        for i in self.config['items']:
            self.assertIn(i['title'],text);self.assertIn(i['description'],text)
        for phrase in (gallery.LABEL,gallery.DISCLAIMER,'не точные скриншоты','Карта схематична','являются условными'):
            self.assertIn(phrase,text)
        self.assertTrue(all(a.get('loading')=='lazy' and a.get('alt') and a.get('width') and a.get('height') for t,a in tags if t=='img'))
        self.assertEqual(sum(t=='a' and a.get('class')=='preview-original' for t,a in tags),11)
    def test_dynamic_captions_escape_html(self):
        self.config['items'][0]['title']='<script>"&test</script>'
        text=gallery.render(self.config);self.assertNotIn('<script>',text);self.assertIn('&lt;script&gt;',text)
    def test_missing_screen_reorder_unreviewed_caption_and_category_rejected(self):
        for mutate in (lambda c:c['items'].pop(),lambda c:c['items'].reverse(),lambda c:c['items'][0].update(privacy_reviewed=False),lambda c:c['items'][0].update(alt=''),lambda c:c['items'][0].update(category='invented')):
            c=copy.deepcopy(self.config);mutate(c)
            with self.subTest(config=c['items'][0]['id']),self.assertRaises(ValueError):gallery.validate(c,ROOT)
    def test_path_integrity_and_dimensions_rejected(self):
        for change in ({'src':'../secret.jpg'},{'full':'https://example.com/a.apk'},{'src':'assets/previews/missing.webp'},{'sha256':'0'*64},{'width':False},{'height':1}):
            c=copy.deepcopy(self.config);c['items'][0].update(change)
            with self.subTest(change=change),self.assertRaises(ValueError):gallery.validate(c,ROOT)
    def test_missing_assets_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'assets/previews').mkdir(parents=True)
            p=root/self.config['items'][0]['src'];p.symlink_to(ROOT/self.config['items'][0]['src'])
            with self.assertRaisesRegex(ValueError,'Missing/unsafe'):gallery.validate(self.config,root)
    def test_disabled_is_backward_compatible(self):
        self.assertFalse(gallery.validate(None,ROOT));self.assertFalse(gallery.validate({'enabled':False},ROOT))
    def test_production_requires_separate_exact_manifest_approval(self):
        publication=json.loads((ROOT/'data/publication.json').read_text())
        publication.pop('preview_gallery',None)  # Isolated unapproved fixture, independent of real release policy.
        with self.assertRaisesRegex(ValueError,'Separate preliminary'):gallery.validate(self.config,ROOT,True,publication)
        publication['preview_gallery']={'approved':True,'manifest_sha256':gallery.fingerprint(self.config),'approval_reference':'TEST ONLY, not owner approval'}
        self.assertTrue(gallery.validate(self.config,ROOT,True,publication))
        self.config['items'][0]['title']+=' changed'
        with self.assertRaisesRegex(ValueError,'Separate preliminary'):gallery.validate(self.config,ROOT,True,publication)
    def test_builder_draft_only_preserves_apk_noindex_and_existing_sections(self):
        site=json.loads((ROOT/'data/site.json').read_text());release=json.loads((ROOT/'data/release.json').read_text())
        html=build.render(site,release,preview=self.config)
        self.assertEqual(html.count('data-preview-id='),11)
        self.assertIn('noindex,nofollow',html);self.assertNotIn('.apk',html)
        self.assertIn('Посмотрите, как выглядит приложение',html)
        self.assertIn('id="viewer-zoom"',html);self.assertIn('class="viewer-canvas"',html)
        self.assertEqual(html.count('<details id="question-'),33)
        publication=json.loads((ROOT/'data/publication.json').read_text())
        publication.pop('preview_gallery',None)  # Isolated unapproved fixture, independent of real release policy.
        with self.assertRaisesRegex(ValueError,'Separate preliminary'):build.render(site,release,True,publication,preview=self.config)
