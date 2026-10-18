#!/usr/bin/env python3
"""Chromium functional matrix. Run against the draft server; fixtures never enter _site."""
import argparse
import importlib.util
import json
from pathlib import Path
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (320, 360, 390, 430, 768, 1024, 1440, 1920)


def gallery_fixture():
    spec = importlib.util.spec_from_file_location('site_build', ROOT/'tools/build.py')
    build = importlib.util.module_from_spec(spec); spec.loader.exec_module(build)
    site = json.loads((ROOT/'data/site.json').read_text())
    # Intentional test-only image fixtures: original mascot files, never passed off as Android screens.
    release = dict(status='verified', version='QA-ONLY', date='2026-10-18', url='https://example.com/qa-only.apk', size_bytes=1, sha256='a'*64, min_android='TEST', source_commit='a'*40, verification_note='MOCK TEST ONLY', approved_for_distribution=True, approval_reference='MOCK TEST ONLY')
    site['features'] = [dict(title='QA fixture', description='Not public product content', verified_version='QA-ONLY', evidence='MOCK TEST ONLY')]
    site['screenshots'] = [dict(src='assets/brand/originals/'+name, width=width, height=height, alt='Только тестовый оригинальный маскот', caption='QA fixture '+str(i), verified_version='QA-ONLY', evidence='MOCK TEST ONLY', approved_for_publication=True) for i,(name,width,height) in enumerate([('mascot_calm.webp',440,512),('ic_launcher_green.png',192,192)])]
    return build.render(site, release)


