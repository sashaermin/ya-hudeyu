# Release manifest

`releases.json` is an array. Keep it empty until an official signed APK is published to GitHub Releases. Each entry requires `version` (unique after trimming whitespace), `url` (HTTPS link to the `.apk` asset), `size` (with units), `date` (valid calendar date in `YYYY-MM-DD`), `android` (minimum supported Android version), `sha256` (64 hexadecimal characters from the APK), and `changes` (array of Russian strings).

The latest release has the most recent date. For releases on the same date, put the newer release first in the manifest. The site sorts by date descending and preserves the authored order within a date. The homepage shows the latest three entries, and `/download/` shows the full history.

An empty array displays the coming-soon state. An invalid or unavailable manifest displays a status error. Both states keep APK actions hidden. A valid nonempty manifest updates the shared release labels on all three pages and displays APK details and download actions on the home and download pages.

The support address is set once in `CONTACT_EMAIL` in `scripts/v12.js`. Support and privacy links open in the visitor's email application. The bug-report link pre-fills a draft, and the visitor can attach screenshots and send it there. The download page also offers a prefilled release-notification email when the manifest is confirmed empty.
