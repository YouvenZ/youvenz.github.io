---
title: 'Singularity/Apptainer: Local to Cluster Workflow'
date: '2026-03-05'
draft: false
description: Singularity/Apptainer lets you package your entire development environment
  into a single .sif file, build it locally, and deploy it to HPC clusters without
  root access or dependency conflicts. Learn the pull-build-run workflow with practical
  examples for researchers and ML practitioners working across machines.
subtitle: Build containerized HPC environments locally, deploy to clusters without
  dependency hell
image: /img/thumbnails/2026-03-05-singularityapptainer-local-to-cluster-workflow.svg
tags:
- Singularity
- Apptainer
- HPC Clusters
- Container Workflow
- Docker Alternatives
- Linux Containers
- Development Environment
- Reproducible Research
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 8.5
source_transcript: cleaned_transcripts_2026-02-27_12-17-55_Setting_Up_Your_Development_Environment_Local_to_C.md
generated: 2026-03-05_07-30-39
---

# Pull, Build, and Deploy Singularity Containers from Local Machine to HPC Clusters

You've got terabytes of data on your HPC cluster and a Python script that works on your laptop. But moving it to the cluster means wrestling with dependency conflicts, mysterious `ModuleNotFoundError` messages, and copying massive datasets you don't want to duplicate. You need a way to package your entire development environment—dependencies, libraries, Python versions—and run it anywhere without breaking it. That's where **Singularity/Apptainer** comes in.

## What This Is

**Singularity** (now called **Apptainer**) is a container platform designed specifically for HPC clusters. Unlike Docker, which requires root access and runs as a background service, Singularity creates a single `.sif` file—a portable, frozen Linux environment—that you build locally and deploy to clusters without modification. You'll learn to **pull** pre-built images, **build** custom ones from recipes, and **run** them locally and on clusters using **bind mounts** to access your data without copying it into the container.

The key difference: Singularity doesn't need root access on the cluster, and the entire environment is a single file. You build locally, transfer once, and it works everywhere.

## Prerequisites

**Software & Versions:**
- **Singularity/Apptainer** (v3.8+) or **Apptainer** (v1.0+) installed locally
- **Linux OS**, **WSL2** (Windows Subsystem for Linux), or **macOS with Lima/Colima** for container runtime
- **HPC cluster access** with Singularity/Apptainer pre-installed (confirm with your cluster admin)
- **Basic terminal/shell knowledge** (navigating directories, running commands)
- **Text editor** for writing `.def` (definition) files (nano, vim, VS Code, etc.)

**Dependencies:**
- Cluster must have Singularity/Apptainer in `$PATH`
- Write permissions in your local working directory and cluster home/project directories
- Sufficient disk space for `.sif` files (typically 500 MB–5 GB per image)

> ⚠️ **Note:** Never pull or build images on the cluster itself. Always build locally, then transfer the `.sif` file to the cluster.

## Installation & Setup

### Step 1: Verify Singularity/Apptainer on Your Local Machine

Open your terminal and check if Singularity or Apptainer is installed:

```bash
apptainer --version
```

or

```bash
singularity --version
```

If you see a version number (e.g., `apptainer version 1.1.5`), you're ready. If not, install Apptainer following the [official Apptainer installation guide](https://apptainer.org/docs/admin/main/installation.html) for your OS.

### Step 2: Create a Local Working Directory Structure

Organize your project with separate folders for containers, code, and data:

```bash
mkdir -p ~/singularity-project/{containers,code,data}
cd ~/singularity-project
```

### Step 3: Test Basic Execution

Pull a lightweight image to verify Apptainer works:

```bash
apptainer pull docker://ubuntu:22.04
```

This downloads an Ubuntu 22.04 image from Docker Hub and saves it as `ubuntu_22.04.sif` in your current directory.

Now run a simple command inside the container:

```bash
apptainer exec ubuntu_22.04.sif ls /
```

You should see the root directory listing of the Ubuntu container. If this works, Apptainer is properly installed.

## Core Workflow: Four Essential Commands

Before hands-on work, understand these four commands:

- **`apptainer pull`** — Downloads a pre-built image from a registry (Docker Hub, Singularity Hub, etc.) and saves it as a `.sif` file.
- **`apptainer build`** — Creates a custom `.sif` image from a recipe file (`.def` file).
- **`apptainer run`** — Executes the default command defined in the image's recipe (the `%runscript` section).
- **`apptainer exec`** — Runs any arbitrary command inside the image, overriding the default.

## Hands-On: Building and Testing Locally

### Pull a Pre-Built Image

Pull an image with Python 3.10 pre-installed:

```bash
apptainer pull docker://python:3.10-slim
```

This creates `python_3.10-slim.sif`. The `docker://` prefix tells Apptainer to fetch from Docker Hub.

### Execute a Python Command

Verify Python is available and check its version:

```bash
apptainer exec python_3.10-slim.sif python3 --version
```

