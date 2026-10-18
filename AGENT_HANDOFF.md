# «Я ХУдЕЮ» — общий handoff сайта

## Точка продолжения

- Repository: `sashaermin/ya-hudeyu`; development branch: `work/website-v2`.
- Последний независимо подтверждённый **implementation checkpoint**: `ad7c5a043d45f31cbc0a4ab6f489592ae14622d2` (W2B). Последующий documentation checkpoint получать из Git: файл не может содержать собственный будущий SHA.
- Последний ответственный писатель: Codex, 18.10.2026 10:22 МСК. Другой активный website writer не известен; это историческая запись, не доказательство отсутствия активной сессии при будущем takeover. Android Claude Code не затрагивался.
- Состояние: независимые задачи W2A / 4B / 3B / W2B выполнены и проверены. Открытые release/device/owner критерии сохранены в IMPLEMENTATION_PROGRESS.md и docs/QA.md. Сайт **не готов к публикации**, она не разрешена.

**Next:** После подтверждённой настройки двух Actions bindings существующего бота в репозитории сайта повторить failed notify job и проверить check-config + Telegram accepted/message_id annotations. Без изменения bindings не повторять тот же неуспешный run и не просить значения в чат. Daily digest требует отдельного разрешения на подготовленный default-branch workflow с учётом legacy Pages side effect; main не менять до этого. Когда владелец выберет и разрешит конкретный APK/реальные screenshots, выполнить docs/RELEASE_CONTENT.md, заполнить version-matched контент и проверить затронутые сценарии. Не выбирать APK самостоятельно и не напоминать повторно об уже зарегистрированных неизменившихся blockers.

## Авторитетные общие документы

AGENTS.md — общие правила; CLAUDE.md ведёт к ним же. Утверждённый оригинальный master specification: project_specs/WEBSITE_MASTER_TZ_2026-10-18.md. Новая постоянная инструкция автономного выполнения сохранена без переписывания в project_specs/AUTONOMOUS_EXECUTION_2026-10-18.txt. Единственный roadmap — IMPLEMENTATION_PROGRESS.md; уведомления — AGENT_NOTIFICATION_PROTOCOL.md. Не начинать заново, не создавать отдельный agent roadmap.

## Проверенные checkpoints / результаты

- `a4de44b`: source audit; `356eaef`: Android brand/tokens; `24ca8d5`: sections/interactions; `227ab74`: общие инструкции/notify; `a14a2c6`: release/SEO/fonts; `65f9410`: reports/dedup; `b3ffaf9`: 4A; `cf7814f`: предыдущий handoff.
- `9ca5397`: W2A — автономные инструкции, safe binding probe, обязательный daily digest 21:00 МСК, pinned upstream Actions v5 refs.
- `46b824d`: 4B — Firefox153/WebKit26.5, по16 viewport/theme runs и по4 axe runs, 0 violations; keyboard/theme/menu/FAQ/gallery/no-JS PASS. Вместе с сохранённым Chromium154 4A — 48 combinations, 12 axe runs. Firefox touch не поддерживается; WebKit native tap/DOM handler PASS, native swipe не проверен. Физические устройства/Safari/Edge отдельно не проверены.
- `237fc81`: 3B — APK distribution approval и website publication approval разделены. data/publication.json=false, data/release.json=unverified. Draft всегда noindex; production render требует оба вида разрешения и verified content. JSON-LD round-trip escaping исправлен. Реальный draft HTML побайтно совпал с проверенным 4A/4B артефактом; тяжёлые browser/Lighthouse checks не повторялись.
- `ad7c5a0`: W2B — recovery недоставленных unchanged open/resolved action records и явных event records, ledger/dedup/partial retries, delivery ack notice. 40 notification + 17 build/workflow tests PASS, без skip. Никаких локальных Telegram отправок.
- Actions run **39107259552** для ad7c5a0: verify **success**, notify **failure**, обе missing-binding annotations. JSON evidence: docs/verification/actions-current.json. Нельзя называть workflow целиком успешным или заявлять доставку.
- Сохранённый Lighthouse мобильного draft: Performance96 / Accessibility100 / BestPractices100 / SEO69 (intentional noindex). Это локальный замер 4A, не production measurement. Подробные результаты/ограничения и 8 owner-review screenshots — docs/QA.md, docs/verification, docs/screenshots.

