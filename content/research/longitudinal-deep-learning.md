---
title: "Longitudinal Deep Learning"
slug: "longitudinal-deep-learning"
icon: "trending-up"
image: "/img/research/longitudinal-deep-learning.svg"
tags: ["longitudinal", "neural-ode", "progression"]
date: 2026-01-01
---

## Overview

Longitudinal learning models the temporal evolution of a patient's condition from sequences of observations collected over months or years. Unlike standard classification or segmentation tasks, longitudinal models must handle irregular time intervals, missing visits, and the inherent continuity of biological processes. My PhD research produced several architectures specifically designed for this setting.

## Key contributions

### LatiM — Latent Time Models
LatiM is a continuous-time latent variable model that represents disease state as a trajectory in a learned latent space. A Neural ODE governs how the latent state evolves between observations, enabling prediction at arbitrary future time points without discretising the timeline.

### LMT — Longitudinal Mixing Training
LMT addresses the data scarcity problem in longitudinal datasets. Rather than requiring complete observation sequences during training, LMT uses a mixing strategy that synthesises plausible longitudinal progressions from unpaired cross-sectional images, greatly expanding the effective training distribution.

### L-MAE — Longitudinal Masked Autoencoder
L-MAE adapts the masked autoencoder pre-training paradigm to temporal sequences of medical images. By masking both spatial patches and temporal frames, the model learns rich representations that capture both appearance and change over time.

## Why this matters

Early and accurate prediction of disease progression directly informs treatment decisions. For diabetic retinopathy, predicting whether a patient will develop sight-threatening progression within 12 months allows timely laser treatment or anti-VEGF injections that can prevent blindness.

## Related themes

- [Predictive Medicine](/research/predictive-medicine/)
- [Multi-modal Learning](/research/multi-modal-learning/)
- [Self-Supervised Learning](/research/self-supervised-learning/)
