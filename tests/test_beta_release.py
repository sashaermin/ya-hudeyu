import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import test_build
from beta_fixture import approved

ROOT=Path(__file__).resolve().parents[1]
build=test_build.build;beta=build.beta_release
spec=importlib.util.spec_from_file_location('verify_beta_apk',ROOT/'tools/verify_beta_apk.py');verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)

class BetaTests(unittest.TestCase):
    def setUp(self):
        self.site=json.loads((ROOT/'data/site.json').read_text());self.default=json.loads((ROOT/'data/release.json').read_text());self.pub=json.loads((ROOT/'data/publication.json').read_text());self.r,self.p=approved(self.default,self.pub)
    def test_apk_cannot_be_copied_as_public_image(self):
        with self.assertRaisesRegex(ValueError,'no APK binaries'):
            build.asset('assets/screens/disguised.apk')

    def test_default_no_download_no_leaked_metadata(self):
        page=build.render_download(self.site,self.default,self.pub)
        self.assertIn('Бета ещё не доступна',page);self.assertNotIn('data-apk-download',page);self.assertNotIn('releases/download/',page)
        self.assertIn('noindex,nofollow',page);self.assertIn('/#faq',page);self.assertIn('/privacy.html',page)
        self.assertFalse(self.pub['beta_release']['approved']);self.assertFalse(self.default['approved_for_distribution'])
    def test_approved_fixture_metadata_notes_and_escaping(self):
        self.r['changes']=['<script>alert("x")</script> & новая запись']
        page=build.render_download(self.site,self.r,self.p)
        for value in [self.r['version'],self.r['sha256'],'1 024 байт',self.r['date'],'Android 8.0','&lt;script&gt;','rel="noopener noreferrer"','data-apk-download']:
            self.assertIn(value,page)
        self.assertNotIn('<script>alert(',page);self.assertIn('TEST ONLY',page)
        home=build.render(self.site,self.r,publication=self.p);self.assertIn('href="/download/">Android · Бета',home)
    def test_three_permissions_independent_and_exact(self):
        mutations=[('r','status','unverified'),('r','approved_for_distribution',False),('r','approval_reference',''),('r','approval_sha256','d'*64),('r','artifact_verification',None)]
        for obj,key,value in mutations:
            with self.subTest(key=key):
                r=copy.deepcopy(self.r);r[key]=value
                with self.assertRaises(ValueError):build.render_download(self.site,r,self.p)
        for field,value in [('approved',False),('approved','true'),('artifact_sha256','d'*64),('approval_reference','')]:
            p=copy.deepcopy(self.p);p['beta_release'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):build.render_download(self.site,self.r,p)
        with self.assertRaises(ValueError):build.render_download(self.site,self.r,self.pub)
    def test_invalid_fields_and_missing_required_metadata(self):
        for field,value in [('version',''),('version_code',True),('version_code',0),('size_bytes',True),('date','2026-99-01'),('date','20261020'),('date',123),('min_android','unverified'),('sha256',None),('sha256',123),('source_commit',123),('source_commit','bad'),('changes',[]),('changes',['']),('known_issues',None),('channel','latest')]:
            r=copy.deepcopy(self.r);r[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):build.render_download(self.site,r,self.p)
    def test_unsafe_urls_rejected(self):
        for url in [None,'javascript:alert(1)','http://github.com/x.apk','https://example.com/a.apk',self.r['url']+'?x=1',self.r['url']+'#x',self.r['url'].replace('test-only-beta','latest'),self.r['url'].replace('test-only.apk','debug.apk'),self.r['url'].replace('test-only.apk','unsigned.apk'),self.r['url'].replace('test-only.apk','%2e%2e.apk'),'https://github.com/sashaermin/ya-hudeyu-android/releases/latest/download/a.apk']:
            r=dict(self.r,url=url)
            with self.subTest(url=url),self.assertRaises(ValueError):build.render_download(self.site,r,self.p)
    def test_proof_mismatches_rejected(self):
        for key,value in [('sha256','d'*64),('size_bytes',1),('version_name','wrong'),('version_code',2),('application_id','com.aleksandr.stepstracker.nutritiontest'),('signature_verified',False),('debuggable',True),('test_only',True),('signer_sha256','bad'),('min_sdk',35),('evidence','')]:
            r=copy.deepcopy(self.r);r['artifact_verification'][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):build.render_download(self.site,r,self.p)
    def test_production_full_and_comingsoon_gates_preserved(self):
        with self.assertRaisesRegex(ValueError,'Publication blocked'):build.render(self.site,self.r,True,self.p)
        with self.assertRaisesRegex(ValueError,'must not contain an APK'):build.render(self.site,self.r,True,dict(self.p,release_mode='coming-soon'))
        fixture=test_build.BuildTests();fixture.setUp();fixture.ready_fixture();site=fixture.site
        # Existing feature/screens evidence must match exact beta version.
        site['features'][0]['verified_version']=self.r['version'];site['screenshots'][0]['verified_version']=self.r['version']
        self.assertIn('noindex,nofollow',build.render(site,self.r,True,self.p))
        with self.assertRaises(ValueError):build.render(site,self.r,True,dict(self.p,approved=False))
    def test_local_bytes_hash_and_size_mismatch(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'test.apk';path.write_bytes(b'NOT AN APK test bytes')
            r=dict(self.r,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size_bytes=path.stat().st_size)
            self.assertEqual(beta.verify_bytes(path,r)['size_bytes'],path.stat().st_size)
            for wrong in [dict(r,sha256='d'*64),dict(r,size_bytes=1)]:
                with self.assertRaises(ValueError):beta.verify_bytes(path,wrong)
    def apk_simulation(self,path,r,**overrides):
        outputs=['Signer #1 certificate SHA-256 digest: '+'c'*64, f"package: name='com.aleksandr.stepstracker' versionCode='{r['version_code']}' versionName='{r['version']}'\nsdkVersion:'26'\n",'E: manifest\n E: application\n']
        for i,text in overrides.items():outputs[int(i)]=text
        return [subprocess.CompletedProcess([],0,stdout=x,stderr='') for x in outputs]
    def test_local_verifier_tools_mocked_signed_manifest_checks(self):
        # Tool output simulation only. No genuine APK tested or approved.
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'test.apk';path.write_bytes(b'fixture');r=dict(self.r,sha256=hashlib.sha256(b'fixture').hexdigest(),size_bytes=7)
            with patch.object(verifier.subprocess,'run',side_effect=self.apk_simulation(path,r)):
                proof=verifier.inspect_apk(path,r,'c'*64);self.assertFalse(proof['debuggable']);self.assertEqual(proof['version_code'],1)
            for changes in [{'0':'Signer #1 certificate SHA-256 digest: '+'d'*64},{'1':"package: name='other.app' versionCode='1' versionName='test'\nsdkVersion:'26'"},{'2':'E: manifest\n E: application\n A: android:debuggable(0x0101000f)=(type 0x12)0xffffffff'},{'2':'E: manifest\n E: application\n A: android:testOnly(0x01010272)=@0x7f000001'}]:
                with patch.object(verifier.subprocess,'run',side_effect=self.apk_simulation(path,r,**changes)),self.assertRaises(ValueError):verifier.inspect_apk(path,r,'c'*64)
            with patch.object(verifier.subprocess,'run',side_effect=subprocess.CalledProcessError(1,'apksigner')),self.assertRaises(subprocess.CalledProcessError):verifier.inspect_apk(path,r,'c'*64)
    def test_pending_beta_never_exposes_candidate_url(self):
        r=dict(self.default,url=self.r['url'],version=self.r['version'],sha256='a'*64)
        page=build.render_download(self.site,r,self.pub);self.assertNotIn(self.r['url'],page);self.assertNotIn(self.r['version'],page)
