---
title: 'Run Multiple Jobs with SLURM Array: The Right Way'
date: '2026-03-05'
draft: false
description: Learn how to eliminate manual job script duplication by using SLURM array
  jobs with CSV parameter files. This guide shows researchers and ML practitioners
  how to scale from dozens to hundreds of experiments automatically while maintaining
  full reproducibility and tracking.
subtitle: Scale HPC experiments from 50 to 500 runs without manual duplication using
  SLURM arrays and CSV parameters.
image: /img/thumbnails/2026-03-05-run-multiple-jobs-with-slurm-array-the-right-way.svg
tags:
- SLURM array jobs
- HPC cluster computing
- parameter sweeps
- job scheduling
- reproducible ML workflows
- experiment automation
- batch processing
- cluster management
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 8.5
source_transcript: cleaned_transcripts_2026-02-27_12-11-40_How_to_Run_Multiple_Jobs_with_SLURM_Array_The_Righ.md
generated: 2026-03-05_07-21-58
---

# Run Multiple Job Variations with SLURM Array Jobs — Without Manual Code Duplication

You've written a solid experiment script. Now you need to run it 50 times with different parameters—learning rates, batch sizes, model architectures—across your HPC cluster.

The tempting shortcut: copy-paste your job script 50 times, manually edit each one, submit them all.

The reality: you'll waste hours managing parameter files, lose track of which job used which settings, and have no way to scale this to 500 experiments.

**The pain point:** Without a structured system, scaling experiments on SLURM becomes a manual nightmare that breaks reproducibility.

## What SLURM Array Jobs Actually Do

**SLURM array jobs** let you submit a single job definition that spawns multiple copies—one per parameter set. By combining SLURM arrays with a CSV parameter file and argument parsing, you can run dozens of experiment variations automatically, track exactly what each job ran, and scale to hundreds of experiments without touching your submission script again.

This is the backbone of serious HPC research workflows. Instead of managing 50 separate shell scripts, you manage one job submission and one CSV file. SLURM handles the scheduling, and your Python script reads its parameters from the CSV using the task array ID as the row index.

## Prerequisites

**Software & versions:**
- SLURM (any recent version; verify with `sinfo` on your cluster)
- Python 3.6+ (with `argparse`, `pandas` built-in)
- A text editor or IDE with remote access (VS Code + SSHFS, PyCharm, etc.)
- Singularity or Apptainer (optional but recommended for reproducible environments)

**Cluster access:**
- SSH login to your HPC cluster
- Write permissions in your scratch/work directory
- Familiarity with `sbatch` and basic SLURM commands

## Setup: Mount Your Cluster Locally

Working directly on the cluster via SSH is slow. **SSHFS** lets you mount your cluster's home directory as a local folder, so you can edit files in VS Code and see changes instantly.

**On Linux:**

```bash
sudo apt install sshfs
mkdir ~/cluster-mount
sudo sshfs -o allow_other username@cluster.edu:/home/username ~/cluster-mount
```

Now your cluster's home directory appears in `~/cluster-mount`. Files sync instantly when you edit them locally.

**On macOS:**

```bash
brew install macfuse
brew install sshfs
mkdir ~/cluster-mount
sshfs username@cluster.edu:/home/username ~/cluster-mount
```

**Verify SLURM is available:**

```bash
ssh username@cluster.edu
sinfo
```

You should see a list of partitions and node availability. If you see `PARTITION AVAIL TIMELIMIT NODES STATE`, you're good.

**Create your project structure:**

```bash
mkdir -p ~/slurm-experiments/{scripts,data,logs}
cd ~/slurm-experiments
```

## Step 1: Write Your Experiment Script with Argument Parsing

Your experiment script needs two things: standard parameters (learning rate, batch size, etc.) and two SLURM-specific arguments that link it to the CSV file.

Create `experiment.py`:

