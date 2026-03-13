---
title: Write Research Papers in Markdown + Pandoc
date: '2026-03-04'
draft: false
description: Ditch LaTeX syntax errors and write research papers in clean Markdown
  instead. This workflow uses Pandoc + pandoc-crossref to convert your .md files into
  publication-ready PDFs with proper citations, cross-references, and IEEE/Springer
  formatting—no manual LaTeX configuration needed.
subtitle: Get LaTeX-quality PDFs without the syntax headaches. Clean Markdown workflow
  for researchers.
image: /img/thumbnails/2026-03-04-write-research-papers-in-markdown-pandoc.svg
tags:
- Pandoc
- Markdown
- Academic Writing
- LaTeX
- pandoc-crossref
- Research Papers
- Citation Management
- PDF Generation
categories:
- academic-writing
is_series: false
article_type: tutorial
cluster: 🖊️ Academic Writing Stack
critic_score: 9.0
source_transcript: cleaned_transcripts_2026-02-27_11-47-52_Write_Research_Papers_in_Markdown__Pandoc__LaTeX_Q.md
generated: 2026-03-04_20-16-16
---

You're staring at a LaTeX error message for the 47th time today. Your paper deadline is tomorrow, but you're debugging `\begin{figure}` placement instead of refining your argument. There's a better way: **write in clean Markdown, get publication-ready PDFs** with equations, cross-references, and IEEE/Springer formatting—all without touching LaTeX syntax until the final export.

## What This Workflow Replaces

Direct LaTeX editing becomes Markdown + Pandoc conversion. You write in readable `.md` files with simple syntax for headings, citations, and figures. **Pandoc** (a universal document converter) transforms your Markdown into professional PDFs or LaTeX source files, using **pandoc-crossref** for numbered references and **citeproc** for bibliographies. Output matches journal templates—single-column, two-column IEEE, ACM formats—without manual `\documentclass` configuration.

### What You Need

**Required software:**
- Pandoc 3.x (tested on 3.1.11)
- pandoc-crossref filter (version MUST match Pandoc major version)
- LaTeX distribution (MiKTeX/MacTeX/TeX Live) for PDF rendering
- Text editor (VS Code, Typora, plain text)

**Assumed knowledge:**
- Basic Markdown syntax (headings, lists, links)
- Familiarity with academic citation formats

## Installation

### Install Pandoc

