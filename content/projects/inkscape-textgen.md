---
title: "TextGen Ink — AI Text Generator for Inkscape"
date: 2026-01-01
description: "Generate, rewrite, or refine text elements using an LLM — captions, labels, descriptions — without leaving Inkscape."
status: "active"
tags: ["inkscape", "extension", "text", "llm", "ai", "python", "open-source"]
github: "https://github.com/YouvenZ/textgen_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-textgen.svg"
---

## Overview

**TextGen Ink** is an Inkscape extension that connects any text element on your canvas to a large language model. Select a text frame, choose an operation, and let the LLM generate, rewrite, summarise, or translate your content in-place.

## Use cases

- **Caption generation**: select a figure and generate a descriptive caption
- **Label refinement**: improve the phrasing of axis labels or legend entries
- **Abstract writing**: generate a draft abstract from a set of bullet points
- **Translation**: translate all text elements in a scientific poster to another language

## Supported operations

| Mode | Description |
|---|---|
| Generate | Write new text from a prompt |
| Rewrite | Paraphrase or improve selected text |
| Summarise | Condense long text to a shorter form |
| Translate | Translate to a target language |

## Installation

```bash
git clone https://github.com/YouvenZ/textgen_ink
```
