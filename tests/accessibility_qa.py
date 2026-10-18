#!/usr/bin/env python3
"""Focused text adaptation, reduced-motion and skip-link QA on a local draft.

Text resizing is a CSS simulation of text-only zoom, not browser or device zoom.
Existing 320px matrix evidence covers reflow; this does not repeat that matrix.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


TEXT_BOUNDS = """() => {
    const failures = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
        const node = walker.currentNode, parent = node.parentElement;
        if (!node.textContent.trim() || !parent.checkVisibility() ||
            parent.closest('script, style, .skip')) continue;
        const range = document.createRange(); range.selectNodeContents(node);
        for (const r of range.getClientRects()) {
            if (r.width && (r.left < -.5 || r.right > innerWidth + .5)) {
                failures.push({text: node.textContent.trim().slice(0, 100),
                    selector: parent.tagName + '.' + parent.className,
                    left: r.left, right: r.right});
                break;
            }
        }
    }
    return failures;
}"""


def run(base, executable, output, engine='chromium'):
    output.mkdir(parents=True, exist_ok=True)
    result = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'method': 'CSS text-only 200% simulation; WCAG 1.4.12 spacing override; not native browser zoom',
              'engine': engine, 'cases': [], 'page_errors': [], 'preferences': []}
    with sync_playwright() as p:
        options = dict(headless=True)
        if executable:
            options['executable_path'] = executable
        if engine == 'chromium':
            options.update(executable_path=executable or '/usr/bin/chromium', args=['--no-sandbox'])
        if engine == 'firefox' and os.environ.get('WEBSITE_FIREFOX_CONTAINER') == '1':
            options['firefox_user_prefs'] = {'security.sandbox.content.level': 0}
        browser = getattr(p, engine).launch(**options)
        result['browser_version'] = browser.version
        for mode in ('text-200', 'text-spacing'):
            for theme in ('light', 'dark'):
                for width in (320, 390, 1440):
                    context = browser.new_context(viewport={'width': width, 'height': 900}, color_scheme=theme)
                    page = context.new_page()
                    page.on('pageerror', lambda error: result['page_errors'].append(str(error)))
                    response = page.goto(base)
                    assert response.status == 200
                    result['site_index_sha256'] = hashlib.sha256(response.body()).hexdigest()
                    page.evaluate('document.fonts.ready')
                    page.evaluate("document.querySelectorAll('details').forEach(el => el.open = true)")
                    if width <= 800:
                        page.locator('#menu-toggle').click()
                    if mode == 'text-200':
                        # Snapshot all computed sizes first to avoid multiplying inherited sizes twice.
                        page.evaluate("""() => {
                            const sizes = [...document.querySelectorAll('body, body *')].map(el => {
                                const s = getComputedStyle(el);
                                return [el, parseFloat(s.fontSize), parseFloat(s.lineHeight)];
                            });
                            for (const [el, size, line] of sizes) {
                                el.style.fontSize = size * 2 + 'px';
                                if (Number.isFinite(line)) el.style.lineHeight = line * 2 + 'px';
                            }
                        }""")
                    else:
                        page.add_style_tag(content='* {line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important} p {margin-bottom:2em!important}')
                    failures = page.evaluate(TEXT_BOUNDS)
                    overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
                    case = dict(mode=mode, theme=theme, width=width, overflow=overflow, out_of_view_text=failures)
                    result['cases'].append(case)
                    if failures or overflow or (width == 320 and theme == 'dark'):
                        page.screenshot(path=str(output/f'{mode}-{width}-{theme}.png'), full_page=True)
                    context.close()
        context = browser.new_context(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        page = context.new_page(); page.goto(base)
        motion = page.evaluate("""() => ({
            matches: matchMedia('(prefers-reduced-motion: reduce)').matches,
            scroll: getComputedStyle(document.documentElement).scrollBehavior,
            transition: getComputedStyle(document.querySelector('.button')).transitionDuration
        })""")
        assert motion == dict(matches=True, scroll='auto', transition='0s'), motion
        result['preferences'].append({'reduced_motion': motion})
        page.keyboard.press('Tab')
        assert page.locator('.skip').evaluate('el => el === document.activeElement')
        assert page.locator('.skip').bounding_box()['y'] >= 0
        assert page.locator('.skip').evaluate("el => getComputedStyle(el).outlineStyle !== 'none'")
        page.keyboard.press('Enter')
        skip_focus = page.evaluate("location.hash === '#main' && document.activeElement.id === 'main'")
        result['preferences'].append({'keyboard_skip_link': {'first_tab_visible_focus': True, 'enter_focus_main': skip_focus}})
        context.close(); browser.close()
    (output/'accessibility-results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    failures = [case for case in result['cases'] if case['overflow'] or case['out_of_view_text']]
    print(json.dumps({'cases': len(result['cases']), 'failures': failures, 'preferences': result['preferences']}, ensure_ascii=False, indent=2))
    assert not result['page_errors'], result['page_errors']
    assert skip_focus, 'Skip link must move keyboard focus to main'
    assert not failures, 'Text adaptation failures; see saved result and screenshots'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:8002/')
    parser.add_argument('--engine', choices=['chromium', 'firefox', 'webkit'], default='chromium')
    parser.add_argument('--executable')
    parser.add_argument('--output', type=Path, default=Path('.test-results/accessibility'))
    args = parser.parse_args()
    run(args.base, args.executable, args.output, args.engine)
