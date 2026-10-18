# Я ХУдЕЮ — официальный сайт

Статический сайт Android-приложения. Разработка: `work/website-v2`; `main` и действующая публикация не изменены. APK для публичного распространения пока **не утверждён**. Карточки возможностей и скриншоты ожидают проверенной сборки; рабочая версия содержит явные временные состояния.

## Начало работы

Сначала прочитайте [AGENTS.md](AGENTS.md), [handoff](AGENT_HANDOFF.md) и [прогресс](IMPLEMENTATION_PROGRESS.md). Claude Code использует тот же маршрут через CLAUDE.md. Утверждённое [мастер-ТЗ](project_specs/WEBSITE_MASTER_TZ_2026-10-18.md) сохранено без замены.

Сборке нужен только Python 3.12+ (stdlib), без установки пакетов. Сайт не требует API, БД, регистрации, аналитики или секретов. Node.js используется только для проверки синтаксиса.

```sh
cd /workspace/ya-hudeyu
python3 tools/build.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory _site
```

Сборщик генерирует `_site` из index.html и JSON. Открытие корневого index.html напрямую не заменяет сборку: это шаблон. Проверять сервер локальными HTTP-запросами к `/`, `/privacy.html`, CSS/JS и ресурсам. Облачный onboarding не предоставляет user-facing localhost preview.

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m unittest discover -s .github/scripts -p 'test_*.py' -v
python3 .github/scripts/telegram_notify.py actions
python3 .github/scripts/telegram_notify.py events
node --check scripts/site.js
node --check scripts/theme.js
```

Браузерный QA и конкретные результаты — [docs/QA.md](docs/QA.md). Дополнительные QA-зависимости устанавливаются отдельно, для обычного сайта они не нужны. GitHub Actions проверяет stdlib build/tests и JS syntax; браузерная матрица пока отдельный запуск.

## Структура

- `index.html`, `styles/site.css`, `scripts/`: шаблон и доступные компоненты.
- `data/site.json`, `data/release.json`: контент и единый источник метаданных APK.
- `assets/`: оригинальный Android-бренд, локальные шрифты/OFL и производные WOFF2.
- `tools/build.py`: draft/production build по белому списку, не deployment.
- `privacy.html`, `CNAME`: действующие юридическая страница и домен, сохранены побайтно.
- [SOURCE_AUDIT](docs/SOURCE_AUDIT.md), [DESIGN_MAPPING](docs/DESIGN_MAPPING.md), [RELEASE_CONTENT](docs/RELEASE_CONTENT.md): происхождение дизайна и честное состояние релиза.
- [AGENT_NOTIFICATION_PROTOCOL](AGENT_NOTIFICATION_PROTOCOL.md): сайт-специфичные GitHub Actions/Telegram, без локальных отправок и без чтения секретов.

Темы: system → light → dark → system по кнопке в шапке; ручной выбор хранится только локально. Меню поддерживает Escape и возврат фокуса; gallery viewer использует native dialog, клавиши, touch и возврат фокуса. При отключённом JS главные секции, ссылки, FAQ и мобильная навигация доступны.

## Подготовка выпуска и откат

`python3 tools/build.py --production` блокируется до утверждения/проверки APK и заполнения подтверждённых возможностей/скриншотов. Команда ничего не публикует. Порядок проверки артефакта и метаданных — RELEASE_CONTENT.

GitHub Pages предполагается по текущей структуре/CNAME; фактические Settings → Pages/source недоступны из среды (403). Перед согласованным релизом сначала проверить существующий механизм и требования домена/HTTPS. **Не менять main, не создавать PR, не сливать, не деплоить и не публиковать APK без явного отдельного разрешения владельца.** Workflow в рабочей ветке только проверяет и уведомляет; Pages deployment в нём нет.

Согласованная публикация должна отдавать только `_site`, сохраняя CNAME и privacy.html, без docs/project_specs. Корень репозитория не является публикуемым артефактом v2.

План отката после будущего разрешённого релиза:

1. Зафиксировать SHA последней рабочей production-версии и Pages deployment до изменения.
2. При проблеме вернуть последний рабочий артефакт через подтверждённый механизм Pages; не использовать force-push/reset shared history.
3. Если для отката нужен commit, согласовать revert релизного коммита отдельно; не удалять историю рабочей ветки.
4. Проверить HTTPS, главную, `/privacy.html`, CNAME/DNS, ссылки и APK. Зафиксировать причину/результат в общих progress/handoff.

В текущей работе публикация и откат production не выполнялись.
