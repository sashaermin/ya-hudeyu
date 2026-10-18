#!/usr/bin/env python3
"""Debian 13 amd64 QA libraries without system installation; apt trust checks stay enabled."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess

PACKAGES=['libgtk-4-1','libgraphene-1.0-0','libharfbuzz-icu0','libmanette-0.2-0','libhyphen0','libgles2','libcairo-script-interpreter2','libhidapi-hidraw0','libglvnd0','liblzo2-2']

def prepare(root, webkit=None):
    root=root.resolve()
    if not root.is_relative_to(Path('/tmp')) or root==Path('/tmp'):
        raise ValueError('Use a dedicated QA directory below /tmp')
    if platform.machine()!='x86_64' or 'VERSION_ID="13"' not in Path('/etc/os-release').read_text():
        raise ValueError('This helper is for the verified Debian 13 amd64 cloud environment')
    marker=root/'.ya-hudeyu-qa-runtime'
    if root.exists() and not marker.exists():
        raise ValueError('Refusing to overwrite an unmanaged directory')
    root.mkdir(parents=True,exist_ok=True);marker.touch()
    for directory in ['conf.d','sources.list.d','lists/partial','archives/partial','downloads','lib-root']:
        (root/directory).mkdir(parents=True,exist_ok=True)
    config=root/'apt.conf'
    config.write_text('\n'.join(f'Dir::{key} "{root/value}";' for key,value in [('Etc::parts','conf.d'),('Etc::sourcelist','sources.list'),('Etc::sourceparts','sources.list.d'),('State::lists','lists'),('Cache::archives','archives')])+'\n')
    (root/'sources.list').write_text('deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main\n')
    environment=dict(os.environ,APT_CONFIG=str(config))
    subprocess.run(['apt-get','-o','APT::Update::Error-Mode=any','update'],env=environment,check=True)
    subprocess.run(['apt-get','download',*PACKAGES],cwd=root/'downloads',env=environment,check=True)
    manifest=[]
    for package in sorted((root/'downloads').glob('*.deb')):
        metadata=subprocess.check_output(['dpkg-deb','-f',str(package),'Package','Version','Architecture'],text=True)
        manifest.append({'file':package.name,'metadata':metadata.strip(),'sha256':hashlib.sha256(package.read_bytes()).hexdigest()})
        subprocess.run(['dpkg-deb','-x',str(package),str(root/'lib-root')],check=True)
    (root/'packages.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if webkit:
        webkit=webkit.resolve()
        if not webkit.is_relative_to(Path('/tmp')) or not (webkit/'pw_run.sh').is_file():
            raise ValueError('Expected the downloaded Playwright WebKit checkout below /tmp')
        destination=webkit/'minibrowser-wpe/sys/lib';destination.mkdir(parents=True,exist_ok=True)
        for library in (root/'lib-root/usr/lib/x86_64-linux-gnu').glob('*.so*'):
            target=destination/library.name
            if target.exists() or target.is_symlink():
                # Preserve existing bundled/runtime libraries. A fresh checkout gets new links.
                continue
            target.symlink_to(library.resolve())
    print(f'Verified QA packages extracted under {root}; manifest: {root / "packages.json"}')
    print('No system package installation, TLS/signature bypass, or browser binary modification.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path('/tmp/ya-hudeyu-browser-runtime'))
    parser.add_argument('--webkit',type=Path)
    args=parser.parse_args();prepare(args.root,args.webkit)
