# PRODUCTION RELEASE AUTHORIZATION — Android Preview Gallery

Repository: `sashaermin/ya-hudeyu`
Development branch: `work/website-v2`
Production website: `https://yahudeyu-app.ru/`

## Explicit Owner Authorization

The owner explicitly approves publishing the completed Android preview gallery to the live production website.

This authorization covers ONE production release of the previously completed and verified 11-image gallery.

No additional owner confirmation is required for this specific release, provided the verified content and mandatory restrictions remain unchanged.

## 1. Restore and verify project state

Read all project instructions, including:

- `AGENTS.md`
- `AGENT_DEVELOPMENT_PROTOCOL.md`
- `AGENT_HANDOFF.md`
- `IMPLEMENTATION_PROGRESS.md`
- `docs/ANDROID_PREVIEW_GALLERY_REVIEW.md`
- Existing production release and rollback procedures.

Fetch current remote branches and verify the latest commits.

Reference development checkpoint:
`c3d8d9f6a659c7e698049af8f27cd50a00b54937`

Reference production checkpoint:
`6810206125ccf72080c8a7aa29072041d5812f0f`

Revalidate both against current remote state. Never overwrite unexpected newer changes.

## 2. Approved release scope

Publish the completed Android preview gallery containing:

- All 11 anonymized demonstration images.
- Five gallery categories.
- Russian screen descriptions.
- Responsive desktop, tablet and mobile layouts.
- Fullscreen image viewer.
- Swipe navigation.
- Keyboard navigation.
- Light and dark theme compatibility.
- Preliminary-interface labels.
- Mandatory disclaimer explaining that images are edited demonstrations, not final application screenshots.

Use the existing reviewed image assets and implementation. Do not regenerate, redesign, or replace them unnecessarily.

## 3. Privacy verification

Before publishing, verify that the public assets contain no identifiable personal information.

Confirm that:

- Personal names and original measurements are removed.
- Medication details and personal reminders are anonymized.
- Real GPS locations and routes are not exposed.
- System notifications and device identifiers are removed.
- EXIF and other sensitive metadata are absent.
- Original private JPEG files are not included.
- Only approved anonymized image assets enter production.

If a privacy-critical issue is found, STOP publication and report it. Do not silently publish altered or unreviewed replacement assets.

## 4. Production release procedure

1. Verify that the owner-approved gallery matches the tested development candidate.
2. Verify the asset inventory and gallery manifest SHA.
3. Preserve the current production state and create a verified rollback checkpoint.
4. Build the website using the existing production build and approval gates.
5. Apply the existing gallery-specific production approval mechanism for this exact reviewed manifest. Do not weaken, bypass, or disable the gate.
6. Produce an exact public-only release manifest.
7. Compare the proposed release against current production.
8. Verify that the changes contain only files necessary for the gallery.
9. Run required tests and security checks.
10. Publish using the established GitHub Pages production mechanism.
11. Wait for the actual deployment result.
12. Verify the live HTTPS website.

Do not merge the development branch wholesale into `main`.

Do not publish internal project files, review documents, raw source screenshots, private data, test fixtures, or development tooling.

## 5. Mandatory restrictions

Preserve:

- Existing Phase 2 content.
- Comprehensive FAQ with 33 questions.
- Existing `/download/` page.
- APK downloads disabled.
- Beta-unavailable state.
- Existing `noindex` and robots policy.
- Privacy policy and legal information.
- Existing CNAME, DNS and HTTPS settings.
- Existing mascot, branding and themes.
- Existing Telegram reporting infrastructure.

Do not:

- Publish an APK.
- Enable beta distribution.
- Change Android or Windows repositories.
- Modify unrelated GitHub workflows.
- Enable search engine indexing.
- Start unrelated feature development.
- Change production hosting infrastructure.

## 6. Post-deployment verification

Verify the real website at `https://yahudeyu-app.ru/`.

Check:

- All 11 gallery images load successfully.
- Images match the approved public asset manifest.
- Five categories and navigation work.
- Fullscreen viewer works.
- Keyboard navigation and Escape work.
- Mobile swipe works.
- Both themes display correctly.
- Russian captions and preliminary-image disclaimer are visible.
- No private source screenshots are accessible.
- The homepage, FAQ and download page remain functional.
- No APK download is available.
- `noindex` remains active.
- Privacy and CNAME are unchanged.
- No internal files or secrets are publicly accessible.
- No critical browser errors or broken resources occur.

Use the existing live production verification workflow and record actual results. Do not substitute local tests for live deployment evidence.

## 7. Rollback

If a critical privacy, security or functional regression is confirmed, perform a safe rollback to the verified pre-release production state.

Do not force-push or rewrite history.

Verify the rollback on the live website and report the incident.

## 8. Documentation and reporting

Update the existing progress, handoff, release evidence and event history.

Record:

- Approved source SHA.
- Gallery manifest SHA.
- Previous production SHA.
- New production SHA.
- Deployment run and status.
- Live verification results.
- Rollback checkpoint.
- Remaining limitations.

Follow the established Telegram notification protocol.

Provide the final report in Russian:

1. Сделано
2. Опубликовано
3. Проверено на действующем сайте
4. Production SHA
5. Rollback SHA
6. Состояние APK и noindex
7. Ошибки и ограничения
8. Что требуется от владельца

## Final instruction

Execute this authorized production release autonomously.

Do not stop after local development, preview generation, or pushing to the development branch.

The task is complete only after successful GitHub Pages deployment and verification of the live website, or after a documented safe stop/rollback if the release cannot be completed.

Do not perform unrelated development.