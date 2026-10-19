"""Read-only unavailable-beta QA, usable on local candidate or live HTTPS; no fixtures."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]

def run(base,output,executable):
    output.mkdir(parents=True,exist_ok=True)
    r=dict(scope='Actual served unavailable page; no simulated APK state',matrix=[],axe=[],nojs=[],page_errors=[],failed_requests=[])
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path=executable,args=['--no-sandbox']);r['browser_version']=b.version
        for theme in ('light','dark'):
            for width in (320,360,390,430,768,1024,1440,1920):
                c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
                page=c.new_page();page.on('pageerror',lambda e:r['page_errors'].append(str(e)));page.on('requestfailed',lambda q:r['failed_requests'].append(q.url))
                response=page.goto(base+'download');assert response.status==200 and page.url==base+'download/'
                page.evaluate('document.fonts.ready')
                expect(page.locator('html')).to_have_attribute('data-theme',theme)
                assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,nofollow'
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert 'бета ещё не доступна' in page.locator('.beta-status').inner_text().casefold()
                assert page.locator('[data-apk-download]').count()==0
                assert not any('.apk' in href.lower() or '/releases/download/' in href.lower() for href in page.locator('a[href]').evaluate_all('els=>els.map(e=>e.getAttribute("href"))'))
                assert 'TEST ONLY' not in response.text() and 'ТЕСТОВЫЙ МАКЕТ' not in response.text()
                assert page.locator('a[href="/#faq"]').count()>=1 and page.locator('a[href="/privacy.html"]').count()>=1
                for img in page.locator('img:visible').all():
                    img.scroll_into_view_if_needed();img.evaluate('el=>el.decode()')
                if width<=768:
                    page.locator('#menu-toggle').click();expect(page.locator('#navigation a').first).to_be_focused();page.keyboard.press('Escape');expect(page.locator('#menu-toggle')).to_be_focused()
                page.locator('.skip').focus();page.keyboard.press('Enter');expect(page.locator('#main')).to_be_focused()
                for details in page.locator('.beta-help details').all():
                    details.locator('summary').focus();page.keyboard.press('Enter');expect(details).to_have_attribute('open','');page.keyboard.press('Space');expect(details).not_to_have_attribute('open','')
                if width in (390,1440):
                    page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'))
                    report=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    r['axe'].append(dict(width=width,theme=theme,violations=[dict(id=v['id'],impact=v['impact']) for v in report['violations']]))
                    page.evaluate('document.activeElement.blur();window.scrollTo(0,0)');page.screenshot(path=str(output/f'download-{width}-{theme}.png'),full_page=True)
                r['matrix'].append(dict(width=width,theme=theme,unavailable=True,noindex=True,apk_download=False,keyboard=True));c.close()
            for width in (320,390,768):
                c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,java_script_enabled=False)
                page=c.new_page();page.goto(base+'download/');assert page.locator('#navigation a').first.is_visible();page.locator('.beta-help summary').first.click();assert page.locator('.beta-help details').first.get_attribute('open') is not None
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert page.locator('[data-apk-download]').count()==0;r['nojs'].append(dict(width=width,theme=theme,status='PASS'));c.close()
        c=b.new_context();page=c.new_page();page.goto(base+'download/');page.evaluate("localStorage.setItem('hudeyu-theme','dark')");page.reload();expect(page.locator('html')).to_have_attribute('data-theme','dark');page.goto(base);expect(page.locator('html')).to_have_attribute('data-theme','dark');page.goto(base+'privacy.html');expect(page.locator('html')).to_have_attribute('data-theme','dark');c.close();b.close()
    (output/'download-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    assert not r['page_errors'] and not r['failed_requests'] and not any(a['violations'] for a in r['axe']),r
    print('Unavailable download actual page:16layouts/4axe0violations/6noJS/keyboard/shared theme PASS')
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--executable',default='/usr/bin/chromium');a=p.parse_args();run(a.base,a.output,a.executable)
