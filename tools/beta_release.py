"""Strict beta metadata gates; never fetch, publish, or infer an APK."""
from datetime import date
import hashlib
import re
from urllib.parse import urlsplit


def required_text(value, field):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError(f'Invalid beta field: {field}')
    return value


def release_url(value):
    # No mutable latest alias, query/fragment, encoded traversal, credentials or arbitrary hosts.
    if not isinstance(value, str) or not re.fullmatch(
        r'https://github\.com/sashaermin/ya-hudeyu-android/releases/download/[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*\.apk', value):
        raise ValueError('Beta APK URL must be an exact versioned Android GitHub Release asset')
    parts = urlsplit(value).path.split('/')
    if parts[-2].lower() in ('latest', '.', '..') or 'debug' in parts[-1].lower() or 'unsigned' in parts[-1].lower():
        raise ValueError('Mutable, debug or unsigned beta asset URL rejected')
    return value


def validate_metadata(release):
    if release.get('channel') != 'beta':
        raise ValueError('Expected beta release channel')
    if release.get('status') != 'verified':
        if release.get('approved_for_distribution') is not False:
            raise ValueError('Unverified beta must keep distribution disabled')
        return False
    for field in ('version', 'date', 'min_android', 'verification_note'):
        required_text(release.get(field), field)
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',release['date']):
        raise ValueError('Beta date must be YYYY-MM-DD')
    date.fromisoformat(release['date'])
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+)*', release['min_android']):
        raise ValueError('Verified beta Android version must be numeric')
    if type(release.get('version_code')) is not int or release['version_code'] <= 0:
        raise ValueError('Beta version_code must be a positive integer')
    if type(release.get('size_bytes')) is not int or release['size_bytes'] <= 0:
        raise ValueError('Invalid beta size_bytes')
    for field, length in [('sha256',64),('source_commit',40)]:
        if not isinstance(release.get(field), str) or not re.fullmatch('[a-f0-9]{'+str(length)+'}', release[field]):
            raise ValueError(f'Invalid beta {field}')
    release_url(release.get('url'))
    for field in ('changes','known_issues'):
        if not isinstance(release.get(field),list) or (field=='changes' and not release[field]):
            raise ValueError(f'Beta {field} must be an explicit list; release notes required')
        for item in release[field]: required_text(item,field)
    proof=release.get('artifact_verification')
    if not isinstance(proof,dict): raise ValueError('Beta artifact_verification required')
    matches={'sha256':release['sha256'],'size_bytes':release['size_bytes'],
             'version_name':release['version'],'version_code':release['version_code'],
             'application_id':'com.aleksandr.stepstracker'}
    for field,value in matches.items():
        if proof.get(field)!=value or type(proof.get(field)) is not type(value):
            raise ValueError(f'Beta artifact verification mismatch: {field}')
    if proof.get('signature_verified') is not True or proof.get('debuggable') is not False or proof.get('test_only') is not False:
        raise ValueError('Beta must be signed and non-debuggable')
    if not re.fullmatch(r'[a-f0-9]{64}',str(proof.get('signer_sha256',''))):
        raise ValueError('Beta signer SHA-256 required')
    if type(proof.get('min_sdk')) is not int or proof['min_sdk']<1:
        raise ValueError('Verified beta min_sdk required')
    versions={26:'8.0',27:'8.1',28:'9',29:'10',30:'11',31:'12',32:'12.1',33:'13',34:'14',35:'15',36:'16'}
    if versions.get(proof['min_sdk']) != release['min_android']:
        raise ValueError('Beta Android version and verified min_sdk mismatch')
    required_text(proof.get('evidence'),'artifact evidence')
    if release.get('approved_for_distribution') is not True or release.get('approval_sha256')!=release['sha256']:
        raise ValueError('Exact beta artifact owner distribution approval required')
    required_text(release.get('approval_reference'),'distribution approval reference')
    return True


def active(release, publication):
    if not validate_metadata(release): return False
    approval=(publication or {}).get('beta_release',{})
    if not isinstance(approval,dict) or approval.get('approved') is not True or approval.get('artifact_sha256')!=release['sha256']:
        raise ValueError('Separate exact beta website publication approval required')
    required_text(approval.get('approval_reference'),'beta website approval reference')
    return True


def verify_bytes(path, release):
    """Local exact-byte check only; not signing, owner approval, or release readiness."""
    digest=hashlib.sha256();size=0
    with open(path,'rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            digest.update(chunk);size+=len(chunk)
    if digest.hexdigest()!=release.get('sha256') or size!=release.get('size_bytes'):
        raise ValueError('APK SHA-256 or size mismatch')
    return {'sha256':digest.hexdigest(),'size_bytes':size}
