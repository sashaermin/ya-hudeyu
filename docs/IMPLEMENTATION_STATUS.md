# Website v1.2 verification

The site follows the approved Android v1.2 package and the implementation at [`c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8`](https://github.com/sashaermin/ya-hudeyu-android/commit/c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8). The tracked APK manifest is empty. The working branch configures the owner-provided support address in `CONTACT_EMAIL`.

## Specification review

Reviewed [WEBSITE_TZ.md](https://github.com/sashaermin/ya-hudeyu-android/blob/f0ec9c49e398c036c30ed9851d84b7e57a22948b/consulting/website/WEBSITE_TZ.md) and the [consultation decisions](https://github.com/sashaermin/ya-hudeyu-android/blob/f0ec9c49e398c036c30ed9851d84b7e57a22948b/consulting/website/WEBSITE_CONSULTING.md) at consultation revision `f0ec9c49e398c036c30ed9851d84b7e57a22948b`. Website starting HEAD was `9e958a34f6d0dbcc6d77d9af9257ed8d371c9b57`. The [initial site audit](WEBSITE_AUDIT.md) remains the record of the migration from the old production design.

| Scope | Verified implementation |
| --- | --- |
| §0–1, status and contact | «О загрузке» and «Скоро для Android» before release, distinct manifest errors, one support destination from every footer, contextual privacy contact and a prefilled release email draft once an address is configured and the manifest is confirmed empty. |
| §2, design identity | Approved v1.2 assets and tokens in both themes. The landing hero uses the canonical mascot and the gallery labels all five design references. The early Today mockup stays in the gallery pending current approved imagery. |
| §3, pages and flows | Landing page, dedicated features guide, download guide and changelog, privacy page, and legacy privacy redirect. The FAQ retains setup and troubleshooting guidance. |
| §4, quality and metadata | Responsive and accessibility checks, self-hosted assets, distinct descriptions and Open Graph text for each page, canonical URLs, social image, sitemap, robots and SoftwareApplication structured data. |
| §5, process and evidence | Implementation and verification recorded on the review branch. Full-page renders at all required widths and themes are linked below. |

## Brand and Android source comparison

- The header, footer and social card use Playfair Display Bold with the curved measuring tape from `HudeyuWordmark.kt`. Android draws it in Compose Canvas, so the website uses live text and an SVG port of the same path, violet edge, yellow gradient and unnumbered ticks. The site favicon combines the Android `mipmap-xxxhdpi` launcher foreground with its approved gradient and a web mask.
- The six feature WebPs and three mascot WebPs are byte-identical to Android's `ds_icon_*` and `ds_mascot_*` resources. The existing Playfair and Manrope 400/600 fonts match sampled Android glyph outlines and advances. The site now also serves the Android Manrope 700 font as WOFF2.
- Light and dark backgrounds, surfaces, divider, text and focus colours follow `HudeyuTokens.kt`. Cards, round controls and the main action use the app's design roles adapted for the web. The buttons use the approved darker violet for text contrast.
- The design package's D-19 direction and `TodayScreen.kt` put the mascot above the goal rings. The approved reference directory still contains the earlier Today mockup. The site shows the canonical mascot on the landing page and labels the retained Today gallery image as an early mockup. The gallery awaits approved, current app screenshots.
- The content was checked against `HelpContent.kt`, `AboutScreen.kt`, `MoreScreen.kt`, `NutritionAddActionGroups.kt`, `MedicationScreen.kt`, `TransferScreen.kt`, `BackupManager.kt`, `CloudBackupManager.kt`, `CloudSyncManager.kt`, `AssistantScreen.kt`, the Android manifest and build configuration. This was a source review of the product copy and privacy disclosures.
- The installation guide uses two Russian Android 14 settings images from [capture run 43012180362](https://github.com/sashaermin/ya-hudeyu/actions/runs/43012180362). The two published WebPs were converted from the 720 × 1280 artifact PNGs. The guide notes that settings labels and placement may differ by device. The Android source declares `minSdk = 26` (Android 8.0).

## Targeted browser verification

- Playwright with headless Chromium 143.0.7499.0 passed 24 route, width and theme combinations at 320, 375, 768 and 1440 px. Checks covered reflow, image and font loading, wordmark bounds, 44 px header targets, and gallery labels. The 375 px header is 93 px high and the hero is 410 px high.
- Twelve axe-core 4.11.1 scans at 375 and 1440 px found zero WCAG 2.0/2.1 A/AA violations. The home scans were also checked with all sections rendered. Seven keyboard checks covered the skip link, mobile navigation, download anchors, support access, gallery open and Escape with focus return, and FAQ disclosure. Follow-up checks confirmed that the skip link advances keyboard focus into the main content on all three pages. Theme choice persisted on reload and the gallery could be themed independently. These are automated browser and targeted keyboard checks.
- Thirty checks covered ten release-manifest variants across the three pages. They verified the pre-release state, valid unordered releases and same-day ties, release metadata and changelog, rejection of invalid entries, and distinct errors for unavailable release information and history. Six contact cases used an intercepted script with a synthetic address and verified visibility and the release-email subject before the support address was configured.
- The legacy privacy redirect passed browser navigation. Static checks verified 103 local references, anchor targets, canonical metadata, sitemap, robots and the absence of external scripts. The three attribution and licence URLs resolved. Google's Russian Pixel help confirmed the installation settings route.
- [Full-page renders](renders/) cover home, download and privacy at 375, 768 and 1440 px in both themes. All 18 were inspected for layout and completeness on `e512fc88e0cfd742f4df2de60de63539f035cebf` before the navigation wording update. The previous [first-screen review](https://github.com/sashaermin/ya-hudeyu/tree/9e958a34f6d0dbcc6d77d9af9257ed8d371c9b57/docs/renders) and Android emulator captures remain available as historical evidence.

### Navigation and wording

- «Экраны приложения» names the gallery in the shared menu and the page heading. The introduction identifies the images as mockups and explains that the finished app may look different. The early Today caption remains visible.
- Shared navigation and headings use direct destination labels. The installation and version history links, release status links, support and privacy labels, and release email wording were reviewed across the three pages. A genuine release remains required for the APK action.
- On narrow screens, the navigation uses a flex row with wider targets for the longer labels. The header remained 93 px high at 320 and 375 px, with targets at least 44 × 44 px. Header captures at 320 and 1440 px were visually inspected in both themes.
- Playwright passed 24 responsive checks, 48 keyboard activations of the four main links across all three pages at 375 and 1440 px in both themes, and the legacy privacy redirect. Each activation revealed its destination heading below the sticky header. Twelve axe scans reported zero WCAG 2.0/2.1 A/AA violations. Gallery and FAQ keyboard checks, theme persistence, 30 release-state cases and six contact cases also passed. Static checks confirmed 62 local links and anchor destinations.

### Features guide

The homepage overview and its `/#features` anchor remain available. The main menu and a link in that overview open [the dedicated guide](../features/), which has six jump links and shares the site's cards, typography, and light and dark themes. The guide uses text and the existing site branding. The labelled mockups remain in the gallery.

The guide's claim sources were reviewed at the pinned Android revision above and checked against the newer [Android HEAD `9d0cd8e69f511cf60f6d92d60f03fb2bdee3ba47`](https://github.com/sashaermin/ya-hudeyu-android/commit/9d0cd8e69f511cf60f6d92d60f03fb2bdee3ba47). The only Kotlin change between them was an icon import in the shared theme components. This was source verification. Release-device testing remains pending.

| Topic | Source checked |
| --- | --- |
| Food and water | `NutritionScreen.kt`, `NutritionV12.kt`, `NutritionAddActionGroups.kt`, `HelpContent.kt`, `WaterTrackerStore.kt` for meals, portions, calories and macros, search and manual entry, and daily water goals. |
| Activity | `HelpContent.kt`, `ManualWorkoutTracker.kt`, `WorkoutEntity.kt`, `WorkoutTrackingService.kt` and `MoreScreen.kt` for step sources, workouts, outdoor routes with location permission, and optional Bluetooth heart rate. |
| Progress | `WeightScreen.kt`, `BodyMeasurementsScreen.kt`, `WeightLossPlanScreen.kt` and `HelpContent.kt` for charts, measurements, weight-goal modes and the estimated time to a weight-loss goal. |
| Health | `SleepVitalsScreen.kt`, `MedicationScreen.kt` and `MoodCard.kt` for manual and imported sleep, medication records and reminders, and mood, energy and daily notes. |
| Assistant | `AssistantScreen.kt` for local text commands, opening sections, reading totals and preparing a weight entry for confirmation. |
| Data and privacy | `HelpContent.kt`, `BackupManager.kt`, `TransferScreen.kt`, `CloudSyncManager.kt` and `HealthConnectScreen.kt` for offline recording, backup and restore, transfer, and optional integrations. |

Playwright passed 32 route, width and theme checks across the four pages at 320, 375, 768 and 1440 px. At 375 and 1440 px it passed 64 main-menu keyboard activations, 24 guide jump-link activations, and four activations of the homepage guide link. Sixteen axe-core WCAG A/AA scans found zero violations. Forty release-state cases and six contact cases passed. Static verification covered 133 local links and resources, all four canonical sitemap URLs, the original homepage anchor and the empty release manifest. Four guide captures at 375 and 1440 px were visually inspected in both themes.

The branch workflow now includes the guide in its mobile Lighthouse audit.

### Support contacts and bug reports

The homepage support section displays the configured address and offers «Сообщить об ошибке». The action opens a mail draft with prompts for the problem, reproduction steps, device, Android version and app version. The nearby note explains that screenshots can be attached in the mail app. The privacy page opens a draft with a privacy-specific subject. All four footers link to the same support section.

Playwright passed 32 layout checks in both themes across the four pages at 320, 375, 768 and 1440 px, 32 generated mail-link checks, four footer keyboard paths and eight axe WCAG A/AA scans with zero violations. The tests checked empty, populated, invalid and unavailable manifests and the unset-contact fallback. The repository's APK manifest remains empty. Mail links were decoded and checked in the browser. Sending and attachment handling are performed by the visitor's email app.

## Hosted Lighthouse

Mobile Lighthouse 13.0.3 passed on website source [`0f1e3181f21d05ba1f48428d36b7c0c2d5874b10`](https://github.com/sashaermin/ya-hudeyu/commit/0f1e3181f21d05ba1f48428d36b7c0c2d5874b10) in [run 43034485307, attempt 2](https://github.com/sashaermin/ya-hudeyu/actions/runs/43034485307/attempts/2). The subsequent verification-record commit changes only this document.

| Page | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Home | 98 | 100 | 100 | 100 |
| Features | 100 | 100 | 100 | 100 |
| Download | 100 | 100 | 100 | 100 |
| Privacy | 100 | 100 | 100 | 100 |

The guide scored 100 in all categories on both hosted attempts. [Attempt 1](https://github.com/sashaermin/ya-hudeyu/actions/runs/43034485307/attempts/1) measured 78 for home performance and 910 ms total blocking time. On the same commit, attempt 2 measured 98 and 40 ms for home, and 0 ms total blocking time on the other pages. The [navigation audit](https://github.com/sashaermin/ya-hudeyu/actions/runs/43020242740) remains evidence for the previous revision.

## Owner review and release dependencies

- **Support update.** Review and approve publication of the configured address and the email-based bug-report action.
- **Signed APK and release metadata.** Provide the signed APK and its [manifest fields](RELEASES.md). Real installation and in-place update testing on Android requires that build. The emulator capture verifies settings screens only.
- **Approved current screenshots or footage.** Approve current v1.2 app screenshots for the gallery. An optional demonstration video requires approved real footage.
- **Owner visual review and approval.** Review the current renders and approve any merge, publication or deployment separately. Browser checks, screenshots and Lighthouse are verification evidence. Owner acceptance is pending.

Independent work in the current scope is complete. Release-specific and publication work depends on the inputs and approvals above.
