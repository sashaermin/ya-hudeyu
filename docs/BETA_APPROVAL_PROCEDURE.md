# Первая настоящая бета: будущая процедура

**Сейчас ни APK, ни beta website release не разрешены.** Этот документ — воспроизводимый план после новых явных решений владельца. Не создавать Release, не скачивать произвольный последний artifact и не использовать Android workspace/эмулятор другой сессии. Существующая coming-soon production авторизация уже исполнена, повторно не применима.

1. Владелец выбирает конкретный release-candidate файл и Android source SHA, ожидаемые package/version/minSdk и независимо доверенный signing certificate SHA256. Уточняет будущий exact GitHub tag/asset и release notes/known issues. Не запрашивать приватный ключ/пароли; website не подписывает APK.
2. В отдельной согласованной тестовой среде получить именно этот файл по нормальному HTTPS, не в website Git. Убедиться, что это APK, не login/HTML. Проверить размер и SHA256; сохранить byte receipt вне public artifact. Никаких больших бинарников в репозитории сайта.
3. Заполнить candidate metadata (пока status=unverified, distribution=false) из реального файла. Использовать доверенные Android SDK build-tools. Запустить локально:

   ```sh
   python3 tools/verify_beta_apk.py /secure/path/approved-candidate.apk \
     --metadata /secure/path/candidate-metadata.json \
     --expected-signer-sha256 <independently-approved-certificate-sha256> \
     --apksigner /path/to/build-tools/apksigner \
     --aapt2 /path/to/build-tools/aapt2 \
     --output /secure/path/technical-verification.json
   ```

   Проверяет exact bytes, `apksigner verify --verbose --print-certs`, package/version/minSdk через badging, AndroidManifest flags через xmltree. Отвергает неподписанный/другой signer/debug/testOnly/.nutritiontest/несогласованные версии; unfamiliar manifest/API/multiple signers требуют исследования, не ослабления проверки. Не выполнять tooling из непроверенного APK. JSON — техническое свидетельство, **не разрешение**.
4. Отдельно проверить fresh install и upgrade с поддерживаемой прежней версией: applicationId, совместимая подпись/lineage, versionCode, миграции/сохранность данных. Проверить функции/настоящие обезличенные screenshots/обе темы. Документировать фактические ограничения. Если прежняя установка несовместима, не рекомендовать удалять её без предупреждения о данных. Не обещать автоматические updates или сохранность данных без сценариев.
5. Владелец явно разрешает распространение **точного SHA256**. Только тогда записать approved_for_distribution=true,approval_reference,approval_sha256. Технический status=verified иartifact_verification фиксировать отдельно. Release notes/known_issues — только проверенные; совместимость — из APK, не версии Gradle.
6. Создание/загрузка публичного GitHub Release требует отдельного явного разрешения в Android repository: read-only граница данной задачи этого не позволяет. Уполномоченный владелец/агент размещает version-specific APK. Не включать автоматическую публикацию и не брать workflow artifacts. После загрузки скачать exact asset повторно, сравнить hash/size/signature/manifest с утверждённым файлом; проверить URL/доступ без авторизации. Release asset может быть заменён: до поддержки GitHub immutable releases проверять его повторно перед выпуском; при mismatch остановиться.
7. Подготовить website candidate в work/website-v2 с этими metadata, verified_version features/screens evidence, release_mode=full. Общее website approved=false до нового разрешения. Проверить три permission gates и обе страницы на изолированных fixtures; для реального download-state нужна отдельная approval beta_release по exact artifact SHA. Получить content/visual/legal acceptance, проверить архив/allowlist/отсутствие приватных данных. Не переносить test metadata из tests/beta_fixture.py.
8. Владелец отдельно разрешает публикацию конкретного website candidate; заполнить publication approved/reference и beta_release approved/reference/artifact_sha256. Это не индексационная авторизация: indexing_approved=false сохраняется. Production build всё ещё требует прежние full-release evidence gates. Проверить tests, browser/accessibility, точное содержимое public-only артефакта и живую загрузку реального APK. Разрешение APK не заменяет разрешение main/Pages.
9. Только после явной publication authorization выполнить минимальный public-only выпуск по docs/FIRST_RELEASE.md, сохранив rollback production8fb7bf2/актуального public SHA. Никакого wholesale merge development. Проверить фактические live hashes, /download→/download/, HTTPS, themes/menu/FAQ/privacy/noindex иреальную APKссылку. Закрыть site-approved-android-release только с фактическими доказательствами, не по готовности UI.
10. При ошибке checksum/signature/identity — не публиковать. После будущего выпуска при critical regression действовать по отдельно разрешённому rollback. Деактивация downloads — такой же проверяемый website release, не скрытая дистанционная смена JSON. Записать handoff/remote proof и Telegram report.

Подготовленный сейчас Python verifier тестирован **на изолированных байтах и mock tool output**, не на настоящем APK. Ни реальная подпись, ни установка, ни готовность Android в этой задаче не подтверждаются. Нет нового publishing workflow, backend, ключей или стороннего хостинга.
