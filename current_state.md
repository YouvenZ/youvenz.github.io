<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║                     RECURSIVE TASK TRACKING DOCUMENT                        ║
║                                                                              ║
║  HOW THIS FILE WORKS (READ BEFORE EDITING)                                   ║
║                                                                              ║
║  This file is designed to be used session-by-session by a coding agent.     ║
║  Rules:                                                                      ║
║    1. The "## Analysis" block at the top is FROZEN after the first round.    ║
║       Only update it if genuinely new structural changes occur.              ║
║    2. "## [New Tasks]" is empty at the start of each fresh session.          ║
║       Add new requests here before touching the other sections.              ║
║    3. "## Plan + Actions + Subtasks" expands with each session's new work.   ║
║    4. At the END of each session, move completed items to "## Done"          ║
║       and leave unfinished items in "## Still Not Done".                     ║
║    5. Never delete the "## Done" history - it is a permanent log.            ║
║    6. The agent should read this file FIRST in every session before starting ║
║       any work, to understand what has already been done.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# Academia Portfolio — Task Tracker

---

## Analysis (Site Audit — Frozen After Round 1)

> Audit date: 2026-04-04 | Repo: YouvenZ/youvenz.github.io | Branch: main

### Architecture Summary

| Layer | Technology | Notes |
|---|---|---|
| Static site generator | Hugo | `hugo.yaml` config |
| Theme | Custom (no Hugo theme dependency) | All layouts handcrafted |
| CSS | Custom properties dual-theme (light/dark) | `assets/css/main.css` |
| Content | Markdown + data YAML | `content/` + `data/` |
| CI/CD | GitHub Actions | `.github/workflows/` |
| Hosting | GitHub Pages | `youvenz.github.io` |

### Sections & Status at Audit

| Section | Layout | Data source | Status |
|---|---|---|---|
| Home | `layouts/index.html` | `hugo.yaml` params | ✅ Functional |
| About | `layouts/about/single.html` | `content/about/index.md` | ✅ Functional |
| Blog | `layouts/blog/list.html` + `single.html` | `content/blog/*.md` | ✅ Functional |
| CV | `layouts/cv/single.html` | `data/cv.yaml` | ⚠️ Download button 404 (no `resume.pdf`) |
| Research | `layouts/research/list.html` **only** | `data/research_areas.yaml` | 🔴 Cards not clickable; no single.html; no images |
| Projects | `layouts/projects/list.html` + `single.html` | `content/projects/*.md` | ⚠️ All thumbnails empty; extensions bundled |
| Publications | `layouts/publications/list.html` | `data/publications.yaml` | ✅ Functional (pipeline source wrong) |
| Talks | `layouts/talks/list.html` **only** | `data/talks.yaml` | ⚠️ No YouTube embed; no image/gif support |
| Videos | `layouts/videos/list.html` | `data/videos.yaml` | ✅ Functional (pipeline needs updating) |
| Newsletter | `layouts/newsletter/single.html` | `data/newsletter_issues.yaml` | ⚠️ Issues all commented out |
| Contact | `layouts/contact/single.html` | Form → Formspree | ⚠️ Formspree ID is placeholder |
| Tags | `layouts/tags/list.html` | Auto taxonomy | ✅ Functional |

### Key Files

| File | Role |
|---|---|
| `assets/css/main.css` | All styles; CSS custom properties for theming |
| `layouts/_default/baseof.html` | Master HTML shell |
| `layouts/partials/header.html` | Nav + dark-mode toggle |
| `layouts/partials/sections/hero.html` | Home hero block |
| `data/research_areas.yaml` | 7 research areas (no `image` or `link` fields yet) |
| `data/talks.yaml` | 3+ talks (`slides` and `video` fields are empty strings) |
| `scripts/update_publications.py` | Uses Semantic Scholar API — needs rewriting for Google Scholar |
| `scripts/youtube_channel_metadata_pipeline.py` | yt-dlp → CSV; only needs channel ID |
| `scripts/csv_to_videos_yaml.py` | CSV → `data/videos.yaml` |
| `scripts/update_videos.py` | Old YouTube Data API v3 approach — superseded |

