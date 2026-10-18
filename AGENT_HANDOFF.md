# «Я ХУдЕЮ» — общий handoff сайта

## Точка продолжения

- Repository: `sashaermin/ya-hudeyu`; development branch: `work/website-v2`.
- Последний независимо подтверждённый remote checkpoint до4D: `6958c0d83863bda00e7fcdbc9ec0fa14dd7b2a25`; его push-triggered run39109598867 success, Telegram accepted message_id84. Предыдущий **implementation checkpoint**: `ad7c5a043d45f31cbc0a4ab6f489592ae14622d2` (W2B). Последующий documentation checkpoint получать из Git: файл не может содержать собственный будущий SHA.
- Последний ответственный писатель: Codex, 18.10.2026 11:02 МСК. Другой активный website writer не известен; это историческая запись, не доказательство отсутствия активной сессии при будущем takeover. Android Claude Code не затрагивался.
- Состояние: независимые задачи W2A / 4B / 3B / W2B / 4C / 4D выполнены и проверены. Открытые release/device/owner критерии сохранены в IMPLEMENTATION_PROGRESS.md и docs/QA.md. Сайт **не готов к публикации**, она не разрешена.

**Next:** R2 завершён: CI39110644873 success; notice117625868753 подтверждает скачанный artifact/22files/4renderedviews/noindex/noAPK/page_errors0; Telegram109. Verified remote0b4eb54. Следующая независимая подготовка — review-only diff coming-soon policy с isolated tests, **без применения к активным gates**. Затем предъявить владельцу конкретный предмет решения, записать owner next и сохранить final handoff. APK не блокирует website-кандидат; main/production/deployment/indexing/download разрешения не менялись.

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

1. `site-telegram-settings-verification` **resolved**: run39107499146 attempt2 подтвердил оба bindings и Telegram accepted message_id67. Metadata API secrets всё ещё ограничен integration scope, но это не блокирует проверенную доставку. Не извлекать значения и не запрашивать новые секреты.
2. `site-digest-default-branch-activation`: `.github/workflows/website-digest.yml` готов (UTC18:00 = МСК21:00), unit/YAML/live API dry-run проверены. Расписание не активно вне default branch. Для активации нужно отдельное разрешение только на этот infrastructure workflow в main; Pages legacy main:/ может автоматически rebuild-иться, поэтому разрешение должно учитывать побочный эффект. Workflow не переносит v2 сайт/не публикует APK. Без разрешения ничего в main не делать.
3. `site-approved-android-release`: владелец явно не утвердил APK. Download action выключен. Не добавлять dev screenshots как релизные, не рекламировать код разработки как выпущенные функции. Реальные feature cards/gallery/hero screenshot ожидают проверенной сборки.

## Неприкосновенные ограничения

Main SHA `9a0857ce260540ad604f344565d535a8d47b2fa0` сохранялся; Pages API подтвердил legacy source main:/. Read-only HTTPS `/` и `/privacy.html`: HTTP200 и bytes равны origin/main. CNAME/privacy в development не изменены. Не делать main update, merge, PR, deployment, public APK download или снятие noindex без соответствующего отдельного разрешения. Не трогать Android/другие клиентские проекты и активные сессии. Сайт только для Android.

Все существенные инструкции и evidence находятся в Git; /tmp не единственный источник состояния. Перед продолжением fetch/status/remote inspection и проверка активного писателя обязательны. Историю не переписывать, чужую работу не перезаписывать.

## Приоритетная проверка Telegram · 18.10.2026 10:47 МСК

Владелец явно запросил безопасный повторный тест; выполнен `gh run rerun 39107499146 --failed`, без изменения workflow/code. Attempt2 завершился success, check-config подтвердил доступность обоих bindings. Check-run117620640488 содержит Telegram accepted: commit87fd265846a415e9e0d53cf7e4dee4ca2d5fe25c message_id67. Это реальный API acknowledgement, не mock или просто exit0. Evidence docs/verification/telegram-delivery-2026-10-18.json; прежний failed evidence сохранён отдельно. Существующий action закрыт, notification-side code fixes не потребовались. Main/publication gate не менялись.

## 4C · Edge и текущее продолжение

