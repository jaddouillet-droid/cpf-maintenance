#!/usr/bin/env python3
"""Rebuild unified HTML pages from legacy full-page files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

IMAGE_MAP = {
    "images/pac-jardin.jpg": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=900&q=80",
    "images/pac-terrasse.jpg": "https://images.unsplash.com/photo-1585777422405-47e154e27173?w=900&q=80",
    "images/isolation-combles.jpg": "https://images.unsplash.com/photo-1504307651254-37204f516a71?w=900&q=80",
    "images/fenetre-pose.jpg": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=900&q=80",
    "images/panneaux-solaires.jpg": "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=900&q=80",
}

PAGES = {
    "index.html": {
        "page": "index",
        "extras": True,
        "title": "CPF Maintenance — Chauffage, Climatisation, Rénovation énergétique",
        "description": "Dépannage, entretien et installation de pompes à chaleur, chaudières et panneaux solaires. Techniciens RGE partenaires EDF, intervention sous 24h.",
    },
    "entretien-pac.html": {
        "page": "entretien-pac",
        "extras": True,
        "title": "Entretien PAC — CPF Maintenance",
        "description": "Contrat d'entretien pompe à chaleur obligatoire. Formules Essentiel, Sérénité et Intégral. Techniciens RGE, intervention sous 24h.",
    },
    "installation-pac.html": {
        "page": "installation-pac",
        "extras": True,
        "title": "Installation PAC — CPF Maintenance",
        "description": "Installation de pompe à chaleur dimensionnée pour votre logement. Techniciens Quali-PAC, aides EDF, garantie 2 ans.",
    },
    "isolation.html": {
        "page": "isolation",
        "extras": True,
        "title": "Isolation — CPF Maintenance",
        "description": "Isolation murs, combles et sous-sol. Gain sur le DPE et réduction des factures de chauffage.",
    },
    "contact.html": {
        "page": "contact",
        "extras": False,
        "title": "Contact — CPF Maintenance",
        "description": "Contactez CPF Maintenance pour un dépannage, un devis ou une question sur votre contrat d'entretien.",
    },
    "about.html": {
        "page": "about",
        "extras": True,
        "title": "À propos — CPF Maintenance",
        "description": "15 ans d'expertise en entretien et dépannage de chauffage, climatisation et rénovation énergétique.",
    },
    "mentions-legales.html": {
        "page": "mentions-legales",
        "extras": False,
        "title": "Mentions légales — CPF Maintenance",
        "description": "Mentions légales du site CPF Maintenance.",
    },
}

HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@500;600;700&family=IBM+Plex+Mono:wght@500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
</head>
<body data-page="{page}" data-extras="{extras}">
<div id="site-header"></div>
<main>
"""

FOOT = """
</main>
<div id="site-extras"></div>
<div id="site-footer"></div>
<script src="js/layout.js"></script>
</body>
</html>
"""


def extract_main(html: str) -> str:
    """Extract content between header and footer."""
    m_start = re.search(r"</header>\s*", html, re.I)
    m_end = re.search(r"<footer", html, re.I)
    if not m_start or not m_end:
        raise ValueError("Could not find header/footer boundaries")
    content = html[m_start.end():m_end.start()].strip()
    return content


def strip_repeated_sections(content: str) -> str:
    """Remove trust, contact-block and duplicate footers from page content."""
    content = re.sub(
        r"<section class=\"trust\">.*?</section>\s*",
        "",
        content,
        flags=re.S,
    )
    content = re.sub(
        r"<section>\s*<div class=\"contact-block\">.*?</section>\s*",
        "",
        content,
        flags=re.S,
    )
    return content.strip()


def replace_images(content: str) -> str:
    for old, new in IMAGE_MAP.items():
        content = content.replace(old, new)
    content = re.sub(
        r'<img src="images/logo-cpf\.png"[^>]*>',
        '<div class="logo-mark">CPF</div>',
        content,
    )
    content = re.sub(
        r'<img src="images/qualisav\.png"[^>]*>',
        '<span class="badge cert-text">QualiSAV</span>',
        content,
    )
    content = re.sub(
        r'<img src="images/partenaire-edf\.png"[^>]*>',
        '<span class="badge cert-text">Partenaire EDF</span>',
        content,
    )
    content = re.sub(
        r'<img src="images/logo-[^"]+\.png"[^>]*>',
        "",
        content,
    )
    return content


def build_page(filename: str, meta: dict) -> str:
  legacy = (ROOT / f"_legacy_{filename}")
  source = legacy if legacy.exists() else (ROOT / filename)
  html = source.read_text(encoding="utf-8")
  main = strip_repeated_sections(extract_main(html))
  main = replace_images(main)
  extras = "true" if meta["extras"] else "false"
  return HEAD.format(
      title=meta["title"],
      description=meta["description"],
      page=meta["page"],
      extras=extras,
  ) + main + FOOT


def main():
    # Backup originals once
    for filename in PAGES:
        path = ROOT / filename
        legacy = ROOT / f"_legacy_{filename}"
        if path.exists() and not legacy.exists():
            legacy.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    for filename, meta in PAGES.items():
        out = build_page(filename, meta)
        (ROOT / filename).write_text(out, encoding="utf-8")
        print(f"Built {filename}")


if __name__ == "__main__":
    main()
