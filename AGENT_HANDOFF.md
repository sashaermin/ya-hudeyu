# «Я ХУдЕЮ» — общий handoff сайта

- Repository: `sashaermin/ya-hudeyu`.
- Branch: `work/website-v2` (от main).
- Последний независимо подтверждённый remote checkpoint: `a14a2c640373e60496cd840cd4f7ad7f9f0e24c6`. Более поздний содержащий этот handoff commit проверять через `git ls-remote`, не полагаться на самоссылку.
- Последний ответственный агент: Codex. В текущей сессии Codex — активный единственный писатель сайта; это историческая запись, не вечный lease. Другой активный website writer неизвестен. Android Claude Code активен отдельно и не затрагивается.
- Текущая задача: этап 4 — сохранить результаты QA и исправления фокуса/performance. W1 и уточнение W1.1 реализованы; живая Telegram-доставка всё ещё не проверена.
- Завершённые checkpoints: этап 0 `a4de44b`; основа этапа 1 `356eaef`; секции/взаимодействия этапа 2 `24ca8d5`. Релизные критерии этапов 2–4 остаются открытыми.

**Next:** Продолжить этапы 3/4: подключить оптимизированные WOFF2-шрифты, проверить production gate, сохранить RELEASE_CONTENT/README, выполнить Chromium viewport/theme/keyboard/touch/axe/Lighthouse QA. W1 реализован и проверен локально; фактическая Telegram-доставка остаётся pending из-за API 403. Не повторять аудит и инфраструктурный setup.

## Текущее исполнение и доказательства

- Сайт — статический HTML template + CSS/JS, конфигурация `data/site.json`, `data/release.json`, dependency-free `python3 tools/build.py` → `_site` (draft noindex). Serve только `_site`.
- Запущенный Codex HTTP на 127.0.0.1:8001, каталог `_site`; процессы не переживают новую cloud task. Старый onboarding server на 8000 может существовать — он не production. Перед остановкой проверять владельца процесса.
- Дизайн: оригинальные Onest/Unbounded, green #58A936, тёплые neutral surfaces, оригинальный mascot_calm, green wordmarks. Provenance: docs/ASSET_SOURCES.json.
- Android read-only clone для аудита: `/tmp/ya-hudeyu-android-audit`, reference commit `874de91cb626b6f0e78532963b378d86901b97d9`. Не используется как workspace Android-разработки. Временные файлы не канон; исходные ссылки и SHA в docs/SOURCE_AUDIT.md.
- Build tests 10/10 PASS. Первоначальные notify tests: 4 failures / 3 skips из 31 при адаптации; исправлены ожидания/регистры; финальные 30/30 notify tests PASS (лишний Android-only registry test удалён). Workflow YAML parsed; build/workflow tests 11/11 PASS. node syntax и первоначальный Chromium 1440px PASS; полной матрицы ещё нет.
- В среде доступны Python Playwright, `/usr/bin/chromium`, Pillow/fontTools. Временные QA npm packages `/tmp/website-qa` (Lighthouse 12.8.2, @axe-core/playwright 4.10.2); Brotli `/tmp/website-font-tools`. Для будущей машины команды/версии нужно сохранить в README.

## Открытые решения / ограничения

- Владелец явно подтвердил: ни один APK не разрешён к публикации. Download недоступен; metadata/screens/функции ждут конкретного артефакта. Ссылка/старый APK не выбираются агентом.
- Главная содержит временные состояния возможностей и галереи; настоящие release screenshots нужны для завершения требований, включая hero.
- Telegram API напрямую не вызывается агентом. Проверка имён Actions secrets через gh api заблокирована 403; отсутствие локальных Telegram env не означает отсутствие repository secrets. Доставка **не проверена**. Pending действия в project_specs/user_actions.json.
- Юридические тексты и CNAME побайтно сохранены. Main, merge, PR, deploy, публикация APK не разрешены. Никакой Windows-рекламы.
- Optional digest не активирован, поскольку schedule требует main. Не менять default branch ради уведомлений.
