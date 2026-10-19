"""Offline fixture gallery. No credentials, network calls or delivery entrypoints."""
from pathlib import Path
import datetime as dt
import hashlib
import html
import json
import sys

import telegram_notify as notify

PLATFORM = 'Website'
REPOSITORY = 'sashaermin/ya-hudeyu'
SHA = 'a' * 40  # Synthetic, deliberately not a real development claim.
BRANCH = 'work/presentation-fixture'
RUN = 'https://github.com/' + REPOSITORY + '/actions/runs/1'


def samples(module=notify, digest=None):
    out = {}
    prose = 'Уточнены подписи & поведение <кнопки>.'
    checks = 'Локально не запускались; результат не подтверждён.'
    message = (prose + '\nAgent: Codex\nSummary-Ru: ' + prose +
        '\nDone-Ru: Обновлена подпись кнопки.\nChecks-Ru: ' + checks +
        '\nReport-Summary: ' + prose + '\nReport-Done: Обновлена подпись кнопки.' +
        '\nReport-Checks: ' + checks)
    out['commit'] = module.commit_message(REPOSITORY, BRANCH, SHA, 'Автор <пример>', message)
    out['commit_unknown'] = module.commit_message(REPOSITORY, BRANCH, SHA, 'Codex', 'fix: button <tag>')
    for event in ('interruption', 'handoff', 'resume'):
        out['agent_' + event] = module.commit_message(REPOSITORY, BRANCH, SHA, '', message + '\nAgent-Event: ' + event)
    for status in module.STATUS_TITLES:
        out['milestone_' + status] = module.milestone_message(REPOSITORY, BRANCH, SHA,
            dict(id='stage-1', title='Этап <пример>', status=status, note='На устройстве не проверялось.', _source='Claude Code', source='Claude Code'))
    for status, counts in (('success',dict(files=1, passed=8, failed=0, skipped=2)), ('failure',dict(files=1, passed=7, failed=1, skipped=2)), ('cancelled',None)):
        out['ci_' + status] = module.ci_message(REPOSITORY, 'Проверки <пример>', BRANCH, SHA, status, RUN, counts)
    action = dict(id='owner-1', task='Проверка', subtask='Выбрать вариант', what='Нужен выбор владельца.',
        steps=['Откройте образец.', 'Подтвердите вариант.'], blocked='Следующий этап', can_continue='Да, другие задачи',
        source='Codex', resolution='Выбран вариант A.', link=RUN)
    out['action'] = module.action_message(REPOSITORY, BRANCH, SHA, action)
    out['resolved'] = module.resolved_message(BRANCH, action, repo=REPOSITORY, sha=SHA)
    node = dict(path=['ТЗ', 'Этап 2', 'Задача 4'], title='Подписи кнопок')
    for kind in module.EVENT_TYPES:
        event = dict(id='fixture-' + kind, type=kind, source='Codex', verified='Проверено только в указанном объёме.',
            done='Обновлены подписи.', next='Проверить экран.', reason='Контрольная точка', status='разработка продолжается',
            checkpoint=SHA, artifact_url=RUN + '/artifacts/2')
        event.update({'from':node, 'to':node})
        out['event_' + kind] = module.event_message(REPOSITORY, BRANCH, SHA, event)
    now = dt.datetime(2026, 10, 19, 18, 0, tzinfo=dt.timezone.utc)  # Frozen fixture, not send time.
    out['digest'] = module.digest_message(REPOSITORY, now, {BRANCH:2}, [],
        [dict(url=RUN,name='Проверки',branch=BRANCH)], 'Проверить экран', BRANCH, ['Нет данных устройства'], open_actions=[action])
    out['digest_empty'] = module.digest_message(REPOSITORY, now, {}, [], [], None, None, [])
    out['warning'] = module.presentation('данные уведомления неполны', [('Агент', 'Не определён', False), ('Механизм', 'GitHub Actions', False), ('Ветка', BRANCH, True)], [module.section('Причина', '2 коммита не перечислены.')], [(RUN, 'Открыть запуск GitHub Actions')])
    out['commit_verified_workflow'] = module.commit_message(REPOSITORY, BRANCH, SHA, '', message, workflow_verified=True)
    out['long_commit'] = module.commit_message(REPOSITORY, BRANCH, SHA, '', message + '\nReport-Done: ' + '&🙂<длинный> ' * 1000)
    out['long_digest'] = module.digest_message(REPOSITORY, now, {BRANCH:2}, [], [], 'Длинное описание &🙂 ' * 1000, BRANCH, [])
    out['long_event'] = module.event_message(REPOSITORY, BRANCH, SHA, dict(event, reason='Причина &🙂 ' * 1000))
    out['long_unicode'] = module.commit_message(REPOSITORY, BRANCH, SHA, '', 'x\nAgent: Codex\nSummary-Ru: ' + '🙂&' * 3500 + '\nReport-Summary: ' + '🙂&' * 3500 + '\nReport-Done: ' + '🙂&' * 3500)
    return out


def gallery(pairs):
    cards = []
    for name, entry in pairs.items():
        after = samples()[name]
        before_parser = notify._PresentationHTML(); before_parser.feed(entry['before_html']); before_parser.close()
        before = before_parser.result()
        cards.append('<section><h2>' + html.escape(name) + '</h2><div class="pair"><article><h3>До</h3><div class="message">' + before + '</div></article><article><h3>После</h3><div class="message">' + after + '</div></article></div></section>')
    return ('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'">'
        '<title>Telegram presentation — ' + PLATFORM + '</title><style>body{font:16px/1.5 system-ui;background:#eef2f6;margin:20px auto;max-width:960px;padding:12px}.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}article{background:white;border-radius:16px;padding:18px;overflow-wrap:anywhere}.message{white-space:pre-wrap}blockquote{margin:8px 0;border-left:3px solid #1685a6;padding:8px 12px;background:#f0f8fb}a{color:#086a9c}code{font-size:.9em}</style>'
        '<h1>' + PLATFORM + ' · оформление Telegram</h1><p>Только offline-макеты. Данные, SHA и run/artifact ID условные; ссылки не доказывают описанную работу. Ничего не отправлено. Карточки «до» сохраняют в том числе прежние сокращения и ограничения.</p>' + ''.join(cards) + '</html>\n')


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Write the local HTML gallery only; no delivery')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parents[2] / '.github/telegram-presentation'
    pairs = json.loads((directory / 'snapshots.json').read_text())
    actual = samples()
    assert set(actual) == set(pairs)
    for name, value in actual.items():
        assert hashlib.sha256(value.encode()).hexdigest() == pairs[name]['after_sha256'], name
    expected = gallery(pairs)
    path = directory / 'preview.html'
    if args.write: path.write_text(expected)
    else: assert path.read_text() == expected
    print(str(len(actual)) + ' offline previews match; no network or Telegram request')


if __name__ == '__main__': main()
