import io, json, os, sys, tempfile, unittest, urllib.error
from unittest import mock
sys.path.insert(0, os.path.dirname(__file__))
import telegram_notify as tn


class FakeGitHub:
    def __init__(self, compare=None, files=None, fail_compare=False):
        self.compare, self.files, self.fail_compare = compare or {}, files or {}, fail_compare
    def compare_commits(self, base, head):
        if self.fail_compare: raise urllib.error.URLError("down")
        commits = self.compare.get((base, head), [])
        return commits, self.compare.get(("total", base, head), len(commits))
    def file_at(self, path, ref):
        return self.files.get((path, ref), self.files.get(ref))


def api_commit(sha, msg, author="Claude"):
    return {"sha": sha, "commit": {"message": msg, "author": {"name": author}}}


class EscapingTest(unittest.TestCase):
    def test_untrusted_text_is_escaped_and_message_preserved(self):
        msg = 'fix: <b>bold</b> & "quotes" $(rm -rf /) `id`\n\nbody line'
        text = tn.commit_message("o/r", "feat/<x>", "a" * 40, "Иван <ivan>", msg)
        self.assertIn("&lt;b&gt;bold&lt;/b&gt; &amp; \"quotes\" $(rm -rf /) `id`\n\nbody line", text)
        self.assertIn("<code>feat/&lt;x&gt;</code>", text)
        self.assertIn("Иван &lt;ivan&gt;", text)
        self.assertIn("Я ХУдЕЮ", text); self.assertIn("aaaaaaa", text)
        self.assertIn('href="https://github.com/o/r/commit/' + "a" * 40 + '"', text)
        for label in ("Проект:", "Автор:", "Ветка:", "Коммит:", "Сообщение:"):
            self.assertIn(label, text)

    def test_overlong_message_is_cut_within_limit_without_breaking_entities(self):
        text = tn.commit_message("o/r", "b", "c" * 40, "a", "&" * 5000)
        self.assertLessEqual(len(text), tn.TELEGRAM_LIMIT)
        self.assertIn("сообщение обрезано", text)
        body = text.split("<pre>")[1].split("\n…")[0]
        self.assertTrue(body.endswith("&amp;"), body[-10:])


class CommitListTest(unittest.TestCase):
    def test_existing_branch_uses_full_compare_in_chronological_order(self):
        ev = {"before": "b" * 40, "after": "e" * 40, "commits": [{"id": "x", "message": "only", "author": {"name": "n"}}]}
        gh = FakeGitHub({("b" * 40, "e" * 40): [api_commit("1" * 40, "first"), api_commit("2" * 40, "second")]})
        commits, warnings = tn.pushed_commits(ev, gh)
        self.assertEqual(["first", "second"], [c["message"] for c in commits]); self.assertEqual([], warnings)

    def test_truncated_compare_is_reported_not_silent(self):
        ev = {"before": "b" * 40, "after": "e" * 40, "commits": []}
        gh = FakeGitHub({("b" * 40, "e" * 40): [api_commit("1" * 40, "m")], ("total", "b" * 40, "e" * 40): 3})
        commits, warnings = tn.pushed_commits(ev, gh)
        self.assertEqual(1, len(commits)); self.assertIn("2 не перечислены", warnings[0])

    def test_api_failure_falls_back_to_payload_with_warning(self):
        ev = {"before": "b" * 40, "after": "e" * 40, "commits": [{"id": "1" * 40, "message": "a", "author": {"name": "n"}}, {"id": "2" * 40, "message": "b", "author": {"username": "u"}}]}
        commits, warnings = tn.pushed_commits(ev, FakeGitHub(fail_compare=True))
        self.assertEqual(["a", "b"], [c["message"] for c in commits]); self.assertEqual("u", commits[1]["author"]); self.assertTrue(warnings)

    def test_new_branch_uses_payload_and_branch_delete_sends_nothing(self):
        ev = {"before": tn.ZERO_SHA, "after": "e" * 40, "commits": [{"id": "1" * 40, "message": "a", "author": {"name": "n"}}]}
        self.assertEqual(1, len(tn.pushed_commits(ev, FakeGitHub())[0]))
        self.assertEqual(([], []), tn.pushed_commits({"before": "b" * 40, "after": tn.ZERO_SHA, "deleted": True}, FakeGitHub()))


