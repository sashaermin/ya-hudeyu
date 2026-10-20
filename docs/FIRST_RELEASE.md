# Первый инкрементальный релиз сайта

Основание: уточнение владельца 18.10.2026 — подготовить редизайн и основные секции отдельно от отложенной интеграции APK. Это процедура приёмки и будущей публикации, не новое ТЗ и не разрешение выполнять deploy.

## Первый опубликованный coming-soon release

Главная с оригинальным Android-брендом/котиком/шрифтами, обе темы, адаптивная навигация, секции знакомства, будущей галереи, установки, FAQ, поддержка и неизменённая `/privacy.html`. Состояние загрузки — «Скоро для Android», без даты, версии, активного download и неподтверждённых функций. Отсутствие APK не блокирует подготовку и приёмку этого website-кандидата. Полные features/screens/download — следующий инкремент по мастер-ТЗ.

Кандидат всегда собирается как draft с noindex и robots Disallow. `python3 tools/package_preview.py` создаёт свежую allowlisted сборку во временной папке и детерминированный ZIP с manifest/SHA-256. В архиве только сайт, без внутренних docs/config/tests/секретов. Manifest указывает Git commit и наличие uncommitted source: локальный dirty candidate не выдаётся за точное содержимое remote. GitHub Actions собирает архив из чистого checkout после проверок и сохраняет на7дней. Это Actions artifact для просмотра, не Pages deployment и не размещённый preview-сайт.

## Как посмотреть

Открыть действующий сайт: **https://yahudeyu-app.ru/**. Текущий UI/UX release —8fb7bf2, Pages39129023427/live39129135130 success; ниже сохранена история первого release9b39ffa. Published commit `9b39ffaf35c48973b8115b630ba0d06165ad09a4`, Pages run39114713056 success; live browser run39125147955 PASS. Это актуальный способ просмотра; прежние archive/screenshot ссылки ниже сохранены как evidence приёмки. Noindex намеренно сохранён; APK недоступен.

Самый простой визуальный просмотр без установки: открыть [главную на компьютере — светлая тема](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-1440-light.png), [тёмная тема](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-1440-dark.png), [мобильная — светлая](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-390-light.png) и [тёмная](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-390-dark.png). Это сохранённые снимки кандидата, не интерактивный сайт. После policy patch draft HTML побайтно совпадает с этим визуальным baseline.

