# Я ХУдЕЮ Website — Phase 2: Content Expansion and Visual Enrichment

## Project

Repository: `sashaermin/ya-hudeyu`
Development branch: `work/website-v2`
Production: `https://yahudeyu-app.ru/`
Current production SHA: `8fb7bf2920a89f39e1ed3a56d53ada91f468b715`
Last known development checkpoint: `5b4ae4f`

## Owner Authorization

The owner authorizes implementing and testing Phase 2 website improvements in the development branch.

**This is NOT authorization to publish, deploy, merge into `main`, or change production.**

The Android application is still under active development. The owner explicitly does not want to distribute an APK yet.

The goal is to make the existing coming-soon website more engaging, informative, visually polished, and useful without presenting unfinished application features as released functionality.

## 1. Read and Verify Existing Project

Before making changes:

1. Read `AGENTS.md`, `CLAUDE.md`, `AGENT_DEVELOPMENT_PROTOCOL.md`, `AGENT_HANDOFF.md`, `IMPLEMENTATION_PROGRESS.md`, `project_specs/WEBSITE_MASTER_TZ_2026-10-18.md`, and `docs/UI_UX_REQUIREMENTS_AUDIT.md`.
2. Inspect the existing website, assets, components, typography, responsive layouts, themes, and mascot illustrations.
3. Review the actual current Android project documentation in read-only mode when needed to verify feature descriptions.
4. Identify which content and visual components can be reused.
5. Preserve completed requirements and existing regression coverage.

Do not rebuild the website from scratch.

## 2. Expand the Main Page

Improve the existing page structure with the following sections, adapting them to the current layout rather than blindly duplicating existing content.

### A. Hero Section

Preserve the established brand identity.

Improve the presentation of:

- Application name and purpose.
- Friendly, recognizable fitness cat mascot.
- Clear value proposition.
- Android coming-soon status.
- A visually balanced composition for mobile and desktop.

Do not introduce an active download button.

### B. Application Capabilities

Create visually distinct, responsive cards explaining the application's intended areas:

- Food and nutrition tracking.
- Weight and body progress.
- Physical activity.
- Workout planning and tracking.
- Statistics and progress visualization.

Verify the actual project scope before writing claims.

Distinguish planned functionality from currently available functionality. Do not promise specific capabilities that cannot be supported by project documentation.

Use appropriate illustrations, icons, and varied card layouts.

Avoid making every section look like the same repeated grid.

### C. How It Works

Add a concise, visually engaging explanation of the intended user journey.

Possible structure:

1. Track nutrition.
2. Record activity and workouts.
3. Monitor weight and progress.
4. Review changes over time.

Use a timeline, connected cards, or another suitable visual pattern.

This must describe the intended product experience, not imply that the application is already publicly available.

### D. Mascot and Motivation

Make better use of the existing fitness cat mascot.

Requirements:

- Reuse approved mascot assets wherever possible.
- Integrate the mascot into useful content rather than adding random decoration.
- Introduce a small number of friendly motivational or informational cards.
- Avoid excessive mascot repetition.
- Preserve visual consistency across light and dark themes.
- Do not replace the mascot with generic cats or unrelated illustrations.

If additional mascot poses would materially improve the result, document the proposed poses and their intended use. Do not silently introduce a different mascot style.

### E. Development Status

Add a clear, polished section explaining that the Android application is in development.

Communicate:

- The project is actively being developed.
- Public APK distribution is not yet available.
- The website will provide official release information when approved.

Do not invent:

- Release dates.
- Development completion percentages.
- Public beta availability.
- App store listings.
- Unsupported development milestones.

### F. FAQ

Review and improve the existing FAQ without unnecessary duplication.

Cover relevant questions such as:

- What is Я ХУдЕЮ?
- Is the application available yet?
- Which platform is planned?
- Where will official release information appear?
- What is known about privacy and data handling?
- How can visitors contact the project?

Only publish factual answers supported by the current project and policies.

## 3. Visual Design Requirements

