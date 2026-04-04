---
title: "Poster Utils Ink — Academic Poster Generator for Inkscape"
date: 2026-01-01
description: "Auto-generate formatted title blocks, author lists, and institution panels for academic conference posters."
status: "active"
tags: ["inkscape", "extension", "poster", "academic", "python", "open-source"]
github: "https://github.com/YouvenZ/poster_utils_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-poster-utils.svg"
---

## Overview

**Poster Utils Ink** automates the most tedious parts of academic poster creation. Fill in your title, authors, affiliations, and abstract — and the extension generates a properly formatted header block, author list with superscript affiliation numbers, and institution row, all placed on the Inkscape canvas at the correct position and typography.

## Features

- Title block at A0/A1/custom poster dimensions
- Author list with numbering, affiliations, and equal-contribution markers
- Institution row with logo placeholder slots
- Abstract section with proper typographic treatment
- One-click update: change any field and re-render in place

## Typical workflow

For a MICCAI or NeurIPS poster:
1. Set page to A0 landscape (or your conference format)
2. Run `Extensions → Poster Utils → New Poster Header`
3. Fill in the form (title, authors, affiliations, conference logo)
4. Click `Insert` — the full header is rendered on the canvas
5. Edit individual elements as needed

## Installation

```bash
git clone https://github.com/YouvenZ/poster_utils_ink
```
