---
title: "Inkscape Extensions Suite"
date: 2026-01-01
description: "A collection of Inkscape extensions that bring diagramming tools, AI generation, and academic utilities directly into your SVG workflow."
status: "active"
tags: ["inkscape", "extensions", "python", "svg", "ai", "productivity", "open-source"]
github: "https://github.com/YouvenZ"
demo: ""
paper: ""
thumbnail: ""
---

## Overview

A suite of **8 open-source Inkscape extensions** designed for researchers and technical creators who want to stay inside their SVG workflow without switching to external tools.

Each extension is independently installable and integrates natively into Inkscape's Extensions menu.

## Extensions

### Diagram Generation
- **[SVG Maker](https://github.com/YouvenZ/svg_maker_ink)** — Generate SVG elements from natural language prompts using an LLM, directly inside Inkscape.
- **[Mermaid Ink](https://github.com/YouvenZ/mermaid_ink)** — Render Mermaid.js diagrams (flowcharts, sequence diagrams, Gantt charts) as native SVG inside Inkscape.
- **[D2 Ink](https://github.com/YouvenZ/D2_ink)** — Write and render D2 architecture diagrams and entity-relationship diagrams as editable SVG.

### AI-Assisted Content
- **[TextGen Ink](https://github.com/YouvenZ/textgen_ink)** — Generate, rewrite, or refine text elements using an LLM — captions, labels, descriptions — without leaving Inkscape.
- **[ImageGen Ink](https://github.com/YouvenZ/Imagegen_ink)** — Generate AI images (Stable Diffusion, DALL·E, Flux) from text prompts as embedded SVG elements.

### Scientific & Data Visualisation
- **[Plt Ink](https://github.com/YouvenZ/plt_ink)** — Write Python Matplotlib code and render publication-quality figures as native SVG directly inside Inkscape.
- **[Poster Utils Ink](https://github.com/YouvenZ/poster_utils_ink)** — Auto-generate formatted title blocks, author lists, and institution panels for academic conference posters.

### Academic Reference
- **[LoadRefs Ink](https://github.com/YouvenZ/Loadrefs_Ink)** — Import bibliography files (.bib, .ris, .json, .enw) and place formatted citations as editable SVG text inside Inkscape.

## Installation

Each extension follows the standard Inkscape extension installation process:

```bash
# Clone the extension repository
git clone https://github.com/YouvenZ/<extension-name>

# Copy to your Inkscape extensions folder
# Linux:   ~/.config/inkscape/extensions/
# macOS:   ~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/
# Windows: %APPDATA%\inkscape\extensions\
```

Restart Inkscape and find each extension under the **Extensions** menu.

## Requirements

- Inkscape 1.x
- Python 3.8+
- Extension-specific dependencies (API keys for AI extensions, D2/Mermaid CLI for diagram extensions)
