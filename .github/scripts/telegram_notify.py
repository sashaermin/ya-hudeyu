#!/usr/bin/env python3
"""Telegram notifications for «Я ХУдЕЮ» (GitHub Actions only; stdlib only).

Subcommands:
  commits    one message per pushed commit (+ USER ACTION REQUIRED alerts and roadmap milestone
             transitions recorded in the same push; alerts are sent first)
  ci-report  CI job result and JUnit test counts from real XML files (used by the composite action)
  digest     daily summary for the last 24 hours
  actions    validate project_specs/user_actions.json locally and preview open alerts (no network)
  event      append one task/stage transition event to project_specs/agent_events.json (no network)
  events     validate project_specs/agent_events.json and preview the messages (no network)

Untrusted text (commit messages, author names, branch names) is only ever passed through
html.escape and the Telegram JSON body — never through a shell. Secrets are read from the
environment and never printed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import sys
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

PROJECT = "САЙТ «Я ХУдЕЮ»"
TELEGRAM_LIMIT = 4096
ZERO_SHA = "0" * 40
MILESTONE_FILE = "project_specs/roadmap_milestones.json"
ACTIONS_FILE = "project_specs/user_actions.json"
EVENTS_FILE = "project_specs/agent_events.json"
ACTION_FIELDS = ("id", "status", "task", "subtask", "what", "steps", "blocked", "can_continue")
STATUS_TITLES = {
    "checkpoint_verified": "проверено в указанном объёме",
    "software_complete": "завершён программно (проверки на устройстве не завершены)",
    "hardware_pending": "завершён, ожидает проверки на реальном устройстве",
    "fully_verified": "полностью проверен",
}


def esc(text: str) -> str:
    return html.escape(text or "", quote=False)


# ---------------------------------------------------------------- GitHub API

class GitHub:
    def __init__(self, repo: str, token: str | None, api: str = "https://api.github.com"):
        self.repo, self.token, self.api = repo, token, api.rstrip("/")

    def get(self, path: str, params: dict | None = None):
        url = f"{self.api}{path}" + (("?" + urllib.parse.urlencode(params)) if params else "")
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def compare_commits(self, base: str, head: str) -> tuple[list[dict], int]:
        """Commits in head not in base, oldest first, all pages; returns (commits, total reported)."""
        commits: list[dict] = []
        total = 0
        page = 1
        while True:
            data = self.get(f"/repos/{self.repo}/compare/{base}...{head}", {"per_page": 100, "page": page})
            total = int(data.get("total_commits", 0))
            batch = data.get("commits", [])
            commits.extend(batch)
            if not batch or len(commits) >= total or page >= 50:
                break
            page += 1
        return commits, total

    def file_at(self, path: str, ref: str) -> str | None:
        try:
            data = self.get(f"/repos/{self.repo}/contents/{urllib.parse.quote(path)}", {"ref": ref})
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
        import base64
        return base64.b64decode(data.get("content", "")).decode("utf-8")


# ---------------------------------------------------------------- Telegram

def send(token: str, chat_id: str, text: str, retries: int = 3) -> int | None:
    """Sends one message; returns Telegram's message_id (logged so a delivery can be located in the chat)."""
    body = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
                if payload.get("ok"):
                    return (payload.get("result") or {}).get("message_id")
                raise RuntimeError(f"Telegram ответил ok=false: {payload.get('description', 'без описания')}")
        except urllib.error.HTTPError as e:
            # Never print the URL: it contains the bot token.
            try:
                detail = json.loads(e.read().decode("utf-8"))
            except Exception:
                detail = {}
            retry_after = (detail.get("parameters") or {}).get("retry_after")
            msg = f"Telegram HTTP {e.code}: {detail.get('description', 'без описания')}"
            if e.code == 429 and retry_after and attempt < retries:
                time.sleep(min(int(retry_after), 30)); continue
            if 500 <= e.code < 600 and attempt < retries:
                time.sleep(2 * attempt); continue
            raise RuntimeError(msg) from None
        except urllib.error.URLError as e:
            if attempt < retries:
                time.sleep(2 * attempt); continue
            raise RuntimeError(f"Telegram недоступен: {type(e.reason).__name__}") from None
        except RuntimeError:
            raise
        except Exception as e:
            # e.g. http.client.InvalidURL: its text would contain the request path with the token.
            raise RuntimeError(f"Ошибка запроса к Telegram: {type(e).__name__} (проверьте секреты: лишние пробелы/переводы строк)") from None


def fit(text: str, limit: int = TELEGRAM_LIMIT) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


# ---------------------------------------------------------------- source

SOURCE_CLAUDE, SOURCE_CODEX, SOURCE_ACTIONS = "Claude Code", "Codex", "GitHub Actions"
SOURCE_UNKNOWN = "Не определён"
SOURCE_OTHER = "Разработчик"


def trailers(message: str) -> dict[str, list[str]]:
    """Only the final contiguous trailer block is explicit provenance/report metadata."""
    result = {}
    for line in reversed((message or "").rstrip().splitlines()):
        match = re.fullmatch(r"([A-Za-z][A-Za-z-]*):[ \t]*(.*)", line)
        if not match:
            break
        result.setdefault(match[1].lower(), []).append(match[2].strip())
    return result


