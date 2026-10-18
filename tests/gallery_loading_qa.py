#!/usr/bin/env python3
"""Delayed/error gallery states with original-mascot QA fixtures, never app screenshots."""
import argparse
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from browser_qa import gallery_fixture
ROOT=Path(__file__).resolve().parents[1]
def run(base, output, before=False, engine="chromium", executable=None):
    output.mkdir(parents=True,exist_ok=True); results=[]
    with sync_playwright() as p:
        options=dict(headless=True)
        if engine=='chromium': options.update(executable_path=executable or '/usr/bin/chromium',args=['--no-sandbox'])
        elif executable: options['executable_path']=executable
        if engine=='firefox' and os.environ.get('WEBSITE_FIREFOX_CONTAINER')=='1': options['firefox_user_prefs']={'security.sandbox.content.level':0}
        b=getattr(p,engine).launch(**options)
        for theme in ('light','dark'):
            c=b.new_context(viewport={'width':390,'height':844},color_scheme=theme)
            page=c.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.route('**/gallery-loading-fixture',lambda route:route.fulfill(content_type='text/html',body=gallery_fixture()))
            pending=[]; page.route('**/delayed-qa-image*',lambda route:pending.append(route))
            page.goto(base+'gallery-loading-fixture');page.evaluate('document.fonts.ready')
            opener=page.locator('.screen-button').first
            page.locator('.screen-button img').first.evaluate("el=>el.dataset.full='/delayed-qa-image-1.webp'")
            page.locator('.screen-button img').nth(1).evaluate("el=>el.dataset.full='/delayed-qa-image-2.webp'")
            opener.click()
            if before:
                assert page.locator('#viewer-loading').count()==0
                page.screenshot(path=str(output/f'before-loading-390-{theme}.png'))
                results.append(dict(theme=theme,loading_feedback=False,fixture='Original mascot, not released Android screen'))
                for route in pending: route.abort()
                c.close();continue
            expect(page.locator('#viewer-loading')).to_be_visible()
            expect(page.locator('#viewer-image')).to_be_hidden()
            expect(page.locator('#viewer-image')).to_have_attribute('aria-busy','true')
            page.screenshot(path=str(output/f'after-loading-390-{theme}.png'))
            page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'))
            loading_axe=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
            assert not loading_axe['violations'],loading_axe['violations']
            assert pending
            pending.pop(0).fulfill(content_type='image/webp',body=(ROOT/'assets/brand/originals/mascot_calm.webp').read_bytes())
            expect(page.locator('#viewer-image')).to_be_visible();expect(page.locator('#viewer-loading')).to_be_hidden()
            expect(page.locator('#viewer-image')).to_have_attribute('aria-busy','false')
            page.locator('#viewer-next').click();expect(page.locator('#viewer-loading')).to_be_visible();expect(page.locator('#viewer-image')).to_be_hidden()
            page.keyboard.press('Escape');expect(opener).to_be_focused()
            expect(page.locator('#viewer-image')).to_have_attribute('aria-busy','false')
            assert pending
            pending.pop(0).fulfill(status=503,body='Intentional QA image error')
            # Reopen the failed second full-image; the error must remain understandable and retryable.
            page.route('**/delayed-qa-image-2.webp',lambda route:route.fulfill(status=503,body='Intentional QA error'))
            page.locator('.screen-button').nth(1).click();expect(page.locator('#viewer-error')).to_be_visible()
            expect(page.locator('#viewer-loading')).to_be_hidden();expect(page.locator('#viewer-image')).to_be_hidden()
            page.screenshot(path=str(output/f'after-error-390-{theme}.png'))
            error_axe=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
            assert not error_axe['violations'],error_axe['violations']
            page.locator('#viewer-close').click()
            page.locator('.screen-button img').nth(1).evaluate("el=>el.dataset.full='/retry-qa-image.webp'")
            page.route('**/retry-qa-image.webp',lambda route:route.fulfill(content_type='image/webp',body=(ROOT/'assets/brand/originals/mascot_calm.webp').read_bytes()))
            page.locator('.screen-button').nth(1).click();expect(page.locator('#viewer-image')).to_be_visible()
            expect(page.locator('#viewer-error')).to_be_hidden();expect(page.locator('#viewer-loading')).to_be_hidden()
            page.evaluate("() => {document.querySelector('#viewer').close(); document.querySelectorAll('.screen-button')[1].click();}")
            expect(page.locator('#viewer-image')).to_be_visible()
            expect(page.locator('#viewer-image')).to_have_attribute('aria-busy','false')
            page.keyboard.press('Escape');assert not errors,errors
            results.append(dict(engine=engine,browser_version=b.version,theme=theme,loading_status=True,stale_image_hidden=True,loaded=True,error=True,retry=True,cancel_focus=True,rapid_reopen=True,page_errors=errors,loading_axe_violations=0,error_axe_violations=0,fixture='Original mascot, not released Android screen'))
            c.close()
        b.close()
    (output/'gallery-loading-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--base',default='http://127.0.0.1:8012/');a.add_argument('--output',type=Path,default=ROOT/'.test-results/uiux-u2');a.add_argument('--before',action='store_true');a.add_argument('--engine',default='chromium',choices=['chromium','firefox','webkit']);a.add_argument('--executable');args=a.parse_args();run(args.base,args.output,args.before,args.engine,args.executable)
