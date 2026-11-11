# Website v1.2 verification

Verified website source [`fc04d52e365be46110b1f7291f3f34d60be9aa69`](https://github.com/sashaermin/ya-hudeyu/commit/fc04d52e365be46110b1f7291f3f34d60be9aa69). The APK manifest is empty and the support email is unset.

## Android source and design comparison

Reviewed the Android design package and source at `fffcc56603b6f93b00a29ebcd34defc885dfd1c8`.

- Design: light blush and dark indigo surfaces, violet actions, Playfair Display headings, Manrope body text, and matching geometry in both themes. Compared the site hero and gallery with the approved paired app mockups. The artwork uses the canonical mascot, soft 3D feature icons and launcher foreground/gradient. Gallery images are explicitly labelled «макет». Primary controls use the dark violet from the design palette behind white labels for contrast.
- FAQ and feature claims: `ui/more/HelpContent.kt`, `nutrition/FoodSearch.kt`, `nutrition/OpenFoodFactsClient.kt`, `trackers/WaterTrackerStore.kt`, `location/WorkoutTrackingService.kt`, `ui/medication/MedicationScreen.kt` and `assistant/AssistantParser.kt` distinguish offline logging from online lookups, optional sync and GPS permissions. The progress description uses the app FAQ's forecast language.
- Privacy: `AndroidManifest.xml`, `backup/BackupManager.kt`, `sync/CloudSyncManager.kt`, `sync/CloudBackupManager.kt` and the in-app help support local storage, optional Google Drive, file copies, transfer and user-controlled Health Connect permissions. The site also discloses the optional Android speech service and online lookups, including USDA FoodData Central when a build configures its key. This was a source review of the Android app. No device acceptance was performed.
- The installation guide follows [Google's Pixel help](https://support.google.com/pixelphone/answer/7391672?hl=ru). The two WebP images match the PNGs from the [Android 14 emulator capture](https://github.com/sashaermin/ya-hudeyu/actions/runs/42996397870). They show the installation source list and the Chrome permission switch in English, with Russian captions. `app/build.gradle.kts` declares `minSdk = 26` (Android 8.0).

## Browser verification

The [18 full-page renders](renders/) cover the home, download and privacy pages at 375, 768 and 1440 px in both themes. They were recovered from local commit `60463eee931434467a3b5a8b969966a0231d6ba9`, whose site files match the verified source. All 18 were checked for their expected widths and reviewed visually, including the installation figures.

Playwright in headless Chromium 143.0.7499.0 passed all 24 route, width and theme combinations, including 320 px, with reflow, image and font checks. Twelve axe-core 4.11.1 scans at 375 and 1440 px found zero WCAG 2.0/2.1 A/AA violations. Keyboard checks passed for the skip link, gallery open, Escape and focus return, and FAQ disclosure. The theme choice persisted after reload, and the gallery theme could be selected independently. Accessibility coverage consists of these automated scans and keyboard checks.

Twelve manifest checks covered six scenarios on the home and download pages. The empty manifest hid APK actions. An intercepted four-release fixture exposed the latest APK and metadata, three homepage entries and the full download history. Invalid dates, an invalid manifest shape, non-HTTPS URLs and an unavailable manifest left APK actions hidden. The tracked `releases.json` remains empty.

Lighthouse 13.0.3 audited the verified source on a local static server in hosted Chrome. The passing [GitHub Actions attempt](https://github.com/sashaermin/ya-hudeyu/actions/runs/42997260373/attempts/2) applies to this documentation and render update because the site files are identical. Categories are scored out of 100.

| Page | Performance | Accessibility | Best practices | SEO |
| --- | ---: | ---: | ---: | ---: |
| Home | 99 | 100 | 100 | 100 |
| Download | 100 | 100 | 100 | 100 |
| Privacy | 100 | 100 | 100 | 100 |

The [first hosted attempt](https://github.com/sashaermin/ya-hudeyu/actions/runs/42997260373/attempts/1) scored 74 for home performance with 1,250 ms total blocking time. The passing attempt measured 0 ms total blocking time and zero layout shift on all three pages. These are lab results for the branch source.

## Release dependencies

The owner needs to provide the support address and a signed APK with its [release metadata](RELEASES.md). Device installation and update verification requires that signed build. The gallery uses labelled design mockups pending approved app screenshots.