def normalized_agent(value: str) -> str:
    # Legacy values are input aliases only. Never infer identity from a prefix/author/runner.
    labels = {"claude code": SOURCE_CLAUDE, "codex": SOURCE_CODEX,
              "разработчик": SOURCE_OTHER, "не определён": SOURCE_UNKNOWN,
              "other agent": SOURCE_OTHER, "unknown": SOURCE_UNKNOWN}
    return labels.get(str(value).strip().casefold(), SOURCE_UNKNOWN)


def agent_source(message: str, author: str = "") -> str:
    values = trailers(message).get("agent", [])
    if len(set(values)) != 1:
        return SOURCE_UNKNOWN
    return normalized_agent(values[0])


def report_field(message: str, key: str, fallback: str, limit: int) -> str:
    values = trailers(message).get(key, [])
    text = values[0] if len(values) == 1 else fallback
    if not re.search(r"[А-Яа-яЁё]", text):
        text = fallback
    # Bound the escaped size, cutting only between whole source characters/entities.
    size, output = 0, []
    for character in text:
        cost = len(esc(character))
        if size + cost > limit - 1:
            return "".join(output) + "…"
        output.append(character); size += cost
    return text


AGENT_EVENTS = {
    "interruption": "⏸️ Работа остановлена (контрольная точка)",
    "handoff": "🔁 Передача работы другому агенту",
    "resume": "▶️ Работа возобновлена",
}


def agent_event(message: str) -> str | None:
    """`Agent-Event: interruption|handoff|resume` trailer → fixed heading (unknown values are ignored)."""
    values = trailers(message).get("agent-event", [])
    return AGENT_EVENTS.get(values[0].lower()) if len(values) == 1 else None


def alert_source(a: dict, fallback: str = SOURCE_UNKNOWN) -> str:
    # A later commit's agent does not prove who implemented a historical event/action.
    return normalized_agent(a.get("source", ""))


# ---------------------------------------------------------------- commits

def commit_message(repo: str, branch: str, sha: str, author: str, message: str, server: str = "https://github.com", workflow_verified: bool = False) -> str:
    url = f"{server}/{repo}/commit/{sha}"
    subject = (message or "").splitlines()[0] if message else ""
    fallback = subject if re.search(r"[А-Яа-яЁё]", subject) else "Обновление рабочей ветки сайта"
    summary = report_field(message, "report-summary", fallback, 220)
    done = report_field(message, "report-done", "Описание изменений не задано по протоколу; полный diff доступен по ссылке.", 800)
    checks = report_field(message, "report-checks", "Результаты локальных проверок не указаны.", 700)
    checks = ("Проверки workflow для этого коммита завершились успешно. Локальная запись: " if workflow_verified else "По записи автора; независимо этим уведомлением не подтверждено: ") + checks
    lines = [f"<b>{esc(PROJECT)} — новый коммит</b>",
             f"<b>Изменение:</b> {esc(summary)}", f"<b>Что сделано:</b> {esc(done)}",
             f"<b>Проверки:</b> {esc(checks)}", f"<b>Агент:</b> {esc(agent_source(message))}",
             f"<b>Ветка:</b> <code>{esc(branch)}</code>", f"<b>Коммит:</b> <code>{esc(sha[:7])}</code>"]
    event = agent_event(message)
    if event:
        lines.append(f"<b>Событие:</b> {esc(event)}")
    lines.append(f'<a href="{esc(url)}">{esc(url)}</a>')
    return "\n".join(lines)


def pushed_commits(event: dict, gh: GitHub) -> tuple[list[dict], list[str]]:
    """Commits of this push in chronological order and warnings about anything not listed."""
    before, after = event.get("before", ZERO_SHA), event.get("after", ZERO_SHA)
    warnings: list[str] = []
    if event.get("deleted") or after == ZERO_SHA:
        return [], []
    listed = [c for c in event.get("commits", []) if c.get("id")]
    norm = [{"sha": c["id"], "author": (c.get("author") or {}).get("name") or (c.get("author") or {}).get("username") or "неизвестен",
             "message": c.get("message", "")} for c in listed]
    if before != ZERO_SHA:
        try:
            raw, total = gh.compare_commits(before, after)
            full = [{"sha": c["sha"], "author": ((c.get("commit") or {}).get("author") or {}).get("name") or "неизвестен",
                     "message": (c.get("commit") or {}).get("message", "")} for c in raw]
            if total > len(full):
                warnings.append(f"GitHub сообщил о {total} коммитах, получено {len(full)}; {total - len(full)} не перечислены.")
            return full, warnings
        except Exception as e:  # fall back to the payload, but never silently
            warnings.append(f"Не удалось получить полный список коммитов через API ({type(e).__name__}); использованы данные события.")
    if len(listed) >= 20 and before == ZERO_SHA:
        warnings.append("Новая ветка: список коммитов события может быть усечён GitHub; перечислены только переданные коммиты.")
    return norm, warnings


# ---------------------------------------------------------------- milestones

def milestone_transitions(before_json: str | None, after_json: str | None) -> list[dict]:
    """Newly reached completion statuses. No baseline (file absent before) → nothing (idempotent)."""
    if before_json is None or after_json is None:
        return []
    try:
        old = {m["id"]: m for m in json.loads(before_json).get("milestones", [])}
        new = json.loads(after_json).get("milestones", [])
    except (ValueError, KeyError, AttributeError):
        return []
    out = []
    for m in new:
        status = m.get("status")
        if status in STATUS_TITLES and old.get(m.get("id"), {}).get("status") != status:
            out.append(m)
    return out


