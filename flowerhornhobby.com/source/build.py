import json, re, os, math, random, html, shutil, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content"); SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
DOMAIN = "https://flowerhornhobby.com"
UPDATED = "2026-09-16"; UPDATED_H = "September 16, 2026"
ORG_ID = "https://www.petzonesd.com/#organization"
NAV = [("", "Home"), ("origins", "Origins"), ("breeding", "Breeding"), ("feng-shui", "Feng shui"), ("pet-fish", "As a pet"), ("glossary", "Glossary"), ("about", "About")]
SEALS = {"origins": "源", "breeding": "育", "feng-shui": "福", "pet-fish": "伴", "glossary": "词", "about": "花", "404": "花"}

def load(name):
    raw = open(os.path.join(CONTENT, name), encoding="utf-8").read()
    m = re.match(r"<!--META (\{.*?\}) -->\n", raw, re.S)
    meta = json.loads(m.group(1)); meta["body"] = raw[m.end():]
    return meta

pages = {}
for f in sorted(os.listdir(CONTENT)):
    p = load(f); pages[p["slug"]] = p

def url(slug): return "/" if slug == "" else ("/404.html" if slug == "404" else f"/{slug}/")

# ---------- fish illustration ----------
def fish_svg(uid="f", anim=True, title=True):
    rnd = random.Random(7)
    body = "M95,205 C92,185 105,168 125,160 C118,118 150,62 208,60 C258,57 288,92 302,110 C362,112 432,135 472,170 C482,180 482,230 472,240 C432,280 352,302 282,302 C200,304 130,272 105,236 C98,226 94,215 95,205 Z"
    pearls = []
    for _ in range(170):
        x = rnd.uniform(110, 480); y = rnd.uniform(70, 300); r = rnd.choice([1.6, 2, 2.4, 2.8, 3.2])
        pearls.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>')
    finpearls = []
    for _ in range(40):
        x = rnd.uniform(320, 590); y = rnd.choice([rnd.uniform(80, 150), rnd.uniform(250, 320), rnd.uniform(150, 250)])
        finpearls.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([1.4,1.8,2.2])}"/>')
    flower = [(262,205,19,14,-8),(300,197,14,11,10),(334,204,13,9,-12),(366,199,10,8,8),(396,207,9,7,-6),(424,206,7,6,0),(450,210,5,4,0)]
    fl = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" transform="rotate({a} {x} {y})"/>' for x,y,rx,ry,a in flower)
    t = '<title>Illustration of a flowerhorn cichlid showing its kok, flower markings and pearling</title>' if title else ''
    cls = "fish fish-anim" if anim else "fish"
    return f'''<svg class="{cls}" viewBox="60 40 560 310" role="img" xmlns="http://www.w3.org/2000/svg">{t}
<defs>
<linearGradient id="{uid}b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B92B25"/><stop offset=".55" stop-color="#D9452F"/><stop offset="1" stop-color="#EE9A3A"/></linearGradient>
<radialGradient id="{uid}k" cx=".45" cy=".35" r=".6"><stop offset="0" stop-color="#DE4A3A"/><stop offset="1" stop-color="#BB2E27"/></radialGradient>
<linearGradient id="{uid}fin" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#C73A2C" stop-opacity=".95"/><stop offset="1" stop-color="#8E2320" stop-opacity=".75"/></linearGradient>
<clipPath id="{uid}c"><path d="{body}"/></clipPath>
</defs>
<g class="fish-body-group">
<path d="M468,168 C512,128 596,138 606,205 C598,272 512,288 468,242 C480,222 480,190 468,168 Z" fill="url(#{uid}fin)"/>
<path d="M292,110 C340,66 438,62 530,116 C540,138 506,160 472,170 C424,136 360,116 300,113 Z" fill="url(#{uid}fin)"/>
<path d="M318,296 C380,334 466,334 528,280 C516,260 494,248 472,242 C432,276 380,293 318,298 Z" fill="url(#{uid}fin)"/>
<g fill="#FFE9C9" fill-opacity=".55">{"".join(finpearls)}</g>
<path d="{body}" fill="url(#{uid}b)"/>
<path d="M125,160 C118,118 150,62 208,60 C258,57 288,92 302,110 C262,118 200,140 150,168 Z" fill="url(#{uid}k)" clip-path="url(#{uid}c)"/>
<g clip-path="url(#{uid}c)">
<g fill="#FFF3DA" fill-opacity=".62">{"".join(pearls)}</g>
<g fill="#16110F" fill-opacity=".86">{fl}</g>
<path d="M210,150 C190,190 194,240 220,274" fill="none" stroke="#7A1C18" stroke-width="3" stroke-opacity=".55"/>
</g>
<path d="M232,288 C226,320 246,346 268,340 C272,318 264,300 252,292 Z" fill="#B53226" fill-opacity=".9"/>
<path d="M204,214 C236,198 272,214 282,242 C254,254 218,244 204,214 Z" fill="#F7B35A" fill-opacity=".55"/>
<path d="M86,200 C90,190 100,188 106,196 C104,204 104,212 108,220 C98,226 88,220 86,200 Z" fill="#9E2622"/>
<circle cx="152" cy="180" r="13" fill="#F4C44A"/><circle cx="152" cy="180" r="9" fill="#C0271F"/><circle cx="150" cy="178" r="4.2" fill="#140C0B"/><circle cx="148" cy="176" r="1.4" fill="#fff"/>
</g></svg>'''

