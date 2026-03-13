---
title: 'Hugo + GitHub Pages: Automate Deployment with GitHub Actions'
date: '2026-03-05'
draft: false
description: Learn how to deploy a Hugo website to GitHub Pages using GitHub Actions
  for automatic, hands-off publishing. This guide walks students and researchers through
  setting up a complete CI/CD workflow that rebuilds and publishes your site with
  every git push—no manual steps required.
subtitle: Deploy your Hugo site automatically with every git push using GitHub Actions.
  No manual rebuilds needed.
image: /img/thumbnails/2026-03-05-hugo-github-pages-automate-deployment-with-github-actions.svg
tags:
- Hugo
- GitHub Pages
- GitHub Actions
- Static Site Generation
- CI/CD
- Web Deployment
- Researchers
- Students
categories:
- academic-presence
is_series: false
article_type: tutorial
cluster: 🌐 Academic Presence
critic_score: 8.8
source_transcript: cleaned_transcripts_2026-02-27_12-03-04_Hugo__GitHub_Pages_Easy_Website_Deployment_with_Gi.md
generated: 2026-03-05_07-09-31
---

# Deploy a Hugo Website to GitHub Pages Using GitHub Actions — Student & Researcher Guide

You've built a beautiful Hugo website locally. It works perfectly when you run `hugo server`. But now what? You're staring at a folder on your laptop, unsure how to share it with the world—or worse, how to update it without manually rebuilding and uploading files every single time. **GitHub Pages + GitHub Actions** solves this: every time you push changes to your repository, your site rebuilds and deploys automatically. No manual steps. No confusion.

## What You'll Get

This guide walks you through a **completely automated deployment workflow**. Instead of manually rebuilding your site and uploading files, you push your changes to GitHub, and a workflow automatically:

- Installs Hugo
- Rebuilds your entire site
- Publishes it to GitHub Pages

Result: Your live website updates instantly with every `git push`.

## Prerequisites

You'll need:

- Hugo installed locally ([install here](https://gohugo.io/installation/))
- Git and basic command-line comfort
- A GitHub account (free tier works fine)
- A Hugo website already created locally
- Familiarity with `git add`, `git commit`, and your Hugo site structure

**Starting from scratch?** Create a Hugo site now:

```bash
hugo new site my-website
cd my-website
git init
git submodule add https://github.com/gurukulkarni/hugo-profile.git themes/hugo-profile
```

## Step 1: Prepare Your Local Repository

Initialize Git in your Hugo folder if you haven't already:

```bash
cd /path/to/your/hugo-website
git init
```

Add your theme as a submodule (this keeps theme updates separate from your content):

```bash
git submodule add https://github.com/your-theme-repo/theme-name.git themes/theme-name
git submodule init
git submodule update
```

## Step 2: Configure Hugo for GitHub Pages

Open `config.yaml` (or `config.toml`) and verify these two lines:

```yaml
baseURL: "https://your-github-username.github.io/repository-name/"
publishDir: "public"
```

> **Note:** For user/organization sites (not project sites), use `https://your-github-username.github.io/` instead.

## Step 3: Create the GitHub Actions Workflow

Create the `.github/workflows` directory:

```bash
mkdir -p .github/workflows
```

Create a file named `deploy.yml`:

```bash
touch .github/workflows/deploy.yml
```

Paste this into `deploy.yml`:

```yaml
name: Deploy Hugo site to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

This workflow runs automatically whenever you push to `main`, rebuilds your site, and deploys it.

## Step 4: Add a .gitignore File

Create `.gitignore` in your project root:

```bash
touch .gitignore
```

Add these lines:

```
# Hugo
/public/
/resources/

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/

# Dependencies
node_modules/
```

## Step 5: Commit and Push to GitHub

Stage everything locally:

```bash
git add .
git commit -m "Initial Hugo setup with GitHub Actions deployment"
```

Create a new repository on [github.com/new](https://github.com/new):

- Name it `your-username.github.io` (user site) or `my-project-name` (project site)
- Choose "Public"
- Do **not** initialize with README, .gitignore, or license
- Click "Create repository"

Link your local repo to GitHub:

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

## Step 6: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages** (left sidebar)
3. Under "Build and deployment," select **GitHub Actions** as the source
4. Save

## Step 7: Monitor and Verify

Go to your repo's **Actions** tab. You should see "Deploy Hugo site to GitHub Pages" running. Once it shows a green checkmark (usually 1–2 minutes), your site is live at:

- **User site:** `https://your-username.github.io`
- **Project site:** `https://your-username.github.io/repo-name`

## Real-World Example: Adding a Blog Post

You want to add a blog post. Here's the complete workflow:

**Create the post locally:**

```bash
hugo new posts/my-first-post.md
```

Edit `content/posts/my-first-post.md`:

```markdown
---
title: "My First Post"
date: 2024-01-15
draft: false
---

This is my first blog post!
```

**Preview locally:**

```bash
hugo server -D
```

Open `http://localhost:1313` and verify the post appears.

**Deploy:**

```bash
git add content/posts/my-first-post.md
git commit -m "Add first blog post"
git push origin main
```

Your post is live within 2 minutes.

## Troubleshooting

### Workflow fails with "Hugo not found"

In `deploy.yml`, ensure the Hugo version is valid:

```yaml
- name: Setup Hugo
  uses: peaceiris/actions-hugo@v2
  with:
    hugo-version: 'latest'
```

Use `'latest'` or a specific version like `'0.120.0'`.

### Site deploys but content is missing

Your `baseURL` in `config.yaml` likely doesn't match your GitHub Pages URL. Fix it:

```yaml
baseURL: "https://your-username.github.io/"  # user sites
baseURL: "https://your-username.github.io/repo-name/"  # project sites
```

Then commit and push:

```bash
git add config.yaml
git commit -m "Fix baseURL"
git push origin main
```

### Submodule not found during deployment

Ensure your checkout step includes `submodules: recursive` (it's in the template above). If you added the theme after creating the workflow, push a new commit to re-run it.

### GitHub Pages source not set to GitHub Actions

Go to **Settings** → **Pages** and select **GitHub Actions** under "Build and deployment."

## What's Next

1. **Customize your config:** Edit `config.yaml` with your title, author, and social links
2. **Add more content:** Use `hugo new` to create pages and posts
3. **Preview before pushing:** Always run `hugo server` locally first
4. **Monitor deployments:** Check the **Actions** tab for build errors
5. **Custom domain (optional):** Add your domain in **Settings** → **Pages**

---

**Your deployment workflow is now fully automated.** Every push to `main` triggers a rebuild and redeploy. No manual uploads. No forgotten deployments.

**What's the first piece of content you're planning to add to your live site?** Reply and let me know—I'd love to see what you build.

---

*What's your current Hugo deployment workflow—manual uploads, or are you already using CI/CD automation?*
