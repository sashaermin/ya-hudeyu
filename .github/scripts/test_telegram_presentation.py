"""Differential checks against pre-change output, without credentials or network."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import preview_telegram as preview
import telegram_notify as notify


class ReadHTML(HTMLParser):
    def __init__(self, strict=False):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.stack, self.strict = [], [], [], strict

    def handle_starttag(self, tag, attrs):
        if self.strict:
            assert tag in ('b', 'i', 'code', 'pre', 'a', 'blockquote'), tag
        if tag == 'a': self.links.append(dict(attrs)['href'])
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.strict: assert self.stack and self.stack[-1] == tag, (tag, self.stack)
        if self.stack and self.stack[-1] == tag: self.stack.pop()

    def handle_data(self, value): self.text.append(value)


def read(text, strict=False):
    parser = ReadHTML(strict); parser.feed(text); parser.close()
    if strict: assert not parser.stack, parser.stack
    return parser


def body(text):
    # Compare the same selected information. Only the project/title frame and
    # whitespace change; event wording/icons are checked separately below.
    if text.startswith('<b>Я ХУдЕЮ | DEV REPORTS</b>'):
        value = text.split('</b>', 2)[2]
        value = value.replace('\n────────', '', 1)
    else:
        value = text.split('</b>', 1)[1]
    return ' '.join(''.join(read(value).text).split())


class PresentationTest(unittest.TestCase):
    def test_every_message_preserves_selected_information_links_and_html_limits(self):
        directory = Path(__file__).resolve().parents[2] / '.github/telegram-presentation'
        expected = json.loads((directory / 'snapshots.json').read_text())
        with patch('urllib.request.urlopen', side_effect=AssertionError('Network forbidden')):
            actual = preview.samples()
        self.assertEqual(set(expected), set(actual))
        for name, text in actual.items():
            with self.subTest(kind=name):
                baseline = expected[name]['before_html']
                self.assertEqual(expected[name]['after_sha256'], hashlib.sha256(text.encode()).hexdigest())
                parsed = read(text, strict=True)
                self.assertEqual(read(baseline).links, parsed.links)
                if len(''.join(read(baseline).text).encode('utf-16-le')) // 2 <= 4096:
                    self.assertEqual(body(baseline), body(text))
                else:
                    self.assertIn('обрезано по лимиту Telegram', text)
                    for word in ('Ветка:', preview.BRANCH):
                        self.assertIn(word, ''.join(parsed.text))
                limit = 3900 if preview.PLATFORM == 'Windows' and 'digest' in name else 4096
                if preview.PLATFORM != 'Windows' or 'digest' in name:
                    self.assertLessEqual(len(text), limit)
                self.assertLessEqual(len(''.join(parsed.text).encode('utf-16-le')) // 2, 4096)
                if not name.startswith('long_'):
                    self.assertTrue(text.startswith('<b>Я ХУдЕЮ | DEV REPORTS</b>\n' + preview.PLATFORM + '\n<b>'))
                self.assertEqual(notify.style_message(text, preview.PLATFORM, limit), text)

    def test_gallery_is_reproducible_and_contains_no_active_assets(self):
        directory = Path(__file__).resolve().parents[2] / '.github/telegram-presentation'
        pairs = json.loads((directory / 'snapshots.json').read_text())
        gallery = (directory / 'preview.html').read_text()
        self.assertEqual(preview.gallery(pairs), gallery)
        self.assertNotIn('<script', gallery)
        self.assertNotIn('<img', gallery)
        self.assertIn("default-src 'none'", gallery)

    def test_hostile_text_stays_escaped_and_technical_details_use_blockquotes(self):
        source = '<b>' + {'Android':'ANDROID «Я ХУдЕЮ» — ', 'Website':'САЙТ «Я ХУдЕЮ» — ', 'Windows':'WINDOWS «Я ХУдЕЮ» | '}[preview.PLATFORM] + 'Проверка</b>\n\n<b>Проверки:</b> &lt;script&gt; &amp; &quot;x&quot;'
        result = notify.style_message(source, preview.PLATFORM)
        self.assertIn('<blockquote>&lt;script&gt; &amp; &quot;x&quot;</blockquote>', result)
        self.assertNotIn('<script>', result)
        self.assertEqual(body(source), body(result))
        read(result, strict=True)
