# QA сайта · draft и первый кандидат

Проверки выполнены 18.10.2026; сохранение отчёта 09:42 МСК (06:42 UTC). Это локальный draft, **не проверка production и не разрешение выпуска**. Последние изменения ресурсов/галереи проверены после оптимизации. Итоговый checkpoint указан в IMPLEMENTATION_PROGRESS.md и Git-истории.

Текущий кандидат: R1 copy/snapshots, R2/R5 actual CI archive/render proof. Последнее подтверждение — [artifact-node24.json](verification/artifact-node24.json), run39111335266 success,22files/4renderedviews/noindex/noAPK, Telegram138. [Просмотр и приёмка](FIRST_RELEASE.md). Подробные исторические проверки ниже сохраняют точную область применимости.

## Исторический срез 4A

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
- [x] Подтверждённый GitHub Actions run и фактическая Telegram-доставка: run39109066640 success, Telegram accepted message_id77; live evidence также в telegram-delivery-2026-10-18.json.
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


## W2B · доставка после настройки bindings

40/40 notification tests PASS, без skip: recovery старых неизменённых action/event records, отложенное resolved, partial failure/retry и dedup предупреждений. Предыдущие успешные checks не заменялись, новые проверки добавлены по конкретному найденному случаю: secret bindings отсутствуют, поэтому diff-only sender терял бы уведомления об уже существующих blockers/events после настройки.

Реальный notify пока не успешен: отсутствуют два Actions bindings. Новые check-run notices содержат message_id только после реального Telegram ok=true; будущий агент проверяет annotations, а не предполагает доставку по наличию workflow. Package versions/SHA для QA runtime дополнительно сохранены в [linux-qa-packages.json](verification/linux-qa-packages.json), бинарные архивы в Git не добавлялись.

