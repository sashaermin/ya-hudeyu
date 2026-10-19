"""Isolated metadata simulation only: no actual APK, owner approval, or release evidence."""
import copy

def approved(release,publication):
    r=copy.deepcopy(release);p=copy.deepcopy(publication)
    r.update(channel='beta',status='verified',version='TEST ONLY — beta 0.0.0-fixture',version_code=1,date='2026-10-20',
             url='https://github.com/sashaermin/ya-hudeyu-android/releases/download/test-only-beta/test-only.apk',
             size_bytes=1024,sha256='a'*64,min_android='8.0',source_commit='b'*40,verification_note='TEST ONLY — no APK exists',
             changes=['TEST ONLY — пример заметки о выпуске, не реальный продукт.'],known_issues=['TEST ONLY — реальные ограничения пока не проверены.'],
             approved_for_distribution=True,approval_reference='TEST ONLY — isolated fixture, not owner permission',approval_sha256='a'*64)
    r['artifact_verification']=dict(sha256='a'*64,size_bytes=1024,version_name=r['version'],version_code=1,application_id='com.aleksandr.stepstracker',signature_verified=True,debuggable=False,test_only=False,signer_sha256='c'*64,min_sdk=26,evidence='TEST ONLY simulated proof, no real signature')
    p.update(approved=True,approval_reference='TEST ONLY',release_mode='full',indexing_approved=False,
             beta_release=dict(approved=True,approval_reference='TEST ONLY — isolated fixture',artifact_sha256='a'*64))
    return r,p
