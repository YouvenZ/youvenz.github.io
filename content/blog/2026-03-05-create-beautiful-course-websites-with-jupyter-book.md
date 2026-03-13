---
title: Create Beautiful Course Websites with Jupyter Book
date: '2026-03-05'
draft: false
description: Jupyter Book transforms Markdown and Jupyter notebooks into interactive,
  web-hosted course websites where readers execute code directly in the browser. This
  tutorial covers installation, configuration, and publishing—perfect for researchers
  and educators who need updatable, executable content without constant rebuilds.
subtitle: Build interactive, executable course content that stays current without
  constant rebuilds.
image: /img/thumbnails/2026-03-05-create-beautiful-course-websites-with-jupyter-book.svg
tags:
- Jupyter Book
- course websites
- interactive content
- Markdown
- GitHub Pages
- executable notebooks
- research education
- static site generators
categories:
- academic-presence
is_series: true
article_type: tutorial
cluster: 🌐 Academic Presence
critic_score: 8.8
source_transcript: cleaned_transcripts_2026-02-27_12-21-24_Create_Beautiful_Course_Websites_with_Jupyter_Book.md
generated: 2026-03-05_07-35-35
series_part: 1
---

# Create Interactive Course Websites with Jupyter Book — For Researchers & Educators Who Need Updatable, Executable Content

Your course materials are already outdated. Your readers can't run your code examples. You can't update without rebuilding everything from scratch. Static PDFs and HTML don't cut it anymore—your audience needs to *interact* with your content, run code in the browser, and access the latest version instantly.

**Jupyter Book solves all three problems at once.**

## What Jupyter Book Does

**The 30-second pitch:** Jupyter Book transforms Markdown files and Jupyter notebooks into interactive, web-hosted course websites with executable code cells, beautiful typography, and one-command publishing to GitHub Pages. Think of it as "the missing middle ground between a static blog and a full web application"—your content stays in plain text (easy to version control), but readers get a modern, interactive experience.

**Why it matters:**

- **Readers execute code directly in the browser** — no local setup needed
- **Content updates automatically** when you push to GitHub
- **Built-in support** for LaTeX equations, callout boxes, and cross-references
- **Professional UI** with dark mode, table of contents, and PDF export
- **Multi-language support** — Python, R, Julia, Scala, and other kernels

This is especially valuable for researchers, educators, and technical teams who want their work to stay current without constant manual rebuilds.

## Prerequisites

**You'll need:**
- Python 3.8+ (with pip installed)
- Git (for version control and GitHub Pages publishing)
- A code editor (VS Code recommended)
- A GitHub account (optional for Parts 1–2, required for Part 3)
- Familiarity with Markdown syntax (basic: headers, bold, links, code blocks)

**Time investment:** 15–20 minutes for Part 1; ~1 hour for the full series.

## Installation & Setup

### Step 1: Create a Python Virtual Environment

Open your terminal and navigate to where you want your book project to live.

```bash
python -m venv jupyter_book_env
```

Activate the environment:

**macOS/Linux:**

```bash
source jupyter_book_env/bin/activate
```

**Windows:**

```bash
jupyter_book_env\Scripts\activate
```

You should see `(jupyter_book_env)` at the start of your terminal prompt.

### Step 2: Install Jupyter Book

```bash
pip install jupyter-book
```

Verify installation:

```bash
jupyter-book --version
```

### Step 3: Install Additional Packages (Recommended)

If your content uses specific libraries, install them now so code cells execute correctly:

```bash
pip install numpy pandas matplotlib scikit-learn
```

Add more packages later as needed.

### Step 4: Test Your Setup

```bash
jupyter-book create my-test-book
```

If a new folder appears with template files, you're ready to proceed.

## Core Workflow

### Step 1: Create Your Book Project

```bash
jupyter-book create my-course-site
```

This generates a folder structure:

