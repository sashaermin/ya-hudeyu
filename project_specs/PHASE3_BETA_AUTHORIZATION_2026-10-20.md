# Я ХУдЕЮ Website — Phase 3: Android Beta Distribution Readiness

## Project

Website repository: `sashaermin/ya-hudeyu`
Development branch: `work/website-v2`
Android reference repository: `sashaermin/ya-hudeyu-android`
Production website: `https://yahudeyu-app.ru/`

## Owner Authorization

The owner authorizes autonomous implementation and testing of the website infrastructure and user interface required for future Android beta distribution.

This task must begin **after the current comprehensive FAQ task has finished**.

The Android application is not ready for public distribution. No APK has been approved.

This authorization covers development and review only.

**Do not publish the website changes, distribute an APK, create a public beta release, or modify production.**

## 1. Initial State Verification

Before starting:

1. Fetch the latest remote `work/website-v2` branch.
2. Read all permanent project and agent instructions.
3. Review the completed Phase 2 work and the latest comprehensive FAQ implementation.
4. Read the website master specification, implementation progress, handoff, release policy, and existing APK readiness documentation.
5. Verify the current production SHA rather than assuming it is unchanged.
6. Inspect existing release configuration, build scripts, public assets, download restrictions, and tests.
7. Review relevant Android project metadata in read-only mode.

Do not overwrite, revert, or duplicate the completed FAQ work.

Do not assume the Android application is release-ready.

## 2. Beta Distribution Architecture

Prepare an architecture supporting direct APK distribution from the official website.

Preferred initial approach:

- Website hosted on the existing GitHub Pages infrastructure.
- Versioned APK files hosted through GitHub Releases.
- A stable official download page on `yahudeyu-app.ru`.
- Explicitly approved release metadata.
- A controlled mechanism for activating and deactivating downloads.

Evaluate this approach against the repository's existing release configuration.

If an alternative is technically preferable, document the reasoning before implementation.

Do not introduce unnecessary hosting services, paid infrastructure, databases, or backend dependencies.

## 3. Dedicated Download Page

Prepare a polished, responsive page at:

`https://yahudeyu-app.ru/download`

The page must support two distinct states.

### State A — Beta Not Available

This is the mandatory default state.

Display:

- Я ХУдЕЮ branding and mascot.
- Android application description.
- Clear beta development status.
- Explanation that public downloads are not yet available.
- Information about what the future beta page will provide.
- Links to the website's functionality guide/FAQ and privacy policy.

No active download link may appear.

### State B — Approved Beta Available

This state must be implemented and tested but remain inactive until a future explicit owner authorization.

When activated, display:

- Application name.
- Beta status.
- Exact version name.
- Version code, if useful.
- Publication date.
- APK file size.
- Supported Android versions, if verified.
- Download APK button.
- SHA-256 checksum.
- Release notes.
- Known issues.
- Installation instructions.
- Feedback/report-a-bug link.

Use the existing visual identity, fonts, themes, navigation, footer, and approved mascot assets.

Do not invent release metadata or unsupported compatibility claims.

## 4. Download Experience

Design the future user journey:

1. Visitor opens the official website.
2. Visitor selects the Android beta section.
3. Visitor reviews version details and known limitations.
4. Visitor downloads the approved APK.
5. Visitor follows Android installation instructions.
6. Visitor can check the installed version and return for future updates.

Provide clear guidance about Android's installation-from-unknown-sources permission.

Explain that Android may require user confirmation before installation.

Do not encourage disabling unrelated security protections.

The site must never silently download or install software.

## 5. Release Metadata and Configuration

Extend the existing release configuration rather than creating conflicting sources of truth.

Support structured, validated fields for:

- Release channel (`beta`).
- Version name.
- Version code.
- APK download URL.
- APK SHA-256.
- APK size.
- Release date.
- Minimum supported Android version.
- Release notes.
- Known issues.
- Download approval status.
- Publication approval status.

Optional metadata must not be fabricated when unknown.

Separate the following permissions:

1. APK artifact has been technically verified.
2. Owner has approved distributing this exact APK.
3. Owner has approved publishing the corresponding website changes.

No single generic boolean should silently imply all three permissions.

Use fail-closed defaults.

Invalid or incomplete release metadata must prevent download activation.

## 6. GitHub Releases Integration

Prepare a maintainable workflow for future versioned APK distribution.

Requirements:

- Prefer immutable, version-specific release assets.
- Never automatically select an arbitrary latest workflow artifact.
- Never automatically publish an APK from a development branch.
- Verify the exact approved file and SHA-256.
- Ensure download links point to the intended approved release.
- Prevent accidental distribution of debug or unsigned builds.
- Document required signing and version consistency checks.
- Avoid placing large APK binaries directly into the website repository.

Do not create or upload a real public APK release during this task.

Do not configure workflows that automatically publish future Android builds.

If a release workflow is needed, prepare it in a safe, disabled/manual form with explicit authorization gates, without changing unrelated repositories.

## 7. Installation and Updating Documentation

Prepare a user-friendly Russian installation guide covering:

- Downloading the APK from the official website.
- Granting installation permission to the selected source when prompted.
- Installing the application.
- Updating an existing beta installation.
- Common installation problems.
- How to check APK integrity.
- How to report a problem.

