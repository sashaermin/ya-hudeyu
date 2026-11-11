# Website v1.2 verification

Baseline `b6f790c00233731d18bdc7ae79110684286c9276`. APK manifest remains empty and the support email is unset.

## Android source and design comparison

Reviewed the Android design package and source at `fffcc56603b6f93b00a29ebcd34defc885dfd1c8`.

- Design: light blush and dark indigo surfaces, violet actions, Playfair Display headings, Manrope body text, and matching geometry in both themes. Compared the site hero and gallery with the approved paired app mockups. The artwork uses the canonical mascot, soft 3D feature icons and launcher foreground/gradient. Gallery images are explicitly labelled «макет». Button labels use the dark violet from the design palette for contrast.
- FAQ and feature claims: `ui/more/HelpContent.kt`, `nutrition/FoodSearch.kt`, `nutrition/OpenFoodFactsClient.kt`, `trackers/WaterTrackerStore.kt`, `location/WorkoutTrackingService.kt`, `ui/medication/MedicationScreen.kt` and `assistant/AssistantParser.kt` distinguish offline logging from online lookups, optional sync and GPS permissions. The progress description uses the app FAQ's forecast language.
- Privacy: `AndroidManifest.xml`, `backup/BackupManager.kt`, `sync/CloudSyncManager.kt`, `sync/CloudBackupManager.kt` and the in-app help support local storage, optional Google Drive, file copies, transfer and user-controlled Health Connect permissions. The site also discloses the optional Android speech service and online lookups. This was a source review of the Android app. No device acceptance was performed.
- Installation text was compared with [Google's Pixel help](https://support.google.com/pixelphone/answer/7391672?hl=ru). Actual Android installation screenshots still require an Android device or emulator and a signed APK. The web renders cover the text guide.

## Browser verification

Headless Chromium runs in the current environment. Final route renders and audit results will be recorded with the browser verification checkpoint.