Edge Stable155.0.4283.62 проверен отдельно:16/16 viewport/theme,4 axe runs без violations; menu/FAQ/theme/gallery/focus/no-JS и native tap/CDP swipe PASS. Официальный пакет проверен через подписанный Microsoft index и извлечён только в /tmp. Evidence docs/verification/edge-results.json;2 screenshots в docs/screenshots/edge-*.png. Native Safari/iOS/Android и screen reader ещё не проверены.

**Эта точка продолжения закрыта4D:** text resize/spacing/reduced motion/skip link выполнены; native400% zoom не заявляется проверенным.

## 4D · финальный доступный draft QA

Исправлены2 реальных дефекта: main теперь получает фокус по skip link (`tabindex=-1`), enlarged text переносится в grid (`body overflow-wrap:anywhere`). Optional оснастка tests/accessibility_qa.py реально выполнена в Chromium/Firefox/WebKit/Edge:48/48 text resize/spacing cases PASS, reduced-motion/skip focus PASS. После изменения inputs все4 обычные matrices также повторены:64/64,16 axe runs0violations, gallery/menu/theme/no-JS PASS.12 comparative screenshots побайтно совпали;17 unit build/workflow PASS. Evidence docs/verification/accessibility-adaptation.json содержит отрицательный baseline и финальные cases;2 screenshots добавлены. Все ограничения и exact next — выше и в docs/QA.md.

Процесс http.server8001 из старой сессии отвечал empty reply; не остановлен, не используется. Отдельный draft8002 реально обслуживал QA; при новой сессии запустить/reuse собственный правильный server. Edge binary извлечён в /tmp/website-edge с signed-index provenance в evidence. Никакие binaries/QA node_modules в Git не добавлены. После текущего checkpoint проверить remote SHA и обычный Actions notify ack; не создавать endless doc commits ради записи собственного SHA/следующего ack.

## R1 · первый coming-soon website-кандидат

Уточнение владельца сохранено в AGENTS.md (раздел первого инкрементального релиза), не заменяет master spec. Pending release copy стал пользовательским «Скоро», поля карточки вынесены в data/site.json. Release/publication data и validate gates не изменены. tools/package_preview.py собирает allowlisted noindex artifact + manifest; website-checks добавляет только upload-artifact, без Pages/deploy/новых write permissions. Порядок публикации/rollback и точный предмет owner approval — docs/FIRST_RELEASE.md. Текущая продолженная задача — проверить удалённый artifact после CI, не остановиться на его подготовке. Последний verified remote22ac98a: run39109916839 success/Telegram accepted90.

## R2 · подготовка проверки фактического artifact

Local rehearsal tests/review_artifact_qa.py:4/4 rendered views PASS, noindex/coming-soon/no download/privacy/resources/digest проверены. Первый harness run неверно сравнивал CSS-uppercase innerText с mixed-case copy; исправлено casefold, повторный run PASS. Это ошибка оснастки, не дефект сайта. CI round-trip ещё не выполнен на момент этой записи; не считать его доказанным до annotations. В workflow добавлены pinned download-artifact v4 и optional pinned Python Playwright в task-local venv; браузер — существующий Chrome runner, без system install/deploy.

Cloud onboarding draft: storage host добавлен к прежним4custom domains с сохранением package_managers preset; start_skill обновлён для текущего приоритета и loopback8002. Save подтверждён, requires_publish=true; runtime не менялся. Активация через save/publish настроек среды нужна только если возобновлять прямое скачивание из cloud. CI alternative проверяется независимо; не запрашивать новый GitHub/Telegram token.

## R2 · проверка завершена

Run39110644873: verify/notify success. Check-run117625868753 notice Website review archive verified подтверждает настоящий round-trip сохранённого artifact, clean source0b4eb54, inner ZIP SHA7877e610…,22files/4Chromeviews, noindex=true/APK=false/page_errors0. Artifact12130197561 (website ZIP+manifest), verification artifact12130182655. Telegram accepted109. Evidence docs/verification/review-artifact-status.json. Cloud direct download остаётся403; это не препятствует CI proof, не требовать смены credentials. Нет hosted preview URL; доступен review artifact. Next — неприменённый proposed policy diff для предметного owner review.
