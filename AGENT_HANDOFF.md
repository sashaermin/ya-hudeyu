# «Я ХУдЕЮ» — общий handoff сайта

- Repository: `sashaermin/ya-hudeyu`.
- Branch: `work/website-v2` (от main).
- Последний независимо подтверждённый remote checkpoint: `cf7814fc5ff60caf0de480aa50c288de5404472a`. Более поздний содержащий этот handoff commit проверять через `git ls-remote`, не полагаться на самоссылку.
- Последний ответственный агент: Codex. В текущей сессии Codex — активный единственный писатель сайта; это историческая запись, не вечный lease. Другой активный website writer неизвестен. Android Claude Code активен отдельно и не затрагивается.
- Текущая стадия: независимый draft QA этапа 4A завершён локально; оставшаяся проверка ожидает сети и утверждённого release content. W1/W1.1 реализованы; фактическая Telegram-доставка не подтверждена.
- Завершённые checkpoints: этап 0 `a4de44b`; основа этапа 1 `356eaef`; секции/взаимодействия этапа 2 `24ca8d5`. Релизные критерии этапов 2–4 остаются открытыми.

**Next:** После W2A push прочитать verify/notify job annotations нового run: probe check-config покажет только имена missing bindings или подтвердит наличие. Не запрашивать токен по ошибке metadata API. Продолжить 4B Firefox/WebKit: скачаны в /tmp/website-browsers, WebKit нужны 6 runtime libraries, официальные подписанные Debian-пакеты скачаны в /tmp/website-apt/downloads и извлечены в /tmp/website-browser-libs. Firefox smoke ещё исследуется; не считать PASS. Подготовленный daily digest ждёт отдельного разрешения только на default-branch workflow, main не менять. APK по-прежнему не выбран/не разрешён.

## Текущее исполнение и доказательства

- Сайт — статический HTML template + CSS/JS, конфигурация `data/site.json`, `data/release.json`, dependency-free `python3 tools/build.py` → `_site` (draft noindex). Serve только `_site`.
- Запущенный Codex HTTP на 127.0.0.1:8001, каталог `_site`; процессы не переживают новую cloud task. Старый onboarding server на 8000 может существовать — он не production. Перед остановкой проверять владельца процесса.
- Дизайн: оригинальные Onest/Unbounded, green #58A936, тёплые neutral surfaces, оригинальный mascot_calm, green wordmarks. Provenance: docs/ASSET_SOURCES.json.
- Android read-only clone для аудита: `/tmp/ya-hudeyu-android-audit`, reference commit `874de91cb626b6f0e78532963b378d86901b97d9`. Не используется как workspace Android-разработки. Временные файлы не канон; исходные ссылки и SHA в docs/SOURCE_AUDIT.md.
- Build/workflow tests 12/12 PASS, notification tests 33/33 PASS, без skip. Первоначальные notify tests: 4 failures / 3 skips из 31 при адаптации; исправлены ожидания/регистры; финальные 30/30 notify tests PASS (лишний Android-only registry test удалён). Workflow YAML parsed; build/workflow tests 11/11 PASS. Исторические числа выше относятся к ранним checkpoints; актуальные полные результаты 4A сохранены ниже.
- В среде доступны Python Playwright, `/usr/bin/chromium`, Pillow/fontTools. Временные QA npm packages `/tmp/website-qa` (Lighthouse 12.8.2, @axe-core/playwright 4.10.2); Brotli `/tmp/website-font-tools`. Команды/версии сохранены в README, docs/QA.md и tools/qa; временные каталоги не являются каноническим источником.

## Открытые решения / ограничения

- Владелец явно подтвердил: ни один APK не разрешён к публикации. Download недоступен; metadata/screens/функции ждут конкретного артефакта. Ссылка/старый APK не выбираются агентом.
- Главная содержит временные состояния возможностей и галереи; настоящие release screenshots нужны для завершения требований, включая hero.
- Telegram API напрямую не вызывается агентом. Проверка имён Actions secrets через gh api заблокирована 403; отсутствие локальных Telegram env не означает отсутствие repository secrets. Доставка **не проверена**. Pending действия в project_specs/user_actions.json.
- Юридические тексты и CNAME побайтно сохранены. Main, merge, PR, deploy, публикация APK не разрешены. Никакой Windows-рекламы.
- Обязательный daily digest подготовлен, но не активирован: schedule требует разрешения на main. Не менять default branch ради уведомлений.