---

## [New Tasks]

> Add new user requests here at the start of each new session.
> Leave this section empty when there are no new additions.

_— (empty — first round) —_

---

## Plan + Actions + Subtasks

---

### TASK 1 — Placeholder Images & Links

**Source:** `note.md` rule: "each time you do not have the data (image, link, etc.) use a real placeholder image generated from a svg or from the internet."

**Why it matters:** Project thumbnails, research images, talk images are all empty or missing — the grid pages show blank cards.

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 1.1 | Generate SVG placeholder logos for each project | `static/img/projects/` | Create SVG files (distinct per project topic) |
| 1.2 | Update each project `.md` `thumbnail` param | `content/projects/*.md` | Set `thumbnail: /img/projects/<name>.svg` |
| 1.3 | Generate SVG placeholder images for each research area | `static/img/research/` | Create SVG files (one per research area) |
| 1.4 | Add `image` field to research_areas.yaml | `data/research_areas.yaml` | Add `image: /img/research/<slug>.svg` |
| 1.5 | Generate placeholder image for OG default | `static/img/og-default.png` | Create or fetch a default OG image |

---

### TASK 2 — Research Section: Clickable Cards + Deep-Dive Pages

**Source:** `note.md`: "Each element should be clickable and lead to a note where we explain deeper the research associated to the element. Possibility to have an image/gif for each theme."

**Current state:** `layouts/research/list.html` renders static cards. No `<a>` links. No `single.html`. `content/research/` has only `_index.md`.

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 2.1 | Add `slug` field to each entry in `data/research_areas.yaml` | `data/research_areas.yaml` | Add `slug: <kebab-name>` per area |
| 2.2 | Create individual research content pages (7 areas) | `content/research/<slug>.md` | Create one `.md` per area with detailed explanation, references, methodology |
| 2.3 | Create `layouts/research/single.html` | `layouts/research/single.html` | **New file** — template for individual research note page (title, image, body, tags, back link) |
| 2.4 | Update `layouts/research/list.html` to wrap cards in `<a>` | `layouts/research/list.html` | Wrap each research card with `<a href="/research/{{ .slug }}/">` |
| 2.5 | Add `image` field support to research cards | `layouts/research/list.html` | Render `<img>` or `<video>` tag if `image` field is set |
| 2.6 | Add `image` field to `data/research_areas.yaml` | `data/research_areas.yaml` | Add `image` field (links to `static/img/research/<slug>.svg`) |

---

### TASK 3 — UI: Obsidian Dark Theme

**Source:** `note.md` UI section: "Use the dark of Obsidian for the theme and make it more elegant and outstanding in terms of design, this should not be considered to be a website built with a LLM and icons generated by LLM."

**Current state:** Dark mode uses `#09090b` background + `#60a5fa` blue accent. Generic/minimal aesthetic.

**Target aesthetic:**
- Obsidian background: `#1e1e2e` (Catppuccin Mocha / Obsidian base)
- Panel/card backgrounds: `#313244` / `#181825`
- Primary accent: `#cba6f7` / `#a78bfa` (lavender/violet — Obsidian default)
- Secondary accent: `#89b4fa` (sapphire blue for links)
- Text: `#cdd6f4` (main), `#bac2de` (subtext)
- Borders: `#45475a`
- Code/mono: `#a6e3a1` (green) on `#1e1e2e`

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 3.1 | Rewrite dark-mode CSS custom properties | `assets/css/main.css` | Replace `[data-theme="dark"]` vars with Obsidian palette |
| 3.2 | Improve default dark typography + contrast | `assets/css/main.css` | Refine `font-size`, `line-height`, heading weight, letter-spacing on dark |
| 3.3 | Improve card design on dark mode | `assets/css/main.css` | Add subtle gradient borders or glow on `.card:hover` using violet accent |
| 3.4 | Improve nav/header dark mode | `assets/css/main.css` + `layouts/partials/header.html` | Glassmorphism-style header with `backdrop-filter: blur` on dark |
| 3.5 | Improve tag/badge styling on dark | `assets/css/main.css` | Tags with violet tint instead of blue, add pill shape refinements |
| 3.6 | Improve hero section design | `layouts/partials/sections/hero.html` + `assets/css/main.css` | More polished avatar treatment, gradient text for name |
| 3.7 | Set dark mode as default | `assets/js/main.js` | Check existing logic; ensure dark is the default (not light) on first visit |

