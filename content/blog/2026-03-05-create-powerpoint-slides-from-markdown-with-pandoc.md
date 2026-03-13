---
title: Create PowerPoint Slides from Markdown with Pandoc
date: '2026-03-05'
draft: false
description: Pandoc lets you build professional PowerPoint presentations from Markdown
  files in seconds. Write once in plain text, version control it, and generate .pptx
  files instantly—no manual formatting or clicking required.
subtitle: Write presentations in plain text, convert to .pptx in seconds. No manual
  formatting.
image: /img/thumbnails/2026-03-05-create-powerpoint-slides-from-markdown-with-pandoc.svg
tags:
- Pandoc
- Markdown
- PowerPoint automation
- presentation tools
- command-line tools
- researchers
- developers
- technical writing
categories:
- academic-writing
is_series: false
article_type: tutorial
cluster: 🖊️ Academic Writing Stack
critic_score: 9.0
source_transcript: cleaned_transcripts_2026-02-27_12-24-25_Create_PowerPoint_Slides_from_Markdown_with_Pando.md
generated: 2026-03-05_07-40-06
---

# Create PowerPoint Presentations from Markdown with Pandoc

You've spent the last hour manually formatting slides in PowerPoint—adjusting fonts, copying text, fixing alignment—only to realize you need to make changes across 20 slides. There's a better way.

**Pandoc** lets you write your entire presentation in plain text, run a single command, and generate a professionally formatted PowerPoint file in seconds. No clicking. No dragging. No wasted time.

## Why This Matters

If you're a developer, researcher, or content creator, you already know the pain: PowerPoint's interface is slow, changes are tedious, and version control is a nightmare. **Markdown + Pandoc** flips the script. You write in plain text (which is version-control friendly), separate slides with `---`, and convert to `.pptx` instantly. Bold, italic, lists, images, tables, equations, links, emojis—all supported. Edit further in PowerPoint if you need to, or ship the file as-is.

## What You Need

- **Pandoc** (latest stable version from [pandoc.org](https://pandoc.org))
- **A text editor** (VS Code, Obsidian, StackEdit, or any Markdown editor)
- **Command line access** (Terminal on macOS/Linux; Command Prompt or PowerShell on Windows)
- **That's it.** No dependencies, no libraries.

## Installation

### macOS (Homebrew)

```bash
brew install pandoc
```

### Windows

Download the `.msi` installer from [pandoc.org](https://pandoc.org), run it, and check "Add Pandoc to PATH" during setup.

### Linux (Ubuntu/Debian)

```bash
sudo apt-get install pandoc
```

### Verify

```bash
pandoc --version
```

You should see a version number. If not, restart your terminal.

## Your First Presentation

### Create a Markdown File

Open your text editor and save this as `presentation.md`:

```markdown
# My First Presentation

This is the title slide.

---

## Slide 2: Key Points

- Point one
- Point two
- Point three

---

## Slide 3: More Content

**Bold text** and *italic text* work too.

[Links](https://example.com) are supported.
```

### Convert to PowerPoint

Open your terminal, navigate to the folder where you saved `presentation.md`, and run:

```bash
pandoc -i presentation.md -o presentation.pptx
```

That's it. A new file named `presentation.pptx` appears in your folder. Open it in PowerPoint, Google Slides, or any compatible viewer.

## Real Example: Tech Talk

Save this as `tech_talk.md`:

```markdown
# Machine Learning Basics

An introduction to ML concepts for beginners.

---

## What is Machine Learning?

- Subset of artificial intelligence
- Systems learn from data without explicit programming
- Powers recommendation engines, image recognition, and more

---

## Key Algorithms

| Algorithm | Use Case |
|-----------|----------|
| Linear Regression | Prediction |
| K-Means | Clustering |
| Neural Networks | Complex patterns |

[Learn more](https://example.com)

---

## Next Steps

1. Choose a problem
2. Gather data
3. Train your model
4. Evaluate and iterate
```

Convert it:

```bash
pandoc -i tech_talk.md -o tech_talk.pptx
```

**Result:** A 4-slide presentation with formatted lists, a table, a hyperlink, and numbered steps—all ready to present or edit further.

## Supported Markdown Features

- **Headings**: `# Title` (slide title), `## Subtitle` (section)
- **Emphasis**: `**bold**` and `*italic*`
- **Lists**: Unordered (`- item`) and ordered (`1. item`)
- **Links**: `[text](url)`
- **Images**: `![alt](path/to/image.png)`
- **Tables**: Standard Markdown syntax
- **LaTeX equations**: `$...$` for inline, `$$...$$` for display
- **Task lists**: `- [ ] unchecked`, `- [x] checked`
- **Emojis**: `🚀`, `✨`, etc.
- **Code blocks**: Fenced with triple backticks and a language tag

## Troubleshooting

### "Pandoc command not found"

**Windows:** Reinstall using the `.msi` and ensure PATH is set. Restart your terminal.

**macOS/Linux:** Verify with `which pandoc`. If empty, reinstall:

```bash
brew install pandoc
```

### File Not Found

Use the full path to your file:

```bash
pandoc -i /Users/yourname/Documents/presentation.md -o /Users/yourname/Documents/presentation.pptx
```

Or navigate to the folder first:

```bash
cd /path/to/folder
pandoc -i presentation.md -o presentation.pptx
```

### Output Doesn't Look Right

Check for unclosed code blocks or special characters. Escape literal `*`, `#`, or `_` with a backslash: `\*`. For detailed diagnostics, run:

```bash
pandoc -i presentation.md -o presentation.pptx -v
```

## Level Up Your Workflow

**Automate bulk conversions:** Create a shell script (macOS/Linux) or batch file (Windows) to convert multiple `.md` files at once.

**Version control:** Store your `.md` files in Git. Markdown diffs are human-readable, making collaboration and history tracking trivial.

**Custom styling:** Use Pandoc's `--reference-doc` flag to apply your own PowerPoint template:

```bash
pandoc -i presentation.md -o presentation.pptx --reference-doc=template.pptx
```

---

**What's your biggest presentation pain point—is it the formatting, the time sink, or keeping content in sync across revisions? Have you tried Pandoc before? Reply and let me know what workflow you'd like to automate next.**

---

*What's your current workflow for creating presentations—and would automating it with Markdown change how you work?*
