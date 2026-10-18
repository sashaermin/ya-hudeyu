"""Static safety checks for a workflow that must never publish the site."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class WorkflowContractTests(unittest.TestCase):
    def test_only_development_pushes_and_no_deploy_permissions(self):
        workflow = (ROOT/'.github/workflows/website-checks.yml').read_text()
        self.assertIn("branches: ['work/**']", workflow)
        self.assertIn('contents: read', workflow)
        self.assertNotIn('pages: write', workflow)
        self.assertNotIn('pull_request_target:', workflow)
        self.assertNotIn('deploy-pages', workflow)
        self.assertNotIn('contents: write', workflow)
        self.assertIn("needs.verify.result == 'success'", workflow)
        self.assertIn('persist-credentials: false', workflow)
        self.assertIn('restore-keys: website-telegram-${{ github.ref }}-', workflow)

    def test_prepared_digest_schedule_has_no_production_side_effects(self):
        workflow=(ROOT/'.github/workflows/website-digest.yml').read_text()
        self.assertIn("cron: '0 18 * * *'",workflow)
        self.assertIn('ref: work/website-v2',workflow)
        self.assertIn('actions: read',workflow)
        self.assertIn('digest --branch work/website-v2',workflow)
        self.assertNotIn('pages: write',workflow)
        self.assertNotIn('contents: write',workflow)
        self.assertNotIn('deploy-pages',workflow)

if __name__ == '__main__': unittest.main()
