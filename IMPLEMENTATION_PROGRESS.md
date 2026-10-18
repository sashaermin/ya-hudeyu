# Реализация сайта «Я ХУдЕЮ»

Единственная общая дорожная карта Codex / Claude Code / других агентов. Основание: неизменённый [мастер-ТЗ](project_specs/WEBSITE_MASTER_TZ_2026-10-18.md). Общие правила — AGENTS.md, текущее продолжение — AGENT_HANDOFF.md.

| Этап ТЗ | Цель / критерии | Состояние и checkpoint | Проверки / остаток |
|---|---|---|---|
| 0. Аудит | Источники, токены, ресурсы, различение release/dev | Аудит выполнен, `a4de44b` | Android SHA зафиксирован; пути/активы описаны. APK и release screenshots ожидают решения владельца. Pages settings недоступны API. |
| 1. Дизайн-основа | Оригинальный бренд, CSS-токены и обе темы, адаптивный каркас | Реализован `356eaef` | Сверены оригинальные ресурсы; node syntax PASS. Браузерная матрица/контраст — этап 4. |
| 2. Контент / секции | Hero, возможности, gallery, установка, FAQ, footer | Каркас и взаимодействия `24ca8d5`; релизный контент частично заблокирован | Draft build PASS; JS syntax PASS; CNAME/privacy побайтно сохранены. Реальные скриншоты, публичные функции и hero screenshot не добавлены без подтверждённой сборки. |
| 3. Загрузка / SEO | Проверенный APK, checksum/версия/совместимость, метатеги, performance | В работе | Download gate реализован, draft noindex, production build блокируется. Нужны проверка gate tests, оптимизация шрифтов и документация релиза. |
| 4. QA | 8 ширин × 2 темы; клавиатура, touch, ссылки, axe/Lighthouse, screenshots | В работе | Первый Chromium desktop: нет pageerror/overflow, шрифты загружены. Полная матрица ещё не выполнена; Firefox/Safari/физические устройства не проверены. |
| 5. Публикация | Одобрение владельца, main/deploy, HTTPS/APK/rollback | Не разрешена, не начата | Нельзя менять main, PR/merge/deploy/publish APK без отдельного разрешения. |

## Дополнительный разрешённый этап W1 — общая работа агентов и уведомления

Объём: общие инструкции, handoff, прогресс, сохранение оригинального ТЗ, сайт-специфичный Telegram через Actions, стабильные event/action IDs. Без Android-записи и без default-branch schedule.

Критерии: единые инструкции без конфликта, только один писатель, детерминированные mock-тесты уведомлений/экранирования/дедупликации/секретов, корректный workflow без deploy, реестр pending APK. Прямой Telegram send из cloud запрещён; фактическая доставка требует доступного Actions run. Локально проверено: 30/30 notification tests PASS без skip; 11/11 build/workflow tests PASS; YAML parsed. Удалён только Android-only repository milestone registry test: состояние сайта хранится в общем tracker, не в дублирующем roadmap registry. Доставка и remote CI run не подтверждены (API 403).

## Решения владельца и открытые ограничения

- APK не утверждён (прямое подтверждение владельца 18.10.2026); registry `site-approved-android-release`.
- Нет подтверждённых release screenshots; не подменять интерфейс.
- Наличие Telegram Actions secrets/доставка неизвестны из-за API 403; registry `site-telegram-settings-verification`.
- Digest 21:00 МСК опционально отложен: требует default-branch workflow, main не разрешён.
- Визуальное сходство подтверждает владелец на этапе приёмки, юридические изменения согласуются отдельно.

## Журнал проверок

- До `24ca8d5`: Python draft build PASS; node --check обоих scripts PASS; privacy/CNAME равны origin/main.
- Первый Chromium 1440px: pageerror 0, scrollWidth = viewport, fonts loaded; снимок временный `/tmp/website-first-desktop.png`, итоговые screenshots будут сохранены в Git на этапе 4.
- W1 первоначальная адаптация Android notification tests: 31 test, 4 failure и 3 skip. Причины: ожидавшиеся старые названия сообщений/путь HANDOFF.md и отсутствующие новые регистры. Ожидания адаптированы к сайту, регистры добавлены; повторный запуск обязателен. Не считать этот run успешным.
- Build regression tests: 10/10 PASS (блокировка неподтверждённых APK/функций/screens, HTTPS/path safety, экранирование и повторяемость сборки).
