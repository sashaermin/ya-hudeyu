#!/usr/bin/env python3
"""Optional maintainer tool: responsive logo encodings; preserve Android originals."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'assets/brand/web';out.mkdir(exist_ok=True)
for theme in ('light','dark'):
    with Image.open(ROOT/f'assets/brand/originals/logo_wordmark_green_{theme}.png') as image:
        for width in (160,320,480):
            # Standard proportional resize only: never redraw, recolor or regenerate the brand.
            sized=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
            sized.save(out/f'wordmark-{theme}-{width}.webp','WEBP',lossless=True,method=6)
