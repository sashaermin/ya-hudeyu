# САЙТ «Я ХУдЕЮ» — общий Telegram-протокол

Основан на read-only Android `.github/AGENT_NOTIFICATION_PROTOCOL.md` и проверяемом скрипте Android `874de91cb626b6f0e78532963b378d86901b97d9`; адаптирован исключительно для репозитория сайта. Один существующий бот «Я ХУдЕЮ | Dev Reports». Никаких локальных отправок, дополнительных ботов или команд исполнения из Telegram.

## Канонический русский формат и provenance

Общие resume/checkpoint/handoff правила — [AGENT_DEVELOPMENT_PROTOCOL.md](AGENT_DEVELOPMENT_PROTOCOL.md); единая точка входа — [AGENTS.md](AGENTS.md), Claude entrypoint — [CLAUDE.md](CLAUDE.md). Эти протоколы обязательны при будущих изменениях workflows/инфраструктуры; не заменять конкурирующими агентскими правилами.

Один commit → одно сообщение. Каноническая визуальная иерархия (текст остаётся русским):

```html
<b>САЙТ «Я ХУдЕЮ» — новый коммит</b>

<b>Проект:</b> САЙТ «Я ХУдЕЮ»
<b>Агент:</b> Codex
<b>Ветка:</b> <code>work/website-v2</code>
<b>Коммит:</b> <code>короткий-SHA</code>

<b>Изменение:</b>
Короткое содержательное русское описание.

<b>Что сделано:</b>
1–3 коротких предложения.

<b>Проверки:</b>
Только реальные результаты либо честный неподтверждённый статус.

<a href="https://github.com/sashaermin/ya-hudeyu/commit/полный-SHA">Открыть коммит на GitHub</a>
```

Та же иерархия обязательна для stage/task transitions, milestone, CI failures, owner action required/resolved, preview artifacts, daily digest и API warnings: один жирный header проекта/события; затем блок жирных metadata labels; далее отдельные жирные секции с пустой строкой между блоками; внизу заметные описательные ссылки. Branch/hash/event/action/stage identifiers — `<code>`. Цели и данные не переводить автоматически и не выдумывать; narratives остаются русскими. Digest представлен этим стилем, но его расписание не активировано без прежнего отдельного main-разрешения.

Формирование сосредоточено в presentation/section/safe_link; это только отображение, не новая система отправки. Динамические текстовые значения и атрибуты проходят HTML escaping, включая кавычки. Clickable URLs — только валидные HTTPS без credentials/control/quote injection; плохая ссылка отклоняется без эха значений. Descriptive anchors ведут непосредственно к commit/Actions run/записи задачи, вместо голого URL. Long-message truncation сохраняет целые entities, сбалансированные HTML tags и резервирует footer links. Mocks проверяют все виды сообщений, malicious values/URL и длинный текст; это не Telegram screenshot/UI test.

Формат хранится только здесь. Структурированные однострочные trailers в последнем непрерывном блоке commit message:

```text
Report-Summary: Единый протокол передачи и отчётов
Report-Done: Закреплены общие правила агентов и русский шаблон уведомлений.
Report-Checks: Локальные проверки пройдены; результаты и область указаны в progress.
Agent: Codex
```

Все три Report-поля обязательны для новых commits; писать реальные результаты, не копировать пример как доказательство. Summary≤220, Done≤800, Checks≤700 символов; Done —1–3 предложения. `report-check` проверяет HEAD (или `--message-file` перед commit), язык/наличие/границы полей и точную canonical Agent запись; workflow запускает его до остальных проверок. Report-Checks — запись implementing agent, она помечается как таковая. Только head SHA успешно проверенного verify job получает отдельное утверждение об успешных workflow checks (`WEBSITE_CHECK_STATUS=success`); старые commits multi-push не выдаются за отдельно проверенные.