Для проверки взаимодействий: [свежий проверенный архив кандидата](https://github.com/sashaermin/ya-hudeyu/actions/runs/39114231216/artifacts/12131711410), source `70527d0e676c3b5dbc497082668af6db9d7cfb33`, run39114231216. CI реально скачал его и открыл390/1440px ×2темы:22files, noindex=true, APK=false, ошибок0. Inner ZIP SHA-256 `7877e610d11a5a3d84b708864e0b5eae7c6c1b2ab263daeb77f7fc0cdd23c6e5`. Архив хранится7дней; для запуска используйте следующие шаги.

1. Открыть последний успешный «САЙТ — проверки и Telegram» для нужного SHA в [Actions](https://github.com/sashaermin/ya-hudeyu/actions/workflows/website-checks.yml).
2. Скачать artifact `website-preview-<полный SHA>-attempt-<номер попытки>` (GitHub может требовать вход). Сверить ZIP с SHA-256 в соседнем manifest; manifest `source_commit` должен совпасть с проверенным SHA, `source_worktree_dirty` — false.
3. Распаковать внутренний `website-preview.zip` в отдельную локальную папку и запустить `python3 -m http.server 8002 --bind 127.0.0.1 --directory <эта папка>`.
4. Открыть `http://127.0.0.1:8002/`. Проверить светлую/тёмную тему, mobile menu/FAQ, поддержку, privacy и «Скоро». Это loopback на компьютере, где запущен сервер; ссылка облачного localhost не доступна владельцу извне.

Инструмента безопасного внешнего изолированного preview-hosting в текущей среде нет. Не создавать публичный tunnel, сторонний hosting или Pages deployment, не менять DNS/CNAME под видом preview. Скриншоты кандидата и проверенные результаты — docs/QA.md и docs/verification/release-candidate.json (QA выполнен).

## Текущее разрешение первого выпуска

Владелец принял кандидат b12b0b0 и явно разрешил первый production release по существующему Pages main:/ и rollback при неуспехе. Область сохранена в [авторизации](../project_specs/FIRST_WEBSITE_RELEASE_AUTHORIZATION_2026-10-18.md). data/publication.json: approved=true, release_mode=coming-soon; APK остаётся unverified/approved_for_distribution=false. Реальный production build проходит согласованные gates без APK и запрещает features/screens/verified APK.

Индексирование не требуется для serving, отдельного безусловного разрешения нет: indexing_approved=false сохраняет noindex/nofollow и robots Disallow даже в валидированной production-сборке. Draft по-прежнему noindex независимо от настроек. Это не обход gate загрузкой draft; production build выполнен с --production и действительным approval_reference. Изменение indexing и любые следующие релизы требуют отдельного решения; digest/main workflow не входит в разрешение.

### История policy diff

[Исходный patch](proposals/first-release-coming-soon.patch) SHA-256 cefd3cc1b1440efa0f09c67b557570e5c9a4f89d0b7f0c63df7b8b407f38fd03 был разрешён и применён в70527d0; теперь активные5 policy tests и2 дополнительных indexing tests проверяют approved coming-soon gate. Не применять proposal повторно.

## Подготовленная безопасная процедура публикации

До авторизации — только чтение и локальные проверки. После соответствующих отдельных разрешений:

1. Fetch/status, единственный писатель, подтвердить разрешённый SHA и archive digest, визуальную/юридическую приёмку и необходимые device checks. Перепроверить уже применённую согласованную gate-политику; переутвердить артефакт при изменении сайта.
2. Сохранить SHA действующего production (`9a0857ce260540ad604f344565d535a8d47b2fa0` при последней проверке; перед выпуском получить заново), копию текущих публичных файлов, Pages source/deployment и контрольные суммы privacy/CNAME. Без токенов/секретов в backup.
3. Pages фактически использует legacy `main:/`. Рабочая ветка содержит шаблон и внутренние документы, поэтому её merge/root publish непригоден. Подготовить для review отдельный commit **только allowlisted собранных публичных файлов** под этот механизм. Не менять DNS/CNAME/source; любые иные изменения deployment согласовать отдельно. Никаких docs/project_specs/data в опубликованном корне.
4. Предъявить точный diff, digest и rollback; только затем выполнить явно разрешённый update main. Сам update может запустить legacy Pages build. Не создавать PR/merge/коммит main/deploy на основании одного разрешения разработки.
5. Проверить действительный Pages run/deployment, HTTPS, новый rendered title/brand, обе темы, ресурсы, `/privacy.html`, отсутствие APK и внутренних файлов. Canonical/robots/noindex должны соответствовать отдельному решению об индексировании. Сохранить доказательства; Telegram сообщать успех только по факту.

## План отката

В разрешении выпуска заранее согласовать rollback именно этого публикационного commit. При проблеме сохранить evidence, выполнить разрешённый revert публикационного commit (без reset/force-push/переписывания истории), дождаться legacy Pages build, сравнить главную/privacy с сохранённой production-копией, проверить HTTPS/CNAME и отсутствие побочного APK/deploy. Если rollback отдельно не разрешён — подготовить конкретный revert для решения владельца. Android/другие клиентские репозитории не затрагивать.

## Проверка сохранённого архива

После upload в verify job тот же workflow скачивает artifact через pinned download-artifact (теперьv8.0.2/Node24). `tests/review_artifact_qa.py` требует совпадения source SHA/clean tree/ZIP SHA с утверждаемым candidate digest, проверяет manifest каждого файла, распаковывает безопасные пути во временную папку и реально открывает этот архив в Chrome на loopback:390/1440px ×2темы, coming-soon/noindex/no download/menu/FAQ/privacy/resources. Успех создаёт notice `Website review archive verified` и отдельный verification artifact. Это реальный round-trip, не повторный render из checkout. Для ручного запуска на скачанном ZIP: `python3 tests/review_artifact_qa.py <archive.zip> --checkpoint <SHA> --executable <Chrome path>`.

Из cloud прямое скачивание artifact12130660202 получило403 на storage host. Дополнительный домен сохранён в черновике среды (не активирован); при необходимости прямого cloud download надо сохранить настройки и опубликовать **среду**, не сайт. Альтернативный CI round-trip не требует этого действия. Статус и доказательства — docs/verification/review-artifact-status.json. Ни локальная rehearsal, ни наличие artifact сами по себе не доказывают успешного remote download/render.

Имена новых artifacts включают `run_attempt`, чтобы попытка была явно видна; upload/download используют одно имя. Реальный retry прошёл, но preservation прежних artifact IDs **не подтверждён**: после rerun API возвращает404 для attempt1 IDs. Ссылки на artifacts не вечные, retention7дней; при необходимости восстановить кандидат из source и сверить известный inner ZIP SHA. Исторические artifacts доR4 имеют прежнее имя без suffix.

R4 [retry evidence](verification/artifact-retry.json): обе попытки successful, round-trip/render прошёл повторно, commit Telegram127 принят вattempt1 и не повторён вattempt2. Исходная гипотеза о name collision не выдаётся за воспроизведённый дефект; фактически доказаны успешный retry и явная attempt provenance. Обещание сохранности старых IDs снято по результату проверки.

Последняя verified review ссылка и digest: [Node24 proof](verification/artifact-node24.json), artifact12131711410/source70527d0. GitHub artifacts ограничены retention и rerun lifecycle, при их недоступности сверяйте восстановленный inner ZIP с зафиксированным SHA. Текущие76 unit tests прошли в CI R6; историческое число58 относится к R5;20 policy proposal tests — историческая изолированная проверка до применения diff.


## Завершение production verification

Actual Pages/HTTPS/22 public hashes/12 internal404/live16 browser cases подтверждены в docs/verification/first-production-release.json и production-http.json. Rollback tag rollback/website-first-release-2026-10-18 указывает на9a0857c. Cloud Chromium упёрся в proxy CA trust; persistent import отклонён automatic approval review и не выполнен. Безопасная проверка сделана на GitHub runner со штатным TLS trust, не отключая сертификаты. Для повторного read-only CI QA при реальной необходимости добавить Verify-Live-Production: true в final commit trailer block; это не разрешение и не запуск deployment. Полный master остаётся частично открытым, см. IMPLEMENTATION_PROGRESS.md.


Production Lighthouse verified в run39125369226: mobile99/100/100/69; первые3 targets достигнуты, SEO69 вызван сохранённым noindex. [Actual evidence](verification/production-lighthouse.json). Это один lab run, не physical-device/real-user метрика. Новых production defects не найдено; ничего повторно не deploy. Первое website-owner действие resolved, APK/download и manual/device требования полного master остаются отдельно открыты.


## Авторизованный UI/UX update U3

Новый конкретный scope — [разрешение владельца](../project_specs/UIUX_PRODUCTION_AUTHORIZATION_2026-10-18.md): publish audited UI from0b706e3, без дополнительного подтверждения. [Manifest](verification/uiux-production-release.json), [rollback](verification/uiux-production-rollback.json); прежняя first-release evidence неизменна. Prepared public-only main commit8fb7bf2 меняет4paths, текущий rollback9b39ffa. Production build сновым approval_reference равен audited ZIP995ef47b; noindex/coming-soon/APK disabled/legal text сохранены. Это не merge dev branch и не изменение deployment configuration. Readiness CI обязателен до main push; расширенный normal-TLS live QA после completed Pages. Только confirmed critical regression допускает согласованный revert к9b39ffa (новый commit с parent=публикационный SHA/tree=rollback tree, без reset/force-push); после revert проверить Pages/HTTPS/hashes изаписать failure evidence. Старый rollback9a0857c не удалять.

U3 actual deployment: published8fb7bf2920a89f39e1ed3a56d53ada91f468b715, Pages39129023427 success, initial HTTPS hash/config PASS. Расширенная UI/privacy/gallery/a11y live verification pending; готовность не подменять одним deploy success. Никакого дополнительного main push/deploy для CI verification не требуется.


## U3 · опубликованный UI/UX release verified

Production SHA `8fb7bf2920a89f39e1ed3a56d53ada91f468b715`, approved source0b706e3, actual public-only4file update/22file manifest, audited archive995ef47b. Pages39129023427 success, live39129135130 success сnormal TLS. Все22 public bytes совпали;16 internal paths404, main16+privacy16/320px layouts,6noJS/focus/legal body/gallery2themes и12axe0violations PASS. Gallery проверена browser-local fixtures сdeployedJS, не публичными Android screenshots. Lighthouse99/100/100/69, SEO изсохранённого noindex. [Exact release proof](verification/uiux-production-release.json), [rollback proof](verification/uiux-production-rollback.json).

Rollback current: `9b39ffaf35c48973b8115b630ba0d06165ad09a4`, tag `rollback/website-uiux-release-2026-10-18`; previousfirst rollback9a0857c не удалён. При confirmed critical regression этого U3 использовать согласованный revert к9b39ffa, затем Pages/HTTPS/hash/UI verification. Откат не понадобился. Main/Pages/DNS/CNAME/HTTPS конфигурацию не меняли; legal text/noindex/APK disabled сохранены. Разрешение U3 не даёт права новых releases; не делать повторный deployment после успешной проверки.

## P4 · Phase2 + FAQ + unavailable download: опубликовано20.10.2026

[Новая узкая авторизация](../project_specs/PHASE2_FAQ_BETA_PRODUCTION_AUTHORIZATION_2026-10-20.md) исполнена: production `6810206125ccf72080c8a7aa29072041d5812f0f`,parent/rollback `f308729f2cd4d7bde3574e08d8fd2fc05e92c4ab`. Только4publicpaths:index,styles,originalhintmascot,download/index;не wholesale merge. Existing Pages/config/.github/legal/privacy/CNAME/noindex/APK-off сохранены. Все24productionfiles равны текущемуreviewZIPed78f72;отпервоначальногоapprovedd48f2d5 отличается только4пробелаemptyHTMLline,безизменениясодержания/вида.

Pages39330940936 success;actual HTTPS/browser39331146457 success:24hashes/25private404/64layouts/20axe0violations,FAQ33/8 и/download unavailable,light/dark/mobile/keyboard/noJS/privacy/gallery. Lighthouse98/100/100/69,SEOизintentionalnoindex. [Release evidence](verification/phase2-faq-beta-production-release.json),[durable live results](verification/phase2-release-live/production.json),[live screenshot mobile light](screenshots/phase2-release/download-390-light.png),[desktop dark](screenshots/phase2-release/download-1440-dark.png). Gallery fixtures были толькоbrowser-local,неpublicscreens.

[Rollback evidence](verification/phase2-faq-beta-rollback.json):remote tag`rollback/website-phase2-faq-beta-2026-10-20` указывает наf308729f,включаясогласованнуюTelegramинфраструктуру. Приconfirmed critical regression этогоP4 разрешён новый rollback commit сtree=f308729f,parent=актуальныйproductioncommit,fast-forward push безforce/reset;затемдождатьсяPages,сверить22старыхHTTPShashes,privacy/CNAME/robots/старуюUIи/download404. СтарыеUI/first-release tags сохраняются. Rollback неиспользовался.

Текущий website release завершён, новыхдействийвладельца длянего нет. APKdistribution/реальная betaavailable не разрешены;approval APK остаётсяотдельноOPEN. Эторазрешениеодноразовое:новыеmain/deploy/indexing/APKрешения требуютновойявнойавторизации. Новыхизмененийсайтаилиповторногодеплоянепланировать.

## G2 · разрешённый выпуск предварительной Android-галереи

Авторизация: `project_specs/ANDROID_PREVIEW_PRODUCTION_AUTHORIZATION_2026-10-20.md`, source `c3d8d9f6a659c7e698049af8f27cd50a00b54937`. Exact gallery config fingerprint: `33718228f5f81036c1d735d8782a009d7b1a8ec2efa56c2305e8be89fb95052d`. Existing gallery gate активирован только для этого manifest; APK/beta false,noindex preserved. Инойmanifest требует новогоownerapproval. Имущественные изображения не заменялись:22WebP hashes равныreview;privacyreview11/11,0targetedOCRmatches,metadata absent.

Manifest: `verification/android-preview-production-release.json`; rollback: `verification/android-preview-production-rollback.json`. Production build содержит46publicfiles иравен reviewedZIPfaa3c3e по каждому fileSHA. Minimal main update меняет25paths:index.html,styles/site.css,scripts/site.js и22assets/previews/*.webp. Download/privacy/CNAME/robots/fonts/brand ивесь.github subtree сохранены. Prepared commit строится через отдельный temporary Git index:read-tree oldmain,hash-object/update-index только manifest changed_public_paths,write-tree,commit-tree сparent=oldmain;текущаяdevbranch иsharedindex не переключаются. Commit/tree/hash-diff задокументированы вmanifest. Пока readiness CI неуспешен,main не пушить.

Rollback checkpoint6810206125ccf72080c8a7aa29072041d5812f0f,remote tag`rollback/website-android-preview-2026-10-20`. До выпуска24HTTPS hashes сверены со старымrelease. Приconfirmed critical privacy/security/functionality regression:новыйcommit сparent=currentmain/tree=6810206,fast-forwardpush безforce/reset,дождатьсяPages,проверить24oldhashes/preview404/noindex/APKoff. Не менять инфраструктуру.

После успешного readiness:повторно сверить main/dev refs иPagesconfig,проверить exact25path diff и46public hashes изpreparedcommit,пушить только productionSHA:main черезexisting legacyPages. Дождатьсяactualdeployment. Existing read-only live verifier направлен наG2manifest:46HTTPS hashes,private404,main/privacy/FAQ/download regression иactual gallery16layouts/8axe/8noJS/176opens/CDPswipes. TLS verification сохранять;cloud certificate trust не обходить,проверять наexistingGitHub runner. Verify-Live-Production:true вdevcommit запускает толькоreadonly QA,не deployment. После успеха записать Pages/live/Telegram proof иSTOP;никакого повторногоdeploy неизменного сайта.

G2 исполнен и **VERIFIED**:productiond7ebfd8e6576e2c1fc286e9c46c6a8ea4a9060ac,Pages39339379755/live39339685332 success.46HTTPS hashes/35private404,80layouts/28axe0violations,actual11-imagegallery/swipes/themes/focus/noJS иFAQ33/download/privacy PASS. MobileLH98/100/100/69;SEOизintentionalnoindex. [Actualreleaseevidence](verification/android-preview-production-release.json),[livecheckannotations/metrics](verification/android-preview-production-live.json). Rollback6810206/tagwebsite-android-preview-2026-10-20 verified,неиспользован. Одноразоваяавторизацияисчерпана;неисполнятьподготовительныеpublishstepsэтогоразделаповторно. Последующиеreleasesтребуютновогоразрешения;APK/beta/indexingнеразрешены.
