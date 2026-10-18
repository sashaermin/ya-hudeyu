# «Я ХУдЕЮ» — общий handoff сайта

## Текущее состояние и точка продолжения

- Проект: официальный сайт «Я ХУдЕЮ», repository `sashaermin/ya-hudeyu`, branch `work/website-v2`.
- Последний независимо verified remote **до этого documentation checkpoint**: `cf277fb28196b0b2bec5d18da9fd113e4cd8bae4` (run39114659470 success). Фактический последний SHA всегда получить через fetch/ls-remote; файл не содержит собственный будущий SHA.
- Последний ответственный агент: Codex, 18.10.2026 11:51 МСК. Другой активный website writer не известен; эта историческая запись не доказывает отсутствия активной сессии при takeover. Только один писатель ветки, Android Claude Code не затрагивать.
- Стадия: первый инкрементальный website-кандидат **подготовлен к приёмке**, с «Скоро для Android», независимо от APK. Первый принятый coming-soon выпуск опубликован; завершается live QA. Исторические ограничения ниже действуют вне этой узкой авторизации.

**Exact next:** проверить CI текущего development checkpoint: read-only tests/production_qa.py выполняет live HTTPS/16 browser cases на GitHub runner со штатным TLS trust. Production уже опубликован:9b39ffaf35c48973b8115b630ba0d06165ad09a4, Pages run39114713056 success; повторный push/deploy неизменённого сайта запрещён. 22 public HTTP hashes и12 internal404 PASS. После browser PASS — сохранить actual notices/Telegram и сопоставить весь master с выполненным, выполнить оставшиеся independent maintenance/QA (включая production Lighthouse); APK requirements отложить отдельно. Publication approved=true/coming-soon, indexing_approved=false, APK approval остаётся false. Не менять main/production без новой авторизации, не начинать deferred redesign. Rollback tag доступен на9a0857ce260540ad604f344565d535a8d47b2fa0.

## Что предъявлено владельцу

