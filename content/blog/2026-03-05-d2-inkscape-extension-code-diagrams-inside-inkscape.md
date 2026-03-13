---
title: 'D2 Inkscape Extension: Code Diagrams Inside Inkscape'
date: '2026-03-05'
draft: false
description: The D2 Inkscape extension lets you write diagrams as code and render
  them live inside Inkscape as editable SVG. Perfect for researchers and technical
  writers who iterate frequently, it eliminates manual redrawing and locked-in exports—just
  edit the code and re-render in seconds.
subtitle: Generate editable system diagrams from D2 code directly in Inkscape—no more
  static exports.
image: /img/thumbnails/2026-03-05-d2-inkscape-extension-code-diagrams-inside-inkscape.svg
tags:
- D2 diagrams
- Inkscape extension
- technical writing
- system architecture
- diagram automation
- SVG generation
- code-based diagramming
- researcher tools
categories:
- visualization
is_series: false
article_type: tutorial
cluster: 🎨 Scientific Visualization
critic_score: 8.8
source_transcript: cleaned_transcripts_2026-02-27_12-40-03_Use_D2_Diagrams_Directly_Inside_Inkscape_NEW_Exten.md
generated: 2026-03-05_07-51-13
---

# Generate Code-Based Diagrams Directly Inside Inkscape Using D2 — For Researchers & Technical Writers

You've spent 20 minutes manually recreating a system architecture diagram in Inkscape because you changed the layout. Or you exported a PNG from a diagram tool, imported it, and now it's locked—you can't edit text or connections without starting over.

The **D2 Inkscape extension** eliminates this friction: write your diagram as code, generate it live inside Inkscape, and keep full editability. No more conversion workflows. No more locked-in exports.

## What This Is

**D2** is a text-based diagram framework that renders flowcharts, system architectures, sequence diagrams, and UML classes as editable SVG directly inside Inkscape. Unlike static exports, everything stays modifiable: colors, text, layout, connections, line thickness, labels. You can delete elements, reorder them, and adjust placement without touching the original code.

This is especially powerful for researchers, technical writers, and course creators who iterate on diagrams frequently. Instead of redrawing when requirements change, you edit the D2 code and re-render in seconds.

## Prerequisites

**Software:**
- Inkscape 1.0 or later
- **D2 CLI** installed on your system
- Git (for cloning the extension)
- Python 3.6+ (usually bundled with Inkscape)

**Operating Systems:**
- Linux (simplest installation)
- macOS (via Homebrew or binary)
- Windows (via `.msi` installer or Scoop)

**Knowledge Level:**
- Basic Inkscape familiarity
- Comfort with terminal (3–4 commands total)
- No prior D2 syntax knowledge required

## Installation & Setup

### Step 1: Install D2 CLI

**Linux:**

```bash
curl -fsSL https://d2lang.com/install.sh | sh -s --
```

**macOS (Homebrew):**

```bash
brew install d2
```

**Windows:**

