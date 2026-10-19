# Task: Add an Android App Preview Gallery to the Я ХУдЕЮ Website

## Project

Repository: `sashaermin/ya-hudeyu`
Development branch: `work/website-v2`
Production website: `https://yahudeyu-app.ru/`

## Objective

Create a polished, responsive, accessible gallery showcasing 11 preliminary Android application screens.

The gallery must help visitors understand the application's interface and functionality while clearly communicating that these are preliminary demonstration images, not final release screenshots.

This task is authorized for development only. Production deployment requires separate explicit owner approval.

## 1. Initial assessment

Before making changes:

1. Read `AGENTS.md`, `CLAUDE.md`, `AGENT_DEVELOPMENT_PROTOCOL.md`, `AGENT_HANDOFF.md`, `IMPLEMENTATION_PROGRESS.md`, and the website master specification.
2. Fetch and verify the latest remote development and production states.
3. Inspect the existing homepage, gallery implementation, branding, layout components, and responsive behavior.
4. Preserve all completed Phase 2, FAQ, and Phase 3 work.
5. Check whether the previous authorized production release has completed. Do not interfere with an active release.
6. Verify which screenshot assets are actually available in the repository or attached to the task.

Do not assume that images shared in a separate ChatGPT conversation are automatically available to the coding agent.

## 2. Image sources and privacy

The owner has provided 11 Android interface screenshots covering:

1. Today — main dashboard.
2. Nutrition.
3. Activity.
4. Progress.
5. Profile and goals.
6. Additional dashboard cards.
7. All goals.
8. GPS walking.
9. My Journey.
10. Weight-loss plan.
11. Charts.

A preliminary anonymized composite image has also been prepared in ChatGPT.

Use only image assets actually supplied and accessible to the agent.

If the 11 individual anonymized images are not available, do not recreate them from memory, fabricate screenshots, or extract individual images from an inaccessible attachment.

Report exactly which assets are missing and request them from the owner.

### Privacy requirements

No real personal or sensitive data may appear in public gallery assets.

Remove or replace:

- Personal names.
- Actual weight and measurement history.
- Real health and medication details.
- Real GPS locations, routes, and coordinates.
- Personal reminders or appointments.
- Account identifiers, notifications, and device-specific information.

Use coherent, realistic fictional demonstration data.

Preserve the visual design of the actual application wherever possible.

Avoid introducing visual features or functionality that do not exist in the source material.

If an image contains a layout defect, fix the demonstration asset only when the correction can be made reliably without misrepresenting the application.

Do not modify the Android repository.

## 3. Gallery design

Add a new homepage section titled:

"Посмотрите, как выглядит приложение"

Subtitle:

"Демонстрационные изображения на основе текущего интерфейса Android-приложения «Я ХУдЕЮ»."

Organize the gallery into meaningful categories:

- Обзор
- Питание
- Активность
- Вес и прогресс
- Цели и здоровье

The gallery must include all 11 screens once their approved anonymized assets are available.

Each gallery item must contain:

- Screenshot.
- Screen title.
- Short, factual Russian description.
- Appropriate accessible alternative text.
- A clear indication that the image is preliminary.

### Screen descriptions

**Сегодня**
Главная панель с калориями, БЖУ, активностью, весом и прогнозом достижения цели.

**Питание**
Дневник питания с учётом калорий и нутриентов, добавлением продуктов, поиском и сканированием.

**Активность**
Шаги, расстояние, активные минуты, тренировки, программы и рекорды.

**Прогресс**
Изменение веса, движение к цели, графики, сравнения и персональные показатели.

**Профиль и цели**
Настройка целей, достижения, параметры отслеживания здоровья и интеграция с Health Connect.

**Дополнительные карточки**
Привычки, настроение, календарь, тренировки, замеры и другие показатели в одном месте.

**Все цели**
Ежедневные цели, история выполнения и серии успешных дней.

**Ходьба с GPS**
Карта маршрута, цель по времени, интервалы и автопауза.

**Мой путь**
История изменения веса, результаты за период и движение к цели.

