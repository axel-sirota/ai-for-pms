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

---

## Corporate Firewall Bypass (IMPORTANT)

**Problem:** Corporate firewalls (e.g., Intuit/Cisco Umbrella) block ALL `*.hf.space` domains.

**Solution:** Run apps in Google Colab with `share=True` to get `*.gradio.live` URLs.

### Quick Steps

1. Open Google Colab
2. Create notebook with 3 cells:
   - Cell 1: `!pip install gradio [deps] -q`
   - Cell 2: Paste app code from `hf_spaces/app-name/app.py`
   - Cell 3: `demo.launch(share=True)`
3. Run all cells - get `*.gradio.live` URL
4. Share URL with students

### Documentation

- **Overview:** `plans/firewall-bypass-overview.md`
- **Per-app migration:** `plans/migration/NN-app-name.md`

### Trade-offs

| HF Spaces | Colab + share=True |
| --------- | ------------------ |
| `*.hf.space` (blocked) | `*.gradio.live` (works) |
| Persistent URL | 72-hour expiry |
| Always running | Run each morning |

### Workshop Morning Procedure

1. Open each Colab notebook
2. Run all cells (Ctrl+F9)
3. Copy `gradio.live` URLs
4. Share URL list with students

---

## GitHub Pages (HTML)

HTML is auto-deployed to GitHub Pages:
`https://axel-sirota.github.io/ai-for-pms/`

To enable on a new repo:
```bash
gh api -X POST "/repos/OWNER/REPO/pages" -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
```
