# flowerhornhobby.com — static site

Plain HTML + one CSS file. No build step is needed to host it; upload the contents of this folder as the site root.

## Pages
/  ·  /origins/  ·  /breeding/  ·  /feng-shui/  ·  /pet-fish/  ·  /glossary/  ·  /about/  ·  /404.html

## Going live (recommended: Cloudflare Pages or Netlify, both free)
1. Create a new project and upload this folder (drag-and-drop works on both).
2. Add the custom domain flowerhornhobby.com (and www, redirecting to the apex).
3. At the domain registrar, point DNS at the host as it instructs.
4. IMPORTANT: flowerhornhobby.com currently 302-redirects to petzonesd.com/flowerhorns/. Remove that forwarding rule at the registrar, or the new site will never be seen.
5. Add the site to Google Search Console and submit https://flowerhornhobby.com/sitemap.xml.

## SEO built in
- Unique title, meta description, canonical, Open Graph/Twitter card on every page
- JSON-LD: WebSite + Organization (linked to petzonesd.com's #organization), Article with author, BreadcrumbList, FAQPage, DefinedTermSet (glossary)
- sitemap.xml, robots.txt (all crawlers allowed, AI crawlers included), 404 page (noindex)
- Cross-links to flowerhorn.co (shop) and petzonesd.com/flowerhorn-san-diego/ (local)

## Editing
Source lives in the `source/` folder next to this one: content/*.html holds page copy, src/site.css the styles, build.py regenerates dist/ (python3 build.py && python3 make_images.py).