def milestone_message(repo: str, branch: str, sha: str, m: dict, server: str = "https://github.com") -> str:
    url = f"{server}/{repo}/commit/{sha}"
    lines = [f"<b>🏁 Этап дорожной карты</b>", f"<b>Проект:</b> {esc(PROJECT)}", f"<b>Агент:</b> {esc(normalized_agent(m.get('_source', '')))}",
             f"<b>Этап:</b> {esc(m.get('title', m.get('id', '')))}",
             f"<b>Статус:</b> {esc(STATUS_TITLES[m['status']])}", f"<b>Ветка:</b> <code>{esc(branch)}</code>"]
    if m.get("note"):
        lines.append(f"<b>Примечание:</b> {esc(m['note'])}")
    lines.append(f"<a href=\"{esc(url)}\">Коммит {esc(sha[:7])}</a>")
    return fit("\n".join(lines))


# ---------------------------------------------------------------- CI report

def junit_counts(pattern: str) -> dict | None:
    files = sorted(set(glob.glob(pattern, recursive=True)))
    if not files:
        return None
    total = failed = skipped = 0
    for f in files:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError:
            return None  # unreliable → report nothing rather than wrong numbers
        suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
        for s in suites:
            total += int(s.get("tests", 0)); failed += int(s.get("failures", 0)) + int(s.get("errors", 0)); skipped += int(s.get("skipped", 0))
    return {"files": len(files), "passed": total - failed - skipped, "failed": failed, "skipped": skipped}


def ci_message(repo: str, workflow: str, branch: str, sha: str, status: str, run_url: str, counts: dict | None) -> str:
    ok = status == "success"
    lines = [f"<b>{esc(PROJECT)} — {'сборка успешна' if ok else 'сборка не прошла'}</b>", f"<b>Проект:</b> {esc(PROJECT)}",
             f"<b>Агент:</b> {SOURCE_UNKNOWN}", f"<b>Механизм:</b> {SOURCE_ACTIONS}", f"<b>Workflow:</b> {esc(workflow)}", f"<b>Ветка:</b> <code>{esc(branch)}</code>",
             f"<b>Коммит:</b> <code>{esc(sha[:7])}</code>", f"<b>Статус:</b> {esc({'success': 'успех', 'failure': 'ошибка', 'cancelled': 'отменено', 'timed_out': 'превышено время'}.get(status, 'не подтверждён'))}"]
    if counts is not None:
        lines.append(f"<b>Тесты (JUnit, {counts['files']} файлов):</b> пройдено {counts['passed']}, упало {counts['failed']}, пропущено {counts['skipped']}")
    else:
        lines.append("<b>Тесты:</b> отчёты JUnit не найдены — количество не сообщается")
    lines.append(f"<a href=\"{esc(run_url)}\">Открыть запуск</a>")
    return fit("\n".join(lines))


# ---------------------------------------------------------------- digest

# ---------------------------------------------------------------- user action alerts

def load_actions(text: str | None) -> dict[str, dict]:
    """Valid alerts by id. Malformed file/entries are ignored (never alert on garbage)."""
    if text is None:
        return {}
    try:
        items = json.loads(text).get("alerts", [])
    except (ValueError, AttributeError):
        return {}
    out = {}
    for a in items if isinstance(items, list) else []:
        if isinstance(a, dict) and all(a.get(k) for k in ACTION_FIELDS) and isinstance(a["steps"], list):
            out[str(a["id"])] = a
    return out


def action_transitions(before_json: str | None, after_json: str | None) -> tuple[list[dict], list[dict]]:
    """(newly opened, newly resolved). An alert fires once when it becomes `open`; a still-open alert is never resent."""
    old, new = load_actions(before_json), load_actions(after_json)
    opened = [a for i, a in new.items() if a["status"] == "open" and old.get(i, {}).get("status") != "open"]
    resolved = [a for i, a in new.items() if a["status"] == "resolved" and old.get(i, {}).get("status") == "open"]
    return opened, resolved


def action_message(repo: str, branch: str, sha: str, a: dict, server: str = "https://github.com", source: str = SOURCE_UNKNOWN) -> str:
    lines = [f"<b>{esc(PROJECT)}</b>", "🚨 <b>ТРЕБУЕТСЯ ВАШЕ ДЕЙСТВИЕ</b>", f"<b>Проект:</b> {esc(PROJECT)}", f"<b>Агент:</b> {esc(alert_source(a, source))}",
             f"<b>Задача:</b> {esc(a['task'])}", f"<b>Подзадача:</b> {esc(a['subtask'])}", "",
             f"<b>Что произошло:</b>\n{esc(a['what'])}", "", "<b>Что нужно сделать:</b>"]
    lines += [f"{n}. {esc(str(step))}" for n, step in enumerate(a["steps"], 1)]
    lines += ["", f"<b>Что заблокировано:</b> {esc(a['blocked'])}",
              f"<b>Можно ли продолжать другие задачи:</b> {esc(a['can_continue'])}"]
    link = a.get("link") or ""
    if link.startswith("https://"):
        lines.append(f"<a href=\"{esc(link)}\">Ссылка на GitHub</a>")
    lines.append(f"<i>Ветка <code>{esc(branch)}</code>, коммит <a href=\"{esc(f'{server}/{repo}/commit/{sha}')}\">{esc(sha[:7])}</a>; id: <code>{esc(a['id'])}</code></i>")
    return fit("\n".join(lines))


