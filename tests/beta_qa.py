"""Actual local beta UI matrix; approved state is an explicitly marked isolated simulation."""
import argparse
import functools
import http.server
import importlib.util
import json
import shutil
import tempfile
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import beta_fixture
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('beta_builder',ROOT/'tools/build.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass

def run(out,engine,executable):
    out.mkdir(parents=True,exist_ok=True);r=dict(engine=engine,layouts=[],axe=[],nojs=[],errors=[],simulation='TEST ONLY; no APK or owner approval')
    site=json.loads((ROOT/'data/site.json').read_text());release=json.loads((ROOT/'data/release.json').read_text());pub=json.loads((ROOT/'data/publication.json').read_text())
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)/'_site';build.build(root)
        test_release,test_pub=beta_fixture.approved(release,pub)
        page=build.render_download(site,test_release,test_pub)
        # Visible evidence boundary is test-harness-only, never the shipped default page.
        page=page.replace('<main id="main"','<p class="wrap" role="note"><strong>ТЕСТОВЫЙ МАКЕТ — APK не существует, разрешения смоделированы. Не для распространения.</strong></p><main id="main"')
        (root/'fixture').mkdir();(root/'fixture/index.html').write_text(page)
        handler=functools.partial(Quiet,directory=root);server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();base=f'http://127.0.0.1:{server.server_port}/'
        try:
            with sync_playwright() as p:
                opts=dict(headless=True)
                if engine=='chromium':opts.update(executable_path=executable or '/usr/bin/chromium',args=['--no-sandbox'])
                elif executable:opts['executable_path']=executable
                if engine=='firefox':opts['firefox_user_prefs']={'security.sandbox.content.level':0}
                b=getattr(p,engine).launch(**opts);r['version']=b.version
                for state,path in [('unavailable','download/'),('fixture','fixture/')]:
                    for theme in ('light','dark'):
                        for width in (320,360,390,430,768,1024,1440,1920):
                            c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce');page=c.new_page();page.on('pageerror',lambda e:r['errors'].append(str(e)));response=page.goto(base+path);assert response.status==200;page.evaluate('document.fonts.ready')
                            expect(page.locator('html')).to_have_attribute('data-theme',theme)
                            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                            assert page.locator('[data-apk-download]').count()==int(state=='fixture')
                            assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,nofollow'
                            assert page.locator('.beta-cat').evaluate('el=>el.complete&&el.naturalWidth>0')
                            if width<=768:
                                page.locator('#menu-toggle').click();expect(page.locator('#navigation a').first).to_be_focused();page.keyboard.press('Escape');expect(page.locator('#menu-toggle')).to_be_focused()
                            page.locator('.skip').focus();page.keyboard.press('Enter');expect(page.locator('#main')).to_be_focused()
                            first=page.locator('.beta-help summary').first;first.focus();page.keyboard.press('Enter');expect(page.locator('.beta-help details').first).to_have_attribute('open','');page.keyboard.press('Space');expect(page.locator('.beta-help details').first).not_to_have_attribute('open','')
                            if width in (390,1440):
                                page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'));a=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                                r['axe'].append(dict(state=state,theme=theme,width=width,violations=[dict(id=v['id'],impact=v['impact']) for v in a['violations']]))
                                if engine=='chromium':
                                    page.locator('.skip').evaluate('(e)=>e.blur()');page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(out/f'{state}-{width}-{theme}.png'),full_page=True)
                            r['layouts'].append(dict(state=state,theme=theme,width=width,overflow=False,keyboard=True));c.close()
                        # No-JS keeps every guide and release detail available without a script.
                        c=b.new_context(viewport={'width':320,'height':900},color_scheme=theme,java_script_enabled=False);page=c.new_page();page.goto(base+path);page.locator('.beta-help summary').first.click();assert page.locator('.beta-help details').first.get_attribute('open') is not None;assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.locator('[data-apk-download]').count()==int(state=='fixture');r['nojs'].append(dict(state=state,theme=theme,width=320,passed=True));c.close()
                # Persistence across pages and CSS text/spacing stress with a long metadata fixture.
                c=b.new_context(viewport={'width':390,'height':900});page=c.new_page();page.goto(base+'download/');page.evaluate("localStorage.setItem('hudeyu-theme','dark')");page.reload();expect(page.locator('html')).to_have_attribute('data-theme','dark');page.goto(base);expect(page.locator('html')).to_have_attribute('data-theme','dark');c.close()
                test_release['version']='TEST ONLY '+('ОченьДлиннаяВерсияБезПробелов'*8);test_release['artifact_verification']['version_name']=test_release['version'];test_release['changes']=['TEST ONLY '+('ДлинноеПримечаниеБезПробелов'*20)]
                (root/'fixture/index.html').write_text(build.render_download(site,test_release,test_pub))
                r['text_adaptation']=[]
                for theme in ('light','dark'):
                    for width in (320,768,1440):
                        c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme);page=c.new_page();page.goto(base+'fixture/');page.add_style_tag(content='body{font-size:200% !important}p,li,dd,dt{font-size:inherit!important;line-height:1.8!important;letter-spacing:.12em!important;word-spacing:.16em!important}')
                        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');r['text_adaptation'].append(dict(theme=theme,width=width,passed=True));c.close()
                b.close()
        finally:server.shutdown();thread.join();server.server_close()
    (out/'beta-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    assert not r['errors'] and not any(a['violations'] for a in r['axe']),r['axe']
    print(engine,'32 layouts /8 axe /4 noJS /6 long-text PASS')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--engine',default='chromium');p.add_argument('--executable');a=p.parse_args();run(a.out,a.engine,a.executable)
