# Phase 2 — пакет визуальной и контентной приёмки

Статус: development candidate, **не опубликован**. Основание — [исходная авторизация Phase2](../project_specs/PHASE2_CONTENT_AUTHORIZATION_2026-10-18.md), дополнение к неизменённому мастер-ТЗ. Текущая production-вёрстка8fb7bf2 сохранена; main3cf7825 не менялся. Telegram COMPLETED, никаких workflow/schedule изменений.

## До / после

До: описание приложения без конкретной области, пустой блок возможностей, только будущая установка. После: понятная область Android-проекта, пять development-направлений, связанный сценарий использования, полезная мотивационная вставка и явный статус разработки. Навигация, footer, темы, типографика Onest/Unbounded и палитра прежние. Нет fake screens, charts/user data, отзывов, дат, процентов, аналитики или сбора email.

- Hero уточняет предназначение, сохраняет оригинального котика и информационный CTA вместо скачивания.
- Возможности: две крупные тематические карточки питания/веса и три компактные активности/тренировок/статистики. Каждый блок подписан как направление разработки; release features остаются пустыми.
- «Свой ритм»: четыре связанных шага предполагаемого будущего опыта; отдельный disclaimer о том, что публичного выпуска нет. Это не инструкция уже доступного приложения.
- Маскот: исходный calm вhero и исходный hint вмотивационной карточке. Новых поз **не предлагается и не требуется**; оригиналы не перерисованы. Activity icon — path изAndroid `res/drawable/ic_run.xml`, белая заливка адаптирована вcurrentColor; остальные badge — текстовые подписи, не придуманные Android icons.
- Статус: разработка продолжается, публичного APK нет, сведения появятся после утверждения; нет графика готовности/сроков.
- FAQ: доступность, назначение, Android, официальная информация, будущая установка, privacy, контакт. Установка и gallery сохранены, без дублей будущего journey. Юридический текст не менялся.

## Снимки настоящей development-сборки

| Экран | Светлая | Тёмная |
|---|---|---|
| Desktop1440, целиком | [После](screenshots/phase2/after-1440-light.png) · [До](screenshots/phase2/before-1440-light.png) | [После](screenshots/phase2/after-1440-dark.png) · [До](screenshots/phase2/before-1440-dark.png) |
| Mobile390, целиком | [После](screenshots/phase2/after-390-light.png) · [До](screenshots/phase2/before-390-light.png) | [После](screenshots/phase2/after-390-dark.png) · [До](screenshots/phase2/before-390-dark.png) |
| Направления1440 | [Открыть](screenshots/phase2/directions-1440-light.png) | [Открыть](screenshots/phase2/directions-1440-dark.png) |
| Journey/mascot1440 | [Открыть](screenshots/phase2/journey-1440-light.png) | [Открыть](screenshots/phase2/journey-1440-dark.png) |
| Статус1440 | [Открыть](screenshots/phase2/status-1440-light.png) | [Открыть](screenshots/phase2/status-1440-dark.png) |

Такие же section captures390px находятся в screenshots/phase2. Это снимки сайта, **не Android screenshots**. Полные PNG можно скачать и увеличить до1:1.

## Все новые продуктовые описания и их источники

