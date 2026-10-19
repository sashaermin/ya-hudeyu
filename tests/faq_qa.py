"""Category navigation, native disclosure/focus and responsive FAQ; local review only."""
import argparse,json,os
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
def run(base,out,engine,executable):
    out.mkdir(parents=True,exist_ok=True);r={'engine':engine,'matrix':[],'axe':[],'nojs':[],'errors':[]}
    with sync_playwright() as p:
        options=dict(headless=True)
        if engine=='chromium':options.update(executable_path=executable or '/usr/bin/chromium',args=['--no-sandbox'])
        elif executable:options['executable_path']=executable
        if engine=='firefox':options['firefox_user_prefs']={'security.sandbox.content.level':0}
        b=getattr(p,engine).launch(**options);r['version']=b.version
        for theme in ('light','dark'):
            for width in (320,360,390,430,768,1024,1440,1920):
                c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce');page=c.new_page();page.on('pageerror',lambda e:r['errors'].append(str(e)));page.goto(base);page.evaluate('document.fonts.ready')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                assert page.locator('.faq-group').count()==8 and page.locator('.faq-group details').count()==33
                for link in page.locator('.faq-categories a').all():
                    box=link.bounding_box();assert box['height']>=44 and box['x']>=0 and box['x']+box['width']<=width+1
                link=page.locator('.faq-categories a[href="#faq-nutrition"]');link.focus();page.keyboard.press('Enter');expect(page.locator('#faq-nutrition')).to_be_focused()
                first=page.locator('#faq-nutrition summary').first;first.focus();page.keyboard.press('Space');expect(page.locator('#faq-nutrition details').first).to_have_attribute('open','');page.keyboard.press('Enter');expect(page.locator('#faq-nutrition details').first).not_to_have_attribute('open','')
                back=page.locator('#faq-nutrition .faq-back');back.focus();page.keyboard.press('Enter');expect(page.locator('#faq-categories')).to_be_focused()
                if width in (390,1440):
                    page.add_script_tag(path=str(ROOT/'tools/qa/node_modules/axe-core/axe.min.js'));a=page.evaluate("async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})")
                    r['axe'].append(dict(width=width,theme=theme,violations=[dict(id=v['id'],impact=v['impact']) for v in a['violations']]))
                    # Show one practical answer in each category for the review image.
                    page.locator('.faq-categories').evaluate('(e)=>e.blur()')
                    for details in page.locator('.faq-group details:first-of-type').all():details.evaluate('(e)=>e.open=true')
                    page.locator('#faq').screenshot(path=str(out/f'faq-{width}-{theme}.png'))
                    page.locator('#faq-nutrition').screenshot(path=str(out/f'nutrition-{width}-{theme}.png'))
                r['matrix'].append(dict(width=width,theme=theme,category_enter_focus=True,space_enter_disclosure=True,back_focus=True,overflow=False));c.close()
            for width in (320,390,768):
                c=b.new_context(viewport={'width':width,'height':900},color_scheme=theme,java_script_enabled=False,reduced_motion='reduce');page=c.new_page();page.goto(base)
                page.locator('.faq-categories a[href="#faq-body"]').click();page.locator('#faq-body summary').first.focus();page.keyboard.press('Enter');assert page.locator('#faq-body details').first.get_attribute('open') is not None
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');r['nojs'].append(dict(width=width,theme=theme,passed=True));c.close()
        # Exercise every actual question once, not only a representative fixture.
        c=b.new_context();page=c.new_page();page.goto(base)
        for details in page.locator('.faq-group details').all():
            summary=details.locator('summary');summary.focus();page.keyboard.press('Enter');expect(details).to_have_attribute('open','');page.keyboard.press('Enter');expect(details).not_to_have_attribute('open','')
        r['all_disclosures']=33;c.close();b.close()
    (out/'faq-results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    assert not r['errors'] and not any(a['violations'] for a in r['axe']),r
    print(engine,'16responsive+4axe+6noJS+33disclosures PASS')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--base',default='http://127.0.0.1:8026/');a.add_argument('--out',type=Path,required=True);a.add_argument('--engine',default='chromium');a.add_argument('--executable');x=a.parse_args();run(x.base,x.out,x.engine,x.executable)
