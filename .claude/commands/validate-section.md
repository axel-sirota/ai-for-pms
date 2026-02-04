---
description: Validate Section completeness, continuity, aesthetics, and guidelines compliance (project)
---

Run comprehensive validation on a section after building it. This checks continuity, aesthetics, and guidelines compliance.

**Usage:** `/validate-section N` (where N is the section number, e.g., `/validate-section 6`)

## MANDATORY PRE-VALIDATION READING

Before running validation, read these files to understand current standards:
1. `AESTHETICS.md` - Brand colors, typography, no rounded corners
2. `GUIDELINES.md` - Content philosophy, deliverable specs
3. `issues/` folder - All existing issue files for known problems
4. `initial_research/ai-pm-course-full-interactive-architecture.md` - Definitive spec

## VALIDATION CHECKLIST

### 1. AESTHETICS COMPLIANCE (AESTHETICS.md)

**HTML Modules - Check each file in `sections/section-N-name/`:**

- [ ] **Colors used correctly:**
  - Primary (Teal): `#40B8A6` for buttons, links, borders, accents
  - Navy: `#1A3D4D` for headings, text
  - Success: `#059669` / Danger: `#dc2626` / Accent: `#f59e0b`
- [ ] **No rounded corners:** `border-radius: 0` (search for `border-radius` and flag any non-zero values)
- [ ] **Mermaid diagrams themed correctly:**
  ```javascript
  primaryColor: '#E6F7F5'
  primaryTextColor: '#1A3D4D'
  primaryBorderColor: '#40B8A6'
  ```
- [ ] **Font family:** Inter (Google Fonts) for body, JetBrains Mono for code
- [ ] **CSS variables used:** `--primary`, `--navy`, `--text`, etc. (not hardcoded colors)

**Gradio Apps - Check each app in `hf_spaces/`:**

- [ ] Uses `gr.themes.Soft()` for consistent look
- [ ] Teal (#40B8A6) used for primary accents in Plotly charts
- [ ] Navy (#1A3D4D) used for text in visualizations

### 2. GUIDELINES COMPLIANCE (GUIDELINES.md)

**Content Philosophy - Every module must follow:**

- [ ] **FAILURE STORY** opens the content (real company, real cost)
- [ ] **PM DECISION POINT** - "As a PM, you would need to decide..."
- [ ] **MINIMAL THEORY** - No math formulas, algorithm taxonomies, architecture internals
- [ ] **HANDS-ON** - Links to interactive apps (HF Spaces)
- [ ] **STAKEHOLDER FRAMING** - "Here's how you'd explain this to your VP..."

**HTML Module Structure:**

- [ ] Shared CSS from `shared/css/course.css`
- [ ] Mermaid loaded via CDN: `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs`
- [ ] Mobile-friendly (check viewport meta tag)
- [ ] No code shown to students
- [ ] Interactive elements work (quizzes, calculators)

**Gradio Apps Structure:**

- [ ] `app.py`, `requirements.txt`, `README.md` present
- [ ] Uses `gr.Blocks()` for layout
- [ ] API keys via `os.environ.get()` (never hardcoded)
- [ ] Works on free CPU tier (no GPU)
- [ ] `gradio==4.44.1` and `huggingface_hub==0.24.0` pinned

**Notebook Structure:**

- [ ] All code cells use `#@title` to hide code
- [ ] ipywidgets for student interaction
- [ ] Plotly for visualizations (not matplotlib)
- [ ] Setup cell has `!pip install "ipywidgets>=7,<8"`
- [ ] Setup cell has `output.enable_custom_widget_manager()`
- [ ] No hardcoded API keys

### 3. CONTINUITY CHECKS (from issues/)

**Section Bridges:**

- [ ] Section index has "Coming From Section X" bridge paragraph
- [ ] Section ends with "Up Next: Section Y" preview
- [ ] Previous/Next navigation links work correctly

**Learning Objectives:**

- [ ] Each module starts with "By the end of this module, you'll be able to..."
- [ ] Objectives use action verbs (understand, apply, evaluate, design)

**PM Decision Context:**

- [ ] Apps have "PM Decision:" framing in intro
- [ ] Apps have "PM Takeaway:" at footer
- [ ] Content explains WHY a PM should care

**Navigation Consistency:**

- [ ] Breadcrumbs follow format: `Section X > Module X.Y > Title`
- [ ] Section labels are consistent (no timing references like "Day 1")
- [ ] Module numbering aligns with section (3.1, 3.2, etc.)

### 4. CROSS-SECTION CONTINUITY

**Storyline Flow:**

- [ ] Concepts build on previous sections (not introduced cold)
- [ ] Failure stories don't repeat across sections (unless intentional callback)
- [ ] Apps reference related apps from earlier sections where relevant

**Terminology Consistency:**

- [ ] Same terms used for same concepts (not "model" in one place, "system" in another)
- [ ] Acronyms defined on first use in each section

### 5. KNOWN ISSUES CHECK

Read `issues/POTENTIAL_STORYLINE_ISSUES_DAY1.md` and any other files in `issues/` folder.

For each issue listed:
- [ ] Check if it applies to this section
- [ ] If critical/medium severity, flag for fix
- [ ] If already fixed, note as resolved

## VALIDATION OUTPUT FORMAT

After checking, provide a report in this format:

```markdown
# Section N Validation Report

## Summary
- Total checks: X
- Passed: Y
- Failed: Z
- Warnings: W

## Critical Issues (Must Fix)
1. [Issue description] - [File:line]
2. ...

## Medium Issues (Should Fix)
1. [Issue description] - [File:line]
2. ...

## Warnings (Nice to Have)
1. [Issue description] - [File:line]
2. ...

## Aesthetics Compliance
- [✅/❌] Color palette
- [✅/❌] No rounded corners
- [✅/❌] Mermaid theming
- [✅/❌] Typography

## Guidelines Compliance
- [✅/❌] Content philosophy (FAILURE->PM DECISION->THEORY->HANDS-ON->STAKEHOLDER)
- [✅/❌] HTML module structure
- [✅/❌] Gradio app structure
- [✅/❌] Notebook structure

## Continuity
- [✅/❌] Section bridges
- [✅/❌] Learning objectives
- [✅/❌] PM decision context
- [✅/❌] Navigation consistency

## Known Issues Status
- Issue #X: [Fixed/Not Fixed/Not Applicable]
- ...

## Recommendations
1. Priority fix: [description]
2. ...
```

## HOW TO RUN VALIDATION

1. Read all files in the section:
   - `sections/section-N-name/*.html`
   - `hf_spaces/app-name/` for section's apps
   - `notebooks/section-N-name/*.ipynb`
   - `notebooks/workshop-apps/` firewall bypass notebooks for section

2. For each file, run the relevant checklist items

3. Cross-reference with issues folder

4. Generate the validation report

5. If critical issues found, list specific fixes needed

## WHEN TO RUN

Run `/validate-section N` after:
- Completing `/build-section N`
- Before running `/next-phase`
- Before marking section as complete
- After making fixes to address feedback
