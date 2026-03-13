---
title: 'AI Text Generator for Inkscape: LLM Inside'
date: '2026-03-05'
draft: false
description: The AI Text Generator extension lets you generate, rewrite, translate,
  and edit text directly inside Inkscape using ChatGPT, Claude, or local LLMs—no context-switching
  required. This guide covers installation, API setup, and core workflows for designers
  seeking AI-powered copy generation without leaving the canvas.
subtitle: Generate, rewrite, and translate design text without leaving Inkscape. Free
  extension for ChatGPT, Claude, and local models.
image: /img/thumbnails/2026-03-05-ai-text-generator-for-inkscape-llm-inside.svg
tags:
- Inkscape
- AI Text Generator
- LLM extension
- ChatGPT integration
- Claude API
- design automation
- AI for designers
- local LLM
categories:
- visualization
is_series: false
article_type: tutorial
cluster: 🎨 Scientific Visualization
critic_score: 8.5
source_transcript: cleaned_transcripts_2026-02-27_12-37-58_Generate_Text_with_an_LLM_Directly_Inside_Inkscape.md
generated: 2026-03-05_07-48-46
---

# Generate Text with an LLM Directly Inside Inkscape — For Designers Who Want AI Copy Without Leaving the App

You're three iterations deep on a design mockup. The headline needs tweaking. The body copy should be shorter. And wait—the client just asked for a French version. You close Inkscape, open ChatGPT, paste the text, copy the result, switch back, paste it in, adjust the font, and realize it doesn't fit anymore.

There's a better way. What if you could **generate, rewrite, translate, and edit all your design text without ever leaving Inkscape**?

## What This Is

The **AI Text Generator** is a free Inkscape extension that pipes your design text directly to local or cloud-based LLMs (ChatGPT, Claude, or self-hosted Llama). Instead of context-switching to a separate tool, you:

- **Create** new text from scratch using custom prompts
- **Modify** selected text: rewrite, translate, expand, summarize, or adjust tone
- **Apply changes in-place** without duplicate layers
- **Control everything** from a single panel: API keys, model selection, temperature, and token limits

No manual copy-paste. No broken formatting. No leaving your canvas.

## Prerequisites

**Software:**
- Inkscape 1.2 or later (Windows, macOS, Linux)
- Git (for cloning the repository)
- A text editor

**API Requirements (pick one):**
- **Cloud:** OpenAI, Google Gemini, Anthropic Claude, or Microsoft Azure API key
- **Local:** Ollama or LLaMA.cpp with a model downloaded (e.g., `mistral`, `llama2`)

