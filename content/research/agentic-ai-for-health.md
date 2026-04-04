---
title: "Agentic AI for Health"
slug: "agentic-ai-for-health"
icon: "bot"
image: "/img/research/agentic-ai-for-health.svg"
tags: ["agentic-ai", "llm", "rag", "healthcare"]
date: 2026-01-01
---

## Overview

Agentic AI refers to systems where a large language model (LLM) acts not just as a question-answering endpoint, but as an autonomous agent — planning, calling tools, retrieving information, and completing multi-step tasks without constant human intervention. In healthcare, this paradigm opens the door to AI systems that can assist clinical workflows, automate research tasks, and synthesise evidence at scale.

## Frameworks I work with

### LangGraph
LangGraph models agent workflows as stateful directed graphs, enabling complex multi-step reasoning chains with loops, conditional branches, and human-in-the-loop checkpoints. This is particularly useful for clinical decision support pipelines that require evidence retrieval → reasoning → recommendation → validation cycles.

### AutoGen & CrewAI
Multi-agent frameworks where specialised sub-agents collaborate on complex tasks. In biomedical research automation, one agent may retrieve papers, another extracts structured data, and a third synthesises findings into a report.

### Retrieval-Augmented Generation (RAG)
RAG grounds LLM outputs in verified clinical evidence by retrieving relevant passages from a curated knowledge base before generation. This significantly reduces hallucination and is essential for any safety-critical medical application.

## Use cases

- **Clinical literature synthesis**: Automated evidence summaries for systematic reviews
- **Retinal report generation**: Structured radiology-style report generation from ophthalmology images
- **Research copilot**: Automated paper ingestion, annotation, and insight extraction

## Safety considerations

Agentic systems in healthcare require careful guardrails: output verification, human-in-the-loop approval for high-stakes actions, audit trails, and adversarial robustness. My research pays particular attention to evaluating failure modes before any clinical deployment.

## Related themes

- [Explainable AI for Health](/research/explainable-ai-for-health/)
- [Benchmark & Challenges](/research/benchmark-and-challenges/)
