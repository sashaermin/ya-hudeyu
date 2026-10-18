#!/usr/bin/env python3
"""Focused UI/UX audit regressions on a local draft, never production fixtures."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
WIDTHS=(320,360,390,430,768,1024,1440,1920)
class LegalContent(HTMLParser):
    def __init__(self): super().__init__(); self.out=[]; self.tags=[]
    def handle_starttag(self,t,a):
        if t in ['h1','h2','p']: self.tags.append(t); self.out.append(('start',t))
        if t=='a' and self.tags: self.out.append(('href',dict(a).get('href')))
    def handle_endtag(self,t):
        if self.tags and t==self.tags[-1]: self.tags.pop(); self.out.append(('end',t))
    def handle_data(self,s):
        if self.tags and s.strip(): self.out.append(('text',' '.join(s.split())))
def legal_hash(text):
    p=LegalContent();p.feed(text)
    return hashlib.sha256(json.dumps(p.out,ensure_ascii=False).encode()).hexdigest()

def run(base, output):
    output.mkdir(parents=True,exist_ok=True)
    result={'scope':'Local development UI audit only; production unchanged','privacy_matrix':[], 'nojs':[], 'focus':[], 'privacy_axe':[], 'privacy_text_adaptation':[], 'page_errors':[]}
    assert legal_hash((ROOT/'privacy.html').read_text())==json.loads((ROOT/'docs/verification/uiux-before.json').read_text())['legal_content_sha256']
    result['legal_content_unchanged']=True
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
        for theme in ('light','dark'):
            for width in WIDTHS:
                c=browser.new_context(viewport={'width':width,'height':900},color_scheme=theme)
                page=c.new_page();page.on('pageerror',lambda e:result['page_errors'].append(str(e)))
                page.goto(base+'privacy.html');page.evaluate('document.fonts.ready')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme)
                assert page.locator('html').get_attribute('data-theme')==theme
                assert page.locator('h1').inner_text()=='Политика конфиденциальности'
                if width in (320,390,1440):
                    page.screenshot(path=str(output/f'privacy-{width}-{theme}.png'),full_page=True)
                if width in (390,1440):
                    page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'))
                    a=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    assert not a['violations'],a['violations']
                    result['privacy_axe'].append(dict(width=width,theme=theme,violations=0,axe_version=a['testEngine']['version']))
                result['privacy_matrix'].append(dict(width=width,theme=theme,status='PASS'))
                c.close()
            for width in (320,390,768):
                c=browser.new_context(viewport={'width':width,'height':900},color_scheme=theme,java_script_enabled=False)
                page=c.new_page();page.goto(base)
                nav=page.locator('#navigation').bounding_box();hero=page.locator('.hero').bounding_box()
                assert nav['y']+nav['height']<=hero['y'],(width,nav,hero)
                expected='rgb(19, 17, 23)' if theme=='dark' else 'rgb(247, 244, 239)'
                assert page.locator('body').evaluate('el=>getComputedStyle(el).backgroundColor')==expected
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                if width==320:page.screenshot(path=str(output/f'nojs-320-{theme}.png'),full_page=True)
                page.goto(base+'privacy.html')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert page.locator('body').evaluate('el=>getComputedStyle(el).backgroundColor')==expected
                result['nojs'].append(dict(width=width,theme=theme,status='PASS'))
                c.close()
        for theme in ('light','dark'):
            for width in (320,390,1440):
                for mode in ('text-200','text-spacing'):
                    c=browser.new_context(viewport={'width':width,'height':900},color_scheme=theme)
                    page=c.new_page();page.goto(base+'privacy.html');page.evaluate('document.fonts.ready')
                    if mode=='text-200':
                        page.evaluate('''() => { for(const el of document.querySelectorAll('body *')) {
                            if(['SCRIPT','STYLE','SVG','PATH','CIRCLE'].includes(el.tagName)) continue;
                            el.dataset.baseFont=getComputedStyle(el).fontSize;
                        } for(const el of document.querySelectorAll('[data-base-font]')) el.style.fontSize=(parseFloat(el.dataset.baseFont)*2)+'px'; }''')
                    else:
                        page.add_style_tag(content='* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p {margin-bottom:2em!important}')
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(theme,width,mode)
                    result['privacy_text_adaptation'].append(dict(width=width,theme=theme,mode=mode,status='PASS',method='CSS simulation, not native zoom'))
                    c.close()
        c=browser.new_context(viewport={'width':390,'height':844});page=c.new_page();page.goto(base)
        toggle=page.locator('#menu-toggle');toggle.focus();page.keyboard.press('Enter')
        assert page.locator('#navigation a').first.evaluate('el=>el===document.activeElement')
        page.keyboard.press('Tab');assert page.locator('#navigation a').nth(1).evaluate('el=>el===document.activeElement')
        page.keyboard.press('Escape');assert toggle.evaluate('el=>el===document.activeElement')
        toggle.press('Space');page.locator('#navigation a[href="#faq"]').click()
        assert page.locator('#faq').evaluate('el=>el===document.activeElement')
        page.set_viewport_size({'width':1024,'height':844});page.locator('#navigation a').first.focus()
        page.set_viewport_size({'width':390,'height':844});expect(toggle).to_be_focused()
        result['focus']=['Keyboard open focuses first link; Tab traverses nav; Escape restores trigger; selection focuses target; hidden-nav resize restores trigger']
        c.close()
        for path in ('','privacy.html'):
            c=browser.new_context(color_scheme='light');page=c.new_page()
            page.add_init_script("localStorage.setItem('hudeyu-theme','dark')")
            page.goto(base+path)
            assert page.locator('html').get_attribute('data-theme')=='dark'
            page.reload();assert page.locator('html').get_attribute('data-theme')=='dark'
            page.locator('#theme-toggle').click();page.emulate_media(color_scheme='light');expect(page.locator('html')).to_have_attribute('data-theme','light')
            c.close()
        result['shared_theme_persistence']='PASS: main/privacy saved dark override and reset to system'
        browser.close()
    assert not result['page_errors'],result['page_errors']
    (output/'uiux-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'privacy_matrix':len(result['privacy_matrix']),'nojs':len(result['nojs']),'privacy_axe':len(result['privacy_axe']),'status':'PASS'}))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--base',default='http://127.0.0.1:8012/');a.add_argument('--output',type=Path,default=ROOT/'.test-results/uiux-u1');args=a.parse_args();run(args.base,args.output)
