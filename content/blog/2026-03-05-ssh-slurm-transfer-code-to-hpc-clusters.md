---
title: 'SSH & SLURM: Transfer Code to HPC Clusters'
date: '2026-03-05'
draft: false
description: 'Learn the three-tool HPC stack: SSH/SCP/Rsync for file transfer, Singularity/Apptainer
  for containerization, and SLURM for job scheduling. This guide walks researchers
  through moving local code to GPU clusters, building reproducible environments, and
  submitting jobs without breaking them.'
subtitle: Master SSH, Singularity/Apptainer & SLURM to move code and run jobs on GPUs—the
  complete HPC workflow for researchers.
image: /img/thumbnails/2026-03-05-ssh-slurm-transfer-code-to-hpc-clusters.svg
tags:
- SSH
- SLURM
- Singularity/Apptainer
- HPC clusters
- GPU computing
- data transfer
- containerization
- rsync
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 9.0
source_transcript: cleaned_transcripts_2026-02-27_12-19-01_Getting_Started_SSH__Data_Transfer_to_HPC_Clusters.md
generated: 2026-03-05_07-32-17
---

## Transfer Code to HPC Clusters Using SSH, Singularity/Apptainer & SLURM

You've written working code on your laptop. Now you need to run it on your institution's HPC cluster with 100+ GPUs—but you're staring at a terminal with no idea how to get your files there, containerize your environment, or submit a job without breaking it.

This is the moment most researchers feel lost.

## The HPC Stack in 90 Seconds

**High-performance computing (HPC) clusters** are shared servers with massive CPU and GPU resources. To use them safely and reproducibly, you need three tools working together:

- **SSH/SCP/Rsync** — Move your code and data from your machine to the cluster
- **Singularity/Apptainer** — Package your Python environment (dependencies, libraries, everything) into a portable container
- **SLURM** — Queue and schedule your jobs so the cluster knows when to run them and on which GPUs

This workflow takes you from local code → containerized environment → cluster submission → job monitoring. The key insight: **Singularity (now Apptainer) is optimized for GPU computing** in ways Docker isn't. That's why HPC clusters prefer it.

## Prerequisites

You'll need:

- **Local machine:** SSH client (built into macOS/Linux; PuTTY or Windows Terminal on Windows)
- **HPC cluster access:** Active account with SSH credentials
- **Apptainer/Singularity:** v1.0+ on the cluster
- **SLURM:** Already installed on your cluster
- **Python 3.7+:** With your code ready locally
- **A Singularity Definition File:** A `.def` file to describe your container

**Verify what's on your cluster:**

```bash
ssh username@cluster.institution.edu
apptainer version
sinfo
```

The `apptainer version` confirms Singularity is installed. The `sinfo` command shows SLURM is running.

## Step 1: Create a Singularity Definition File

On your laptop, create `environment.def` that describes your container:

```
Bootstrap: docker
From: python:3.10-slim

%post
    apt-get update
    apt-get install -y build-essential
    pip install numpy pandas torch torchvision

%environment
    export PYTHONUNBUFFERED=1

%runscript
    exec python "$@"
```

Replace the package list with whatever your code needs. The `%post` section runs installation commands. The `%environment` section sets variables. The `%runscript` defines what happens when you run the container.

## Step 2: Build the Container

```bash
apptainer build my_env.sif environment.def
```

This creates `my_env.sif`—a single file containing your entire environment. On some clusters, you may need to build this *on* the cluster due to permissions. Ask your cluster admin if you hit permission errors.

**Verify it works:**

```bash
apptainer run my_env.sif python --version
```

You should see Python 3.10.

## Step 3: Organize Your Local Code

Create a clean structure:

```
my_project/
├── src/
│   ├── main.py
│   ├── utils.py
│   └── config.yaml
├── data/
│   └── input_data.csv
├── environment.def
├── submit_job.sh
└── logs/
```

Keep code, data, and scripts separate—easier to debug and transfer.

## Step 4: Copy Everything to the Cluster

From your local terminal:

```bash
rsync -avz --progress \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.git' \
  my_project/ username@cluster.institution.edu:/home/username/my_project/
```

