---
title: "Deep Learning for Retinal Degeneration Assessment: The MARIO AMD Progression Challenge"
date: 2024-10-10
draft: false
summary: "A comprehensive analysis of the MARIO challenge held at MICCAI 2024, evaluating AI algorithms for detecting and monitoring age-related macular degeneration progression using OCT imaging."
tags: ["deep learning", "medical imaging", "AMD", "OCT", "retinal imaging", "computer vision", "MICCAI challenge"]
categories: ["current"]
image: "/images/thumbnails/mario_challenge.jpg"
authors: ["Rachid Zeghlache and al."]
funding: "French National Research Agency (ANR) - Evired project RHU program - ANR-18-RHUS-0008"
---

## Project Overview

The MARIO (Monitoring Age-Related macular degeneration with Intelligent Ophthalmology) challenge represents a landmark initiative in applying artificial intelligence to retinal disease monitoring. Held at MICCAI 2024 in Marrakesh, this challenge specifically addressed the critical need for automated detection and monitoring of age-related macular degeneration (AMD) through optical coherence tomography (OCT) image analysis.

## Research Objectives

The challenge focused on two primary computational tasks:

1. **Task 1: Evolution Classification** - Classify changes between two consecutive 2D OCT B-scans to detect disease activity modifications
2. **Task 2: Progression Prediction** - Predict future AMD evolution over a three-month period for patients undergoing anti-VEGF therapy

## Dataset and Methodology

The challenge utilized a unique multi-modal dataset comprising:
- **Primary Dataset**: 136 patients from Brest, France (training and testing)
- **Auxiliary Dataset**: 5 patients from Algeria (domain adaptation evaluation)
- **Data Types**: OCT B-scans, infrared localizer images, and clinical metadata
- **Annotation**: Expert ophthalmologist annotations with inter-annotator agreement analysis

## Key Findings

### Challenge Results
- **35 teams participated** with 12 finalists presenting their methodologies
- **Task 1 Success**: AI algorithms demonstrated performance comparable to physicians in measuring AMD progression
- **Task 2 Challenges**: Prediction of future evolution remains difficult, with no team achieving fully satisfactory results

### Technical Innovations
- **Foundation Models**: Teams using RetFound (retinal-specific pre-trained models) showed superior performance
- **Multi-modal Learning**: Integration of OCT images, localizer data, and clinical variables improved outcomes
- **Domain Adaptation**: Significant performance variations observed between European and African datasets

## Clinical Significance

The challenge addressed a critical gap in longitudinal monitoring of neovascular activity in AMD patients receiving anti-VEGF therapy. Current treatment paradigms (fixed-interval, PRN, treat-and-extend) require accurate assessment of disease activity markers, particularly fluid presence and evolution patterns.

## Collaborators

- **LaTIM UMR 1101, Inserm** - Primary organizing institution
- **CHU Brest** - Clinical data provider and expert annotations
- **Lazouni Ophthalmology Clinic, Algeria** - Domain adaptation dataset
- **35 International Teams** - Algorithm development and validation

## Publications

1. Zeghlache, R., et al. (2025). "Deep Learning for Retinal Degeneration Assessment: A Comprehensive Analysis of the MARIO AMD Progression Challenge." arXiv:2506.02976v2 [cs.CV].

## Technical Achievements

### Winning Methodologies
- **MIPLAB Team**: Multi-modal fusion approach combining OCT, localizer images, and clinical variables
- **yyama Team**: MaxViT architecture with innovative image concatenation strategies
- **MIC Group 6**: Siamese networks with foundation model encoders

### Performance Metrics
- **Task 1**: F1-scores ranging from 0.691 to 0.858 across teams
- **Task 2**: Quadratic Weighted Kappa scores indicating substantial room for improvement
- **Cross-dataset Performance**: Notable degradation when applying models to different populations/devices

## Future Directions

The challenge identified several areas for advancement:

1. **Enhanced Generative Approaches**: Better synthetic data generation for data augmentation
2. **Improved Multi-modal Integration**: Standardized frameworks for combining diverse data types
3. **Domain Adaptation**: Robust methods for handling population and device shifts
4. **Temporal Modeling**: Advanced architectures for longitudinal disease progression
5. **Clinical Integration**: Incorporation of treatment history and patient-specific factors

## Funding

This research was conducted within the Evired project framework, funded by the French National Research Agency (ANR) under the RHU program, with support from the French government's "Investissements d'Avenir" program (ANR-18-RHUS-0008).

## Data Availability

The Brest dataset has been made publicly available via Zenodo to facilitate reproducible research and continued algorithm development in the AMD monitoring domain.