# Website v1.2 verification

Baseline `b6f790c00233731d18bdc7ae79110684286c9276`. APK manifest remains empty and the support email is unset.

## Android source and design comparison

Reviewed the Android design package and source at `fffcc56603b6f93b00a29ebcd34defc885dfd1c8`.

- Design: light blush and dark indigo surfaces, violet actions, Playfair Display headings, Manrope body text, and matching geometry in both themes. Compared the site hero and gallery with the approved paired app mockups. The artwork uses the canonical mascot, soft 3D feature icons and launcher foreground/gradient. Gallery images are explicitly labelled «макет». Primary controls use the dark violet from the design palette behind white labels for contrast.
- FAQ and feature claims: `ui/more/HelpContent.kt`, `nutrition/FoodSearch.kt`, `nutrition/OpenFoodFactsClient.kt`, `trackers/WaterTrackerStore.kt`, `location/WorkoutTrackingService.kt`, `ui/medication/MedicationScreen.kt` and `assistant/AssistantParser.kt` distinguish offline logging from online lookups, optional sync and GPS permissions. The progress description uses the app FAQ's forecast language.
- Privacy: `AndroidManifest.xml`, `backup/BackupManager.kt`, `sync/CloudSyncManager.kt`, `sync/CloudBackupManager.kt` and the in-app help support local storage, optional Google Drive, file copies, transfer and user-controlled Health Connect permissions. The site also discloses the optional Android speech service and online lookups, including USDA FoodData Central when a build configures its key. This was a source review of the Android app. No device acceptance was performed.
- Installation text was compared with [Google's Pixel help](https://support.google.com/pixelphone/answer/7391672?hl=ru). Actual Android installation screenshots still require an Android device or emulator and a signed APK. The web renders cover the text guide.

## Browser verification

Headless Chromium 143 and Playwright rendered all three pages at 375, 768 and 1440 px in both themes. [Full-page renders](renders/) include the download guide. All 24 route, width and theme combinations (including 320 px) passed the reflow, image and font checks. Twelve axe scans at 375 and 1440 px reported zero WCAG A/AA violations. Keyboard checks covered the skip link, gallery open, Escape and focus return, and FAQ disclosure. The theme switch persisted after reload. This is targeted WCAG verification, not a full assistive technology audit.

The empty manifest hid APK actions on both entry points. An intercepted four-release fixture exposed the latest APK and metadata, three homepage entries and the full download history. Malformed entries, non-HTTPS URLs and an unavailable manifest left APK actions hidden. No fixture was committed to `releases.json`.

Lighthouse 13.0.3 ran mobile audits on a local static server. Categories are scored out of 100.

| Page | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Home | 99 | 100 | 100 | 100 |
| Download | Unscored | 100 | 100 | 100 |
| Privacy | Unstable | 100 | 100 | 100 |

The subpage audits repeatedly reported `NO_SCREENSHOTS` in the performance trace, including on fresh browser sessions. An initial privacy trace measured 74 with high blocking time while renders were running. The ≥90 mobile performance target is confirmed only for the home page. The missing Android device screenshots and a stable subpage performance run remain open.
