/* ============================================================
   Academia Portfolio — Main JavaScript
   ============================================================ */

// ---------- Theme Toggle ----------
(function () {
  const root = document.documentElement;
  const btn = document.getElementById('theme-toggle');
  const stored = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = stored || (prefersDark ? 'dark' : 'light');
  root.setAttribute('data-theme', theme);

  btn?.addEventListener('click', () => {
    const current = root.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
})();

// ---------- Mobile Menu ----------
(function () {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const nav = document.getElementById('main-nav');
  menuBtn?.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', isOpen);
  });
  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!e.target.closest('#main-nav') && !e.target.closest('#mobile-menu-btn')) {
      nav?.classList.remove('open');
      menuBtn?.setAttribute('aria-expanded', 'false');
    }
  });
})();

// ---------- Search (Fuse.js) ----------
(function () {
  const toggle = document.getElementById('search-toggle');
  const overlay = document.getElementById('search-overlay');
  const closeBtn = document.getElementById('search-close');
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  if (!toggle || !overlay) return;

  let fuse = null;
  let loaded = false;

  async function loadIndex() {
    if (loaded) return;
    loaded = true;
    try {
      const resp = await fetch(window.searchIndexURL);
      const data = await resp.json();
      const Fuse = (await import('https://cdn.jsdelivr.net/npm/fuse.js@7/dist/fuse.mjs')).default;
      fuse = new Fuse(data, {
        keys: ['title', 'summary', 'tags', 'content'],
        threshold: 0.3,
        includeScore: true,
      });
    } catch (e) { console.error('Search index load failed', e); }
  }

  function openSearch() {
    overlay.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    input?.focus();
    loadIndex();
  }
  function closeSearch() {
    overlay.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    if (results) results.innerHTML = '';
    if (input) input.value = '';
  }

  toggle.addEventListener('click', openSearch);
  closeBtn?.addEventListener('click', closeSearch);
  overlay?.addEventListener('click', (e) => { if (e.target === overlay) closeSearch(); });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeSearch();
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
  });

  input?.addEventListener('input', () => {
    if (!fuse || !results) return;
    const q = input.value.trim();
    if (!q) { results.innerHTML = ''; return; }
    const hits = fuse.search(q).slice(0, 8);
    results.innerHTML = hits.length
      ? hits.map(({ item }) => `
          <a href="${item.permalink}" class="search-result-item">
            <h4>${item.title}</h4>
            <p>${item.summary ? item.summary.slice(0, 120) : ''}</p>
          </a>`).join('')
      : '<p style="padding:12px;color:var(--text-muted)">No results found.</p>';
  });
})();

// ---------- Publication Abstract Toggle ----------
document.querySelectorAll('.pub-abstract-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const abstract = btn.nextElementSibling;
    const open = abstract?.classList.toggle('open');
    btn.textContent = open ? '▲ Hide abstract' : '▼ Show abstract';
    btn.setAttribute('aria-expanded', open);
  });
});

// ---------- BibTeX Copy ----------
document.querySelectorAll('.bibtex-copy-btn').forEach(btn => {
  btn.addEventListener('click', async () => {
    const bibtex = btn.dataset.bibtex;
    try {
      await navigator.clipboard.writeText(bibtex);
      btn.textContent = 'Copied!';
      setTimeout(() => { btn.textContent = 'Cite'; }, 2000);
    } catch (e) { console.error(e); }
  });
});

// ---------- Filter System ----------
document.querySelectorAll('.filter-bar').forEach(bar => {
  bar.addEventListener('click', (e) => {
    const btn = e.target.closest('.filter-btn');
    if (!btn) return;
    bar.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    const target = bar.dataset.target;
    document.querySelectorAll(`[data-filter-group="${target}"] [data-tags]`).forEach(item => {
      if (filter === 'all') {
        item.style.display = '';
      } else {
        const tags = JSON.parse(item.dataset.tags || '[]');
        item.style.display = tags.includes(filter) ? '' : 'none';
      }
    });
  });
});

// ---------- Active Nav Highlight ----------
// Hugo's IsMenuCurrent already sets .active on the correct item via the template.
// We only add active here for sub-pages (e.g., a blog post should highlight Blog).
(function () {
  const path = window.location.pathname;
  // Only run if Hugo hasn't already marked something active
  const alreadyActive = document.querySelector('.nav-link.active');
  if (alreadyActive) return;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    // Skip root '/' and require a real prefix match (not just any substring)
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    }
  });
})();

// ---------- Lazy Images ----------
if ('loading' in HTMLImageElement.prototype) {
  document.querySelectorAll('img[data-src]').forEach(img => {
    img.src = img.dataset.src;
  });
} else {
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/lazysizes@5/lazysizes.min.js';
  document.body.appendChild(script);
}