def run(base, output, axe_path, interactions_only=False):
    results = {'matrix':[], 'interactions':[], 'axe':[], 'page_errors':[], 'failed_requests':[]}
    output.mkdir(parents=True,exist_ok=True)
    if interactions_only:
        results = json.loads((output/'browser-results.json').read_text())
        results['interactions'] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        results['browser_version'] = browser.version
        for theme in (() if interactions_only else ('light','dark')):
            for width in WIDTHS:
                context = browser.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
                page=context.new_page()
                page.on('pageerror',lambda error: results['page_errors'].append(str(error)))
                page.on('requestfailed',lambda request: results['failed_requests'].append(request.url))
                response=page.goto(base); assert response.status==200
                page.evaluate('document.fonts.ready')
                assert page.locator('html').get_attribute('data-theme')==theme
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,theme,'overflow')
                # The actual heading, CTA and footer must fit, not merely an overflow-hidden root.
                for selector in ['h1','.hero-actions','.release','.footer-top']:
                    box=page.locator(selector).bounding_box(); assert box['x']>=0 and box['x']+box['width']<=width+.5, (width,theme,selector,box)
                for anchor in page.locator('a[href^="#"]').all():
                    target=anchor.get_attribute('href')[1:]
                    assert page.locator('[id="'+target+'"]').count()==1, target
                assert page.locator('a[href$=".apk"]').count()==0
                if width<=800:
                    toggle=page.locator('#menu-toggle'); toggle.click()
                    assert toggle.get_attribute('aria-expanded')=='true'
                    page.locator('#navigation a').first.focus(); page.keyboard.press('Escape')
                    assert toggle.get_attribute('aria-expanded')=='false'
                    assert toggle.evaluate('(el)=>el===document.activeElement')
                    toggle.click(); page.locator('#navigation a[href="#faq"]').click()
                    assert toggle.get_attribute('aria-expanded')=='false'
                summary=page.locator('summary').first; summary.focus(); page.keyboard.press('Enter')
                assert page.locator('details').first.get_attribute('open') is not None
                page.keyboard.press('Enter')
                assert page.locator('details').first.get_attribute('open') is None
                page.evaluate('scrollTo(0,document.body.scrollHeight)'); page.wait_for_timeout(100)
                page.evaluate('scrollTo(0,0)'); page.wait_for_timeout(100)
                for image in page.locator('img:visible').all():
                    assert image.evaluate('(el)=>el.complete && el.naturalWidth>0'), image.get_attribute('src')
                if width in (390,1440):
                    page.evaluate('document.activeElement.blur()')
                    page.screenshot(path=str(output/f'{width}-{theme}.png'),full_page=True)
                if width in (390,1440) and axe_path:
                    page.add_script_tag(path=axe_path)
                    report=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    results['axe'].append({'width':width,'theme':theme,'axe_version':report['testEngine']['version'],'violations':[{'id':v['id'],'impact':v['impact'],'targets':[n['target'] for n in v['nodes']]} for v in report['violations']]})
                results['matrix'].append({'width':width,'theme':theme,'overflow':False,'menu_faq_links_images':'PASS'})
                context.close()
        (output/'browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
        context=browser.new_context(viewport={'width':390,'height':844},color_scheme='light',has_touch=True)
        page=context.new_page();page.goto(base)
        button=page.locator('#theme-toggle'); button.click() # system -> light
        button.click() # light -> dark
        assert page.locator('html').get_attribute('data-theme')=='dark'
        page.reload(); assert page.locator('html').get_attribute('data-theme')=='dark'
        page.locator('#theme-toggle').click() # dark -> system
        page.emulate_media(color_scheme='light');expect(page.locator('html')).to_have_attribute('data-theme','light')
        page.emulate_media(color_scheme='dark');expect(page.locator('html')).to_have_attribute('data-theme','dark')
        results['interactions'].append('Theme persistence, reset to system and OS changes PASS')
        page.route('**/gallery-qa-fixture',lambda route:route.fulfill(content_type='text/html',body=gallery_fixture()))
        page.goto(urljoin(base,'gallery-qa-fixture'))
        opener=page.locator('.screen-button').first
        opener.click();assert page.locator('#viewer').evaluate('(el)=>el.open')
        page.keyboard.press('ArrowRight'); assert '2 / 2' in page.locator('#viewer-caption').inner_text()
        page.keyboard.press('ArrowLeft'); assert '1 / 2' in page.locator('#viewer-caption').inner_text()
        page.locator('#viewer-close').focus();page.keyboard.press('Shift+Tab')
        assert page.locator('#viewer-next').evaluate('(el)=>el===document.activeElement'), 'Native dialog focus containment'
        page.keyboard.press('Escape');assert not page.locator('#viewer').evaluate('(el)=>el.open')
        assert opener.evaluate('(el)=>el===document.activeElement')
        opener.tap()
        box=page.locator('#viewer-image').bounding_box()
        cdp=context.new_cdp_session(page)
        y=box['y']+box['height']/2
        cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box['x']+box['width']*.8,'y':y}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':box['x']+box['width']*.2,'y':y}]})
        cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        assert '2 / 2' in page.locator('#viewer-caption').inner_text()
        page.locator('#viewer-image').evaluate("el=>el.src='/missing-image-qa.webp'")
        page.locator('#viewer-error').wait_for(state='visible')
        page.locator('#viewer-close').tap()
        results['interactions'].append('Gallery test-only fixtures: keyboard, native focus trap, Escape/restore focus, touch/swipe, image error PASS')
        context.close()
        context=browser.new_context(viewport={'width':320,'height':844},java_script_enabled=False)
        page=context.new_page();page.goto(base)
        assert page.locator('#navigation a').first.is_visible()
        page.locator('summary').first.click();assert page.locator('details').first.get_attribute('open') is not None
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        results['interactions'].append('No-JS mobile navigation and native FAQ PASS')
        context.close();browser.close()
    (output/'browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    assert not results['page_errors'],results['page_errors']
    assert not results['failed_requests'],results['failed_requests']
    violations=[v for run in results['axe'] for v in run['violations']]
    print(json.dumps({'matrix_runs':len(results['matrix']),'interactions':results['interactions'],'axe_violations':violations},ensure_ascii=False,indent=2))
    assert not violations,violations

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://127.0.0.1:8001/');parser.add_argument('--output',type=Path,default=ROOT/'.test-results/browser');parser.add_argument('--interactions-only',action='store_true');parser.add_argument('--axe',default='/tmp/website-qa/node_modules/axe-core/axe.min.js');args=parser.parse_args()
    run(args.base,args.output,args.axe,args.interactions_only)