Разрешённые **выводимые** значения Agent ровно: `Claude Code`, `Codex`, `Разработчик`, `Не определён`. Использовать точную явную provenance запись; Git author, co-author, repository/branch/workflow/runner/session URL и префиксы имён не определяют implementing agent. Конфликтующие/неизвестные записи → `Не определён`. Исторические input aliases `Other agent`/`Unknown` читаются для совместимости, но новые commits используют только canonical labels. События/actions/milestones должны иметь собственный source: агент более позднего commit не присваивается старому событию. CI/digest без достоверного implementing-agent metadata: Agent `Не определён`, отдельно «Механизм: GitHub Actions».

У stage/CI/owner-action/resolution reports те же русские подписи проекта/агента, фактические проверки и ссылки. Технические identifiers не переводить, русские narrative поля заполняет агент. Preview artifact: event `preview_artifact_ready`, verified, from, source и `artifact_url` — только проверенная HTTPS GitHub artifact ссылка этого сайта; подпись явно «архив для просмотра, не онлайн-превью». Не выдавать ZIP/localhost за доступный веб-сайт. CLI поддерживает `--artifact-url`. Новые форматы тестируются mocks; отдельные живые test messages не отправлять.

## Механизм

`.github/workflows/website-checks.yml` на push `work/**` выполняет тесты и сборку. Только после успешных проверок уведомляет о коммитах, действиях и явно зарегистрированных этапах. При провале проверок отправляет отдельный отчёт об ошибке; непроверенный коммит не называется проверенным. Отправитель — `.github/scripts/telegram_notify.py`, stdlib Python. Все сообщения содержат **САЙТ «Я ХУдЕЮ»**. Android не затрагивается.

GitHub Actions получает repository secrets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (тот же бот/чат) и временный `github.token` с `contents:read`. Значения не читать и не выводить. Облачные локальные переменные не заменяют Actions secrets. Metadata API списка секретов возвращает 403 Resource not accessible by integration. Исторический probe run39106472358 показал отсутствие bindings. При новой проверке 18.10.2026 10:47 МСК run39107499146 attempt2 подтвердил: оба bindings доступны, notify success, Telegram accepted message_id67. Значения не извлекались. Блокер настройки закрыт; повторно запрашивать секреты не нужно.

## Единые записи

- Commit: canonical provenance/report trailers определены выше. Ledger keys сохраняются при смене формата, старые сообщения не переотправлять ради нового шаблона.
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

Ежедневный digest в 21:00 МСК обязателен по новой инструкции владельца. Подготовлен `.github/workflows/website-digest.yml`: cron `0 18 * * *` (UTC), только чтение API/общих реестров, вывод событий с доказательствами, pending действий и точного next из handoff, защита по Moscow date + branch в ledger. Предпросмотр `digest --dry-run --branch work/website-v2` не отправляет сообщения; он проверен на настоящем GitHub API.

**Расписание ещё не активно.** GitHub исполняет schedule только из default branch. Чтобы включить, нужно отдельное разрешение владельца поместить **только подготовленный `.github/workflows/website-digest.yml`** в main. Этот workflow checkout-ит `work/website-v2` для script/tests, не содержит deploy и не изменяет сайт. До разрешения main не трогать. `workflow_dispatch` также станет доступным после размещения файла в default branch. GitHub может задерживать scheduled jobs; точную минуту доставки не гарантировать.

`check-config` в Actions проверяет только наличие двух secret bindings и формирует аннотацию с отсутствующими именами. Значения не выводятся. Список repository secrets через API недоступен по правам integration; проверка binding внутри runner позволяет диагностировать это без нового токена. Все сетевые Telegram-проверки выполняет Actions, не локальный агент.

## Если настройки действительно отсутствуют

1. В `sashaermin/ya-hudeyu` откройте Settings → Secrets and variables → Actions.
2. Если имён TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID нет, добавьте секреты существующего бота и чата безопасно в GitHub (не в переписку).
3. В Actions → «САЙТ — проверки и Telegram» проверьте результат verify и notify; после изменения секретов перезапустите неуспешный workflow.