class LedgerAndRunTest(unittest.TestCase):
    def test_rerun_skips_commits_already_sent(self):
        with tempfile.TemporaryDirectory() as d:
            event = os.path.join(d, "event.json"); ledger = os.path.join(d, "sent.txt")
            with open(event, "w") as f: json.dump({"before": "b" * 40, "after": "e" * 40, "commits": []}, f)
            with open(ledger, "w") as f: f.write(f"commit:main:{'1' * 40}\n")
            sent = []
            gh = FakeGitHub({("b" * 40, "e" * 40): [api_commit("1" * 40, "old"), api_commit("2" * 40, "new")]})
            envv = {"GITHUB_EVENT_PATH": event, "GITHUB_REPOSITORY": "o/r", "GITHUB_REF_NAME": "main", "TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}
            with mock.patch.dict(os.environ, envv), mock.patch.object(tn, "GitHub", return_value=gh), \
                 mock.patch.object(tn, "send", side_effect=lambda t, c, text: sent.append(text)):
                rc = tn.main(["commits", "--ledger", ledger])
            self.assertEqual(0, rc); self.assertEqual(1, len(sent)); self.assertIn("new", sent[0])
            with open(ledger) as f: self.assertIn(f"commit:main:{'2' * 40}", f.read())

    def test_telegram_failure_fails_the_job_and_hides_the_token(self):
        err = urllib.error.HTTPError("https://api.telegram.org/botSECRET/sendMessage", 401, "x", {}, io.BytesIO(b'{"ok":false,"description":"Unauthorized"}'))
        with mock.patch("urllib.request.urlopen", side_effect=err):
            with self.assertRaises(RuntimeError) as ctx:
                tn.send("SECRET", "chat", "hi")
        self.assertNotIn("SECRET", str(ctx.exception)); self.assertIn("401", str(ctx.exception))


class MultiCommitPushTest(unittest.TestCase):
    """Regression: every commit of a multi-commit push gets its own message; a failure loses nothing."""
    def run_push(self, d, commits, fail_on=(), ledger_name="sent.txt"):
        event = os.path.join(d, "event.json"); ledger = os.path.join(d, ledger_name)
        with open(event, "w") as f: json.dump({"before": "b" * 40, "after": "e" * 40, "commits": []}, f)
        gh = FakeGitHub({("b" * 40, "e" * 40): commits})
        sent = []
        def fake_send(t, c, text):
            if any(x in text for x in fail_on): raise RuntimeError("Telegram HTTP 502: Bad Gateway")
            sent.append(text); return len(sent)
        envv = {"GITHUB_EVENT_PATH": event, "GITHUB_REPOSITORY": "o/r", "GITHUB_REF_NAME": "w", "TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}
        out = io.StringIO()
        with mock.patch.dict(os.environ, envv), mock.patch.object(tn, "GitHub", return_value=gh), \
             mock.patch.object(tn, "send", side_effect=fake_send), mock.patch("sys.stdout", out):
            rc = tn.main(["commits", "--ledger", ledger])
        return rc, sent, out.getvalue()

    def test_each_commit_sent_once_in_order_and_identical_messages_are_not_merged(self):
        commits = [api_commit("1" * 40, "feat(G): share records"), api_commit("2" * 40, "same text"), api_commit("3" * 40, "same text")]
        with tempfile.TemporaryDirectory() as d:
            rc, sent, log = self.run_push(d, commits)
        self.assertEqual(0, rc); self.assertEqual(3, len(sent))
        for text, sha in zip(sent, ("1" * 40, "2" * 40, "3" * 40)):
            self.assertIn(f"<code>{sha}</code>", text)
        self.assertIn("message_id 3", log)

    def test_failure_of_one_commit_fails_job_keeps_others_and_rerun_sends_only_the_missing_one(self):
        commits = [api_commit("1" * 40, "first"), api_commit("2" * 40, "second"), api_commit("3" * 40, "third")]
        with tempfile.TemporaryDirectory() as d:
            rc, sent, log = self.run_push(d, commits, fail_on=("second",))
            self.assertEqual(1, rc); self.assertEqual(2, len(sent)); self.assertIn("::error::", log)
            rc2, sent2, _ = self.run_push(d, commits)        # re-run of the same run (same ledger)
        self.assertEqual(0, rc2); self.assertEqual(1, len(sent2)); self.assertIn("second", sent2[0])


def ev(i, typ="task_transition", source="Claude Code", **kw):
    e = {"id": i, "type": typ, "source": source,
         "from": {"path": ["Task03", "G"], "title": "Share Studio <2.0>"}, "to": {"path": ["Task03", "H", "H1"], "title": "Сравнение"},
         "verified": "JVM 856/0", "status": "разработка продолжается", "checkpoint": "abc1234"}
    e.update(kw); return e


def evfile(*events): return json.dumps({"events": list(events)})


class TransitionEventTest(unittest.TestCase):
    def test_transition_message_matches_the_requested_russian_format(self):
        text = tn.event_message("o/r", "w", "e" * 40, ev("e1"))
        self.assertTrue(text.startswith("<b>САЙТ «Я ХУдЕЮ»</b>")); self.assertIn("<b>Агент:</b> Claude Code",text); self.assertIn("переход к следующей задаче",text)
        self.assertIn("<b>Завершено:</b> Task03 › G — Share Studio &lt;2.0&gt;", text)
        self.assertIn("<b>Начато:</b> Task03 › H › H1 — Сравнение", text)
        self.assertIn("<b>Статус:</b> разработка продолжается", text)
        self.assertIn('<b>Последний checkpoint:</b> <a href="https://github.com/o/r/commit/abc1234">abc1234</a>', text)
        self.assertIn("событие <code>e1</code>", text)

    def test_every_type_and_any_nesting_depth(self):
        deep = {"path": ["ТЗ-09", "Этап 2", "Задача 4", "Подзадача 4.1", "Шаг"], "title": "x"}
        for typ, (heading, f, t, needs) in tn.EVENT_TYPES.items():
            e = {"id": typ, "type": typ, "source": "Codex", "verified": "ok", "from": deep, "to": deep}
            self.assertIsNone(tn.event_problem(e), typ)
            text = tn.event_message("o/r", "w", "e" * 40, e)
            self.assertIn(heading, text); self.assertIn("<b>Агент:</b> Codex", text); self.assertTrue(text.startswith("<b>САЙТ «Я ХУдЕЮ»</b>"))
            self.assertIn("ТЗ-09 › Этап 2 › Задача 4 › Подзадача 4.1 › Шаг — x", text)

    def test_completion_without_verification_and_malformed_events_are_never_sent(self):
        self.assertIsNotNone(tn.event_problem(ev("a", verified="")))
        self.assertIsNotNone(tn.event_problem(ev("b", typ="roadmap_completed", verified=" ")))
        self.assertIsNone(tn.event_problem(ev("c", typ="task_started", verified="")))
        self.assertIsNotNone(tn.event_problem(ev("d", typ="unknown")))
        self.assertIsNotNone(tn.event_problem(ev("e", checkpoint="$(id)")))
        self.assertIsNotNone(tn.event_problem({"id": "f", "type": "task_started", "to": {"path": [], "title": "x"}}))
        self.assertEqual([], tn.new_events(None, evfile(ev("g", verified=""))))

    def test_new_events_only_once_in_order_with_stable_ids(self):
        before = evfile(ev("1"))
        after = evfile(ev("1", status="изменено"), ev("2", typ="task_started"), ev("2", typ="task_started"), ev("3", typ="stage_completed"))
        self.assertEqual(["2", "3"], [e["id"] for e in tn.new_events(before, after)])
        self.assertEqual([], tn.new_events(after, after))                         # repeated push
        self.assertEqual([], tn.new_events(after, evfile(ev("3", typ="stage_completed"))))  # trimming old entries
        self.assertEqual(["1"], [e["id"] for e in tn.new_events(None, evfile(ev("1")))])  # file created in this push

    def test_run_sends_events_after_commits_and_rerun_or_second_agent_push_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            event = os.path.join(d, "event.json"); ledger = os.path.join(d, "sent.txt")
            with open(event, "w") as f: json.dump({"before": "b" * 40, "after": "e" * 40, "commits": []}, f)
            claude = ev("c-1", typ="task_completed", to=None)
            codex = ev("x-1", typ="task_started", source="Codex", **{"from": None})
            gh = FakeGitHub({("b" * 40, "e" * 40): [api_commit("1" * 40, "work\n\nAgent: Codex")]},
                            {(tn.EVENTS_FILE, "b" * 40): evfile(), (tn.EVENTS_FILE, "e" * 40): evfile(claude, codex)})
            envv = {"GITHUB_EVENT_PATH": event, "GITHUB_REPOSITORY": "o/r", "GITHUB_REF_NAME": "w", "TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}
            for expected in (3, 0):  # first run: commit + 2 events; re-run of the same run: nothing
                sent = []
                with mock.patch.dict(os.environ, envv), mock.patch.object(tn, "GitHub", return_value=gh), \
                     mock.patch.object(tn, "send", side_effect=lambda t, c, text: sent.append(text) or len(sent)), mock.patch("sys.stdout", io.StringIO()):
                    self.assertEqual(0, tn.main(["commits", "--ledger", ledger]))
                self.assertEqual(expected, len(sent))
                if expected:
                    self.assertIn("Проверенный коммит", sent[0])
                    self.assertIn("задача завершена и проверена",sent[1]); self.assertIn("<b>Агент:</b> Claude Code",sent[1])  # explicit source wins
                    self.assertIn("<b>начата задача</b>",sent[2]); self.assertIn("<b>Агент:</b> Codex",sent[2])

    def test_add_event_cli_is_deterministic_validated_and_refuses_unverified_completion(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "events.json")
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(0, tn.main(["event", "--file", path, "--type", "stage_transition", "--source", "Codex", "--id", "s-1",
                                             "--from-path", "Task03 > G", "--from-title", "Share", "--to-path", "Task03 > H", "--to-title", "UX",
                                             "--verified", "JVM 856/0", "--checkpoint", "abc1234"]))
                self.assertEqual(1, tn.main(["event", "--file", path, "--type", "task_completed", "--source", "Codex",
                                             "--from-path", "A", "--from-title", "B"]))  # no --verified
                self.assertEqual(1, tn.main(["event", "--file", path, "--type", "task_started", "--source", "Codex", "--id", "s-1",
                                             "--to-path", "A", "--to-title", "B"]))  # duplicate id
                self.assertEqual(0, tn.main(["events", "--file", path]))
            with open(path, encoding="utf-8") as f: data = json.load(f)
            self.assertEqual(["s-1"], [e["id"] for e in data["events"]])
            self.assertEqual({"path": ["Task03", "G"], "title": "Share"}, data["events"][0]["from"])

    def test_repository_events_file_is_valid(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", tn.EVENTS_FILE)
        if not os.path.exists(path): self.skipTest("events file lives on the development branch")
        with mock.patch("sys.stdout", io.StringIO()):
            self.assertEqual(0, tn.main(["events", "--file", path]))


class SecretHandlingTest(unittest.TestCase):
    def test_surrounding_whitespace_in_secrets_is_trimmed(self):
        with mock.patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": " 123:ABC\n"}):
            self.assertEqual("123:ABC", tn.env("TELEGRAM_BOT_TOKEN"))

    def test_invalid_url_style_errors_never_include_the_request_path(self):
        import http.client
        with mock.patch("urllib.request.urlopen", side_effect=http.client.InvalidURL("URL can't contain control characters. '/botSECRET TOKEN/sendMessage'")):
            with self.assertRaises(RuntimeError) as ctx:
                tn.send("SECRET TOKEN", "chat", "hi")
        self.assertNotIn("SECRET", str(ctx.exception)); self.assertIn("InvalidURL", str(ctx.exception))


class MilestoneTest(unittest.TestCase):
    def reg(self, **st): return json.dumps({"milestones": [{"id": k, "title": k, "status": v} for k, v in st.items()]})
    def test_only_new_completion_statuses_and_no_baseline_means_nothing(self):
        self.assertEqual([], tn.milestone_transitions(None, self.reg(a="fully_verified")))
        got = tn.milestone_transitions(self.reg(a="in_progress", b="software_complete", c="queued"),
                                       self.reg(a="software_complete", b="software_complete", c="in_progress"))
        self.assertEqual(["a"], [m["id"] for m in got])
        got = tn.milestone_transitions(self.reg(a="software_complete"), self.reg(a="fully_verified"))
        self.assertEqual("fully_verified", got[0]["status"])
        self.assertIn("полностью проверен", tn.milestone_message("o/r", "b", "f" * 40, got[0]))
        self.assertEqual([], tn.milestone_transitions("not json", self.reg(a="fully_verified")))



def alert(i="tok", status="open", **kw):
    a = {"id": i, "status": status, "task": "Telegram", "subtask": "Секрет <bot>", "what": "InvalidURL & co",
         "steps": ["Откройте Settings", "Сохраните `$(id)`"], "blocked": "уведомления", "can_continue": "да",
         "link": "https://github.com/o/r/actions/runs/1"}
    a.update(kw); return json.dumps({"alerts": [a]})


class UserActionTest(unittest.TestCase):
    def test_message_has_all_required_sections_escaped(self):
        text = tn.action_message("o/r", "b", "a" * 40, json.loads(alert())["alerts"][0])
        self.assertTrue(text.startswith("🚨 <b>ТРЕБУЕТСЯ ВАШЕ ДЕЙСТВИЕ</b>"))
        for label in ("Задача:", "Подзадача:", "Что произошло:", "Что нужно сделать:", "Что заблокировано:", "Можно ли продолжать другие задачи:"):
            self.assertIn(label, text)
        self.assertIn("Секрет &lt;bot&gt;", text); self.assertIn("InvalidURL &amp; co", text)
        self.assertIn("1. Откройте Settings\n2. Сохраните `$(id)`", text)
        self.assertIn('href="https://github.com/o/r/actions/runs/1"', text)
        self.assertNotIn("javascript", tn.action_message("o/r", "b", "a" * 40, json.loads(alert(link="javascript:x"))["alerts"][0]))

    def test_fires_once_on_open_and_once_on_resolve(self):
        self.assertEqual(1, len(tn.action_transitions(None, alert())[0]))           # registry created with an open alert
        self.assertEqual(([], []), tn.action_transitions(alert(), alert(what="обновлено")))  # still open → no duplicate
        opened, resolved = tn.action_transitions(alert(), alert(status="resolved"))
        self.assertEqual([], opened); self.assertEqual(1, len(resolved))
        self.assertEqual(([], []), tn.action_transitions(None, alert(status="resolved")))
        self.assertEqual(([], []), tn.action_transitions(None, '{"alerts": [{"id": "x", "status": "open"}]}'))  # incomplete → ignored
        self.assertEqual(([], []), tn.action_transitions(None, "not json"))

    def test_run_sends_alert_first_and_rerun_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            event = os.path.join(d, "event.json"); ledger = os.path.join(d, "sent.txt")
            with open(event, "w") as f: json.dump({"before": "b" * 40, "after": "e" * 40, "commits": []}, f)
            gh = FakeGitHub({("b" * 40, "e" * 40): [api_commit("1" * 40, "alert commit")]},
                            {(tn.ACTIONS_FILE, "b" * 40): None, (tn.ACTIONS_FILE, "e" * 40): alert()})
            envv = {"GITHUB_EVENT_PATH": event, "GITHUB_REPOSITORY": "o/r", "GITHUB_REF_NAME": "w", "TELEGRAM_BOT_TOKEN": "t", "TELEGRAM_CHAT_ID": "c"}
            for expected in (2, 0):
                sent = []
                with mock.patch.dict(os.environ, envv), mock.patch.object(tn, "GitHub", return_value=gh), \
                     mock.patch.object(tn, "send", side_effect=lambda t, c, text: sent.append(text)):
                    self.assertEqual(0, tn.main(["commits", "--ledger", ledger]))
                self.assertEqual(expected, len(sent))
                if expected:
                    self.assertIn("ТРЕБУЕТСЯ ВАШЕ ДЕЙСТВИЕ", sent[0]); self.assertIn("Проверенный коммит", sent[1])

    def test_repository_registry_is_valid(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", tn.ACTIONS_FILE)
        if not os.path.exists(path): self.skipTest("registry lives on the development branch")
        with mock.patch("sys.stdout", io.StringIO()):
            self.assertEqual(0, tn.main(["actions", "--file", path]))


class AgentSourceTest(unittest.TestCase):
    def test_source_comes_from_trailers_and_never_echoes_untrusted_text(self):
        self.assertEqual("Claude Code", tn.agent_source("fix\n\nAgent: Claude Code"))
        self.assertEqual("Codex", tn.agent_source("fix\n\nAgent: Codex"))
        self.assertEqual("Codex", tn.agent_source("fix\n\nagent: codex (cloud)"))
        self.assertEqual("Claude Code", tn.agent_source("fix\n\nCo-Authored-By: Claude Opus <noreply@anthropic.com>"))
        self.assertEqual("Claude Code", tn.agent_source("fix\n\nClaude-Session: https://claude.ai/code/x"))
        self.assertEqual(tn.SOURCE_UNKNOWN, tn.agent_source("fix", author="codex-bot"))
        self.assertEqual(tn.SOURCE_UNKNOWN, tn.agent_source("fix\n\nAgent: <b>evil</b>"))
        self.assertEqual(tn.SOURCE_UNKNOWN, tn.agent_source("manual fix", author="Sasha"))
        # An explicit Agent trailer wins over a co-author line.
        self.assertEqual("Codex", tn.agent_source("x\n\nAgent: Codex\nCo-Authored-By: Claude <c>"))

    def test_every_message_kind_names_its_source(self):
        self.assertIn("<b>Источник:</b> Codex", tn.commit_message("o/r", "b", "a" * 40, "n", "m\n\nAgent: Codex"))
        self.assertIn("<b>Источник:</b> GitHub Actions", tn.ci_message("o/r", "CI", "b", "a" * 40, "failure", "https://x", None))
        a = json.loads(alert())["alerts"][0]
        self.assertIn("<b>Источник:</b> Claude Code", tn.action_message("o/r", "b", "a" * 40, a, source=tn.SOURCE_CLAUDE))
        self.assertIn("<b>Источник:</b> Codex", tn.action_message("o/r", "b", "a" * 40, dict(a, source="Codex"), source=tn.SOURCE_CLAUDE))
        self.assertIn("<b>Источник:</b> Codex", tn.resolved_message("b", dict(a, source="codex")))
        self.assertIn("источник: GitHub Actions", tn.digest_message("o/r", tn.dt.datetime(2026, 10, 18, tzinfo=tn.dt.timezone.utc), {}, [], [], None, None, []))


class AgentEventTest(unittest.TestCase):
    def test_interruption_handoff_resume_headings_only_from_fixed_values(self):
        self.assertTrue(tn.commit_message("o/r", "b", "a" * 40, "n", "x\n\nAgent-Event: handoff\nAgent: Codex").startswith("<b>🔁 Передача работы"))
        self.assertTrue(tn.commit_message("o/r", "b", "a" * 40, "n", "x\n\nAgent-Event: interruption").startswith("<b>⏸️"))
        self.assertTrue(tn.commit_message("o/r", "b", "a" * 40, "n", "x\n\nAgent-Event: <b>x</b>").startswith("<b>Проверенный коммит</b>"))


class DigestSourceTest(unittest.TestCase):
    def test_handoff_and_alerts_come_from_newest_branch_that_has_them_not_from_main(self):
        class GH:
            def get(self, path, params=None):
                if path.endswith("/branches"): return [{"name": "main"}, {"name": "work"}]
                if path.endswith("/commits"):
                    at = {"main": "2026-10-18T05:00:00Z", "work": "2026-10-18T04:00:00Z"}[params["sha"]]
                    return [{"sha": params["sha"] + "-head", "commit": {"committer": {"date": at}}, "parents": [{"sha": "p"}]}]
                return {"workflow_runs": []}
            def file_at(self, path, ref):
                if ref == "work" and path == "AGENT_HANDOFF.md": return "**Next:** G3"
                if ref == "work" and path == tn.ACTIONS_FILE: return alert()
                return None
        out = io.StringIO()
        with mock.patch.dict(os.environ, {"GITHUB_REPOSITORY": "o/r"}), mock.patch.object(tn, "GitHub", return_value=GH()), mock.patch("sys.stdout", out):
            self.assertEqual(0, tn.main(["digest", "--dry-run"]))
        text = out.getvalue()
        self.assertIn("• G3 (<code>work</code>)", text)
        self.assertIn("Ждут вашего действия", text); self.assertIn("Секрет &lt;bot&gt;", text)
        self.assertNotIn("Нет данных", text)


class CiAndDigestTest(unittest.TestCase):
    def test_junit_counts_only_from_real_reports(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertIsNone(tn.junit_counts(os.path.join(d, "*.xml")))
            open(os.path.join(d, "a.xml"), "w").write('<testsuite tests="5" failures="1" errors="1" skipped="1"/>')
            open(os.path.join(d, "b.xml"), "w").write('<testsuites><testsuite tests="3" failures="0" errors="0" skipped="0"/></testsuites>')
            self.assertEqual({"files": 2, "passed": 5, "failed": 2, "skipped": 1}, tn.junit_counts(os.path.join(d, "*.xml")))
            open(os.path.join(d, "c.xml"), "w").write('<broken')
            self.assertIsNone(tn.junit_counts(os.path.join(d, "*.xml")))
        text = tn.ci_message("o/r", "CI", "b", "a" * 40, "failure", "https://x/run", None)
        self.assertIn("не найдены", text); self.assertIn("не прошла", text)

    def test_digest_distinguishes_facts_from_missing_data(self):
        import datetime as dt
        now = dt.datetime(2026, 10, 18, 18, 0, tzinfo=dt.timezone.utc)
        text = tn.digest_message("o/r", now, {"work/<x>": 3}, [], [], None, None, ["HANDOFF.md"])
        self.assertIn("21:00 МСК", text); self.assertIn("work/&lt;x&gt;</code>: 3", text)
        self.assertIn("нет записанных завершений", text); self.assertIn("не удалось определить", text); self.assertIn("Нет данных:</b> HANDOFF.md", text)
        self.assertEqual("F5", tn.next_action("x\n**Next:** F5\n**Next:** old"))


class WebsiteContractTest(unittest.TestCase):
    def test_reliable_other_agent_label(self):
        self.assertEqual(tn.SOURCE_OTHER, tn.agent_source("fix\n\nAgent: Other agent"))
        self.assertEqual(tn.SOURCE_UNKNOWN, tn.agent_source("fix", "codex-user"))

    def test_stage_report_has_site_agent_evidence_and_next(self):
        event={"id":"test-stage", "type":"stage_completed", "source":"Codex", "from":{"path":["Сайт","QA"],"title":"QA"},"verified":"tests PASS","done":"Gallery keyboard fixed","next":"Owner release choice"}
        text=tn.event_message("o/r","work/website-v2","a"*40,event)
        for word in ["САЙТ «Я ХУдЕЮ»", "Агент:", "Проверено:", "Сделано:", "Далее:", "Owner release choice"]:
            self.assertIn(word,text)

    def test_ci_failure_rerun_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger=os.path.join(folder,"sent.txt")
            variables={"GITHUB_REPOSITORY":"o/r", "GITHUB_RUN_ID":"123", "TELEGRAM_BOT_TOKEN":"fake-test-only", "TELEGRAM_CHAT_ID":"fake-test-only"}
            with mock.patch.dict(os.environ,variables), mock.patch.object(tn,"send") as send, mock.patch("sys.stdout",io.StringIO()):
                for _ in range(2): self.assertEqual(0,tn.main(["ci-report","--workflow","website","--status","failure","--ledger",ledger]))
            self.assertEqual(send.call_count,1)


class AutonomousDigestTest(unittest.TestCase):
    def test_config_probe_reports_names_without_values(self):
        output=io.StringIO()
        with mock.patch.dict(os.environ,{},clear=True),mock.patch("sys.stdout",output):
            self.assertEqual(1,tn.main(["check-config"]))
        self.assertIn("Missing Telegram binding",output.getvalue())
        output=io.StringIO()
        with mock.patch.dict(os.environ,{"TELEGRAM_BOT_TOKEN":"sensitive-test-value", "TELEGRAM_CHAT_ID":"private-test-id"},clear=True),mock.patch("sys.stdout",output):
            self.assertEqual(0,tn.main(["check-config"]))
        self.assertNotIn("sensitive-test-value",output.getvalue());self.assertNotIn("private-test-id",output.getvalue())

    def test_digest_completion_uses_verified_shared_events_only(self):
        since=tn.dt.datetime(2026,10,17,18,tzinfo=tn.dt.timezone.utc);now=since+tn.dt.timedelta(days=1)
        recent=ev("recent",typ="stage_completed",at="2026-10-18T10:00:00Z")
        old=ev("old",at="2026-10-10T10:00:00Z")
        no_proof=ev("no-proof",at="2026-10-18T10:00:00Z",verified="")
        future=ev("future",at="2026-10-20T10:00:00Z")
        malformed=ev("bad-time",at="invalid")
        result=tn.completed_events_since(evfile(recent,old,no_proof,future,malformed),since,now)
        self.assertEqual(["recent"],[x["id"] for x in result])

    def test_quiet_branch_still_reports_handoff_and_daily_rerun_sends_once(self):
        class GH:
            def get(self,path,params=None):return [] if path.endswith("/commits") else {"workflow_runs":[]}
            def file_at(self,path,ref):
                if path=="AGENT_HANDOFF.md":return "**Next:** Continue browser QA"
                if path==tn.ACTIONS_FILE:return alert()
                return None
        with tempfile.TemporaryDirectory() as folder:
            ledger=os.path.join(folder,"digest.txt");output=io.StringIO()
            variables={"GITHUB_REPOSITORY":"o/r", "TELEGRAM_BOT_TOKEN":"test-only", "TELEGRAM_CHAT_ID":"test-only"}
            with mock.patch.dict(os.environ,variables),mock.patch.object(tn,"GitHub",return_value=GH()),mock.patch.object(tn,"send") as send,mock.patch("sys.stdout",output):
                for _ in range(2):self.assertEqual(0,tn.main(["digest","--branch","work/website-v2","--ledger",ledger]))
            self.assertEqual(1,send.call_count);text=send.call_args.args[2]
            self.assertIn("Continue browser QA",text);self.assertIn("Ждут вашего действия",text)


if __name__ == "__main__":
    unittest.main()