The `--exclude` flags skip junk files and speed up transfer. The trailing slash on `my_project/` copies *contents*, not the folder itself.

> **On Windows without Rsync?** Use SCP instead: `scp -r my_project/ username@cluster.institution.edu:/home/username/`

## Step 5: Build the Image on the Cluster

```bash
ssh username@cluster.institution.edu
cd ~/my_project
apptainer build my_env.sif environment.def
```

This takes 2–5 minutes depending on image size.

## Step 6: Create a SLURM Submission Script

Create `submit_job.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=my_analysis
#SBATCH --output=logs/output_%j.log
#SBATCH --error=logs/error_%j.log
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gpus=1
#SBATCH --time=01:00:00
#SBATCH --partition=gpu

cd ~/my_project
apptainer run my_env.sif python src/main.py --config config.yaml
```

Key directives:

- `--gpus=1` — Request 1 GPU (change as needed)
- `--time=01:00:00` — Max runtime (adjust for your job)
- `--partition=gpu` — Use the GPU partition (check with your admin)
- `%j` — Job ID placeholder in log filenames

## Step 7: Submit and Monitor

```bash
sbatch submit_job.sh
```

You'll see a job ID. Check status:

```bash
squeue -u username
```

Watch logs in real time:

```bash
tail -f logs/output_*.log
```

## Practical Example: PyTorch Training

**Scenario:** A PyTorch model training script using 1 GPU for 45 minutes.

`environment.def`:

```
Bootstrap: docker
From: pytorch/pytorch:2.0-cuda11.8-runtime-ubuntu22.04

%post
    pip install scikit-learn matplotlib tensorboard

%environment
    export CUDA_VISIBLE_DEVICES=0
```

`src/train.py`:

```python
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
# ... rest of training code
```

**Transfer and build:**

```bash
rsync -avz --progress my_project/ user@hpc.edu:/home/user/pytorch_train/
ssh user@hpc.edu
cd ~/pytorch_train
apptainer build pytorch.sif environment.def
```

`submit_job.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=pytorch_train
#SBATCH --output=logs/train_%j.log
#SBATCH --gpus=1
#SBATCH --time=01:00:00
#SBATCH --partition=gpu

cd ~/pytorch_train
apptainer run pytorch.sif python src/train.py
```

**Submit and monitor:**

```bash
sbatch submit_job.sh
squeue -u user
tail -f logs/train_*.log
```

Download results when done:

```bash
rsync -avz user@hpc.edu:/home/user/pytorch_train/results/ ./results/
```

## Common Issues & Fixes

**"apptainer: command not found"**

The cluster doesn't have Apptainer in your PATH. Try:

```bash
module avail singularity
module load singularity
apptainer version
```

**"Permission denied" during build**

You lack privileges on the login node. Ask your admin to build the image for you.

**SLURM job stuck in "PENDING"**

The cluster is busy or you requested unavailable resources. Check:

```bash
sinfo
squeue
```

Reduce `--gpus` or `--time` and resubmit.

**"CUDA out of memory"**

Your job uses more GPU memory than available. Reduce batch size in your code or request a different GPU type:

```bash
#SBATCH --gpus=1
#SBATCH --constraint=gpu_type
```

**Files not transferring with Rsync**

Verify SSH connectivity first:

```bash
ssh user@cluster.edu echo "Connected"
```

Check for typos in paths. Use absolute paths if relative paths fail.

## Next Steps

1. **Test locally first.** Build and run your Singularity image on your laptop before transferring.
2. **Start small.** Submit a 10-minute test job before running a 10-hour job.
3. **Monitor and log.** Always redirect output to log files for debugging.
4. **Use SSHFS for file browsing.** Mount your cluster home directory locally:

```bash
mkdir ~/cluster_mount
sshfs user@cluster.edu:/home/user ~/cluster_mount
```

Now you can browse and edit cluster files like a local folder.

---

**What's your biggest bottleneck right now—getting code to the cluster, containerizing your environment, or debugging SLURM jobs?** Reply and let me know.

---

*What's your biggest friction point when submitting jobs to HPC clusters—file transfer, containerization, or SLURM configuration?*