---

### TASK 4 — CV: Fix Download Button

**Source:** `note.md` cv section: "The download button is not working cause there is no cv. Should it be put in assets? Add a placeholder pdf named: resume.pdf."

**Current state:** `layouts/cv/single.html` and `hugo.yaml` both reference `/cv.pdf` but no PDF exists in `static/`.

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 4.1 | Create placeholder `resume.pdf` in `static/` | `static/resume.pdf` | Generate a minimal valid PDF (single-page placeholder) using Python `fpdf2` or a binary-safe minimal PDF |
| 4.2 | Update `hugo.yaml` `social.cv` to `/resume.pdf` | `hugo.yaml` | Change `cv: "/cv.pdf"` → `cv: "/resume.pdf"` |
| 4.3 | Verify `layouts/cv/single.html` download href | `layouts/cv/single.html` | Ensure button uses `{{ .Site.Params.social.cv }}` or hardcoded `/resume.pdf` |
| 4.4 | Fix `content/cv/index.md` title casing | `content/cv/index.md` | Change `title: "Cv"` → `title: "CV"` |

---

### TASK 5 — Projects: Split Inkscape Extensions + Add Images/Logos

**Source:** `note.md` projects section: "Each extension should have its own project. An image/logo can be added for each project."

**Current state:** All 8+ Inkscape extensions are described in one monolithic `content/projects/inkscape-extensions.md`.

Known extensions (from blog posts and existing project file):
1. LLM Text Generator for Inkscape
2. AI Image Generator for Inkscape (Stable Diffusion / DALL·E)
3. AI SVG Generator for Inkscape
4. D2 Diagrams extension for Inkscape
5. Mermaid Diagrams extension for Inkscape
6. Matplotlib Figure extension for Inkscape
7. Next Generator (general purpose extension)
8. TexText wrapper (LaTeX rendering)

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 5.1 | Read `content/projects/inkscape-extensions.md` to extract all extensions | `content/projects/inkscape-extensions.md` | Audit existing content for extension names, descriptions, links |
| 5.2 | Create individual project `.md` for each extension | `content/projects/inkscape-<ext>.md` × 8 | One file per extension with proper frontmatter (`title`, `status`, `thumbnail`, `github`, `tags[]`, `description`) |
| 5.3 | Create SVG logos per extension | `static/img/projects/inkscape-<ext>.svg` | Inline SVG placeholder logo for each (or fetch from GitHub) |
| 5.4 | Delete (or archive) the monolithic `inkscape-extensions.md` | `content/projects/inkscape-extensions.md` | Remove or keep as a "suite overview" page — decide based on content |
| 5.5 | Add real logos for non-extension projects | `static/img/projects/` | MARIO, MedFlowAssist, Auto-Publication-List logos |

---

### TASK 6 — Talks: YouTube Embed + Image/GIF Support

**Source:** `note.md` talks section: "possibility to add youtube video associated to the event or simply image or gif."

**Current state:** `layouts/talks/list.html` renders `.video` as a plain `<a>` link. No embed, no image, no gif support.

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 6.1 | Add `image` field to `data/talks.yaml` schema | `data/talks.yaml` | Add `image: ""` field to each talk entry |
| 6.2 | Update `layouts/talks/list.html` to embed YouTube | `layouts/talks/list.html` | If `.video` contains `youtube.com` or `youtu.be`, render `<iframe>` embed instead of plain link |
| 6.3 | Update `layouts/talks/list.html` to show image/gif | `layouts/talks/list.html` | If `.image` is set, render `<img>` or `<video>` in the talk card |
| 6.4 | (Optional) Create `layouts/talks/single.html` | `layouts/talks/single.html` | **New file** — richer individual talk page (full abstract, embed, slides download). Only needed if content-driven talks are desired. |