Последний проверенный GitHub run [39107259552](https://github.com/sashaermin/ya-hudeyu/actions/runs/39107259552) для ad7c5a0: verify success, notify failure по missing bindings. [Сохранённые jobs/annotations](verification/actions-current.json). Числа57 unit tests относятся к текущим inputs; 48 viewport/theme и12 axe включают сохранённый неизменённый Chromium artifact и реально выполненные новые Firefox/WebKit runs. Доставка и обязательное расписание всё ещё не активны.

## 4C · Microsoft Edge Stable

Отдельно проверен настоящий Microsoft Edge155.0.4283.62 на Linux, не замена Edge обычным Chromium. [Результат и происхождение пакета](verification/edge-results.json):16/16 ширин/тем,4 axe runs без нарушений; theme/menu/FAQ/gallery/focus/no-JS/native tap/CDP swipe PASS; page errors и failed requests0. [390 dark](screenshots/edge-390-dark.png), [1440 light](screenshots/edge-1440-light.png). Совокупно с предыдущими неизменёнными inputs64 viewport/theme runs и16 axe runs.

Пакет получен из официального https://packages.microsoft.com/repos/edge/; GPG InRelease signature проверена ключом Microsoft fingerprint BC528686B50D79E339D3721CEB3E94ADBE1229CF, SHA-256 Packages.gz совпал с подписанным index, размер и SHA-256 deb совпали с Packages. Пакет извлечён `dpkg-deb -x` в `/tmp/website-edge`, без system install. Key получен по HTTPS из https://packages.microsoft.com/keys/microsoft.asc; GPG предупреждение об отсутствии personal web-of-trust не подменяется заявлением о наличии локальной доверительной цепочки.

Повторить на уже подготовленном официальном бинарнике:

```sh
python3 tests/browser_qa.py --engine chromium --executable /tmp/website-edge/opt/microsoft/msedge/msedge --base http://127.0.0.1:8002/ --output .test-results/edge --axe tools/qa/node_modules/axe-core/axe.min.js
```

`engine: chromium` обозначает Playwright protocol; product/package в evidence указывает настоящий Edge. Старый server8001 отвечал empty reply; его не останавливали, использован отдельный read-only draft server8002. Физические Android/iOS, Safari и screen reader остаются непроверенными.

Текущее Telegram-состояние заменяет исторические missing-binding записи выше: **DELIVERED**, последний проверенный push run39109066640 accepted message_id77. Обязательное daily schedule всё ещё ожидает отдельного разрешения main; доставка по push этого не меняет.

## 4D · увеличение текста, интервалы, reduced motion и skip link

Новая независимая проверка обнаружила два дефекта: skip link прокручивал, но не фокусировал main; при CSS-увеличении текста до200% на320/390px grid-карточки выходили за viewport. Исправлено: `tabindex="-1"` у main и наследуемый `overflow-wrap:anywhere` у body. Отрицательный baseline сохранён, не считается PASS.

[Доказательства до/после](verification/accessibility-adaptation.json): **48/48 PASS** — по12 сценариев в Chromium154, Firefox153, WebKit26.5 и Edge155:320/390/1440px ×2темы ×200% текст/увеличенные интервалы. Для интервалов применены line-height1.5, letter-spacing.12em, word-spacing.16em, paragraph margin2em; FAQ раскрыт, mobile menu открыт. Проверяются scrollWidth и границы видимых текстовых ranges, а не маскировка overflow. Во всех4 браузерах: reduced-motion отключает transitions/smooth scroll; первый Tab показывает skip link, Enter переносит фокус в main.

[Текст200% ·320 dark](screenshots/accessibility-text-200-320-dark.png), [интервалы ·320 dark](screenshots/accessibility-text-spacing-320-dark.png). Это CSS-симуляция **text-only resize**, не native browser zoom и не замена screen reader/manual/device acceptance. Reflow до320 CSSpx уже покрыт матрицей; реальный400% zoom отдельного браузера не заявляется проверенным.

После изменения HTML/CSS обоснованно повторены4 обычные matrices:64/64 viewport/theme,16 axe runs0violations, interactions PASS. Текущие browser-results/firefox-results/webkit-results/edge-results обновлены и содержат hash нового HTML. Все12 имеющихся сравнительных screenshots побайтно прежние, обычный дизайн не изменился. 17 build/workflow unit tests PASS; notification code не менялся, его40 tests повторно исполняет обычный CI. Lighthouse96/100/100/69 остаётся историческим замером4A; он не запускался снова ради не влияющего на обычный layout исправления.

Воспроизведение дополнительного QA:

```sh
python3 tests/accessibility_qa.py --base http://127.0.0.1:8002/
python3 tests/accessibility_qa.py --base http://127.0.0.1:8002/ --executable /tmp/website-edge/opt/microsoft/msedge/msedge --output .test-results/accessibility-edge
```

Firefox/WebKit используют те же runtime environment variables и executable, что recipes4B, с `tests/accessibility_qa.py --engine firefox|webkit --output ...`. Все зависимости остаются optional QA; внутренние отчёты/fixtures в `_site` не добавлены. Telegram push checkpoint6958c0d: run39109598867 success, accepted message_id84.

### Текущий остаток приёмки

Доступные в этой Linux-среде независимые draft-задачи этапов0–4 выполнены. Открыты: утверждение конкретного APK, его техническая/функциональная проверка, реальные hero/gallery screens обеих тем, owner visual/legal acceptance, реальные Android/iOS/Safari и screen reader. После нового контента QA нужен снова по затронутым сценариям. Daily digest требует разрешения main; публикация сайта требует отдельного разрешения. Ни один этот критерий не закрыт успешными draft-тестами.

## R1 · кандидат первого сайта с «Скоро»

Первый инкремент готовится независимо от APK по новому указанию владельца. [Машинный результат](verification/release-candidate.json):18 build/workflow/package unit tests PASS; Chromium16/16 ширин/тем,4 axe runs0violations, interaction/runtime checks PASS. После изменения пользовательского текста проверены48/48 text resize/spacing cases в Chromium/Firefox/WebKit/Edge, reduced-motion/skip focus PASS. Это новая проверка затронутого copy; старые4D full-browser matrices остаются историческим подтверждением совместимости структуры, а не новым запуском на этом copy.

Кандидат для визуальной приёмки: [390 light](screenshots/rc-390-light.png), [390 dark](screenshots/rc-390-dark.png), [1440 light](screenshots/rc-1440-light.png), [1440 dark](screenshots/rc-1440-dark.png). Галерея не имитирует Android UI, функции не выдуманы, download отсутствует, дата выпуска не обещана. noindex/robots Disallow и data approvals сохранены.

Архив проверен на повторяемость и allowlist, включая неизменённые CNAME/privacy и отсутствие внутренних docs/config/APK. Local manifest честно помечает dirty tree; окончательный CI source/digest проверяется отдельно вR2. Публикация/изменение production gate не выполнялись. [Приёмка, разрешения и план отката](FIRST_RELEASE.md).

## R2 · фактический CI artifact

[Verified artifact](https://github.com/sashaermin/ya-hudeyu/actions/runs/39110644873/artifacts/12130197561), source0b4eb54. Run39110644873 success: upload→download реального artifact, clean source/digest/22file manifests PASS, actual Chrome rendering390/1440×2themes PASS, noindex/noAPK/page_errors0. Отдельный notice117625868753 — доказательство выполнения, не только success job. [Evidence](verification/review-artifact-status.json); Telegram109. Прямое cloud скачивание403 остаётся отдельным ограничением среды, local rehearsal не подменяет remote proof; remote proof получен на GitHub runner. Это архив для просмотра, не hosted preview/production publication.

R5 current artifact pipeline: native Node24 official upload7.0.2/download8.0.2 pinned refs проверены статически и live CI. Run39111335266 success, notice117627928319 подтверждает22files/4views, Telegram138; Node20 warning отсутствует. 58 current unit tests CI PASS. Результат rerun R4 и ограничение старых artifact IDs — [artifact-retry.json](verification/artifact-retry.json). Proposal policy20 tests проверены только в изолированном экспорте, **не применены** к active code; это не новая фактическая авторизация.

## P1 · cross-agent cold start и формат уведомлений

47 notification mock tests +20 site/workflow/handoff tests PASS. Проверены русский commit contract, exact agent provenance/unknown/conflicts, escaped-size limit/ссылка, head-only verification, API errors/token safety и существующие ledger retry/backlog/dedup cases. Новый preview event явно архив, не online preview; URL validation отклоняет injection. Repository-only cold-start [evidence](verification/cold-start-handoff.json) содержит все вопросы/ответы и источники; реальный Claude↔Codex transfer **не выполнялся**. Базовые entrypoint/next/spec/QA/restriction regression checks включены в CI. Actual draft HTML совпал с R1, browser matrices не повторены. Live acceptance нового обычного commit проверяется отдельно после push, никакой локальной Telegram отправки.

P1 live confirmation: run39112341703 success/Telegram157, [evidence](verification/permanent-agent-protocol.json). Own-source milestone follow-up покрыт48 notification tests PASS; вместе с20 site/handoff —68 tests. Real Claude↔Codex transfer не заявляется; холодный старт — repository-only simulation/contract checks. Дизайн и generated HTML не менялись.

## T1 · единая HTML-иерархия всех Telegram сообщений

51 notification tests и20 site/workflow/handoff tests PASS. [Mock examples/evidence](verification/telegram-presentation.json): commit/milestone/CI/action/resolution/stage/preview/digest проверены HTML parser на balanced tags, безопасные href/quoted attrs, headers/metadata/paragraph spacing. Long messages сохраняют whole entities/closing tags/footer; malicious URLs отвергаются без эха credentials. Существующие retry/dedup/source/token-safety проверки сохранены. Это не скриншот Telegram UI и не дополнительная живая отправка. Whole workflow/protected files и delivery/ledger functions сравнялись с8888818; draft HTML прежний. Полная browser матрица без изменений сайта не повторялась.

T1 live proof: run39113063235 success,51+20 tests, actual archive/noindex/noAPK PASS; Telegram accepted165 через обычный commit. Exact notices в [telegram-presentation.json](verification/telegram-presentation.json). Проверена API-приёмка HTML-сообщения и локальная markup структура, не screenshot реальных Telegram/Android/Windows clients.


## R7/R8 · actual production verification (18.10.2026)

Production https://yahudeyu-app.ru/ опубликован на9b39ffaf35c48973b8115b630ba0d06165ad09a4; Pages39114713056 success. Live QA39125147955 и39125369226 success:22 public file hashes совпали с утверждённым allowlist/принятым HTML,12 internal paths404, privacy/CNAME/Pages config прежние;16 Chrome viewport/theme cases320–1920 и menu/FAQ/theme persistence/no-JS PASS, page_errors0. Generic gallery fixture checks остаются явно test-only, не являются release screenshots. Actual HTTPS/normal TLS verified на GitHub runner; cloud Chromium proxy trust limitation не выдаётся за production defect, TLS нигде не отключали.

Lighthouse12.8.2 simulated mobile на production:99/100/100/69, FCP1052ms,LCP1952ms,TBT0,CLS0.000058, warnings0. Цели90/95/95 достигнуты; SEO69 из intentional noindex/nofollow/robots Disallow. Не включать indexing ради score. Physical Android/iOS/Safari, screen reader/native zoom, native WebKit swipe и будущий APK-specific UI не проверены; текущий release их не закрывает. Полный master checklist — IMPLEMENTATION_PROGRESS.md.

Evidence: [публикация](verification/first-production-release.json), [HTTP hashes/404](verification/production-http.json), [production Lighthouse](verification/production-lighthouse.json), [rollback](verification/first-production-rollback.json). Read-only repeat QA только при изменившейся причине/Verify-Live-Production: true, не на каждом docs checkpoint. У сайта не было повторного deployment в этой verification сессии.


## U0–U2 · UI/UX implementation audit

Сверены44 UI требования с source/render и current read-only Android960e43b. [Аудит](UI_UX_REQUIREMENTS_AUDIT.md):35 complete/0partial/0missing/7releaseblocked/2manual. Исправлены навигация без JS, keyboard focus/traversal/selection/resize, system dark fallback, privacy shared themes/Onest/reflow и gallery loading/error/retry/cancel/rapid reopen. Все legal paragraphs/date/links неизменны (normalized hash). Production9b39ffa/его privacy/CNAME не менялись; новые UI fixes только development.

Fresh proof [U1](verification/uiux-u1.json), [U2](verification/uiux-u2.json):64 main и64 privacy width/theme cases вChromium154/Firefox153/WebKit26.5/Edge155;48axe0violations,24no-JS cases,60 CSS text/spacing cases; gallery states2themes×4engines. Native zoom/AT/physical Safari иWebKit native swipe не проверены. Перед последним rapid-close guard main visible-layout matrices уже прошли; HTML/CSS прежние, affected gallery states после guard повторены4engines. Не выдавать эти fixtures за release screenshots.

Воспроизведение: fresh `python3 tools/build.py`; task-local `python3 -m http.server 8012 --bind 127.0.0.1 --directory _site` (прежний8002 давал RemoteDisconnected, чужой процесс не остановлен). `python3 tests/uiux_qa.py`, `python3 tests/gallery_loading_qa.py`, `python3 tests/browser_qa.py --base http://127.0.0.1:8012/ --axe tools/qa/node_modules/axe-core/axe.min.js`; browser/env flags те же, что в4B/4C выше. New focused scripts также поддерживают `--engine`/`--executable`; before gallery mode предназначен только для baseline без loading state. Loopback не является внешним owner-preview.

CI smoke сверяет current development ZIP/hash по `verification/current-preview.json`; исторический R1 candidate и approved production manifest не переписывать. U2run39127437892 success/78unit tests/actual archive4views. Детальные browser suites выполнены локально и сохранены вGit, не выдаются за дополнительные CI jobs. Before/after вscreenshots/uiux, включаяprivacy320/light/dark, no-JS overlap иgallery loading/error. Дальнейшие public release changes — только с отдельным разрешением.
