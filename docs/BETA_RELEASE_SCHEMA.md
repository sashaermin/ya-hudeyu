# Схема beta-метаданных

Исполняемый валидатор — `tools/beta_release.py`; regression tests — `tests/test_beta_release.py`. Конфигурация одна: `data/release.json`, без копии версии/URL в HTML. Не редактировать public HTML для выпуска. Default: channel=beta,status=unverified,approved_for_distribution=false; неизвестные значения=null,changes/known_issues=[]. В таком состоянии любые черновые версии/URL не выводятся.

| Поле release.json | Требования при активации |
|---|---|
| channel | `beta`; unknown/missing channel у новой beta-конфигурации отклоняется |
| status | `verified` — техническая проверка конкретного APK, не разрешение владельца |
| version / version_code | Непустая versionName / положительный integer versionCode, точно как в APK |
| date | Фактическая дата публикации ISO YYYY-MM-DD |
| url | Только credential-free HTTPS `https://github.com/sashaermin/ya-hudeyu-android/releases/download/<exact-tag>/<exact-file>.apk`, без query/fragment/кодированного пути/latest/debug/unsigned |
| sha256 / size_bytes | 64 lowercase hex / positive integer, по фактическим байтам |
| min_android | Числовая версия Android из проверенного minSdk; сейчас mapping API26–36, неизвестный API блокирует до отдельной проверки |
| source_commit / verification_note | Полный Android SHA40 / фактические доказательства и результаты |
| changes / known_issues | Списки непустых строк; changes непустой, known_issues допускает явно пустой список, не обещает отсутствия ошибок |
| artifact_verification | См. ниже; требуется отдельное техническое свидетельство |
| approved_for_distribution | Только boolean true по явному owner approval |
| approval_reference / approval_sha256 | Ссылка на решение о распространении **именно этого** файла / его SHA256 |

`artifact_verification`: sha256,size_bytes,application_id (com.aleksandr.stepstracker),version_name,version_code,min_sdk,signature_verified=true,debuggable=false,test_only=false,signer_sha256 (доверенный сертификат),evidence (фактическая процедура). SHA/size/version должны совпадать с верхним уровнем. Минимальная Android version должна соответствовать min_sdk. Доверенный fingerprint брать из независимо утверждённого источника; не из самого скачанного APK для самоподтверждения.

В `data/publication.json` сохранены прежние поля approved/approval_reference/release_mode/indexing_approved. Новое `beta_release` содержит отдельные `approved=false`, `approval_reference=null`, `artifact_sha256=null`. Для доступной beta требуются true/reference/точный SHA. Старое разрешение coming-soon не подходит. Для production по-прежнему дополнительно нужны отдельное общее website approval/full mode/features/screens evidence; ни fixture, ни `beta_release.approved` сами этого не обходят. Draft всегда noindex; download page также noindex. Эти поля не являются разрешением агента на push main/deploy.

Невалидные или неполные активируемые metadata останавливают сборку; старый проверенный production остаётся работающим. Никаких «fallback на latest» или частично заполненных ссылок. Для аварийной деактивации подготовить unverified/approved_for_distribution=false и beta_release.approved=false в development; публикация такого изменения требует отдельного разрешения. URL/hash могут оставаться в приватном Git JSON для истории, но не попадут в публичный unavailable HTML.

Legacy full-release test fixture без beta extension сохранён ради проверки прежних release gates. Это не рекомендованный путь для будущей beta и не разрешение использовать legacy generic metadata вместо трёх beta-проверок.