Read-only Android snapshot: `6c4e8c081c578108bb05c4ee3c7f6f15ebc9eea6`. [Дерево исходников](https://github.com/sashaermin/ya-hudeyu-android/tree/6c4e8c081c578108bb05c4ee3c7f6f15ebc9eea6/app/src/main/java/com/aleksandr/stepstracker/ui). Source inventory подтверждает область разработки, **не функциональность распространяемого APK**. Скачивания/сборки/Android-тестов не проводилось, Android-ветки/сессия не менялись.

| Описание вhero/cards/journey/FAQ | Опора относительно ui/ | Граница утверждения |
|---|---|---|
| Питание, дневник/КБЖУ | nutrition/NutritionScreen.kt | Направление разработки; точность/полнота учёта не обещается |
| Вес и наблюдение изменений | weight/WeightScreen.kt | Только область проекта, без обещаний похудения |
| Движение/активность | workout/ActivityHubScreen.kt | Без обещаний GPS/датчиков/фоновой работы |
| Планирование и записи тренировок | workout/WorkoutTemplatesScreen.kt | Нет гарантий отдельных упражнений/нагрузок |
| Обзоры/визуализация записей | stats/StatsScreen.kt | Нет вымышленных данных/готовых charts |
| Android вразработке, APK не открыт, даты нет | Авторизация владельца Phase2; Android ACTIVITY_PROGRESS_V1785_STATUS.md прямо отделяет source inventory от acceptance/build | Нет public beta/app-store обещаний |
| Здесь появится утверждённый выпуск | Авторизация Phase2, действующие site/release gates | Не обещание даты или готового APK |
| Privacy/контакт/будущая установка | неизменённая privacy.html, существующие support иinstall copy | Не добавлены гарантии sync/backup/update для неизвестной сборки |

Тексты мотивации — редакционное приглашение к небольшим наблюдениям, не продуктовая функция и не медицинское обещание. Вdata/site.json planned_areas отдельно отverified features/screenshots, сsource SHA/path иобязательным in-development status; source evidence вpublic HTML не выводится. Полные release gates сохранены.

## Проверки и ограничения

[Машинный отчёт](verification/phase2-review.json), подробности — verification/phase2/.48 viewport/theme layouts:320/360/390/430/768/1024/1440/1920×light/dark×Chromium/Firefox/WebKit.12axe runs,0violations; ссылки/FAQ/menu/focus/themes/gallery fixtures иошибка изображения PASS.12 CSS text/spacing cases, reduced motion/skip-link;6no-JS cases;privacy320×2темы PASS.31website +68notification unit tests PASS;JS syntax PASS. Все изображения загружаются, включая lazy hint; browser QA теперь явно доводит lazy image до успешной загрузки, а не считает её синхронной.

Сайт осмотрен поactual captures; автоматические PASS не заменяют приёмку владельца или полную WCAG-сертификацию. Физические Android/iOS, настоящий Safari, screen reader/native zoom иnative WebKit swipe не проверялись; Firefox touch unsupported. Безapproved APK нельзя проверить actual release functions/screens/download. Исходные7release-blocked/2manual UI items остаются открытыми. FAQ/privacy требуют обычной владелецкой проверки перед будущей публикацией.

## Просмотр и точный источник

Проверенный ZIP содержит только23public files, не корень checkout; SHA-256 `37e3a7a063fcc443d80606b681949d07f9755ddabbbba39928b64ca1bc7bc6d1`. APK disabled, noindex/Disallow сохранены. Размер ZIP436989bytes; дополнительная иллюстрация — исходный hint. **Точный UI source SHA: `27247f4bf8b5df0efedf4d79a98a972d1d6d8e3c`.** [Скачать проверенный review artifact](https://github.com/sashaermin/ya-hudeyu/actions/runs/39146021733/artifacts/12143292977) из [run39146021733](https://github.com/sashaermin/ya-hudeyu/actions/runs/39146021733), attempt1. Artifact12143292977 существует/не expired на момент проверки; срок хранения до25.10.2026 19:39МСК. Actual upload→download archive roundtrip:23files/4rendered views/noindex=true/APK=false/page_errors0, clean source. CI99unit tests PASS; Telegram topic6 accepted55/56. Последующие documentation-only checkpoints не меняют эти UI bytes.

Архив — **для локального просмотра**, внешнего hosted preview нет. Нажать ссылку artifact выше (требуется обычный доступ кэтому GitHub-репозиторию), скачать ZIP и распаковать внешний bundle, затем вложенный website-preview.zip вreview-site. На **своём компьютере** выполнить `python3 -m http.server 8080 --directory review-site`, открыть localhost:8080 вбраузере. Это локальный сервер владельца, не ссылка вcloud workspace. Сверить SHA-256 внутреннего ZIP сэтим отчётом; source_commit/source_worktree_dirty=false иper-file manifest проверяются CI. Retention7дней, затем artifact может быть недоступен; воспроизвести пакет через `python3 tools/package_preview.py` източного verified source SHA, сверить тотже ZIP digest. Изменение только документов не меняет innerZIP bytes.

## Что требуется утвердить

Визуальное представление иdevelopment-copy этого кандидата, особенно формулировки направлений ибудущего опыта. Текущая задача **не разрешает публикацию**; старый publication approval относится кпрошлому website release. После review — исправления по замечаниям либо отдельное явное разрешение конкретного нового public-only release. Сейчас STOP перед production, main/Pages/APK/indexing не менять. Утверждение APK — отдельная, всё ещё открытая задача.
