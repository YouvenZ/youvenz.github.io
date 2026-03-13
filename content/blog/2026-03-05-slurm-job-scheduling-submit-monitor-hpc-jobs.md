---
title: 'SLURM Job Scheduling: Submit & Monitor HPC Jobs'
date: '2026-03-05'
draft: false
description: SLURM powers 60% of the world's HPC clusters, but cryptic path errors
  and resource misconfiguration trip up most researchers. Learn the exact patterns
  for writing single-CPU, parallel array, and GPU job scripts—plus how to interpret
  logs and debug common failures.
subtitle: Master SLURM batch scripts, resource allocation, and HPC debugging without
  losing files to path errors.
image: /img/thumbnails/2026-03-05-slurm-job-scheduling-submit-monitor-hpc-jobs.svg
tags:
- SLURM
- HPC job scheduling
- batch scripts
- resource management
- sbatch
- GPU computing
- cluster computing
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 7.0
source_transcript: cleaned_transcripts_2026-02-27_12-14-15_Slurm_Essentials_Job_Scheduling__Resource_Manageme.md
generated: 2026-03-05_07-25-34
---

# Submit & Monitor HPC Jobs Using SLURM — Without Losing Your Data to Path Errors

You've just logged into your university's HPC cluster for the first time. You write what you think is a perfect job script, submit it with `sbatch`, and 10 minutes later you find a cryptic error in the log file: "file does not exist." Your absolute path was wrong. Or you forgot to specify GPU resources and your job waited in the queue for 3 hours doing nothing.

**This is the moment most researchers abandon SLURM and go back to running jobs on their laptop.**

The good news: SLURM job submission is learnable in one sitting—if you know the exact patterns to follow and the gotchas to avoid.

## What SLURM Actually Does

**SLURM** (Simple Linux Utility for Resource Management) powers 60% of the world's HPC clusters. Instead of running code directly on shared hardware, you write a batch script that tells SLURM:

- How many CPUs or GPUs you need
- How much memory and wall-clock time
- Which compute partition (CPU-only, GPU, high-memory, etc.)
- What command to run

SLURM queues your job and runs it when resources are available. You get structured logs, job IDs, and the ability to submit 100 jobs without crashing anything.

In this guide, you'll write three working scripts—a single-CPU job, a parallel CPU array, and a GPU job—then interpret the output logs to debug the most common errors.

## Prerequisites

### Access & Software

- SSH access to an HPC cluster with SLURM installed
- A text editor on the cluster (nano, vim, or VS Code remote SSH)
- Bash shell (default on Linux/Mac; use WSL2 on Windows)

### Cluster Info You Need to Gather

Before writing your first script, get this from your cluster admin or documentation:

- Available partition names (e.g., `cpu`, `gpu`, `high-mem`) — run `sinfo` to list them
- CPU/GPU node specs (cores per node, GPU type, memory) — run `sinfo -N -l`
- Max job duration allowed per partition
- GPU types available (e.g., A100 40GB, RTX 3090 24GB)

A small dataset or script you've already tested locally (to avoid debugging SLURM + code bugs at once) is also helpful.

## Setup in 4 Commands

SLURM is already installed on your cluster. Just set up your working directory:

```bash
ssh username@cluster.university.edu
mkdir -p ~/hpc_workshop/{scripts,logs,data}
cd ~/hpc_workshop
which sbatch && sinfo
```

The last command verifies SLURM is available and shows you which partitions you can access.

> ⚠️ **Critical rule:** Always use absolute paths in SLURM scripts. Relative paths are the #1 cause of "file does not exist" errors.

## The Standard Workflow

Every SLURM job follows this cycle:

1. Write a batch script (`.sh` file with SLURM directives + code)
2. Submit it with `sbatch`
3. Check status with `squeue`
4. Read the output/error logs
5. Debug and resubmit

Let's build three examples that cover 90% of real-world use cases.

## Example 1: Single CPU Job

Create `job_single_cpu.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=cpu_demo
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=logs/cpu_demo_%j.out
#SBATCH --error=logs/cpu_demo_%j.err

python scripts/my_analysis.py
```

**What each directive does:**

- `--job-name`: Human-readable label (appears in `squeue`)
- `--partition`: Which compute nodes to use (ask your admin for names)
- `--ntasks`: Number of parallel tasks (usually 1 for single jobs)
- `--cpus-per-task`: CPU cores per task (increase for multithreading)
- `--mem`: Total RAM allocated (4G, 16G, 64G, etc.)
- `--time`: Max runtime in HH:MM:SS (job terminates if exceeded)
- `--output` / `--error`: Log file paths (`%j` = job ID, `%a` = array index)