Go to [pandoc.org/installing.html](https://pandoc.org/installing.html) and download the installer for your OS. Choose one or two versions behind the bleeding edge for stability—3.1.11 instead of 3.2.0.

Verify installation:

```bash
pandoc -v
```

Expected output: `pandoc 3.1.11` with Lua 5.4 details.

### Download pandoc-crossref

Visit the [pandoc-crossref releases page](https://github.com/lierdakil/pandoc-crossref/releases). Download the version matching your Pandoc installation—if you have Pandoc 3.1.x, get crossref 0.3.17.0.

**Windows:** Place the `.exe` in `C:\Users\[YourName]\AppData\Local\Pandoc` or add to PATH.

**macOS/Linux:** Move binary to `/usr/local/bin/`.

Test it:

```bash
pandoc-crossref -v
```

Expected output: Version matching Pandoc (e.g., `v0.3.17.0`).

### Install LaTeX Distribution

**Windows:** [MiKTeX](https://miktex.org/download)

**macOS:** [MacTeX](https://www.tug.org/mactex/)

**Linux:**

```bash
sudo apt-get install texlive-full
```

> ⚠️ **Note:** Full TeX Live is ~5GB. Use `texlive-base` for minimal setup.

## Core Workflow

### Set Up Project Structure

```
my-paper/
├── paper.md          # Your manuscript
├── references.bib    # BibTeX bibliography
├── ieee.csl          # Citation style
└── figures/
    └── diagram.png
```

### Write YAML Metadata Block

At the top of `paper.md`:

```yaml
---
title: "Your Paper Title Here"
author: 
  - Jane Doe
  - John Smith
institute: "University of Example"
abstract: |
  This paper demonstrates a Markdown-based workflow for academic writing.
  Multiple lines supported with the pipe character.
keywords: [Pandoc, Markdown, Academic Writing]
bibliography: references.bib
---
```

### Add Body Content

**Headings:** `# Introduction`, `## Methods`, `### Subsection`

**Citations:** `[@smith2023]` for inline, `@smith2023` for narrative

**Equations:** `$E = mc^2$` inline, `$$\int_0^\infty e^{-x} dx$$` display

**Figures:** `![Caption](figures/diagram.png){#fig:diagram}`

**Cross-references:** `See [@fig:diagram]` or `Equation [@eq:loss]`

### Create Bibliography File

Export from Zotero/Mendeley or write manually in `references.bib`:

```bibtex
@article{smith2023,
  author = {Smith, J.},
  title = {Example Research},
  journal = {Journal of Examples},
  year = {2023}
}
```

### Download Citation Style

Go to [Zotero Style Repository](https://www.zotero.org/styles), search for your target journal (IEEE, Nature, Springer), download the `.csl` file to your project folder.

### Convert to PDF

Basic command:

```bash
pandoc paper.md --filter pandoc-crossref --citeproc --output paper.pdf
```

**With formatting options:**

```bash
pandoc paper.md \
  --filter pandoc-crossref \
  --citeproc \
  --csl=ieee.csl \
  --number-sections \
  --toc \
  --variable geometry:margin=1in \
  --variable fontsize=12pt \
  --variable colorlinks=true \
  --output paper.pdf
```

**Options explained:**
- `--number-sections`: Auto-numbers headings
- `--toc`: Generates table of contents
- `--variable geometry:margin=1in`: Sets margins
- `--variable colorlinks=true`: Clickable colored links

### Generate Two-Column IEEE Format

```bash
pandoc paper.md \
  --filter pandoc-crossref \
  --citeproc \
  --csl=ieee.csl \
  --variable documentclass=IEEEtran \
  --variable classoption=conference \
  --output paper.pdf
```

Change `classoption` to `journal` for different IEEE layouts.

## Practical Example

**Scenario:** Machine learning conference paper with equations, figures, IEEE citations.

Create `ml-paper.md`:

```markdown
---
title: "Neural Network Optimization via Gradient Descent"
author: "A. Researcher"
bibliography: refs.bib
---

# Introduction

Recent work by @goodfellow2016 shows that loss functions...

# Methods

The loss is computed as:

$$L(\theta) = \frac{1}{n}\sum_{i=1}^n (y_i - \hat{y}_i)^2$$ {#eq:mse}

See [@eq:mse] for mean squared error formulation.

![Training accuracy over epochs](figures/accuracy.png){#fig:acc width=80%}

Results in [@fig:acc] demonstrate convergence.
```

Convert:

```bash
pandoc ml-paper.md \
  --filter pandoc-crossref \
  --citeproc \
  --csl=ieee.csl \
  --variable documentclass=IEEEtran \
  --variable classoption=conference \
  --number-sections \
  --output ml-paper.pdf
```

**Output:** Two-column IEEE conference paper with numbered equations (Equation 1), numbered figures (Figure 1), inline citations [1], bibliography in IEEE format.

## Common Issues & Fixes

**"pandoc-crossref not found" error**

Filter isn't in PATH. Verify with `pandoc-crossref -v` and add installation directory to system PATH.

---

**Version mismatch between Pandoc and pandoc-crossref**

Major versions don't align. Download matching crossref version from GitHub releases—check compatibility matrix in repository README.

---

**Citations not appearing**

Missing `--citeproc` flag or incorrect `bibliography` field. Ensure YAML includes `bibliography: references.bib` and command includes `--citeproc`.

---

**Figures not cross-referencing**

Missing `{#fig:label}` syntax. Use `![Caption](path.png){#fig:mylabel}` and reference with `[@fig:mylabel]`.

---

**LaTeX errors during PDF generation**

Missing packages or complex table syntax. Install via MiKTeX Package Manager (Windows) or `tlmgr install [package]` (macOS/Linux). Test with simpler Markdown syntax first.

## Next Steps

**Generate LaTeX instead of PDF:**

```bash
pandoc paper.md \
  --filter pandoc-crossref \
  --citeproc \
  --output paper.tex
```

Upload to Overleaf for collaborative editing with LaTeX-focused co-authors.

**Switch citation styles:** Replace `ieee.csl` with `nature.csl` or `springer-lncs.csl` from Zotero. Entire bibliography reformats automatically.

**Version control:** Commit `.md` and `.bib` files to Git. Markdown's plain-text format makes diffs readable, unlike binary `.docx` files.

---

This workflow saved me countless hours during PhD work on diabetic retinopathy papers. I could focus on writing and let Pandoc handle formatting—no more fighting with figure placement at 2 AM before deadlines.

**What's your biggest pain point with academic writing tools right now?** Reply and let me know if you'd like a follow-up on custom LaTeX templates or automated bibliography management.

---

*What's currently slowing down your paper writing process—LaTeX debugging, citation management, or formatting across templates?*
