# Первый инкрементальный релиз сайта

Основание: уточнение владельца 18.10.2026 — подготовить редизайн и основные секции отдельно от отложенной интеграции APK. Это процедура приёмки и будущей публикации, не новое ТЗ и не разрешение выполнять deploy.

## Подготовленный кандидат

Главная с оригинальным Android-брендом/котиком/шрифтами, обе темы, адаптивная навигация, секции знакомства, будущей галереи, установки, FAQ, поддержка и неизменённая `/privacy.html`. Состояние загрузки — «Скоро для Android», без даты, версии, активного download и неподтверждённых функций. Отсутствие APK не блокирует подготовку и приёмку этого website-кандидата. Полные features/screens/download — следующий инкремент по мастер-ТЗ.

Кандидат всегда собирается как draft с noindex и robots Disallow. `python3 tools/package_preview.py` создаёт свежую allowlisted сборку во временной папке и детерминированный ZIP с manifest/SHA-256. В архиве только сайт, без внутренних docs/config/tests/секретов. Manifest указывает Git commit и наличие uncommitted source: локальный dirty candidate не выдаётся за точное содержимое remote. GitHub Actions собирает архив из чистого checkout после проверок и сохраняет на7дней. Это Actions artifact для просмотра, не Pages deployment и не размещённый preview-сайт.

## Как посмотреть