### Submit and Monitor

```bash
sbatch job_single_cpu.sh
```

SLURM responds with your job ID:

```
Submitted batch job 12345
```

Check status:

```bash
squeue -u $USER
```

Watch in real-time (updates every 2 seconds):

```bash
watch -n 2 squeue -u $USER
```

Key columns: `JOBID` (your job number), `ST` (status: R = running, PD = pending, CA = cancelled, F = failed), `TIME` (elapsed time), `NODES` (which compute node).

### Read the Logs

Once the job finishes:

```bash
cat logs/cpu_demo_12345.out    # Standard output
cat logs/cpu_demo_12345.err    # Errors and warnings
```

If you see "file does not exist," verify all paths are absolute (start with `/`):

```bash
pwd  # Print working directory
ls -lh /absolute/path/to/file
```

## Example 2: CPU Array Job (Parallel Runs)

To run the same script 5 times with different inputs, use `--array`:

```bash
#!/bin/bash
#SBATCH --job-name=cpu_array_demo
#SBATCH --partition=cpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --array=0-4
#SBATCH --output=logs/cpu_array_%j_%a.out
#SBATCH --error=logs/cpu_array_%j_%a.err

python scripts/my_analysis.py --task_id $SLURM_ARRAY_TASK_ID
```

Submit once; SLURM launches 5 parallel instances:

```bash
sbatch job_cpu_array.sh
```

Each instance gets a unique array index (`%a`) in the log filename, so logs don't overwrite each other.

### Run in Batches

To limit concurrent jobs (e.g., only 2 running at once):

```bash
#SBATCH --array=0-19%2
```

This runs jobs 0–19 with a max of 2 simultaneously. Once 2 finish, the next 2 start.

## Example 3: GPU Job

```bash
#!/bin/bash
#SBATCH --job-name=gpu_demo
#SBATCH --partition=gpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH --output=logs/gpu_demo_%j.out
#SBATCH --error=logs/gpu_demo_%j.err

python scripts/my_gpu_script.py
```

**Key differences from CPU jobs:**

- `--partition=gpu`: Use a GPU partition (not `cpu`)
- `--gres=gpu:1`: Request 1 GPU (`gres` = generic resources)
- `--cpus-per-task=4`: CPU cores to support GPU (typically 4–8)
- `--mem=16G`: Increase memory for GPU workloads

### Request Specific GPU Types

If your cluster has multiple GPU types (A100 40GB, RTX 3090 24GB, etc.), specify which you want:

```bash
#SBATCH --gres=gpu:a100:1
```

Or allow any GPU:

```bash
#SBATCH --gres=gpu:1
```

## Common Issues & Fixes

### "File Does Not Exist"

**Cause:** You used a relative path (e.g., `data/myfile.csv`) instead of an absolute path.

**Fix:** Always use absolute paths. Verify with:

```bash
pwd
ls -lh /absolute/path/to/file
```

### Job Stays in "PD" (Pending) for Hours

**Cause:** You requested more resources than available, or the partition is overloaded.

**Fix:** Check available resources:

```bash
sinfo -N -l
```

Reduce `--mem`, `--cpus-per-task`, or `--time`. Or switch partitions.

### GPU Job Fails with "GPU Not Found"

**Cause:** Missing `--gres=gpu:1` or wrong partition.

**Fix:** Add `--gres=gpu:1` and ensure `--partition=gpu`.

### Job Killed After Timeout

**Cause:** `--time` limit was too short.

**Fix:** Increase `--time`. Start generous and reduce after seeing actual runtime in logs.

## Next Steps

1. **Submit your first single-CPU job** with a simple test (e.g., `python -c "print('Hello from HPC')"`)
2. **Create an array job** that runs 5 instances and logs results
3. **Request GPU resources** and verify CUDA is accessible
4. **Use `watch -n 2 squeue -u $USER`** to see jobs launch and complete in real-time
5. **Name jobs meaningfully** — `job_lr0.001_batch32` beats `job_1` when you're running 100 experiments

---

**What's your first SLURM job going to be—a quick CPU test, or do you have a GPU model ready to train? Reply and let me know.**

---

*What's the most frustrating SLURM error you've hit, and how did you finally debug it?*
