---
title: "Multi-modal Learning"
slug: "multi-modal-learning"
icon: "layers"
image: "/img/research/multi-modal-learning.svg"
tags: ["multi-modal", "fusion", "medical-imaging"]
date: 2026-01-01
---

## Overview

Multi-modal learning addresses one of the fundamental challenges in medical AI: clinical decisions are rarely made from a single data source. A clinician diagnosing diabetic macular oedema consults fundus photographs, OCT B-scans, fluorescein angiography, and the patient's longitudinal record simultaneously. My research develops deep learning architectures that can fuse these heterogeneous modalities into a coherent representation.

## Key research directions

### Cross-modal feature alignment
Standard concatenation of modality-specific features often fails because different modalities live in incompatible representation spaces. I explore contrastive objectives and cross-attention mechanisms that align representations across modalities without requiring paired data at every follow-up visit.

### Missing-modality robustness
In real clinical settings, not every modality is available for every patient at every time point. My models are trained to degrade gracefully when one or more modalities are absent at inference, using masking strategies and conditional generation as priors.

### Ophthalmology-specific fusion
The primary application domain is ophthalmology where fundus images, OCT volumes, and angiography capture complementary aspects of retinal pathology. Combining these sources yields significantly better prediction of progression to advanced AMD and sight-threatening diabetic retinopathy than any single modality alone.

## Representative publications

- *Multi-modal longitudinal learning for AMD progression* — MICCAI 2024
- *LatiM: continuous-time multi-modal representation learning* — MICCAI 2024

## Related themes

- [Longitudinal Deep Learning](/research/longitudinal-deep-learning/)
- [Medical Image Analysis](/research/medical-image-analysis/)
- [Predictive Medicine](/research/predictive-medicine/)
