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
