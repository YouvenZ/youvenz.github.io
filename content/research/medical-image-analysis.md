---
title: "Medical Image Analysis"
slug: "medical-image-analysis"
icon: "image"
image: "/img/research/medical-image-analysis.svg"
tags: ["medical-imaging", "oct", "ophthalmology", "fundus"]
date: 2026-01-01
---

## Overview

Medical image analysis is the computational backbone of my research. Before building longitudinal or predictive models, we need robust methods for understanding what is in a single image: detecting lesions, quantifying biomarkers, segmenting anatomical structures. In my work the primary modalities are ophthalmological.

## Imaging modalities

### Colour Fundus Photography
Wide-field retinal photographs capture the optic disc, macula, vessels, and peripheral retina. DR grading, vessel segmentation, and optic disc detection are well-established tasks. I use fundus images as the primary modality in several longitudinal and progression prediction pipelines.

### Optical Coherence Tomography (OCT)
OCT provides cross-sectional depth profiles of retinal layers with micrometre resolution. Retinal layer segmentation, drusen volume measurement, and detection of fluid (IRF/SRF/PED) are key tasks for AMD monitoring. OCT is the workhorse modality in the MARIO challenge.

### Fluorescein Angiography (FA)
FA captures vascular leakage and neovascularisation patterns that are invisible on fundus photography or OCT. Incorporating FA into multi-modal fusion models adds complementary disease activity information.

## Core tasks

| Task | Modality | Relevance |
|---|---|---|
| DR grading | Fundus | Screening automation |
| AMD staging | OCT + Fundus | Progression monitoring |
| Fluid detection | OCT | Treatment decision |
| Vessel segmentation | Fundus / FA | Biomarker extraction |
| Layer segmentation | OCT | Thickness maps |

## Related themes

- [Multi-modal Learning](/research/multi-modal-learning/)
- [Self-Supervised Learning](/research/self-supervised-learning/)
- [Benchmark & Challenges](/research/benchmark-and-challenges/)
