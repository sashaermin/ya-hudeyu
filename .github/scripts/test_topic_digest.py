"""Topic wire format and safe, factual 24h digest regression checks; no network sends."""
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import telegram_notify as tn


class TopicRoutingTest(unittest.TestCase):
    def payload(self, value):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"ok":true,"result":{"message_id":42,"message_thread_id":6}}'
        with mock.patch('sys.stdout', io.StringIO()), mock.patch.dict(os.environ, {'TELEGRAM_MESSAGE_THREAD_ID': value}), mock.patch.object(tn.urllib.request, 'urlopen', return_value=response) as call:
            self.assertEqual(42, tn.send('TEST_TOKEN', 'TEST_CHAT', '<b>Report</b>'))
        return json.loads(call.call_args.args[0].data)

    def test_topic_is_integer_and_existing_html_options_unchanged(self):
        p = self.payload('6')
        self.assertEqual(6, p['message_thread_id'])
        self.assertIs(type(p['message_thread_id']), int)
        self.assertEqual('HTML', p['parse_mode'])
        self.assertTrue(p['disable_web_page_preview'])
        self.assertEqual('<b>Report</b>', p['text'])

    def test_unconfigured_topic_preserves_legacy_request(self):
        for value in ['', '   ']:
            self.assertNotIn('message_thread_id', self.payload(value))

    def test_invalid_topic_never_posts_to_general_or_leaks_value(self):
        for value in ['0', '-6', '6.0', 'secret-invalid', '６']:
            with self.subTest(value=value), mock.patch.dict(os.environ, {'TELEGRAM_MESSAGE_THREAD_ID': value}), mock.patch.object(tn.urllib.request, 'urlopen') as call:
                with self.assertRaises(RuntimeError) as error:
                    tn.send('TEST_TOKEN', 'TEST_CHAT', 'text')
                call.assert_not_called()
                self.assertNotIn(value, str(error.exception))

    def test_retry_keeps_topic_and_payload(self):
        response = mock.MagicMock()
        response.__enter__.return_value.read.return_value = b'{"ok":true,"result":{"message_id":42,"message_thread_id":6}}'
        with mock.patch('sys.stdout', io.StringIO()), mock.patch.dict(os.environ, {'TELEGRAM_MESSAGE_THREAD_ID': '6'}), mock.patch.object(tn.time, 'sleep'), mock.patch.object(tn.urllib.request, 'urlopen', side_effect=[tn.urllib.error.URLError('test'), response]) as call:
            self.assertEqual(42, tn.send('TEST_TOKEN', 'TEST_CHAT', 'text'))
        self.assertEqual(2, call.call_count)
        self.assertEqual(call.call_args_list[0].args[0].data, call.call_args_list[1].args[0].data)
        self.assertEqual(6, json.loads(call.call_args.args[0].data)['message_thread_id'])

    def test_check_config_rejects_invalid_optional_routing(self):
        with mock.patch.dict(os.environ, {'TELEGRAM_BOT_TOKEN':'TEST', 'TELEGRAM_CHAT_ID':'TEST', 'TELEGRAM_MESSAGE_THREAD_ID':'invalid'}), mock.patch('sys.stdout', io.StringIO()):
            self.assertEqual(1, tn.run_check_config())


