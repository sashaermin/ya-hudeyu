"""Repository-only cold-start contract; not an actual transfer between agents."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('handoff_notify', ROOT/'.github/scripts/telegram_notify.py')
notify = importlib.util.module_from_spec(spec); spec.loader.exec_module(notify)


class HandoffContractTests(unittest.TestCase):
    def test_common_entrypoints_and_local_canonical_links_are_present(self):
        for name in ['AGENTS.md', 'CLAUDE.md', 'AGENT_HANDOFF.md', 'AGENT_NOTIFICATION_PROTOCOL.md']:
            text = (ROOT/name).read_text()
            self.assertIn('AGENT_DEVELOPMENT_PROTOCOL.md', text, name)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((ROOT/target.split('#')[0]).is_file(), (name, target))
        workflow=(ROOT/'.github/workflows/website-checks.yml').read_text()
        self.assertIn('AGENT_DEVELOPMENT_PROTOCOL.md', workflow)
        self.assertIn('AGENT_NOTIFICATION_PROTOCOL.md', workflow)
        self.assertIn('telegram_notify.py report-check',workflow)

    def test_repository_handoff_contains_action_spec_qa_and_release_boundary(self):
        text=(ROOT/'AGENT_HANDOFF.md').read_text()
        self.assertTrue(notify.next_action(text))
        for fact in ['sashaermin/ya-hudeyu','work/website-v2','IMPLEMENTATION_PROGRESS.md','WEBSITE_MASTER_TZ_2026-10-18.md','docs/QA.md','python3 tools/build.py','noindex','main','site-first-website-release-policy']:
            self.assertIn(fact,text)
        self.assertRegex(text,r'`[0-9a-f]{40}`')
        self.assertIn('patch применён',text)
        self.assertIn('APK approval остаётся false',text)
        self.assertIn('indexing_approved=false',text)
