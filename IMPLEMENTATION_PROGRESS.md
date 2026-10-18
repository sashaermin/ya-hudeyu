# Реализация сайта «Я ХУдЕЮ»

Единственная общая дорожная карта Codex / Claude Code / других агентов. Основание: неизменённый [мастер-ТЗ](project_specs/WEBSITE_MASTER_TZ_2026-10-18.md). Общие правила — AGENTS.md, текущее продолжение — AGENT_HANDOFF.md.

| Этап ТЗ | Цель / критерии | Состояние и checkpoint | Проверки / остаток |
|---|---|---|---|
| 0. Аудит | Источники, токены, ресурсы, различение release/dev | Аудит выполнен, `a4de44b` | Android SHA зафиксирован; пути/активы описаны. APK и release screenshots ожидают решения владельца. Первоначально Pages API недоступен; в4B подтверждён legacy main:/ и HTTPS preservation. |
| 1. Дизайн-основа | Оригинальный бренд, CSS-токены и обе темы, адаптивный каркас | Реализован `356eaef` | Сверены оригинальные ресурсы; node syntax PASS. Матрица/контраст подтверждены в4A/4B, owner visual acceptance pending. |
| 2. Контент / секции | Hero, возможности, gallery, установка, FAQ, footer | Каркас и взаимодействия `24ca8d5`; релизный контент частично заблокирован | Draft build PASS; JS syntax PASS; CNAME/privacy побайтно сохранены. Реальные скриншоты, публичные функции и hero screenshot не добавлены без подтверждённой сборки. |
| 3. Загрузка / SEO | Проверенный APK, checksum/версия/совместимость, метатеги, performance | В работе | Download gate реализован, draft noindex, production build блокируется. Gate tests PASS, WOFF2/SEO/релизная документация реализованы (`a14a2c6`); APK ожидает утверждения. |
| 4. QA | 8 ширин × 2 темы; клавиатура, touch, ссылки, axe/Lighthouse, screenshots | В работе | 16/16 Chromium viewport/theme PASS, 4 axe runs 0 violations, keyboard/touch/gallery PASS. Lighthouse 96/100/100/69 (draft noindex); 4 screenshots сохранены. Firefox/WebKit также проверены (4B); физические устройства, отдельные Edge/Safari и release content pending. См. docs/QA.md. |
| 5. Публикация | Одобрение владельца, main/deploy, HTTPS/APK/rollback | Не разрешена, не начата | Нельзя менять main, PR/merge/deploy/publish APK без отдельного разрешения. |

## Дополнительный разрешённый этап W1 — общая работа агентов и уведомления

Объём: общие инструкции, handoff, прогресс, сохранение оригинального ТЗ, сайт-специфичный Telegram через Actions, стабильные event/action IDs. Без Android-записи и без default-branch schedule.

Критерии: единые инструкции без конфликта, только один писатель, детерминированные mock-тесты уведомлений/экранирования/дедупликации/секретов, корректный workflow без deploy, реестр pending APK. Прямой Telegram send из cloud запрещён; фактическая доставка требует доступного Actions run. Локально проверено: 30/30 notification tests PASS без skip; 11/11 build/workflow tests PASS; YAML parsed. Удалён только Android-only repository milestone registry test: состояние сайта хранится в общем tracker, не в дублирующем roadmap registry. Доставка и remote CI run не подтверждены (API 403).

## Решения владельца и открытые ограничения

- APK не утверждён (прямое подтверждение владельца 18.10.2026); registry `site-approved-android-release`.
- Нет подтверждённых release screenshots; не подменять интерфейс.
- Telegram bindings восстановлены: live sendMessage ack67 и последующий push ack77; registry `site-telegram-settings-verification` resolved. Исторические failed runs ниже сохранены как журнал.
- Digest 21:00 МСК обязателен и подготовлен в website-digest.yml; активация требует разрешения на default-branch workflow, main не разрешён.
- Визуальное сходство подтверждает владелец на этапе приёмки, юридические изменения согласуются отдельно.

## Журнал проверок

