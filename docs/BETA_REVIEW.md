# Phase3 — пакет приёмки beta preparation

**Текущий выпуск20.10.2026:** владелец разрешил единый Phase2+FAQ33/8+/download unavailable production release. Текущий combined source561971b;происхождение всехтрёхпакетов сверено в[release manifest](verification/phase2-faq-beta-production-release.json). Original approved ZIPd48f2d5… воспроизведён точно;только4пробела пустой generated HTML-строки удалены дляwhitespace gate,безизменениятекста/UX. Current artifacted78f72…;publication pending доactual Pages/live verification. Ниже — сохранённая историяdevelopment review,неповторный запрос уже данногоразрешения.


Development/review only. Ни APK, ни новый website release не утверждены. Production public source8fb7bf2920a89f39e1ed3a56d53ada91f468b715 неизменён; mainf308729f2cd4d7bde3574e08d8fd2fc05e92c4ab содержит только отдельно согласованную Telegram инфраструктуру сверх production. FAQ33/8 иPhase2 сохранены. Exact UI source — `011eb4b146552aa79a30e91ed04a26b7f0f4bc46`; clean CI39328336826 success,115unit tests,actual archive24files/4home+4download views/noindex/APK-disabled/page_errors0. Telegram topic6/messages328–329 подтверждены API.

- [Архитектура](BETA_DISTRIBUTION.md): GitHub Pages +versioned GitHub Releases APK, никакого нового backend/hosting/publisher.
- [Схема](BETA_RELEASE_SCHEMA.md): единственный release.json, независимые technical /owner distribution /website approvals; fail-closed.
- [Будущая процедура APK](BETA_APPROVAL_PROCEDURE.md): signing,manifest,bytes,real install/upgrade,release asset integrity,full gate,приёмка,отдельная публикация/rollback.
- [Памятка установки](BETA_INSTALLATION.md): выбранный источник/подтверждение Android без отключения защиты,контроль суммы,обновление,ошибки.
- Feedback использует existing verified email изmaster/data/site.json; ничего не собирает автоматически. Неизвестная доставка email/ответ оператора не заявляется.

## Визуальный просмотр

| Состояние | Desktop1440 | Mobile390 |
|---|---|---|
| Unavailable, light | [Снимок](screenshots/beta/unavailable-1440-light.png) | [Снимок](screenshots/beta/unavailable-390-light.png) |
| Unavailable, dark | [Снимок](screenshots/beta/unavailable-1440-dark.png) | [Снимок](screenshots/beta/unavailable-390-dark.png) |
| TEST ONLY fixture, light | [Снимок](screenshots/beta/fixture-1440-light.png) | [Снимок](screenshots/beta/fixture-390-light.png) |
| TEST ONLY fixture, dark | [Снимок](screenshots/beta/fixture-1440-dark.png) | [Снимок](screenshots/beta/fixture-390-dark.png) |

Снимки настоящего website UI, не Android. Fixture содержит видимое предупреждение «ТЕСТОВЫЙ МАКЕТ» иversion/notes TEST ONLY. APK не существует; URL — simulation, не выполнять загрузку. Fixture page создаёт только QA harness во временной папке, вобычном preview ZIP её **нет**. Обычный ZIP содержит только unavailable `/download/`.

## Проверки и ограничения

- Website suite:47tests (включая11beta regression cases),notification suite68tests. Byte mismatch/signing/debug/testOnly/package/version/minSdk failures проверены тестами; Android SDK stdout имитирован, реального signed APK не было.
- Beta32responsive cases наengine ×3=96:320/360/390/430/768/1024/1440/1920,2themes,2states.24axe0violations;12no-JS;18long-version/release-notes/200% CSS text-and-spacing cases; keyboard menu/Escape/skip/native disclosure иtheme persistence.
- Главная16layout/4axe0violations; FAQ16layout/4axe0violations/6noJS/33disclosures вChromium. Никакого нового JS/analytics.
- После уточнения installation-copy снимки/Chromium beta suite обновлены; Firefox/WebKit matrix относится к тому же layout/gates с первоначальным текстом памятки. Это не physical-device/AT/native-zoom/Safari acceptance.
- Privacy/CNAME побайтно прежние; main/public Git bytes сверены read-only, Pages built/HTTPS enforced. Новый live production HTTP/browser run не выполнялся, website не публиковался.
- Future availability проверена наизолированных metadata fixtures, не на APK. Реальные signing/install/update/device/data migration/compatibility/features/screens пока не подтверждены.

## Воспроизведение

`python3 tools/build.py` создаёт `_site` с`download/index.html`,noindex ибезAPKs. `python3 tools/package_preview.py` создаёт fresh allowlisted детерминированный ZIP; он не публикует сайт. Для unavailable-состояния распаковать ZIP насвоём компьютере, запустить `python3 -m http.server 8080 --directory <распакованная-папка>` иоткрыть там `/download` (HTTP redirect на`/download/`). Cloud loopback не является внешним preview URL.

Симуляция available без изменения config: `python3 tests/beta_qa.py --out .test-results/beta/chromium`. Harness собирает own temporary pages/server, проверяет оба состояния, сохраняет screenshots/results иудаляетfixture server. Используются pinned Playwright иaxe поdocs/QA.md. Не копироватьfixture metadata вdata/.

## Предмет решения владельца

Посмотреть unavailable/TEST ONLY states ипринять layout/русский текст либо дать замечания. Приёмка подготовки **не разрешает** публиковать website/APK. Для первой реальной беты нужны точный APK, доверенный signer/source/version metadata,проверки реальнойсборки иотдельные разрешения artifact distribution иwebsite publication. APK не требуется дляприёмки этой подготовки. Noindex/indexing,legaltext иproduction отдельно сохраняются.

## Проверенный архив и checkpoint

[Скачать review artifact](https://github.com/sashaermin/ya-hudeyu/actions/runs/39328336826/artifacts/12224030587) из [успешного CI](https://github.com/sashaermin/ya-hudeyu/actions/runs/39328336826). Source `011eb4b146552aa79a30e91ed04a26b7f0f4bc46`,attempt1,artifact12224030587; хранится до **27.10.2026 00:32 МСК** (7дней). Это downloadable ZIP, не публичный preview URL. Распаковать внешний bundle, затем `website-preview.zip` в отдельную папку на своём компьютере и запустить локальный сервер по инструкции выше.

Inner ZIP SHA-256: `d48f2d5a714faffb0bdecea8b19b75ec13ca94913f14776361a0407d70e55e8f`. Проверены upload→download,24file hashes,clean source,4home+4download renders,обе темы,noindex=true,APK=false. Fixture page отсутствует в ZIP; её видны восемь снимков выше ивоспроизводит QA harness. При истечении срока пересобрать exact source черезpackage_preview.py и сверить этот digest, не выбирать случайный artifact.

Последующие documentation-only checkpoint сохраняют эти UI bytes; актуальный development HEAD брать черезGit. Production page `/download/` этой задачей не публикуется. Последний Pages build commit по API —f308729f; public website files побайтно равны уже выпущенному8fb7bf2.
