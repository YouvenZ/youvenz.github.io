---
title: "Auto Publication List"
date: 2025-06-01
description: "A GitHub Actions pipeline that automatically fetches Google Scholar metrics and exports a BibTeX bibliography file for use in LaTeX documents."
status: "active"
tags: ["python", "github-actions", "google-scholar", "bibtex", "latex", "automation"]
github: "https://github.com/YouvenZ/Auto-Publication-List"
demo: ""
paper: ""
thumbnail: ""
---

## Overview

**Auto Publication List** is a lightweight automation pipeline that keeps your publication list up to date without manual intervention. It fetches your Google Scholar profile export and generates both a BibTeX bibliography file and a LaTeX metrics snippet.

## How It Works

1. **Fetch** — Downloads your Google Scholar export (BibTeX-like text) using your Scholar user ID
2. **Parse** — Cleans and normalises the entries into valid BibTeX format
3. **Metrics** — Extracts citation counts, h-index, and i10-index and writes them to `metrics.tex`
4. **Export** — Outputs `publications.bib` ready to include in any LaTeX document

## Usage

```python
from update_publications import fetch_scholar_publications

# Fetch and export
fetch_scholar_publications(user_id="YOUR_SCHOLAR_ID", output_dir="./output")
```

## GitHub Actions Integration

Add the workflow to your repository to run on a schedule:

```yaml
name: Update Publications
on:
  schedule:
    - cron: '0 6 * * 1'   # Every Monday at 06:00 UTC
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python update_publications.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: auto-update publications"
```

## Output Files

| File | Description |
|------|-------------|
| `publications.bib` | Full BibTeX bibliography |
| `metrics.tex` | LaTeX snippet with Scholar metrics (citations, h-index, i10-index) |
