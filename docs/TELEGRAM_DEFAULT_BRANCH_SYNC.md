# Изолированное включение daily digest — план, не разрешение

Текущая рабочая ветка — `work/website-v2`, default branch — `main`. Цель: Telegram-группа «Я худею GROUP», тема «Сайт | Я ХУдЕЮ», `message_thread_id=6`. Владелец сообщил об обновлении repository secret TELEGRAM_CHAT_ID; значение не извлекалось. Routing ID не является секретом и явно задан в обоих notification jobs. Bot/token и существующие secrets сохранены.

## Что уже работает в development

Push запускает прежний website-checks pipeline и затем отправляет все commit/event/action/failure сообщения через единый sender с topic6. Без TELEGRAM_MESSAGE_THREAD_ID sender сохраняет прежний JSON без message_thread_id; неправильное непустое значение блокирует запрос, без fallback в общую тему. Retry, HTML escaping и dedup keys сохранены; старые сообщения не переотправляются из-за смены назначения. Подтверждение реального topic возможно по `Telegram topic confirmed`: sender записывает его только если Telegram API вернул соответствующий message_thread_id в Message, вместе с message_id. `Telegram accepted` без такого подтверждения не доказывает тему.

## Что ждёт отдельной авторизации

GitHub запускает schedule только при наличии workflow на default branch. Там сейчас website-digest.yml отсутствует (API404). Workflow_dispatch также требует файл на default branch, поэтому не обещать запуск кнопкой до синхронизации. Локальный CLI dry-run использует фактический GitHub API без отправки Telegram; это не scheduled run.

После явного разрешения владельца перенести **только следующие четыре файла** из проверенного working checkpoint, без merge development branch целиком:

1. `.github/workflows/website-digest.yml`
2. `.github/scripts/telegram_notify.py`
3. `.github/scripts/test_telegram_notify.py`
4. `.github/scripts/test_topic_digest.py`

SHA-256 каждого файла и изолированный тест этого набора — [verification/telegram-topic-digest.json](verification/telegram-topic-digest.json). Не включать website-checks.yml, docs, project_specs, site source/data, assets или публикационные настройки. Website-checks остаётся только на development; отдельный allowlist добавляет исключительно требуемый daily workflow/runtime/tests.

## Проверяемая процедура после разрешения

1. Fetch main и development, подтвердить approved source SHA и hashes четырёх файлов; если ветки продвинулись — сначала inspect, без reset/force-push. Повторно проверить Pages source/config и сохранить public-only manifest/rollback checkpoint.
2. Подготовить один минимальный main commit с этим allowlist, проверить diff и отсутствие изменений всех существующих public files. `.github` — служебный каталог GitHub/Jekyll, не публичный контент; после обновления подтвердить его HTTP-недоступность. Не копировать внутренние документы в public root.
3. Перед записью main учесть: текущий legacy Pages main:/ может автоматически rebuild даже при Telegram-only изменении. Авторизация должна явно покрывать этот возможный побочный эффект; не менять deployment config и не запускать deployment вручную. Сейчас запись main не разрешена и не выполнена.
4. Workflow берёт код из `${{ github.sha }}` — SHA текущего dispatch/default schedule, а данные читает read-only API из work/website-v2. Так future edits development не становятся исполняемым кодом default-branch job до review/sync. Permissions только contents/actions read, credentials checkout отключены.
5. Выполнить workflow_dispatch с `dry_run=true` (default): test suite + фактический API; без проверки Telegram secrets, отправки, восстановления/записи cache ledger. Проверить 24-часовое окно, реальные commit summaries, Actions statuses, completed events, open actions/blockers; недоступные данные указаны явно.
6. Затем dispatch с `dry_run=false`: одна отправка в тему6, verify actual Telegram Message.message_thread_id и message_id; повторный запуск в тот же московский день не должен дублировать digest. Тестовый реальный digest в этот день заменяет scheduled отправку благодаря прежнему daily key.
7. Проверить remote main SHA, actual scheduled run и тему; `0 18 * * *` =21:00 Europe/Moscow, GitHub может задерживать schedule. Убедиться, что public website hashes, HTTPS, noindex и APK-disabled неизменны. Закрыть существующий alert `site-digest-default-branch-activation` только после подтверждённой активации, не создавать второй alert.

Дайджест перечисляет activity предшествующих24часов, а не заявляет непрерывный мониторинг агента. Сообщение ограничено Telegram4096; выводит последние3описания коммитов/Actions runs, до4completed stages и до3failures, общий commit count и ссылки на полную историю; actual statuses не равны результату каждого теста. Completed events требуют явного типа завершения, времени и verified evidence; transitions не считаются completed. Open user actions/blockers берутся из общего registry, next — из handoff. Cache ledger дедуплицирует по прежнему Moscow-day key; глобальная exactly-once доставка при потере cache/сетевой неопределённости не гарантируется.
