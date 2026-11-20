"""Package authorized media already saved by Craft's dedicated capture browser.

Only image/font bytes are read; original stylesheets/scripts are never imported.
Usage: python tools/package-captured-assets.py /path/to/Cache_Data
"""
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]
manifest = {}
destinations = {}
font_names = {'7735a0ac': 'roboto-regular', '7735a0a6': 'roboto-medium',
              '7750282a': 'oxanium-medium', '77502826': 'oxanium-semibold'}
for entry in sorted(Path(sys.argv[1]).glob('*_0')):
    with entry.open('rb') as stream:
        header = stream.read(24)
        if len(header) != 24 or struct.unpack_from('<Q', header)[0] != 0xfcfb6d1ba7725c30:
            continue
        key = stream.read(struct.unpack_from('<I', header, 12)[0]).decode(errors='ignore')
        match = re.search(r'https://(?:www\.bhr-is\.nl|use\.typekit\.net)/\S+$', key)
        if not match:
            continue
        url = match.group()
        parts = urlsplit(url)
        if not (re.search(r'\.(webp|png|woff2)$', parts.path) or parts.hostname == 'use.typekit.net'):
            continue
        body = stream.read()
    if body.startswith(b'RIFF') and body[8:12] == b'WEBP':
        size = struct.unpack_from('<I', body, 4)[0] + 8
    elif body.startswith(b'\x89PNG\r\n\x1a\n'):
        end = body.find(b'IEND')
        if end < 0:
            continue
        size = end + 8
    elif body.startswith(b'wOF2'):
        size = struct.unpack_from('>I', body, 8)[0]
    else:
        continue
    payload = body[:size]
    assert len(payload) == size
    if parts.hostname == 'use.typekit.net':
        name = next((v for k, v in font_names.items() if k in parts.path), None)
        if not name:
            continue
        destination = '/assets/fonts/' + name + '.woff2'
    else:
        destination = '/assets/images/' + Path(parts.path).name
    digest = hashlib.sha256(payload).hexdigest()
    if destination in destinations and destinations[destination] != digest:
        item = Path(destination)
        destination = str(item.with_stem(item.stem + '-' + digest[:8]))
    destinations[destination] = digest
    out = root / 'public' / destination.lstrip('/')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(payload)
    manifest[url] = {'path': destination, 'bytes': size, 'sha256': digest}
(root / 'assets-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Packaged {len(set(v["path"] for v in manifest.values()))} original assets.')
