# Deploy Section to HuggingFace Spaces

Deploy Gradio apps to HuggingFace Spaces for student access.

## Prerequisites

1. HuggingFace account with write access
2. Login: `huggingface-cli login` (paste token from https://huggingface.co/settings/tokens)

## Deploy Commands

### Deploy All Apps
```bash
.venv/bin/python3 scripts/deploy_hf_spaces.py
```

### Deploy Single App
```bash
.venv/bin/python3 scripts/deploy_hf_spaces.py <app-name>
```

### List Available Apps
```bash
.venv/bin/python3 scripts/deploy_hf_spaces.py --list
```

## App Names by Section

**Section 1:**
- ai-paradigm-picker
- build-vs-buy-calculator
- model-comparison-arena

**Section 2:**
- classical-ml-playground
- metrics-explainer
- data-drift-simulator
- llm-vs-ml-showdown

**Section 3:**
- token-counter
- temperature-playground
- prompt-engineering-lab
- prompt-injection-sim
- embedding-explorer

## After Deployment

Apps will be available at:
`https://huggingface.co/spaces/axelsirota/<app-name>`

## Troubleshooting

- **Rate limited**: Wait 30 seconds and retry
- **Invalid colorTo**: Valid values: red, yellow, green, blue, indigo, purple, pink, gray
- **Not logged in**: Run `huggingface-cli login`

## GitHub Pages (HTML)

HTML is auto-deployed to GitHub Pages:
`https://axel-sirota.github.io/ai-for-pms/`

To enable on a new repo:
```bash
gh api -X POST "/repos/OWNER/REPO/pages" -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
```
