#!/usr/bin/env python3
"""Package a fresh noindex draft for review; never deploy or render production."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('website_build', ROOT / 'tools/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def package(output):
    output = Path(output)
    if output.suffix != '.zip' or output.is_symlink() or output.with_suffix('.manifest.json').is_symlink():
        raise ValueError('Expected a regular .zip review output')
    output.parent.mkdir(parents=True, exist_ok=True)
    files = []
    with tempfile.TemporaryDirectory() as temporary:
        site = Path(temporary) / '_site'
        builder.build(site)  # Always fresh, allowlisted, noindex draft. Never --production.
        page = (site / 'index.html').read_text()
        if 'content="noindex,nofollow"' not in page or (site / 'robots.txt').read_text() != 'User-agent: *\nDisallow: /\n':
            raise ValueError('Review archive must retain draft indexing protection')
        with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for source in sorted(site.rglob('*')):
                if source.is_symlink():
                    raise ValueError('Symlinks must not enter the review archive')
                if not source.is_file():
                    continue
                name = source.relative_to(site).as_posix()
                content = source.read_bytes()
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content, compresslevel=9)
                files.append(dict(path=name, size_bytes=len(content), sha256=hashlib.sha256(content).hexdigest()))
    checkpoint = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip())
    manifest = dict(type='noindex website review archive; not publication approval',
                    source_commit=checkpoint, source_worktree_dirty=dirty, archive=output.name,
                    sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                    size_bytes=output.stat().st_size, files=files)
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(f'Review archive: {output}; SHA-256: {manifest["sha256"]}; no deployment')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.test-results/release-candidate/website-preview.zip')
    args = parser.parse_args()
    package(args.output)
