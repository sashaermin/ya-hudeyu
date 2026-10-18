# САЙТ «Я ХУдЕЮ» — общий Telegram-протокол

Основан на read-only Android `.github/AGENT_NOTIFICATION_PROTOCOL.md` и проверяемом скрипте Android `874de91cb626b6f0e78532963b378d86901b97d9`; адаптирован исключительно для репозитория сайта. Один существующий бот «Я ХУдЕЮ | Dev Reports». Никаких локальных отправок, дополнительных ботов или команд исполнения из Telegram.

## Механизм

`.github/workflows/website-checks.yml` на push `work/**` выполняет тесты и сборку. Только после успешных проверок уведомляет о коммитах, действиях и явно зарегистрированных этапах. При провале проверок отправляет отдельный отчёт об ошибке; непроверенный коммит не называется проверенным. Отправитель — `.github/scripts/telegram_notify.py`, stdlib Python. Все сообщения содержат **САЙТ «Я ХУдЕЮ»**. Android не затрагивается.

GitHub Actions получает repository secrets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (тот же бот/чат) и временный `github.token` с `contents:read`. Значения не читать и не выводить. Облачные локальные переменные не заменяют Actions secrets. Имена секретов пытались проверить через `gh api …/actions/secrets`: API запретил доступ (403). Существование/работоспособность bindings поэтому пока **не подтверждены**, а не объявлены отсутствующими. Доставка и CI должны проверяться в GitHub Actions, когда есть доступ.

## Единые записи

- Commit: trailer `Agent: Codex` / `Agent: Claude Code` / `Agent: Other agent`. Имя git-автора само по себе не доказывает агентский источник. Без достоверного trailer — Unknown.
- Этап/переход: append-only `project_specs/agent_events.json`. Уникальный постоянный id, `source`, `from`/`to` (`path` массив и `title`), `verified` для завершения, `checkpoint` последнего проверенного SHA. Не выводить завершение из активности агента или одного сообщения коммита. Не заявлять полное завершение ТЗ при открытых критериях.
- USER ACTION REQUIRED: `project_specs/user_actions.json`, поля `id`, `status` (open/resolved), `task`, `subtask`, `what`, `steps` массив, `blocked`, `can_continue`, `source`. Один id на проблему; при решении `status: resolved` и `resolution`. Новая запись/переход open→resolved отправляется один раз при нормальном выполнении workflow. Не переоткрывать решённый вопрос без причины.
- Значимые ошибки: автоматический CI report и/или явный `task_blocked` event с проверенной причиной. Не засыпать владельца уведомлениями на каждую команду.

Пример (локально только записывает событие):

```sh
python3 .github/scripts/telegram_notify.py event --type stage_transition --source Codex --id site-qa-start-20261018 --from-path 'Сайт > 2' --from-title 'Секции' --to-path 'Сайт > 4' --to-title 'QA' --verified 'draft build PASS; JS syntax PASS' --checkpoint 24ca8d51ec4c194ee84d72392194b923a843cbb7 --status 'разработка продолжается'
python3 .github/scripts/telegram_notify.py actions
python3 .github/scripts/telegram_notify.py events
python3 -m unittest discover -s .github/scripts -p 'test_*.py' -v
```

## Дедупликация и ограничения

Workflow сериализуется по ветке, `cancel-in-progress: false`. Ledger `.telegram-ledger/sent.txt` сохраняется в GitHub Actions cache с ключом ветки и run/attempt; повторный запуск восстанавливает предыдущий ledger. Коммиты дедуплицируются по SHA/ветке, события по id, действия по id/status/ветке, CI failure reports по repository/run_id/status. Повторное редактирование открытого действия не создаёт новый alert. Тесты используют mocks и не отправляют сообщения.

Cache — вспомогательное хранилище, не вечная гарантия exactly-once: eviction, сбой после принятия Telegram до записи ledger или сбой GitHub могут привести к повтору/недоставке. Не обещать гарантированную доставку или наблюдение за аварийным завершением агента. Запуски, ошибки и checkpoint проверять через GitHub Actions. Ожидаемая передача может регистрироваться trailer `Agent-Event: handoff`; неожиданное завершение не может достоверно отправить событие.

Ежедневный digest в 21:00 МСК опционален. Пока **не активирован**: schedule работает из default branch, а main изменять запрещено. Не добавлять schedule в рабочую ветку с обещанием, что он запустится. Имеющийся script digest — только техническая возможность, до отдельного разрешения на default-branch workflow не использовать.

## Если настройки действительно отсутствуют

1. В `sashaermin/ya-hudeyu` откройте Settings → Secrets and variables → Actions.
2. Если имён TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID нет, добавьте секреты существующего бота и чата безопасно в GitHub (не в переписку).
3. В Actions → «САЙТ — проверки и Telegram» проверьте результат verify и notify; после изменения секретов перезапустите неуспешный workflow.

Эта проверка не блокирует сайт. Не просить новый токен только из-за недоступности API или отсутствия локальных переменных.

Формат stage report: заголовок «САЙТ «Я ХУдЕЮ»», событие, агент, этап from/to, `Сделано` (поле done), `Проверено` (verified), `Далее` (next или to.title), статус и commit/checkpoint ссылки. CLI `event` поддерживает `--done` и `--next`; для новых событий заполнять их конкретно.