## Среда и воспроизведение

- `python3 tools/build.py` → `_site` (stdlib-only). Сервер: `python3 -m http.server 8001 --bind 127.0.0.1 --directory _site`. Проверять/reuse корректный существующий процесс; не останавливать чужие процессы. В новой задаче процессы запускаются снова.
- Ресурсы/шрифты/палитра из read-only Android SHA `874de91cb626b6f0e78532963b378d86901b97d9`, provenance docs/ASSET_SOURCES.json. Не повторять source audit без изменения входов. Ни код, ни branches Android не менялись.
- Сеть CDN/API/домена фактически работает: старый network action resolved. Tool discovery предоставил только draft read/update, без API активации; способ публикации среды не заявляется как проверенный. Новая task restore отдельно не проверялась.
- Firefox/WebKit скачаны в `/tmp/website-browsers`. Native libraries получены через официальный подписанный Debian trixie index и распакованы в task-local каталоги; система/ключи/браузерные бинарники не менялись. Воспроизводимый helper tools/qa/prepare_linux_libs.py реально выполнен. Package versions/SHA — docs/verification/linux-qa-packages.json. Финальные команды (включая Firefox container-only setting и WebKit explicit launcher) — docs/QA.md.
- Optional QA dependencies pinned: tools/qa/package-lock.json и requirements.txt. Проверен npm ci (202 packages). Базовая сборка не требует этих пакетов.
- Cloud start_skill уже сохранён для `_site`; его draft save не исполняет команды и не деплоит сайт. Для текущей разработки новых environment edits не требуется.

## Внешние prerequisites — зарегистрированы один раз

1. `site-telegram-settings-verification`: probe Actions доказал отсутствие TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID для workflow сайта. Вводятся только в защищённых GitHub repository Actions settings существующего бота «Я ХУдЕЮ | Dev Reports». Metadata API secrets ограничен integration scope. Не извлекать секреты Android или значения из логов. После meaningful change — retry, доказательство Telegram ok=true/message_id, затем action resolved.
2. `site-digest-default-branch-activation`: `.github/workflows/website-digest.yml` готов (UTC18:00 = МСК21:00), unit/YAML/live API dry-run проверены. Расписание не активно вне default branch. Для активации нужно отдельное разрешение только на этот infrastructure workflow в main; Pages legacy main:/ может автоматически rebuild-иться, поэтому разрешение должно учитывать побочный эффект. Workflow не переносит v2 сайт/не публикует APK. Без разрешения ничего в main не делать.
3. `site-approved-android-release`: владелец явно не утвердил APK. Download action выключен. Не добавлять dev screenshots как релизные, не рекламировать код разработки как выпущенные функции. Реальные feature cards/gallery/hero screenshot ожидают проверенной сборки.

## Неприкосновенные ограничения

Main SHA `9a0857ce260540ad604f344565d535a8d47b2fa0` сохранялся; Pages API подтвердил legacy source main:/. Read-only HTTPS `/` и `/privacy.html`: HTTP200 и bytes равны origin/main. CNAME/privacy в development не изменены. Не делать main update, merge, PR, deployment, public APK download или снятие noindex без соответствующего отдельного разрешения. Не трогать Android/другие клиентские проекты и активные сессии. Сайт только для Android.

Все существенные инструкции и evidence находятся в Git; /tmp не единственный источник состояния. Перед продолжением fetch/status/remote inspection и проверка активного писателя обязательны. Историю не переписывать, чужую работу не перезаписывать.