- Проверенный [review artifact](https://github.com/sashaermin/ya-hudeyu/actions/runs/39114231216/artifacts/12131711410) из run39114231216, source `70527d0`, attempt1. Это ZIP для локального просмотра, **не hosted preview URL**.
- Внешнего безопасного preview-hosting tool нет. Инструкция просмотра, предмет решения, безопасная публикация и rollback: `docs/FIRST_RELEASE.md`.
- Inner ZIP SHA-256 `7877e610d11a5a3d84b708864e0b5eae7c6c1b2ab263daeb77f7fc0cdd23c6e5`. Сайт в последующих doc/CI checkpoints не менялся; новый artifact должен совпадать по этому digest, пока не меняется контент/код сайта.
- 4 current candidate screenshots: `docs/screenshots/rc-{390,1440}-{light,dark}.png`; links и границы доказательств в `docs/QA.md`.
- Ранее review-only patch теперь **применён по прямому разрешению владельца** к tools/build.py и tests/test_coming_soon_policy.py; исходный proposal сохранён побайтно. Evidence `docs/verification/first-release-policy-proposal.json`; 15 existing+5 proposed tests PASS. Default full-release gates сохраняются; предлагаемый coming-soon mode требует отдельный site approval и запрещает APK/features/screens.
- Artifact retention7дней, URL не вечный. После реального rerun старые artifact IDs дали API404; не обещать сохранность IDs. При истечении срока/недоступности заново получить/собрать из verified source и сверить digest, не выбирать произвольный файл.

## Выполнено и проверено

Общий roadmap — только `IMPLEMENTATION_PROGRESS.md`, исходное неизменённое ТЗ — `project_specs/WEBSITE_MASTER_TZ_2026-10-18.md`. Постоянные инструкции — `AGENTS.md`, [канонический cross-agent протокол](AGENT_DEVELOPMENT_PROTOCOL.md) и [Telegram-протокол](AGENT_NOTIFICATION_PROTOCOL.md); `CLAUDE.md` ведёт к тем же правилам. Новый приоритет первого инкрементального релиза сохранён в AGENTS.md, не заменяет master.

- Этапы0/1: read-only Android audit, исходный бренд/котик/шрифты/токены обеих тем, адаптивный каркас. Provenance `docs/ASSET_SOURCES.json`, Android SHA `874de91cb626b6f0e78532963b378d86901b97d9`. Не повторять аудит неизменённых входов.
- Этап2: секции/навигация/FAQ/темы/галерея/ошибки; R1 — пользовательское coming-soon состояние. Реальные APK features/screens — deferred инкремент, не fabricated UI. Hero пока оригинальный маскот.
- Этап3: allowlisted stdlib build, SEO/fonts, noindex draft; независимые APK/site approvals. Actual `data/publication.json=false`, `data/release.json=unverified`. Validate/full-release guard сохранён; render изменён только согласованным coming-soon patch. Mode по умолчанию full, отдельное website approval обязательно.
- Этап4: исправлены gallery focus trap, skip target (`tabindex=-1`) и переполнение200% текста (`overflow-wrap:anywhere`). 4D baseline:64 viewport/theme runs в Chromium/Firefox/WebKit/Edge,16 axe0violations. После coming-soon copy R1:Chromium16/16+4axe0violations,48 text resize/spacing cases в4браузерах PASS. Не выдавать старую полную матрицу за новый запуск на новом copy. CSS text simulation — не native zoom/screen reader/device test.
- R2/R5: настоящий CI upload→download artifact; clean source/SHA/22file manifests и Chrome rendering390/1440×2темы PASS, noindex=true/APK=false/page_errors0. Текущие58 unit tests (40 notify+18 build/workflow/package) PASS в CI. Code/UI не менялся послеR1, повторные matrices не нужны.
- R4: run39110987166 attempts1/2 success, оба archive round-trip notices; Telegram127 толькоattempt1, повторного commit notice вattempt2 нет. `artifact-retry.json` честно фиксирует API404 старых IDs; global exactly-once не обещать.
- R5: current official Node24 upload7.0.2/download8.0.2 pinned SHAs, compatible inputs сверены. Run39111335266 success; verify117627928319 с `Website review archive verified`, notify117628076983 с accepted138. Node20 annotation отсутствует. `docs/verification/artifact-node24.json`.
- Lighthouse96/100/100/69 — исторический локальный4A, SEO69 из intentional noindex; не новый production замер. Физические Android/iOS/Safari, screen reader, native WebKit swipe, owner visual/legal acceptance остаются открыты. Движковая эмуляция их не заменяет.

## Незакрытые решения и ограничения

Все alert IDs стабильны в `project_specs/user_actions.json`, не создавать дубли.

1. `site-first-website-release-policy`: ближайший owner review кандидата; разрешение на patch уже получено и выполнено. Затем отдельное разрешение публикации. Это реальная текущая внешняя граница.
2. `site-approved-android-release`: APK не утверждён, скачивание выключено. Только последующий APK/features/screens инкремент по `docs/RELEASE_CONTENT.md`; не делать APK prerequisite website readiness.
3. `site-digest-default-branch-activation`: обязательное21:00 МСК расписание подготовлено, но не активно вне default branch. Main update требует разрешения с учётом legacy Pages side effect; не включать автоматически в разрешение website policy.
4. Telegram settings и network cross-browser actions resolved. Не запрашивать заново секреты/доступ браузерных CDN без новой причины. Telegram delivery реально подтверждена; secret values не читать/не печатать.

## Среда и воспроизведение

- Базовая сборка: `python3 tools/build.py`; stdlib Python3.12. Draft `_site` — единственный public artifact, корень checkout является шаблоном/внутренними документами.
- Own draft server8002 проверен: `python3 -m http.server 8002 --bind 127.0.0.1 --directory _site`. При новой сессии процессы восстановить; reuse только правильный server. Старый8001 давал empty reply, не остановлен. Localhost не показывать как доступный владельцу cloud preview.
- `python3 tools/package_preview.py` создаёт ZIP/manifest из свежего temp `_site`, указывает source SHA/dirty state. Unit/QA recipes — README/docs/QA.md; optional dependencies pinned в tools/qa.
- Browser/runtime файлы в `/tmp/website-browsers`, `/tmp/ya-hudeyu-browser-runtime`; Edge в `/tmp/website-edge` с signed Microsoft provenance. В Git нет browser binaries/node_modules. Нужные Linux QA library helper/manifest — tools/qa/prepare_linux_libs.py и docs/verification/linux-qa-packages.json.
- Cloud прямой artifact download получил403 на `productionresultssa15.blob.core.windows.net`. Domain additive + актуальный start_skill сохранены в environment **draft**, status saved/requires_publish=true, не активированы. Для прямого cloud download нужно save/publish **среды**; это optional для website proof, потому что CI round-trip уже прошёл. Не запрашивать token и не печатать signed URLs.
- Telegram отправляет только Actions по `AGENT_NOTIFICATION_PROTOCOL.md`; commit trailer `Agent: Codex`. Events append-only `project_specs/agent_events.json`. Обычный новый push автоматически проверяет и отправляет; не создавать бесконечные doc commits ради собственного SHA/следующего ack.

## Неприкосновенное

Main `9a0857ce260540ad604f344565d535a8d47b2fa0`; production Pages source legacy main:/. CNAME/privacy побайтно равны исходному main, DNS/Pages/deploy не менялись. Нельзя main update/merge/PR/deploy, public APK, изменение gates или снятие draft noindex без соответствующего явного разрешения. Не менять Android/другие клиентские репозитории/сессии. Весь существенный контекст, evidence и точный next находятся в Git; /tmp не единственный источник. При следующей сессии fetch/status/AGENTS/handoff/progress/latest verified remote обязательны.

## P1 · постоянная совместимость агентов и русские Telegram-отчёты

По новому указанию владельца общий порядок resume/checkpoint/handoff выделен в единственный AGENT_DEVELOPMENT_PROTOCOL.md с входом через AGENTS/CLAUDE. Формат и provenance определяет только AGENT_NOTIFICATION_PROTOCOL.md; CI report-check обеспечивает обязательные русские Report-* trailers и точный Agent. Прежний website roadmap/дизайн/gates не меняются. Cold-start проверяется по файлам репозитория, реальный transfer Claude↔Codex не заявляется. После проверки/сохранения этого этапа продолжить exact next выше; разрешение неприменённого gate patch пока не получено.

P1 локально проверен:47 notification tests +20 site/workflow/handoff tests PASS; draft build/JS syntax PASS, HTML hash побайтно совпадает с R1 candidate. Cold-start simulation по repository-only sources/remote GitHub checkpoint — docs/verification/cold-start-handoff.json; real transfer=false. Новые source/report поля меняют только Telegram-представление, ledger keys/credentials/destination и website public artifact не меняются. После remote checkpoint проверить CI/Telegram ack без отдельной test-send; затем возобновить прежний exact next (owner decision ещё не дано).

P1 remote verification:24c5102/run39112341703 success,47+20 tests и actual archive22files/4views PASS; Telegram accepted157. Evidence docs/verification/permanent-agent-protocol.json содержит exact API notices и воспроизведённый русский report template (не выдаётся за чтение Telegram-чата). Финальное own-source milestone правило локально48 notification tests PASS; head-agent hints удалены из sender. После текущего doc/fix checkpoint проверить новый remote SHA/CI/notify; не создавать бесконечную цепочку commits для записи собственного SHA. Next остаётся owner review/неприменённый gate patch выше; всё независимо исполнимое по новому постоянному указанию выполнено. Реальный agent transfer не тестировался.

## T1 · единая визуальная иерархия Telegram

Новое указание принято после safe remote checkpoint8888818 и successful CI. Все существующие Telegram message types используют общий presentation: bold project/event header, metadata и section titles, blank paragraphs, descriptive HTTPS links, code branch/hash/IDs. Escaping включает quote-safe attributes; общий truncator сохраняет balanced HTML/entities и footer links. Единственная спецификация — AGENT_NOTIFICATION_PROTOCOL.md, AGENTS ссылается на неё. 51 notification tests PASS, включая parser validation всех типов/опасных URL/длинных сообщений; прежняя дедупликация/ошибки покрыты. Workflow файл/triggers/secrets и send/ledger routing не менялись. После checkpoint проверить CI/обычный accepted notice, затем прежний exact next; новые approvals/gate permissions не предоставлены.

T1 remote verification завершена:674e5f5 independently confirmed; run39113063235 verify/notify success,71 tests и actual archive22files/4views/noindex/noAPK PASS; Telegram accepted165. Exact notices сохранены в telegram-presentation.json. Дополнительных живых test sends/Telegram UI screenshot не было. Задача оформления завершена; следующий approved website action остаётся exact next выше и зависит от ранее зарегистрированного owner decision. Новое указание не разрешает gate patch/main/deploy, независимых незавершённых задач с текущими inputs не найдено. Передача следующему агенту — по AGENT_DEVELOPMENT_PROTOCOL.md; текущий собственный SHA проверять через Git/Actions, не создавать endless doc commits.


## R6 · авторизованная coming-soon политика

Владелец явно разрешил применить только docs/proposals/first-release-coming-soon.patch. На clean latest remote8a0e726 SHA-256 cefd3cc1b1440efa0f09c67b557570e5c9a4f89d0b7f0c63df7b8b407f38fd03 совпал, git apply --check PASS. Patch применён без изменения предложенных bytes. 25 site/build/workflow/handoff tests PASS; draft build PASS, HTML SHA af74145de9543065e6822cc79c3252673ae43a53b2b7eeb50484b1caf61b1357 прежний. Исторические P1/T1 записи выше описывают прежние permissions, текущее узкое разрешение зафиксировано здесь. Publication approved=false, APK unverified/approved_for_distribution=false; production build с реальными config по-прежнему блокируется. Workflow/бот/production/main/noindex не меняются. Remote70527d0 подтверждён; run39114231216 success, 76 unit tests и actual archive22files/4views/noindex=true/APK=false/page_errors=0 PASS. Telegram accepted173. Exact API notices и ссылка на кандидат — docs/verification/coming-soon-policy-applied.json; быстрые screenshots/просмотр — docs/FIRST_RELEASE.md. Это доказательство отправки API, не прочтения человеком. После documentation checkpoint проверить новый remote/CI без endless doc commits.


## R7 · первый разрешённый production release (в работе)

Согласованный patch применён в R6; remote b12b0b0/main9a0857c сверены. Pages API: legacy main:/, CNAME yahudeyu-app.ru, HTTPS enforced=true; actual старые index/privacy200 и SHA совпали с Git. Backup manifest docs/verification/first-production-rollback.json; remote annotated rollback tag подтверждён независимо. Approved production build27 site tests PASS, accepted HTML SHA прежний; privacy/CNAME прежние. Indexing не нужен для serving, сохранён noindex через узкую настройку indexing_approved=false; default/full/security gates не ослаблены. Real site approved=true только по сохранённой авторизации; APK не утверждён. Нельзя выдавать подготовку за completed deployment; следующий шаг указан в Exact next.


### R7 · возобновление live QA

Remote main9b39ffa и devcf277fb подтверждены, Pages run39114713056 success. Все22 HTTP public bytes совпадают с manifest/принятым ZIP,12 internal paths404, HTTPS/Pages config сохранены (production-http.json). Chromium cloud ERR_CERT_AUTHORITY_INVALID — проблема proxy CA trust, не доказательство дефекта public certificate. Пробное временное NSS trust db не используется из-за существующего legacy NSS directory. Automatic approval review отклонил import CA в persistent NSS как расширение доверия без отдельного разрешения. Изменение не выполнено, TLS не отключался, обхода нет. Безопасная альтернатива — read-only browser QA в существующем verify workflow на штатном GitHub runner; trigger/permissions/бот не меняются, deployment не добавлен. До реального CI proof browser status pending; не заявлять PASS. Manifest/HTTP evidence прежней прерванной порции сохранены без потери.
