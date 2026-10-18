# Релизный контент: состояние и подключение

**Ни один APK не утверждён владельцем для публичного распространения.** Это прямое решение 18.10.2026, не технический дефект сайта. `data/release.json` остаётся unverified, download action недоступен. Старый v1372, номер версии build.gradle и dev evidence не являются релизом.

## Единственные источники контента

- `data/site.json`: основной контент, FAQ, features и screenshots.
- `data/release.json`: один конкретный APK и его сведения. Не дублировать URL/версию в шаблоне.
- `data/publication.json`: отдельное разрешение сайта, режим выпуска и независимое разрешение индексации.
- `docs/ASSET_SOURCES.json`: брендовые активы, оригинальный Android commit/path, производные WOFF2.

Каждая feature: `title`, `description`, `verified_version` (точно release.version), `evidence` (проверка APK с версией, сценарием и результатом); optional `icon` — только существующий оригинальный ресурс в assets/.

Каждый screenshot: `src` (assets/screens/…), `width`, `height` (реальные размеры), `alt`, `caption`, `verified_version`, `evidence` (сборка/сценарий/обезличенные данные), `approved_for_publication: true`. Файлы сохранять в исходных пропорциях; не рисовать UI. Первый экран используется также в hero. Для обеих тем нужны подтверждённые изображения; до их получения не выдавать dev screenshots за release. Viewer готов к подключению; отсутствие изображений отображается как структурное состояние, а не поддельный телефон.

## После выбора владельцем конкретного артефакта

1. Сохранить ссылку на явное разрешение в `approval_reference`; `approved_for_distribution: true` ставить только по этому разрешению. Разрешение APK отдельно от разрешения deploy.
2. Скачать именно разрешённый файл по HTTPS, проверить, что скачан ZIP/APK, а не HTML/login response; размер/полный SHA-256 посчитать по bytes. Проверить signing certificate (`apksigner verify --print-certs`) и сопоставить с доверенным сертификатом приложения; не менять/не переподписывать APK.
3. Из фактического AndroidManifest APK (aapt/apkanalyzer) проверить package, versionName/versionCode и minSdk. Сопоставить с ожидаемым приложением и релизом. `minSdk 26` в просмотренном dev-коде **не публикуется** как требование неизвестного APK.
4. Установить эту сборку в согласованной тестовой среде, подтвердить заявляемые функции и снимки экранов; не использовать активный Android workspace/сессию Claude для этих действий.
5. Заполнить `version`, ISO `date`, `url`, целочисленный `size_bytes`, lowercase `sha256`, `min_android`, точный `source_commit`, `verification_note` (сертификат, manifest, сценарии, результат). `changes` — только подтверждённая история этого выпуска.
6. Только после этих проверок поставить `status: verified`, заполнить version-matched features/screenshots. Пустой список функций или галереи блокирует полный (`release_mode: full`) production build. Уже опубликованный coming-soon режим — отдельное явно разрешённое исключение без APK/features/screenshots. Сборщик проверяет полноту и согласованность метаданных, но **не заменяет** независимую проверку APK или разрешение владельца.
7. Проверить HTTPS download URL полным скачиванием, размер и хеш повторно; проверить ссылки, mobile layout, light/dark, gallery и доступность, согласовать визуальный вид и юртекст. Закрыть registry `site-approved-android-release` с resolution.
8. В development выбрать `release_mode: full` в `data/publication.json` для APK-кандидата; сохранить `indexing_approved: false`. Прошлое разрешение coming-soon/UI/UX выпуска не разрешает этот новый выпуск: до новой авторизации выставить `approved: false`, `approval_reference: null`. Обычный `python3 tools/build.py` позволяет проверить полный контент в draft с noindex. Только после отдельного разрешения конкретного нового website-кандидата записать его ссылку и `approved: true`, затем проверить `python3 tools/build.py --production`. Это локальная сборка, не deploy; main/merge/PR/публикация требуют соответствующей отдельной авторизации.
9. Сверить новый public-only manifest, выполнить release-content/browser/accessibility QA и приёмку; сохранить production rollback по `docs/FIRST_RELEASE.md`. Никакой старый site approval не использовать повторно для будущей публикации. Индексацию не включать вместе с APK автоматически.