---

### TASK 7 — GitHub Actions: Google Scholar Publications Pipeline

**Source:** `note.md` github action section: "Use my Google profile directly to update my publications, scrape my publication based on my Google Scholar ID. I used the export all feature of Google Scholar. Can you automatically go there with headless scraping? https://scholar.googleusercontent.com/citations?view_op=export_citations&user=iWgYuY0AAAAJ... If required I can use my Google Scholar ID — that's it, the other ID is changing."

**Current state:** `scripts/update_publications.py` uses Semantic Scholar API. The GitHub workflow sets `SEMANTIC_SCHOLAR_AUTHOR_ID`.

**Known Scholar ID:** `iWgYuY0AAAAJ`

**Approach:** The Google Scholar export endpoint (`view_op=export_citations`) requires a fresh `citsig` token per session (it changes). The stable approach is:
- Use the **`scholarly`** Python library which handles Google Scholar scraping and provides citations export, OR
- Use a headless browser (Playwright) to load the Scholar profile and trigger the export — but `citsig` changes each session
- Most robust: use `scholarly` to fetch all publications by Scholar ID, parse into structured data matching `publications.yaml` schema

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 7.1 | Rewrite `scripts/update_publications.py` | `scripts/update_publications.py` | Use `scholarly` library: `search_author_id('iWgYuY0AAAAJ')`, fill publications, write to `data/publications.yaml` |
| 7.2 | Update `requirements.txt` | `scripts/requirements.txt` | Add `scholarly`, `fake-useragent` (for Scholar anti-bot); remove Semantic Scholar deps if not needed |
| 7.3 | Update GitHub Actions workflow | `.github/workflows/update_publications.yml` | Replace `SEMANTIC_SCHOLAR_AUTHOR_ID` env var with `GOOGLE_SCHOLAR_ID: iWgYuY0AAAAJ` (or hardcode); install new requirements |
| 7.4 | Handle BibTeX parsing from Scholar export | `scripts/update_publications.py` | Parse `scholarly` publication dicts → `publications.yaml` fields (`title`, `authors`, `venue`, `year`, `doi`, `citations`, `abstract`, `bibtex`) |
| 7.5 | Test locally before pushing | — | Run script manually: `python scripts/update_publications.py` |

---

### TASK 8 — YouTube Pipeline: Replace API Key Approach with yt-dlp Pipeline

**Source:** `note.md` youtube section: "The pipeline should be: youtube_channel_metadata_pipeline (to produce the csv) + csv_to_videos_yaml (to use the csv and create the videos.yaml data for the website). No need to add the state of the pipeline GitHub workflow on the website."

**Current state:** GitHub Actions `update_videos.yml` calls `scripts/update_videos.py` (YouTube Data API v3 key). The desired pipeline is `yt-dlp` based (no API key needed).

| # | Subtask | File(s) to change | Action |
|---|---|---|---|
| 8.1 | Update GitHub Actions `update_videos.yml` | `.github/workflows/update_videos.yml` | Replace `python scripts/update_videos.py` with: (1) `python scripts/youtube_channel_metadata_pipeline.py` then (2) `python scripts/csv_to_videos_yaml.py` |
| 8.2 | Remove `YOUTUBE_API_KEY` secret dependency | `.github/workflows/update_videos.yml` | Only `YOUTUBE_CHANNEL_ID` (or hardcode `UCpT8vuVv62-VWoy8wTsABsw`) needed |
| 8.3 | Verify `youtube_channel_metadata_pipeline.py` accepts channel ID as env var | `scripts/youtube_channel_metadata_pipeline.py` | Read script; ensure it reads `YOUTUBE_CHANNEL_ID` or accepts CLI arg |
| 8.4 | Verify `csv_to_videos_yaml.py` output path | `scripts/csv_to_videos_yaml.py` | Ensure it writes to `data/videos.yaml` (not a temp path) |
| 8.5 | Remove pipeline status display from website | `layouts/` (search for pipeline status) | Find and remove any "pipeline status" badge or section from layouts |

