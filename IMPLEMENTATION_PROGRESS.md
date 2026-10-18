# Реализация сайта «Я ХУдЕЮ»

Единственная общая дорожная карта Codex / Claude Code / других агентов. Основание: неизменённый [мастер-ТЗ](project_specs/WEBSITE_MASTER_TZ_2026-10-18.md). Общие правила — AGENTS.md, текущее продолжение — AGENT_HANDOFF.md.

**Актуальный срез R7/R8:** первый coming-soon website release опубликован и проверен: production9b39ffa, Pages39114713056 success, live browser39125147955 PASS. Это **не завершение мастер-ТЗ**. Исторические записи ниже — журнал, текущее состояние и независимые next tasks определяет следующая таблица. APK не блокирует уже опубликованный сайт; только соответствующие пункты deferred. Production без новой авторизации не менять.

| Этап ТЗ | Текущее состояние | Проверенные критерии и незавершённое |
|---|---|---|
| 0. Аудит | Выполнен для исходного design/source SHA | SOURCE_AUDIT/ASSET_SOURCES/DESIGN_MAPPING; релизный APK/source audit отложен до выбранного артефакта. Android/другие проекты не изменены. |
| 1. Дизайн-основа | Реализована; первый визуальный кандидат принят владельцем | Оригинальные бренд/маскот/шрифты/tokens, обе темы, адаптивность и состояния. Полное сравнение release screens зависит от APK. Deferred redesign не разрешён. |
| 2. Контент/секции | Coming-soon вариант опубликован; full-content открыт | §4.1–4.8: навигация, hero с маскотом, безопасные empty states, установка, FAQ, footer/privacy работают. CTA скачивания, hero screenshot, features, gallery реальных screens и release-specific FAQ deferred до APK evidence/approval. Неподтверждённых claims нет. |
| 3. Загрузка/SEO | Независимая инфраструктура готова; APK integration deferred | data configs, release gates, метатеги/canonical/OG/Twitter/favicon/robots/sitemap и SoftwareApplication с достоверными полями реализованы; версии/size/SHA/minAndroid/changelog/URL и настоящий download не заполнены без артефакта. Intentional noindex/Disallow сохранён, SEO target исключение политики. |
| 4. QA | Автоматизированный QA выполнен, production Lighthouse следующий | Исторический4D:64 browser viewport/theme +16axe; послеR1 copy Chromium16/4axe и48 adaptation cases. Актуальный live coming-soon:16 Chrome cases320–1920×темы, меню/FAQ/theme/no-JS PASS,22files/12internal404 PASS. Physical Android/iOS/Safari, screen reader/native zoom и native WebKit swipe не выполнялись; требуют устройства/ручного оператора. Не выдавать engine emulation за device tests. |
| 5. Публикация | Первый coming-soon выпуск завершён по отдельному разрешению | Pages39114713056/production9b39ffa/HTTPS/privacy/CNAME/public allowlist verified; rollback tag9a0857c. Полный APK-сайт и дальнейшие releases не разрешены этим выпуском. |

### Чеклист остатка мастер-ТЗ (единственный roadmap, без нового ТЗ)

| Требование | Статус / зависимость | Точное следующее действие |
|---|---|---|
| §3, §7.1–3 release audit/APK | Deferred: нет approved APK | После owner artifact approval проверить manifest/signature/version/size/SHA/URL/реальный download по RELEASE_CONTENT.md. |
| §4.1/4.2 download CTA/hero screen | Deferred: APK/screens | Подключить только утверждённые реальные screens и download, affected QA; не генерировать интерфейс. |
| §4.3 verified feature cards | Deferred: release evidence | Проверить каждую функцию в выбранной версии; добавить реальные icons/evidence, не обещать dev features. |
| §4.4 gallery real content | Deferred: release screens обеих тем | Generic gallery/error/focus/swipe реализованы и проверены на явно test-only fixtures; публикация actual screens после approval. |
| §4.5/4.6 versioned installation/release data | Deferred: APK | Не выдумывать совместимость, дату, версию, URL, changelog. |
| §4.7 sync/backup/update FAQs | Deferred только release-specific ответы | Текущие честные установка/privacy/support FAQs готовы; уточнить release-specific поведение по APK/code/doc evidence. |
| §5/6/7 browser/device/manual accessibility | External manual capability | Physical Android Chrome/iOS Safari, standalone Safari, real screen reader/native zoom/WebKit swipe; automated engines и axe не заменяют эти проверки. |
| §6 production Lighthouse mobile ≥90/95/95/95 | Independent R8: подготовлен read-only runner замер | Получить actual scores/metrics; устранить обоснованные defects только в development, deployment отдельно. SEO<95 при intentional noindex документировать как разрешённую причину отклонения. |
| §6 SEO indexing | Owner policy decision, не APK blocker | Сейчас indexing_approved=false; не включать только ради score. |
| §7.8 screenshots/visual acceptance | Первый coming-soon кандидат принят | Снимки4тем/ширин сохранены; release-specific full UI сравнение и приёмка после настоящих screens. |
| §8 final full release | Deferred: release content/приёмка + новая production authorization | Первый coming-soon не закрывает требования APK/download и не разрешает следующий production push. |
| Shared notifications21:00 МСК | Prepared; owner main-workflow authorization required | Digest schedule default branch ещё не активен; не менять production/main для этого без отдельного разрешения. |

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

