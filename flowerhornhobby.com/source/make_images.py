import asyncio, re
src = open('build.py').read().split("def build():")[0]
g = {"__file__": "/home/claude/fhh/build.py"}; exec(src, g)
fish = g["fish_svg"]("og", anim=False, title=False); FAV = g["FAVICON"]
og = '''<!doctype html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;background:#EDF1EA;font-family:Georgia,"DejaVu Serif",serif;color:#16201D;display:grid;grid-template-columns:600px 1fr;align-items:center;overflow:hidden}
.t{padding:0 0 0 80px} .e{font:500 20px/1 monospace;letter-spacing:.14em;text-transform:uppercase;color:#6E7D77}
h1{font-size:62px;line-height:1.04;margin:22px 0 0;font-weight:800;letter-spacing:-1px} h1 em{font-style:normal;color:#A62F28}
.u{margin-top:30px;font:500 22px monospace;color:#4B5B55}
.art{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:10px;padding:0 50px 0 30px}
.hz{display:flex;flex-direction:column;font:700 84px/1.08 "Noto Serif CJK SC","Noto Sans CJK SC",serif;color:#A62F28}
</style></head><body><div class="t"><div class="e">Flowerhorn Hobby</div><h1>A fish made <em>by people, for people</em></h1><div class="u">flowerhornhobby.com</div></div>
<div class="art"><div class="hz"><span>花</span><span>罗</span><span>汉</span></div>FISH</div></body></html>'''.replace("FISH", fish)
icon = '<!doctype html><html><body style="margin:0">' + FAV.replace("<svg ", '<svg width="180" height="180" ') + '</body></html>'
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1200,"height":630}); await pg.set_content(og); await pg.screenshot(path="dist/assets/og.png")
        pg = await b.new_page(viewport={"width":180,"height":180}); await pg.set_content(icon); await pg.screenshot(path="dist/assets/apple-touch-icon.png")
        await b.close()
asyncio.run(main())