def resolved_message(branch: str, a: dict, source: str = SOURCE_UNKNOWN) -> str:
    return fit(f"<b>{esc(PROJECT)}</b> — действие больше не требуется\n<b>Агент:</b> {esc(alert_source(a, source))}\n<b>{esc(a['subtask'])}</b>"
               + (f"\n{esc(a['resolution'])}" if a.get("resolution") else "")
               + f"\n<i>id: <code>{esc(a['id'])}</code>, ветка <code>{esc(branch)}</code></i>")


# ---------------------------------------------------------------- task / roadmap transition events

# type → (heading after the source, label for `from`, label for `to`, whether `verified` is required)
EVENT_TYPES = {
    "task_started": ("начата задача", None, "Начато", False),
    "task_completed": ("задача завершена и проверена", "Завершено", None, True),
    "task_transition": ("переход к следующей задаче", "Завершено", "Начато", True),
    "preview_artifact_ready": ("архив для просмотра готов (не онлайн-превью)", "Артефакт", None, True),
    "stage_started": ("начат этап", None, "Начато", False),
    "stage_completed": ("этап завершён и проверен", "Завершено", None, True),
    "stage_transition": ("переход к следующему этапу", "Завершено", "Начато", True),
    "task_paused": ("задача приостановлена", "Задача", None, False),
    "task_blocked": ("задача заблокирована", "Задача", None, False),
    "task_resumed": ("работа возобновлена", None, "Задача", False),
    "roadmap_completed": ("дорожная карта / ТЗ завершены", "Завершено", None, True),
}
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")


def _node(n) -> dict | None:
    """{"path": ["Task03", "G", "G2"], "title": "…"} — any depth (roadmap → stage → task → subtask)."""
    if not isinstance(n, dict) or not isinstance(n.get("path"), list) or not n["path"] or not n.get("title"):
        return None
    return n if all(isinstance(x, str) and x.strip() for x in n["path"]) else None


def event_problem(e: dict) -> str | None:
    """Why an event is not sendable (None = valid)."""
    if not isinstance(e, dict) or not str(e.get("id", "")).strip():
        return "нет id"
    spec = EVENT_TYPES.get(e.get("type"))
    if spec is None:
        return f"неизвестный type {e.get('type')!r}"
    _, from_label, to_label, needs_verified = spec
    if from_label and not _node(e.get("from")):
        return "нужен from {path, title}"
    if to_label and not _node(e.get("to")):
        return "нужен to {path, title}"
    if needs_verified and not str(e.get("verified", "")).strip():
        return "завершение без verified (проверки) не отправляется"
    if e.get("checkpoint") and not SHA_RE.match(str(e["checkpoint"])):
        return "checkpoint должен быть SHA"
    if e.get("type") == "preview_artifact_ready":
        if not re.fullmatch(r"https://github\.com/sashaermin/ya-hudeyu/actions/runs/[0-9]+/artifacts/[0-9]+", str(e.get("artifact_url", ""))):
            return "нужна проверенная HTTPS-ссылка review artifact сайта на GitHub"
    return None


def load_events(text: str | None) -> list[dict]:
    if text is None:
        return []
    try:
        items = json.loads(text).get("events", [])
    except (ValueError, AttributeError):
        return []
    return [e for e in items if isinstance(e, dict)] if isinstance(items, list) else []


def new_events(before_json: str | None, after_json: str | None) -> list[dict]:
    """Valid events whose id is not in the previous state, in file (chronological) order. Ids are stable:
    re-pushes, rewording or trimming old entries never resend."""
    seen = {str(e.get("id")) for e in load_events(before_json)}
    out, ids = [], set()
    for e in load_events(after_json):
        i = str(e.get("id"))
        if i in seen or i in ids or event_problem(e):
            continue
        ids.add(i); out.append(e)
    return out


def _label(n: dict) -> str:
    return f"{' › '.join(n['path'])} — {n['title']}"


def event_message(repo: str, branch: str, sha: str, e: dict, server: str = "https://github.com", source: str = SOURCE_UNKNOWN) -> str:
    heading, from_label, to_label, _ = EVENT_TYPES[e["type"]]
    who = alert_source(e, source)
    lines = [f"<b>{esc(PROJECT)}</b>", f"<b>{esc(heading)}</b>", f"<b>Агент:</b> {esc(who)}"]
    if from_label:
        lines.append(f"<b>{from_label}:</b> {esc(_label(e['from']))}")
    if to_label:
        lines.append(f"<b>{to_label}:</b> {esc(_label(e['to']))}")
    if e.get("verified"):
        lines.append(f"<b>Проверено:</b> {esc(str(e['verified']))}")
    if e.get("done"):
        lines.append(f"<b>Сделано:</b> {esc(str(e['done']))}")
    next_step = e.get("next") or (e.get("to") or {}).get("title") or "См. AGENT_HANDOFF.md"
    lines.append(f"<b>Далее:</b> {esc(str(next_step))}")
    if e.get("reason"):
        lines.append(f"<b>Причина:</b> {esc(str(e['reason']))}")
    if e.get("status"):
        lines.append(f"<b>Статус:</b> {esc(str(e['status']))}")
    if e.get("artifact_url") and not event_problem(e):
        lines.append(f'<a href="{esc(e["artifact_url"])}">Скачать архив для локального просмотра</a>')
    cp = str(e.get("checkpoint") or "")
    if cp:
        lines.append(f"<b>Последний checkpoint:</b> <a href=\"{esc(f'{server}/{repo}/commit/{cp}')}\">{esc(cp[:7])}</a>")
    lines.append(f"<i>Ветка <code>{esc(branch)}</code> · событие <code>{esc(str(e['id']))}</code> · "
                 f"<a href=\"{esc(f'{server}/{repo}/commit/{sha}')}\">коммит {esc(sha[:7])}</a></i>")
    return fit("\n".join(lines))


