#!/usr/bin/env python3
"""Inject shared mobile header/nav and responsive CSS into all CPF pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = [
    "index.html",
    "entretien-pac.html",
    "installation-pac.html",
    "isolation.html",
    "contact.html",
    "about.html",
    "mentions-legales.html",
]

NAV_ITEMS = [
    ("index.html", "Accueil"),
    ("entretien-pac.html", "Entretien PAC"),
    ("installation-pac.html", "Installation PAC"),
    ("isolation.html", "Isolation"),
    ("contact.html", "Contact"),
]

MOBILE_CSS = """
/* ---- mobile navigation ---- */
.nav-toggle{display:none;align-items:center;justify-content:center;width:44px;height:44px;border:1.5px solid var(--line);border-radius:4px;background:#fff;color:var(--text-dark);cursor:pointer;flex-shrink:0;padding:0;}
.phone-icon{display:none;align-items:center;justify-content:center;width:44px;height:44px;border:1.5px solid var(--line);border-radius:4px;color:var(--navy);flex-shrink:0;}
.utility-hours-mobile{display:none;font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:rgba(255,255,255,0.75);}
.nav-overlay{position:fixed;inset:0;background:rgba(11,21,34,0.52);z-index:150;opacity:0;visibility:hidden;transition:opacity .2s ease,visibility .2s ease;}
body.menu-open .nav-overlay{opacity:1;visibility:visible;}
.nav-mobile{position:fixed;top:0;right:0;width:min(320px,100%);height:100%;background:#fff;z-index:160;padding:16px 20px 28px;display:flex;flex-direction:column;gap:2px;box-shadow:-10px 0 40px rgba(0,0,0,0.18);transform:translateX(100%);transition:transform .25s ease;overflow-y:auto;}
body.menu-open .nav-mobile{transform:translateX(0);}
.nav-mobile[hidden]{display:flex;}
.nav-mobile-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid var(--line);}
.nav-mobile-header span{font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:var(--orange);letter-spacing:0.04em;}
.nav-close{display:flex;align-items:center;justify-content:center;width:44px;height:44px;border:1.5px solid var(--line);border-radius:4px;background:#fff;cursor:pointer;color:var(--text-dark);}
.nav-mobile a{display:flex;align-items:center;min-height:44px;padding:10px 0;font-size:0.95rem;font-weight:500;color:var(--text);border-bottom:1px solid var(--line);}
.nav-mobile a.active,.nav-mobile a:hover{color:var(--text-dark);}
.nav-mobile-phone{display:flex;align-items:center;gap:10px;min-height:44px;margin-top:12px;padding:12px 0;font-family:'IBM Plex Mono',monospace;font-weight:600;color:var(--navy);border-top:1px solid var(--line);}
.nav-mobile .btn{margin-top:12px;min-height:44px;justify-content:center;width:100%;}

@media(max-width:900px){
  .nav-desktop{display:none;}
  .nav-toggle{display:flex;}
  .phone-icon{display:flex;}
  .phone-badge{display:none;}
}

@media(max-width:600px){
  .utility-bar{font-size:0.72rem;}
  .utility-inner{padding:6px 16px;justify-content:flex-start;}
  .utility-tag{display:none;}
  .utility-right .utility-hours-full,.utility-zone{display:none;}
  .utility-hours-mobile{display:block;}
  .header-inner{padding:8px 16px;gap:10px;min-height:56px;}
  .logo img{height:32px !important;}
  .logo-text{font-size:0.9rem;line-height:1.1;}
  .logo-text small{display:none;}
  .header-cta{gap:8px;}
  .btn-devis{padding:10px 14px;font-size:0.8rem;min-height:44px;}
  .hero{padding-bottom:56px;}
  .hero h1{font-size:clamp(1.65rem,7vw,2.9rem);}
  .page-hero{padding-bottom:48px;}
  .page-hero h1{font-size:clamp(1.55rem,6.5vw,2.3rem);}
  .footer-grid{grid-template-columns:1fr;}
  .contact-block{margin:0 16px 48px;padding:36px 24px;}
  .wrap{padding:0 16px;}
  .cta-band{margin-left:16px;margin-right:16px;padding:18px 16px;}
  .cta-band .btn{width:100%;justify-content:center;min-height:44px;}
}

@media(max-width:480px){
  .hero-actions,.page-hero-actions{flex-direction:column;width:100%;}
  .hero-actions .btn,.page-hero-actions .btn{width:100%;justify-content:center;min-height:44px;}
}

@media(max-width:760px){
  .photo-card::after{background:linear-gradient(180deg,rgba(11,21,34,0) 40%,rgba(11,21,34,0.95) 100%);}
  .photo-card-body h3{font-size:1rem;}
  .photo-services-row3 .photo-card-body h3{font-size:0.92rem;}
}

html,body{overflow-x:hidden;}
body.menu-open{overflow:hidden;}
"""

MOBILE_JS = """
<script>
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var closeBtn = document.querySelector('.nav-close');
  var mobileNav = document.getElementById('mobile-nav');
  var overlay = document.querySelector('.nav-overlay');
  if (!toggle || !mobileNav) return;

  function openMenu() {
    document.body.classList.add('menu-open');
    mobileNav.hidden = false;
    if (overlay) overlay.hidden = false;
    toggle.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    document.body.classList.remove('menu-open');
    mobileNav.hidden = true;
    if (overlay) overlay.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', function () {
    if (mobileNav.hidden) openMenu();
    else closeMenu();
  });
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay) overlay.addEventListener('click', closeMenu);
  mobileNav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });
})();
</script>
"""


def nav_links(active_href: str, mobile: bool = False) -> str:
    parts = []
    for href, label in NAV_ITEMS:
        active = " class=\"active\"" if href == active_href else ""
        parts.append(f'<a href="{href}"{active}>{label}</a>')
    return "\n      ".join(parts)


def header(filename: str, logo_img: str) -> str:
    active = filename
    desktop_nav = nav_links(active)
    mobile_nav = nav_links(active)

    return f'''<div class="utility-bar"><div class="utility-inner">
    <span class="utility-tag">INTERVENTIONS&nbsp;/&nbsp;RÉPARATIONS</span>
    <span class="utility-hours-mobile">9h–17h · Lun–Ven</span>
    <div class="utility-right">
      <span class="utility-hours-full">Horaires : <b>9h–17h</b>, Lundi au Vendredi</span>
      <span class="utility-zone">Zone : <b>Île-de-France</b></span>
    </div>
  </div></div>
<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      {logo_img}
      <div class="logo-text">CPF Maintenance<small>ENTRETIEN &amp; DÉPANNAGE ÉNERGIE</small></div>
    </a>
    <nav class="nav-desktop">
      {desktop_nav}
    </nav>
    <div class="header-cta">
      <a class="phone-icon" href="tel:+33180925326" aria-label="Appeler le 01 80 92 53 26">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
      </a>
      <div class="phone-badge"><b>01 80 92 53 26</b><span>Lun–Ven · 9h–17h</span></div>
      <a class="btn btn-orange btn-devis" href="contact.html">Devis gratuit</a>
      <button class="nav-toggle" type="button" aria-label="Ouvrir le menu" aria-expanded="false">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <div class="nav-overlay" hidden></div>
  <nav class="nav-mobile" id="mobile-nav" hidden>
    <div class="nav-mobile-header">
      <span>MENU</span>
      <button class="nav-close" type="button" aria-label="Fermer le menu">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
    {mobile_nav}
    <a class="nav-mobile-phone" href="tel:+33180925326">01 80 92 53 26</a>
    <a class="btn btn-orange" href="contact.html">Devis gratuit</a>
  </nav>
</header>'''


def patch_css(html: str) -> str:
    html = re.sub(r"nav\{display:flex;gap:2px;\}", ".nav-desktop{display:flex;gap:2px;}", html)
    html = re.sub(
        r"nav a\{font-size:0\.86rem;font-weight:500;color:var\(--text\);padding:10px 14px;border-bottom:2px solid transparent;\}",
        ".nav-desktop a{font-size:0.86rem;font-weight:500;color:var(--text);padding:10px 14px;border-bottom:2px solid transparent;}",
        html,
    )
    html = re.sub(
        r"nav a\.active,nav a:hover\{color:var\(--text-dark\);border-bottom-color:var\(--orange\);\}",
        ".nav-desktop a.active,.nav-desktop a:hover{color:var(--text-dark);border-bottom-color:var(--orange);}",
        html,
    )
    html = re.sub(r"@media\(max-width:900px\)\{\s*nav\{display:none;\}\s*\}", "", html)

    marker = "@media (prefers-reduced-motion: reduce)"
    if "/* ---- mobile navigation ---- */" not in html:
        html = html.replace(marker, MOBILE_CSS + marker)

    return html


def patch_file(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    filename = path.name

    logo_match = re.search(r"<a href=\"index\.html\" class=\"logo\">(.*?</a>)", html, re.S)
    if not logo_match:
        raise ValueError(f"Logo not found in {filename}")
    logo_inner = logo_match.group(1)
    img_match = re.search(r"<img[^>]+>", logo_inner)
    logo_img = img_match.group(0) if img_match else ""

    html = patch_css(html)

    new_header_block = header(filename, logo_img)
    html = re.sub(
        r"<div class=\"utility-bar\">.*?</header>",
        new_header_block,
        html,
        count=1,
        flags=re.S,
    )

    html = re.sub(r"<script>\s*\(function \(\) \{[\s\S]*?mobile-nav[\s\S]*?</script>\s*", "", html)
    if "document.body.classList.add('menu-open')" not in html:
        html = html.replace("</body>", MOBILE_JS + "\n</body>")

    path.write_text(html, encoding="utf-8")
    print(f"Patched {filename}")


def main() -> None:
    for name in PAGES:
        patch_file(ROOT / name)


if __name__ == "__main__":
    main()