---

## Done

> Session 2 completed: 2026-04-04

### ✅ TASK 4 — CV Download Button
- 4.1 Created `static/resume.pdf` (minimal valid placeholder PDF)
- 4.2 Updated `hugo.yaml` `social.cv` from `/cv.pdf` → `/resume.pdf`
- 4.3 Fixed `layouts/cv/single.html` download href to use `{{ .Site.Params.social.cv }}`
- 4.4 Fixed `content/cv/index.md` title "Cv" → "CV"

### ✅ TASK 8 — YouTube Pipeline: yt-dlp approach
- 8.1 Updated `.github/workflows/update_videos.yml` to call `youtube_channel_metadata_pipeline.py` then `csv_to_videos_yaml.py`
- 8.2 Removed `YOUTUBE_API_KEY` dependency; channel ID hardcoded (`UCpT8vuVv62-VWoy8wTsABsw`)
- 8.3 Updated `scripts/youtube_channel_metadata_pipeline.py` to read `YOUTUBE_CHANNEL_ID` env var
- 8.5 Removed pipeline status badges from `layouts/about/single.html`

### ✅ TASK 2 — Research: Clickable Cards + Individual Pages
- 2.1 Added `slug` field to all 8 entries in `data/research_areas.yaml`
- 2.2 Created 8 individual research content pages in `content/research/`
- 2.3 Created `layouts/research/single.html`
- 2.4–2.5 Updated `layouts/research/list.html`: cards are now `<a>` links with image support
- 2.6 Added `image` field to all research_areas entries

### ✅ TASK 5 — Projects: Split Inkscape Extensions
- 5.1–5.2 Created 8 individual project pages: `inkscape-svg-maker`, `inkscape-mermaid`, `inkscape-d2`, `inkscape-textgen`, `inkscape-imagegen`, `inkscape-plt`, `inkscape-poster-utils`, `inkscape-loadrefs`
- 5.3 Created SVG logos for each extension in `static/img/projects/`
- 5.4 Original `content/projects/inkscape-extensions.md` kept as suite overview page

### ✅ TASK 6 — Talks: YouTube Embed + Image/GIF Support
- 6.1 Added `image: ""` field to all talk entries in `data/talks.yaml`
- 6.2 Updated `layouts/talks/list.html`: YouTube URLs auto-embed as `<iframe>`
- 6.3 Updated layout: `image` field renders `<img>` or `<video>` in talk card
- Added `.talk-media`, `.talk-media-embed` CSS classes

### ✅ TASK 7 — Publications: Google Scholar Pipeline
- 7.1 Rewrote `scripts/update_publications.py`: replaced Semantic Scholar → `scholarly` library
- 7.2 `scholarly` already in `scripts/requirements.txt`
- 7.3 Updated `.github/workflows/update_publications.yml`: `GOOGLE_SCHOLAR_ID: iWgYuY0AAAAJ`
- Scholar ID hardcoded as `iWgYuY0AAAAJ`

### ✅ TASK 3 — Obsidian Dark Theme
- 3.1 Rewrote `[data-theme="dark"]` CSS vars: Catppuccin Mocha palette (`#1e1e2e` bg, `#cba6f7` accent)
- 3.2 Added dark typography improvements and link colour overrides
- 3.3 Added violet border glow on card hover in dark mode
- 3.4 Glassmorphism header (`backdrop-filter: blur(16px)`) on dark
- 3.5 Tags with violet tint (`#2a1f4a` bg, `#cba6f7` text) on dark
- 3.6 Hero name gets gradient text (violet→blue→green) via `.hero-name-gradient`
- 3.7 Dark mode set as default: inline script in `<head>`, JS default changed

### ✅ TASK 1 — Placeholder Images
- 1.1–1.3 Created 8 SVG placeholders in `static/img/research/` and 8 in `static/img/projects/`
- 1.4 `image` fields already added in TASK 2

---

