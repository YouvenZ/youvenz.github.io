---
title: "ImageGen Ink — AI Image Generator for Inkscape"
date: 2026-01-01
description: "Generate AI images (Stable Diffusion, DALL·E, Flux) from text prompts as embedded SVG elements."
status: "active"
tags: ["inkscape", "extension", "image-generation", "stable-diffusion", "dalle", "ai", "python", "open-source"]
github: "https://github.com/YouvenZ/Imagegen_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-imagegen.svg"
---

## Overview

**ImageGen Ink** adds AI image generation to Inkscape's toolset. Describe an image in natural language, choose a backend (Stable Diffusion, DALL·E 3, Flux), and the result is embedded as an SVG `<image>` element on your canvas — ready to be combined with vector elements.

## Backends supported

- **Stable Diffusion** (local via Automatic1111 or ComfyUI API)
- **DALL·E 3** (OpenAI API)
- **Flux** (via Replicate or local)

## Typical workflow

1. Open a new layer in Inkscape for raster assets
2. Run `Extensions → ImageGen Ink → Generate`
3. Type your prompt (e.g. *"microscopy image of retinal fundus, professional photo"*)
4. Choose resolution and backend
5. Image is placed on canvas; scale and position as needed

## Installation

```bash
git clone https://github.com/YouvenZ/Imagegen_ink
```
