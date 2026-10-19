"""Preliminary edited demonstrations, separate from APK-verified release screenshots."""
import hashlib
import html
import json
import re
from pathlib import Path

CATEGORIES=[('overview','Обзор'),('nutrition','Питание'),('activity','Активность'),('progress','Вес и прогресс'),('goals','Цели и здоровье')]
ORDER=['today','nutrition','activity','progress','profile','cards','goals','gps','journey','plan','charts']
LABEL='Предварительный интерфейс · В разработке'
DISCLAIMER='Представленные изображения демонстрируют текущую концепцию интерфейса «Я ХУдЕЮ» и носят ознакомительный характер. Дизайн, расположение элементов, набор функций и их внешний вид могут измениться в процессе разработки. Финальная версия приложения может отличаться от показанной.'

def fingerprint(config):
    return hashlib.sha256(json.dumps(config,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate(config,root,production=False,publication=None):
    if not config or config.get('enabled') is False:return False
    if config.get('enabled') is not True or config.get('kind')!='edited-development-demonstration':raise ValueError('Invalid preliminary gallery state')
    items=config.get('items',[])
    if [i.get('id') for i in items]!=ORDER:raise ValueError('Preliminary gallery requires exactly11 ordered screens')
    category_ids={k for k,_ in CATEGORIES}
    if {i.get('category') for i in items}!=category_ids:raise ValueError('Preview categories incomplete')
    for i in items:
        for key in ('title','description','alt'):
            if not isinstance(i.get(key),str) or not i[key].strip():raise ValueError('Missing preview caption')
        if i.get('privacy_reviewed') is not True or i.get('preliminary') is not True:raise ValueError('Preview requires privacy review and preliminary label')
        for field,hashfield in [('src','sha256'),('full','full_sha256')]:
            name=i.get(field,'')
            if not re.fullmatch(r'assets/previews/[a-z-]+(?:-full)?\.webp',name):raise ValueError('Unsafe preview image path')
            path=root/name
            if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to((root/'assets/previews').resolve()):raise ValueError('Missing/unsafe preview image')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=i.get(hashfield):raise ValueError('Preview integrity mismatch')
            if b'EXIF' in path.read_bytes() or b'XMP ' in path.read_bytes():raise ValueError('Preview metadata must be stripped')
        if type(i.get('width')) is not int or type(i.get('height')) is not int or not 0<i['width']<i['height']:raise ValueError('Preview portrait dimensions required')
    if production:
        approval=(publication or {}).get('preview_gallery',{})
        if approval.get('approved') is not True or approval.get('manifest_sha256')!=fingerprint(config) or not approval.get('approval_reference'):
            raise ValueError('Separate preliminary gallery publication approval required')
    return True

def render(config):
    e=lambda value:html.escape(str(value),quote=True)
    out='<p class="preview-label">'+LABEL+'</p><nav class="preview-categories" aria-label="Категории изображений">'
    out+=''.join(f'<a href="#preview-{key}">{title}<span>{sum(i["category"]==key for i in config["items"])}</span></a>' for key,title in CATEGORIES)+'</nav>'
    out+='<div class="gallery-track preview-track" tabindex="0" role="region" aria-label="Предварительные изображения Android-приложения">'
    for key,category in CATEGORIES:
        members=[i for i in config['items'] if i['category']==key]
        for index,i in enumerate(members):
            target=f' id="preview-{key}" tabindex="-1"' if index==0 else ''
            out+=f'<figure class="screen-item preview-item"{target} data-preview-id="{i["id"]}"><button class="screen-button" type="button" data-caption="Предварительный экран · {e(i["title"])}" aria-label="Увеличить: {e(i["title"])}"><img src="{e(i["src"])}" data-full="{e(i["full"])}" alt="{e(i["alt"])}" width="{i["width"]}" height="{i["height"]}" loading="lazy" decoding="async"></button><figcaption><span class="preview-item-label">{category} · Предварительное изображение</span><h3>{e(i["title"])}</h3><p>{e(i["description"])}</p><a class="preview-original" href="{e(i["full"])}">Открыть изображение: {e(i["title"])} ↗</a></figcaption></figure>'
    out+='</div><div class="gallery-toolbar preview-gallery-toolbar"><button class="icon-button" type="button" data-gallery-direction="-1" aria-label="Предыдущие изображения" hidden>←</button><button class="icon-button" type="button" data-gallery-direction="1" aria-label="Следующие изображения" hidden>→</button></div>'
    return out+'<aside class="preview-disclaimer" aria-labelledby="preview-disclaimer-title"><h3 id="preview-disclaimer-title">Предварительные изображения приложения</h3><p>'+DISCLAIMER+'</p><p>Все персональные данные и показатели на демонстрационных изображениях являются условными.</p><p>Изображения отредактированы для демонстрации и обезличивания. Карта схематична. Это не точные скриншоты финальной версии и не подтверждение доступности функций в публичном APK.</p></aside>'
