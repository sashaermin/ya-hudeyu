# QA черновика · этап 4A

Проверки выполнены 18.10.2026; сохранение отчёта 09:42 МСК (06:42 UTC). Это локальный draft, **не проверка production и не разрешение выпуска**. Последние изменения ресурсов/галереи проверены после оптимизации. Итоговый checkpoint указан в IMPLEMENTATION_PROGRESS.md и Git-истории.

## Фактические результаты

| Проверка | Результат | Область |
|---|---|---|
| Python build/workflow regression | 12/12 PASS, без skip | release approval gate, escaping, asset paths, repeatability, защита от публикации внутренних файлов, workflow без deploy |
| Notification unit tests | 33/33 PASS, без skip | mocks, источники, HTML escaping, секреты в ошибках не выводятся, ledger, события/actions, повторный CI failure report |
| JS syntax | PASS обоих файлов | Node 24.19.0 |
| Draft build | PASS, повторяемый output | Python 3.12.14, без build dependencies |
| Production build без одобрения APK | **Ожидаемая блокировка**, exit 1 | APK/feature/screenshot gate; не дефект сборки |
| Viewport/theme | 16/16 PASS | 320/360/390/430/768/1024/1440/1920 × light/dark в Chromium 154.0.8037.57 |
| Видимые изображения/ссылки | PASS | обе темы, ресурсы/якоря загружаются, layout CTA/heading/footer внутри viewport |
| Навигация/FAQ | PASS | mobile open/close, Escape, возврат фокуса, keyboard FAQ; no-JS mobile nav и native details |
| Темы | PASS | system light/dark, ручной выбор, reload persistence, возврат к OS preference |
| Галерея | PASS на изолированной fixture | keyboard arrows, native dialog + явная focus trap, Escape/restore focus, touch tap/CDP swipe, handled image failure |
| axe-core 4.10.3 | 0 violations | WCAG 2A/AA, 2.1AA, 2.2AA: 390 и 1440, обе темы (4 runs) |
| Main privacy/CNAME | Побайтно равны исходному main | local/served build; main SHA остался 9a0857ce260540ad604f344565d535a8d47b2fa0 |
| Внутренние файлы через HTTP | 404, как ожидается | /docs/SOURCE_AUDIT.md, /project_specs/user_actions.json, /data/release.json |
| Console/runtime | pageerror 0, failed requests 0 в обычной матрице | gallery fixture намеренно запрашивает отсутствующее изображение для проверки error state |

Галерея не содержит реальных release screens: они не получены. Fixture использует оригинальные mascot/icon с явными QA ONLY подписями, существует только в памяти browser_qa.py, никогда не попадает в JSON контента или `_site`. Проверка механики галереи не доказывает корректность отсутствующего релизного контента. CDP — Chromium touch emulation, не физический телефон.

[Машинный результат браузера](verification/browser-results.json).

## Lighthouse · мобильный профиль

Lighthouse 12.8.2, Chrome headless, simulated throttling, локальный Python HTTP server; один финальный run после целевой оптимизации:

| Категория | Score |
|---|---:|
| Performance | 96 |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 69 |

FCP 1.1 s, LCP 2.9 s, CLS 0. [Сохранённый результат](verification/lighthouse-summary.json).

SEO снижен намеренно: draft содержит noindex/nofollow и Disallow в robots.txt. Их не удаляли ради оценки. Production SEO ≥95 пока не проверен: gate закрыт до утверждённого APK. Сервер Python также не моделирует cache/compression/HTTPS Pages; production-метрики и домен нужно проверять после разрешённого deployment.

Первый run: Performance 86 / Accessibility 100 / Best Practices 100 / SEO 69. Исправления: адаптивные lossless WebP-логотипы, сохранённые оригинальные PNG; WOFF2-шрифты; ранняя инициализация темы и CSS встроены сборщиком, preload используемых шрифтов. Финальный run 96/100/100/69. Не выдавать это за полевые метрики или замер действующего домена.

## Снимки для визуальной приёмки владельцем

- [390px · светлая](screenshots/390-light.png)
- [390px · тёмная](screenshots/390-dark.png)
- [1440px · светлая](screenshots/1440-light.png)
- [1440px · тёмная](screenshots/1440-dark.png)

Сопоставление с Android: оригинальные логотип/маскот/шрифты; токены обоих режимов и формы карточек соответствуют docs/DESIGN_MAPPING.md. Веб-сетка и крупный hero адаптированы. Владелец ещё не подтвердил визуальное сходство. Hero использует только котика до получения настоящего скриншота APK; требование hero screenshot остаётся открытым.

## Как повторить

