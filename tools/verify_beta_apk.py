#!/usr/bin/env python3
"""Read-only local APK byte/manifest/signature verifier. Never approves or uploads."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import beta_release

ANDROID_VERSIONS={26:'8.0',27:'8.1',28:'9',29:'10',30:'11',31:'12',32:'12.1',33:'13',34:'14',35:'15',36:'16'}


def inspect_apk(path, release, trusted_signer, apksigner='apksigner', aapt2='aapt2'):
    if not re.fullmatch(r'[a-f0-9]{64}',trusted_signer): raise ValueError('Expected independently trusted signer SHA-256')
    if Path(path).is_symlink() or Path(path).suffix.lower()!='.apk': raise ValueError('Expected local regular APK, not symlink')
    result=beta_release.verify_bytes(path,release)
    # check=True rejects invalid signatures. Tools are Android SDK build-tools, never a shell string.
    certs=subprocess.run([apksigner,'verify','--verbose','--print-certs',str(path)],check=True,text=True,capture_output=True).stdout
    signers=re.findall(r'^Signer #\d+ certificate SHA-256 digest: ([a-fA-F0-9]{64})$',certs,re.M)
    if len(signers)!=1 or signers[0].lower()!=trusted_signer:
        raise ValueError('APK signer differs from independently trusted certificate, or multiple signers require review')
    badging=subprocess.run([aapt2,'dump','badging',str(path)],check=True,text=True,capture_output=True).stdout
    package=re.search(r"^package: name='([^']+)' versionCode='([0-9]+)' versionName='([^']+)'",badging,re.M)
    sdk=re.search(r"^sdkVersion:'([0-9]+)'",badging,re.M)
    if not package or not sdk: raise ValueError('APK manifest metadata missing')
    app_id,code,name=package.groups();min_sdk=int(sdk[1])
    if (app_id,name,int(code))!=('com.aleksandr.stepstracker',release.get('version'),release.get('version_code')):
        raise ValueError('APK identity/version mismatch')
    if ANDROID_VERSIONS.get(min_sdk)!=release.get('min_android'):
        raise ValueError('APK minSdk does not match the documented Android version; unknown API requires review')
    tree=subprocess.run([aapt2,'dump','xmltree',str(path),'--file','AndroidManifest.xml'],check=True,text=True,capture_output=True).stdout
    if 'E: manifest' not in tree or 'E: application' not in tree:
        raise ValueError('Cannot verify application manifest flags')
    # Absent attributes default false. Present attributes must be explicit false, no resource reference.
    flags=re.findall(r'A: android:(debuggable|testOnly)[^=]*=(.*)',tree)
    for flag,value in flags:
        if not re.fullmatch(r'\(type 0x12\)0x0|false',value.strip()):
            raise ValueError(f'APK {flag} flag is enabled or cannot be verified')
    if 'application-debuggable' in badging: raise ValueError('Debug APK rejected')
    result.update(application_id=app_id,version_name=name,version_code=int(code),min_sdk=min_sdk,
                  signature_verified=True,debuggable=False,test_only=False,signer_sha256=trusted_signer,
                  evidence='Local apksigner verify --verbose --print-certs; aapt2 dump badging and AndroidManifest.xml xmltree; exact bytes verified')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('apk',type=Path);p.add_argument('--metadata',type=Path,required=True);p.add_argument('--expected-signer-sha256',required=True);p.add_argument('--apksigner',default='apksigner');p.add_argument('--aapt2',default='aapt2');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try: result=inspect_apk(a.apk,json.loads(a.metadata.read_text()),a.expected_signer_sha256,a.apksigner,a.aapt2)
    except (ValueError,subprocess.CalledProcessError,OSError) as error: p.exit(1,f'APK verification rejected: {type(error).__name__}; inspect local tools/file/metadata, no approval granted\n')
    a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('Technical evidence written; distribution and website approval remain separate.')
