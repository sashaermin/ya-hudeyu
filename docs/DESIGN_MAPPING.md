# Android → Web · этап 1

Источник: Android `874de91cb626b6f0e78532963b378d86901b97d9`; точные пути см. SOURCE_AUDIT и ASSET_SOURCES.json.

| Android | CSS | Компоненты |
|---|---|---|
| AccentColors.green #58A936 | --primary | CTA, маркеры |
| hudeyuContentOn(green), тёмный контент | --on-primary #131117 | подпись CTA; проверяется контраст |
| BackgroundLight / Graphite | --bg #F7F4EF / #131117 | страница |
| SurfaceLight / GraphiteSurface | --surface #FFFFFF / #1E1B23 | карточки, меню, viewer |
| Ink / onSurface | --ink #1D1B22 / #F4F1F7 | текст, фокус |
| MutedLight / MutedDark | --muted #67626E / #ABA4B5 | вторичный текст |
| surfaceContainer | --track #EFEAE3 / #26222C | поля, резерв галереи |
| outlineVariant | --line #E8E2D9 / #3A3440 | разделители |
| outline | --outline #8C8692 / #77707F | границы контролов |
| error | --error #D70015 / #FF453A | ошибки изображения |
| HudeyuField.food.field / text | --food / --food-ink | поле котика |
| HudeyuField.steps.field / text | --steps / --steps-ink | релиз, текстовые акценты |
| HudeyuField.weight.field / text | --weight / --weight-ink | категории |
| Onest Regular / SemiBold | @font-face Onest 400/600 | основной текст и элементы управления |
| Unbounded SemiBold | @font-face Unbounded 600 | hero, заголовки |
| HudeyuField / Interactive / Card / SheetShape | --field 14 / --interactive 18 / --card 24 / --sheet 28 px | поля, карточки, панели |
| HudeyuControlShape / BadgeShape | --pill / 50% | CTA, icon buttons |
| HudeyuSpaceXs/Sm/Md/Lg/Xl | --xs/sm/md/lg/xl = 4/8/12/16/24 px | базовый ритм |
| HudeyuActionHeight / TouchTarget | 52px / 48px | кнопки / touch |
| HudeyuCardElevation | --shadow, очень мягкая тень | карточки |

Веб-адаптация: hero до 64px (Android displayLarge 44sp); сетка до 1320px; вертикальные интервалы секций 48–96px. Это значения для сайта, не выданные за токены приложения. Текстовые акценты используют HudeyuField.text вместо малоконтрастного зелёного на белом. Зелёный CTA имеет тёмную подпись.

Оригинальные маскоты и логотипы сохранены без изменения пропорций/цветов. Онбординг с встроенным текстом не используется как новый маскот. Файлы шрифтов локальны, обе OFL-лицензии приложены. Light/dark следуют system до ручного выбора; выбор хранится локально, ранний theme.js предотвращает вспышку темы. Фокус, hover/active, disabled и error определены; сетевые loading-состояния не нужны статическому документу.

Проверка этапа 1: файлы/лицензии сверены с Git blobs; синтаксис theme.js проверен node. Полная проверка браузером и контраста — этап 4 после подключения HTML.


UI audit U1/U2: current Android960e43b Theme/Color/Components/System/AccentColors и original fonts/logo/mascot совпали с source (uiux-android-reference.json). Privacy presentation теперь использует shared palette/Onest/theme control; Onest для длинного document heading сохраняет слово на320px без произвольного разрыва, legal text/URL неизменны. No-JS использует те же Android dark tokens; palette не инвертировалась автоматически. Gallery status/error остаются в существующей системе компонентов; никаких новых mascot poses/screens/дизайн-концепций. Это development changes, production9b39ffa прежний.
