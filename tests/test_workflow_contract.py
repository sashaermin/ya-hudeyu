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

if __name__ == '__main__': unittest.main()