## Приоритет первого инкрементального релиза · R1

Новое указание владельца: первый сайт с редизайном/основными секциями и «Скоро» готовится независимо от APK. Полные APK/features/screens — deferred инкремент мастер-ТЗ, не blocker website readiness. Это уточняет прежний exact next4D; master не заменён. Existing production/publication gates не меняются без отдельной авторизации.

R1 scope: пользовательское coming-soon состояние, воспроизводимый allowlisted noindex ZIP/manifest, review artifact после verify в существующем Actions (не hosting/deploy), процедура публикации/отката docs/FIRST_RELEASE.md. Критерии: нет APK/download/unverified claims, noindex сохранён, archive reproducible/без internal files, source SHA/dirty state честные, QA копирайта и archive check. Следующий независимый шаг R2 — скачать именно CI artifact, проверить bytes/manifest и локально открыть реальный архивный rendered сайт. Owner policy action зарегистрирован один раз; не просить APK как prerequisite website-кандидата.

R1 проверен:18 unit tests PASS, включая воспроизводимость allowlisted noindex ZIP; current copy Chromium16/16 и4 axe0violations;48 text adaptation cases в4браузерах PASS.4 candidate screenshots сохранены. Workflow YAML parsed, upstream upload-artifact v4 SHA закреплён, deployment/write permissions не добавлены. СледующееR2: фактическое скачивание CI artifact, source/digest проверка и isolated local rendering.

R2: R1 remote52ba269 подтверждён; run39110310967 success, Telegram95, artifact12130660202 создан. Прямой cloud download403 на blob host; evidence не выдаётся за успешный download. Local archive rehearsal4/4 views PASS, source/digest/allowlist/privacy/noindex/no download проверены. Добавлен реальный round-trip download/render step на GitHub runner; его запуск и proof пока pending. Workflow YAML и2 workflow contract tests PASS. Следующее действие — проверить этот новый CI, затем завершить R2, сохранив proof и точный owner next.

R2 завершён и проверен: remote0b4eb54, run39110644873 success; реальный download-artifact и browser-render проверили22files и4views, noindex/noAPK/page_errors0. Notice117625868753 сохранён, Telegram109; review artifact12130197561, verification artifact12130182655. Cloud403 не блокирует доказанный CI round-trip. Следующий независимый шаг подготовки — review-only coming-soon policy diff и изолированные проверки без изменения текущего gate.

R3 подготовлен: review-only patch first-release-coming-soon.patch не применён к рабочему builder/config. git apply --check и isolated apply PASS;15 existing build+5 proposed policy tests PASS. Default full gates сохранены, explicit coming-soon требует настоящего site approval и запрещает APK/features/screens. Предмет owner решения конкретен, APK не prerequisite первого сайта. В ходе проверки workflow найден оставшийся retry issue: immutable upload-artifact name совпадёт при rerun того же run. Следующий независимый шагR4 — добавить attempt-specific artifact names и проверить реальный безопасный rerun/dedup.

R4: upload/download review artifact и verification evidence names дополнены run_attempt. Это делает attempt provenance явным; предполагаемая collision не выдаётся за воспроизведённый дефект. Overwrite/delete самим workflow не используется, но сохранность старых IDs зависит от платформы. Workflow YAML/name matching и existing contract tests проверяются локально, реальный attempt2 round-trip/dedup — после push, пока не считается PASS.

