---
title: Create Course Materials in Markdown + Pandoc
date: '2026-03-05'
draft: false
description: Master the Markdown + Pandoc workflow to create professional course materials
  once and convert them instantly to PDFs, HTML, and more. Eliminate formatting drift,
  maintain version control, and spend less time on presentation and more on content—perfect
  for teachers and professors managing exercises, quizzes, and lab work at scale.
subtitle: Write once, generate PDFs, HTML & more instantly. A complete workflow for
  teachers.
image: /img/thumbnails/2026-03-05-create-course-materials-in-markdown-pandoc.svg
tags:
- Pandoc
- Markdown
- Course Materials
- LaTeX
- Document Conversion
- Teachers
- Educational Content
- Version Control
categories:
- academic-writing
is_series: false
article_type: tutorial
cluster: 🖊️ Academic Writing Stack
critic_score: 8.0
source_transcript: cleaned_transcripts_2026-02-27_11-57-03_Create_Course_Materials_in_Markdown__Complete_Work.md
generated: 2026-03-05_07-01-20
---

# Create Professional Course Materials in Markdown Using Pandoc — A Complete Workflow for Teachers & Professors

You're spending hours formatting exercise sets, lab work, and quizzes in Word or Google Docs—adjusting margins, fixing font inconsistencies, regenerating the same content in three different formats. What if you could write once in Markdown and generate polished PDFs, HTML, and more in seconds?

**Markdown + Pandoc** eliminates this friction entirely. You write your exercises, quizzes, and lab work once in plain text, store it in version control, and convert it instantly to publication-ready PDFs and interactive HTML. No more juggling file formats or losing formatting when sharing with colleagues.

## Why This Matters

The traditional approach—Word documents, Google Docs, repeated manual formatting—breaks down at scale. You end up maintaining multiple versions, fighting with formatting drift, and spending more time on presentation than content.