- До `24ca8d5`: Python draft build PASS; node --check обоих scripts PASS; privacy/CNAME равны origin/main.
- Первый Chromium 1440px: pageerror 0, scrollWidth = viewport, fonts loaded; снимок временный `/tmp/website-first-desktop.png`, итоговые screenshots будут сохранены в Git на этапе 4.
- W1 первоначальная адаптация Android notification tests: 31 test, 4 failure и 3 skip. Причины: ожидавшиеся старые названия сообщений/путь HANDOFF.md и отсутствующие новые регистры. Ожидания адаптированы к сайту, регистры добавлены; повторный запуск обязателен. Не считать этот run успешным.
- Build regression tests: 10/10 PASS (блокировка неподтверждённых APK/функций/screens, HTTPS/path safety, экранирование и повторяемость сборки).

- W1 checkpoint `227ab74` подтверждён на remote. Этап 3A: WOFF2 178264 bytes вместо 563240 bytes TTF (−68%); оригиналы и лицензии сохранены. Build/workflow 12/12 PASS; explicit owner approval требуется отдельно от status verified. RELEASE_CONTENT/README добавлены; реальный APK остаётся pending.

- W1.1: stage report соответствует общему формату сайта; `done/next` сохраняются в событиях; повторный CI failure report дедуплицируется по run_id/status. 33/33 notification tests PASS (mocks, без сетевых отправок).

- Этап 4A: все независимые draft проверки завершены, доказательства и 4 screenshots — docs/QA.md. Production build проверенно блокируется exit 1. Исправлены focus trap и performance 86→96; ошибки оснастки theme/touch отделены от дефектов сайта. Интеграция с реальным APK и production QA ещё не выполнены.

- 18.10.2026 09:48 МСК: сетевые browser downloads попробованы и получили 403; сохранён config draft с start_skill и additive domains. Новое owner action site-network-crossbrowser-qa. Проверено npm ci (202 packages); provenance bytes/полный cmap WOFF2 PASS. Проверка фактического Actions run, environment activation/new-task restore не выполнялась.

Итоговый проверенный implementation checkpoint этапа 4A: `b3ffaf9ceb9d7f998e673468bfb4a0718393b961` (remote подтверждён). Разрешённая независимая работа выполнена; продолжение — сетевой доступ/оставшиеся браузеры и утверждённый APK/screens. Этапы 2–4 частично открыты по release/owner/device критериям; этап 5 не разрешён и не начат.

## Новый автономный цикл: W2 и 4B

Инструкция владельца сохранена в project_specs/AUTONOMOUS_EXECUTION_2026-10-18.txt. Сеть разблокирована для CDN/домена/API; прежний network action resolved, успешный Chromium QA не повторяется. Первая задача: определить причину notify failure по Actions evidence, подготовить обязательный daily digest 21:00 МСК без записи в main; параллельно установить доступные браузеры и продолжить 4B. verify run 39105427770 success, notify failure; metadata secrets 403 по integration permissions.

W2A проверен: автономная инструкция сохранена; сеть CDN/API/домена подтверждена, старый action resolved. Официальные Firefox153/WebKit26.5 скачаны. Notification probe + digest workflow подготовлены; 36 notification и 13 build/workflow tests PASS, YAML parsed; dry-run настоящего GitHub API без Telegram отправки PASS. Workflow actions v5 refs сверены с upstream и закреплены SHA. Daily schedule не активирован: main permission action site-digest-default-branch-activation. Pages API подтвердил legacy deployment из main:/; production не меняется.

4B завершён в доступном объёме: Firefox153/WebKit26.5 по16 ширин/тем, по4 axe runs (0 violations), keyboard/focus/theme/gallery/no-JS PASS; runtime helper и engine QA recipes проверены. Firefox touch и WebKit native swipe/device Safari/Edge остаются отдельными непроведёнными checks. Production HTTPS побайтно равен main; Pages legacy source main:/ подтверждён read-only. Доставка Telegram теперь конкретно блокируется missing bindings по check-run annotations39106472358.

3B: отдельный gate site-publication (data/publication.json=false) и независимые APK/site approval tests реализованы. 17 build/workflow tests PASS; исходный draft HTML сохраняется побайтно, browser/Lighthouse QA не повторялся. JSON-LD escaping исправлен и подтверждён round-trip test. Main/deploy/noindex/download статусы не менялись.

W2B: восстановление пропущенных action/event records с ledger + dedup API warnings реализовано; 40 notification tests PASS. Итог текущих focused unit suites: 40 notification + 17 build/workflow = 57 PASS (на актуальных затронутых inputs). Browser artifact после3B побайтно прежний, поэтому 48 viewport/theme runs и12 axe runs валидны без повторения. Остаток: настройкиbindings, разрешениеdigestmain, APK/screens и owner/device release acceptance.