R4 фактически проверен: run39110987166 attempts1/2 success, оба actual archive notices с22files/4views и одинаковым inner ZIP SHA. Telegram127 толькоattempt1, duplicate commit notice вattempt2 отсутствует. API дляattempt1 artifact IDs вернул404, поэтому прежние URLs/сохранность не обещаются. Evidence artifact-retry.json содержит это ограничение. Следующий targeted R5: actual runner annotation обнаружила Node20 deprecation новых v4 artifact Actions; upstream current stable v7.0.2 upload /v8.0.2 download используют Node24, совместимые inputs сверены и refs закреплены SHA. Новые Action versions требуют своего live round-trip, пока pending.

R5 завершён: remotefec5137, run39111335266 success. Official Node24 artifact Actions реально выполнили upload→download/22file validation/4Chromeviews; Node20 annotation отсутствует, Telegram accepted138. Active gate AST unchanged since22ac98a, real approvals false/unverified, CNAME/privacy equal main. Evidence artifact-node24.json. Доступные independent approved задачи завершены; exact next — owner review кандидата/неприменённого patch, затем по конкретной авторизации. APK не блокирует website readiness, actual deployment остаётся запрещённым. Handoff сокращён до текущих фактов с ссылками на сохранённую историю/evidence.

## P1 · постоянный cross-agent протокол и русские Telegram-отчёты

Цель: взаимозаменяемость Claude/Codex без чата и канонический русский формат существующего Telegram. Объём: AGENT_DEVELOPMENT_PROTOCOL.md (перенесены существующие resume/checkpoint правила, не второй roadmap), ссылки из AGENTS/CLAUDE/handoff/notification/workflow; precise agent provenance, обязательные Report-* trailers и CI report-check; единообразные русские agent labels, archive-review event; digest читает текущий Exact next marker.

Критерии: четыре допустимых Agent labels, без автор/runner/prefix inference; exact commit fields/direct URL, honest head-only workflow verification; entity-safe Telegram limit; неизменённые ledger keys/секреты/чат; repository-only cold-start и честное real_transfer=false. Первоначальные4 format-fixture/regression failures исправлены: escaped-size limit, SHA/partial-retry fixtures нового шаблона, обязательная archive URL для нового event type. Финально47 notification tests PASS и20 site/workflow/handoff tests PASS; build/JS syntax PASS, draft HTML byte-identical. Evidence docs/verification/cold-start-handoff.json. Browser matrices не повторялись без изменения public artifact. Remote CI/notification confirmation — после checkpoint, не подменять local mocks live delivery.

Текущий website roadmap/дизайн/master/publication gates не меняются. После P1 проверок продолжение — прежняя приёмка website-кандидата и owner authorization конкретного неприменённого patch; новое постоянное указание не разрешает его применение/main/deploy/noindex/download.

P1 checkpoint24c5102 независимо подтверждён на remote, run39112341703 success:67 tests и actual archive round-trip/render PASS; Telegram157. Добавлена последняя attribution regression: milestone source берётся только из собственной записи, head-commit hints не используются. Финально48 notification tests PASS (теперь68 active unit tests вместе с20 site/handoff); code/UI/gates не меняются. Evidence permanent-agent-protocol.json. Roadmap возобновлён с прежнего exact next: owner acceptance и разрешение неприменённого patch; этого разрешения новое указание не содержит. Новых независимых approved задач не найдено, повторный запрос неизменившегося решения не создаётся.

## T1 · единое визуальное представление Telegram

Цель: применить общий русский HTML presentation standard ко всем сообщениям, сохранив инфраструктуру. Начато после verified8888818/run39112501232 success; существующие website checkpoints сохранены. Объём ограничен message rendering, safe escaping/links, форматными тестами и canonical docs. Triggers/secrets/concurrency/ledger IDs/routing не меняются.

Реализованы bold project/event header + metadata + отделённые секции + descriptive footer links; code branch/hash/technical IDs. Commit/stage/milestone/CI/action/resolution/digest/preview/warnings используют одну иерархию. HTTPS URL validation отклоняет credentials/injection/invalid ports, не печатает значения. Balanced HTML/entity truncation сохраняет footer. Первые7 failures относились к старым layout ожиданиям; ожидания адаптированы без снятия assertions о содержимом/порядке/дедупликации.51 notification tests PASS, в том числе3 новых parser/security/long-message проверки. Build/website QA и доказательство неизменности защищённых областей — перед checkpoint. После задачи возобновить прежний roadmap; owner policy patch всё ещё неприменён.

T1 итог локально:51 notification +20 site/workflow/handoff tests PASS; draft build PASS/HTML byte-identical. AST send/pushed_commits/load_ledger/run_ci_report/run_digest/action_transitions/new_events неизменён относительно safe8888818; оба workflows, approvals, index/CSS, CNAME/privacy побайтно прежние. Evidence telegram-presentation.json содержит mock-примеры, не live send. Следующее — обычный commit/push, remote SHA и CI/accepted notice; отдельные тестовые сообщения не нужны.