**System Knowledge:**
- Basic comfort navigating Inkscape's Extensions menu
- Ability to locate your system's extensions folder
- Familiarity with copying API keys and editing JSON files

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/[creator]/ai-text-generator.git
```

### Step 2: Find Your Extensions Folder

In Inkscape, go to **Edit → Preferences → System → User Extensions**. A file browser opens showing your extensions directory.

**Common paths:**
- **Linux:** `~/.config/inkscape/extensions/`
- **macOS:** `~/Library/Application Support/Inkscape/extensions/`
- **Windows:** `%APPDATA%\Inkscape\extensions\`

### Step 3: Create a New Folder and Copy Files

Create a subfolder named `textgen` in your extensions directory, then copy these three files from the cloned repo:

```bash
mkdir ~/.config/inkscape/extensions/textgen
cp /path/to/cloned/repo/textgen.inx ~/.config/inkscape/extensions/textgen/
cp /path/to/cloned/repo/textgen.py ~/.config/inkscape/extensions/textgen/
cp /path/to/cloned/repo/config.example.json ~/.config/inkscape/extensions/textgen/
```

### Step 4: Configure Your API Credentials

Rename `config.example.json` to `config.json`:

```bash
mv ~/.config/inkscape/extensions/textgen/config.example.json ~/.config/inkscape/extensions/textgen/config.json
```

Open `config.json` in your text editor and add your credentials:

```json
{
  "provider": "openai",
  "api_key": "sk-your-actual-api-key-here",
  "model": "gpt-4-turbo",
  "temperature": 0.7,
  "max_tokens": 500
}
```

Save the file. ⚠️ **Keep your API key private—never commit this file to version control.**

### Step 5: Restart Inkscape

Close and reopen Inkscape completely. Navigate to **Extensions → Text → AI Text Generator**. If you see this menu item, you're ready to go.

## Core Workflow

### Creating New Text from Scratch

1. Go to **Extensions → Text → AI Text Generator → Create Text**.

2. Enter your prompt in the "Text Prompt" field.
   - Example: `"Write a punchy tagline for a sustainable fashion brand in 5 words or less."`

3. (Optional) Adjust settings:
   - **Tone:** Formal, casual, playful, technical
   - **Language:** English, French, Spanish, etc.
   - **Temperature:** Lower (0.3) = consistent; Higher (0.9) = creative

4. Click **Apply**. The LLM generates text as a new object on your canvas. Position and style it using Inkscape's normal text tools.

### Modifying Existing Text

1. Select the text object you want to modify.

2. Go to **Extensions → Text → AI Text Generator → Modify Text**.

3. Choose an action:
   - **Rewrite:** Rephrase while keeping meaning
   - **Translate:** Convert to another language
   - **Summarize:** Condense to key points
   - **Expand:** Add detail and explanation
   - **Change Tone:** Shift from casual to formal

4. (Optional) Add a custom instruction in "Additional Prompt."
   - Example: `"Make it sound more urgent and action-oriented."`

5. Click **Apply**. The text updates in place—no new layer, no duplication.

## Practical Example

You're designing a landing page for a fitness app. Your headline reads: "Get fit fast." The client wants it to sound more motivational and energetic.

1. Select the text "Get fit fast" on your canvas.

2. Open **Extensions → Text → AI Text Generator → Modify Text**.

3. Select **Action: Rewrite** and **Tone: Playful & Energetic**.

4. In "Additional Prompt," type: `"Use exclamation marks and action verbs. Keep it under 4 words."`

5. Click **Apply**. Text updates to: "Crush Your Fitness Goals!"

6. Font size and color remain unchanged. Now you want a Spanish version.

7. With the same text selected, open **Modify Text** again.

8. Select **Action: Translate** and **Language: Spanish**.

9. Click **Apply**. Text now reads: "¡Domina Tus Objetivos de Fitness!"

All changes happened inside Inkscape. No tab-switching. No manual copy-paste. No formatting loss.

## Common Issues & Fixes

**Extension not appearing in menu after restart**
- Double-check that all three files (`textgen.inx`, `textgen.py`, `config.json`) are in the same `textgen` subfolder.
- Verify the folder path matches your Inkscape preferences.
- Restart your computer to clear the extension cache.

**API key error or "401 Unauthorized"**
- Log into your API provider's dashboard and generate a fresh API key.
- Copy it exactly—no extra spaces.
- Paste it into `config.json` and restart Inkscape.

**"Model not found" error**
- For **OpenAI:** Verify you're using a current model name like `gpt-4-turbo` or `gpt-3.5-turbo`.
- For **local models (Ollama):** Ensure Ollama is running and the model is downloaded. Test with: `ollama list`.
- Update `config.json` with the correct model name.

**Generated text has unwanted markdown formatting**
- Use the **Post-Processing** option in the dialog to strip markdown.
- Or add to your prompt: `"Do not use markdown formatting. Return plain text only."`

## Next Steps

You now have a workflow that cuts design iteration time in half.

**What to try next:**
- Experiment with different **temperature** settings (0.3–0.9) to find the right balance between consistency and creativity for your brand voice.
- Use **local models** (Ollama) if you want to avoid API costs or keep text generation private.
- Combine this with Inkscape's other AI extensions for a fully integrated design workflow.

What type of design work would benefit most from instant AI text generation in your workflow? Reply and let me know.

---

*What's your current workflow for generating copy in design projects—and would you switch to in-app LLM generation?*