Expected output: `Python 3.10.x`

### Create a Custom Definition File

Create `containers/my-env.def`:

```
# my-env.def
Bootstrap: docker
From: python:3.10-slim

%post
    apt-get update
    apt-get install -y \
        git \
        curl \
        build-essential
    pip install --upgrade pip
    pip install numpy pandas scikit-learn

%environment
    export PYTHONUNBUFFERED=1
    export PATH="/usr/local/bin:$PATH"

%runscript
    exec python3 "$@"
```

This recipe starts from Python 3.10, installs system packages and libraries, sets environment variables, and defines a runscript that executes Python by default.

### Build Your Custom Image

```bash
apptainer build my-env.sif containers/my-env.def
```

This creates `my-env.sif` in your current directory. The build process may take 2–5 minutes.

### Test the Built Image

```bash
apptainer exec my-env.sif python3 -c "import numpy; print(numpy.__version__)"
```

Expected output: `1.24.x` (or the installed NumPy version)

### Bind Mount a Data Directory

Create test data:

```bash
mkdir -p data/input
echo -e "sample,value\n1,100\n2,200" > data/input/data.csv
```

Run Python with a bind mount:

```bash
apptainer exec --bind data/input:/mnt/data my-env.sif python3 -c "import pandas; df = pandas.read_csv('/mnt/data/data.csv'); print(df)"
```

The `--bind local/path:/container/path` flag maps your local directory to a path inside the container. The container sees the data without it being copied into the `.sif` file.

### Transfer the Image to Your HPC Cluster

```bash
scp my-env.sif username@cluster.example.com:~/containers/
```

## Practical Example: Running a Machine Learning Script

**Scenario:** You have a Python script that trains a scikit-learn model on a 10 GB dataset stored on your cluster. You want the exact same Python and library versions everywhere.

### Create the Definition File

Save as `ml-pipeline.def`:

```
Bootstrap: docker
From: python:3.10-slim

%post
    apt-get update
    apt-get install -y build-essential
    pip install --upgrade pip
    pip install numpy==1.24.3 pandas==2.0.3 scikit-learn==1.3.0 matplotlib

%environment
    export PYTHONUNBUFFERED=1

%runscript
    exec python3 "$@"
```

### Build Locally

```bash
apptainer build ml-pipeline.sif ml-pipeline.def
```

### Create a Training Script

Save as `code/train.py`:

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Read data from bind-mounted directory
data = pd.read_csv('/mnt/data/dataset.csv')
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save results
score = model.score(X_test, y_test)
print(f"Model accuracy: {score:.4f}")
```

### Test Locally

```bash
apptainer exec --bind data/input:/mnt/data ml-pipeline.sif python3 code/train.py
```

### Transfer and Run on Cluster

Copy the image and script:

```bash
scp ml-pipeline.sif username@cluster.example.com:~/containers/
scp code/train.py username@cluster.example.com:~/code/
```

On the cluster, run the script:

```bash
apptainer exec --bind /cluster/data:/mnt/data ~/containers/ml-pipeline.sif python3 ~/code/train.py
```

The `--bind /cluster/data:/mnt/data` flag maps the cluster's data directory to `/mnt/data/` inside the container. Your script reads from `/mnt/data/` without caring about the actual cluster path.

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `apptainer: command not found` | Install Apptainer following the [official guide](https://apptainer.org/docs/admin/main/installation.html) |
| `FATAL: While making image from oci registry: failed to get checksum` | Check internet connection and verify image name (e.g., `docker://python:3.10-slim`) |
| Container can't access data with `--bind` | Use absolute paths: `--bind /full/local/path:/full/container/path`. Test with `apptainer exec --bind /local/path:/mnt/test my-env.sif ls /mnt/test` |
| Build fails with permission errors | Never build on the cluster. Build locally, then transfer the `.sif` file |
| Packages don't appear in container | Ensure `pip install package-name` is in the `%post` section. Rebuild: `apptainer build --force my-env.sif my-env.def` |

## Next Steps

You now have a reproducible, portable development environment. Here's what to do next:

1. **Customize your definition file** — Add your own packages and Python libraries to match your research environment.
2. **Test locally first** — Always verify your workflow on your local machine before deploying to the cluster.
3. **Use absolute paths** — When binding data directories on the cluster, always use absolute paths (e.g., `/home/username/data`, not `~/data`).
4. **Version your images** — Name your `.sif` files with version numbers (e.g., `ml-pipeline-v1.0.sif`, `ml-pipeline-v1.1.sif`) so you can track which environment produced which results.
5. **Document your recipe** — Keep your `.def` file in version control (Git) alongside your code so collaborators can rebuild your exact environment.

**What's one specific dependency conflict or environment issue you've struggled with in your research? How might containerizing that environment solve it? Reply and let me know.**

---

*How do you currently manage dependencies across your local machine and HPC cluster—and have you tried Singularity yet?*
