# Daily digest: активированное расписание и следующий notification-only sync

Назначение неизменно: «Я худею GROUP» → «Сайт | Я ХУдЕЮ», topic6. Секреты не извлекались. Main сейчас `e37f521c0f62226fb3c4419372a11a79699ec38c`; относительно public release8fb7bf2 изменены только четыре Telegram-файла в.github, public content прежний.

## Подтверждённое состояние

- `.github/workflows/website-digest.yml` существует наdefaultmain, workflow388551143 имеет state active. Cron `0 18 * * *` =21:00 Europe/Moscow. Checkout runtime — `${{ github.sha }}`; данные берутся read-only API изwork/website-v2.
- Manual workflow_dispatch39141327550 и39141381414 success. Digest check117716359241 подтвердил Telegram topic6/message28. Владелец также подтвердил фактическую доставку.
- В проверенной API-истории только эти manual runs. **Первый автоматический schedule ещё не проверен**; наличие active/cron не доказывает его успешное выполнение. Не запускать лишний digest и не сбрасывать ledger для проверки.
- `site-digest-default-branch-activation` resolved: запрос выполнен. APK approval остаётся отдельным открытым действием.

## Исправление attribution в development

Digest учитывает Agent trailers всех unique SHA в actual24h query scope, через existing agent_source/normalized_agent; автор, GitHub username иrunner не определяют identity. Один агент → «Агент», несколько → «Агенты»; смесь known/unknown явно partial, безknown → «Не определён», нолькоммитов → «Агенты: Нет данных». «Механизм: GitHub Actions» сохранён отдельно. При сканировании нескольких веток одинSHA считается впервой запрошенной ветке, повторно не увеличивает count/attribution ине попадает вsummaries. При штатном --branch scope остаётся work/website-v2.

## Явный allowlist следующей синхронизации

Требует **нового отдельного разрешения владельца**, не повторной активации расписания. Не merge development branch. Синхронизировать только:

1. `.github/scripts/telegram_notify.py` — factual contributor aggregation/dedup.
2. `.github/scripts/test_digest_attribution.py` — новые regression tests.
3. `.github/scripts/test_topic_digest.py` — pagination fixture с уникальнымиSHA.
4. `.github/scripts/test_telegram_notify.py` — presentation contract допускает требуемый plural «Агенты».

Хеши и isolated-main validation — [verification/digest-attribution.json](verification/digest-attribution.json). Workflow, secrets, topic6, retries, HTML, provenance, daily dedup keys иdry_run **не требуют изменений**. Не переносить docs/project_specs/AGENTS/handoff/website-checks/public data/content/tests сайта вmain. Handoff/action registry читаются сdevelopment через API, поэтому корректировка status после dev push уже доступна старому runtime; исправление Agent header станет доступно main-runtime только после разрешённого sync.

После разрешения fetch обеих веток, inspect advancement, сверить allowlist/hashes; сохранить текущий main/public manifest. Подготовить минимальный commit только четырёх файлов, проверить неизменность всех public bytes и прежнего workflow. Legacy Pages main:/ может автоматически rebuild при main push: авторизация должна учитывать это; deployment config не менять и вручную deploy не запускать. После push проверить mainSHA, сайт/HTTPS/noindex/APK-disabled инедоступность.github. Не reset/force-push/rewrite history.

Для safe preview использовать workflow_dispatch dry_run=true (default) после sync либо CLI --dry-run до него: реальный API без sends/cache/ledger mutations. Не выполнять live dispatch заново ради этого fix: daily key по Moscow day сохранён, прежние уведомления не пересылать. Первый реальный scheduled run проверить read-only поevent=schedule/conclusion=success иactual Telegram topic/message annotations. GitHub может задерживать расписание; global exactly-once при потереcache/неопределённости сети не гарантируется.