T1 remote подтверждён:674e5f5/run39113063235 success;71 tests, actual archive/noindex/noAPK, Telegram accepted165. Точный API proof — telegram-presentation.json. Workflow/секреты/бот/ledger/website gates не менялись; visual standard применяется ко всем существующим message types. Возобновлён прежний roadmap: owner acceptance и разрешение ранее подготовленного gate-diff по-прежнему pending. Повторно запрашивать неизменившееся разрешение или применять diff нельзя; независимая часть выполнена.


## R6 · применение разрешённой coming-soon политики

Цель: применить только согласованный proposal к актуальному work/website-v2, не разрешая фактическую публикацию. Владелец явно авторизовал применение patch; SHA-256 cefd3cc1b1440efa0f09c67b557570e5c9a4f89d0b7f0c63df7b8b407f38fd03 совпал; clean local/remote HEAD8a0e726 и git apply --check PASS. Applied bytes: только tools/build.py и новый tests/test_coming_soon_policy.py. Default full gates сохранены; explicit coming-soon требует отдельного approval, запрещает APK/features/screens. Реальные config/approval/noindex/main/deploy не менялись.

25 site/build/workflow/handoff tests PASS, включая5 активированных proposal tests; draft build PASS, index SHA af74145de9543065e6822cc79c3252673ae43a53b2b7eeb50484b1caf61b1357 прежний. Документы/реестр уточнены без нового roadmap/дублированного owner action. После checkpoint — CI actual archive round-trip, Telegram ack, обновлённая review ссылка. Следующий независимый шаг — предъявление проверенного кандидата; далее owner visual/legal acceptance и отдельная публикационная авторизация, APK не prerequisite.

R6 remote70527d0 подтверждён, run39114231216 success:76 unit tests, actual stored archive22files/4views/noindex=true/APK=false/page_errors=0; inner ZIP SHA прежний. Telegram accepted173. Evidence coming-soon-policy-applied.json; свежий review artifact12131711410 и прямые screenshots закреплены в FIRST_RELEASE/handoff. Exact next — owner visual/legal acceptance/замечания, затем отдельная публикационная авторизация; новых независимых approved задач не выявлено. APK по-прежнему не блокирует приёмку.


## R7 · первый production release (авторизован владельцем)

Владелец принял первый кандидат b12b0b0 и прямо разрешил Pages publication/main public-only commit и rollback при failure. Это отдельное разрешение от R6; исходное ТЗ сохраняется. Авторизация сохранена в project_specs/FIRST_WEBSITE_RELEASE_AUTHORIZATION_2026-10-18.md. Предыдущий main9a0857c и HTTPS bytes index/privacy проверены; Pages legacy main:/, CNAME/HTTPS config сохранены. Rollback manifest и remote tag rollback/website-first-release-2026-10-18 подтверждены. Production approved=true/coming-soon; APKfalse/unverified, features/screens пусты. Узкий indexing_approved=false оставляет noindex/Disallow в настоящей валидированной production-сборке, без обхода publication gate. 27 site tests PASS (включая2 indexing regression tests), production HTML побайтно совпадает с принятым кандидатом, privacy/CNAME неизменны. Следующее: проверить readiness CI, public-only commit/push, actual Pages/HTTPS/browser checks и Telegram proof; пока deployment не объявлен PASS.


R7 production опубликован9b39ffa, Pages39114713056 success; backup tag на9a0857c подтверждён.22 public bytes/12 internal404/HTTPS/config unchanged PASS (production-http.json). Live Chromium cloud остановился на proxy CA trust, не на product defect. Persistent CA import отклонён automatic approval review; TLS не отключали, CA не меняли. Read-only production QA добавлен в существующий verify workflow на GitHub runner с normal TLS, без новых triggers/permissions/deployment; фактический browser result pending. Следующее — проверить реальный CI, затем актуализировать полный checklist master и закрывать independent QA, не объявляя весь master завершённым первым coming-soon release.

R7 live verification фактически завершён в run39125147955:78 unit tests и production notice16 browser cases/22files/12internal404/TLS/noindex/APKfalse PASS. R8 следующий независимый шаг: read-only production Lighthouse в существующем verify; expensive live QA теперь только при Verify-Live-Production: true, чтобы не повторять на обычных docs commits. Полный master checklist выше сохраняет все незавершённые требования и конкретные зависимости; новые функции/редизайн не начаты.
