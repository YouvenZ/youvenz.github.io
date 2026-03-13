---
title: Deploy Jupyter Book to GitHub Pages FREE
date: '2026-03-05'
draft: false
description: Learn how to deploy your Jupyter Book to GitHub Pages completely free
  using GitHub Actions. This step-by-step guide shows you how to automate your book's
  build and deployment—every push to main triggers a live update with zero manual
  effort.
subtitle: Automate your book deployment with GitHub Actions—no manual steps, zero
  cost.
image: /img/thumbnails/2026-03-05-deploy-jupyter-book-to-github-pages-free.svg
tags:
- Jupyter Book
- GitHub Pages
- GitHub Actions
- CI/CD
- documentation hosting
- Python deployment
- automated publishing
categories:
- academic-presence
is_series: true
article_type: tutorial
cluster: 🌐 Academic Presence
critic_score: 8.8
source_transcript: cleaned_transcripts_2026-02-27_12-20-13_Deploy_Jupyter_Book_to_GitHub_Pages_FREE_Step-by-S.md
generated: 2026-03-05_07-33-52
series_part: 2
---

## Deploy Jupyter Book to GitHub Pages Using GitHub Actions

You've built your Jupyter Book locally. It looks great on your machine. But right now, it's trapped there—invisible to the world. You need a live URL to share with collaborators, students, or your audience. You need it updated automatically every time you push, and you need it *free*. That's exactly what we're solving today.

**GitHub Pages** + **GitHub Actions** = automated, free hosting for your Jupyter Book. Every time you push changes, a workflow automatically rebuilds your book and publishes it live. No manual steps. No paid hosting. Just push → build → live.

This is Part 2 of the Jupyter Book Deployment Series. You'll need a working local Jupyter Book before following this guide.

## Prerequisites

You'll need:
- Git installed locally
- A GitHub account (free tier works)
- A **working local Jupyter Book** with a `requirements.txt` file
- VS Code or any code editor
- Python 3.8+ with `jupyter-book` installed

## Organize Your Book & Push to GitHub

### Step 1: Structure Your Files

Before pushing, organize your book into clean subdirectories:

```
my-jupyter-book/
├── chapters/
│   ├── intro.md
│   ├── chapter1.ipynb
│   └── chapter2.ipynb
├── _config.yml
├── _toc.yml
├── requirements.txt
└── .gitignore
```

### Step 2: Update `_toc.yml`

Ensure all chapters reference the correct paths:

```yaml
- file: chapters/intro.md
- file: chapters/chapter1.ipynb
- file: chapters/chapter2.ipynb
```

### Step 3: Build Locally to Verify

```bash
jupyter-book build .
```

Check `_build/html/` to confirm everything renders correctly.

### Step 4: Initialize Git & Create `.gitignore`

```bash
cd /path/to/my-jupyter-book
git init
```

Create `.gitignore`:

```
_build/
.DS_Store
__pycache__/
*.pyc
.ipynb_checkpoints/
```

### Step 5: Commit & Push to GitHub

```bash
git add .
git commit -m "initial commit: Jupyter Book setup"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
git push -u origin main
```

Replace `YOUR-USERNAME` and `YOUR-REPO-NAME` with your actual values. Make sure the repository is **Public**.

## Set Up GitHub Actions

### Step 1: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment," select **GitHub Actions**
4. Save

### Step 2: Create the Workflow File

Create `.github/workflows/deploy.yml` in your local repo:

```bash
mkdir -p .github/workflows
```

Add this content to `deploy.yml`:

```yaml
name: Deploy Jupyter Book

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install jupyter-book ghp-import
      
      - name: Build Jupyter Book
        run: jupyter-book build .
      
      - name: Deploy to GitHub Pages
        run: ghp-import -n -p -f _build/html
```

**What happens:**
- **Checkout**: Grabs your latest code
- **Setup Python**: Prepares Python 3.10
- **Install dependencies**: Installs packages from `requirements.txt`, plus `jupyter-book` and `ghp-import`
- **Build**: Generates HTML from your book
- **Deploy**: Pushes the built files to GitHub Pages

### Step 3: Push the Workflow

```bash
git add .github/
git commit -m "add GitHub Actions workflow"
git push
```

### Step 4: Watch It Deploy

1. Go to the **Actions** tab in your GitHub repo
2. Watch the "Deploy Jupyter Book" workflow run
3. Once you see a green checkmark ✓, your book is live
4. Go to **Settings** → **Pages** to find your live URL

## Add a New Chapter (No Manual Deployment)

**Scenario:** You want to add a new chapter and have it automatically published.

### Step 1: Create the New File

Add `chapters/chapter3.ipynb` with your content.

### Step 2: Update `_toc.yml`

```yaml
- file: chapters/intro.md
- file: chapters/chapter1.ipynb
- file: chapters/chapter2.ipynb
- file: chapters/chapter3.ipynb
```

### Step 3: Test Locally

```bash
jupyter-book build .
```

### Step 4: Push

```bash
git add chapters/chapter3.ipynb _toc.yml
git commit -m "add chapter 3: Advanced Topics"
git push
```

That's it. GitHub Actions automatically rebuilds and deploys within 1–2 minutes. No manual steps.

## Troubleshooting

**Workflow fails with "ModuleNotFoundError"**
Your `requirements.txt` is missing a dependency. Add it and push:

```
jupyter-book>=0.13.0
matplotlib
pandas
numpy
```

**"Permission Denied" on `ghp-import`**
Go to **Settings** → **Actions** → **General** and set "Workflow permissions" to **Read and write permissions**.

**Live site shows old content**
Hard refresh your browser (`Ctrl+Shift+R` on Windows/Linux, `Cmd+Shift+R` on Mac). GitHub Pages can take 1–2 minutes to propagate.

**404 error on live site**
Make sure your repository is **Public**. GitHub Pages requires this on the free tier.

## What's Next?

- **Customize appearance**: Edit `_config.yml` to change themes and styling
- **Add interactivity**: Enable Thebe or Binder for live code execution
- **Use a custom domain**: Point your own domain to GitHub Pages
- **Invite collaborators**: Others can push chapters; the workflow rebuilds automatically

What's your biggest challenge right now—organizing content, customizing the design, or getting collaborators set up? Reply and let me know.

---

*What's your current workflow for publishing and updating technical documentation or course materials?*
