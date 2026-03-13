---
title: 'AI SVG Generator: Create Diagrams in Inkscape with LLMs'
date: '2026-03-05'
draft: false
description: The AI SVG Generator is a new Inkscape extension that lets you generate
  fully editable SVG diagrams by describing them in plain English. Connect your favorite
  LLM (OpenAI, Claude, Google, or LLaMA), write a prompt, and get production-ready
  technical diagrams in seconds—no manual drawing required.
subtitle: Generate editable technical SVGs directly inside Inkscape using your favorite
  LLM—no manual drawing required.
image: /img/thumbnails/2026-03-05-ai-svg-generator-create-diagrams-in-inkscape-with-llms.svg
tags:
- Inkscape
- AI SVG Generator
- LLM
- Diagram generation
- Vector graphics automation
- Claude API
- Technical illustration
- AI-assisted design
categories:
- visualization
is_series: false
article_type: tutorial
cluster: 🎨 Scientific Visualization
critic_score: 8.2
source_transcript: cleaned_transcripts_2026-02-27_12-34-28_Generate_SVG_with_an_LLM_Directly_Inside_Inkscape.md
generated: 2026-03-05_07-45-12
---

# Generate SVG Diagrams with an LLM Directly Inside Inkscape

You've spent the last hour manually drawing a neural network architecture in Inkscape—boxes, arrows, labels, grouped elements—only to realize your client wants it restructured. You start over. This is the pain point: **creating complex technical SVGs by hand is repetitive, time-consuming, and fragile to changes.** What if you could describe the diagram in plain English and have a fully editable SVG appear on your canvas in seconds?

## What This Is

The **AI SVG Generator** is a new Inkscape extension that connects your favorite LLM (OpenAI, Anthropic, Google, or LLaMA) directly to your canvas. Write a natural-language prompt—"neural network with LSTM cells, sigmoid gates, and data flow arrows"—click Apply, and the extension generates a complete, editable SVG object. Every element (shapes, text, groups) is fully modifiable: recolor it, resize it, ungroup it, or delete parts. It's a draft-to-final workflow that turns prompt engineering into design iteration.

## Prerequisites

**Required:**
- Inkscape 1.2 or later (tested on Linux, macOS, Windows)
- An API key from at least one provider:
  - OpenAI (GPT-4 or GPT-4o)
  - Anthropic (Claude 3.5 Sonnet recommended for SVG quality)
  - Google (Gemini 2.0 Flash)
  - Local LLaMA setup (optional, advanced)
- Git installed on your machine
- Basic terminal comfort
- ~5 minutes of setup time

**Recommended:**
- Anthropic API key (Claude produces cleaner SVGs than other models)
- Text editor (VS Code, Sublime, or system default)

## Installation & Setup

### Step 1: Clone the Repository

Open your terminal and navigate to a working directory.

```bash
git clone https://github.com/[creator-username]/svg-maker-inc.git
cd svg-maker-inc
```

This downloads the extension files: `svg_element.py`, `ui.py`, and `config.json`.

### Step 2: Locate Your Inkscape Extensions Folder

Open Inkscape and go to **Edit** → **Preferences** (Windows/Linux) or **Inkscape** → **Preferences** (macOS).

Click the **System** tab on the left sidebar. Look for **User extensions** and click the folder icon next to it.

### Step 3: Create a New Folder for the Extension

In the extensions folder, create a new subfolder:

```bash
mkdir svg_maker_inc
```

### Step 4: Copy Extension Files

Copy the three files from your cloned repository into `svg_maker_inc`:

```bash
cp svg_element.py ui.py config.json /path/to/extensions/svg_maker_inc/
```

### Step 5: Add Your API Keys

Open `config.json` in a text editor:

```json
{
  "openai_api_key": "your-openai-key-here",
  "anthropic_api_key": "your-anthropic-key-here",
  "google_api_key": "your-google-key-here"
}
```

Paste your API keys into the appropriate fields. Save the file.

> ⚠️ **Never commit this file to a public repository.** Add `config.json` to your `.gitignore`.

### Step 6: Restart Inkscape

Close Inkscape completely and reopen it. Verify installation by going to **Extensions** → **Generate** → **AI SVG Generator**. You should see the dialog window.

## Core Workflow

### Step 1: Open the AI SVG Generator Dialog

In Inkscape, go to **Extensions** → **Generate** → **AI SVG Generator**.

A dialog window opens with these fields:
- **AI Provider** (dropdown)
- **Prompt** (large text area)
- **Model** (auto-populated based on provider)
- **Size** (width/height in pixels)
- **Style** (technical, minimal, detailed, etc.)
- **Color Scheme** (monochrome, pastel, vibrant)
- **Positioning** (center, origin, next to selection)
- **Group Output** (checkbox)
- **Apply** button

### Step 2: Select Your AI Provider

