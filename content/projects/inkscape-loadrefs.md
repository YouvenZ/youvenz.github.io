---
title: "LoadRefs Ink — Bibliography Import for Inkscape"
date: 2026-01-01
description: "Import bibliography files (.bib, .ris, .json, .enw) and place formatted citations as editable SVG text inside Inkscape."
status: "active"
tags: ["inkscape", "extension", "bibliography", "latex", "academic", "python", "open-source"]
github: "https://github.com/YouvenZ/Loadrefs_Ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-loadrefs.svg"
---

## Overview

**LoadRefs Ink** solves the citation formatting problem in Inkscape posters and presentations. Import your `.bib`, `.ris`, or `.json` bibliography file, choose a citation style (APA, IEEE, Vancouver, custom), and insert formatted references as native SVG text elements — no copy-paste, no manual formatting.

## Supported input formats

| Format | Extension |
|---|---|
| BibTeX | `.bib` |
| RIS | `.ris` |
| CSL-JSON | `.json` |
| Endnote XML | `.enw` |

## Citation styles

- APA 7th edition
- IEEE
- Vancouver (numerical, for biomedical)
- Nature
- Custom CSL template support

## Workflow

1. Run `Extensions → LoadRefs Ink → Insert References`
2. Browse to your `.bib` file
3. Select entries from the parsed list
4. Choose citation style
5. Click `Insert` — references are placed as a text group at the bottom of your canvas

## Installation

```bash
git clone https://github.com/YouvenZ/Loadrefs_Ink
pip install pybtex citeproc-py
```
