---
title: 'VS Code Collab Extension: GPU Training in Jupyter'
date: '2026-03-05'
draft: false
description: The VS Code Collab extension connects your local Jupyter notebooks to
  Google Colab's GPU compute, eliminating context-switching between editors. Train
  PyTorch models on T4/TPU directly from VS Code without uploading files or leaving
  your notebook environment.
subtitle: Run ML models on GPU directly from VS Code—no Colab browser tabs, no context
  switching.
image: /img/thumbnails/2026-03-05-vs-code-collab-extension-gpu-training-in-jupyter.svg
tags:
- VS Code Collab
- GPU training
- Jupyter Notebooks
- PyTorch
- Local ML development
- Google Colab integration
- VS Code extensions
- ML researchers
categories:
- hpc
is_series: false
article_type: tutorial
cluster: ⚙️ HPC & Dev Environment
critic_score: 8.2
source_transcript: cleaned_transcripts_2026-02-27_11-52-11_The_new_Vscode_extension_that_allow_you_to_run_cod.md
generated: 2026-03-05_06-54-44
---

## Run Python Code with GPU Inside VS Code — Without Leaving Your Jupyter Notebooks

You've built a machine learning model locally, but your GPU is sitting idle because you're switching between VS Code and Google Colab every time you need accelerated compute. Or worse—you're uploading files, waiting for notebooks to load, and losing your development flow. The **VS Code Collab extension** eliminates that friction: connect to CPU, GPU, or TPU compute directly from your Jupyter notebooks without ever leaving your editor.

## What This Is

The **VS Code Collab extension** bridges Google Colab's compute resources with your local VS Code environment. Instead of opening a browser tab, uploading datasets, and managing separate notebooks, you select a kernel from your local Jupyter file and instantly connect to a remote Colab server. Your code runs on cloud compute, but your workflow stays in VS Code. Perfect for researchers and students who need GPU access without the context-switching tax.

## Prerequisites

- **VS Code** (latest version)
- **Jupyter Notebook extension** for VS Code
- **Python 3.8+** (local environment)
- **Google Account** (to authenticate with Colab)
- **Active internet connection**
- **Notebook files only:** `.ipynb` files (not standalone Python scripts)

> ⚠️ This extension works exclusively with Jupyter Notebook files, not Python scripts.

## Installation & Setup

### Step 1: Install the Extension

Open VS Code and press `Ctrl+Shift+X` / `Cmd+Shift+X` to open Extensions. Search for **VS Code Collab** (published by Google) and click **Install**.

### Step 2: Authenticate with Google

Once installed, VS Code prompts you to sign in. Click **Enable** and complete the OAuth flow in your browser. Return to VS Code—you're authenticated.

### Step 3: Open a Jupyter Notebook

Create or open a `.ipynb` file. You should see a **kernel selector** in the top-right corner of the notebook.

## Core Workflow

### Connect to a Collab Server

1. Click the **kernel selector** (top-right of notebook)
2. Select **Collab** from the dropdown
3. Choose **New Collab server** (or **Auto-connect** if you've used one before)
4. Pick your compute type:
   - **CPU** (free, prototyping)
   - **GPU** (T4, training)
   - **TPU** (large-scale models)
5. Name your server (e.g., `GPU_training_v1`)
6. Select runtime language (**Python 3** recommended)
7. Wait for initialization; your kernel selector will update with the server name

### Test the Connection

Run this cell to verify GPU access:

```python
import torch
print(f"GPU available: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

## Practical Example: Train an ML Model on GPU

### Set Up Your Session

```python
import os
import torch
import torch.nn as nn
import pandas as pd

# Verify GPU
print(f"GPU available: {torch.cuda.is_available()}")
print(f"Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")

# Create output directory
os.makedirs('/content/results', exist_ok=True)
```

### Define and Train a Model

```python
# Simple linear regression model
model = nn.Linear(10, 1)
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Training loop
losses = []
for epoch in range(100):
    x = torch.randn(32, 10, device=device)
    y = torch.randn(32, 1, device=device)
    
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    
    losses.append(loss.item())
    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/100, Loss: {loss.item():.4f}")

print("Training complete!")
```

### Save Results

```python
# Save model
torch.save(model.state_dict(), '/content/results/model_weights.pth')

# Save loss history
loss_df = pd.DataFrame({'epoch': range(len(losses)), 'loss': losses})
loss_df.to_csv('/content/results/training_loss.csv', index=False)

print("Results saved to /content/results/")
```

### Reload Later

```python
# Reconnect to the same server and reload
model = nn.Linear(10, 1).to(device)
model.load_state_dict(torch.load('/content/results/model_weights.pth'))
loss_df = pd.read_csv('/content/results/training_loss.csv')

print("Model loaded successfully!")
```

## Common Issues & Fixes

**"Cannot Create Multiple Servers with Same Device Type"**

Each device type (CPU, GPU, TPU) allows only **one active server**. To create a fresh GPU environment, delete the existing one first. Open the **Command Palette** (`Ctrl+Shift+P`), type `Collab: Remove Server`, and select the server to delete.

> ⚠️ Deleting a server removes all files within that session. Export critical results first.

**"Files Not Found When Switching Servers"**

Each Collab server is an **isolated session**. Files saved in one server's `/content/` directory don't exist in another server's session. Always reconnect to the original server using **Auto-connect** or the kernel dropdown, or download files locally and re-upload to a different server.

**"CUDA Not Available on GPU Server"**

The GPU server may still be initializing. Wait 10–15 seconds and run the cell again. If the issue persists, delete the GPU server and create a new one.

## Next Steps

1. **Scale your training:** Load real datasets (Hugging Face, Kaggle) and train larger models.
2. **Try TPU:** For production-scale work, experiment with the TPU server option.
3. **Automate workflows:** Use the Command Palette to quickly switch between CPU, GPU, and TPU as needed.
4. **Version control:** Download trained models locally and commit them to your repository.

---

**What's your biggest bottleneck right now—switching between editors, waiting for compute allocation, or managing files across environments?** Reply and let me know, and I'll create a follow-up tutorial tailored to your workflow.

---

*What's your current workflow for accessing GPU compute during local development—are you still juggling Colab tabs?*
