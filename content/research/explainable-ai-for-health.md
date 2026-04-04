---
title: "Explainable AI for Health"
slug: "explainable-ai-for-health"
icon: "eye"
image: "/img/research/explainable-ai-for-health.svg"
tags: ["xai", "interpretability", "deep-learning"]
date: 2026-01-01
---

## Overview

Deep learning models used in clinical settings must not only be accurate — they must be interpretable. Clinicians need to understand *why* a model predicts high-risk progression to trust and act on that prediction. Explainable AI (XAI) provides tools to open the black box and reveal which input features drive each decision.

## Techniques I apply

### Saliency maps
Gradient-based saliency methods (GradCAM, Integrated Gradients, SHAP for images) highlight which spatial regions of a retinal image or OCT scan most influenced the model's prediction. A heatmap overlaid on a fundus image showing drusen, haemorrhages, or neovascularisation has direct clinical meaning.

### Attention visualisation
Transformer-based models (ViT, MAE) produce attention maps as a by-product. Cross-modal and temporal attention weights reveal which time points and which modality the model "looked at" most when generating a prediction.

### Concept-based explanations
Beyond pixel-level attribution, I explore concept-level explanations where clinically meaningful concepts (drusen area, retinal thickness, vessel tortuosity) are aligned with latent directions in the model's representation space.

## Why XAI matters for regulatory approval

Medical AI systems increasingly fall under MDR/FDA SaMD regulations that require demonstrable transparency and auditability. XAI is not an academic nicety — it is a prerequisite for clinical deployment and regulatory approval.

## Related themes

- [Medical Image Analysis](/research/medical-image-analysis/)
- [Predictive Medicine](/research/predictive-medicine/)
- [Longitudinal Deep Learning](/research/longitudinal-deep-learning/)
