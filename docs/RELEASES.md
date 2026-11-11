# Release manifest

`releases.json` is an array ordered newest first. Keep it empty until an official signed APK is published to GitHub Releases. Each entry requires `version`, `url` (HTTPS link to the `.apk` asset), `size` (with units), `date` (`YYYY-MM-DD`), `android` (minimum supported Android version), `sha256` (64 hexadecimal characters from the APK), and `changes` (array of Russian strings). An invalid or unavailable manifest leaves the APK action hidden. The homepage shows the latest three entries and `/download/` shows the full history.

Set `CONTACT_EMAIL` in `scripts/v12.js` when the owner provides the address. The site displays contact availability text until then.