This phase is an enrichment of the approved design, NOT the postponed full redesign.

Preserve:

- Existing logo and brand identity.
- Approved cat mascot.
- Onest and Unbounded typography.
- Established green accent and theme tokens.
- Light and dark modes.
- Existing navigation and footer.
- Existing privacy policy and legal text.

Improve visual variety using:

- Feature cards with different compositions.
- Clear typography hierarchy.
- Selective illustrations and iconography.
- Timeline or step-by-step visualization.
- Appropriate spacing and section transitions.
- Subtle interactive states and transitions.
- Meaningful progress-themed visual motifs.

Avoid:

- Generic template appearance.
- Excessive gradients and shadows.
- Unnecessary animation.
- Decorative charts that imply real user data.
- Fake application screenshots.
- Fake testimonials.
- Artificial countdown timers.
- Unapproved email collection.

## 4. Responsive and Accessibility Requirements

Support at least:

- 320 px and 360 px mobile.
- 390 px and 430 px mobile.
- 768 px tablet.
- 1024 px laptop.
- 1440 px desktop.
- 1920 px wide desktop.

Check both light and dark themes.

Requirements:

- No horizontal overflow.
- Readable typography.
- Correct card stacking and spacing.
- No navigation overlap.
- Keyboard accessibility.
- Visible focus indicators.
- Appropriate semantic markup.
- Reduced-motion support.
- Meaningful alternative text.
- WCAG AA contrast where applicable.
- Reasonable loading and asset sizes.
- Graceful behavior without JavaScript where practical.

## 5. Content Integrity and Release Restrictions

The site must remain in coming-soon mode.

Mandatory restrictions:

- APK download disabled.
- No APK file published.
- No fabricated application screenshots.
- No invented release claims.
- `noindex` preserved.
- Privacy policy text preserved.
- No production configuration changes.
- No Android or Windows repository modifications.
- No unrelated GitHub Actions changes.
- No activation of the daily Telegram digest.

Do not use external stock illustrations that conflict with the existing brand.

## 6. Implementation Workflow

Work autonomously within `work/website-v2`.

1. Audit the current sections and avoid duplicating existing content.
2. Define a concise Phase 2 implementation plan.
3. Implement the approved improvements.
4. Reuse existing components and design tokens.
5. Add or update tests for new behavior.
6. Run the full relevant regression suite.
7. Perform browser-based responsive and accessibility checks.
8. Capture actual screenshots of the updated development build.
9. Update progress and handoff documentation.
10. Commit and push verified development changes.
11. Verify the remote SHA.
12. Send the established Russian Telegram development report.

Do not repeatedly run large test matrices without a meaningful reason.

## 7. Mandatory Owner Review

Before any publication, prepare a review package containing:

- A concise before/after summary.
- Full-page desktop screenshots in light and dark themes.
- Full-page mobile screenshots in light and dark themes.
- Screenshots highlighting the new sections.
- A description of any proposed new mascot poses.
- A list of all new factual product claims and their supporting sources.
- Test results.
- Known limitations.
- Exact development commit SHA.
- Instructions for reviewing the updated website locally or through a genuinely available preview mechanism.

Do not invent a publicly hosted preview URL.

If a preview artifact is used, identify its actual source, retention limitations, and verification method.

## 8. Completion Rules

After implementation and verification:

**STOP before production deployment.**

Do not merge into `main`.

Do not deploy to GitHub Pages.

Do not ask for permission to publish until the review package is complete.

The owner must explicitly approve the new design and content before any production release.

## Final Report — Russian

Provide:

1. Сделано
2. Новые разделы и визуальные улучшения
3. Что изменилось относительно текущего сайта
4. Скриншоты для просмотра
5. Проверено
6. Development SHA
7. Production SHA — unchanged
8. Остаточные ограничения
9. Что требуется утвердить
10. Следующий шаг

Execute Phase 2 autonomously within the development branch, preserve all release restrictions, and deliver a complete review package.