def next_action(handoff: str | None) -> str | None:
    if not handoff:
        return None
    m = re.search(r"\*\*(?:Exact next|Next):\*\*\s*(.+)", handoff)
    return m.group(1).strip() if m else None


def digest_message(repo: str, now: dt.datetime, branch_commits: dict[str, int], milestones: list[dict], failures: list[dict],
                   active: str | None, active_branch: str | None, missing: list[str], server: str = "https://github.com",
                   open_actions: list[dict] | None = None) -> str:
    msk = now.astimezone(dt.timezone(dt.timedelta(hours=3)))
    lines = [f"<b>📋 Итоги дня — {esc(PROJECT)}</b>", f"<i>за 24 ч до {msk:%d.%m.%Y %H:%M} МСК · механизм: {SOURCE_ACTIONS} · агент: {SOURCE_UNKNOWN}</i>", "", "<b>Коммиты:</b>"]
    if branch_commits:
        for b, n in sorted(branch_commits.items(), key=lambda kv: -kv[1]):
            lines.append(f"• <code>{esc(b)}</code>: {n}")
    else:
        lines.append("• коммитов не было")
    lines.append("")
    lines.append("<b>Завершённые этапы:</b>")
    lines += [f"• {esc(m.get('title', m.get('id', '')))} — {esc(STATUS_TITLES.get(m.get('status', ''), m.get('status', '')))}" for m in milestones] or ["• нет записанных завершений"]
    lines.append("")
    lines.append("<b>Неуспешные проверки GitHub Actions:</b>")
    lines += [f"• <a href=\"{esc(f['url'])}\">{esc(f['name'])}</a> · <code>{esc(f['branch'])}</code>" for f in failures[:10]] or ["• нет"]
    lines.append("")
    lines.append("<b>Текущий этап (по handoff):</b>")
    lines.append(f"• {esc(active)}" + (f" (<code>{esc(active_branch)}</code>)" if active_branch else "") if active else "• не удалось определить")
    if open_actions:
        lines.append("")
        lines.append("🚨 <b>Ждут вашего действия:</b>")
        lines += [f"• {esc(a['subtask'])} (<code>{esc(a['id'])}</code>)" for a in open_actions]
    if missing:
        lines.append("")
        lines.append("<b>Нет данных:</b> " + esc("; ".join(missing)))
    lines.append(f"\n<a href=\"{server}/{repo}/commits\">Коммиты на GitHub</a>")
    return fit("\n".join(lines))


# ---------------------------------------------------------------- entry points

def env(name: str) -> str:
    # Secrets pasted with a trailing newline/space are a common setup error; surrounding whitespace is never valid.
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Не задана переменная окружения {name}")
    return value


def load_ledger(path: str) -> set[str]:
    try:
        with open(path, encoding="utf-8") as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