**План похудения**
Целевой вес, расчётный темп похудения, прогноз и сравнение плана с фактическим результатом.

**Графики**
Наглядная статистика веса и других показателей за выбранные периоды.

Validate every description against the supplied screenshots and, where necessary, the current Android source in read-only mode.

Do not make unsupported claims about production readiness, availability, or fully verified functionality.

## 4. Interaction and responsive behavior

Desktop:

- Display multiple screenshots in a balanced layout.
- Preserve the portrait aspect ratio of the Android screens.
- Avoid excessive whitespace and tiny unreadable previews.

Mobile:

- Display one prominent screenshot at a time.
- Support convenient swipe navigation where practical.
- Provide accessible previous/next controls.

All devices:

- Support light and dark website themes.
- Provide an enlarged image viewer with keyboard controls.
- Support Escape to close the viewer.
- Restore focus after closing.
- Support accessible category navigation.
- Avoid layout shifts and horizontal page overflow.
- Respect reduced-motion preferences.
- Use optimized image formats and lazy loading.
- Preserve usability without JavaScript wherever practical.

Reuse existing website components and design tokens rather than introducing an unrelated visual style.

## 5. Mandatory preliminary-image disclaimer

Display a visible label near the gallery heading:

"Предварительный интерфейс · В разработке"

Below the gallery, display:

**Предварительные изображения приложения**

"Представленные изображения демонстрируют текущую концепцию интерфейса «Я ХУдЕЮ» и носят ознакомительный характер. Дизайн, расположение элементов, набор функций и их внешний вид могут измениться в процессе разработки. Финальная версия приложения может отличаться от показанной.

Все персональные данные и показатели на демонстрационных изображениях являются условными."

The disclaimer must remain readable on mobile and desktop in both themes.

Do not describe edited demonstration images as exact screenshots of the final application.

## 6. Existing website restrictions

Preserve:

- Existing homepage and Phase 2 sections.
- The comprehensive FAQ.
- The `/download/` beta preparation page.
- Existing mascot and branding.
- Privacy policy and legal content.
- `noindex` until separately authorized.
- APK download disabled.
- Existing deployment configuration.
- Current production website.

Do not publish an APK or enable download buttons.

Do not modify Android or Windows repositories.

Do not merge the entire development branch into `main`.

## 7. Testing

Run appropriate existing and new tests covering:

- Gallery item count and ordering.
- All 11 images, when available.
- Image asset existence and integrity.
- Privacy and demonstration-data checks.
- Category navigation.
- Enlarged image viewer.
- Keyboard navigation and focus management.
- Mobile swipe behavior.
- Light and dark themes.
- Responsive layouts.
- Accessibility checks.
- No-JavaScript fallback.
- Performance and image optimization.
- Regression tests for homepage, FAQ, and download page.
- Preservation of APK-disabled and noindex states.

Test at mobile, tablet, and desktop viewport sizes.

Document any tests that cannot be performed.

## 8. Review package

Prepare:

- Desktop screenshots in both themes.
- Mobile screenshots in both themes.
- Gallery interaction evidence.
- Asset inventory with source and anonymization status.
- Privacy verification results.
- Test results.
- List of limitations and unresolved questions.
- Owner review instructions.

Create or update an appropriate gallery review document.

## 9. GitHub and reporting

Commit and push verified development changes to `work/website-v2`.

Update:

- `IMPLEMENTATION_PROGRESS.md`
- `AGENT_HANDOFF.md`
- Relevant verification documents
- Agent event history

Follow the existing Telegram notification protocol.

The final report must be in Russian and include:

1. Сделано
2. Использованные изображения
3. Проверка обезличивания
4. Результаты тестирования
5. Ссылки на скриншоты сайта
6. Development SHA
7. Состояние production
8. Что требуется от владельца

## 10. Authorization boundary

Development and review preparation are authorized.

Production publication is NOT authorized by this task.

If the required individual anonymized images are unavailable, stop the image-dependent implementation and request the missing assets instead of inventing them.

Do not claim completion of the full 11-image gallery until all 11 approved assets are included and verified.

Do not perform unrelated development.