Click **AI Provider** and choose one:
- **Anthropic** (recommended—Claude produces cleanest SVGs)
- **OpenAI** (fast, good for simple diagrams)
- **Google** (cost-effective)
- **LLaMA** (local, requires setup)

### Step 3: Enter Your Prompt

Describe the SVG you want in plain English. Specificity matters.

**Good prompt:**
> A flowchart showing a machine learning pipeline: input data → preprocessing → model training → evaluation → output predictions. Use boxes for steps, arrows for flow. Label each box clearly.

**Weak prompt:**
> Make a diagram.

Include:
- Element types (boxes, circles, arrows, text)
- Labels and content
- Relationships and flow
- Visual style hints

### Step 4: Configure Output (Optional)

- **Size:** Set width and height (default: 800×600 px)
- **Style:** Choose technical, minimal, detailed, or artistic
- **Color Scheme:** Choose monochrome, pastel, vibrant
- **Positioning:** Where the SVG appears on canvas
- **Group Output:** Check to group all elements as one object

### Step 5: Click Apply

The extension sends your prompt to the LLM. Processing time: 2–10 seconds depending on complexity.

The generated SVG appears on your canvas, fully editable.

### Step 6: Edit and Iterate

The SVG is completely modifiable:
- **Select elements** individually with the selection tool
- **Change colors:** Right-click → Fill and Stroke
- **Resize:** Drag handles or use the Transform panel
- **Ungroup:** Right-click → Ungroup to edit individual shapes
- **Delete:** Select and press Delete
- **Reposition:** Drag or use arrow keys

Refine your prompt and click **Apply** again if needed. Delete the old version and iterate.

## Practical Example: LSTM Cell Diagram

**Scenario:** You need to illustrate an LSTM cell for a machine learning blog post. Manual drawing takes 30+ minutes. Using the extension:

**Prompt:**
```
Create a detailed LSTM cell diagram showing:
- Input gate with sigmoid activation function
- Forget gate with sigmoid activation function
- Cell state with tanh activation
- Output gate with sigmoid activation function
- Cell state line flowing left to right
- Input arrow entering from the left
- Output arrow exiting to the right
Use rectangles for operations, circles for activation functions, and arrows to show data flow. Label each component clearly. Style: technical, minimal design.
```

**Result:** A complete LSTM diagram with labeled gates, activations, and flow arrows appears in ~5 seconds.

**Next iteration:** Refine the prompt to add more detail:

```
Improve the LSTM cell diagram by adding:
- Tanh activation functions shown as circles
- Pointwise multiplication operations shown as ⊗ symbols
- Pointwise addition operations shown as ⊕ symbols
- Clearer labeling of hidden state and cell state
- Color coding: gates in blue, activations in green, operations in orange
```

A polished, professional diagram appears. You can now ungroup elements to adjust individual colors, resize the entire diagram, and export as PDF or PNG.

## Common Issues & Fixes

### "Extension not found in menu"
**Cause:** Inkscape didn't reload the extension.

**Fix:** Completely close Inkscape (check Activity Monitor/Task Manager). Reopen it.

### "API key invalid" error
**Cause:** Typo in `config.json` or expired key.

**Fix:** 
- Double-check your API key in the config file (no extra spaces)
- Regenerate the key in your provider's dashboard
- Restart Inkscape

### Generated SVG is too small or large
**Cause:** Default size doesn't match your document scale.

**Fix:** Adjust **Size** (width/height in pixels) before clicking Apply. For print at 300 dpi: multiply desired inches by 300. For web at 72 dpi: multiply desired inches by 72.

### SVG elements are grouped but I need to edit individual shapes
**Cause:** **Group Output** was enabled.

**Fix:** Right-click the SVG → **Ungroup** (Ctrl+Shift+G). Each element is now individually selectable.

### Generated diagram is incomplete or missing elements
**Cause:** Vague prompt or LLM struggled with complexity.

**Fix:** 
- Refine your prompt with more detail
- Break complex diagrams into smaller parts
- Switch to Anthropic (Claude) for better output quality

## Next Steps

1. **Generate a simple diagram** (flowchart, org chart) to get comfortable with prompting.
2. **Experiment with different AI providers** to find your preferred output style.
3. **Build a prompt library** for recurring diagram types (neural networks, pipelines, state machines).
4. **Save source files** of every generated SVG for version control and iteration.
5. **Combine with native Inkscape tools:** Generate a base diagram, then hand-refine details.

The real power isn't replacing manual design—it's compressing the draft-to-feedback cycle. Instead of 2 hours drawing, you spend 10 minutes prompting and 10 minutes refining. Client asks for changes? Update the prompt, regenerate, and iterate in real time.

---

**What kind of diagram would you generate first if you installed this extension today? Reply and let me know—I'd love to see what you build.**

---

*What's the most complex diagram you've had to redraw, and how would an AI-powered tool change your workflow?*
