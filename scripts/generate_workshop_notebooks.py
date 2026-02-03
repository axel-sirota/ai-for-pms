#!/usr/bin/env python3
"""Generate Colab workshop notebooks for all HF Space apps.

Creates notebooks in notebooks/workshop-apps/ with share=True for firewall bypass.
"""

import json
import os
from pathlib import Path

# App definitions: (number, name, extra_deps)
APPS = [
    ("01", "ai-paradigm-picker", []),
    ("02", "build-vs-buy-calculator", []),
    ("03", "model-comparison-arena", ["openai", "anthropic"]),
    ("04", "token-counter", ["tiktoken"]),
    ("05", "temperature-playground", ["openai"]),
    ("06", "llm-vs-ml-showdown", ["plotly"]),
    ("07", "prompt-engineering-lab", []),
    ("08", "prompt-injection-sim", []),
    ("09", "classical-ml-playground", ["scikit-learn", "plotly", "pandas", "numpy"]),
    ("10", "embedding-explorer", ["sentence-transformers", "scikit-learn", "plotly", "numpy"]),
    ("11", "data-drift-simulator", ["scikit-learn", "plotly", "numpy"]),
    ("12", "metrics-explainer", ["plotly", "numpy"]),
    ("13", "rag-playground", ["sentence-transformers", "chromadb"]),
    ("14", "rag-failure-simulator", []),
    ("15", "chunking-visualizer", []),
    ("16", "rag-vs-finetuning", []),
    ("17", "vector-db-cost-calculator", []),
]

def create_notebook(num: str, app_name: str, extra_deps: list[str], hf_spaces_dir: Path, output_dir: Path):
    """Create a Colab notebook for the given app."""
    app_py = hf_spaces_dir / app_name / "app.py"

    if not app_py.exists():
        print(f"  SKIP: {app_py} not found")
        return False

    # Read app code
    app_code = app_py.read_text()

    # Remove the final demo.launch() line - we'll add it in a separate cell
    lines = app_code.split('\n')
    new_lines = []
    for line in lines:
        # Skip lines that are just demo.launch() at the module level
        if line.strip().startswith('demo.launch(') and 'if __name__' not in '\n'.join(lines[max(0, lines.index(line)-5):lines.index(line)]):
            continue
        # Skip if __name__ == "__main__" block
        if line.strip() == 'if __name__ == "__main__":':
            break
        new_lines.append(line)

    app_code_clean = '\n'.join(new_lines).rstrip()

    # Build deps string
    deps = ["gradio"] + extra_deps
    deps_str = " ".join(deps)

    # Create notebook structure
    notebook = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "#@title Install Dependencies\n",
                    "%%capture\n",
                    f"!pip install {deps_str} -q"
                ],
                "outputs": []
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [f"#@title {app_name.replace('-', ' ').title()} App\n"] + [line + "\n" for line in app_code_clean.split('\n')],
                "outputs": []
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "#@title Launch App - Copy the gradio.live URL below\n",
                    "demo.launch(share=True)"
                ],
                "outputs": []
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # Write notebook
    output_path = output_dir / f"{num}-{app_name}.ipynb"
    with open(output_path, 'w') as f:
        json.dump(notebook, f, indent=1)

    print(f"  OK: {output_path.name}")
    return True


def main():
    # Paths
    repo_root = Path(__file__).parent.parent
    hf_spaces_dir = repo_root / "hf_spaces"
    output_dir = repo_root / "notebooks" / "workshop-apps"

    # Create output dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating workshop notebooks...")
    print(f"Source: {hf_spaces_dir}")
    print(f"Output: {output_dir}")
    print()

    success = 0
    for num, name, deps in APPS:
        created = create_notebook(num, name, deps, hf_spaces_dir, output_dir)
        if created:
            success += 1

    print()
    print(f"Done: {success}/{len(APPS)} notebooks created")


if __name__ == "__main__":
    main()
