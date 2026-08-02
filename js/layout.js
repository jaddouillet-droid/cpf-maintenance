(function () {
  const PHONE = '01 80 92 53 26';
  const page = document.body.dataset.page || '';

  const navItems = [
    { id: 'index', href: 'index.html', label: 'Accueil' },
    { id: 'entretien-pac', href: 'entretien-pac.html', label: 'Entretien PAC' },
    { id: 'installation-pac', href: 'installation-pac.html', label: 'Installation PAC' },
    { id: 'isolation', href: 'isolation.html', label: 'Isolation' },
    { id: 'contact', href: 'contact.html', label: 'Contact' },
  ];

  function navLink(item) {
    const active = item.id === page ? ' class="active"' : '';
    return `<a href="${item.href}"${active}>${item.label}</a>`;
  }

  function mobileNavLink(item) {
    const active = item.id === page ? ' class="active"' : '';
    return `<a href="${item.href}"${active}>${item.label}</a>`;
  }

  const headerHtml = `
<div class="utility-bar"><div class="utility-inner">
  <span class="utility-tag">INTERVENTIONS&nbsp;/&nbsp;RÉPARATIONS</span>
  <div class="utility-right">
    <span>Horaires : <b>9h–17h</b>, Lundi au Vendredi</span>
    <span>Zone : <b>Île-de-France</b></span>
  </div>
</div></div>
<header>
  <div class="header-inner">
    <a href="index.html" class="logo">
      <div class="logo-mark">CPF</div>
      <div class="logo-text">CPF Maintenance<small>ENTRETIEN &amp; DÉPANNAGE ÉNERGIE</small></div>
    </a>
    <nav class="nav-desktop">${navItems.map(navLink).join('')}</nav>
    <div class="header-cta">
      <div class="phone-badge"><b>${PHONE}</b><span>Lun–Ven · 9h–17h</span></div>
      <a class="btn btn-orange" href="contact.html">Devis gratuit</a>
      <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </div>
  <nav class="nav-mobile" hidden>${navItems.map(mobileNavLink).join('')}</nav>
</header>`;

  const trustHtml = `
<section class="trust">
  <div class="wrap">
    <div class="trust-top">
      <div class="badge-row">
        <div class="badge"><span class="dot"></span>RGE Reconnu Garant Environnement</div>
        <span class="badge cert-text">QualiSAV</span>
        <span class="badge cert-text">Partenaire EDF</span>
      </div>
      <a href="contact.html" class="service-link" style="font-size:0.82rem;">Vérifier notre certification <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg></a>
    </div>
    <div class="partners-strip">
      <span class="partner-logo">Toshiba</span>
      <span class="partner-logo">Mitsubishi</span>
      <span class="partner-logo">Daikin</span>
      <span class="partner-logo">Domofinance</span>
      <span class="partner-logo">Crédit Agricole</span>
    </div>
  </div>
</section>`;

  const contactHtml = `
<section>
  <div class="contact-block">
    <div class="contact-grid">
      <div>
        <h2>Une panne aujourd'hui ? On peut intervenir vite.</h2>
        <p>Ligne dédiée du lundi au vendredi, 9h–17h. En dehors de ces horaires, laissez vos coordonnées, un technicien vous rappelle en priorité.</p>
        <div class="contact-phone">
          <div><div class="num">${PHONE}</div><div class="hrs">Lun–Ven · 9h–17h</div></div>
        </div>
      </div>
      <div class="contact-form">
        <h3>Demande de rappel</h3>
        <input type="text" placeholder="Nom">
        <input type="tel" placeholder="Téléphone">
        <select><option>Type d'équipement</option><option>Pompe à chaleur</option><option>Chaudière</option><option>Climatiseur</option><option>Panneaux solaires</option></select>
        <button class="btn btn-orange" type="button">Être rappelé</button>
      </div>
    </div>
  </div>
</section>`;

  const footerHtml = `
<footer>
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="footer-brand">
          <div class="logo-mark">CPF</div>
          <div style="color:#fff;font-family:'IBM Plex Sans',sans-serif;font-weight:600;">CPF Maintenance</div>
        </div>
        <p>Entretien, dépannage et installation de systèmes de chauffage, climatisation et rénovation énergétique. Techniciens RGE, partenaire EDF.</p>
        <p class="mono" style="margin-top:16px;">${PHONE}</p>
        <p>Lundi – Vendredi, 9h – 17h</p>
      </div>
      <div class="footer-col">
        <h4>Navigation</h4>
        <a href="index.html">Accueil</a>
        <a href="entretien-pac.html">Entretien PAC</a>
        <a href="installation-pac.html">Installation PAC</a>
        <a href="isolation.html">Isolation</a>
        <a href="contact.html">Contact</a>
      </div>
      <div class="footer-col">
        <h4>Services</h4>
        <a href="entretien-pac.html">Entretien pompe à chaleur</a>
        <a href="installation-pac.html">Installation PAC / climatiseur</a>
        <a href="isolation.html">Isolation mur, combles, sous-sol</a>
        <a href="contact.html">Dépannage chaudière</a>
        <a href="contact.html">Panneaux photovoltaïques</a>
      </div>
      <div class="footer-col">
        <h4>Entreprise</h4>
        <a href="about.html">À propos</a>
        <a href="mentions-legales.html">Mentions légales</a>
        <a href="contact.html">Nous contacter</a>
        <a href="contact.html">Devenir partenaire</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© CPF Maintenance — Tous droits réservés</span>
      <span>RGE · Quali-PAC · Partenaire EDF</span>
    </div>
  </div>
</footer>`;

  const headerEl = document.getElementById('site-header');
  const footerEl = document.getElementById('site-footer');
  const extrasEl = document.getElementById('site-extras');

  if (headerEl) headerEl.innerHTML = headerHtml;
  if (footerEl) footerEl.innerHTML = footerHtml;

  const showExtras = document.body.dataset.extras === 'true';
  if (extrasEl && showExtras) {
    extrasEl.innerHTML = trustHtml + contactHtml;
  }

  const toggle = document.querySelector('.nav-toggle');
  const mobileNav = document.querySelector('.nav-mobile');
  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      const open = mobileNav.hasAttribute('hidden');
      mobileNav.toggleAttribute('hidden', !open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();