> Session 3 completed: 2026-04-05

### ✅ CV Teaching + Service Sections
- Added `teaching` and `service` rendering blocks to `layouts/cv/single.html`
- Both sections driven by existing `data/cv.yaml` entries

### ✅ Giscus Initial Dark Mode Sync
- `assets/js/main.js`: added `window.addEventListener('message', onGiscusReady)` to sync theme on iframe load
- Theme now applied both on first load and on toggle

### ✅ Per-Section RSS Autodiscovery
- `layouts/partials/head/seo.html`: per-section `<link rel="alternate">` tags via `OutputFormats.Get "RSS"`
- Site-wide feed retained on homepage

### ✅ TASK 5.5 — Project Thumbnails (MARIO / MedFlowAssist / Auto-Publication-List)
- Created `static/img/projects/mario-challenge.svg`
- Created `static/img/projects/medflowassist.svg`
- Created `static/img/projects/auto-publication-list.svg`
- Wired up `thumbnail` fields in respective `content/projects/*.md`

---

> Session 4 completed: 2026-04-05

### ✅ Newsletter Issues Populated
- Fetched live Substack RSS feed (`augmentedscholars.substack.com/feed`)
- Replaced all commented-out placeholders in `data/newsletter_issues.yaml` with 10 real issues (Dec 2025 → Jul 2025)

### ✅ TASK 6.4 — Talks Individual Pages (`layouts/talks/single.html`)
- Added `slug` field to all 5 entries in `data/talks.yaml`
- Created `layouts/talks/single.html` (data lookup by `slug == File.ContentBaseName`)
- Created 5 content stubs: `mario-amd-2024.md`, `latim-miccai-2024.md`, `ssl-neural-ode-2023.md`, `lmt-miccai-2023.md`, `dr-ssl-omia-2022.md`
- Updated `layouts/talks/list.html`: talk titles now link to `/talks/<slug>/`
- Added `.talk-single*` CSS classes to `assets/css/main.css`
- Build: 767 pages (+ 5 vs Session 3)

---

> Session 5 completed: 2026-04-05

### ✅ Homepage Enrichment — Active Projects Section
- Added "Active Projects" section to `layouts/index.html` (after publications)
- Queries `where .Section "projects"` filtered by `status == "active"`, shows first 3
- Added `.project-grid-home` and `.home-project-card` CSS classes to `assets/css/main.css`

### ✅ 404 Page — Search Button
- `layouts/404.html`: added "Search the site" button alongside "Go Home"
- Button triggers `#search-toggle` click to open the search overlay
- Only rendered when `site.Params.search: true`
- Added `.error-actions` CSS for button row layout

### ✅ Pagination — Page Count Display
- Created `layouts/partials/pagination.html`: custom partial showing "Page X of Y" + numbered links
- Replaced `{{ template "_internal/pagination.html" . }}` in `layouts/blog/list.html`, `layouts/tags/list.html`, and `layouts/_default/list.html`
- Added `.pagination-nav`, `.pagination-info`, `.pagination-btn` CSS classes
- Build: 767 pages, 10 paginator pages ✅

### ✅ Search Index Prefetch
- `layouts/partials/scripts.html`: added `<link rel="prefetch" href="/index.json" as="fetch" crossorigin>`
- Browser now pre-fetches the search index in the background after page load
- Removed dead `resources.Get "search-index.json"` line

---

## Still Not Done

### 🟡 Requires User Action

- [ ] Fix `hugo.yaml` `contactFormAction` — needs real Formspree ID from formspree.io
- [ ] Fix `hugo.yaml` `giscusCategoryId` — needs setup at giscus.app
- [ ] Replace `static/resume.pdf` placeholder with real CV PDF

### 🟡 Nice-to-Have

- [ ] **TASK 5.4** — Consider removing/redirecting monolithic `inkscape-extensions.md` (kept as suite overview for now)
- [ ] Add video/slides URLs to `data/talks.yaml` entries once available

---

_Last updated: 2026-04-05 | Session 5 — Homepage projects, 404 search, pagination count, search prefetch_