class DailyDigestTest(unittest.TestCase):
    def test_pagination_period_statuses_and_dry_run_without_secrets_or_ledger(self):
        class GH:
            def __init__(self): self.calls=[]
            def get(self, path, params=None):
                self.calls.append((path,params))
                if path.endswith('/commits'):
                    item={'sha':'a'*40,'commit':{'committer':{'date':'2026-10-18T13:00:00Z'},'message':'subject\n\nReport-Summary: Реальное <изменение> & проверка\nAgent: Codex'}}
                    return [item]*100 if params['page']==1 else [dict(item,sha='b'*40)]
                item={'name':'Проверка <HTML>', 'html_url':'https://github.com/o/r/actions/runs/1', 'head_branch':'work/website-v2','conclusion':'success'}
                return {'workflow_runs':[item,dict(item,conclusion='failure'),dict(item,conclusion=None,status='in_progress')]}
            def file_at(self,path,ref):
                if path=='AGENT_HANDOFF.md': return '**Exact next:** Ожидается APK'
                if path==tn.ACTIONS_FILE:
                    return json.dumps({'alerts':[dict(id='apk',status='open',source='Codex',task='APK',subtask='Нужен APK',what='Нет разрешения',steps=['Выбрать файл'],blocked='Нет <артефакта>',can_continue='Независимые задачи выполнены')]})
                return None
        gh=GH()
        with tempfile.TemporaryDirectory() as folder:
            ledger=Path(folder)/'missing'/'ledger.txt'
            output=io.StringIO()
            with mock.patch.dict(os.environ, {'GITHUB_REPOSITORY':'o/r'},clear=True), mock.patch.object(tn,'GitHub',return_value=gh), mock.patch.object(tn,'send') as sender, mock.patch('sys.stdout',output):
                self.assertEqual(0,tn.main(['digest','--branch','work/website-v2','--dry-run','--ledger',str(ledger)]))
            sender.assert_not_called(); self.assertFalse(ledger.exists())
        text=output.getvalue()
        for value in ['</code>: 101','Реальное &lt;изменение&gt; &amp; проверка','success','failure','in_progress','Нет &lt;артефакта&gt;','Ожидается APK']:
            self.assertIn(value,text)
        commit_params=[params for path,params in gh.calls if path.endswith('/commits')]
        self.assertEqual([1,2],[p['page'] for p in commit_params])
        start=tn.dt.datetime.fromisoformat(commit_params[0]['since']); end=tn.dt.datetime.fromisoformat(commit_params[0]['until'])
        self.assertEqual(tn.dt.timedelta(hours=24),end-start)
        runs_params=[params for path,params in gh.calls if path.endswith('/actions/runs')][0]
        self.assertEqual('work/website-v2',runs_params['branch'])
        self.assertIn('..',runs_params['created'])

    def test_failed_send_does_not_mark_digest_sent_and_first_send_creates_ledger(self):
        class GH:
            def get(self,path,params=None): return [] if path.endswith('/commits') else {'workflow_runs':[]}
            def file_at(self,path,ref): return '**Next:** APK' if path=='AGENT_HANDOFF.md' else None
        with tempfile.TemporaryDirectory() as folder:
            ledger=Path(folder)/'new'/'digest.txt'
            with mock.patch.dict(os.environ,{'GITHUB_REPOSITORY':'o/r','TELEGRAM_BOT_TOKEN':'TEST','TELEGRAM_CHAT_ID':'TEST'}), mock.patch.object(tn,'GitHub',return_value=GH()), mock.patch.object(tn,'send',side_effect=[RuntimeError('test'),42]) as sender, mock.patch('sys.stdout',io.StringIO()):
                argv=['digest','--branch','work/website-v2','--ledger',str(ledger)]
                self.assertEqual(1,tn.main(argv)); self.assertFalse(ledger.exists())
                self.assertEqual(0,tn.main(argv)); self.assertTrue(ledger.exists())
                self.assertEqual(0,tn.main(argv)); self.assertEqual(2,sender.call_count)

    def test_workflow_dry_run_and_default_branch_contract(self):
        root=Path(__file__).resolve().parents[2]
        workflow=(root/'.github/workflows/website-digest.yml').read_text()
        for fact in ["cron: '0 18 * * *'", 'dry_run:', 'default: true', "TELEGRAM_MESSAGE_THREAD_ID: '6'", 'ref: ${{ github.sha }}', 'contents: read', 'actions: read', '--dry-run']:
            self.assertIn(fact,workflow)
        self.assertNotIn('pages: write',workflow)
