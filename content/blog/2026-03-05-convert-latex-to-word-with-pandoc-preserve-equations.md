---
title: 'Convert LaTeX to Word with Pandoc: Preserve Equations'
date: '2026-03-05'
draft: false
description: Pandoc is a universal document converter that transforms LaTeX files
  into Word format while preserving equations, citations, tables, and cross-references.
  Learn the complete setup, core workflow commands, and practical examples to convert
  research papers in under 5 minutes—no broken formatting, no manual reconstruction.
subtitle: Master Pandoc to convert LaTeX documents to .docx without breaking equations,
  citations, or tables.
image: /img/thumbnails/2026-03-05-convert-latex-to-word-with-pandoc-preserve-equations.svg
tags:
- Pandoc
- LaTeX to Word conversion
- Document conversion tools
- Research paper formatting
- BibTeX citations
- Equation preservation
- AI/ML researchers
categories:
- academic-writing
is_series: false
article_type: tutorial
cluster: 🖊️ Academic Writing Stack
critic_score: 8.8
source_transcript: cleaned_transcripts_2026-02-27_11-51-03_Convert_LaTeX_to_Word_WITHOUT_Breaking_Equations.md
generated: 2026-03-05_06-53-07
---

## Convert LaTeX to Word WITHOUT Breaking Equations Using Pandoc

You've spent weeks perfecting your LaTeX document—equations are crisp, references are linked, tables are formatted, and the bibliography flows perfectly. Then your advisor asks: "Can you send this as a Word file?" Your stomach drops. You've heard the horror stories: equations become unreadable images, references break, tables collapse, and you're left manually reconstructing everything in Word.

There's a better way, and it takes under 5 minutes to set up.

## What This Is

**Pandoc** is a universal document converter that transforms LaTeX files into Word (.docx) format while preserving equations, citations, tables, and cross-references. Unlike copy-paste or online converters that destroy formatting, Pandoc understands LaTeX syntax natively and translates it into Word-compatible markup.

The result? Your collaborator opens the file in Word, adds comments, suggests edits, and you merge feedback back into your LaTeX source. No broken equations. No missing citations. No reformatting required.

## Prerequisites

You'll need:
- **Pandoc** (v2.18+) — the converter itself
- A LaTeX document (`.tex` file)
- A BibTeX file (`.bib`) — optional but recommended
- A terminal/command line
- Word, Google Docs, or any `.docx` reader

**Heads up:** Complex TikZ graphics, advanced algorithm packages, and highly customized LaTeX styling won't translate perfectly. We'll handle those edge cases below.

## Installation & Setup

### Step 1: Download Pandoc

Visit [pandoc.org/installing.html](https://pandoc.org/installing.html) and grab the installer for your OS:

- **Windows:** .msi installer
- **macOS:** .pkg installer or Homebrew
- **Linux:** Use your package manager (apt, yum, etc.)

### Step 2: Verify Installation

Open your terminal and run:

```bash
pandoc --version
```

You should see a version number and supported formats. If you get "command not found," skip to the Common Issues section.

### Step 3: Organize Your Files

Create a working folder:

```
your-project-folder/
├── main.tex
├── references.bib
└── figures/
    ├── figure1.png
    └── figure2.pdf
```

### Step 4: Navigate to Your Project Folder

```bash
cd path/to/your-project-folder
```

## Core Workflow

### Basic Conversion

Test your setup with the simplest command:

```bash
pandoc main.tex -o main.docx
```

Check the output—equations should render as Word equations, tables should be intact, and text should be readable.

### Add Bibliography Support

If your document uses `\cite{}` commands:

```bash
pandoc main.tex --bibliography=references.bib --citeproc -o main.docx
```

The `--citeproc` flag processes citations and generates a proper bibliography at the end.

### Enable Table of Contents

For longer documents:

```bash
pandoc main.tex --bibliography=references.bib --citeproc --toc --toc-depth=2 -o main.docx
```

The `--toc` flag adds an auto-generated table of contents; adjust `--toc-depth=2` for deeper nesting.

### Add Code Highlighting

If your document includes code blocks or algorithms:

```bash
pandoc main.tex --bibliography=references.bib --citeproc --toc --toc-depth=2 --highlight-style=tango -o main.docx
```

Try other styles: `kate`, `monochrome`, `espresso`, or `zenburn`.

### Save as a Reusable Script

**Windows** — create `convert.bat`:

```batch
@echo off
pandoc main.tex --bibliography=references.bib --citeproc --toc --toc-depth=2 --highlight-style=tango -o main.docx
echo Conversion complete! Check main.docx
pause
```

**macOS/Linux** — create `convert.sh`:

```bash
#!/bin/bash
pandoc main.tex --bibliography=references.bib --citeproc --toc --toc-depth=2 --highlight-style=tango -o main.docx
echo "Conversion complete! Check main.docx"
```

Run with:

```bash
bash convert.sh
```

## Practical Example: Converting a Research Paper

You have a 15-page paper (`neural-networks.tex`) with:
- Title, author, abstract
- 4 sections with subsections
- 12 equations (matrices, proofs)
- 3 tables (results, hyperparameters, comparison)
- 2 figures (architecture, loss curves)
- 25 citations from `ml-references.bib`
- 2 code blocks (Python snippets)

Your command:

```bash
pandoc neural-networks.tex --bibliography=ml-references.bib --citeproc --toc --toc-depth=2 --highlight-style=kate -o neural-networks.docx
```

**What you get:**

- Front matter (title, author, date)
- Clickable table of contents
- All sections with inline equations as Word Math objects
- Citations linked to bibliography
- Code blocks with syntax highlighting
- Embedded figures with captions
- Properly formatted tables
- Complete bibliography

> **Note:** Matrices may not render with perfect LaTeX formatting in Word, but they remain readable. Complex TikZ diagrams won't convert—compile those to PNG separately and embed them.

## Common Issues & Fixes

### "pandoc: command not found"

**Windows:** Add Pandoc's folder (usually `C:\Users\YourName\AppData\Local\Pandoc`) to your system PATH, then restart your terminal.

**macOS/Linux:** If installed via Homebrew, it's automatic. Otherwise, find it with:

```bash
which pandoc
```

### Citations Not Appearing

- Ensure your command includes `--citeproc`
- Verify the `.bib` file is in the same folder
- Check that your `.tex` file uses `\cite{}` syntax

### Equations Render as Broken Images

Use standard equation environments: `equation`, `align`, `gather`. Avoid nested custom commands. For TikZ diagrams, compile to PDF separately and embed as images.

### Images Not Showing

- Use relative paths: `\includegraphics{figures/figure1.png}`
- Ensure all image files match the folder structure
- Stick to PNG, PDF, or JPG (not EPS)

### Table Formatting is Off

- Use basic `tabular` environments
- Avoid `multirow` and `multicol` for critical tables
- Minor manual tweaks in Word are usually all you need

## Next Steps

1. Run your first conversion using the basic command
2. Check the output in Word—spot any formatting issues
3. Add flags one at a time (`--toc`, `--bibliography`, `--highlight-style`)
4. Save your script for re-conversion when your LaTeX changes
5. Share with collaborators—they can now edit in Word and send feedback

You keep your source in LaTeX (version control, perfect equations, professional output) while collaborators work in Word (familiar, easy to comment, no learning curve). Best of both worlds.

---

**What's your biggest pain point with sharing academic documents—is it getting non-LaTeX users to understand your work, or managing feedback from multiple collaborators?** Reply and let me know.

---

*What's your current workflow for sharing LaTeX documents with collaborators who use Word?*
