#!/usr/bin/env python3
"""Dependency-free static build. Draft output is never a publishable release."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

def escape(value):
    return html.escape(str(value), quote=True)

def https(value):
    parsed = urlparse(str(value))
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Expected a credential-free HTTPS URL')
    return str(value)

def asset(value):
    path = Path(value)
    if not value.startswith('assets/') or '..' in path.parts or not (ROOT / path).is_file() or not (ROOT / path).resolve().is_relative_to((ROOT / 'assets').resolve()):
        raise ValueError(f'Missing or unsafe asset: {value}')
    return escape(value)

def validate(site, release, production=False):
    https(site['domain'])
    if not re.fullmatch(r'[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}', site['support']):
        raise ValueError('Invalid support email')
    if release['status'] not in ('unverified', 'verified'):
        raise ValueError('Unknown release status')
    verified = release['status'] == 'verified'
    if verified:
        if release.get('approved_for_distribution') is not True or not release.get('approval_reference'):
            raise ValueError('Owner approval for APK distribution required')
        for key in ('version', 'date', 'size_bytes', 'min_android', 'source_commit', 'verification_note', 'sha256', 'url'):
            if not release.get(key):
                raise ValueError(f'Missing verified release field: {key}')
        https(release['url'])
        if not re.fullmatch(r'[a-f0-9]{64}', release['sha256']):
            raise ValueError('SHA-256 must contain 64 lowercase hex digits')
        if not isinstance(release['size_bytes'], int) or release['size_bytes'] <= 0:
            raise ValueError('Invalid APK size')
        if not re.fullmatch(r'[a-f0-9]{40}', release['source_commit']):
            raise ValueError('Expected full Android source commit')
        from datetime import date
        date.fromisoformat(release['date'])
    for feature in site['features']:
        if feature.get('verified_version') != release.get('version') or not verified or not feature.get('evidence'):
            raise ValueError('Feature is not verified against this APK')
        if feature.get('icon'):
            asset(feature['icon'])
    for screen in site['screenshots']:
        if not verified or screen.get('verified_version') != release['version'] or not screen.get('evidence') or not screen.get('approved_for_publication'):
            raise ValueError('Screenshot is not approved for this APK')
        asset(screen['src'])
        if not screen.get('alt') or not screen.get('caption'):
            raise ValueError('Screenshot requires alt and caption')
        if not isinstance(screen['width'], int) or not isinstance(screen['height'], int) or min(screen['width'], screen['height']) <= 0:
            raise ValueError('Invalid screenshot dimensions')
    if production and (not verified or not site['features'] or not site['screenshots']):
        raise ValueError('Publication blocked: verified APK, feature evidence and approved real screenshots required')
    return verified

def render(site, release, production=False, publication=None):
    verified = validate(site, release, production)
    if production and (not publication or publication.get('approved') is not True or not isinstance(publication.get('approval_reference'), str) or not publication['approval_reference'].strip()):
        raise ValueError('Separate website publication approval required before enabling indexing')
    values = {key: escape(site[key]) for key in ('description', 'domain', 'support')}
    values['theme_init'] = '<script>' + (ROOT / 'scripts/theme.js').read_text() + '</script>'
    values['stylesheet'] = '<style>' + (ROOT / 'styles/site.css').read_text() + '</style>'
    values.update(robots='index,follow' if production else 'noindex,nofollow',
                  download_label='Скачать для Android' if verified else 'О выпуске для Android',
                  hero_release_note=f'Android · Версия {escape(release["version"])}' if verified else 'Скоро для Android. Дата выпуска пока не объявлена.',
                  features_intro='Возможности подтверждены для указанной ниже версии приложения.' if site['features'] else 'Знакомство с возможностями — вместе с доступной версией приложения.',
                  screens_intro='Настоящие экраны версии ' + escape(release['version']) + '.' if site['screenshots'] else 'Галерея экранов появится вместе с доступной версией приложения.',
                  release_summary='Проверенный файл и сведения о выпуске — в одном месте.' if verified else 'Готовим сведения о проверенном выпуске. Ссылка появится после проверки APK.')
    mascot = '<img class="hero-cat" src="assets/brand/originals/mascot_calm.webp" width="440" height="512" alt="Рыжий котик — маскот Я ХУдЕЮ" fetchpriority="high">'
    if site['screenshots']:
        first = site['screenshots'][0]
        values['hero_visual'] = '<div class="hero-art with-screen"><div class="mascot-field" aria-hidden="true"></div><div class="phone-frame"><img src="' + asset(first['src']) + '" alt="' + escape(first['alt']) + '" width="' + str(first['width']) + '" height="' + str(first['height']) + '" fetchpriority="high"></div>' + mascot + '</div>'
    else:
        values['hero_visual'] = '<div class="hero-art"><div class="mascot-field" aria-hidden="true"></div><span class="art-orbit" aria-hidden="true">✦</span>' + mascot + '<div class="art-note"><strong>Большие перемены<br>начинаются с малого.</strong>По одному шагу за раз.</div></div>'
    if site['features']:
        values['features'] = '<div class="feature-grid">' + ''.join(
            '<article class="panel">' + (f'<img class="feature-icon" src="{asset(f["icon"])}" alt="" width="52" height="52" loading="lazy">' if f.get('icon') else '') +
            f'<h3>{escape(f["title"])}</h3><p>{escape(f["description"])}</p></article>' for f in site['features']) + '</div>'
    else:
        values['features'] = '<div class="panel empty-features"><h3 style="margin:0">Расскажем больше к выпуску</h3><p>Здесь появится подробный рассказ о возможностях доступной версии. Пока можно познакомиться с приложением и найти ответы на вопросы ниже.</p></div>'
    if site['screenshots']:
        values['gallery'] = '<div class="gallery-track" tabindex="0" role="region" aria-label="Скриншоты приложения">' + ''.join(
            f'<figure class="screen-item"><button class="screen-button" type="button" data-caption="{escape(s["caption"])}" aria-label="Открыть: {escape(s["caption"])}"><img src="{asset(s["src"])}" alt="{escape(s["alt"])}" width="{s["width"]}" height="{s["height"]}" loading="lazy"></button><figcaption>{escape(s["caption"])}</figcaption></figure>' for s in site['screenshots']) + '</div><div class="gallery-toolbar"><button class="icon-button" type="button" data-gallery-direction="-1" aria-label="Предыдущие экраны">←</button><button class="icon-button" type="button" data-gallery-direction="1" aria-label="Следующие экраны">→</button></div>'
    else:
        values['gallery'] = '<div class="screen-empty"><div><h3>Приложение изнутри — скоро</h3><p>Добавим сюда скриншоты проверенного выпуска, чтобы вы могли познакомиться с приложением до установки.</p></div><div class="screen-reserved">Скриншоты появятся к выпуску</div></div>'
    if verified:
        fields = [('Версия', release['version']), ('Дата выпуска', release['date']), ('Размер файла', f'{release["size_bytes"]:,} байт'.replace(',', ' ')), ('Совместимость', 'Android ' + release['min_android']), ('SHA-256', release['sha256'])]
        values['release'] = '<div class="release-status"><span class="status-label">Проверенный APK</span><dl class="release-data">' + ''.join(f'<dt>{escape(k)}</dt><dd>{escape(v)}</dd>' for k, v in fields) + f'</dl><a class="button" href="{escape(https(release["url"]))}" rel="noopener noreferrer">Скачать для Android ↓</a>' + ('<h3>Что нового</h3><ul>' + ''.join('<li>'+escape(c)+'</li>' for c in release.get('changes', [])) + '</ul>' if release.get('changes') else '') + '</div>'
    else:
        pending = site['pending_release']
        values['release'] = '<div class="release-status"><span class="status-label">' + escape(pending['label']) + '</span><h3>' + escape(pending['title']) + '</h3><p>' + escape(pending['description']) + '</p><p><a href="mailto:' + escape(site['support']) + '">Связаться с поддержкой ↗</a></p></div>'
    faq = list(site['faq'])
    if verified:
        faq[0] = dict(question='Где скачать приложение?', answer='Проверенный Android APK доступен в разделе загрузки. Сверьте версию и контрольную сумму файла перед установкой.')
    values['faq'] = ''.join(f'<details><summary>{escape(f["question"])}</summary><p>{escape(f["answer"])}</p></details>' for f in faq)
    # No ratings, price, release version, or unverified platform compatibility in structured data.
    application = {'@context': 'https://schema.org', '@type': 'SoftwareApplication', 'name': site['name'], 'operatingSystem': 'Android', 'url': site['domain'] + '/'}
    if verified:
        application.update(softwareVersion=release['version'], downloadUrl=release['url'])
    values['structured_data'] = '<script type="application/ld+json">' + json.dumps(application, ensure_ascii=False).replace('<', r'\u003c') + '</script>'
    template = (ROOT / 'index.html').read_text()
    result = re.sub(r'\{\{(\w+)\}\}', lambda match: values[match[1]], template)
    if '{{' in result:
        raise ValueError('Unresolved template field')
    return result

def build(output, production=False):
    site = json.loads((ROOT / 'data/site.json').read_text())
    release = json.loads((ROOT / 'data/release.json').read_text())
    publication = json.loads((ROOT / 'data/publication.json').read_text())
    page = render(site, release, production, publication)
    if output.is_symlink():
        raise ValueError('Symlink output is not allowed')
    output = output.resolve()
    if output == ROOT or ROOT.is_relative_to(output) or output.name != '_site':
        raise ValueError('Output must be a dedicated directory named _site')
    output.mkdir(parents=True, exist_ok=True)
    # Do not publish repository docs, configs, source maps, test fixtures, or original unused assets.
    files = ['privacy.html', 'CNAME', 'styles/site.css', 'scripts/site.js', 'scripts/theme.js',
             'assets/brand/originals/mascot_calm.webp', 'assets/brand/originals/ic_launcher_green.png',
             'assets/fonts/onest_regular.woff2', 'assets/fonts/onest_semibold.woff2', 'assets/fonts/unbounded_semibold.woff2',
             'assets/fonts/Onest-OFL.txt', 'assets/fonts/Unbounded-OFL.txt']
    files += [str(p.relative_to(ROOT)) for p in (ROOT / 'assets/brand/web').glob('*.webp')]
    files += [f['icon'] for f in site['features'] if f.get('icon')]
    files += [s['src'] for s in site['screenshots']]
    # Refuse symlink targets: never delete unrelated output or write through external links.
    if output.is_symlink() or any(p.is_symlink() for p in output.rglob('*')):
        raise ValueError('Symlink found in output directory')
    for p in output.iterdir():
        if p.is_dir(): shutil.rmtree(p)
        else: p.unlink()
    for name in set(files):
        dest = output / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, dest)
    (output / 'index.html').write_text(page)
    (output / '.nojekyll').touch()
    (output / 'robots.txt').write_text('User-agent: *\n' + ('Allow: /\nSitemap: '+site['domain']+'/sitemap.xml\n' if production else 'Disallow: /\n'))
    (output / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>'+escape(site['domain']+path)+'</loc></url>' for path in ['/', '/privacy.html']) + '</urlset>\n')
    print(f'Built {output} ({"production" if production else "draft, noindex"})')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', action='store_true', help='Require verified release content; does not deploy')
    parser.add_argument('--output', type=Path, default=ROOT / '_site')
    args = parser.parse_args()
    try: build(args.output, args.production)
    except (ValueError, KeyError) as error: parser.exit(1, f'Build blocked: {error}\n')
