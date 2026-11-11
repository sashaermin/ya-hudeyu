# Release manifest

`releases.json` is an array. Keep it empty until an official signed APK is published to GitHub Releases. Each entry requires `version` (unique after trimming whitespace), `url` (HTTPS link to the `.apk` asset), `size` (with units), `date` (valid calendar date in `YYYY-MM-DD`), `android` (minimum supported Android version), `sha256` (64 hexadecimal characters from the APK), and `changes` (array of Russian strings).

The latest release has the most recent date. For releases on the same date, put the newer release first in the manifest. The site sorts by date descending and preserves the authored order within a date. The homepage shows the latest three entries, and `/download/` shows the full history.

An empty array displays the coming-soon state. An invalid or unavailable manifest displays a status error. Both states keep APK actions hidden. A valid nonempty manifest updates the shared release labels on all three pages and displays APK details and download actions on the home and download pages.

Set `CONTACT_EMAIL` in `scripts/v12.js` when the owner provides the address. The support and privacy contacts then open an email draft. The download page also offers a prefilled release-notification email when the manifest is confirmed empty.
