---
title: "Plt Ink — Matplotlib Figures for Inkscape"
date: 2026-01-01
description: "Write Python Matplotlib code and render publication-quality figures as native SVG directly inside Inkscape."
status: "active"
tags: ["inkscape", "extension", "matplotlib", "python", "data-visualisation", "scientific", "open-source"]
github: "https://github.com/YouvenZ/plt_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-plt.svg"
---

## Overview

**Plt Ink** embeds a Python/Matplotlib code editor inside Inkscape. Write your figure code, hit render, and the resulting SVG is placed on your canvas as a native, fully editable SVG group — not a rasterised image.

## Why native SVG matters

Unlike exporting a PNG from Jupyter and importing it, Plt Ink produces *editable* SVG: individual lines, bars, and labels are XML elements you can select, recolour, or reposition in Inkscape without going back to Python.

## Features

- Full Python editor with syntax highlighting
- `plt.savefig('__ink__.svg')` convention — the extension intercepts the output
- Figure dimensions automatically matched to selected Inkscape frame
- Supports `numpy`, `pandas`, `scipy`, `matplotlib` out of the box

## Example

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 200)
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(x, np.sin(x), lw=2, color='#cba6f7')
ax.set_xlabel('Angle (rad)')
ax.set_ylabel('sin(x)')
plt.tight_layout()
```

## Installation

```bash
git clone https://github.com/YouvenZ/plt_ink
pip install matplotlib numpy
```
