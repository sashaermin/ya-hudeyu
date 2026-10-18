#!/usr/bin/env python3
"""Optional maintainer tool: WOFF2 compression, no glyph subsetting. Keep original TTF/OFL."""
from pathlib import Path
from fontTools.ttLib import TTFont
root=Path(__file__).resolve().parents[1]
for path in (root/'assets/fonts').glob('*.ttf'):
    font=TTFont(path)
    font.flavor='woff2'
    font.save(path.with_suffix('.woff2'))
