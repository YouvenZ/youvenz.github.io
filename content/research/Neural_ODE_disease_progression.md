---
title: "Neural ODEs for Disease Progression Modeling"
date: 2023-11-15
draft: false
summary: "Developing Neural Ordinary Differential Equations to model and predict diabetic retinopathy progression."
tags: ["neural odes", "disease progression", "diabetic retinopathy", "deep learning"]
categories: ["current"]
image: "/images/thumbnails/blog1.jpg"
authors: ["Rachid Zeghlache"]
funding: ""
---

## Project Overview

This research project focuses on developing Neural Ordinary Differential Equations (Neural ODEs) to model the continuous-time dynamics of diabetic retinopathy progression. By combining differential equation modeling with deep learning, we aim to predict disease progression trajectories and identify critical intervention points for better patient outcomes.

## Research Objectives

1. Develop Neural ODE architectures for modeling continuous disease progression dynamics
2. Create interpretable models that capture the underlying biological mechanisms of diabetic retinopathy
3. Apply Neural ODEs to predict individual patient progression trajectories
4. Build computationally efficient methods for real-time clinical decision support

## Mathematical Framework

Our approach models disease progression as a continuous dynamical system:

$$\frac{dh(t)}{dt} = f_\theta(h(t), t)$$

where $h(t)$ represents the hidden disease state at time $t$, and $f_\theta$ is a neural network parameterized by $\theta$.

The observed clinical measurements $y(t)$ are related to the hidden state through:

$$y(t) = g_\phi(h(t)) + \epsilon(t)$$

where $g_\phi$ is an observation function and $\epsilon(t)$ represents measurement noise.

For diabetic retinopathy progression, we incorporate multiple biomarkers:

$$\frac{d}{dt}\begin{bmatrix} h_1(t) \\ h_2(t) \\ h_3(t) \end{bmatrix} = \begin{bmatrix} f_1(h(t), \theta) \\ f_2(h(t), \theta) \\ f_3(h(t), \theta) \end{bmatrix}$$

where $h_1(t)$, $h_2(t)$, and $h_3(t)$ represent retinal thickness, vascular density, and inflammatory markers respectively.

## Current Progress


## Collaborators


## Publications



## Funding

