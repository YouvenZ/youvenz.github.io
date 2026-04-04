---
title: "SVG Maker — AI SVG Generator for Inkscape"
date: 2026-01-01
description: "Generate SVG elements from natural language prompts using an LLM, directly inside Inkscape."
status: "active"
tags: ["inkscape", "extension", "svg", "llm", "python", "ai", "open-source"]
github: "https://github.com/YouvenZ/svg_maker_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-svg-maker.svg"
---

## Overview

**SVG Maker** is an Inkscape extension that lets you describe any diagram, icon, or figure in plain English and have an LLM generate the corresponding SVG code, which is then inserted directly into your Inkscape canvas.

## Features

- Natural language → SVG generation powered by GPT-4, Claude, or any OpenAI-compatible API
- Iterative refinement: describe changes to the selected SVG element to modify it
- Preview before insertion
- Works with any Inkscape 1.x installation

## Installation

```bash
git clone https://github.com/YouvenZ/svg_maker_ink
# Copy to your Inkscape extensions folder
# Linux:   ~/.config/inkscape/extensions/
# Windows: %APPDATA%\inkscape\extensions\
```

## Requirements

- Inkscape 1.x
- Python 3.8+
- OpenAI / Anthropic API key (set in extension preferences)
