"""Smoke test: load index.html in Chromium, build every example, run the
generated code with the real Tirotir interpreter (CPython).
Requires: pip install playwright && playwright install chromium
Usage: PYTHONPATH=/path/to/tirotir/src python tests/smoke_test.py
"""
import asyncio, pathlib
import tirotir.core as C
from tirotir.contracts import Capability as K
from playwright.async_api import async_playwright
PAGE = (pathlib.Path(__file__).resolve().parent.parent / 'index.html').as_uri()

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(PAGE); await pg.wait_for_timeout(500)
        codes = []
        n = await pg.locator('#ex option').count()
        for i in range(n - 1):
            await pg.select_option('#ex', str(i)); codes.append(await pg.inner_text('#code'))
        await b.close()
    assert not errs, errs
    for c in codes:
        out = []
        R = C.Interpreter(output=lambda *a: out.append(' '.join(map(str, a))),
                          input_fn=lambda *a: 'x', play_audio=False,
                          runtime_context=C.RuntimeContext.from_capabilities([K.GRAPHICS, K.AUDIO]))
        R.run(C.parse(c)); print('OK', out[:4])
    print('all examples passed:', len(codes))
asyncio.run(main())