Обычные build/unit/registry commands — README. В среде уже проверены `/usr/bin/chromium`, Python Playwright 1.62.0. Для новой машины используйте имеющийся Chromium или установите его штатным способом. Дополнительные Python QA-пакеты перечислены в `tools/qa/requirements.txt`; для самой сборки сайта они не нужны. Например, можно установить их в отдельный `/tmp` target, не меняя систему:

```sh
python3 -m pip install --target /tmp/website-python-qa --cache-dir /tmp/pip-cache -r tools/qa/requirements.txt
npm ci --prefix tools/qa --cache /tmp/npm-cache --ignore-scripts --no-audit --no-fund
python3 tools/build.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory _site
```

В другом терминале:

```sh
PYTHONPATH=/tmp/website-python-qa python3 tests/browser_qa.py --axe tools/qa/node_modules/axe-core/axe.min.js
CHROME_PATH=/usr/bin/chromium tools/qa/node_modules/.bin/lighthouse http://127.0.0.1:8001/ --chrome-flags='--headless --no-sandbox' --output=json --output-path=/tmp/website-lighthouse.json --only-categories=performance,accessibility,best-practices,seo --quiet
```

В текущей сессии npm QA packages установлены и запускались из `/tmp/website-qa` с теми же версиями; `npm ci --prefix tools/qa --ignore-scripts --no-audit --no-fund` также реально выполнен успешно (202 packages); их package-lock сохранён в tools/qa для воспроизведения. Дополнительные проверки запускаются вручную, browser QA пока не включён в GitHub Actions. `--interactions-only` повторяет взаимодействия поверх уже сохранённой матрицы при исправлении исключительно тестовой оснастки; не использовать старую матрицу после изменения сайта.

Перекодирование оригинальных активов — optional maintainer-команды, не часть обычной сборки:

```sh
PYTHONPATH=/tmp/website-python-qa python3 tools/optimize_assets.py
PYTHONPATH=/tmp/website-python-qa python3 tools/optimize_fonts.py
```

## Выявленные и исправленные проблемы / границы доказательств

- Первый harness проверял OS theme сразу после emulate_media: событие асинхронное, исправлено ожидание фактического атрибута; это ошибка оснастки, не найденный дефект темы.
- Native dialog сам по себе не обеспечил требуемый wrap Shift+Tab в тесте: добавлена явная циклическая focus trap; повторно keyboard/focus PASS.
- Изначальный синтетический TouchEvent был некорректен (неполный TouchInit); заменён на CDP touchStart/move/end, свайп PASS.
- Начальные notification failures при адаптации Android перечислены в IMPLEMENTATION_PROGRESS; финальные 33 tests PASS. Сетевые отправки не выполнялись агентом.
- Firefox, WebKit/Safari, Edge отдельно, физические Android/iOS, screen reader и production HTTPS ещё не проверены. Chromium automation и axe не заменяют их.

## Чеклист перед выпуском

- [x] Исходники Android только для чтения, оригинальный бренд и provenance.
- [x] Draft build, статические и функциональные проверки, локальная матрица/axe.
- [x] Общие инструкции/roadmap/handoff и GitHub checkpoints.
- [x] Privacy URL, CNAME и main сохранены; deployment отсутствует.
- [ ] Утверждённый APK, подпись/manifest/SHA/размер/HTTPS URL.
- [ ] Функции и реальные screens именно этого APK, включая hero, обе темы.
- [ ] Визуальное подтверждение владельца и юридическая актуальность.
- [ ] Остальные браузеры/устройства и ручная accessibility-проверка.
- [ ] Подтверждённый GitHub Actions run и фактическая Telegram-доставка.
- [ ] Отдельное разрешение владельца на main/публикацию, затем проверка production SEO/HTTPS/Pages/download и готовый rollback.

Firefox/WebKit installer был запущен с отдельным PLAYWRIGHT_BROWSERS_PATH=/tmp/website-browsers. Firefox download остановлен proxy 403 Domain forbidden на cdn.playwright.dev и playwright.download.prss.microsoft.com; WebKit installer до загрузки не дошёл. Нужные домены вместе с api.github.com и yahudeyu-app.ru добавлены в **черновик** настроек среды; существующий package_managers preset сохранён. Start_skill также обновлён для запуска `_site`. Сохранение этих полей подтверждено, применение/публикация среды и повторная проверка пока не выполнены. Registry: site-network-crossbrowser-qa.

Дополнительно проверено: все неизменённые скопированные Android-активы побайтно равны исходным Git blobs; WOFF2 сохраняет glyph order и полный cmap оригинальных TTF.

## 4B · Firefox и WebKit после активации сети

Сеть действительно изменилась: CDN и production HTTPS отвечают 200; повторно скачаны Firefox 153.0 (Playwright revision 1538), WebKit 26.5 (revision 2336). После подготовки runtime выполнены **16/16 viewport/theme runs в каждом движке**, 4 axe-core 4.10.3 runs в каждом — 0 violations. Новые 32 проверки дополняют прежние 16 Chromium; успешный Chromium run не повторялся.

