---
title: 'Apptainer & Conda: Reproducible HPC Python Environments'
date: '2026-03-05'
draft: false
description: 'Apptainer + Conda solves the researcher''s tax: environment reproduction
  across machines. Package your complete Python environment—dependencies, versions,
  and all—into a single .sif file that runs identically on your laptop and HPC cluster.
  Learn the exact workflow from local Conda export to production deployment.'
subtitle: Build once, run anywhere. Container-based Python for HPC clusters without
  the environment headaches.
image: /img/thumbnails/2026-03-05-apptainer-conda-reproducible-hpc-python-environments.svg
tags:
- Apptainer
- Conda
- HPC
- containerization
- reproducible research
- Python environments
- SLURM
- cluster computing
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 8.0
source_transcript: cleaned_transcripts_2026-02-27_12-15-26_Advanced_Apptainer_Best_Practices__Container_Manag.md
generated: 2026-03-05_07-27-17
---

# Build Reproducible Python Environments with Apptainer & Conda — For HPC Researchers

Your Python script runs perfectly on your laptop. You transfer it to the cluster. Runtime fails. Missing dependencies. Version conflicts. Different Python builds. You spend hours debugging environment mismatches instead of running science.

This is the researcher's tax: **environment reproduction across machines is broken by default.**

## What This Solves

**Apptainer** (formerly Singularity) is a containerization tool built for HPC clusters. Unlike Docker, it doesn't require root privileges and integrates seamlessly with cluster job schedulers like SLURM and PBS. Combined with **Conda**, it lets you package a complete, reproducible Python environment—dependencies, versions, and all—into a single `.sif` file that runs identically on your laptop, your colleague's machine, and any HPC node.

**What you'll do today:** Build a Conda environment locally → export its configuration → embed it in an Apptainer container → deploy to your cluster.

## Prerequisites

**Software:**
- **Apptainer** ≥ 1.0 (or Singularity 3.8+)
- **Conda** (Anaconda or Miniconda) installed locally
- **Cluster access** with Apptainer installed (`apptainer --version` to verify)
- **Disk space:** ~5–10 GB for building

**Systems:** Linux, macOS (via Docker), or Windows (WSL2)

**Assumed knowledge:** Basic Conda workflow, terminal commands, understanding of your Python dependencies

## Installation & Setup

### Create a Conda Environment Locally

```bash
conda create --name workshop python=3.10 -y
conda activate workshop
python --version
```

You should see `Python 3.10.x`.

### Install Your Core Dependencies

Install the packages your research uses. Here's an example:

```bash
conda install numpy scipy scikit-learn pytorch::pytorch pytorch::torchvision pytorch::torchaudio -c pytorch -y
```

Adjust package names to match your actual requirements.

### Export the Environment Configuration

Once all packages work together, export as YAML:

```bash
conda env export --no-build > workshop.yml
cat workshop.yml
```

This YAML file is your **environment blueprint**—exact package versions so anyone can recreate it identically.

### Create the Apptainer Recipe

Create `workshop.def`:

```bash
nano workshop.def
```

Paste this:

```
Bootstrap: docker
From: continuumio/anaconda3:latest

%files
    workshop.yml /tmp/workshop.yml

%post
    apt-get update && apt-get install -y build-essential
    conda env create --name workshop --file /tmp/workshop.yml
    conda clean --all -y

%environment
    export PATH="/opt/conda/envs/workshop/bin:$PATH"

%runscript
    source activate workshop
    exec "$@"
```

**What each section does:**
- `%files` — Copies your `workshop.yml` into the container
- `%post` — Installs build tools, creates the Conda environment from YAML, cleans up
- `%environment` — Sets PATH so your environment's Python is found first
- `%runscript` — **Activates your Conda environment every time the container runs** (critical!)

> ⚠️ Without `%runscript`, you'll run the base Anaconda environment, which lacks your packages. Always activate your named environment here.

### Build the Apptainer Image

```bash
apptainer build workshop.sif workshop.def
```

This takes 3–5 minutes. Result: `workshop.sif` — a single ~2–3 GB file containing Ubuntu, Anaconda, and your full Python environment.

## Core Workflow

### Test the Container Locally

Verify your environment is inside:

```bash
apptainer exec workshop.sif python --version
apptainer exec workshop.sif python -c "import torch; print(torch.__version__)"
```

### Run a Script Inside the Container

Create a test script:

