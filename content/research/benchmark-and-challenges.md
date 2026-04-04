---
title: "Benchmark & Challenges"
slug: "benchmark-and-challenges"
icon: "award"
image: "/img/research/benchmark-and-challenges.svg"
tags: ["benchmark", "challenge", "dataset", "retinal"]
date: 2026-01-01
---

## Overview

Progress in medical AI is only reproducible when the community shares standardised datasets, evaluation protocols, and leaderboards. I contribute to this infrastructure by co-organising international challenges and building open benchmarks that allow fair comparison of methods under identical conditions.

## MARIO Challenge — MICCAI 2024

The **MARIO (Monitoring Age-Related Macular Degeneration Intelligence and Outcomes)** challenge was a satellite event at MICCAI 2024 in Marrakesh. It provided:

- A multi-modal longitudinal OCT dataset for AMD progression prediction
- Standardised train/validation/test splits with held-out labels for fair evaluation
- Two tracks: binary conversion prediction and interval-to-conversion regression
- Participation from international teams across 3 continents

Results were presented at the MICCAI 2024 main conference. The challenge data and evaluation server remain publicly available for continued benchmarking.

### Challenge outcomes

The challenge revealed several key insights:
1. Multi-modal fusion consistently outperformed single-modality approaches
2. Longitudinal models with ≥12 months of history yielded the largest gains
3. Uncertainty calibration was a significant differentiator between top-performing systems

## Why challenges matter

- **Reproducibility**: all participants evaluate on the same held-out test set
- **Community progress**: leaderboards incentivise focused innovation
- **Clinical translation**: challenge metrics are designed in collaboration with clinicians to ensure clinical relevance
- **Data sharing**: challenges make rare clinical datasets accessible under controlled conditions

## Related themes

- [Predictive Medicine](/research/predictive-medicine/)
- [Medical Image Analysis](/research/medical-image-analysis/)
- [Multi-modal Learning](/research/multi-modal-learning/)