Эта проверка не блокирует сайт. Не просить новый токен только из-за недоступности API или отсутствия локальных переменных.

Формат stage report: заголовок «САЙТ «Я ХУдЕЮ»», событие, агент, этап from/to, `Сделано` (поле done), `Проверено` (verified), `Далее` (next или to.title), статус и commit/checkpoint ссылки. CLI `event` поддерживает `--done` и `--next`; для новых событий заполнять их конкретно.


## Recovery после отсутствующих bindings / частичного сбоя

На каждом успешном verify sender читает текущие action/event records, а ledger решает, что уже доставлено. Неотправленные open/resolved действия и валидные явно зарегистрированные этапы восстанавливаются, даже если их JSON не менялся в последнем commit. Повторный run пропускает delivered keys; частичный сбой оставляет failed item для следующей попытки, сохраняя успешные items. Полный API-сбой чтения реестра делает notify job неуспешным, не скрывается как успешная доставка.

Повторные API fallback warnings также имеют ledger key branch/head. После реального Telegram ok=true ответ message_id для commit появляется как check-run notice `Telegram accepted`; это проверяемое подтверждение приёма Telegram, не доказательство прочтения человеком. Локальные tests полностью mock, никаких сообщений из cloud-сессии агент не отправляет. Старые commit-сообщения прошлых failed runs автоматически не backfill-ятся; сохраняются актуальные commit notifications и backlog явных event/action records. Ledger cache ограничения описаны выше.

Уточнение после чтения Pages API: source сайта — legacy main:/. Хотя digest workflow не содержит deploy, сам update main может запустить действующий legacy Pages build. До main update разрешение должно учитывать этот побочный эффект. Не переносить в main workflow по одному лишь общему разрешению разработки; v2 сайт и APK остаются вне разрешения.

Проверенная live-доставка: docs/verification/telegram-delivery-2026-10-18.json. GitHub status success сам по себе недостаточен: здесь сохранён отдельный notice Telegram accepted с message_id67 из фактического sendMessage. Повторять тот же run без причины не нужно; ledger предотвращает повторные уведомления.

## Представление не меняет доставку

Обновление HTML не меняет workflow triggers/secrets/concurrency, бота/чат, ledger keys, retry/backlog/partial-failure поведение или существующие notification IDs. Старые уведомления не пересылать ради нового оформления. Живую проверку выполнять через обычный verified commit push, без дополнительных тестовых сообщений. Ошибка metadata API не означает отсутствие secrets; последние реальные accepted notices остаются доказательством доступности.

## Topic6 и daily digest · текущая конфигурация

Все website sends используют optional TELEGRAM_MESSAGE_THREAD_ID; workflow notify/digest задают `6` для группы «Я худею GROUP» / темы «Сайт | Я ХУдЕЮ». TELEGRAM_CHAT_ID обновлён владельцем, его значение не читать. Без optional ID прежний sender совместим; malformed ID — ошибка до HTTP, не fallback. Retry/HTML/secret protection/provenance и существующие ledger keys не меняются. Topic подтверждён только если actual Telegram Message вернул6 и annotation `Telegram topic confirmed` сmessage_id; mock и request payload не доказывают delivery.

Daily cron18:00UTC =21:00Europe/Moscow подготовлен, но не активен до отдельно разрешённого default-branch sync. `workflow_dispatch.inputs.dry_run` boolean/default true: фактический read-only GitHub API, без sends/cache/ledger mutations и без необходимости Telegram secrets. Отчёт содержит 24h commits/summaries, реальные Actions statuses, только явные verified completed events, open actions/blockers и handoff; API failures отмечаются как missing data. [Изолированный план активации](docs/TELEGRAM_DEFAULT_BRANCH_SYNC.md), allowlist/hashes/tests — docs/verification/telegram-topic-digest.json. Main/Pages сейчас не менять. Не выдавать наличие cron вdevelopment за действующее расписание.
