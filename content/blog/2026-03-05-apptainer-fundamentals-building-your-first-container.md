---
title: 'Apptainer Fundamentals: Building Your First Container'
date: '2026-03-05'
draft: false
description: Learn how to build and deploy Apptainer containers on HPC clusters without
  Docker. This practical guide walks researchers through definition files, image building,
  and binding host directories—from first principles to production-ready workflows.
subtitle: Master containerization for HPC clusters without Docker—step-by-step guide
  for researchers.
image: /img/thumbnails/2026-03-05-apptainer-fundamentals-building-your-first-container.svg
tags:
- Apptainer
- Singularity
- HPC containers
- Container building
- Linux containerization
- SLURM workflows
- Reproducible research
- Container deployment
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 5.5
source_transcript: cleaned_transcripts_2026-02-27_12-16-22_Apptainer_Fundamentals_Building_Your_First_Contain.md
generated: 2026-03-05_07-28-50
---

# Build Your First Apptainer Container Without Docker — A Practical Guide for HPC Researchers

You've got HPC cluster access, but containerizing your workflow feels like a black box. **Singularity (now Apptainer) promises reproducibility and portability**, but the documentation jumps between concepts, and you're not sure where to start. You don't want to learn Docker first—you just want a working container on your cluster *today*.

Here's the good news: **Apptainer is simpler than you think, and you don't need Docker to get started.**

## What Apptainer Is (and Why It Matters for HPC)

**Apptainer** (formerly Singularity) is a container runtime purpose-built for HPC environments. Unlike Docker, it doesn't require root privileges to *run*, integrates seamlessly with job schedulers (SLURM, PBS), and runs on shared clusters without security headaches.

Think of an **Apptainer definition file** as a recipe card: it lists your base OS, dependencies, environment variables, and the default command your container should run. Apptainer converts that recipe into a single `.sif` file (Singularity Image Format)—a portable, versioned artifact you can move anywhere.

## Prerequisites

Before you start, you'll need:

- **Apptainer installed** (v1.0 or later; check with `apptainer --version`)
- **Linux system** or WSL2 (macOS users: use a Linux VM or remote cluster)
- **Sudo or fakeroot access** (for local builds)
- **~2 GB disk space** for container images
- **Basic Linux shell familiarity** (cd, ls, echo)

## Installation & Setup

### Verify Apptainer Installation

Check if Apptainer is available:

```bash
apptainer --version
```

Expected output: `apptainer version 1.0.0` (or later)

### Install Apptainer (if needed)

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install -y apptainer
```

**CentOS/RHEL:**

```bash
sudo yum install -y apptainer
```

### Create a Working Directory

```bash
mkdir -p ~/apptainer-project
cd ~/apptainer-project
```

## Your First Container: Step by Step

### Step 1: Write a Definition File

Create `my-container.def`:

```bash
nano my-container.def
```

Paste this template:

```
Bootstrap: docker
From: ubuntu:22.04

%post
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install numpy scipy

%environment
    export PATH=/usr/local/bin:$PATH
    export LANG=C.UTF-8

%runscript
    python3 "$@"

%labels
    Author YourName
    Version 1.0
```

**Section breakdown:**

- **Bootstrap & From:** Base OS image source (Docker Hub, local file, or registry)
- **%post:** Commands run during build (equivalent to RUN in Docker)
- **%environment:** Variables set when the container runs
- **%runscript:** Default command executed with `apptainer run`
- **%labels:** Metadata tags for documentation

Save and exit (Ctrl+X → Y → Enter).

### Step 2: Build the Container Image

Convert the definition file into a runnable `.sif` file:

```bash
sudo apptainer build my-container.sif my-container.def
```

**What happens:**

- Apptainer downloads the base Ubuntu image
- Runs all `%post` commands sequentially
- Creates `my-container.sif` (a single, portable file)
- Process takes 2–5 minutes depending on package size

Expected output:

```
INFO:    Starting build...
INFO:    Downloading docker image...
INFO:    Building from docker image...
INFO:    Running post scriptlet...
INFO:    Creating SIF file...
INFO:    Build complete: my-container.sif
```

### Step 3: Test the Container

Run a command inside the container:

```bash
apptainer exec my-container.sif python3 --version
```

Expected output:

```
Python 3.10.6
```

The `exec` command lets you run any command inside the container without triggering `%runscript`.

### Step 4: Execute the Runscript

Call the default command defined in `%runscript`:

```bash
apptainer run my-container.sif -c "import numpy; print(numpy.__version__)"
```

Expected output:

```
1.21.0
```

### Step 5: Bind Host Directories

Mount a folder from your host system into the container:

```bash
apptainer exec --bind /home/user/data:/data my-container.sif ls /data
```

This maps `/home/user/data` (host) → `/data` (container). Essential for accessing input files and writing results without copying data into the image.

## Real-World Example: Python Analysis Pipeline

**Scenario:** Run a Python analysis script on an HPC cluster with pinned dependencies, bypassing the cluster's outdated Python environment.

### Definition File (analysis.def):

```
Bootstrap: docker
From: python:3.11-slim

%post
    apt-get update
    apt-get install -y gcc gfortran
    pip install numpy scipy matplotlib pandas

%files
    analysis.py /opt/

%environment
    export PYTHONUNBUFFERED=1

%runscript
    cd /opt
    python3 analysis.py "$@"

%labels
    Purpose DataAnalysis
    Version 1.0
```

The `%files` section copies your local `analysis.py` into the container at build time.

### Build:

```bash
sudo apptainer build analysis.sif analysis.def
```

### SLURM Job Script:

```bash
#!/bin/bash
#SBATCH --job-name=analysis
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4

apptainer run --bind /scratch/user/input:/input analysis.sif --input-file /input/data.csv
```

**Result:** Your script runs with pinned NumPy, SciPy, and Matplotlib versions, regardless of what's installed on the cluster. Reproducibility guaranteed.

## Common Issues & Fixes

### "Permission Denied" During Build

**Fix:** Use fakeroot mode (works without root, but with limitations):

```bash
apptainer build --fakeroot my-container.sif my-container.def
```

For full functionality, request sudo access from your cluster admin.

### "Failed to Download Docker Image"

**Verify the image exists:**

```bash
apptainer pull docker://ubuntu:22.04
```

If network access is restricted, use a local base image:

```
Bootstrap: localimage
From: /path/to/existing/base.sif
```

### Bind Mount Not Working

**Check the host path exists:**

```bash
ls -la /home/user/data
```

**Ensure the container path is writable** (add to `%post` if needed):

```bash
mkdir -p /data && chmod 777 /data
```

### "Image Not Found" When Running

```bash
ls -lh *.sif
apptainer run ~/apptainer-project/my-container.sif
```

Always use the full path if you're in a different directory.

## Next Steps

1. **Version your definition file:** Commit `my-container.def` to Git.
2. **Test on the actual cluster:** Copy your `.sif` and run it in a real job.
3. **Explore advanced sections:** Learn about `%setup`, `%test`, and multi-stage builds.
4. **Share your image:** Push to a registry (Sylabs Cloud, Docker Hub, or local repo).

---

**What's your use case?** Are you containerizing a legacy application, pinning Python dependencies, or running compiled code? Reply and let me know—I'd love to hear what you're building.

---

*What's your go-to base image for containerizing scientific workflows—and have you hit any Apptainer gotchas we should know about?*
