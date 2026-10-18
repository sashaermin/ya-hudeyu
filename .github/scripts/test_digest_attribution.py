"""Factual contributors for the same unique 24h commit scope as the digest."""
import io
import json
import os
import unittest
from unittest import mock
import telegram_notify as tn


class DigestAttributionTests(unittest.TestCase):
    def render(self, messages):
        counts = {}
        for message in messages:
            source = tn.agent_source(message)
            counts[source] = counts.get(source, 0) + 1
        return tn.digest_message('o/r', tn.dt.datetime.now(tn.dt.timezone.utc), {'work':len(messages)}, [], [], 'Ожидается APK', 'work', [], agent_counts=counts)

    def test_single_codex(self):
        self.assertIn('<b>Агент:</b> Codex', self.render(['change\n\nAgent: Codex']))

    def test_single_claude(self):
        self.assertIn('<b>Агент:</b> Claude Code', self.render(['change\n\nAgent: Claude Code']))

    def test_multiple_known_agents(self):
        text=self.render(['change\n\nAgent: Codex', 'change\n\nAgent: Claude Code'])
        self.assertIn('<b>Агенты:</b> Codex, Claude Code',text)
        self.assertIn('<b>Механизм:</b> GitHub Actions',text)

    def test_partial_attribution(self):
        text=self.render(['change\n\nAgent: Codex','unsigned change'])
        self.assertIn('<b>Агент:</b> Codex; частичная атрибуция: без надёжной подписи 1 из 2 коммитов',text)

    def test_unknown_and_conflicting_trailers(self):
        text=self.render(['change','change\n\nAgent: Codex\nAgent: Claude Code','change\n\nAgent: GitHub Actions'])
        self.assertIn('<b>Агент:</b> Не определён',text)

    def test_no_commits(self):
        self.assertIn('<b>Агенты:</b> Нет данных',self.render([]))

    def test_no_commits_without_explicit_counts(self):
        text=tn.digest_message('o/r',tn.dt.datetime.now(tn.dt.timezone.utc),{},[],[],None,None,[])
        self.assertIn('<b>Агенты:</b> Нет данных',text)

    def test_existing_alias_and_normalization_rules(self):
        self.assertIn('<b>Агент:</b> Claude Code',self.render(['change\n\nAgent: claude code']))
        self.assertIn('<b>Агент:</b> Разработчик',self.render(['change\n\nAgent: Other agent']))

    def test_unique_scope_closed_actions_and_no_author_or_runner_heuristics(self):
        class GH:
            def __init__(self): self.params=[]
            def get(self,path,params=None):
                self.params.append(params)
                if path.endswith('/branches'): return [{'name':'main'},{'name':'work/website-v2'}]
                if not path.endswith('/commits'): return {'workflow_runs':[]}
                def c(sha,message):
                    return {'sha':sha*40,'author':{'login':'codex'},'commit':{'message':message,'author':{'name':'Claude Code'},'committer':{'date':'2026-10-18T15:00:00Z','name':'GitHub Actions'}}}
                common=c('a','Verified change\n\nAgent: Codex')
                return [common] if params['sha']=='main' else [common,c('b','codex: unsigned change')]
            def file_at(self,path,ref):
                if path=='AGENT_HANDOFF.md': return '**Exact next:** Текущий этап'
                if path==tn.ACTIONS_FILE:
                    alerts=[dict(id='digest-activation',status='resolved',source='Codex',task='Telegram',subtask='Устаревший запрос активации',what='Готово',steps=['Готово'],blocked='Нет',can_continue='Да',resolution='Включено'),dict(id='apk',status='open',source='Codex',task='APK',subtask='Нужен APK',what='Нет APK',steps=['Выбрать'],blocked='Нет артефакта',can_continue='Да')]
                    return json.dumps({'alerts':alerts})
                return None
        gh=GH();out=io.StringIO()
        with mock.patch.dict(os.environ,{'GITHUB_REPOSITORY':'o/r','GITHUB_ACTOR':'codex','GITHUB_WORKFLOW':'Claude Code'},clear=True),mock.patch.object(tn,'GitHub',return_value=gh),mock.patch.object(tn,'send') as sender,mock.patch('sys.stdout',out):
            self.assertEqual(0,tn.main(['digest','--dry-run']))
        sender.assert_not_called();text=out.getvalue()
        self.assertIn('без надёжной подписи 1 из 2 коммитов',text)
        self.assertIn('<code>main</code>: 1',text)
        self.assertIn('<code>work/website-v2</code>: 1',text)
        self.assertEqual(1,text.count('https://github.com/o/r/commit/'+'a'*40))
        self.assertNotIn('Агенты:</b> Codex, Claude Code',text)
        self.assertNotIn('Устаревший запрос активации',text)
        self.assertIn('Нужен APK',text)
        for params in [p for p in gh.params if p and 'since' in p]:
            self.assertEqual(tn.dt.timedelta(hours=24),tn.dt.datetime.fromisoformat(params['until'])-tn.dt.datetime.fromisoformat(params['since']))