```python
import argparse
import pandas as pd
from argparse import Namespace

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=0.001)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--model_type', type=str, default='resnet50')
    # SLURM-specific arguments
    parser.add_argument('--slurm_id', type=int, default=-1)
    parser.add_argument('--params_csv', type=str, default=None)
    return parser

def load_params_from_csv(csv_path, task_id):
    """Load the task_id-th row from CSV and return as argparse Namespace."""
    df = pd.read_csv(csv_path)
    row = df.iloc[task_id].to_dict()
    return Namespace(**row)

def main(args):
    # Your experiment code here
    print(f"Running with LR={args.learning_rate}, BS={args.batch_size}, Model={args.model_type}")
    # Train model, log results, save checkpoints, etc.
    pass

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    
    # If SLURM array task ID is set, load parameters from CSV
    if args.slurm_id != -1 and args.params_csv:
        args = load_params_from_csv(args.params_csv, args.slurm_id)
    
    main(args)
```

**How it works:**
- When you run locally: `python experiment.py --learning_rate 0.01`, it uses your command-line values.
- When SLURM runs it: it passes `--slurm_id=5 --params_csv=params.csv`, and the script loads row 5 from the CSV instead.

## Step 2: Generate Your Parameter Grid

Instead of manually writing 50 parameter combinations, generate them programmatically.

Create `generate_params.py`:

```python
import pandas as pd
from itertools import product

# Define parameter ranges
learning_rates = [0.0001, 0.001, 0.01]
batch_sizes = [16, 32, 64]
model_types = ['resnet50', 'vit_base']

# Create all combinations
param_combinations = list(product(learning_rates, batch_sizes, model_types))

# Convert to DataFrame
data = []
for lr, bs, mt in param_combinations:
    data.append({
        'learning_rate': lr,
        'batch_size': bs,
        'model_type': mt,
        'epochs': 10
    })

df = pd.DataFrame(data)
df.to_csv('params.csv', index=False)
print(f"Generated {len(df)} parameter combinations in params.csv")
```

Run it locally:

```bash
python generate_params.py
```

Inspect the output:

```bash
head -5 params.csv
```

```
learning_rate,batch_size,model_type,epochs
0.0001,16,resnet50,10
0.0001,16,vit_base,10
0.0001,32,resnet50,10
```

This generates 18 parameter combinations (3 × 3 × 2). You now have a **single source of truth** for what each job will run.

## Step 3: Create the SLURM Submission Script

This is the key file that tells SLURM to spawn multiple jobs and pass the array task ID to your Python script.

Create `submit_array.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=experiment_array
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --array=0-17%5
#SBATCH --time=01:00:00
#SBATCH --partition=gpu
#SBATCH --gpus=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G

# Load environment (adjust for your cluster)
module load python/3.10
module load cuda/11.8

# Run experiment with SLURM task array ID
python experiment.py \
    --slurm_id=$SLURM_ARRAY_TASK_ID \
    --params_csv=params.csv
```

**Key SLURM directives:**
- `--array=0-17%5`: Run 18 jobs (indices 0–17), but no more than 5 in parallel.
- `%x_%A_%a`: Log file naming—job name, array job ID, and task index.
- `$SLURM_ARRAY_TASK_ID`: Environment variable SLURM sets for each task (0, 1, 2, ..., 17).

> **Note:** Adjust `--partition`, `--gpus`, `--mem`, and `module load` commands to match your cluster's configuration. Ask your HPC admin or check `module avail`.

## Step 4: Submit and Monitor

```bash
sbatch submit_array.sh
```

Check the status:

```bash
squeue -u $USER
```

You should see:

```
JOBID PARTITION NAME USER ST TIME NODES CPUS NODELIST
12345_0 gpu experiment_array yourname R 0:05 1 4 node-01
12345_1 gpu experiment_array yourname R 0:05 1 4 node-02
12345_2 gpu experiment_array yourname R 0:03 1 4 node-03
12345_3 gpu experiment_array yourname PD 0:00 1 4 (None)
12345_4 gpu experiment_array yourname PD 0:00 1 4 (None)
```