Explain that successful installation over an existing version depends on compatible application identity, signing, and versioning.

Do not promise automatic updates.

Do not claim user data will always survive upgrades unless the relevant behavior has been verified.

Do not add an in-app update mechanism to the Android repository.

## 8. Beta Feedback

Prepare a clear feedback entry point.

Prefer an existing verified project contact channel.

Possible future feedback categories:

- Application crashes.
- Incorrect calculations.
- Interface defects.
- Installation problems.
- Data loss or corruption.
- Feature suggestions.

Do not invent support email addresses or Telegram bots.

Do not introduce user registration, analytics, tracking, or collection of personal data without separate approval.

If a public issue-reporting channel is unsuitable or not yet configured, present a safe placeholder and document the missing owner decision.

## 9. Main Website Integration

Prepare the main page to support future beta availability.

When downloads are disabled:

- Preserve the existing coming-soon presentation.
- Keep all APK buttons inactive or absent.
- Do not imply public beta access.

When a beta is explicitly approved:

- Allow the hero to link to the download page.
- Show an accurate beta status.
- Present the approved version.
- Provide a clear path to installation instructions.

Ensure the main page and download page use the same release metadata.

Avoid duplicated hardcoded version information.

## 10. Visual and UX Requirements

Preserve the existing Phase 2 design and comprehensive FAQ.

Implement:

- Responsive layouts from 320 px to desktop.
- Light and dark themes.
- Clear visual distinction between unavailable and available states.
- Accessible buttons and links.
- Keyboard navigation.
- Visible focus indicators.
- Semantic markup.
- Reduced-motion support.
- No horizontal overflow.
- Graceful failure if release metadata is missing or invalid.
- Correct handling of long version names and release notes.

Use the existing approved cat mascot and visual assets.

Do not start the postponed full redesign.

## 11. Security and Release Safety

Mandatory safeguards:

- APK downloads remain disabled by default.
- No APK is added to the repository or public artifact.
- No unapproved release URLs are exposed as active downloads.
- Existing privacy and legal content remains unchanged.
- Existing `noindex` policy remains unchanged.
- No production deployment.
- No changes to `main`.
- No changes to the Android or Windows repositories.
- No unrelated GitHub Actions modifications.
- No automatic public release creation.
- No automatic APK publication.

Use isolated test fixtures to verify the future approved-beta state.

Test both the disabled and enabled states without enabling production downloads.

## 12. Verification

Run appropriate automated and browser tests.

At minimum, verify:

1. Default downloads-disabled state.
2. Fully configured approved-beta fixture.
3. Missing approval rejection.
4. Invalid metadata rejection.
5. Missing checksum rejection.
6. Missing or invalid APK URL rejection.
7. Mismatched APK checksum rejection when the artifact is available to the verifier.
8. Correct version display.
9. Correct release notes rendering.
10. Safe handling of external links.
11. Responsive download page.
12. Light and dark themes.
13. Accessibility.
14. Keyboard navigation.
15. Existing Phase 2 and FAQ regressions.
16. Preservation of production release gates.
17. Absence of APK binaries in public preview artifacts.

Do not treat a simulated APK fixture as evidence that a real Android build is release-ready.

## 13. Review Package

Produce a complete owner review package containing:

- Proposed beta distribution architecture.
- New download page screenshots.
- Unavailable-beta state.
- Simulated approved-beta state, clearly marked as a test fixture.
- Mobile and desktop views.
- Light and dark themes.
- Release metadata schema.
- Installation guide.
- Future APK approval procedure.
- Required signing and version verification steps.
- Regression and security test results.
- Exact development SHA.
- List of remaining owner decisions.

Prepare a reproducible local preview or verified review artifact.

Do not invent a public preview URL.

## 14. Documentation and Handoff

Update the relevant existing documents:

- Implementation progress.
- Agent handoff.
- Release instructions.
- APK readiness documentation.
- Phase 3 review package.

Document a precise future release procedure that another coding agent can execute after receiving explicit authorization and a verified APK.

Commit and push verified changes to `work/website-v2`.

Confirm the remote SHA.

Send the standard Russian Telegram development report.

## 15. Completion Conditions

This task is complete when:

- The future beta download interface is implemented.
- The default state is safely disabled.
- The approved-beta state works with isolated test data.
- The release configuration is validated.
- The future APK publication procedure is documented.
- The existing FAQ and Phase 2 features remain intact.
- All relevant tests pass.
- A complete visual review package is available.

**STOP before production publication.**

Do not request an actual APK as a prerequisite for completing this preparation work.

Do not enable downloads or publish the beta.

## Final Report — Russian

Report:

1. Сделано
2. Архитектура распространения APK
3. Страница скачивания
4. Управление версиями и релизами
5. Инструкция установки
6. Механизм обратной связи
7. Проверки безопасности
8. Скриншоты для приёмки
9. Development SHA
10. Production SHA — unchanged
11. Что потребуется для первой реальной беты
12. Что требуется утвердить

Execute the authorized Phase 3 preparation autonomously, preserve the completed FAQ and Phase 2 work, and stop before production deployment.