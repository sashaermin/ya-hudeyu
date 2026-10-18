# Аудит источников · этап 0

Дата: 18.10.2026. Это отчёт реализации утверждённого мастер-ТЗ, не новое ТЗ.

## Снимки и границы

- Сайт: `sashaermin/ya-hudeyu`, база `main` / `9a0857ce260540ad604f344565d535a8d47b2fa0`.
- Android main: `9345245ba2d67ddc28b4ceb7f92b0bbe72e5a596`.
- Эталон текущего Android UI: read-only снимок `work/activity-progress-v6-4daeaa5` / `874de91cb626b6f0e78532963b378d86901b97d9`. Отдельный clone без checkout в `/tmp`; исходная сессия и удалённые ветки не изменялись. Более поздние коммиты могут отличаться.
- Сайт: четыре исходных файла, без сборки/зависимостей/CI. CNAME `yahudeyu-app.ru`; privacy.html и контакты сохраняются побайтно.
- HTTPS-домен и GitHub Pages API из среды недоступны (proxy 403); Git read работает. GitHub Pages предполагается по CNAME и структуре, но настройки публикации не подтверждены. Перед публикацией проверить Pages source и workflow в GitHub Settings.

## UI и ресурсы

Пути ниже относительно `app/src/main/` Android, ссылки привязаны к неизменяемому SHA:
[исходники](https://github.com/sashaermin/ya-hudeyu-android/tree/874de91cb626b6f0e78532963b378d86901b97d9/app/src/main).

| Источник | Проверено | Применение |
|---|---|---|
| `java/com/aleksandr/stepstracker/ui/theme/Theme.kt` | Onest для текста; Unbounded SemiBold для заголовков; system/light/dark; default accent green | локальные шрифты, темы сайта |
| `…/ui/theme/Color.kt` | фон light #F7F4EF, surface #FFFFFF, ink #1D1B22; dark #131117 / #1E1B23 / #F4F1F7 | CSS-токены |
| `…/settings/AccentColors.kt` | green #58A936 (один из 12 акцентов) | основной акцент сайта |
| `…/ui/theme/HudeyuComponents.kt` | радиусы 14/18/24/28, капсула; action 52, touch 48; интервалы 4/8/12/16/24 | компоненты и адаптация на web |
| `…/ui/theme/HudeyuSystem.kt`, `HudeyuField` | food #FFEFDC / #36281B, steps #E1F4E7 / #17301F, weight #EEEAFE / #272243 | тематические поля |
| `…/ui/theme/BrandSplash.kt` | слоган «Маленькие шаги к большим изменениям», кот на тёплом поле | hero |
| `res/drawable/mascot_{calm,celebrate,hint}.webp` | оригинальные позы | иллюстрации, без генерации |
| `res/drawable/onboarding_welcome_cat.webp` | оригинальная иллюстрация с текстом онбординга | сохранена как исходник; не используется в hero |
| `res/drawable-nodpi/logo_wordmark_green_{light,dark}.png` | оригинальные логотипы обеих тем | шапка, подвал |
| `res/mipmap-xxxhdpi/ic_launcher_green.png` | оригинальная иконка | favicon/OG |
| `res/font/*`, `assets/licenses/*-OFL.txt` | кириллица, SIL OFL | локальное размещение с лицензиями |

Точные пути, SHA и соответствие скопированных файлов: `ASSET_SOURCES.json`. Android dp переводятся в CSS px как базовая геометрия; размеры hero и web-сетки — адаптация, а не Android-токены.

## Функции: исходный код ≠ выпущенный APK

| Функция | Свидетельство в снимке Android | Выпуск / публичный контент |
|---|---|---|
| Питание и КБЖУ | `…/ui/nutrition/NutritionScreen.kt`: NutritionScreen, приёмы пищи, калории, макронутриенты | APK не подтверждён; карточка не публикуется |
| Вес | `…/ui/weight/WeightScreen.kt`: WeightScreen, запись и история веса | APK не подтверждён; карточка не публикуется |
| Тренировки | `…/ui/workout/WorkoutScreen.kt` | наличие исходника; поведение APK не проверено |
| Шаги и сравнение периодов | `activity_progress_v6/evidence/e-persistent-comparison/adaptive-matrix/persistent-layout-portrait-font100-light-task3_period_expanded_activity.png` | изображение тестовой разработки, просмотрено только как UI-референс |
| Backup / Drive | `…/backup/BackupManager.kt`, `…/sync/DriveSyncClient.kt` | наличие кода не доказывает надёжность/доступность релиза; маркетинговые обещания отключены |
| Поделиться графиками, G3/G4 | `HANDOFF.md` рабочей Android-ветки | разработка; не рекламируется |

## Блокеры выпуска

1. Не получен конкретный утверждённый APK / его стабильный HTTPS URL. В просмотренных Git trees нет APK, `git ls-remote --tags` не вернул тегов. GitHub API недоступен (403), web releases вернул 404; это **не доказывает отсутствие приватных релизов**. Не использовать исторический v1372 или номер версии исходников как сведения о выпуске.
2. Скриншоты в рабочей ветке — тестовые evidence; соответствие выпускаемому APK не установлено. Не помещать их в публичную галерею. Нужны обезличенные экраны утверждённой сборки с версией/темой.
3. До релиза нужны визуальное одобрение владельца, подтверждение Pages source и юридическая проверка. Изменения юридического текста не входят в эту реализацию.

Независимая работа продолжается: оригинальные активы, дизайн-система, секции со структурными состояниями, доступность, конфигурация релиза с безопасным запретом скачивания/публикации до проверки. Вопрос об APK и скриншотах отправлен владельцу; секреты не запрашивались.
