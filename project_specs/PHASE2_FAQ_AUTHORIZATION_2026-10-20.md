# Phase 2 — Comprehensive Feature-Based FAQ

Repository: `sashaermin/ya-hudeyu`
Website branch: `work/website-v2`
Android reference: `sashaermin/ya-hudeyu-android`

## Owner Requirement

Redesign the website FAQ into a comprehensive, categorized guide explaining the actual functionality and intended user workflows of the Я ХУдЕЮ Android application.

The FAQ must help visitors understand not only what the application is, but also what each major section does, how its features work, and how users are expected to interact with them.

The Android application is still under development. Do not publish unverified functionality as a finished or publicly available feature.

## 1. Mandatory Android Functionality Audit

Before writing FAQ content:

1. Read the current website master specification, Phase 2 review, and project agent instructions.
2. Inspect the latest relevant Android source code and documentation in read-only mode.
3. Identify the actual application navigation structure, screens, and feature modules.
4. Examine relevant ViewModels, UI states, data models, persistence, and implemented user interactions.
5. Distinguish implemented, partially implemented, planned, and unverified functionality.
6. Record supporting Android file paths and commit SHAs for each FAQ topic.
7. Identify important user-facing limitations.

Do not infer functionality from screen names alone.

Do not modify the Android repository.

## 2. FAQ Information Architecture

Organize the FAQ into meaningful categories based on the real Android application.

Candidate categories:

- General information and getting started.
- Nutrition and food diary.
- Weight and body measurements.
- Activity tracking.
- Workouts and exercises.
- Statistics and progress.
- Settings and personalization.
- Data, privacy, availability, and support.

Adjust, merge, rename, or split categories according to the actual Android project.

Do not invent sections that the application does not support.

## 3. Answer Quality

Each FAQ answer must explain practical behavior.

Where relevant, cover:

- What the feature is for.
- Where the user finds it.
- What actions the user can perform.
- What information must be entered.
- What the application calculates or displays.
- How records can be changed or deleted.
- How the information appears in history, charts, or statistics.
- Relevant limitations and dependencies.

Prefer specific, useful explanations over generic marketing language.

Example of insufficient FAQ content:

"What can I do in Nutrition?"
"You can track your nutrition."

Preferred depth:

Explain how the food diary is organized, how entries are created, what nutritional values are shown, and how the user reviews or edits entries — but only to the extent confirmed by current Android implementation.

All public-facing text must be in natural, clear Russian.

## 4. Coverage and Completeness

Create a feature-to-FAQ coverage matrix.

For each verified user-facing feature, record:

- Android feature or workflow.
- Source evidence.
- Implementation/verification status.
- Corresponding FAQ category.
- FAQ question.
- Whether the answer is safe to publish.

Prioritize complete coverage of major user workflows over an arbitrary number of questions.

Avoid repetitive questions and unnecessarily long answers.

For incomplete or unstable functionality, either clearly describe it as under development or omit detailed behavior from the public FAQ.

## 5. Website UX

Make the expanded FAQ convenient to navigate.

Requirements:

- Clear category navigation.
- Expandable questions and answers.
- Responsive layout.
- Keyboard accessibility.
- Screen-reader-friendly semantics.
- Visible focus states.
- Correct light/dark themes.
- No horizontal overflow.
- No unnecessary JavaScript dependency.
- Convenient navigation on mobile devices.
- Optional category filtering or search only if it materially improves usability.

Do not introduce complex UI merely for decoration.

Consider a short introductory explanation stating that the FAQ describes the application's development direction and that individual features may change before release.

## 6. Content Integrity

Strictly prohibit:

- Fabricated functionality.
- Unsupported claims about AI capabilities.
- Unsupported automatic calculations or integrations.
- Invented synchronization, cloud storage, or backup guarantees.
- Medical or guaranteed weight-loss claims.
- Unverified screenshots.
- Public availability claims.
- Release dates or download promises.

Preserve the privacy policy verbatim.

Preserve the current coming-soon mode, disabled APK downloads, and `noindex`.

## 7. Implementation and Verification

1. Implement the FAQ improvements on `work/website-v2`.
2. Preserve the existing approved website design.
3. Update navigation and layout only where necessary.
4. Add tests for FAQ category navigation, expanding/collapsing, keyboard interaction, and responsive behavior.
5. Check light/dark themes and mobile layouts.
6. Validate every factual FAQ answer against Android evidence.
7. Generate desktop and mobile screenshots of the new FAQ.
8. Update Phase 2 review documentation and the feature coverage matrix.
9. Commit and push verified changes to the development branch.
10. Confirm the remote SHA.
11. Send the established Russian Telegram report.

## 8. Publication Restrictions

This task authorizes development and review only.

DO NOT:

- Merge into `main`.
- Deploy to production.
- Modify Android or Windows repositories.
- Publish an APK.
- Enable indexing.
- Start the postponed full redesign.
- Activate unrelated workflows.

## 9. Owner Review Package

Prepare:

1. Complete categorized FAQ content.
2. Feature-to-FAQ coverage matrix with Android sources.
3. List of omitted or unverified features.
4. Desktop and mobile screenshots in both themes.
5. Accessibility and regression test results.
6. Exact development SHA.
7. A clear explanation of how the FAQ can be expanded as Android development progresses.

## Final Report — Russian

Report:

- Изученные Android-модули
- Категории FAQ
- Количество вопросов
- Какие функции подробно объяснены
- Какие функции исключены и почему
- Скриншоты
- Результаты проверок
- Development SHA
- Production SHA (unchanged)
- Что требуется утвердить

Complete the FAQ development and verification autonomously, then STOP before publication.