---
description: Validate Notebooks (project)
---

Run validation on course notebooks to verify quality and correctness.

## What to Validate

For each notebook in `notebooks/section-N-name/`:

### 1. Structure Checks
- First cell is markdown with title and learning objectives
- All code cells use `#@title` to hide code from students
- No raw code visible to students (everything collapsed)
- Markdown cells alternate with code cells appropriately

### 2. Content Philosophy Checks
- Opens with a failure story or real-world scenario
- Contains PM decision points (not technical implementation)
- Has discussion prompts between demos
- Ends with stakeholder framing
- No math formulas, algorithm taxonomies, or code snippets shown to students

### 3. Technical Checks
- `ipywidgets` used for all student interaction (sliders, dropdowns, etc.)
- `plotly` used for all visualizations (not matplotlib)
- Setup cell includes `!pip install "ipywidgets>=7,<8"`
- Setup cell includes `from google.colab import output; output.enable_custom_widget_manager()`
- No hardcoded API keys
- All imports in setup cell

### 4. Execution Check
- Read the notebook JSON and verify:
  - All code cells have valid Python syntax
  - No undefined variables across cells
  - Import statements are present for all used libraries

## How to Run

```bash
# Validate a specific notebook
.venv/bin/python3 -c "
import json, ast, sys
with open('notebooks/section-N-name/section_N_name.ipynb') as f:
    nb = json.load(f)
errors = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if '#@title' not in source and source.strip():
            errors.append(f'Cell {i}: Missing #@title (code visible to students)')
        try:
            ast.parse(source)
        except SyntaxError as e:
            errors.append(f'Cell {i}: Syntax error: {e}')
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        if '```python' in source:
            errors.append(f'Cell {i}: Code block in markdown (students should not see code)')
if errors:
    print('VALIDATION ERRORS:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('All checks passed')
"
```

## When to Run

- After creating/editing any notebook
- Before marking a section as complete
- Before distributing notebooks to students
