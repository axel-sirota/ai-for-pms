# AI for Product Managers - Course Development

## FRESH CONVERSATION? START HERE

1. Run `/read` to load all context (GUIDELINES.md, initial_research/, sections/)
2. Then run the appropriate skill for your task (see GUIDELINES.md for the full workflow)
3. The build order per section is: `/phase-plan` → `/build-html-module` → `/build-gradio-app` → `/build-section` → `/validate-notebooks` → **DEPLOY** → `/next-phase`

## DEPLOYMENT (MANDATORY AFTER EACH SECTION)

After building a section, deploy immediately:

```bash
# Deploy Gradio apps to HuggingFace Spaces
.venv/bin/python3 scripts/deploy_hf_spaces.py <app-name>

# Or deploy all
.venv/bin/python3 scripts/deploy_hf_spaces.py
```

**Live URLs:**

- Apps: `https://huggingface.co/spaces/axelsirota/<app-name>`
- HTML: `https://axel-sirota.github.io/ai-for-pms/`

See `.claude/commands/deploy.md` for full instructions.

---

## Project Overview

This is a **3-day "AI for Product Managers" course** built by Data Trainers LLC. The course teaches PMs to lead AI initiatives confidently through interactive experiences, not lectures.

### Delivery Architecture
| Component | Format | Purpose |
|-----------|--------|---------|
| Concepts | HTML + Mermaid diagrams | Visual context (minimal theory) |
| Hands-on | HF Spaces (Gradio apps) | PMs EXPERIENCE every concept |
| Calculators | HF Spaces | ROI, cost, timeline estimators |
| Notebooks | Google Colab → deploy to HF Spaces | Build → test → deploy |

### Course Sections (9 modules, 3 days)
1. **AI Landscape** - Three paradigms (Classical ML / LLM / Agent)
2. **Classical ML** - When structured data + prediction wins
3. **LLMs** - Tokens, temperature, embeddings, prompt engineering
4. **RAG** - Knowledge-grounded AI, failure modes
5. **Agents** - Copilot vs Agent, ReAct, human-in-the-loop
6. **Evaluation** - ML metrics, LLM-as-judge, feedback loops
7. **Guardrails** - Input/output safety, compliance, incident response
8. **Cost & Timeline** - Token economics, project planning
9. **Strategy** - Decision frameworks, stakeholder communication

### Target Audience
Non-technical Product Managers. **No coding required from students.**

---

## Development Rules

### Content Philosophy
- **FAILURE STORY → PM DECISION POINT → MINIMAL THEORY → HANDS-ON → STAKEHOLDER FRAMING**
- 20% theory / 50% hands-on / 30% discussion
- Every concept must be EXPERIENCED, not just read about
- PMs need DECISION FRAMEWORKS, not implementation depth
- Kill all math formulas, algorithm taxonomies, architecture internals
- Keep: business cost framing, real failure stories, interactive demos

### File Organization
```
ai-for-pms-2026/
├── initial_research/          # TDD research docs (reference only)
├── sections/                  # Course content by section
│   ├── section-1-landscape/   # HTML + notebooks + HF Space code
│   ├── section-2-classical-ml/
│   ├── section-3-llms/
│   ├── section-4-rag/
│   ├── section-5-agents/
│   ├── section-6-evaluation/
│   ├── section-7-guardrails/
│   ├── section-8-cost-timeline/
│   └── section-9-strategy/
├── shared/                    # Shared assets (CSS, JS, templates)
├── hf_spaces/                 # HF Space app code (Gradio)
├── notebooks/                 # Colab notebooks
├── plans/                     # Temp planning docs (gitignored)
└── assets/                    # Images, diagrams, sample data
```

### HF Spaces / Gradio Apps
- All interactive apps use **Gradio** for consistent UX
- Code hidden from students - they interact via sliders/dropdowns/text boxes
- API keys managed via HF Secrets (never committed)
- ~25-30 total apps across the course
- Each app = a deployed HF Space students can access via URL

### Notebook Standards
- All code cells hidden with `@title` or collapsed
- Students see only widgets (ipywidgets) and outputs (Plotly charts)
- Use `ipywidgets` for sliders, dropdowns, checkboxes
- Use `plotly` for interactive visualizations
- Sample datasets included for every lab
- Zero coding required from students

### HTML Module Standards
- Single-page modules per sub-topic
- Mermaid diagrams for flowcharts and decision trees
- Mobile-friendly (works on tablets for workshop use)
- Links to relevant HF Spaces embedded
- Interactive elements via JavaScript (calculators, quizzes)

---

## Tech Stack

### Python Dependencies
- gradio (HF Spaces apps)
- plotly (interactive charts)
- ipywidgets (Colab interactivity)
- scikit-learn (classical ML demos)
- openai (LLM API calls)
- anthropic (Claude API calls)
- chromadb or faiss-cpu (vector search for RAG demos)
- sentence-transformers (embeddings)
- pandas, numpy (data handling)

### Environment
- Python virtualenv: `.venv/bin/python3`
- All pip commands: `.venv/bin/python3 -m pip install <package>`
- Always add new packages to `requirements.txt`
- Never use `python3` or `pip` directly - always use virtualenv

---

## Key References

### Research Documents (in initial_research/)
- **`ai-pm-course-full-interactive-architecture.md`** - **THE DEFINITIVE SPEC.** Final course architecture with all 9 sections, ~30 HF Spaces apps, delivery format, and "Experience Everything" principle. **Always read this first. When in doubt, this document wins.**
- `ai-pm-course-curriculum-design.md` - Background curriculum design with storyline, teaching philosophy, and module breakdowns (context/reference)
- `ai-pm-course-section4-tdd-research-interactive.md` - Section 4 RAG deep dive with calculator specs (context/reference)
- `ai-pm-course-section4-tdd-research.md` - TDD research findings, 100+ sources (context/reference)
- `ai_for_pms_course_review_complete.md` - Gap analysis of existing materials (context/reference)
- `ai_for_pms_course_review_updated.md` - Updated review with Model Tour + Prompt Patterns (context/reference)

### Key Stats PMs Should Know
- 95% of AI pilots fail to deliver P&L impact (MIT 2025)
- 90% retention with hands-on vs 10% with lecture
- Build vs Buy success: 33% vs 67% (MIT)
- 42% of companies abandoned AI initiatives in 2025

### Failure Stories Used Throughout
- Air Canada chatbot ($800K lawsuit)
- Meta Galactica (3-day shutdown)
- Knight Capital ($440M loss in 45 min)
- Microsoft Tay (racist in 24 hours)
- DPD chatbot (swore at customers)