Pandoc solves this by treating your course materials as **source code**. You write in Markdown (a format that's human-readable and version-control-friendly), add a YAML metadata block for styling, run a single command, and get beautifully formatted output. It's reproducible, collaborative, and fast.

## What You'll Need

- **Pandoc** (version 2.0+) — the document converter
- **LaTeX distribution** (TeX Live, MacTeX, or MiKTeX) — for PDF generation
- **Text editor** (VS Code, Sublime Text, or any plain-text editor)
- **Basic Markdown knowledge** (headers, lists, code blocks)
- **Command-line comfort** (ability to run terminal commands)
- **Optional: Git** — for version control

## Installation

### Pandoc

Download from [pandoc.org](https://pandoc.org/installing.html) or use your package manager:

```bash
# macOS
brew install pandoc
```

```bash
# Ubuntu/Debian
sudo apt-get install pandoc
```

```bash
# Windows (Chocolatey)
choco install pandoc
```

Verify:

```bash
pandoc --version
```

### LaTeX

Pandoc needs LaTeX to generate PDFs:

```bash
# macOS
brew install basictex
```

```bash
# Ubuntu/Debian
sudo apt-get install texlive-xetex texlive-fonts-recommended
```

Windows users: download **MiKTeX** from [miktex.org](https://miktex.org/).

Verify:

```bash
xelatex --version
```

### Project Structure

Set up a simple folder hierarchy:

```bash
mkdir course-materials
cd course-materials
mkdir markdown output
```

## The Core Workflow

### 1. Create a Markdown File with YAML Metadata

Every course material starts with a **YAML metadata block**—this controls formatting. Create `exercise-set-1.md`:

```markdown
---
title: "Exercise Set 1: Functions and Variables"
author: "Dr. Jane Smith"
date: "Spring 2024"
documentclass: article
geometry: margin=1in
fontsize: 11pt
numbersections: true
header-includes:
  - \usepackage{amsmath}
  - \usepackage{amssymb}
---
```

The metadata block sits between `---` delimiters. Key fields:
- `documentclass` — LaTeX document type (article, report, book)
- `geometry` — controls margins and page layout
- `header-includes` — loads LaTeX packages (math symbols, fonts, etc.)

### 2. Write Content in Markdown

Below the metadata, use standard Markdown syntax:

```markdown
# Objectives

- Understand function syntax
- Practice variable assignment
- Apply concepts to real problems

## Background

Functions are reusable blocks of code that perform specific tasks.

## Exercise 1: Basic Function Definition

Write a function that takes two numbers and returns their sum.

**Hint:** Use the `+` operator.
```

### 3. Add Collapsible Solutions for HTML

Wrap solutions in `<details>` tags so students reveal answers on demand:

```markdown
## Exercise 2: Function with Conditions

Write a function that returns "even" or "odd" for any integer.

<details>
<summary>Click to reveal solution</summary>

```python
def check_even_odd(n):
    return "even" if n % 2 == 0 else "odd"
```

</details>
```

This HTML element is ignored in PDF output but works beautifully in browsers.

### 4. Include Tables and Code

Add formatted tables and syntax-highlighted code directly:

```markdown
| Concept | Definition |
|---------|-----------|
| Variable | A named container for data |
| Function | A reusable block of code |

Example:

```python
def greet(name):
    return f"Hello, {name}!"
```
```

### 5. Convert to PDF

```bash
pandoc exercise-set-1.md -o output/exercise-set-1.pdf \
  --pdf-engine=xelatex \
  --table-of-contents \
  --toc-depth=2
```

**Flags explained:**
- `--pdf-engine=xelatex` — uses XeLaTeX for better font and special character support
- `--table-of-contents` — auto-generates TOC from headers
- `--toc-depth=2` — includes headers up to level 2

### 6. Convert to Interactive HTML

```bash
pandoc exercise-set-1.md -o output/exercise-set-1.html \
  --standalone \
  --mathjax \
  --css=style.css
```

**Flags explained:**
- `--standalone` — creates a complete, self-contained HTML document
- `--mathjax` — enables browser-based math rendering
- `--css=style.css` — links optional custom styling

## Practical Example: A Complete Quiz

Create `quiz-module-1.md`:

```markdown
---
title: "Quiz 1: Python Fundamentals"
author: "Course Instructor"
date: "February 2024"
documentclass: article
geometry: margin=0.75in
fontsize: 10pt
numbersections: false
---

# Instructions

Answer all questions. Select the best response.

---

## Question 1

What is the output of `print(2 + 3 * 4)`?

A) 20  
B) 14  
C) 18  
D) 11  

**Correct Answer:** B

**Explanation:** Following order of operations (PEMDAS), multiplication happens first. 3 × 4 = 12, then 2 + 12 = 14.

---

## Question 2

Which of the following is NOT a valid Python variable name?

A) `my_var`  
B) `_private`  
C) `2nd_place`  
D) `MyClass`  

**Correct Answer:** C

**Explanation:** Variable names cannot start with a number in Python.
```

Generate both formats:

```bash
pandoc quiz-module-1.md -o quiz-module-1.pdf --pdf-engine=xelatex
pandoc quiz-module-1.md -o quiz-module-1.html --standalone --mathjax
```

You now have two formats of the same quiz from a single source file.

## Troubleshooting

### Special Characters Break PDF Compilation

**Problem:** LaTeX chokes on `&`, `%`, `#`, or `_` in regular text.

**Fix:** Escape them with a backslash:

```markdown
This is 50\% off.
Use the \& symbol for "and".
```

Or wrap in inline code: `` `&` ``.

### Math Not Rendering in HTML

**Problem:** LaTeX equations don't display in HTML output.

**Fix:** Use the `--mathjax` flag and wrap math in dollar signs:

```markdown
Inline: $E = mc^2$

Display:
$$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$
```

### PDF Engine Not Found

**Problem:** Error message says "xelatex not found."

**Fix:** Verify LaTeX is installed:

```bash
xelatex --version
```

If this fails, reinstall your LaTeX distribution.

### Collapsible Solutions Don't Work in PDF

**Problem:** `<details>` tags are ignored when converting to PDF.

**Fix:** This is expected. Use `<details>` only for HTML, or add a separate "Solutions" section for PDF readers.

## Next Steps

1. **Create a reusable template** — save your preferred YAML metadata for future use
2. **Build a library** — convert all your existing materials to Markdown
3. **Add version control** — commit your materials to Git; your course content becomes trackable and collaborative
4. **Automate batch conversion** — write a shell script to convert all `.md` files at once
5. **Integrate with AI workflows** — feed your course outline to ChatGPT or Claude, ask for exercises in Markdown format, then refine and convert with Pandoc

The payoff: you write once, generate many formats, and maintain a single source of truth. Your materials are future-proof, shareable, and simple to version control.

**What's your current biggest pain point when creating course materials—formatting, version control, or something else?** Reply and let me know.

---

*What's your current workflow for managing and distributing course materials across multiple formats?*
