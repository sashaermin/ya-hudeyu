# Phase2 FAQ — пакет приёмки

**Текущий выпуск20.10.2026:** владелец разрешил единый Phase2+FAQ33/8+/download unavailable production release. Текущий combined source561971b;происхождение всехтрёхпакетов сверено в[release manifest](verification/phase2-faq-beta-production-release.json). Original approved ZIPd48f2d5… воспроизведён точно;только4пробела пустой generated HTML-строки удалены дляwhitespace gate,безизменениятекста/UX. Current artifacted78f72…;**Опубликовано и проверено:** production6810206,Pages39330940936/live39331146457 success,24hashes/64layouts/20axe0violations. [Сайт](https://yahudeyu-app.ru/) · [Недоступная бета](https://yahudeyu-app.ru/download/). APK выключен, noindex сохранён. Ниже — сохранённая историяdevelopment review,неповторный запрос уже данногоразрешения.


Статус: development/review only, STOP перед publication. Основание — дословное [задание владельца](../project_specs/PHASE2_FAQ_AUTHORIZATION_2026-10-20.md), дополнение кmaster иPhase2, не replacement specification.

**33 вопроса /8категорий.** Полный русский текст — [FAQ_GUIDE.md](FAQ_GUIDE.md). Каждый вопрос, workflow, implementation status, immutable AndroidSHA/file/line иpublication boundary — [FAQ_FEATURE_COVERAGE.md](FAQ_FEATURE_COVERAGE.md), [машинная матрица](verification/faq-feature-coverage.json). [Аудит](verification/faq-source-audit.json) фиксирует24цепочки UI/state/models/persistence иhashes; Android snapshot787175c, веткаwork/activity-progress-v6-4daeaa5 прочитана без изменения, сборки иливмешательства впроцессы. Website baselinec91fdd4 включает последующие Telegram formatter changes, они сохранены.

## Содержание

1. Знакомство и первые шаги —4вопроса: APK unavailable, пять реальных bottom destinations, обзор дня, профиль/первые записи.
2. Питание и дневник —6: день/приём пищи, количество/основа расчёта, неизвестные нутриенты, edit/delete/undo, copy/repeat/move, рецепты/порции.
3. Вес и замеры —4: записи/история, исправление веса, поля замеров/редактирование, сопоставление дат без медицинских выводов.
4. Активность —3: выбранный день/источник шагов, расчётные distance/energy иих зависимость отпрофиля, missing data/permissions.
5. Тренировки и упражнения —5: старт, GPS/manual, pause/resume/finish/error, templates противфакта выполнения, история/load/delete.
6. Статистика и прогресс —4: периоды, пустая история, влияние edit/delete, фото соявными границами аудита.
7. Настройки и персонализация —3: профиль/save/error, theme/accent/units, границы дополнительных разделов.
8. Данные, приватность и поддержка —4: local storage≠offline/backup guarantee, privacy/cloud, разрешения, support.

Функции классифицированы как реализованные висходниках, частично проверенные науровнеисходников/устройств, planned release илинепроверенное поведение релиза. «Реализовано висходниках» **не означает** проверенный APK. Перед FAQ есть development disclaimer; release availability/date/compatibility не выдумываются. Подробные AI/медицинские советы, гарантии HealthConnect/BLE/фона, sync/backup/videoexport исключены. Другие маршруты (лекарства/цикл/голодание/сон/трекеры/достижения) обнаружены, но полные сценарии не исследованы: это не утверждение обих отсутствии илинеработоспособности. Фото не обещают UI editing/deletion только потому, чтовstorage есть соответствующий метод. Замеры не обещают поле заметки только потому, чтооно есть вentity.

## UX и снимки

Сохранён approved дизайн: Onest/Unbounded/токены/темы, общий header/footer, все прежние секции Phase2. FAQ содержит category anchors, count вопросов, native details/summary и«Ктемам» внутрикаждой группы; IDs стабильны, targets focusable, footer-style links min44px. Нет custom tabs/search/filter илиновой JS-зависимости. При выключенномJS доступны категории, ответы ивозврат. Наdesktop сохранена intro+content сетка; mobile складывается водин столбец.

| FAQ | Light | Dark |
|---|---|---|
| Desktop1440 | [Снимок](screenshots/faq/faq-1440-light.png) | [Снимок](screenshots/faq/faq-1440-dark.png) |
| Mobile390 | [Снимок](screenshots/faq/faq-390-light.png) | [Снимок](screenshots/faq/faq-390-dark.png) |
| Деталь: питание1440 | [Снимок](screenshots/faq/nutrition-1440-light.png) | [Снимок](screenshots/faq/nutrition-1440-dark.png) |
| Деталь: питание390 | [Снимок](screenshots/faq/nutrition-390-light.png) | [Снимок](screenshots/faq/nutrition-390-dark.png) |

Снимки реальнойdevelopment-страницы; вполном FAQ открыт первый ответ каждойкатегории, чтобыбыли видны итипографика ответов, ииерархия. Это не скриншотыAndroid. Ранее сделанные Phase2 снимки/ZIP вPHASE2_REVIEW.md — история дорасширенияFAQ.

## Проверки

[QA evidence](verification/faq-review.json), подробности verification/faq-qa/.36website+68notification tests PASS;48FAQ responsive cases320/360/390/430/768/1024/1440/1920×2темы×Chromium/Firefox/WebKit;ещё16main layout cases.16axe runs (12FAQ+4main),0violations;18no-JS FAQ cases,33questions native keyboard expand/collapse вкаждом движке, category Enter→target focus, back→nav focus, touch bounds≥44px.12CSS text/spacing scenarios/reduced-motion/skip-link PASS. Общиеmenu/FAQ/themes/gallery fixture/image-error регрессии PASS. Browser screenshots осмотрены; нет горизонтальногоoverflow/pageerrors. Privacy file побайтно прежний; source/publication/release gates/noindex/APK-disabled сохранены, .github/main/production не менялись.

Android-функции не запускались/не тестировались наустройствах. Физические Android/iOS/Safari, реальныйscreenreader/nativezoom остаются непроверенными. Firefox touch неподдерживается; WebKit automation не равен Safari-device test. NoAPK/screens release-specific критерии мастер-ТЗ всё ещё blocked. Ни automatedPASS, ниsource audit не заменяют owner content review илиWCAG-сертификацию.

Воспроизведение: `python3 tools/build.py`, local draft server для_site, затем `python3 tests/faq_qa.py --base <local-draft-url> --out .test-results/faq/chromium`. Engine/executable флаги иtask-local libraries — docs/QA.md. Unit suites как вAGENTS.md. Результаты проверки текущего FAQ не требуют повторения неизменённого полного Androidаудита.

## Источник и просмотр

**Точный UI source SHA: `1611a15b1aadf3c27953b935a9fb7670686846ff`.** [Проверенный ZIP дляпросмотра](https://github.com/sashaermin/ya-hudeyu/actions/runs/39325727846/artifacts/12221768739), run39325727846/attempt1/artifact12221768739. Verify job success:104unit tests,stored upload→download23file manifest/4rendered views,clean source/noindex/APK-disabled/page_errors0. Срок хранения до27.10.2026 00:13МСК (7дней). Initial run failure был только из-за Telegram TOPIC_CLOSED. Владелец открыл тему; failed-job reruns39325727846/39326114527 attempt2 завершены success. Telegram подтвердил topic6/messages318,319,321,322,323: доставка восстановлена, action resolved. Секреты check-config прошли; никаких новых bindings илисмены назначения не требуется. Послеdocs-only checkpoint UI bytes этогоисточника не меняются. Local preview ZIP SHA-256 `d0b00ec9c67400a3ae308a3428b99733270f9fa30bd5207b2069b83275373dd8`,23public files; никакихdocs/sourceJSON/тестов/секретов внутри. Это архив длялокального просмотра, hostedpreview отсутствует. После получения CI ZIP распаковать внешнийbundle, затем website-preview.zip вreview-site; на **своём компьютере** запустить `python3 -m http.server 8080 --directory review-site` иоткрыть localhost:8080. Это не ссылка вконтейнер. Retention7дней; сверять innerZIP digest/sourceSHA иmanifest, при истечении срока пересобрать източного verified source черезtools/package_preview.py.

## Как поддерживать FAQ

При измененииAndroid выбрать immutable SHA ипрочитать связанную цепочку UI→state→calculation/persistence, включая ошибки/ограничения. Вdata/site.json сохранить прежниеquestion/category IDs, обновить текст илидобавить категорию без пустыхгрупп. Длякаждого topic обновить faq-feature-coverage.json иsource-audit.json (SHA/path/line/symbol/hash), Markdownматрицу иFAQ_GUIDE.md. Поддерживать source-vs-runtime статусы исписок omitted; fields модели безUI не обещать. Unit contract проверяет соответствие answer↔matrix иsafe IDs; при расширении обновить осознанно count assertions. После изменениякопии проверитьaffected widths/themes/keyboard/noJS/axe, обновитьснимки/preview manifest. Ни один source-only FAQ update не разрешает APK илиproduction.

Что требуется от владельца: приёмка полноты/формулировок справочника итекущего UX. Existing site-phase2-owner-review сохраняется, APK approval — отдельно open. Доэтого STOP: не main/merge/deploy/indexing/APK, новых unrelated задач не начинать.