```bash
cat > test_script.py << 'EOF'
import numpy as np
import torch
print("NumPy version:", np.__version__)
print("PyTorch version:", torch.__version__)
EOF
```

Run it:

```bash
apptainer exec workshop.sif python test_script.py
```

### Create a Sandbox for Modifications

If you need to add packages without rebuilding from scratch, use a **sandbox**—a writable directory version:

```bash
apptainer build --sandbox workshop_sandbox workshop.sif
```

### Enter the Sandbox with Write Permissions

```bash
apptainer shell --writable workshop_sandbox
conda init bash
exit
apptainer shell --writable workshop_sandbox
conda activate workshop
conda install xgboost -y
exit
```

### Rebuild the SIF from the Updated Sandbox

```bash
apptainer build workshop_v2.sif workshop_sandbox
apptainer exec workshop_v2.sif python -c "import xgboost; print(xgboost.__version__)"
```

### Transfer to the Cluster

```bash
scp workshop_v2.sif username@cluster.edu:~/containers/
ssh username@cluster.edu
apptainer exec ~/containers/workshop_v2.sif python /path/to/your/script.py
```

### Run on the Cluster with SLURM

Create `job_script.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=ml_job
#SBATCH --time=01:00:00
#SBATCH --gpus=1

apptainer exec ~/containers/workshop_v2.sif python train_model.py
```

Submit:

```bash
sbatch job_script.sh
```

## Practical Example: ML Pipeline

**Scenario:** Train a PyTorch + scikit-learn model locally, run it on a GPU cluster without reinstalling.

**Step 1: Create and test locally**

```bash
conda create --name ml_pipeline python=3.10 -y
conda activate ml_pipeline
conda install pytorch::pytorch pytorch::torchvision pytorch::torchaudio scikit-learn -c pytorch -y
python -c "import torch; print(torch.cuda.is_available())"
```

**Step 2: Export the environment**

```bash
conda env export --no-build > ml_pipeline.yml
```

**Step 3: Create the recipe**

```bash
cat > ml_pipeline.def << 'EOF'
Bootstrap: docker
From: continuumio/anaconda3:latest

%files
    ml_pipeline.yml /tmp/ml_pipeline.yml

%post
    apt-get update && apt-get install -y build-essential
    conda env create --name ml_pipeline --file /tmp/ml_pipeline.yml
    conda clean --all -y

%environment
    export PATH="/opt/conda/envs/ml_pipeline/bin:$PATH"

%runscript
    source activate ml_pipeline
    exec "$@"
EOF
```

**Step 4: Build and test**

```bash
apptainer build ml_pipeline.sif ml_pipeline.def
apptainer exec ml_pipeline.sif python train_model.py
```

**Step 5: Transfer and run on cluster**

```bash
scp ml_pipeline.sif username@cluster.edu:~/containers/
ssh username@cluster.edu
apptainer exec ~/containers/ml_pipeline.sif python train_model.py
```

Same environment. Same results. No reinstalling.

## Common Issues & Fixes

**"conda activate" doesn't work inside the container**

→ You skipped the `%runscript` section or forgot to activate your environment. Rebuild with the correct recipe.

**"Permission denied" when entering sandbox with `--writable`**

→ Check permissions: `ls -la workshop_sandbox`. Rebuild the sandbox in a location you own.

**Container builds successfully but imports fail at runtime**

→ The package was installed in the base environment, not your named environment. Verify `workshop.yml` includes all dependencies. Rebuild and test locally first.

**SIF file is too large (~5+ GB)**

→ Add `conda clean --all -y` to your recipe's `%post` section. Consider splitting into multiple lighter containers.

## Next Steps

1. **Version your recipes** — Keep `.def` and `.yml` files in Git alongside your code
2. **Document dependencies** — Add comments explaining why each package is needed
3. **Test on the cluster** — Run a small test job before submitting large batches
4. **Share with collaborators** — Send the `.sif` file; they don't need to rebuild anything
5. **Explore advanced features** — Bind mount directories with `--bind`, use GPUs with `--nv`, or customize with environment variables

**The real win?** You've decoupled your code from your compute environment. Your script works the same way on your laptop, your colleague's machine, and a 1000-node cluster.

---

**What's your biggest pain point right now—dependency conflicts, environment setup time, or something else?** Reply and let me know what you're working with.

---

*How do you currently manage Python environments across your lab's machines and clusters? Still debugging version conflicts?*
