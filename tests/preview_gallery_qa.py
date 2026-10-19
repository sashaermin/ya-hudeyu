"""Real preliminary gallery: layouts, categories, full-size viewer, no-JS and touch."""
import argparse,json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
WIDTHS=(320,360,390,430,768,1024,1440,1920)
ORDER=['today','cards','nutrition','activity','gps','progress','journey','plan','charts','profile','goals']
def run(base,out,engine,executable):
    out.mkdir(parents=True,exist_ok=True)
    r=dict(engine=engine,matrix=[],axe=[],nojs=[],page_errors=[])
    with sync_playwright() as p:
        opts=dict(headless=True)
        if engine=='chromium':opts.update(executable_path=executable or '/usr/bin/chromium',args=['--no-sandbox'])
        elif executable:opts['executable_path']=executable
        if engine=='firefox' and os.environ.get('WEBSITE_FIREFOX_CONTAINER')=='1':opts['firefox_user_prefs']={'security.sandbox.content.level':0}
        b=getattr(p,engine).launch(**opts);r['version']=b.version
        for theme in ('light','dark'):
            for width in WIDTHS:
                c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
                page=c.new_page();page.on('pageerror',lambda e:r['page_errors'].append(str(e)));page.goto(base);page.evaluate('document.fonts.ready')
                assert page.locator('html').get_attribute('data-theme')==theme
                assert page.locator('meta[name=robots]').get_attribute('content')=='noindex,nofollow'
                assert page.locator('a[href$=".apk"],[data-apk-download]').count()==0
                assert page.locator('.preview-item').evaluate_all('(es)=>es.map(e=>e.dataset.previewId)')==ORDER
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert page.locator('html').evaluate('e=>getComputedStyle(e).scrollBehavior')=='auto'
                for link in page.locator('.preview-categories a').all():
                    link.scroll_into_view_if_needed();box=link.bounding_box();assert box['height']>=44 and box['x']>=0 and box['x']+box['width']<=width+1
                    link.focus();target=page.locator(link.get_attribute('href'));page.keyboard.press('Enter');expect(target).to_be_focused()
                    box=target.bounding_box();assert box['x']>=-1 and box['x']<width
                for item in page.locator('.preview-item').all():
                    item.scroll_into_view_if_needed();img=item.locator('img');img.evaluate('e=>e.decode()');box=img.bounding_box()
                    assert box['width']>190 and box['height']>box['width']*2
                    assert abs(box['height']/box['width']-1866/843)<.03
                first=page.locator('.screen-button').first;first.click();expect(page.locator('#viewer-image')).to_be_visible();page.locator('#viewer-image').evaluate('e=>e.decode()')
                expect(page.locator('#viewer-close')).to_be_focused();page.keyboard.press('Tab');expect(page.locator('.viewer-canvas')).to_be_focused();page.keyboard.press('Tab');expect(page.locator('#viewer-prev')).to_be_focused()
                page.keyboard.press('ArrowRight');expect(page.locator('#viewer-caption')).to_contain_text('2 / 11')
                page.locator('#viewer-image').evaluate('e=>e.decode()');page.locator('#viewer-zoom').click();expect(page.locator('#viewer-zoom')).to_have_attribute('aria-pressed','true')
                assert page.locator('.viewer-canvas').evaluate('e=>e.scrollHeight>e.clientHeight')
                page.locator('.viewer-canvas').evaluate('e=>e.scrollTop=300');assert page.locator('.viewer-canvas').evaluate('e=>e.scrollTop')>0
                page.keyboard.press('ArrowRight');expect(page.locator('#viewer-zoom')).to_have_attribute('aria-pressed','false')
                page.keyboard.press('Escape');expect(first).to_be_focused()
                # Every source opens the matching full image and survives repeated opening.
                for index,button in enumerate(page.locator('.screen-button').all()):
                    button.click();expect(page.locator('#viewer-image')).to_be_visible();page.locator('#viewer-image').evaluate('e=>e.decode()')
                    assert page.locator('#viewer-image').get_attribute('src')==button.locator('img').get_attribute('data-full')
                    expect(page.locator('#viewer-caption')).to_contain_text(f'{index+1} / 11')
                    page.keyboard.press('Escape');expect(button).to_be_focused()
                if width<=800:
                    page.locator('.preview-track').evaluate('e=>e.scrollLeft=0');page.locator('[data-gallery-direction="1"]').click()
                    page.wait_for_function('document.querySelector(".preview-track").scrollLeft>50')
                if width in (390,1440):
                    page.locator('.preview-track').evaluate('e=>e.scrollLeft=0')
                    page.locator('#screenshots').scroll_into_view_if_needed()
                    page.screenshot(path=str(out/f'gallery-{width}-{theme}.png'))
                    page.locator('.preview-disclaimer').scroll_into_view_if_needed()
                    page.screenshot(path=str(out/f'disclaimer-{width}-{theme}.png'))
                    page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'))
                    a=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    r['axe'].append(dict(width=width,theme=theme,state='page',violations=[v['id'] for v in a['violations']]))
                    first.click();page.locator('#viewer-image').evaluate('e=>e.decode()')
                    a=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    r['axe'].append(dict(width=width,theme=theme,state='viewer',violations=[v['id'] for v in a['violations']]))
                    page.screenshot(path=str(out/f'viewer-{width}-{theme}.png'))
                print(engine,width,theme,'PASS',flush=True)
                r['matrix'].append(dict(width=width,theme=theme,images=11,categories=5,opens=11,focus=True,zoom=True,overflow=False));c.close()
            for width in (320,390,768,1440):
                c=b.new_context(viewport={'width':width,'height':900},java_script_enabled=False,color_scheme=theme)
                page=c.new_page();page.goto(base);page.locator('.preview-categories a[href="#preview-progress"]').click();expect(page.locator('#preview-progress')).to_be_focused()
                assert page.locator('.preview-original').count()==11
                for a in page.locator('.preview-original').all():
                    response=page.request.get(base+a.get_attribute('href'));assert response.status==200 and response.headers['content-type']=='image/webp'
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                r['nojs'].append(dict(width=width,theme=theme,native_categories=True,full_image_links=11));c.close()
        c=b.new_context(viewport={'width':390,'height':900},has_touch=True,is_mobile=True);page=c.new_page();page.goto(base)
        # Request abort tests the real loading/error/retry state without publishing a fixture.
        pattern='**/assets/previews/today-full.webp';page.route(pattern,lambda route:route.abort())
        page.locator('.screen-button').first.click();expect(page.locator('#viewer-error')).to_be_visible();expect(page.locator('#viewer-zoom')).to_be_disabled()
        page.unroute(pattern);page.locator('#viewer-next').click();page.locator('#viewer-prev').click();expect(page.locator('#viewer-image')).to_be_visible();page.locator('#viewer-image').evaluate('e=>e.decode()');r['error_retry']=True
        if engine=='chromium':
            session=c.new_cdp_session(page);box=page.locator('#viewer-image').bounding_box();x=box['x']+box['width']*.8;y=box['y']+box['height']*.5
            session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
            session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-120,'y':y}]})
            session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            expect(page.locator('#viewer-caption')).to_contain_text('2 / 11');r['cdp_viewer_swipe']=True
            page.keyboard.press('Escape');track=page.locator('.preview-track');track.scroll_into_view_if_needed();track.evaluate('e=>e.scrollLeft=0');box=track.bounding_box();x=box['x']+box['width']*.8;y=max(20,min(850,box['y']+150))
            session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
            for step in range(1,7):session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-30*step,'y':y}]})
            session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
            page.wait_for_function('document.querySelector(".preview-track").scrollLeft>50');r['cdp_track_swipe']=True
        c.close();b.close()
    assert not r['page_errors'] and not any(a['violations'] for a in r['axe']),r
    (out/'gallery-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(engine,'16layouts/176opens/8axe/8noJS/error-retry PASS')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--base',default='http://127.0.0.1:8032/');a.add_argument('--out',type=Path,required=True);a.add_argument('--engine',default='chromium');a.add_argument('--executable');x=a.parse_args();run(x.base,x.out,x.engine,x.executable)
