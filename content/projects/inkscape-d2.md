---
title: "D2 Ink — D2 Architecture Diagrams for Inkscape"
date: 2026-01-01
description: "Write and render D2 architecture diagrams and entity-relationship diagrams as editable SVG inside Inkscape."
status: "active"
tags: ["inkscape", "extension", "d2", "diagrams", "architecture", "python", "open-source"]
github: "https://github.com/YouvenZ/D2_ink"
demo: ""
paper: ""
thumbnail: "/img/projects/inkscape-d2.svg"
---

## Overview

**D2 Ink** integrates the [D2 diagram language](https://d2lang.com) into Inkscape. D2 produces beautiful, automatically-laid-out architecture diagrams, entity-relationship diagrams, and software design maps from a declarative text syntax.

## Why D2?

D2's automatic layout engine (powered by ELK, Dagre, or TALA) produces publication-quality diagrams without manual positioning. Combined with Inkscape's SVG editing capabilities, D2 Ink is perfect for creating and then polishing technical architecture figures for papers and presentations.

## Example

```d2
User -> API Gateway -> Auth Service
API Gateway -> Business Logic
Business Logic -> Database
```

## Installation

```bash
git clone https://github.com/YouvenZ/D2_ink
```

Requires [D2 CLI](https://d2lang.com/tour/install) to be on your `PATH`.
