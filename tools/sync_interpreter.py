#!/usr/bin/env python3
"""Re-embed the Tirotir interpreter into index.html.
Usage: python tools/sync_interpreter.py /path/to/tirotir/src/tirotir
"""
import json, re, sys, pathlib
src = pathlib.Path(sys.argv[1])
files = ['__init__.py', 'core.py', 'contracts.py', 'audio.py', 'semantic.py']
pkg = {f: (src / f).read_text(encoding='utf-8') for f in files}
blob = json.dumps(pkg, ensure_ascii=True).replace('</', '<\\/')
page = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
html = page.read_text(encoding='utf-8')
new, n = re.subn(r'(<script type="application/json" id="pkg">).*?(</script>)',
                 lambda m: m.group(1) + blob + m.group(2), html, count=1, flags=re.S)
assert n == 1, 'pkg script tag not found'
page.write_text(new, encoding='utf-8')
print('embedded', len(blob), 'bytes from', src)
