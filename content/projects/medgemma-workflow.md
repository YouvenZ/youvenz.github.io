---
title: "MedFlowAssist"
date: 2026-02-01
description: "A multi-agent medical assistant powered by MedGemma, MedASR & LiteLLM with 13 clinical workflows, voice dictation, and multimodal document support."
status: "active"
tags: ["agentic-ai", "medgemma", "healthcare", "llm", "python", "flask", "multi-agent"]
github: "https://github.com/YouvenZ/MedFlowAssit"
demo: ""
paper: ""
thumbnail: ""
---

## Overview

**MedFlowAssist** is a multi-agent medical assistant that combines the power of [MedGemma](https://deepmind.google/models/medgemma/), medical speech recognition (MedASR), and [LiteLLM](https://github.com/BerriAI/litellm) to deliver clinical-grade AI assistance across a wide range of healthcare workflows.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://github.com/YouvenZ/MedFlowAssit#prerequisites)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)](https://github.com/YouvenZ/MedFlowAssit#quick-start-step-by-step)
[![License: Research](https://img.shields.io/badge/License-Research%20%2F%20Educational-green)](https://github.com/YouvenZ/MedFlowAssit#license)

## Key Features

- **13 clinical workflows** covering documentation, triage, diagnosis support, and more
- **12 pre-built scenarios** ready to deploy out of the box
- **Voice dictation** via MedASR for hands-free clinical note-taking
- **Multimodal input** — image, PDF, and CSV upload supported
- **Multi-agent orchestration** with LangGraph-style task delegation

## Clinical Workflows

The assistant covers end-to-end workflows including:
- Patient history summarisation
- Differential diagnosis generation
- Radiology report analysis
- Lab result interpretation
- Clinical note drafting (SOAP format)
- Drug interaction checking
- ICD-10 coding assistance

## Architecture

```
User Input (text / voice / image / PDF)
         │
         ▼
   MedFlowAssist Router
    ├── MedGemma (vision + language)
    ├── MedASR (speech → text)
    └── LiteLLM Proxy (model routing)
         │
         ▼
   Clinical Workflow Agents
    ├── Summariser
    ├── Diagnostics
    ├── Documentation
    └── ...
```

## Quick Start

```bash
git clone https://github.com/YouvenZ/MedFlowAssit
cd MedFlowAssit
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` to access the interface.

## Prerequisites

- Python 3.11+
- API key for MedGemma or compatible model endpoint
- (Optional) MedASR setup for voice features