Download the latest `.msi` from [d2lang.com/releases](https://d2lang.com/releases) and run it. This adds D2 to your PATH automatically.

### Step 2: Verify Installation

```bash
d2 --version
```

You should see a version number (e.g., `D2 v0.6.5`). On Windows, close and reopen your terminal after installing the `.msi` for PATH changes to take effect.

### Step 3: Clone the Extension Repository

```bash
git clone https://github.com/d2lang/d2-inkscape.git
```

### Step 4: Find Your Inkscape Extensions Folder

1. Open Inkscape
2. Go to **Edit** → **Preferences**
3. Click **System** in the left sidebar
4. Click **User Extensions** — a file browser opens

**Typical paths:**
- **Linux:** `~/.config/inkscape/extensions/`
- **macOS:** `~/Library/Application Support/Inkscape/extensions/`
- **Windows:** `C:\Users\[YourUsername]\AppData\Roaming\Inkscape\extensions\`

### Step 5: Install Extension Files

1. Create a folder named `d2-inkscape` in your extensions directory
2. Copy all files from the cloned repository into it
3. Close Inkscape completely, then reopen it

### Step 6: Test the Installation

Go to **Extensions** → **D2 Diagrams** → **D2 Render**. A dialog should appear. Verify D2 is accessible:

```bash
which d2
```

(On Windows: `where d2`)

You should see the path to your D2 executable (e.g., `/usr/local/bin/d2`).

## Core Workflow

### Step 1: Open an Inkscape Document

Start a new document (**File** → **New**) or open an existing one.

### Step 2: Access the D2 Extension

Navigate to **Extensions** → **D2 Diagrams** → **D2 Render**. The configuration dialog opens.

### Step 3: Choose Your Diagram Type

Select from preset examples or paste your own **D2 code**. Common types:
- **Flowchart** (boxes and arrows)
- **Sequence Diagram** (interactions over time)
- **Class Diagram** (UML structure)
- **Graph** (nodes and connections)

### Step 4: Configure Output Settings

- **Format:** `SVG` (editable) or `PNG` (fixed)
- **Theme:** Built-in options (Neutral, Dark, Sketch)
- **Layout Engine:** `dagre` (default) or `elk` (better for complex layouts)
- **Sketch Mode:** Toggle for hand-drawn appearance
- **Scaling:** `Auto` (document-fit) or `Manual` (fixed dimensions)

### Step 5: Set Placement & Layer

- **Placement:** Center, Top-Left, or other anchors
- **Layer:** Optionally group the diagram in a named layer
- **Temporary Directory:** Where D2 writes intermediate files (default is fine)

### Step 6: Render

Click **Apply**. D2 generates your diagram and embeds it on the canvas. Wait 3–5 seconds for rendering.

### Step 7: Edit the Result

The diagram appears as an SVG group. You can now:
- Select individual elements and change colors
- Resize boxes by dragging handles
- Edit text directly (double-click)
- Delete or reorder elements
- Adjust line thickness and style

### Step 8: Iterate (Optional)

To update:
1. Edit your D2 code in the dialog
2. Click **Apply** again
3. The new version replaces the old one

## Practical Example

You're writing a research paper and need a simple system architecture diagram showing three microservices communicating with a database.

**D2 Code:**

```d2
direction: right

API [label: "API Gateway"]
Auth [label: "Auth Service"]
Data [label: "Data Service"]
DB [label: "PostgreSQL"]

API -> Auth: authenticate
API -> Data: query
Auth -> DB: verify user
Data -> DB: fetch records
```

**Steps:**

1. Open **Extensions** → **D2 Diagrams** → **D2 Render**
2. Paste the code above
3. Set **Theme** to "Neutral" and **Layout Engine** to "dagre"
4. Click **Apply**

**Result:** A clean, left-to-right diagram appears showing the three services and database with labeled arrows.

**Editing:** You realize the API should also connect directly to the database for caching. Simply add one line:

```d2
API -> DB: cache check
```

Re-open the dialog, add the line, click **Apply**, and the diagram updates instantly. No re-drawing. No manual repositioning.

## Common Issues & Fixes

### "D2 Command Not Found" Error

Verify D2 is installed:

```bash
d2 --version
```

- On Windows, restart your terminal after installing the `.msi`
- On macOS, ensure installation completed:

```bash
brew install d2
```

- In the extension dialog, manually set the D2 executable path (e.g., `/usr/local/bin/d2` on macOS or `C:\Program Files\D2\d2.exe` on Windows)

### Diagram Looks Distorted or Off-Center

- Adjust the **Placement** option (try Center)
- Change **Scaling** from Auto to Manual with a specific dimension
- Try a different **Layout Engine** (`elk` instead of `dagre`)
- Increase the **Temporary Directory timeout** if rendering is incomplete

### SVG Edits Don't Persist After Re-rendering

Place your manual edits on a separate layer from the D2 diagram. Remember: re-rendering replaces the entire group, so save edits separately or export as PNG for reference.

### Text or Connectors Look Blurry

- Ensure you're exporting to **SVG**, not PNG
- Zoom in to verify—Inkscape may display at reduced quality at low zoom
- If exporting to PNG, increase DPI in the export dialog

## Next Steps

1. **Learn D2 Syntax:** Visit the [D2 playground](https://play.d2lang.com) to experiment with sequence diagrams, class diagrams, tables, and more.

2. **Try Advanced Themes:** The extension supports multiple themes. Experiment to match your paper or presentation style.

3. **Combine with Inkscape Tools:** Use Inkscape's native tools (text, shapes, annotations) alongside D2 diagrams for hybrid technical figures.

4. **Automate Batch Diagrams:** Script D2 CLI directly for bulk generation, then import into Inkscape.

5. **Share Editable Diagrams:** Export as SVG and share the `.svg` file with collaborators—they can edit the diagram code without special software.

**What diagram type are you planning to create first—a system architecture, flowchart, or sequence diagram? Reply with your use case, and I'll show you the exact D2 syntax you'll need.**

---

*What's your current workflow for creating and updating technical diagrams—and how often do you find yourself redrawing when requirements change?*
