import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preview', ROOT / 'tools/package_preview.py')
preview = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preview)


class PreviewPackageTests(unittest.TestCase):
    def test_archive_is_reproducible_and_contains_only_protected_public_draft(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / 'preview.zip'
            first = preview.package(archive)
            original = archive.read_bytes()
            self.assertEqual(first, preview.package(archive))
            self.assertEqual(original, archive.read_bytes())
            self.assertEqual(first, json.loads(archive.with_suffix('.manifest.json').read_text()))
            with zipfile.ZipFile(archive) as content:
                names = content.namelist()
                self.assertEqual(sorted(names), sorted(item['path'] for item in first['files']))
                self.assertIn('index.html', names)
                self.assertIn('.nojekyll', names)
                self.assertIn('privacy.html', names)
                self.assertIn('noindex,nofollow', content.read('index.html').decode())
                self.assertEqual(b'User-agent: *\nDisallow: /\n', content.read('robots.txt'))
                self.assertFalse(any(name.startswith(('docs/', 'data/', 'project_specs/', '.github/', 'tests/')) for name in names))
                self.assertFalse(any(name.endswith('.apk') for name in names))
                self.assertEqual(content.read('CNAME'), (ROOT / 'CNAME').read_bytes())
                self.assertEqual(content.read('privacy.html'), (ROOT / 'privacy.html').read_bytes())


if __name__ == '__main__':
    unittest.main()
