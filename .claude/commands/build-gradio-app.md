---
description: Build a Gradio app for HF Spaces deployment (project)
---

Build Gradio app: $ARGUMENTS

(Pass the app name, e.g., "rag-playground" or "cost-calculator")

## Pre-Work: MANDATORY Reading

**READ THESE FILES BEFORE DOING ANYTHING:**

1. **CLAUDE.md** - Content philosophy, tech stack
2. **GUIDELINES.md** - Gradio app specs, HF Spaces file layout
3. **initial_research/ai-pm-course-full-interactive-architecture.md** - **DEFINITIVE SPEC** (app specifications, this wins when in doubt)
4. **initial_research/ai-pm-course-section4-tdd-research-interactive.md** - Detailed specs (if Section 4 app)
5. **Existing apps** in hf_spaces/ (for consistency)

## Plan the App

**IN CHAT, SHOW ME YOUR PLAN:**

1. App name and purpose
2. Which section it belongs to
3. What PM concept it teaches
4. Input components (sliders, dropdowns, text boxes - list each with ranges/options)
5. Output components (plots, text, tables - describe each)
6. Layout structure (tabs, accordions, rows, columns)
7. API keys needed (if any - will use HF Secrets)
8. Dependencies beyond gradio

**DO NOT PROCEED until I approve this plan.**

## HF Spaces File Structure

Every app gets this structure:

```
hf_spaces/app-name/
    README.md           # HF Spaces metadata
    app.py              # Main Gradio application
    requirements.txt    # App-specific deps (NOT gradio itself)
```

### README.md Template

```yaml
---
title: App Display Name
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
license: mit
---
```

### app.py Structure

```python
import gradio as gr
import os

# API keys from HF Secrets (never hardcoded)
# API_KEY = os.environ.get("OPENAI_API_KEY")

def main_function(input1, input2):
    """Core logic - PM-friendly outputs only."""
    # ... processing ...
    return output

# Build the interface
with gr.Blocks(title="App Name", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# App Title")
    gr.Markdown("Brief PM-friendly description")

    with gr.Tab("Main"):
        # Input components
        with gr.Row():
            slider1 = gr.Slider(...)
            dropdown1 = gr.Dropdown(...)

        # Output components
        output_plot = gr.Plot(label="Results")
        output_text = gr.Textbox(label="PM Insight")

        # Button to trigger
        btn = gr.Button("Analyze", variant="primary")
        btn.click(fn=main_function, inputs=[...], outputs=[...])

    with gr.Tab("How to Read This"):
        gr.Markdown("Explanation for PMs on how to interpret results")

if __name__ == "__main__":
    demo.launch()
```

## Design Principles

### For PMs, Not Engineers
- Labels use business language ("Monthly Cost" not "token_count * price_per_token")
- Outputs include PM insights ("This means your project will..." not raw numbers)
- Include a "How to Read This" tab explaining what the output means
- Error messages are friendly ("Try a different combination" not stack traces)
- **No em dashes** - use regular dashes `-` instead of `&mdash;` or em dash characters

### Gradio Component Selection
- **gr.Slider()** - For numeric ranges (cost, percentage, count)
- **gr.Dropdown()** - For categorical choices (model selection, approach)
- **gr.Radio()** - For binary/few choices (yes/no, small set)
- **gr.Textbox()** - For free text input (prompts, queries)
- **gr.Plot()** - For plotly figures
- **gr.Dataframe()** - For comparison tables
- **gr.Markdown()** - For dynamic text outputs and insights

### Layout Patterns
- Use `gr.Blocks()` (never `gr.Interface()` for complex apps)
- Use `gr.Tab()` to separate concerns (Main, Settings, Help)
- Use `gr.Accordion()` for advanced options PMs can optionally explore
- Use `gr.Row()` and `gr.Column(scale=N)` for side-by-side layouts
- Use `theme=gr.themes.Soft()` for a professional, non-intimidating look

### API Key Handling
- NEVER hardcode keys in app.py
- Access via: `os.environ.get("KEY_NAME")`
- Document required secrets in README.md
- Provide fallback/mock data when keys are missing:
  ```python
  if not API_KEY:
      gr.Warning("API key not configured. Showing demo data.")
      return mock_response()
  ```

### Performance
- All apps must work on free CPU tier (no GPU)
- Cache expensive computations with `@gr.cache`
- Keep response times under 5 seconds for interactive elements
- Use sample/mock data for demos that would otherwise need large models

## File Locations

**HF Space app:**
Save to: `hf_spaces/app-name/` (README.md, app.py, requirements.txt)

**Colab workshop notebook:**
Save to: `notebooks/workshop-apps/NN-app-name.ipynb`

Use sequential number (01, 02, 03...) based on existing files in `notebooks/workshop-apps/`.

---

## MANDATORY: Create Colab Workshop Notebook

**Corporate firewalls block `*.hf.space`.** Create a Colab notebook that uses `share=True` to generate `*.gradio.live` URLs.

### Notebook Structure (3 cells)

**Cell 1: Install Dependencies**
```python
#@title Install Dependencies
%%capture
!pip install gradio [other-deps] -q
```

**Cell 2: App Code**
```python
#@title App Code (Run this cell)
import gradio as gr
# ... EXACT SAME CODE as hf_spaces/app-name/app.py ...
# BUT change the launch line at the end
```

**Cell 3: Launch with Share**
```python
#@title Launch App (Copy the gradio.live URL)
demo.launch(share=True)
```

### Key Differences from HF Space Version

1. `demo.launch()` becomes `demo.launch(share=True)`
2. All code in single notebook (not split into files)
3. Cells use `#@title` to collapse in Colab

### NotebookEdit Usage

```python
# Create notebook with 3 cells
# Cell 0: Install (markdown type or code with %%capture)
# Cell 1: App code (code type with #@title)
# Cell 2: Launch (code type with #@title)
```

## Checklist Before Complete

**HF Space:**

- [ ] README.md has correct HF Spaces metadata
- [ ] app.py runs locally with `.venv/bin/python3 hf_spaces/app-name/app.py`
- [ ] No hardcoded API keys (uses os.environ.get)
- [ ] Graceful fallback when API keys missing
- [ ] Labels use PM-friendly business language
- [ ] Includes "How to Read This" help tab
- [ ] Works on free CPU tier
- [ ] requirements.txt lists all deps except gradio
- [ ] Error handling with gr.Warning/gr.Info (no raw exceptions)
- [ ] Layout uses Blocks with tabs/accordions appropriately
- [ ] Added to requirements.txt in project root if new deps needed

**Colab Workshop Notebook:**

- [ ] Created at `notebooks/workshop-apps/NN-app-name.ipynb`
- [ ] Cell 1: Install dependencies with `%%capture`
- [ ] Cell 2: Full app code with `#@title`
- [ ] Cell 3: `demo.launch(share=True)`
- [ ] Runs in Colab and produces `*.gradio.live` URL
