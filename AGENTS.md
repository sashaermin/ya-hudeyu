# Общие инструкции разработки сайта «Я ХУдЕЮ»

Авторитетный документ для Codex, Claude Code и будущих агентов. GitHub — единый источник состояния. Пользовательские инструкции имеют приоритет. Последнее подтверждённое решение владельца: продолжать сайт автоматически; APK для публичного распространения **не утверждён**.

## Возобновление и единственный писатель

Порядок resume/fetch/единственного писателя и передачи хранится в [AGENT_DEVELOPMENT_PROTOCOL.md](AGENT_DEVELOPMENT_PROTOCOL.md). Это общий протокол Claude Code/Codex/других разрешённых агентов, без постоянного владельца-агента. Прочитать его и handoff до изменений; не опираться на историю чата.

## Область и запреты

- Рабочая ветка сайта `sashaermin/ya-hudeyu`: `work/website-v2`, создана от main. Сохранять main, production, CNAME и существующий privacy.html.
- **Без отдельного явного разрешения владельца запрещены**: изменение main, merge, PR, deployment, публикация APK. Обычный checkpoint commit/push рабочей ветки разрешён.
- Android `sashaermin/ya-hudeyu-android` строго read-only, включая `work/activity-progress-v6-4daeaa5`. Не менять его код/ветки/сессию/процессы, не запускать Android-разработку.
- Только Android в контенте сайта. Не предлагать другие клиентские платформы.
- Утверждённое мастер-ТЗ: `project_specs/WEBSITE_MASTER_TZ_2026-10-18.md` — исходный файл владельца, хранить без переписывания. Единственная дорожная карта — IMPLEMENTATION_PROGRESS.md, по этапам этого ТЗ.
- Реальные брендовые ресурсы и токены берутся из Android с SHA и путём в ASSET_SOURCES.json. Не генерировать замену маскоту/скриншотам и не выдумывать APK/функции/отзывы/показатели.
- Код в Android-ветке не доказывает выпуск. APK требует выбора и разрешения владельца, технической проверки и доказательств. До этого download action недоступен, full production build блокируется; coming-soon разрешён только по отдельной site policy/авторизации ниже. Визуальное и юридическое одобрение перед выпуском остаются обязательными.
- Не публиковать внутренние отчёты и конфигурацию. Публикуемый артефакт — только `_site`, генерируемый белым списком; никогда не выкладывать корень checkout как готовый сайт.

## Короткие этапы и доказательства

Канонический порядок ограниченных проверяемых этапов, checkpoint и handoff: [AGENT_DEVELOPMENT_PROTOCOL.md](AGENT_DEVELOPMENT_PROTOCOL.md). Выполнять его при каждом возобновлении/передаче, независимо от агента.

## Проверки и запуск

