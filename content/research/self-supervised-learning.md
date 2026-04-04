---
title: "Self-Supervised Learning"
slug: "self-supervised-learning"
icon: "zap"
image: "/img/research/self-supervised-learning.svg"
tags: ["self-supervised", "masked-autoencoder", "representation-learning"]
date: 2026-01-01
---

## Overview

Supervised deep learning requires large amounts of labelled data. In medical imaging, expert annotations are expensive, time-consuming, and often in short supply. Self-supervised learning (SSL) sidesteps this bottleneck by learning rich representations from *unlabelled* data through pretext tasks — the labels emerge from the data itself.

## Methods

### Masked Autoencoders (MAE)
Inspired by BERT in NLP, MAE randomly masks a high proportion (75%) of image patches and trains an encoder-decoder to reconstruct the missing regions. The encoder learns spatially rich features without any labels. My L-MAE extends this to temporal sequences of medical images, masking across both space and time.

### Contrastive Learning
Contrastive methods (SimCLR, MoCo, DINO) learn representations by pulling together augmented views of the same image and pushing apart views from different images. In ophthalmology, I explore domain-specific augmentations that respect the clinical semantics of retinal images (e.g., preserving colour balance unlike standard photographic augmentations).

### Longitudinal Self-Supervision
A key insight from my PhD: *a patient's own follow-up visits provide natural supervision signals*. Given images from visit $t$ and visit $t+n$, the model learns to predict the direction of **change** rather than just recognising static features. This is the foundation of L-MAE and part of LatiM's pretraining.

## Why it matters

SSL pre-trained models consistently outperform randomly initialised models on small labelled datasets — exactly the regime that characterises most clinical datasets in rare disease and specialised imaging modalities. A 10% fine-tuning label budget with a strong SSL backbone often matches 100% supervised training from scratch.

## Related themes

- [Longitudinal Deep Learning](/research/longitudinal-deep-learning/)
- [Predictive Medicine](/research/predictive-medicine/)
- [Medical Image Analysis](/research/medical-image-analysis/)