- `_config.yml` — Title, author, theme settings
- `_toc.yml` — Table of contents (chapters and sections)
- `intro.md` — Home page (Markdown)
- `chapters/` — Your content files
- `references.bib` — Bibliography file

### Step 2: Configure Your Book

Edit **`_config.yml`**:

```yaml
title: My Data Science Course
author: Your Name
logo: logo.png
execute:
  execute_notebooks: force  # Always run code cells
```

Edit **`_toc.yml`** to define your book's structure:

```yaml
format: jb-book
chapters:
- file: intro
- file: chapters/chapter1
- file: chapters/chapter2
```

### Step 3: Build Your Book

```bash
jupyter-book build my-course-site
```

This converts Markdown/notebooks to HTML, executes code cells, and generates a table of contents.

### Step 4: View Your Book Locally

```bash
open my-course-site/_build/html/index.html
```

(Use `start` on Windows; `xdg-open` on Linux.)

### Step 5: Edit & Rebuild

Edit `.md` or `.ipynb` files, then rebuild:

```bash
jupyter-book build my-course-site
```

Refresh your browser to see changes.

## Practical Example: A Data Science Course

**Scenario:** You're teaching introductory data science and want a course website with executable Python examples.

**Step-by-step:**

1. **Create the book:**

```bash
jupyter-book create data-science-101
cd data-science-101
```

2. **Update `_config.yml`:**

```yaml
title: Data Science 101
author: Dr. Jane Smith
execute:
  execute_notebooks: force
```

3. **Update `_toc.yml`:**

```yaml
format: jb-book
chapters:
- file: intro
- file: chapters/01-numpy-basics
- file: chapters/02-pandas-intro
```

4. **Replace `intro.md`:**

```markdown
# Welcome to Data Science 101

This course teaches foundational data science skills using Python.

## What You'll Learn
- NumPy arrays and operations
- Pandas DataFrames and data manipulation
- Basic visualization with Matplotlib
```

5. **Create `chapters/01-numpy-basics.md`:**

```markdown
# NumPy Basics

NumPy is Python's numerical computing library.

```{code-cell}
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(f"Array: {arr}")
print(f"Mean: {arr.mean()}")
```
```

The `{code-cell}` syntax tells Jupyter Book this code is executable.

6. **Build and view:**

```bash
jupyter-book build .
open _build/html/index.html
```

Readers now see a professional course website where they can click a **Rocket** icon to run code cells in the browser—no local setup required.

## Troubleshooting

### Code cells don't execute in the browser

**Fix:** Update `_config.yml`:

```yaml
execute:
  execute_notebooks: force
```

Then rebuild with `--all`:

```bash
jupyter-book build my-course-site --all
```

### Build fails with "module not found"

**Fix:** Install missing packages in your virtual environment:

```bash
pip install numpy pandas matplotlib
```

Then rebuild.

### Changes don't appear after rebuild

**Fix:** Hard refresh your browser (Cmd+Shift+R on macOS; Ctrl+Shift+R on Windows/Linux).

> ⚠️ **Note:** First builds take longer because Jupyter Book executes all code cells. Use `execute_notebooks: cache` in `_config.yml` for faster subsequent builds.

## What's Next

You now have a working Jupyter Book that builds locally and displays beautifully.

**In Part 2**, we'll cover:
- Writing rich content with **MyST Markdown** (callout boxes, equations, cross-references)
- Embedding interactive plots with **IPyWidgets**
- Adding citations with BibTeX
- Customizing the look and feel

**In Part 3**, we'll automate publishing:
- Push your book to GitHub
- Set up GitHub Actions to rebuild automatically
- Host on GitHub Pages (free, no server setup)

For now, experiment with the template. Add a few chapters, try executable code cells, and get comfortable with the build process.

---

**What's your biggest pain point with sharing course materials or research documentation right now—is it keeping content updated, making it interactive, or something else?** Reply and let me know.

---

*What's your current workflow for hosting course materials, and what's the biggest pain point you face when updating them?*