Самый простой визуальный просмотр без установки: открыть [главную на компьютере — светлая тема](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-1440-light.png), [тёмная тема](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-1440-dark.png), [мобильная — светлая](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-390-light.png) и [тёмная](https://github.com/sashaermin/ya-hudeyu/blob/70527d0e676c3b5dbc497082668af6db9d7cfb33/docs/screenshots/rc-390-dark.png). Это сохранённые снимки кандидата, не интерактивный сайт. После policy patch draft HTML побайтно совпадает с этим визуальным baseline.

Для проверки взаимодействий: [свежий проверенный архив кандидата](https://github.com/sashaermin/ya-hudeyu/actions/runs/39114231216/artifacts/12131711410), source `70527d0e676c3b5dbc497082668af6db9d7cfb33`, run39114231216. CI реально скачал его и открыл390/1440px ×2темы:22files, noindex=true, APK=false, ошибок0. Inner ZIP SHA-256 `7877e610d11a5a3d84b708864e0b5eae7c6c1b2ab263daeb77f7fc0cdd23c6e5`. Архив хранится7дней; для запуска используйте следующие шаги.

1. Открыть последний успешный «САЙТ — проверки и Telegram» для нужного SHA в [Actions](https://github.com/sashaermin/ya-hudeyu/actions/workflows/website-checks.yml).
2. Скачать artifact `website-preview-<полный SHA>-attempt-<номер попытки>` (GitHub может требовать вход). Сверить ZIP с SHA-256 в соседнем manifest; manifest `source_commit` должен совпасть с проверенным SHA, `source_worktree_dirty` — false.
3. Распаковать внутренний `website-preview.zip` в отдельную локальную папку и запустить `python3 -m http.server 8002 --bind 127.0.0.1 --directory <эта папка>`.
4. Открыть `http://127.0.0.1:8002/`. Проверить светлую/тёмную тему, mobile menu/FAQ, поддержку, privacy и «Скоро». Это loopback на компьютере, где запущен сервер; ссылка облачного localhost не доступна владельцу извне.

Инструмента безопасного внешнего изолированного preview-hosting в текущей среде нет. Не создавать публичный tunnel, сторонний hosting или Pages deployment, не менять DNS/CNAME под видом preview. Скриншоты кандидата и проверенные результаты — docs/QA.md и docs/verification/release-candidate.json (QA выполнен).

## Что требует отдельного решения владельца

**Текущее разрешение — подготовка, без публикации.** Реальные data/publication.json=false и data/release.json=unverified остаются неизменными. Существующий `--production` всё ещё требует APK/features/screens и отдельное разрешение сайта. Его обход через загрузку draft не является допустимой процедурой.

Для первого релиза без APK владелец отдельно разрешил применение конкретного [diff](proposals/first-release-coming-soon.patch), SHA-256 `cefd3cc1b1440efa0f09c67b557570e5c9a4f89d0b7f0c63df7b8b407f38fd03`. Он применён без изменений после проверки совместимости с remote8a0e726. Builder поддерживает явный `release_mode: coming-soon` с отдельным site approval, запрещая APK/features/screens; default full-release gates сохранены. Реальный config не переключён: approved=false, release_mode отсутствует (default full). Draft всегда noindex. Это авторизация только реализации политики, не выпуска и не снятия noindex. 25 site/build/workflow/handoff tests PASS; исходный proposal содержит историческое REVIEW-ONLY описание тестов, теперь активированных по разрешению. APK не нужен для приёмки текущего кандидата.

После приёмки кандидата требуются: визуальное/юридическое подтверждение, явное разрешение публикации конкретного website-SHA/артефакта и согласованного способа Pages. Разрешение также должно определить индексирование и право отката; нельзя молча снимать noindex. Отдельный digest-main workflow не включён в такое разрешение автоматически.

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

## Предмет разрешения: неприменённый policy diff

[Точный patch](proposals/first-release-coming-soon.patch), [проверки](verification/first-release-policy-proposal.json). SHA-256 patch указан в evidence. Активный tools/build.py и реальные approval-файлы **не изменены**. Patch проверен через git apply --check и применение только во временном git archive экспорте:15 существующих build tests +5 новых proposed policy tests PASS.

Предлагаемое поведение: default mode `full` сохраняет существующие APK/features/screens gates. Только явно выбранный `publication.release_mode=coming-soon` вместе с настоящим отдельным site approval и непустой approval_reference допускает первый production-кандидат без APK. В этом режиме запрещены verified APK, функции и скриншоты; неизвестные modes отклоняются. Draft всегда noindex. Реальные mode/approval не выставлены, индексирование/публикация/main этим review не разрешаются.

Предмет ближайшего решения владельца — **разрешить применение именно этого patch**, либо дать замечания. Это не разрешение main/deploy/APK/снятия noindex в текущем draft. После применения и проверок публикация конкретного SHA/артефакта согласуется отдельно.

Воспроизведение proposal tests: экспортировать текущий Git checkpoint во временную папку, применить patch там через `git apply --no-index --check` и `git apply --no-index`, выполнить `python3 -m unittest discover -s tests -p test_build.py -v` и `python3 -m unittest discover -s tests -p test_coming_soon_policy.py -v`. Не применять patch к активной ветке без указанной авторизации. TEST ONLY approvals существуют лишь в isolated test fixtures.

Имена новых artifacts включают `run_attempt`, чтобы попытка была явно видна; upload/download используют одно имя. Реальный retry прошёл, но preservation прежних artifact IDs **не подтверждён**: после rerun API возвращает404 для attempt1 IDs. Ссылки на artifacts не вечные, retention7дней; при необходимости восстановить кандидат из source и сверить известный inner ZIP SHA. Исторические artifacts доR4 имеют прежнее имя без suffix.

R4 [retry evidence](verification/artifact-retry.json): обе попытки successful, round-trip/render прошёл повторно, commit Telegram127 принят вattempt1 и не повторён вattempt2. Исходная гипотеза о name collision не выдаётся за воспроизведённый дефект; фактически доказаны успешный retry и явная attempt provenance. Обещание сохранности старых IDs снято по результату проверки.

Последняя verified review ссылка и digest: [Node24 proof](verification/artifact-node24.json), artifact12131711410/source70527d0. GitHub artifacts ограничены retention и rerun lifecycle, при их недоступности сверяйте восстановленный inner ZIP с зафиксированным SHA. Текущие76 unit tests прошли в CI R6; историческое число58 относится к R5;20 policy proposal tests — отдельная изолированная проверка неприменённого diff.