def seal_mark(ch="花"):
    return f'<span class="seal" aria-hidden="true">{ch}</span>'

# ---------- helpers ----------
def text_only(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def faqs(body):
    out = []
    for q, a in re.findall(r"<details><summary>(.*?)</summary><div>(.*?)</div></details>", body, re.S):
        out.append({"@type": "Question", "name": text_only(q), "acceptedAnswer": {"@type": "Answer", "text": text_only(a)}})
    return out

def toc(body):
    items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)
    items = [(i, t) for i, t in items if not i.startswith(("faq", "src"))]
    if len(items) < 3: return ""
    lis = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in items)
    return f'<nav class="toc" aria-label="On this page"><p class="toc-label">On this page</p><ol>{lis}</ol></nav>'

def words(body): return len(text_only(body).split())

def jsonld(p):
    slug = p["slug"]; u = DOMAIN + url(slug)
    graph = []
    org = {"@type": "Organization", "@id": ORG_ID, "name": "Pet Zone Tropical Fish", "url": "https://www.petzonesd.com/", "sameAs": ["https://flowerhorn.co/"]}
    site = {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/", "name": "Flowerhorn Hobby", "description": pages[""]["description"], "publisher": {"@id": ORG_ID}, "inLanguage": "en-US"}
    author = {"@type": "Person", "@id": DOMAIN + "/about/#roger-ma", "name": "Roger Ma", "jobTitle": "Founder, Pet Zone Tropical Fish", "worksFor": {"@id": ORG_ID}}
    if slug == "":
        graph += [site, org]
    elif p["type"] in ("article", "glossary", "about"):
        crumbs = {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": p["h1"], "item": u}]}
        if p["type"] == "article":
            graph.append({"@type": "Article", "@id": u + "#article", "headline": p["h1"], "description": p["description"], "url": u,
                          "mainEntityOfPage": u, "image": DOMAIN + "/assets/og.png", "datePublished": UPDATED, "dateModified": UPDATED,
                          "wordCount": words(p["body"]), "author": author, "publisher": {"@id": ORG_ID}, "isPartOf": {"@id": DOMAIN + "/#website"}, "inLanguage": "en-US"})
        elif p["type"] == "glossary":
            terms = re.findall(r'<div id="([^"]+)"><dt>(.*?)</dt><dd>(.*?)</dd></div>', p["body"])
            graph.append({"@type": "DefinedTermSet", "@id": u + "#terms", "name": "Flowerhorn glossary", "url": u,
                          "hasDefinedTerm": [{"@type": "DefinedTerm", "name": text_only(t), "description": text_only(d), "url": f"{u}#{i}"} for i, t, d in terms]})
        else:
            graph.append({"@type": "AboutPage", "url": u, "name": p["h1"], "about": {"@id": DOMAIN + "/#website"}, "publisher": {"@id": ORG_ID}})
            graph.append(author)
        graph.append(crumbs)
    f = faqs(p["body"])
    if f: graph.append({"@type": "FAQPage", "@id": u + "#faq", "url": u, "mainEntity": f})
    if not graph: return ""
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/") + "</script>"

def all_cjk():
    s = "".join(p["body"] for p in pages.values()) + "花罗汉" + "".join(SEALS.values())
    return "".join(sorted(set(ch for ch in s if "一" <= ch <= "鿿")))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=Shippori+Mincho+B1:wght@700;800&display=swap">'
         f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700&display=swap&text={all_cjk()}">')

def header(slug):
    cur = ' aria-current="page"'
    lis = "".join(f'<li><a href="{url(s)}"{cur if s == slug else ""}>{n}</a></li>' for s, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/">{seal_mark()}<span><span class="brand-name">Flowerhorn Hobby</span><span class="brand-sub">The luohan, explained</span></span></a>
<nav class="site-nav" aria-label="Main"><ul>{lis}</ul></nav>
</div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="wrap">
<div><a class="brand" href="/">{seal_mark()}<span><span class="brand-name">Flowerhorn Hobby</span></span></a>
<p style="margin-top:1rem;max-width:26rem">A free guide to the flowerhorn cichlid: its history, breeding, meaning and care. Published by Pet Zone Tropical Fish, San Diego, since 2007.</p></div>
<div><h2>Guides</h2><ul><li><a href="/origins/">Origins &amp; history</a></li><li><a href="/breeding/">Breeding &amp; strains</a></li><li><a href="/feng-shui/">Feng shui</a></li><li><a href="/pet-fish/">Flowerhorn as a pet</a></li><li><a href="/glossary/">Glossary</a></li></ul></div>
<div><h2>From Pet Zone</h2><ul><li><a href="https://flowerhorn.co/">Shop flowerhorns</a></li><li><a href="https://www.petzonesd.com/flowerhorn-san-diego/">Flowerhorns in San Diego</a></li><li><a href="https://www.petzonesd.com/">Pet Zone Tropical Fish</a></li><li><a href="https://www.petzonesd.com/contact-location/">Visit our stores</a></li><li><a href="/about/">About this site</a></li></ul></div>
<p class="fine">&copy; 2026 Pet Zone Tropical Fish &middot; Last updated {UPDATED_H}</p>
</div></footer>'''

def main_html(p):
    slug = p["slug"]
    if slug == "":
        head = f'''<section class="hero"><div class="wrap">
<div><p class="eyebrow">Flowerhorn cichlid &middot; <span lang="zh-Hans">花罗汉</span> huā luóhàn</p>
<h1>The flowerhorn: a fish made <em>by people, for people</em></h1>
<p class="dek">Bred in Malaysia in the 1990s, treasured across Asia as a bringer of luck, and loved by keepers everywhere as the aquarium fish that bonds like a dog. This is its story.</p>
<div class="hero-links"><a class="btn btn-solid" href="/origins/">Start with the history</a><a class="btn btn-line" href="/pet-fish/">Why it bonds with people</a></div></div>
<figure class="hero-art" style="margin:0"><p class="hanzi-column" lang="zh-Hans" aria-hidden="true"><span>花</span><span>罗</span><span>汉</span></p>{fish_svg("hero")}
<figcaption>Kok (head hump) &middot; flower (black markings) &middot; pearling (spangled scales)</figcaption></figure>
</div></section>'''
        return head + f'<main id="main" class="home"><div class="wrap prose">{p["body"]}</div></main>'
    mins = max(1, round(words(p["body"]) / 230))
    by = f'<p class="byline">By Roger Ma, Pet Zone Tropical Fish &middot; Updated {UPDATED_H} &middot; {mins} min read</p>' if p["type"] == "article" else ""
    head = f'''<header class="page-head"><div class="wrap">
<div><p class="eyebrow">{html.escape(p.get("kicker",""))}</p><h1>{p["h1"]}</h1><p class="dek">{p.get("dek","")}</p>{by}{toc(p["body"])}</div>
<p class="page-seal" lang="zh-Hans" aria-hidden="true">{SEALS.get(slug,"花")}</p>
</div></header>'''
    nxt = ""
    if p.get("next"):
        n = pages[p["next"]]
        nxt = f'<aside class="next"><div class="wrap"><a href="{url(n["slug"])}"><span class="next-label">Keep reading</span><span class="next-title">{n["h1"]}</span></a></div></aside>'
    return f'<main id="main">{head}<div class="wrap prose">{p["body"]}</div>{nxt}</main>'

def page_doc(p):
    slug = p["slug"]; u = DOMAIN + url(slug)
    robots = '<meta name="robots" content="noindex">' if slug == "404" else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{html.escape(p["title"])}</title>
<meta name="description" content="{html.escape(p["description"])}">
{robots}
<link rel="canonical" href="{u}">
<meta name="theme-color" content="#EDF1EA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1614" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="{"website" if slug=="" else "article"}">
<meta property="og:site_name" content="Flowerhorn Hobby">
<meta property="og:title" content="{html.escape(p["h1"] if slug else p["title"])}">
<meta property="og:description" content="{html.escape(p["description"])}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{DOMAIN}/assets/og.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/site.css?v=20260916">
{jsonld(p)}
</head>
<body>
{header(slug)}
{main_html(p)}
{footer()}
</body>
</html>
'''

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#A62F28"/><path d="M11,36 C10,31 13,28 17,27 C16,18 22,11 31,11 C38,11 42,16 44,19 C50,20 55,24 57,29 C58,33 58,38 56,41 C50,49 40,52 31,52 C21,52 13,46 11,40 Z" fill="#FFF6F1"/><circle cx="20" cy="31" r="2.6" fill="#A62F28"/><g fill="#A62F28"><ellipse cx="33" cy="36" rx="3.4" ry="2.6"/><ellipse cx="40" cy="35" rx="2.6" ry="2"/><ellipse cx="46" cy="36" rx="1.8" ry="1.5"/></g></svg>'''

def build():
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "assets"))
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(DIST, "assets", "site.css"))
    open(os.path.join(DIST, "favicon.svg"), "w").write(FAVICON)
    for slug, p in pages.items():
        out = os.path.join(DIST, "404.html") if slug == "404" else os.path.join(DIST, slug, "index.html") if slug else os.path.join(DIST, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(page_doc(p))
    prio = {"": "1.0", "origins": "0.9", "breeding": "0.9", "feng-shui": "0.9", "pet-fish": "0.9", "glossary": "0.6", "about": "0.4"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s, _ in NAV:
        sm.append(f"  <url><loc>{DOMAIN}{url(s)}</loc><lastmod>{UPDATED}</lastmod><priority>{prio[s]}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(DIST, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(DIST, "assets", "fish.svg"), "w").write(fish_svg("s", anim=False))

    # ---------- single-file preview for the Artifact ----------
    css = open(os.path.join(SRC, "site.css")).read()
    sections = []
    for slug, p in pages.items():
        if slug == "404": continue
        inner = header(slug) + main_html(p) + footer()
        sections.append(f'<div class="pv-page" data-route="{url(slug)}"{"" if slug=="" else " hidden"}>{inner}</div>')
    body = "\n".join(sections)
    body = re.sub(r'href="/([a-z\-]*/?)(#[^"]*)?"', lambda m: f'href="#/{m.group(1)}"', body)
    body = body.replace('id="main"', "").replace('<a class="skip" href="#/">Skip to content</a>', "").replace('<a class="skip" href="#main">Skip to content</a>', "")
    preview = f'''<title>Flowerhorn Hobby</title>
{FONTS}
<style>{css}
.pv-bar{{background:var(--ink);color:var(--ground);font:500 .75rem/1.4 var(--f-mono);letter-spacing:.04em;padding:.55rem var(--gutter);text-align:center}}
</style>
<p class="pv-bar">Preview of flowerhornhobby.com &middot; all pages clickable</p>
{body}
<script>
(function(){{
  var pages=[].slice.call(document.querySelectorAll('.pv-page'));
  function route(){{
    var h=(location.hash||'#/').slice(1); if(h.charAt(0)!=='/') return;
    var hit=pages.filter(function(p){{return p.getAttribute('data-route')===h}})[0]||pages[0];
    pages.forEach(function(p){{p.hidden=(p!==hit)}}); window.scrollTo(0,0);
  }}
  document.addEventListener('click',function(e){{
    var a=e.target.closest('a[href^="#"]'); if(!a) return;
    var h=a.getAttribute('href'); if(h.charAt(1)==='/') return;
    var t=document.querySelector('.pv-page:not([hidden]) [id="'+h.slice(1)+'"]'); if(t){{e.preventDefault(); t.scrollIntoView({{behavior:'smooth'}});}}
  }});
  window.addEventListener('hashchange',route); route();
}})();
</script>'''
    open(os.path.join(ROOT, "flowerhorn-hobby-preview.html"), "w", encoding="utf-8").write(preview)
    print("built", len(pages), "pages; cjk:", all_cjk())

build()