- `python3 tools/build.py` → draft `_site` с noindex; `python3 -m http.server 8002 --bind 127.0.0.1 --directory _site`.
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`.
- `python3 -m unittest discover -s .github/scripts -p 'test_*.py' -v`.
- `node --check scripts/site.js` и `node --check scripts/theme.js`.
- Браузерный QA, его зависимости и артефакты — README и docs/QA.md, когда доступны. Нельзя выдавать непроведённые проверки браузеров/устройств за PASS.
- Не создавать git worktree без явной просьбы: облачная задача уже изолирована; использовать существующий checkout.

## Уведомления и отчёты

Следовать AGENT_NOTIFICATION_PROTOCOL.md. Не отправлять Telegram из локальной сессии: отправляет GitHub Actions после push. Используется существующий бот «Я ХУдЕЮ | Dev Reports», repository secrets TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID. Значения никогда не читать/печатать/коммитить. Не создавать нового бота. Проверять только имена/наличие секретов; отсутствие переменных в облачной машине не доказывает отсутствие Actions secrets.

Каждый commit снабжать каноническими provenance/report trailers по [AGENT_NOTIFICATION_PROTOCOL.md](AGENT_NOTIFICATION_PROTOCOL.md); CI проверяет их через `report-check`. Значения агента, единая HTML-иерархия, описательные ссылки и escaping определены только там. Сохранять этот стандарт для всех видов событий; оформление не меняет механизм доставки. Не определять агента по автору/runner/ветке. Изменения статуса этапа регистрировать в project_specs/agent_events.json; решения владельца — в project_specs/user_actions.json. Для open → resolved записать resolution, чтобы workflow отправил закрытие. Нельзя дублировать события под новым id.

Короткие пользовательские отчёты только по-русски:

Сделано: …
Проверено: …
Далее: …
Требуется от меня: … (только при реальном действии владельца, с краткими нумерованными шагами).

## Автономное продолжение · указание владельца 18.10.2026

Оригинальная постоянная инструкция всех агентов сохранена в `project_specs/AUTONOMOUS_EXECUTION_2026-10-18.txt`. Она дополняет утверждённое мастер-ТЗ, не заменяет его. Продолжать все разрешённые этапы без промежуточного запроса согласия: реализация, UI, исправления, допустимые зависимости, проверки, документы, commit/push и переходы разрешены.

Проверять блокер настроек среды доступными tools; сохраняемый draft и его фактическая активация — разные операции. Не считать публикацию среды deployment сайта. Если платформа требует действие владельца, зарегистрировать его один раз и продолжать независимые задачи. Не спрашивать заново о неизменившемся блокере.

Daily digest в **21:00 Europe/Moscow теперь обязателен** (раньше был опциональным). Реализовать и проверить всё доступное в рабочей ветке; запуск GitHub schedule из default branch по-прежнему требует отдельного разрешения на main. Нельзя скрывать этот неустранённый предел или обещать работу неактивного расписания.

Сохранять intentional noindex до **отдельного разрешения публикации сайта**, независимо от утверждения APK. Скачивание APK остаётся выключенным, пока владелец не выбрал и явно не разрешил конкретный артефакт. Подтверждённые тесты не повторять без изменившихся входов или новой диагностики. Не трогать Android/другие клиентские проекты. GitHub остаётся единственным общим источником состояния, допускается только один активный писатель сайта.

Отдельное согласие на публикацию сайта фиксируется в data/publication.json только после явного разрешения владельца; approval APK в data/release.json этого не заменяет. Draft всегда noindex. Нельзя заполнять approval_reference вымышленным решением; тестовые значения допустимы только в изолированных in-memory test fixtures.

## Первый инкрементальный релиз · уточнение владельца 18.10.2026

Приоритет — подготовить редизайн главной и основные секции к первому отдельному website release. APK — отложенная независимая интеграция: его отсутствие не блокирует разработку и подготовку кандидата сайта; показывать честное «Скоро», без загрузки, дат и неподтверждённых возможностей. Мастер-ТЗ сохраняется, его полные APK/screens критерии остаются задачами последующего инкремента.

Существующие quality/publication gates не ослаблять. Default full `--production` требует APK/screens и site approval; отдельно согласованный coming-soon режим описан в R6/R7 ниже. Не обходить gates загрузкой draft. Main/production/DNS/CNAME/deployment не менять. Draft noindex сохранять. Архив проверенного draft для просмотра не означает разрешение публикации или доступное веб-превью.

Эквивалентные правила автономного цикла выше действуют без дублирования: не останавливаться после отдельного checkpoint; выбирать следующую независимую задачу, не спрашивать разрешения на обычную работу в development branch. Остановка допустима только при отсутствии доступных approved задач, реальном блокере или завершении среды; перед ней сохранить проверенный handoff с точным следующим действием. Инструкции действуют для всех последующих агентов.

### Применённая политика первого релиза · R6

Владелец отдельно разрешил применение точного first-release-coming-soon.patch (SHA-256 cefd3cc1b1440efa0f09c67b557570e5c9a4f89d0b7f0c63df7b8b407f38fd03). Он применён: builder поддерживает explicit coming-soon без APK при отдельном реальном site approval и пустых features/screenshots. Default full gates сохранены. Это уточняет прежнее описание неприменённого proposal выше; не разрешает никаких дальнейших изменений gates. На историческом R6 checkpoint publication approved=false, release_mode не включён; текущее разрешение первого выпуска зафиксировано в R7 ниже, APK downloads выключены. Визуальная/юридическая приёмка и публикация конкретного SHA, main/deploy/indexing/rollback по-прежнему требуют отдельных решений.

### Первый production release · явная авторизация владельца

Владелец принял текущий coming-soon кандидат b12b0b0 и отдельно разрешил первый production release через существующий legacy Pages main:/, minimal public-only commit, проверку production и rollback при неуспехе. Точная область — project_specs/FIRST_WEBSITE_RELEASE_AUTHORIZATION_2026-10-18.md. data/publication.json отражает это реальное разрешение: approved=true, release_mode=coming-soon, indexing_approved=false. Production builder проверяет разрешение, контент и APK gates; noindex/nofollow и robots Disallow сохранены, не выдавать это за SEO-ready indexing. Это исключение только для данного первого выпуска, не общий доступ main/deploy и не разрешение будущих релизов/редизайна. APK approval остаётся false. Digest-main и другие workflows не активировать. При неуспехе — разрешённый revert publication commit к verified rollback9a0857c; не reset/force-push. После успеха только approved maintenance/QA, deferred redesign без новых указаний не начинать.

### Возобновление полного мастер-ТЗ после первого выпуска

После production verification владелец поручил продолжать весь approved master roadmap на work/website-v2 автоматически; первый coming-soon release не закрывает полное ТЗ. Текущий покритериальный checklist и зависимости — только IMPLEMENTATION_PROGRESS.md. Откладывать лишь конкретные APK-зависимые требования; выполнять остальные независимые approved задачи/QA по порядку, проверять/commit/push/remote/Telegram. Production/main без новой отдельной авторизации не менять, неизменённый сайт не redeploy; deferred redesign/новые вне-ТЗ features не начинать. Перед остановкой сохранить точный next и все оставшиеся требования. Проверенный R7 production публично доступен на9b39ffa; rollback9a0857c сохранён. Noindex/indexing_approved=false сохранять до отдельного owner решения. Live QA на normal-TLS runner включать лишь при реальной необходимости trailer Verify-Live-Production: true; он не означает deployment authorization.

### U0–U2 UI/UX-аудит и исправления

По новому заданию владельца аудит44 UI требований и объективные fixes выполнены вdevelopment, без нового визуального направления. Канонический gap/evidence report — docs/UI_UX_REQUIREMENTS_AUDIT.md, единственный roadmap — IMPLEMENTATION_PROGRESS.md. Current35 COMPLETE/0PARTIAL/0MISSING/7release-blocked/2manual. Не объявлять full master завершённым, не повторять verified fixes. Current preview hashes — docs/verification/current-preview.json; historical approved production/release-candidate evidence сохранять. Privacy presentation исправлена, но все legal headings/paragraphs/date/links сохранены; любые будущие legal text changes требуют согласования. Новые UI changes не разрешены кпубликации старым approval первого release. Main/production9b39ffa, APK restrictions иnoindex сохранять до соответствующих отдельных разрешений.

### U3 · узкая авторизация UI/UX production update

Владелец прямо разрешил выпуск проверенных UI corrections из0b706e3/2981a45/6798295: только index/privacy presentation/CSS/JS и необходимые уже проверенные public assets. Это новое исключение к прежнему запрету публикации UI fixes; полная область project_specs/UIUX_PRODUCTION_AUTHORIZATION_2026-10-18.md. Разрешены public-only main commit через текущий Pages, live verification и rollback к9b39ffa при confirmed critical regression, без дополнительного подтверждения. CNAME/DNS/Pages/HTTPS/legal text/coming-soon/noindex/APK-disabled неизменны. Никаких unrelated workflows/digest, других repo, features или redesign. Actual release/evidence/точный next — AGENT_HANDOFF/docs/verification/uiux-production-release.json; эта авторизация не распространяется на будущие releases. Live QA использует normal TLS и явный current manifest; fixtures только внутри браузера, не вpublic tree.

U3 исполнен иverified: production8fb7bf2/Pages39129023427/live39129135130 success. Rollback9b39ffa истарый9a0857c сохранены. Нельзя повторно использовать данную owner authorization для новой UI/features публикации; currentnoindex/APK-disabled остаются. Все futureagents читают текущий handoff/manifest, не исполняют исторические Exact next/publish steps изжурнала.
