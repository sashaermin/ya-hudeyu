# Website v1.2 verification

The site follows the approved Android v1.2 package and the implementation at [`c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8`](https://github.com/sashaermin/ya-hudeyu-android/commit/c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8). The tracked APK manifest is empty and the support email is unset.

## Specification review

Reviewed [WEBSITE_TZ.md](https://github.com/sashaermin/ya-hudeyu-android/blob/f0ec9c49e398c036c30ed9851d84b7e57a22948b/consulting/website/WEBSITE_TZ.md) and the [consultation decisions](https://github.com/sashaermin/ya-hudeyu-android/blob/f0ec9c49e398c036c30ed9851d84b7e57a22948b/consulting/website/WEBSITE_CONSULTING.md) at consultation revision `f0ec9c49e398c036c30ed9851d84b7e57a22948b`. Website starting HEAD was `9e958a34f6d0dbcc6d77d9af9257ed8d371c9b57`. The [initial site audit](WEBSITE_AUDIT.md) remains the record of the migration from the old production design.

| Scope | Verified implementation |
| --- | --- |
| §0–1, status and contact | Honest coming-soon and manifest-error states, one support destination from every footer, contextual privacy contact and a prefilled release email draft once an address is configured and the manifest is confirmed empty. |
| §2, design identity | Approved v1.2 assets and tokens in both themes. The landing hero uses the canonical mascot and the gallery labels all five design references. The early Today mockup stays in the gallery pending current approved imagery. |
| §3, pages and flows | Landing page, download guide and changelog, privacy page, and legacy privacy redirect. The landing steps and FAQ cover setting goals, adding food, offline use, Health Connect, backup, restore, transfer and updates. The optional help page is covered by the existing guide and FAQ. |
| §4, quality and metadata | Responsive and accessibility checks, self-hosted assets, distinct descriptions and Open Graph text for each page, canonical URLs, social image, sitemap, robots and SoftwareApplication structured data. |
| §5, process and evidence | Implementation and verification recorded on the review branch. Full-page renders at all required widths and themes are linked below. |

## Brand and Android source comparison

- The header, footer and social card use Playfair Display Bold with the curved measuring tape from `HudeyuWordmark.kt`. Android draws it in Compose Canvas, so the website uses live text and an SVG port of the same path, violet edge, yellow gradient and unnumbered ticks. The site favicon combines the Android `mipmap-xxxhdpi` launcher foreground with its approved gradient and a web mask.
- The six feature WebPs and three mascot WebPs are byte-identical to Android's `ds_icon_*` and `ds_mascot_*` resources. The existing Playfair and Manrope 400/600 fonts match sampled Android glyph outlines and advances. The site now also serves the Android Manrope 700 font as WOFF2.
- Light and dark backgrounds, surfaces, divider, text and focus colours follow `HudeyuTokens.kt`. Cards, round controls and the main action use the app's design roles adapted for the web. The buttons use the approved darker violet for text contrast.
- The design package's D-19 direction and `TodayScreen.kt` put the mascot above the goal rings. The approved reference directory still contains the earlier Today mockup. The site shows the canonical mascot on the landing page and labels the retained Today gallery image as an early mockup. The gallery awaits approved, current app screenshots.
- The privacy and FAQ copy were checked against `HelpContent.kt`, `MoreScreen.kt`, `TransferScreen.kt`, `BackupManager.kt`, `CloudBackupManager.kt`, `CloudSyncManager.kt`, `AssistantScreen.kt`, the Android manifest and build configuration. They cover local storage, file restore and its safety copy, direct transfer, optional Google Drive, Health Connect permissions, online product lookups, maps and Android speech recognition.
- The installation guide uses two Russian Android 14 settings images from [capture run 43012180362](https://github.com/sashaermin/ya-hudeyu/actions/runs/43012180362). The two published WebPs were converted from the 720 × 1280 artifact PNGs. The guide notes that settings labels and placement may differ by device. The Android source declares `minSdk = 26` (Android 8.0).

## Targeted browser verification

- Playwright with headless Chromium 143.0.7499.0 passed 24 route, width and theme combinations at 320, 375, 768 and 1440 px. Checks covered reflow, image and font loading, wordmark bounds, 44 px header targets, and gallery labels. The 375 px header is 93 px high and the hero is 410 px high.
- Twelve axe-core 4.11.1 scans at 375 and 1440 px found zero WCAG 2.0/2.1 A/AA violations. The home scans were also checked with all sections rendered. Seven keyboard checks covered the skip link, mobile navigation, download anchors, support access, gallery open and Escape with focus return, and FAQ disclosure. Theme choice persisted on reload and the gallery could be themed independently. These are automated browser and targeted keyboard checks.
- Thirty checks covered ten release-manifest variants across the three pages. They verified the pre-release state, valid unordered releases and same-day ties, release metadata and changelog, rejection of invalid entries, and distinct errors for unavailable release information and history. Six contact cases used an intercepted script with a synthetic address and verified visibility and the release-email subject. The tracked manifest is empty and the address remains unset.
- The legacy privacy redirect passed browser navigation. Static checks verified 103 local references, anchor targets, canonical metadata, sitemap, robots and the absence of external scripts. The three attribution and licence URLs resolved. Google's Russian Pixel help confirmed the installation settings route.
- [Full-page renders](renders/) cover home, download and privacy at 375, 768 and 1440 px in both themes. All 18 were inspected for layout and completeness. The previous [first-screen review](https://github.com/sashaermin/ya-hudeyu/tree/9e958a34f6d0dbcc6d77d9af9257ed8d371c9b57/docs/renders) and Android emulator captures remain available as historical evidence.

## Hosted Lighthouse

The [previous hosted run](https://github.com/sashaermin/ya-hudeyu/actions/runs/43014113058) passed on `fe9e43bee7426c3eeaf2ae40cb2c7d3ca4cfaa56`, with 98/100/100 performance on home, download and privacy and 100 in each other category. The branch workflow will verify the current site files on push.

## Owner review and release dependencies

- **Support email.** Supply the address to enable contact links. The configuration still uses the placeholder.
- **Signed APK and release metadata.** Provide the signed APK and its [manifest fields](RELEASES.md). Real installation and in-place update testing on Android requires that build. The emulator capture verifies settings screens only.
- **Approved current screenshots or footage.** Approve current v1.2 app screenshots for the gallery. An optional demonstration video requires approved real footage.
- **Owner visual review and approval.** Review the current renders and approve any merge, publication or deployment separately. Browser checks, screenshots and Lighthouse are verification evidence. Owner acceptance is pending.

The independent work in the current scope is complete after the current hosted check is recorded. Release-specific and publication work depends on the inputs and approvals above.