- [Firefox: машинные результаты](verification/firefox-results.json)
- [WebKit: машинные результаты](verification/webkit-results.json)
- [Firefox mobile dark](screenshots/firefox-390-dark.png), [desktop light](screenshots/firefox-1440-light.png)
- [WebKit mobile dark](screenshots/webkit-390-dark.png), [desktop light](screenshots/webkit-1440-light.png)

В обоих движках PASS: overflow/границы CTA, заголовки, картинки/якоря, native FAQ, no-JS nav/FAQ, mobile menu/Escape/focus return, theme persistence/reset/system updates, gallery arrows/focus trap/Escape/restore focus и handled image error. Firefox touch emulation Playwright не поддерживает — **не запускалась**. В WebKit проверены native tap и DOM gesture handler; native swipe не проверен. Chromium CDP touch swipe остаётся отдельным ранее подтверждённым результатом. Это движки в Linux cloud, не физические Android/iOS и не проверка установленного Safari/Edge.

WebKit при первом запуске взаимодействий не позволил создать `new Touch`: ошибка test harness, не приложения. Матрица/axe уже прошли, поэтому повторены только interaction checks с явно помеченным DOM event fixture; assert переключения кадра сохранён. Native WebKit swipe остаётся открытым device-check.

### Runtime без изменения системы

Cloud Debian 13 amd64 не содержит GTK4/graphene/harfbuzz-icu/manette/hyphen/GLES и части runtime libs. Встроенные sources указывали на недоступный snapshot.debian.org. Использован отдельный task-local APT config с официальным `https://deb.debian.org/debian trixie main`, системным Debian archive keyring, обязательной проверкой обновления и штатной checksum/signature validation. Никакие системные APT-файлы не менялись. Package archives извлечены через dpkg-deb в /tmp; бинарники браузеров не переписывались.

Воспроизводимый helper `tools/qa/prepare_linux_libs.py` **реально выполнен успешно**. Он сохраняет package versions/SHA-256 в локальном packages.json и добавляет отсутствующие dependency links в предусмотренный bundled wrapper каталог `minibrowser-wpe/sys/lib`, сохраняя существующие файлы. HTTPS и подписи не отключаются.

```sh
PLAYWRIGHT_BROWSERS_PATH=/tmp/website-browsers python3 -m playwright install firefox webkit
python3 tools/qa/prepare_linux_libs.py --webkit /tmp/website-browsers/webkit-2336
mkdir -p /tmp/website-runtime/cache /tmp/website-runtime/config
PLAYWRIGHT_BROWSERS_PATH=/tmp/website-browsers XDG_CACHE_HOME=/tmp/website-runtime/cache XDG_CONFIG_HOME=/tmp/website-runtime/config WEBSITE_FIREFOX_CONTAINER=1 MOZ_DISABLE_CONTENT_SANDBOX=1 python3 tests/browser_qa.py --engine firefox --axe tools/qa/node_modules/axe-core/axe.min.js
PLAYWRIGHT_BROWSERS_PATH=/tmp/website-browsers XDG_CACHE_HOME=/tmp/website-runtime/cache XDG_CONFIG_HOME=/tmp/website-runtime/config python3 tests/browser_qa.py --engine webkit --executable /tmp/website-browsers/webkit-2336/pw_run.sh --axe tools/qa/node_modules/axe-core/axe.min.js
```

Firefox default content sandbox не может создать nested uid_map внутри cloud sandbox и launch timeout; container-only flag отключает вложенный browser content sandbox для **локальной fixture**, агентский sandbox сохраняется. Это параметр QA, не сайта. WebKit system-cache probe не видит GLES из task-local LD path; фактический dlopen проверен, затем использован поддержанный custom executable_path штатного pw_run.sh с полным набором verified runtime libs. Финальный запуск не использует PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS и не меняет системный ldconfig. Промежуточный диагностический запуск с этим флагом завершился отсутствующей зависимостью; после исправления выполнен финальный реальный smoke/matrix.

### Production и CI: только чтение

GitHub Pages API теперь подтвердил `build_type: legacy`, source `main:/`, status built. Read-only HTTPS-проверки `/` и `/privacy.html`: HTTP 200 и полное побайтное соответствие текущему origin/main. Production не менялся.

Actions run [39106472358](https://github.com/sashaermin/ya-hudeyu/actions/runs/39106472358): verify success (36 notify + 13 build/workflow tests); notify failure на новом check-config. Check-run annotations однозначно указывают на отсутствующие TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID для workflow. Metadata secrets API по-прежнему запрещён integration scope, значения не извлекались. Доставка **не проверена/не работает до настройки bindings**. Existing registry обновлён, повторный alert с новым id не создавался.