The `_0`, `_1`, etc. are your array tasks. `R` = running, `PD` = pending.

Cancel all tasks if needed:

```bash
scancel 12345
```

## Real Example: Tuning a PyTorch Classifier

You're tuning an image classifier. You want to test 3 learning rates × 3 batch sizes × 2 architectures = **18 experiments**.

**Generate the grid:**

```bash
python generate_params.py
```

Verify the output:

```bash
wc -l params.csv
# 19 (header + 18 rows)
```

**Update `submit_array.sh` to match:**

```bash
#SBATCH --array=0-17%5
```

**Submit:**

```bash
sbatch submit_array.sh
```

SLURM spawns 18 parallel jobs. Each task:
1. Reads its task ID (0–17) from `$SLURM_ARRAY_TASK_ID`
2. Loads the corresponding row from `params.csv`
3. Runs your experiment with those parameters
4. Logs output to `logs/experiment_array_JOBID_TASKID.out`

**Monitor in real-time:**

```bash
watch squeue -u $USER
```

**Collect results after completion:**

```bash
ls logs/
# experiment_array_12345_0.out
# experiment_array_12345_1.out
# ... (18 files total)
```

## Troubleshooting

### "Invalid task ID" or job fails immediately

**Cause:** Your CSV has fewer rows than the array size.

**Fix:** Regenerate `params.csv` to match your `--array` directive:

```bash
python generate_params.py
# Verify row count matches --array=0-N
wc -l params.csv
```

### Jobs stay in "PD" (pending) forever

**Cause:** Your cluster is busy or you've hit a resource limit.

**Fix:** Lower the concurrency limit in `--array=0-17%2` (from `%5` to `%2`), or reduce `--mem` or `--gpus`.

### "ModuleNotFoundError: No module named pandas"

**Cause:** Your Python environment doesn't have `pandas` installed.

**Fix:** Install it in your cluster's Python, or use a Singularity container:

```bash
# In submit_array.sh, replace the python line with:
singularity exec /path/to/container.sif python experiment.py \
    --slurm_id=$SLURM_ARRAY_TASK_ID \
    --params_csv=params.csv
```

### Log files are huge or unreadable

**Cause:** Your code is printing too much (e.g., full model summaries).

**Fix:** Use structured logging instead:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Starting training with LR={args.learning_rate}")
```

## Level Up: Aggregating Results

After all jobs finish, compile your results into a single table:

```python
import glob
import re
import pandas as pd

results = []
for log_file in glob.glob("logs/*.out"):
    # Parse task ID from filename
    match = re.search(r'_(\d+)\.out$', log_file)
    if match:
        task_id = int(match.group(1))
        # Read log, extract metrics (e.g., final accuracy)
        with open(log_file) as f:
            content = f.read()
            # Parse your custom metrics here
        results.append({'task_id': task_id, 'accuracy': 0.95})

results_df = pd.merge(pd.read_csv('params.csv'), pd.DataFrame(results), left_index=True, right_on='task_id')
results_df.to_csv('results.csv', index=False)
print(results_df.sort_values('accuracy', ascending=False).head(10))
```

## What's Next

1. **Add result aggregation:** Compile all output logs into a results table automatically.
2. **Use Singularity containers:** Pin all dependencies for true reproducibility.
3. **Implement adaptive search:** Use Optuna to generate smarter parameter combinations based on previous results.
4. **Set up monitoring:** Track experiments in real-time with Weights & Biases or MLflow.
5. **Scale to thousands:** Increase array size to 500+ and adjust concurrency as needed.

---

**What kind of experiments are you planning to run? Are you tuning a deep learning model, running simulations, or something else entirely?** Reply and let me know—I'd love to help you optimize your SLURM workflow for your specific use case.

---

*What's your current workflow for managing parameter sweeps across your HPC cluster—and how many experiment variations do you typically run?*
