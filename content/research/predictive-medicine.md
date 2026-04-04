---
title: "Predictive Medicine"
slug: "predictive-medicine"
icon: "activity"
image: "/img/research/predictive-medicine.svg"
tags: ["diabetic-retinopathy", "amd", "prediction"]
date: 2026-01-01
---

## Overview

Predictive medicine applies machine learning to answer the clinical question: *what will happen to this patient?* Rather than diagnosing the current state, predictive models estimate the probability and timeline of future events — disease progression, treatment response, or transition to a more severe stage.

## Clinical applications

### Diabetic Retinopathy Progression
Diabetic retinopathy is the leading cause of blindness in working-age adults globally. My research builds end-to-end deep learning pipelines that process sequential retinal fundus images and OCT scans to predict whether a patient will progress to proliferative DR or develop diabetic macular oedema within a given follow-up window.

### Age-Related Macular Degeneration (AMD)
AMD progression from early/intermediate to late neovascular AMD is a critical decision point for preventive treatment with anti-VEGF agents. Models trained on multi-modal imaging data from the MARIO dataset can identify high-risk patients up to 12 months before conversion.

### MARIO Challenge
I co-organised the **MARIO AMD Progression Monitoring Challenge** at MICCAI 2024, providing the community with a standardised benchmark and evaluation protocol for AMD progression prediction from longitudinal OCT imaging.

## Methodology

The pipeline typically involves:
1. **Pre-training** on large unlabelled imaging datasets (self-supervised)
2. **Fine-tuning** on labelled longitudinal cohorts with survival or classification objectives
3. **Calibration** to produce reliable probability estimates for clinical decision support

## Related themes

- [Longitudinal Deep Learning](/research/longitudinal-deep-learning/)
- [Multi-modal Learning](/research/multi-modal-learning/)
- [Benchmark & Challenges](/research/benchmark-and-challenges/)
