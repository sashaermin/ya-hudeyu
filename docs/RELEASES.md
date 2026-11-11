# Release manifest

`releases.json` is an array ordered newest first. Keep it empty until an APK is published. Each entry uses `version`, `url` (HTTPS), `size`, `date`, `android`, `sha256` and `changes` (array of strings). APKs belong in GitHub Releases, not this repository. Example shape (do not publish as a release):

```json
{"version":"1.0","url":"https://example.com/app.apk","size":"25 MB","date":"2026-01-01","android":"8.0+","sha256":"...","changes":["First release"]}
```

Set `CONTACT_EMAIL` in `scripts/v12.js` when the owner provides the address. Until then contact links are unavailable.