## SEO и разделение артефактов

Draft `_site`: robots noindex,nofollow; robots.txt Disallow. Production build дополнительно проверяет website approval и режим выпуска. Индексация регулируется отдельно: при текущем явном `indexing_approved: false` и HTML, и robots.txt сохраняют запрет даже в production. Не удалять это поле: default при его отсутствии — разрешённая индексация для успешно прошедшего production gate. Менять на true можно только по отдельному решению владельца, не ради Lighthouse score. Canonical/OG/Twitter/favicon и SoftwareApplication содержат достоверные поля без оценок/цены/цифр пользователей. SHA и поля релиза появляются только из проверенной конфигурации.

Опубликованный артефакт — `_site` с белым списком файлов. В нём нет docs, project_specs, QA fixtures, секретов и исходной JSON-конфигурации. Оригиналы ресурсов и лицензии сохранены в Git; production содержит только используемые ресурсы. Шрифты WOFF2 с полным набором glyphs; сжатие без изменения дизайна, TTF сохранены для происхождения.

## Действующая политика

Юридический текст, заголовки, дата и ссылки `privacy.html` сохранены; оформление и reflow обновлены в опубликованном UI/UX выпуске. Это не побайтная копия исходной страницы до первого релиза; доказательства сохранности legal body — `docs/verification/uiux-production-release.json` и UI QA. Она описывает Google-аккаунт/Drive; не расширять её произвольно и не выводить из неё гарантии конкретной сборки. Перед публикацией владелец проверяет юридическую актуальность. Шаблон главной использует ссылку `/privacy.html`; перенаправление не требуется.

## Дополнительный gate публикации сайта · этап 3B

`data/publication.json` отделяет разрешение публикации **сайта** от разрешения распространения APK. Текущее состояние: `approved: true`, `release_mode: coming-soon`, `indexing_approved: false`; `approval_reference` ссылается на уже выполненную узкую авторизацию UI/UX выпуска. Production — `8fb7bf2920a89f39e1ed3a56d53ada91f468b715`, rollback — `9b39ffaf35c48973b8115b630ba0d06165ad09a4`. Это описание состоявшегося выпуска, не разрешение следующего. APK остаётся `unverified`, `approved_for_distribution: false`; реальные features/screenshots пусты.

Режим `coming-soon` требует website approval и запрещает verified APK, features и screenshots. Режим `full` (также default при отсутствии release_mode) требует verified APK с отдельным owner approval, version-matched evidence функций и approved screenshots. Даже корректный полный контент не разрешает production render без website approval/reference. Ни один режим не является командой публикации. Конфигурация не копируется в `_site`; draft всегда noindex.

## Проверенная готовность к APK-инкременту

[Readiness evidence](verification/apk-readiness.json): существующий builder собрал полный production fixture в изолированном временном каталоге, без правок реальных data-файлов или public assets. Проверены download URL, version/date/SHA, changelog, hero screen, feature cards, gallery, копирование используемого screen asset, noindex/robots Disallow и исключение private data. Coming-soon отверг тот же APK fixture. Использованы только TEST ONLY metadata и исходный mascot как QA asset, **не реальный APK/скриншот приложения и не release acceptance**.

27 существующих build/policy/package/workflow/handoff tests PASS, включая независимость APK/site approvals, escaping и reproducible allowlisted archive. Конфигурации и существующих компонентов достаточно; перестройка сайта не требуется. Фактический download/signature/manifest, release-specific функции/FAQ и screenshots можно проверить только после получения утверждённого артефакта. Физические устройства, screen reader/native zoom и визуальная приёмка будущего release-content остаются отдельными проверками.
