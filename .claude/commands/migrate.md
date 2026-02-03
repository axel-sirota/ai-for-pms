---
description: Migrate HF Space app to Colab notebook with share=True (project)
---

Migrate existing HF Space app to Colab workshop notebook: $ARGUMENTS

(Pass the app name, e.g., "rag-playground" or "token-counter")

## Purpose

Corporate firewalls block `*.hf.space` domains. This command creates a Colab notebook that uses `demo.launch(share=True)` to generate `*.gradio.live` URLs (not blocked).

## Pre-Work

1. Verify the app exists at `hf_spaces/$ARGUMENTS/app.py`
2. Read the app.py to understand dependencies and structure
3. Check `notebooks/workshop-apps/` for existing notebooks to get next number

## Migration Steps

### Step 1: Read Source App

```bash
# Read the HF Space app
hf_spaces/$ARGUMENTS/app.py
hf_spaces/$ARGUMENTS/requirements.txt
```

### Step 2: Determine Next Number

Check existing notebooks in `notebooks/workshop-apps/` and use next sequential number (01, 02, 03...).

### Step 3: Create Colab Notebook

Create notebook at: `notebooks/workshop-apps/NN-$ARGUMENTS.ipynb`

**Cell 0: Install Dependencies**

```python
#@title Install Dependencies
%%capture
!pip install gradio [deps-from-requirements.txt] -q
```

**Cell 1: App Code**

```python
#@title App Code
import gradio as gr
# ... paste FULL contents of app.py ...
# IMPORTANT: Remove or comment out the final demo.launch() line
```

**Cell 2: Launch with Share**

```python
#@title Launch App - Copy the gradio.live URL below
demo.launch(share=True)
```

### Step 4: Update Migration Tracking

Update `plans/migration/NN-$ARGUMENTS.md` to note notebook was created.

## NotebookEdit Usage

```python
# First cell (install)
NotebookEdit(
    notebook_path="notebooks/workshop-apps/NN-app-name.ipynb",
    edit_mode="insert",
    cell_type="code",
    new_source="#@title Install Dependencies\n%%capture\n!pip install gradio [deps] -q"
)

# Second cell (app code) - use cell_id from previous
NotebookEdit(
    notebook_path="notebooks/workshop-apps/NN-app-name.ipynb",
    edit_mode="insert",
    cell_id="<previous-cell-id>",
    cell_type="code",
    new_source="#@title App Code\nimport gradio as gr\n# ... full app code ..."
)

# Third cell (launch) - use cell_id from previous
NotebookEdit(
    notebook_path="notebooks/workshop-apps/NN-app-name.ipynb",
    edit_mode="insert",
    cell_id="<previous-cell-id>",
    cell_type="code",
    new_source="#@title Launch App - Copy the gradio.live URL\ndemo.launch(share=True)"
)
```

## Checklist

- [ ] Read source `hf_spaces/$ARGUMENTS/app.py`
- [ ] Read source `hf_spaces/$ARGUMENTS/requirements.txt`
- [ ] Determined next notebook number
- [ ] Created notebook at `notebooks/workshop-apps/NN-$ARGUMENTS.ipynb`
- [ ] Cell 0: Install with correct dependencies
- [ ] Cell 1: Full app code (without final `demo.launch()`)
- [ ] Cell 2: `demo.launch(share=True)`
- [ ] Notebook runs in Colab and produces `*.gradio.live` URL

## Batch Migration

To migrate all apps at once:

```
/migrate ai-paradigm-picker
/migrate build-vs-buy-calculator
/migrate model-comparison-arena
... etc
```

Or list all apps:

```bash
ls hf_spaces/
```
