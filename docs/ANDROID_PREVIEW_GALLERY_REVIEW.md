# Предварительная Android-галерея — review-пакет

**Статус: реализовано и локально проверено, development only.** Все 11 исходных JPEG получены ZIP-вложением владельца. Прежний технический блокер файлов устранён. Агент выполнил обезличивание по прямому указанию «сам обезличь и выполни тз»; повторное разрешение на обработку не требуется. [Исходное задание](../project_specs/ANDROID_PREVIEW_GALLERY_AUTHORIZATION_2026-10-20.md) и [уточнение](../project_specs/ANDROID_PREVIEW_ANONYMIZATION_AUTHORIZATION_2026-10-20.md) сохранены без замены мастер-ТЗ. Публикация галереи **не разрешена**.

## Реализация

- Главная: «Посмотрите, как выглядит приложение», точный подзаголовок задания, предварительный label, disclaimer под галереей. Это отдельная демонстрационная коллекция, не `site.screenshots` утверждённого APK.
- Пять категорий с обычными якорями: Обзор, Питание, Активность, Вес и прогресс, Цели и здоровье. Метаданные сохраняют исходный порядок 11 экранов; в UI они сгруппированы по категориям: Сегодня, Дополнительные карточки; Питание; Активность, GPS; Прогресс, Мой путь, План, Графики; Профиль, Все цели. Каждая карточка имеет заголовок, фактическую подпись, alt и предварительную маркировку.
- Desktop: три колонки, tablet 801–1024px: две; mobile: одна крупная карточка, соседняя видна частично, native scroll snapping, свайп и кнопки. Использованы существующие токены, шрифты, mascot и темы; другие разделы не переделывались.
- Native dialog: полноразмерное изображение, назад/вперёд, клавиатура, Escape, focus trap/restore, загрузка/ошибка/повтор, свайп. Кнопка «Масштаб 100%» включает исходный размер отредактированного файла с прокруткой, включая клавиатурную прокрутку области. Это не оригинал приватного снимка.
- Без JS доступны категории и отдельные ссылки на все 11 полных **обезличенных** WebP; переключатели, требующие JS, скрыты до инициализации. Reduced motion сохраняется.

## Изображения и приватность

[Инвентарь и SHA-256](verification/android-preview-assets.json), [конфигурация](../data/android_preview.json). 11 обработанных изображений, по две WebP-версии: карточка 420px и увеличение 843×1866px. Всего 22 файла, **1 091 352 байта**. EXIF/XMP/ICC metadata отсутствуют; исходные JPEG, ZIP, личные значения и приватные OCR-транскрипты не включены в Git или публичный артефакт.

Все 11 файлов редактировались с прямой ссылкой на соответствующий исходник, затем проверены визуально. Имя заменено на «Гость», даты и индивидуальные нормы/история/цели — согласованными условными примерами. Удалены системные панели, уведомления/сведения устройства. Медицинские название/дозировка/расписание и личные напоминания заменены нейтральными подписями. Реальная карта и точка полностью заменены неидентифицируемой условной схемой. График стал иллюстративным; сломанный перенос в изображении плана исправлен только в демонстрационном asset, Android не изменялся.

Дополнительная OCR-проверка `rus+eng` выполнена на 11/11 изображениях: **0 совпадений с проверяемыми исходными персональными/чувствительными значениями**. Это дополнение к визуальной проверке, а не доказательство математически полного удаления любых данных. Источник русского OCR model и проверенный git blob записаны в инвентаре. Приватный список исходных значений намеренно не хранится в репозитории.

Условная история: 84→82кг, цель78кг, осталось4кг,33%; 20 января2026, план−0,5кг/неделю/дефицит550ккал, ориентир17марта2026; рацион1800ккал, БЖУ100/60/215г; цель8000шагов. Показатели придуманы для демонстрации, не являются прогнозом/медицинским советом или расчётами проверенного APK.

**Ограничение:** обработка изображений может менять мелкую типографику и геометрию. Это отредактированные демонстрации на основе предоставленного UI, не точные скриншоты финальной версии. Кнопки и пункты меню подтверждают только наличие соответствующих элементов в исходных снимках. Работоспособность поиска/сканирования, Health Connect, GPS и расчётов не выводится из картинок; новых release claims не добавлено. Исходный брендинг сайта и отдельный оригинальный маскот сохранены.

## Проверки