def run_commits(args) -> int:
    with open(env("GITHUB_EVENT_PATH"), encoding="utf-8") as f:
        event = json.load(f)
    repo = env("GITHUB_REPOSITORY"); branch = os.environ.get("GITHUB_REF_NAME", "")
    gh = GitHub(repo, os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"), os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    token, chat = env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID")
    commits, warnings = pushed_commits(event, gh)
    ledger = load_ledger(args.ledger)
    failures = 0
    after = event.get("after", ZERO_SHA); before = event.get("before", ZERO_SHA)
    # USER ACTION REQUIRED alerts go out before anything else in the push.
    if after != ZERO_SHA and before != ZERO_SHA:
        try:
            current_actions = load_actions(gh.file_at(ACTIONS_FILE, after))
            # Recover records missed while bindings/delivery were unavailable. Stable ledger
            # keys, not only the previous commit diff, decide whether a record was delivered.
            opened = [item for item in current_actions.values() if item["status"] == "open"]
            resolved = [item for item in current_actions.values() if item["status"] == "resolved"]
        except Exception as e:
            failures += 1
            opened, resolved = [], []; print(f"::error::Не удалось прочитать реестр действий: {type(e).__name__}")
        for a, kind in [(a, "open") for a in opened] + [(a, "resolved") for a in resolved]:
            key = f"action:{branch}:{a['id']}:{kind}"
            if key in ledger:
                continue
            try:
                head_source = agent_source(commits[-1]["message"], commits[-1]["author"]) if commits else SOURCE_UNKNOWN
                send(token, chat, action_message(repo, branch, after, a, server, head_source) if kind == "open" else resolved_message(branch, a, head_source))
                with open(args.ledger, "a", encoding="utf-8") as f:
                    f.write(key + "\n")
                print(f"Отправлено действие ({kind}): {a['id']}")
            except RuntimeError as e:
                failures += 1; print(f"::error::Не удалось отправить «ТРЕБУЕТСЯ ВАШЕ ДЕЙСТВИЕ» ({a['id']}): {e}")
    for w in warnings:
        print(f"::warning::{w}")
    for c in commits:
        key = f"commit:{branch}:{c['sha']}"
        if key in ledger:
            print(f"Пропуск {c['sha'][:7]}: уже отправлено в этом запуске")
            continue
        try:
            message_id = send(token, chat, commit_message(repo, branch, c["sha"], c["author"], c["message"], server, workflow_verified=os.environ.get("WEBSITE_CHECK_STATUS") == "success" and c["sha"] == after))
            with open(args.ledger, "a", encoding="utf-8") as f:
                f.write(key + "\n")
            print(f"Отправлено: {c['sha'][:7]} (message_id {message_id})")
            if message_id is not None:
                print(f"::notice title=Telegram accepted::commit {c['sha']} message_id {message_id}")
        except RuntimeError as e:
            failures += 1
            print(f"::error::Не удалось отправить уведомление о коммите {c['sha'][:7]}: {e}")
    warning_key = f"warning:{branch}:{after}"
    if warnings and commits and warning_key not in ledger:
        try:
            send(token, chat, fit(f"<b>⚠️ {esc(PROJECT)}</b>: " + esc(" ".join(warnings)) + f"\n<b>Агент:</b> {SOURCE_UNKNOWN}\n<b>Механизм:</b> {SOURCE_ACTIONS}\n<b>Ветка:</b> <code>{esc(branch)}</code>"))
            with open(args.ledger, "a", encoding="utf-8") as stream:
                stream.write(warning_key + "\n")
        except RuntimeError as e:
            failures += 1; print(f"::error::Не удалось отправить предупреждение: {e}")
    # Task / roadmap transition events recorded in this push (explicit agent state, never inferred).
    if after != ZERO_SHA and before != ZERO_SHA:
        try:
            events = new_events(None, gh.file_at(EVENTS_FILE, after))
        except Exception as e:
            failures += 1
            events = []; print(f"::error::Не удалось прочитать журнал событий: {type(e).__name__}")
        head_source = agent_source(commits[-1]["message"], commits[-1]["author"]) if commits else SOURCE_UNKNOWN
        for ev in events:
            key = f"event:{ev['id']}"
            if key in ledger:
                continue
            try:
                message_id = send(token, chat, event_message(repo, branch, after, ev, server, head_source))
                with open(args.ledger, "a", encoding="utf-8") as f:
                    f.write(key + "\n")
                print(f"Отправлено событие {ev['type']}: {ev['id']} (message_id {message_id})")
            except RuntimeError as e:
                failures += 1; print(f"::error::Не удалось отправить событие {ev['id']}: {e}")
    # Milestones recorded in this push (before → after state of the registry).
    if after != ZERO_SHA and before != ZERO_SHA:
        try:
            transitions = milestone_transitions(gh.file_at(MILESTONE_FILE, before), gh.file_at(MILESTONE_FILE, after))
        except Exception as e:
            transitions = []; print(f"::warning::Не удалось прочитать реестр этапов: {type(e).__name__}")
        for m in transitions:
            key = f"milestone:{branch}:{m.get('id')}:{m.get('status')}"
            if key in ledger:
                continue
            try:
                m["_source"] = agent_source(commits[-1]["message"], commits[-1]["author"]) if commits else SOURCE_UNKNOWN
                send(token, chat, milestone_message(repo, branch, after, m, server))
                with open(args.ledger, "a", encoding="utf-8") as f:
                    f.write(key + "\n")
            except RuntimeError as e:
                failures += 1; print(f"::error::Не удалось отправить уведомление об этапе: {e}")
    print(f"Коммитов: {len(commits)}, ошибок отправки: {failures}")
    return 1 if failures else 0


def run_ci_report(args) -> int:
    repo = env("GITHUB_REPOSITORY")
    run_url = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{env('GITHUB_RUN_ID')}"
    counts = junit_counts(args.junit) if args.junit else None
    if args.status == "success" and not args.notify_success:
        print("Успешная сборка: уведомление не требуется"); return 0
    key = f"ci:{repo}:{os.environ.get('GITHUB_RUN_ID', '')}:{args.status}"
    ledger = getattr(args, "ledger", ".telegram-ledger/sent.txt")
    if key in load_ledger(ledger):
        print("Отчёт этого запуска уже отправлен"); return 0
    try:
        send(env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID"),
             ci_message(repo, args.workflow, os.environ.get("GITHUB_REF_NAME", ""), os.environ.get("GITHUB_SHA", ""), args.status, run_url, counts))
    except RuntimeError as e:
        print(f"::error::Не удалось отправить отчёт CI: {e}"); return 1
    with open(ledger, "a", encoding="utf-8") as f:
        f.write(key + "\n")
    return 0


