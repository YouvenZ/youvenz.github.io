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

  function setGiscusTheme(theme) {
    const iframe = document.querySelector('iframe.giscus-frame');
    if (iframe) {
      iframe.contentWindow.postMessage(
        { giscus: { setConfig: { theme: theme === 'dark' ? 'dark' : 'light' } } },
        'https://giscus.app'
      );
    }
  }

  btn?.addEventListener('click', () => {
    const current = root.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    setGiscusTheme(next);
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

  let activeIdx = -1;

  function renderResults(hits) {
    results.innerHTML = '';
    activeIdx = -1;
    if (!hits.length) {
      const p = document.createElement('p');
      p.style.cssText = 'padding:12px;color:var(--text-muted)';
      p.textContent = 'No results found.';
      results.appendChild(p);
      return;
    }
    hits.forEach(({ item }) => {
      const a = document.createElement('a');
      a.href = item.permalink;
      a.className = 'search-result-item';
      const h4 = document.createElement('h4');
      h4.textContent = item.title;
      const p = document.createElement('p');
      p.textContent = item.summary ? item.summary.slice(0, 120) : '';
      a.appendChild(h4);
      a.appendChild(p);
      results.appendChild(a);
    });
  }

  function updateActiveResult() {
    const items = results.querySelectorAll('.search-result-item');
    items.forEach((el, i) => {
      el.classList.toggle('search-active', i === activeIdx);
    });
    if (items[activeIdx]) items[activeIdx].scrollIntoView({ block: 'nearest' });
  }

  input?.addEventListener('input', () => {
    if (!fuse || !results) return;
    const q = input.value.trim();
    if (!q) { results.innerHTML = ''; return; }
    const hits = fuse.search(q).slice(0, 8);
    renderResults(hits);
  });

  input?.addEventListener('keydown', (e) => {
    const items = results.querySelectorAll('.search-result-item');
    if (!items.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIdx = (activeIdx + 1) % items.length;
      updateActiveResult();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIdx = (activeIdx - 1 + items.length) % items.length;
      updateActiveResult();
    } else if (e.key === 'Enter' && activeIdx >= 0 && items[activeIdx]) {
      e.preventDefault();
      items[activeIdx].click();
    }
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

// ---------- Reading Progress Bar ----------
(function () {
  const bar = document.getElementById('reading-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const winH = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    bar.style.width = winH > 0 ? (window.scrollY / winH * 100) + '%' : '0%';
  }, { passive: true });
})();

// ---------- TOC Scrollspy ----------
(function () {
  const toc = document.querySelector('.toc');
  if (!toc) return;
  const links = toc.querySelectorAll('a');
  const ids = Array.from(links).map(a => a.getAttribute('href')?.replace('#', '')).filter(Boolean);
  const headings = ids.map(id => document.getElementById(id)).filter(Boolean);
  if (!headings.length) return;

  function update() {
    let current = '';
    for (const h of headings) {
      if (h.getBoundingClientRect().top <= 100) current = h.id;
    }
    links.forEach(a => {
      a.classList.toggle('toc-active', a.getAttribute('href') === '#' + current);
    });
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
})();

// ---------- Copy Code Button ----------
(function () {
  document.querySelectorAll('.highlight pre, .article-content pre, .prose pre').forEach(pre => {
    if (pre.querySelector('.code-copy-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.addEventListener('click', async () => {
      const code = pre.querySelector('code') || pre;
      try {
        await navigator.clipboard.writeText(code.textContent);
        btn.textContent = 'Copied!';
        setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
      } catch (e) { console.error(e); }
    });
    pre.style.position = 'relative';
    pre.appendChild(btn);
  });
})();

// ---------- Back to Top Button ----------
(function () {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();

// ---------- Social Share ----------
(function () {
  document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(document.title);
      const type = btn.dataset.share;
      const urls = {
        twitter: `https://twitter.com/intent/tweet?url=${url}&text=${title}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
        copy: null,
      };
      if (type === 'copy') {
        navigator.clipboard.writeText(window.location.href).then(() => {
          btn.textContent = 'Copied!';
          setTimeout(() => { btn.textContent = 'Copy Link'; }, 2000);
        });
        return;
      }
      if (urls[type]) window.open(urls[type], '_blank', 'width=600,height=400');
    });
  });
})();