- 56 website unit tests (включая9 новых gallery tests) и68 notification tests: PASS. Проверены состав/порядок/категории, captions/escaping, целостность22файлов, отсутствие metadata, небезопасные пути/symlink, обязательный privacy-review и отдельный production gate.
- Chromium, Firefox, WebKit: **48 responsive cases** (320/360/390/430/768/1024/1440/1920×2темы×3движка), все11изображений увеличивались в каждой комбинации;24axe runs без нарушений WCAG A/AA. Категории/фокус/клавиатура/zoom/ошибка-повтор проверены. [Задержанная загрузка](verification/android-preview/loading.json):loading visible,image hidden,zoom disabled до реального завершения запроса;после успеха состояния восстановлены. [Chromium](verification/android-preview/chromium.json), [Firefox](verification/android-preview/firefox.json), [WebKit](verification/android-preview/webkit.json).
- 24 no-JS cases; реальные CDP touch events проверили свайпы mobile gallery иviewer вChromium. Физические устройства и native Safari/VoiceOver/TalkBack не проверялись; движковая эмуляция их не заменяет.
- Регрессии: [главная](verification/android-preview/homepage.json)16layouts/темы/menu/persistence/4axe/legacyviewer; [FAQ](verification/android-preview/faq.json)16layouts/4axe/6noJS/33disclosures; [download](verification/android-preview/download.json)16layouts/4axe/6noJS/unavailable/sharedtheme. Ошибок JS не обнаружено.
- [6 дополнительных коротких viewport/text-spacing cases](verification/android-preview/text-adaptation.json), включая320×568, PASS. CSS-симуляция не является nativezoom/screenreader проверкой.
- [Локальный mobile Lighthouse](verification/android-preview/lighthouse.json): **93/100/100/69**, CLS≈0,000014. SEO69 ожидаем приnoindex. Это один локальный HTTP-замер, не production/реальное устройство; cache/compression на простом локальном сервере не эквивалентны Pages.
- Воспроизводимый review ZIP:46 public files; SHA-256 `faa3c3e406cb0baab71155572ae95bc901aa7abc2760c41d07d512c6c2c03c51`. Локальный archive→render rehearsal:4homepage+4download views PASS. Чистый CI upload→download→render проверяется после push; точное подтверждение в handoff/CI evidence.

## Снимки сайта

Сняты с реально отрисованного development-сайта, не созданы генератором. Галерея длиннее viewport; поэтому отдельно показаны начало, карточки, предупреждение и просмотрщик.

| Состояние | 390 светлая | 390 тёмная | 1440 светлая | 1440 тёмная |
|---|---|---|---|---|
| До изменений, локальный render production6810206 | [до](screenshots/android-preview/before-390-light.png) | [до](screenshots/android-preview/before-390-dark.png) | [до](screenshots/android-preview/before-1440-light.png) | [до](screenshots/android-preview/before-1440-dark.png) |
| Заголовок/категории | [снимок](screenshots/android-preview/gallery-390-light.png) | [снимок](screenshots/android-preview/gallery-390-dark.png) | [снимок](screenshots/android-preview/gallery-1440-light.png) | [снимок](screenshots/android-preview/gallery-1440-dark.png) |
| Карточки | [снимок](screenshots/android-preview/cards-390-light.png) | [снимок](screenshots/android-preview/cards-390-dark.png) | [снимок](screenshots/android-preview/cards-1440-light.png) | [снимок](screenshots/android-preview/cards-1440-dark.png) |
| Disclaimer | [снимок](screenshots/android-preview/disclaimer-390-light.png) | [снимок](screenshots/android-preview/disclaimer-390-dark.png) | [снимок](screenshots/android-preview/disclaimer-1440-light.png) | [снимок](screenshots/android-preview/disclaimer-1440-dark.png) |
| Viewer | [снимок](screenshots/android-preview/viewer-390-light.png) | [снимок](screenshots/android-preview/viewer-390-dark.png) | [снимок](screenshots/android-preview/viewer-1440-light.png) | [снимок](screenshots/android-preview/viewer-1440-dark.png) |

## Как посмотреть и что дальше

1. Проще всего начать со снимков выше, затем сообщить замечания к 11 изображениям, подписям и расположению галереи. Это контентная/визуальная приёмка development, не APK approval.
2. Для интерактивного просмотра скачать `website-preview-<SHA>-attempt-1` из успешного website-checks run, распаковать внешний artifact и внутренний `website-preview.zip`, выполнить `python3 -m http.server 8002` в распакованной папке, открыть `http://localhost:8002/`. ZIP хранится7дней; его можно воспроизвести из verifiedGitSHA командой `python3 tools/package_preview.py`. Это **не размещённый веб-preview**.
3. После review — замечания или отдельная явная авторизация новой website публикации. Сейчас **STOP перед owner review**, никаких main/deploy/APK/indexing операций.

Production остаётся `6810206125ccf72080c8a7aa29072041d5812f0f`; Phase2/FAQ33/8 и`/download/` недоступная бета сохранены. `data/publication.json`, `data/release.json`, privacy/CNAME/robots/deployment/workflows иAndroid/Windows не изменялись. Preview approval отсутствует: production builder отклоняет эту галерею без отдельного разрешения точного manifestSHA. Release-specificscreens/APK требования master остаются отложенными; предварительная галерея их не закрывает.
