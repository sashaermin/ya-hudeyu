# Покритериальный UI/UX-аудит сайта «Я ХУдЕЮ»

Основание — неизменённый [мастер-ТЗ](../project_specs/WEBSITE_MASTER_TZ_2026-10-18.md), не новое ТЗ/roadmap. Рабочая база4a8755665a14d9c4d6eb9c3799fa99c7ebbee119; production9b39ffa **не меняется**. Единственный roadmap — IMPLEMENTATION_PROGRESS.md. Этот документ — детализация требований/evidence, не новая концепция. COMPLETE означает реализацию проверенного конкретного свойства, не автоматическую приёмку всего продукта/WCAG.

## Источники и метод

Read-only Android current960e43b545fb0203e1199256db93885acca6e33d: Color.kt, Theme.kt, HudeyuComponents.kt, HudeyuSystem.kt побайтно совпали с design source874de91c. Current AccentColors и original font/mascot/logo bytes также совпадают с originals сайта; [SHA/blob proof](verification/uiux-android-reference.json). Источники Theme/Color/Components/System относительно `app/src/main/java/com/aleksandr/stepstracker/ui/theme/`; [Android snapshot](https://github.com/sashaermin/ya-hudeyu-android/tree/960e43b545fb0203e1199256db93885acca6e33d/app/src/main). Android dev screenshot осмотрен только как reference, не как released UI. Web hero/grids — адаптация под сайт, не придуманный Android screen. Android checkout/ветки/процессы не изменены.

Прочитаны AGENTS/handoff/progress/design mapping/QA/release content, проверены source selectors и rendered draft. [Before reproduction](verification/uiux-before.json), [mobile before](screenshots/uiux/before-390-light.png), [desktop before](screenshots/uiux/before-1440-dark.png), [no-JS overlap](screenshots/uiux/before-nojs-320.png), [privacy overflow](screenshots/uiux/before-privacy-320.png). Исторические production99/100/100/69 и automated matrices — контекст, не основание объявить все UI требования выполненными. Для каждого исправления ниже нужен отдельный targeted browser proof; после visual changes — fresh matrix/axe/screenshots.

## Покрытие44 проверяемых требований (после U1/U2)

COMPLETE: 35; PARTIAL: 0; MISSING: 0; BLOCKED_BY_RELEASE_CONTENT: 7; REQUIRES_MANUAL_VERIFICATION: 2.

| ID | Мастер-ТЗ | Требование | Статус | Точный source reference | Evidence / граница |
|---|---|---|---|---|---|
| U01 | §3/5 | Android primary/background/surface/ink/error | COMPLETE | styles/site.css:4–5; Color.kt/HudeyuSystem.kt | Токены сверены с текущим Android SHA; контраст и rendered цвета проверяются отдельно. |
| U02 | §3/5 | Onest/Unbounded, веса и читаемость | COMPLETE | styles/site.css:1–3,6; Theme.kt | Локальные лицензированные шрифты совпадают с Android; headings/paragraphs визуально осмотрены. |
| U03 | §5 | Spacing и web grids | COMPLETE | styles/site.css:4,6–10; HudeyuComponents.kt | 4/8/12/16/24 tokens; адаптивные 1/2/3-column grids — web-адаптация, не Android pixel clone. |
| U04 | §5 | Радиусы и тени | COMPLETE | styles/site.css:4–6; HudeyuComponents.kt | 14/18/24/28/pill; мягкая light shadow и dark none соответствуют mapping. |
| U05 | §3/7.1 | Оригинальные logo/icon | COMPLETE | index.html:head/header/footer; docs/ASSET_SOURCES.json | Текущие Android logo bytes совпадают; WebP derivatives сохраняют пропорции. |
| U06 | §4.2/5 | Оригинальный маскот без подмены | COMPLETE | tools/build.py:hero_visual; styles/site.css:.hero-cat | Current Android mascot bytes совпадают; natural aspect ratio сохранён. |
| U07 | §2/3/7.8 | Техническая визуальная преемственность Android | COMPLETE | docs/DESIGN_MAPPING.md; uiux-android-reference.json | Текущие theme/components files неизменны с принятого design source; осмотрен dev-reference, не выдаётся за релиз. |
| U08 | §5 | Начальное отображение сохранённой темы | COMPLETE | index.html:head; scripts/theme.js:1–18 | Inline theme script до CSS; storage errors обрабатываются; проверить pre-style dark state. |
| U09 | §5 | Ручной выбор и persistence темы | COMPLETE | scripts/site.js:updateThemeButton/click | system/light/dark, localStorage, reload; runtime не определяет продуктовые функции. |
| U10 | §5 | Изменение системной темы | COMPLETE | scripts/theme.js:matchMedia listener | Реакция только в system mode, ручной выбор не перезаписывается. |
| U11 | §5/6 | Системная dark тема без JS | COMPLETE | styles/site.css:root selectors | CSS fallback использует те же dark tokens и logo при JS disabled;6 no-JS width/theme cases PASS. |
| U12 | §4.8/5/7.4 | Privacy: reflow и единая тема/типографика | COMPLETE | privacy.html:style/head | Privacy использует существующие Onest/tokens/theme control;16 cases/4axe PASS, legal content hash прежний. |
| U13 | §4.2/5 | Hero composition и CTA hierarchy | COMPLETE | index.html:hero; styles/site.css:.hero/.hero-actions | Оригинальный маскот, primary release-info/secondary possibilities; честный coming-soon вариант принят. |
| U14 | §4.1/4.2/4.6 | Активный CTA скачивания | BLOCKED_BY_RELEASE_CONTENT | tools/build.py:download_label/release; data/release.json | APK не утверждён: ссылка намеренно отсутствует; info CTA не подменяет финальное требование. |
| U15 | §4.2 | Настоящий hero screenshot | BLOCKED_BY_RELEASE_CONTENT | tools/build.py:hero_visual; data/site.json:screenshots | Нет approved release screens; маскот — честный временный hero, не скриншот приложения. |
| U16 | §4.3/5 | Геометрия и состояния feature cards | COMPLETE | styles/site.css:.feature-grid/.panel; tools/build.py:features | 3→1 columns; применённые generic fixture checks не означают проверку продукта. |
| U17 | §4.3/7.2 | Подтверждённый контент функций | BLOCKED_BY_RELEASE_CONTENT | data/site.json:features; docs/RELEASE_CONTENT.md | features=[]; проверяемого APK/evidence по функциям нет. |
| U18 | §4.4/5 | Галерея/placeholder layout и пропорции | COMPLETE | styles/site.css:.screen-empty/.gallery-track/.screen-item | Не подделывает UI; category navigation не обязательна без категорий. |
| U19 | §4.4/7.1 | Реальные экраны обеих тем | BLOCKED_BY_RELEASE_CONTENT | data/site.json:screenshots; docs/ASSET_SOURCES.json | Рабочие Android evidence не разрешены как release screenshots. |
| U20 | §4.4/7.5 | Стрелки/свайп/подписи/fullscreen | COMPLETE | scripts/site.js:show/ArrowLeft/ArrowRight/touch; index.html:viewer | Generic test-only gallery, captions и native dialog работают; physical swipe отдельно. |
| U21 | §4.4/5 | Модальный focus trap/Escape/restore | COMPLETE | scripts/site.js:dialog keydown/close; index.html:viewer | Фокус ограничен модальным dialog; закрытие возвращает opener. |
| U22 | §5 | Состояние загрузки изображения | COMPLETE | scripts/site.js:show; index.html:viewer-image | Loading role=status/aria-busy, stale image скрыт; delayed/load/error/retry/cancel/rapid reopen в4 engines PASS. |
| U23 | §5 | Ошибка изображения и восстановление | COMPLETE | scripts/site.js:image error; index.html:viewer-error | Видимый role=alert; повторный выбор сбрасывает ошибку; loading fix должен сохранить retry. |
| U24 | §4.5 | Установка без отключения общей защиты | COMPLETE | index.html:install/install-note | Условный процесс после выпуска; source-specific Android permission, без выдуманного minAndroid. |
| U25 | §4.6/7.3 | Фактическое скачивание проверенного APK | BLOCKED_BY_RELEASE_CONTENT | data/release.json; tools/build.py:validate/release | Ни один файл не выбран/не утверждён; download tests пока только fixtures. |
| U26 | §4.6 | Версия/дата/size/SHA/minAndroid/changelog | BLOCKED_BY_RELEASE_CONTENT | data/release.json; tools/build.py:fields | Схема/рендер готова, реальных проверенных данных нет. |
| U27 | §4.7 | FAQ disclosure/keyboard и честные ответы | COMPLETE | data/site.json:faq; tools/build.py:faq; scripts/site.js:details | Native details/summary с синхронизацией aria-expanded, без ложных гарантий. |
| U28 | §4.7 | Release-specific backup/sync/update FAQ | BLOCKED_BY_RELEASE_CONTENT | data/site.json:faq; docs/RELEASE_CONTENT.md | Текущие ответы явно не обещают непроверенное поведение будущей сборки. |
| U29 | §4.8 | Footer brand/contact/privacy/top/year | COMPLETE | index.html:site-footer | Ссылки и год присутствуют; прямой mailto, без сторонних tracker/API. |
| U30 | §4.8/7.6 | URL privacy и сохранение юридического текста | COMPLETE | privacy.html; docs/verification/first-production-rollback.json | Сохранять весь legal body/date/links; оформление не является изменением юридических условий. |
| U31 | §5/7.4 | 8 ширин320–1920 ×2темы, bounds | COMPLETE | tests/browser_qa.py:WIDTHS/matrix; production proof39125369226 | Current main layout прошёл16 cases; дополнительно проверить изменённый draft, не опираться только на старый PASS. |
| U32 | §4.1/6 | No-JS mobile navigation не перекрывает контент | COMPLETE | styles/site.css:@media800 .nav; index.html:header | No-JS nav в потоке; absolute только data-collapsed после JS init; ни hero, ни headings не перекрыты. |
| U33 | §4.1/5 | Tab order при открытии mobile menu | COMPLETE | scripts/site.js:setMenu; index.html:nav before trigger | Keyboard open фокусирует first link; relatedTarget устраняет преждевременное закрытие при Tab. |
| U34 | §4.1/5 | Закрытие меню и focus после выбора/resize | COMPLETE | scripts/site.js:nav click/mobile change | Выбор фокусирует target; Escape/hidden focus на resize возвращают toggle; targeted regressions PASS. |
| U35 | §5 | Visible focus и skip link | COMPLETE | styles/site.css::focus-visible/.skip; index.html:main tabindex | Skip переносит фокус main; outline видим в обеих темах. |
| U36 | §5 | Hover/active/feedback где применимо | COMPLETE | styles/site.css:.button/.icon-button/.nav/summary | Primary active transform/hover, native FAQ expanded и theme labels; декоративным панелям не нужен искусственный hover. |
| U37 | §4.6/5 | Недоступные действия не вводят в заблуждение | COMPLETE | tools/build.py:pending_release; styles/site.css:button:disabled | Вместо ложного download доступно release-info; disabled helper не выдаётся за реально работающий APK. |
| U38 | §5 | Умеренное движение/reduced-motion | COMPLETE | styles/site.css:@media reduced-motion; scripts/site.js:scrollBy | Нет autoplay/video, reduced motion отключает transition/scroll animation. |
| U39 | §5/7.7 | WCAG AA contrast/targets | COMPLETE | styles/site.css:tokens/buttons; docs/QA.md:axe | Palette/48px icon/52px CTA/native summary; свежий axe/bounds после fixes обязателен, не утверждать manual WCAG conformance. |
| U40 | §5 | Семантика/alt/headings/ARIA | COMPLETE | index.html:main/sections/dialog; tools/build.py:faq/gallery | Landmarks, h1/h2, meaningful alt и native controls. Это structural evidence, не реальный screen-reader session. |
| U41 | §5/7.4 | 200% text/spacing/reflow | COMPLETE | tests/accessibility_qa.py; privacy.html:style | Main12 adaptation cases и privacy12 CSS text/spacing cases PASS; это не native zoom. |
| U42 | §5/6 | Настоящий screen reader/native zoom | REQUIRES_MANUAL_VERIFICATION | docs/QA.md:limitations | Нет AT/operator integration; DOM snapshot/CSS text simulation не являются screen reader/native zoom. |
| U43 | §6/7.5 | Physical Android/iOS Safari/native WebKit swipe | REQUIRES_MANUAL_VERIFICATION | docs/QA.md:4B/4C/production | Engine emulation/desktop Edge не заменяют physical devices/Safari app. |
| U44 | §5/7.8 | Иерархия, whitespace, readability | COMPLETE | styles/site.css:hero/section/panel/faq; screenshots/uiux | Осмотр mobile/desktop обеих тем; общий принятый визуальный строй сохраняется. Новая художественная концепция не требуется. |

## Зафиксированный gap analysis (история до исправлений, текущие статусы выше)

| ID / ТЗ | Текущая реализация и точный недостаток | Влияние на пользователя | Коррекция | Без APK? | Критерий проверки |
|---|---|---|---|---|---|
| U11 §5 | System theme только JS, CSS fallback отсутствует | При отключённом JS dark preference игнорируется | Те же Android dark tokens/wordmarks в prefers-color-scheme fallback | Да | JS disabled/light иdark → соответствующие computed colors и logo, без overflow |
| U12 §4.8/5 | Legacy privacy light/purple и long heading overflow397px при320px | Горизонтальный скролл, разрыв единой темы | Reuse существующих fonts/colors/theme control; responsive wrapping; все legal paragraphs/date/links сохранить | Да, меняется только UI вdevelopment |320–1920 обе темы, no overflow, legal text/links byte-equivalent после HTML normalization; before/after |
| U14 §4.1/2/6 | Info CTA вместо реального download | APK недоступен, честно показано | Подключить approved HTTPS artifact через release config | Нет | Actual artifact download/hash/version + owner approval; пока ссылок0 |
| U15 §4.2 | Hero без phone screenshot | Нет ознакомления с реальным UI релиза | Добавить approved release screen в существующий phone frame | Нет | Screenshot относится к APK, обе темы, правильные размеры/alt |
| U17 §4.3 | Карточки без публичных функций | Полезность не раскрыта до релиза | Проверить каждую функцию и заполнить existing config | Нет | Per-feature version/evidence, нет dev-only claims |
| U19 §4.4 | Только честный gallery placeholder | Нельзя посмотреть приложение | Approved sanitized screens обеих тем, existing gallery | Нет | Source/version/evidence/consent + controls/focus/errors QA |
| U22 §5 | Gallery show меняет src без loading status | Медленная загрузка выглядит как отсутствие реакции | Accessible loading status, hide stale image, recover load/error/retry | Да, test-only fixture | Delayed response показывает status; load/error/cancel/next clears state, Escape/focus сохраняются |
| U25 §4.6/7.3 | Нет разрешённого APK | Невозможно установить приложение с сайта | Owner-approved artifact, проверка signing/manifest/HTTPS/SHA | Нет | Фактические file bytes/metadata совпадают, gates проходят |
| U26 §4.6 | Release fields null | Нет версии/совместимости/size/checksum | Заполнить только фактические данные выбранного APK | Нет | Render/source values и скачанный файл совпадают |
| U28 §4.7 | Release-specific FAQ намеренно осторожные | Нет гарантий sync/backup/update | Уточнить по verified release evidence | Нет | Документированный источник каждого обещания |
| U32 §4.1/6 | No-JS mobile nav absolute и overlaps h1 | Заголовок закрыт меню | Inline flow fallback; absolute только для JS disclosure | Да | JS disabled320/390/768, navigation.bottom≤hero.top, ссылки/FAQ работают |
| U33 §4.1/5 | Nav DOM before toggle, open не переносит focus | Keyboard Tab пропускает меню | При открытии focus первой ссылки, корректный close/restore | Да | Enter/Space open → first nav; Tab traverses links, Escape returns toggle |
| U34 §4.1/5 | Link/resize закрывают focused nav без destination | Keyboard focus теряется/становится невидимым | Focus выбранной section и toggle при скрывающем resize | Да | anchor target focus + bounds; resize с focused nav не оставляет hidden focus |
| U41 §5/7.4 | Main text QA есть, privacy long word overflow | Text zoom на правовой странице неудобен | Wrapping и common typography, reflow main/privacy | Да | 200% text/CSS spacing both pages320/390/1440; native zoom отдельно |
| U42 §5/6 | AT/native zoom не запускались | Реальный speech/zoom UX ещё не доказан | Ручная проверка screen reader/native zoom с оператором | Не зависит от APK, недоступна интеграция | Реальный AT/device session record, не DOM mock |
| U43 §6/7.5 | Только desktop engines/emulated touch | Physical Safari/Android/iOS поведение не подтверждено | Проверка на реальных устройствах и Safari app | Не зависит от APK, нужны устройства | OS/browser versions, keyboard/touch/swipe/themes/zoom screenshots |

## Что не является обязательным исправлением

Новая художественная hero-концепция, новые позы котика, feature illustrations без approved release, дополнительная анимация и декоративный hover у статичных панелей — optional redesign/неподтверждённый контент. Не реализовывать их как якобы gaps ТЗ. Категории галереи нужны только при реальном наборе screens. Native details/summary уже обеспечивает disclosure semantics; не заменять его custom accordion ради DOM attrs. Device/AT проверку не подменять новым автоматическим PASS.

## Порядок выполнения в текущем roadmap

U1: no-JS/keyboard navigation + shared privacy theme/reflow + system CSS fallback (U11/U12/U32/U33/U34/U41). U2: gallery loading/error/retry (U22). Source audit/current Android comparison завершены. После каждого этапа focused QA + current matrix/axe/screenshots, commit/push/remote/Telegram; production не менять. APK-dependent/manual остаток перечислен выше, всего мастер-ТЗ не закрывать.


## U1 · доказательства исправления

Навигация/focus/no-JS и privacy themes/reflow исправлены без APK. Все legal headings/paragraphs/date/links сохранены, normalized content SHA в uiux-before/uiux-u1. Main layout/visual direction прежние; правовая страница использует тот же Android Onest и palette, без переписывания политики. [Current proof](verification/uiux-u1.json): main16 иprivacy16 cases; main4 иprivacy4axe0violations; main12 +privacy12 text adaptation;6 no-JS cases; keyboard open/Tab/Escape/select/resize; persistence main/privacy PASS. Before/post визуально осмотрены, включая readability long heading на320. [Privacy after](screenshots/uiux/after-u1-privacy-320-light.png), [dark](screenshots/uiux/after-u1-privacy-320-dark.png), [no-JS after](screenshots/uiux/after-u1-nojs-320-light.png), [desktop](screenshots/uiux/after-u1-1440-dark.png). На U1 U22 ещё не был завершён; итог U2 приведён ниже. Исторический release-candidate.json не перезаписан: CI сверяет новую development preview по current-preview.json; production evidence и artifact остаются отдельно неизменными.


## U2 · итог завершения независимо доступных UI требований

[Полное доказательство](verification/uiux-u2.json):64 main +64 privacy viewport/theme cases,24 no-JS cases; main16 +privacy16 +gallery16 axe runs (всего48,0violations). Main12 иprivacy48 CSS text/spacing cases; keyboard nav/select/resize и shared themes проверены в4 engines. Это не native zoom/AT/device verification. Матрицы относятся к текущему видимому HTML/CSS; после последней малой защиты queued close от rapid reopen отдельно повторены gallery states в4 browsers. Generic gallery QA использует явно оригинальные mascot fixtures, без публичных Android screens.

U22: доступный loading status, aria-busy, отсутствие stale image; успех/ошибка/повторный выбор/закрытие/rapid reopen не оставляют неверное состояние. Native close event асинхронен: тест ждёт фактическое semantic состояние, не утверждает синхронный callback. [Before](screenshots/uiux/before-loading-390-light.png), [after](screenshots/uiux/after-loading-390-light.png), [dark error](screenshots/uiux/after-error-390-dark.png). Скриншоты осмотрены; новую художественную концепцию не добавляли.

Итог:35 COMPLETE,0 PARTIAL,0 MISSING,7 BLOCKED_BY_RELEASE_CONTENT,2 REQUIRES_MANUAL_VERIFICATION (44 atomic UI items). Исторический baseline до fixes:28/6/1/7/2. Нельзя интерпретировать35 как completion всего master: реальные features/screens/APK и physical/AT проверки остаются открыты. Нужны owner-approved APK +sanitized screens обеих тем; отдельно manual device/Safari/AT/native zoom session. Вопросы release-specific FAQ относятся к подтверждению поведения APK. Повторно просить уже выданное разрешение первого coming-soon release не требуется; выпуск новых UI fixes требует нового решения, production не менялся.


## Удалённое подтверждение

[U1 commit](https://github.com/sashaermin/ya-hudeyu/commit/2981a4578f7514d9d14cc08c4fcc033aaa06e816), [U2 commit](https://github.com/sashaermin/ya-hudeyu/commit/6798295a2d39ded17f0465348601f2793c1eb615): remote проверены, оба CI success. Последний run39127437892:78 active unit tests и реальный stored archive22files/4render views/noindex/noAPK PASS. Exact notices в uiux-u2.json. [Review ZIP](https://github.com/sashaermin/ya-hudeyu/actions/runs/39127437892/artifacts/12135589715) хранится7дней, не является размещённым preview. Для распаковки/локального просмотра — docs/FIRST_RELEASE.md; production9b39ffa не содержит этих изменений и не трогался.


## U3 · публикация по отдельному разрешению владельца

После завершённого audit владелец отдельно разрешил выпуск именно этих fixes. Они опубликованы8fb7bf2 (approved source0b706e3), Pages39129023427 иnormal-TLS live39129135130 success:22file hashes/16internal404,main16+privacy16 layouts/noJS6/focus/gallery2themes/12axe0violations. [Production proof](verification/uiux-production-release.json). Классификация44UI требований не изменена:35complete/7releaseblocked/2manual; новые непроверенные claims/screens/APK не добавлены. Фразы онеизменённом production выше относятся кпериоду аудита до отдельной авторизации U3. Rollback9b39ffa сохранён; будущие production updates требуют нового owner решения.

## Phase2 development enrichment (отдельная owner authorization)

Новый coming-soon development candidate добавляет5 source-backed **planned** directions, journey, original mascot hint, status/FAQ — docs/PHASE2_REVIEW.md. Это не released features и не Android screenshots; U14/U15/U17/U19/U25/U26/U28 остаются BLOCKED_BY_RELEASE_CONTENT, U42/U43 manual. Исходные44 статуса не подменяются Phase2 layout tests. Матрица нового кандидата48cases/12axe0violations/6noJS/12text adaptation, evidence phase2-review.json; production не меняется. Owner visual/content review pending.