def run_check_config() -> int:
    """Names/presence only. Emits check-run annotations, never secret values."""
    missing = [name for name in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID") if not os.environ.get(name, "").strip()]
    for name in missing:
        print(f"::error title=Missing Telegram binding::{name} is not configured for this workflow; add the existing bot/chat in repository Actions secrets.")
    if not missing:
        print("Telegram bindings present: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (values hidden; delivery not yet verified)")
    return 1 if missing else 0


def completed_events_since(text, since, now):
    result = []
    for event in load_events(text):
        if event_problem(event) or event.get("type") not in {"task_completed", "stage_completed", "task_transition", "stage_transition", "roadmap_completed"}:
            continue
        try:
            at = dt.datetime.fromisoformat(event.get("at", "").replace("Z", "+00:00"))
            if at.tzinfo is None or not since <= at <= now:
                continue
        except (ValueError, TypeError):
            continue
        result.append({"id": event["id"], "title": _label(event["from"]), "status": "checkpoint_verified", "note": event["verified"]})
    return result


def run_digest(args) -> int:
    repo = env("GITHUB_REPOSITORY")
    gh = GitHub(repo, os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN"), os.environ.get("GITHUB_API_URL", "https://api.github.com"))
    now = dt.datetime.now(dt.timezone.utc); since = now - dt.timedelta(hours=24)
    missing: list[str] = []
    branch_commits: dict[str, int] = {}
    recent: list[tuple[str, str]] = []
    seen_milestones: dict[str, dict] = {}
    selected_branch = getattr(args, "branch", "")
    if selected_branch:
        branches = [{"name": selected_branch}]
    else:
        try:
            branches = gh.get(f"/repos/{repo}/branches", {"per_page": 100})
        except Exception as error:
            branches = []; missing.append(f"список веток недоступен ({type(error).__name__})")
    for b in branches:
        name = b["name"]
        recent.append(("", name))
        try:
            commits = gh.get(f"/repos/{repo}/commits", {"sha": name, "since": since.isoformat(), "per_page": 100})
        except Exception:
            missing.append(f"коммиты ветки {name}"); continue
        if commits:
            branch_commits[name] = len(commits)
            at = commits[0]["commit"]["committer"]["date"]
            recent.append((at, name))
        try:
            for item in completed_events_since(gh.file_at(EVENTS_FILE, name), since, now):
                seen_milestones[item["id"]] = item
        except Exception as error:
            missing.append(f"журнал проверенных событий ветки {name} ({type(error).__name__})")
    failures = []
    try:
        runs = gh.get(f"/repos/{repo}/actions/runs", {"status": "failure", "created": f">={since:%Y-%m-%dT%H:%M:%SZ}", "per_page": 50})
        failures = [{"name": r.get("name", ""), "branch": r.get("head_branch", ""), "url": r.get("html_url", "")} for r in runs.get("workflow_runs", [])]
    except Exception as e:
        missing.append(f"запуски GitHub Actions ({type(e).__name__})")
    # Handoff and action registry: the most recently active branch that actually has them (the default branch
    # carries only the notification infrastructure).
    active = None; active_branch = None; open_actions: list[dict] | None = None
    for _, name in sorted(recent, reverse=True):
        try:
            if active is None:
                active = next_action(gh.file_at("AGENT_HANDOFF.md", name)); active_branch = name if active else None
            if open_actions is None:
                text = gh.file_at(ACTIONS_FILE, name)
                if text is not None:
                    open_actions = [a for a in load_actions(text).values() if a["status"] == "open"]
        except Exception:
            missing.append(f"handoff/реестр действий ветки {name}")
        if active is not None and open_actions is not None:
            break
    text = digest_message(repo, now, branch_commits, list(seen_milestones.values()), failures, active, active_branch, missing,
                          os.environ.get("GITHUB_SERVER_URL", "https://github.com"), open_actions or [])
    if args.dry_run:
        print(text); return 0
    ledger = getattr(args, "ledger", ".telegram-ledger/digest.txt")
    moscow_day = now.astimezone(dt.timezone(dt.timedelta(hours=3))).date().isoformat()
    key = f"digest:{repo}:{selected_branch}:{moscow_day}"
    if key in load_ledger(ledger):
        print("Дайджест за этот день уже отправлен"); return 0
    try:
        send(env("TELEGRAM_BOT_TOKEN"), env("TELEGRAM_CHAT_ID"), text)
    except RuntimeError as e:
        print(f"::error::Не удалось отправить дайджест: {e}"); return 1
    with open(ledger, "a", encoding="utf-8") as stream:
        stream.write(key + "\n")
    print("Дайджест отправлен"); return 0


def run_add_event(args) -> int:
    """Deterministic event append for agents: no network, no LLM text — fields come from the handoff/roadmap."""
    try:
        with open(args.file, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"about": "Task/roadmap transition events (append-only; stable ids). Protocol: AGENT_NOTIFICATION_PROTOCOL.md", "events": []}
    now = dt.datetime.now(dt.timezone.utc)
    e = {"id": args.id or f"evt-{now:%Y%m%dT%H%M%SZ}-{os.urandom(3).hex()}", "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "type": args.type, "source": args.source}
    for name in ("from", "to"):
        path, title = getattr(args, f"{name}_path"), getattr(args, f"{name}_title")
        if path or title:
            e[name] = {"path": [x.strip() for x in (path or "").split(">") if x.strip()], "title": (title or "").strip()}
    for name in ("verified", "status", "reason", "checkpoint", "done", "next", "artifact_url"):
        if getattr(args, name):
            e[name] = getattr(args, name).strip()
    problem = event_problem(e)
    if problem or e["id"] in {str(x.get("id")) for x in data.get("events", [])}:
        print(f"Событие не добавлено: {problem or 'id уже есть'}"); return 1
    data.setdefault("events", []).append(e)
    with open(args.file, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print(event_message("OWNER/REPO", "BRANCH", "0" * 40, e)); return 0


def run_validate_events(args) -> int:
    with open(args.file, encoding="utf-8") as f:
        events = load_events(f.read())
    bad = [(str(e.get("id")), event_problem(e)) for e in events if event_problem(e)]
    ids = [str(e.get("id")) for e in events]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    for i, why in bad:
        print(f"Некорректное событие {i}: {why}")
    if dups:
        print(f"Повторяющиеся id: {', '.join(dups)}")
    print(f"Событий: {len(events)}, некорректных: {len(bad)}, повторов id: {len(dups)}")
    return 1 if bad or dups else 0


def run_validate_actions(args) -> int:
    with open(args.file, encoding="utf-8") as f:
        raw = json.load(f).get("alerts", [])
    valid = load_actions(json.dumps({"alerts": raw}))
    bad = [str(x.get("id", "?")) if isinstance(x, dict) else "?" for x in raw if not (isinstance(x, dict) and str(x.get("id")) in valid)]
    bad += [i for i, x in valid.items() if x["status"] not in ("open", "resolved")]
    for i, x in valid.items():
        if x["status"] == "open":
            print(action_message("OWNER/REPO", "BRANCH", "0" * 40, x)); print("-" * 40)
    if bad:
        print(f"Некорректные записи (будут проигнорированы): {', '.join(bad)}. Обязательные поля: {', '.join(ACTION_FIELDS)}; status: open|resolved")
        return 1
    print(f"OK: записей {len(valid)}, открытых {sum(x['status'] == 'open' for x in valid.values())}")
    return 0


def run_report_check(args) -> int:
    message = open(args.message_file, encoding="utf-8").read() if args.message_file else subprocess.check_output(["git", "log", "-1", "--format=%B"], text=True)
    fields = trailers(message)
    problems = []
    allowed = {SOURCE_CLAUDE, SOURCE_CODEX, SOURCE_OTHER, SOURCE_UNKNOWN}
    if len(fields.get("agent", [])) != 1 or fields["agent"][0] not in allowed:
        problems.append("Agent: нужна одна точная каноническая подпись")
    for key, limit in [("report-summary", 220), ("report-done", 800), ("report-checks", 700)]:
        values = fields.get(key, [])
        if len(values) != 1 or not re.search(r"[А-Яа-яЁё]", values[0]) or len(values[0]) > limit:
            problems.append(key + ": нужна одна краткая русская запись")
    for problem in problems:
        print("::error::" + problem)  # Field names only; never echo commit/secret values.
    if not problems:
        print("Русские поля отчёта и явная подпись агента корректны")
    return int(bool(problems))


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("commits"); c.add_argument("--ledger", default=".telegram-ledger/sent.txt")
    r = sub.add_parser("ci-report"); r.add_argument("--workflow", required=True); r.add_argument("--status", required=True)
    r.add_argument("--junit", default=""); r.add_argument("--notify-success", action="store_true"); r.add_argument("--ledger", default=".telegram-ledger/sent.txt")
    d = sub.add_parser("digest"); d.add_argument("--dry-run", action="store_true"); d.add_argument("--branch", default=""); d.add_argument("--ledger", default=".telegram-ledger/digest.txt")
    sub.add_parser("check-config")
    report = sub.add_parser("report-check"); report.add_argument("--message-file", default="")
    v = sub.add_parser("actions"); v.add_argument("--file", default=ACTIONS_FILE)
    ev = sub.add_parser("event"); ev.add_argument("--file", default=EVENTS_FILE)
    ev.add_argument("--type", required=True, choices=sorted(EVENT_TYPES)); ev.add_argument("--source", required=True, choices=[SOURCE_CLAUDE, SOURCE_CODEX, SOURCE_OTHER, SOURCE_UNKNOWN])
    ev.add_argument("--id", default=""); ev.add_argument("--from-path", default=""); ev.add_argument("--from-title", default="")
    ev.add_argument("--to-path", default=""); ev.add_argument("--to-title", default="")
    for name in ("--verified", "--status", "--reason", "--checkpoint", "--done", "--next", "--artifact-url"):
        ev.add_argument(name, default="")
    evs = sub.add_parser("events"); evs.add_argument("--file", default=EVENTS_FILE)
    a = p.parse_args(argv)
    if a.cmd == "report-check":
        return run_report_check(a)
    if a.cmd == "check-config":
        return run_check_config()
    if a.cmd == "event":
        return run_add_event(a)
    if a.cmd == "events":
        return run_validate_events(a)
    if a.cmd == "actions":
        return run_validate_actions(a)
    if a.cmd == "commits":
        os.makedirs(os.path.dirname(a.ledger) or ".", exist_ok=True)
        return run_commits(a)
    if a.cmd == "ci-report":
        os.makedirs(os.path.dirname(a.ledger) or ".", exist_ok=True)
        return run_ci_report(a)
    if not a.dry_run:
        os.makedirs(os.path.dirname(a.ledger) or ".", exist_ok=True)
    return run_digest(a)


if __name__ == "__main__":
    sys.exit(main())