## Актуальное состояние · 18.10.2026 10:22 МСК

| Завершённый независимый checkpoint | Доказательства | Открытая граница |
|---|---|---|
| W2A `9ca5397` | 36 notify +13 build/workflow tests, YAML/live API dry-run PASS | Daily schedule вdevelopment не активен; нужно разрешение default-branch infrastructure update |
| 4B `46b824d` | Firefox/WebKit по16 combinations и4 axe, 0violations; runtime helper PASS | Физические устройства и отдельные Safari/Edge; native WebKit swipe не проверен |
| 3B `237fc81` | 17 build/workflow tests PASS; отдельный publication gate, реальный artifact hash сохранён | Нет APK/site publication approvals, production build не разрешён |
| W2B `ad7c5a0` | 40 notification tests PASS; backlog recovery, partial retry, dedup/ack | Два Telegram bindings отсутствуют; реальная доставка не подтверждена |

Run39107259552: verify success, notify failure (missing TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID). Workflow целиком не прошёл, deployment в нём нет. Network action resolved по фактическому доступу, нового действия с настройками сети не требуется. Следующие незавершённые approved задачи зависят от перечисленных внешних prerequisites; повторный запрос тех же неизменившихся действий не нужен. Мастер-ТЗ целиком не закрыто: релизные функции/screens, визуальное/юридическое/device принятие и отдельная публикация ещё впереди.

## Telegram priority verification · 18.10.2026 10:47 МСК

По прямому запросу владельца повторён existing notify mechanism: run39107499146 attempt2 success; check-config success; Telegram accepted message_id67 для87fd265. **Telegram: DELIVERED** в смысле подтверждённой отправки Telegram, без утверждения о прочтении человеком. Missing bindings action resolved, код исправлять не потребовалось. Сохранены live jobs/annotations/evidence и прежний failed snapshot. Scope main/production/deployment/publication gate сохранён. Остальные owner gates не считаются снятыми.

## 4C · отдельный Microsoft Edge

Цель: закрыть отдельную проверку Edge по этапу4 без повторения Chromium/Firefox/WebKit. Критерии:16 ширин/тем,4 axe runs, основные взаимодействия, no-JS, отсутствие runtime errors; официальный browser binary с проверяемым происхождением.

Результат: Edge155.0.4283.62 —16/16 PASS,4 axe runs0violations; theme/menu/FAQ/gallery keyboard/focus/Escape/error/native tap/CDP swipe/no-JS PASS. Пакет Microsoft SHA-256 и signed index проверены; система не изменена. Evidence docs/verification/edge-results.json,2 owner-review screenshots. Совокупно64 viewport/theme и16 axe runs; это не физические устройства/Safari и не проверка релизных screens. Следующая независимая задача: text resize/reflow/reduced motion.

## 4D · доступность и исправления

Цель: закрыть доступные text resize/spacing/reduced-motion/skip-link критерии этапа4. Объём ограничен двумя найденными дефектами и воспроизводимой optional browser QA оснасткой, без новых продуктовых функций.

До исправления: skip target не получал фокус; text200% переполнял320/390px в обеих темах. После `main tabindex=-1` и `body overflow-wrap:anywhere`:48/48 дополнительных случаев в4 браузерах PASS; reduced-motion/keyboard skip PASS. После изменения HTML/CSS повторены4 обычные matrices:64/64 PASS,16 axe runs0violations;12 ранее сохранённых comparative screenshots побайтно совпали.17 build/workflow unit tests PASS. Evidence docs/verification/accessibility-adaptation.json,2 дополнительных screenshots; browser evidence обновлён. CSS text simulation не называется native zoom или screen reader проверкой.

**Первое незавершённое действие:** после решения владельца `site-approved-android-release` проверить конкретный APK и подключить подтверждённые функции/screens по docs/RELEASE_CONTENT.md, затем провести affected QA. Независимых задач с имеющимися входами больше не найдено. Остальные открытые границы: visual/legal/device acceptance, отдельное main authorization для daily digest, отдельное разрешение публикации. Главные этапы2–4 частично открыты, этап5 запрещён. Main/production/deployment/publication gate/noindex/download не изменялись. Последний подтверждённый remote до4D:6958c0d; его Actions success/Telegram accepted84.
