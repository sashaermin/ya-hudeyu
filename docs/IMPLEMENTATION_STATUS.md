# Website v1.2 verification

The design and release-state update follows the approved Android v1.2 package and the implementation at [`c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8`](https://github.com/sashaermin/ya-hudeyu-android/commit/c6ffc1f31e793dd7ac3c64bcbbb000fe929b26f8). The tracked APK manifest is empty and the support email is unset.

## Brand and Android source comparison

- The header, footer and social card use Playfair Display Bold with the curved measuring tape from `HudeyuWordmark.kt`. Android draws it in Compose Canvas, so the website uses live text and an SVG port of the same path, violet edge, yellow gradient and unnumbered ticks. The site favicon combines the Android `mipmap-xxxhdpi` launcher foreground with its approved gradient and a web mask.
- The six feature WebPs and three mascot WebPs are byte-identical to Android's `ds_icon_*` and `ds_mascot_*` resources. The existing Playfair and Manrope 400/600 fonts match sampled Android glyph outlines and advances. The site now also serves the Android Manrope 700 font as WOFF2.
- Light and dark backgrounds, surfaces, divider, text and focus colours follow `HudeyuTokens.kt`. Cards, round controls and the main action use the app's design roles adapted for the web. The buttons use the approved darker violet for text contrast.
- The design package's D-19 direction and `TodayScreen.kt` put the mascot above the goal rings. The approved reference directory still contains the earlier Today mockup. The site shows the canonical mascot on the landing page and labels the retained Today gallery image as an early mockup. The gallery awaits approved, current app screenshots.
- The privacy and FAQ copy were checked against `HelpContent.kt`, `MoreScreen.kt`, `TransferScreen.kt`, `BackupManager.kt`, `CloudBackupManager.kt`, `CloudSyncManager.kt`, `AssistantScreen.kt`, the Android manifest and build configuration. They cover local storage, file restore and its safety copy, direct transfer, optional Google Drive, Health Connect permissions, online product lookups, maps and Android speech recognition.
- The installation guide uses two Russian Android 14 settings images from [capture run 43012180362](https://github.com/sashaermin/ya-hudeyu/actions/runs/43012180362). The two published WebPs were converted from the 720 × 1280 artifact PNGs. The guide notes that settings labels and placement may differ by device. The Android source declares `minSdk = 26` (Android 8.0).

## Targeted browser verification

- Playwright with headless Chromium 143.0.7499.0 passed 24 route, width and theme combinations at 320, 375, 768 and 1440 px. Checks covered reflow, font and image loading, wordmark bounds, 44 px header targets and gallery labels. At 375 px the header measured 93 px versus 143 px previously. The homepage hero measured 410 px versus 1,107 px, and the first feature card measured 106 px versus 224 px.
- Twelve axe-core 4.11.1 scans at 375 and 1440 px found zero WCAG 2.0/2.1 A/AA violations. Keyboard checks covered the skip link, mobile navigation and sticky-header anchor offset, gallery open, Escape and focus return, and FAQ disclosure. The theme persisted after reload, and the gallery theme could be selected independently. This covers automated checks and targeted keyboard interactions.
- Twenty-four release-state checks covered eight manifest variants on all three pages. The valid fixture checked unsorted dates and the publisher's order within a day. The empty, invalid and unavailable cases left APK actions hidden. Shared status and link labels update across pages. The home and download pages display the latest APK and metadata when the manifest is valid. The privacy page links to the download page. See the [manifest contract](RELEASES.md).
- [Mobile first-screen renders](renders/v12-polish-mobile.webp) cover all three pages in both themes. [Desktop first-screen renders](renders/v12-polish-desktop.webp) cover the homepage in both themes. The previous 18 full-page renders remain in [the earlier checkpoint](https://github.com/sashaermin/ya-hudeyu/tree/0173d6ca070493d724958b7efd056688ce52ad1e/docs/renders).

## Hosted Lighthouse

Mobile Lighthouse 13.0.3 passed on site source [`fe9e43bee7426c3eeaf2ae40cb2c7d3ca4cfaa56`](https://github.com/sashaermin/ya-hudeyu/commit/fe9e43bee7426c3eeaf2ae40cb2c7d3ca4cfaa56) in [run 43014113058](https://github.com/sashaermin/ya-hudeyu/actions/runs/43014113058). This record update leaves the audited site files identical.

| Page | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Home | 98 | 100 | 100 | 100 |
| Download | 100 | 100 | 100 | 100 |
| Privacy | 100 | 100 | 100 | 100 |

Total blocking time was 0 ms on all three pages. Layout shift was 0 on home and download, and 0.009 on privacy. The [previous Lighthouse run](https://github.com/sashaermin/ya-hudeyu/actions/runs/42997260373/attempts/2) remains linked to the earlier site source.

## Release dependencies

The owner needs to provide the support email and a signed APK with release metadata. Installation and update verification on a device remains pending that build. Approved current app screenshots can replace the gallery mockups when available.
