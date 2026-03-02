# Academia Portfolio — Hugo Website

A complete, self-maintaining academic/researcher website built with **Hugo** (v0.140+).

## Features

| Feature | Status |
|---|---|
| Responsive minimalist design | ✅ |
| Dark / light mode toggle | ✅ |
| SEO (Open Graph, Twitter Cards, JSON-LD) | ✅ |
| Fuse.js client-side search | ✅ |
| WCAG 2.1 AA accessible | ✅ |
| Publications list (filterable, BibTeX copy) | ✅ |
| Projects card grid | ✅ |
| YouTube video gallery | ✅ |
| Blog with ToC, related posts, Giscus comments | ✅ |
| Talks list | ✅ |
| Research areas + grants | ✅ |
| Newsletter page (Substack embed) | ✅ |
| CV page (HTML + PDF download) | ✅ |
| Contact page (Formspree) | ✅ |
| Custom 404 page | ✅ |
| Cookie consent banner | ✅ |
| Breadcrumbs | ✅ |
| Sitemap + robots.txt | ✅ |
| **Pipeline 1** — Auto blog post from YouTube | ✅ |
| **Pipeline 2** — Auto-update publications | ✅ |
| **Pipeline 3** — Auto-update video gallery | ✅ |

---

## Quick Start

```bash
# 1. Clone / open the repo
cd Academia_Portfolio

# 2. Start the dev server
hugo server --buildDrafts

# 3. Open http://localhost:1313
```

---

## Customisation

### 1. Identity

Edit `hugo.yaml` and update the `params` section:

```yaml
params:
  name: "Your Name"
  role: "Assistant Professor"
  institution: "Your University"
  email: "you@example.edu"
```

### 2. Avatar

Replace `assets/img/avatar.jpg` with your own photo (square, ≥400×400 px).

### 3. CV PDF

Replace `static/cv.pdf` with your actual PDF.

### 4. Education & CV Data

Edit `data/cv.yaml` and `data/education.yaml`.

### 5. Publications

Add entries to `data/publications.yaml` manually, or run the auto-update pipeline.

### 6. Videos

Add entries to `data/videos.yaml` manually, or run the auto-update pipeline.

### 7. Talks

Edit `data/talks.yaml`.

### 8. Research Areas

Edit `data/research_areas.yaml`.

### 9. Grants

Edit `data/grants.yaml`.

### 10. Newsletter Issues

Edit `data/newsletter_issues.yaml`.

---

## Automation Pipelines

All three pipelines live in `scripts/` and are triggered by GitHub Actions workflows in `.github/workflows/`.

### Required Secrets (GitHub → Settings → Secrets and Variables → Actions)

| Secret | Used by | How to obtain |
|---|---|---|
| `YOUTUBE_API_KEY` | Pipelines 1 & 3 | [Google Cloud Console](https://console.cloud.google.com/) → Create API key → enable YouTube Data API v3 |
| `ANTHROPIC_API_KEY` | Pipeline 1 | [console.anthropic.com](https://console.anthropic.com/) |
| `GH_PAT` | All pipelines | GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained → contents: write |

### Required Variables (GitHub → Settings → Secrets and Variables → Variables)

| Variable | Description |
|---|---|
| `YOUTUBE_CHANNEL_ID` | Your YouTube channel ID (e.g., `UCxxxxxxxxxx`) |
| `SEMANTIC_SCHOLAR_AUTHOR_ID` | Your numeric Semantic Scholar author ID |
| `UNPAYWALL_EMAIL` | Any valid email for Unpaywall OA PDF lookup |
| `ARXIV_AUTHOR_NAME` | e.g., `Alex Researcher` |

### Running Locally

```bash
pip install -r scripts/requirements.txt

# Pipeline 1
YOUTUBE_API_KEY=... ANTHROPIC_API_KEY=... YOUTUBE_CHANNEL_ID=... python scripts/video_to_blog.py

# Pipeline 2
SEMANTIC_SCHOLAR_AUTHOR_ID=... python scripts/update_publications.py

# Pipeline 3
YOUTUBE_API_KEY=... YOUTUBE_CHANNEL_ID=... python scripts/update_videos.py
```

---

## Deployment

### GitHub Pages (included)

The `.github/workflows/deploy.yml` workflow automatically builds and deploys to GitHub Pages on every push to `main`.

1. Go to repo **Settings → Pages** → Source: **Deploy from a branch** → Branch: `gh-pages`.
2. Update `baseURL` in `hugo.yaml` to your GitHub Pages URL.

### Netlify

1. Connect the repo to Netlify.
2. Build command: `hugo --minify`
3. Publish directory: `public`
4. Set environment variable `HUGO_VERSION` to `0.148.2`.

---

## Project Structure

```
.
├── .github/workflows/       # GitHub Actions pipelines + deploy
├── assets/
│   ├── css/main.css         # All styles
│   └── js/main.js           # Theme toggle, search, filters
├── content/                 # Markdown content
│   ├── about/
│   ├── blog/
│   ├── contact/
│   ├── cv/
│   ├── newsletter/
│   ├── projects/
│   ├── publications/
│   ├── research/
│   ├── talks/
│   └── videos/
├── data/                    # YAML data files
│   ├── cv.yaml
│   ├── education.yaml
│   ├── grants.yaml
│   ├── newsletter_issues.yaml
│   ├── publications.yaml
│   ├── research_areas.yaml
│   ├── talks.yaml
│   └── videos.yaml
├── layouts/                 # Hugo templates
│   ├── _default/
│   ├── about/
│   ├── blog/
│   ├── contact/
│   ├── cv/
│   ├── newsletter/
│   ├── partials/
│   ├── projects/
│   ├── publications/
│   ├── research/
│   ├── shortcodes/
│   ├── talks/
│   ├── videos/
│   ├── 404.html
│   └── index.html
├── logs/                    # Pipeline run logs (auto-generated)
├── scripts/                 # Automation scripts
│   ├── requirements.txt
│   ├── topics_map.yaml
│   ├── update_publications.py
│   ├── update_videos.py
│   ├── utils.py
│   └── video_to_blog.py
├── static/
│   ├── cv.pdf               # Your CV PDF
│   ├── publications.bib     # Auto-generated BibTeX
│   └── robots.txt
└── hugo.yaml                # Site configuration
```

---

## Giscus Comments

1. Install the [Giscus GitHub App](https://github.com/apps/giscus) on your repo.
2. Enable **Discussions** in repo Settings.
3. Visit [giscus.app](https://giscus.app) to get your `repoId` and `categoryId`.
4. Update `hugo.yaml`:

```yaml
params:
  giscusRepo: "yourname/yourname.github.io"
  giscusRepoId: "R_xxx"
  giscusCategory: "Comments"
  giscusCategoryId: "DIC_xxx"
```

---

## Analytics

Set **one** of the following in `hugo.yaml`:

```yaml
params:
  googleAnalytics: "G-XXXXXXXXXX"   # Google Analytics 4
  plausibleDomain: "yoursite.com"   # Plausible (privacy-friendly)
```

---

## Contact Form (Formspree)

1. Create a free account at [formspree.io](https://formspree.io).
2. Create a new form and copy the endpoint URL.
3. Update `hugo.yaml`:

```yaml
params:
  contactFormAction: "https://formspree.io/f/yourformid"
```

---

## License

MIT — feel free to adapt for your own academic website.