## Проверенный результат 4A · 18.10.2026 09:48 МСК

- Chromium 154.0.8037.57: все 16 viewport/theme сочетаний PASS; 4 axe-core 4.10.3 runs — 0 violations; theme persistence/system, mobile menu/Escape, FAQ, keyboard dialog trap/restore focus, touch tap/CDP swipe, handled gallery error, no-JS nav/FAQ PASS.
- Local Lighthouse mobile: Performance 96, Accessibility 100, Best Practices 100, SEO 69 — последнее намеренно снижено draft noindex. Production SEO/HTTPS не проверены. Метрики, ограничения, история исправлений и 4 owner-review screenshots сохранены в docs/QA.md, docs/verification, docs/screenshots.
- `python3 tools/build.py --production` проверенно возвращает exit 1 без утверждённого APK; это ожидаемый gate. Draft build и повторяемость PASS; privacy/CNAME побайтно равны main. Main SHA 9a0857ce260540ad604f344565d535a8d47b2fa0 сохранён.
- Реальные release screens и hero screenshot отсутствуют. Демо-галерея протестирована только in-memory QA fixture, не в публичном контенте. Owner visual/legal approval pending. Firefox/WebKit/Edge/Safari/физические устройства не проверены.
- Firefox/WebKit install попробован отдельно через PLAYWRIGHT_BROWSERS_PATH=/tmp/website-browsers: Firefox download получил proxy 403 Domain forbidden на обоих official CDN; WebKit не установлен. Это сетевой блокер, TLS/подписи не отключались.
- Start_skill и additive domains сохранены в environment config draft (persistence confirmed). Package-manager presets сохранены. Runtime activation / environment publication / новая task не проверены. Не путать публикацию среды с запрещённым website deployment.
- `npm ci --prefix tools/qa --cache /tmp/npm-cache --ignore-scripts --no-audit --no-fund` реально выполнен успешно (202 packages). Lockfile/optional Python pins и encoders сохранены; `_site` остаётся stdlib-only. Rebuild commands: README и docs/QA.md. Node_modules/_site/.test-results ignored.
- Все существенные результаты сохранены в Git, temp logs не являются единственным источником. Новая cloud task: прочитать общие файлы и remote, rebuild draft, restart server по startup instructions; завершённые проверки не повторять без изменившихся входов.

Проверенный implementation checkpoint `b3ffaf9ceb9d7f998e673468bfb4a0718393b961` отправлен и независимо подтверждён через git ls-remote. Рабочее дерево после него чистое. Эта финальная запись handoff — отдельный documentation checkpoint; его актуальный SHA получать из Git. Дальнейшая работа по открытым release/network критериям требует описанных действий владельца; независимые draft-задачи завершены. Не считать session label бессрочным доказательством отсутствия другого активного агента.

## Возобновление автономного цикла

Сеть повторно проверена после возобновления: official CDN и действующий домен HTTP 200; прежний network action resolved. GitHub Actions runs доступны; checkpoint cf7814f: verify success, notify failure. Secrets metadata 403 по правам integration. Логи run redirect на results-receiver.actions.githubusercontent.com пока недоступны из среды; не выводить signed URLs в отчёты. Firefox/WebKit install запущен после подтверждённого изменения сети. Сохранены постоянные автономные инструкции владельца; W2 — digest/notification diagnosis, затем 4B cross-browser QA.

W2A: notification tests 36/36 и build/workflow 13/13 PASS, YAML parsed. Live GitHub digest dry-run PASS без отправки. Новые actions probe и digest runtime dedup проверены с mocks. Последний remote cf7814f подтверждён перед продолжением.
