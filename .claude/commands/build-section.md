---
description: Build Colab notebook for a course section (project)
---

Build the Colab notebook for section: $ARGUMENTS

## Pre-Work: MANDATORY Reading

**READ THESE FILES BEFORE DOING ANYTHING:**

1. **CLAUDE.md** - Content philosophy, delivery architecture, tech stack
2. **GUIDELINES.md** - Build workflow, deliverable specs, content checklist
3. **initial_research/ai-pm-course-full-interactive-architecture.md** - **DEFINITIVE SPEC** (read first, this wins when in doubt)
4. **initial_research/ai-pm-course-curriculum-design.md** - Background context/reference
5. **The section folder** in sections/section-N-name/ (HTML modules if they exist already)

## Extract Section Information

From the **definitive spec** (ai-pm-course-full-interactive-architecture.md), extract for the requested section:

- Section title, duration, and learning objectives
- Key concepts to cover
- Failure stories to use
- PM decision points
- Apps/demos that accompany this section
- Stakeholder framing angles

## Plan the Notebook Structure

**IN CHAT, SHOW ME YOUR PLAN:**

1. Section title and learning objectives
2. Failure story to open with
3. List of 2-4 interactive demos (ipywidgets + plotly)
4. For EACH demo:
   - What concept it teaches
   - What widgets the PM interacts with (sliders, dropdowns, etc.)
   - What plotly visualization they see
   - What PM decision it illustrates
5. Discussion prompts between demos
6. Stakeholder framing summary

**DO NOT PROCEED until I approve this plan.**

## Notebook Design Principles

### Target Audience: Non-Technical PMs
- **ZERO coding** - Students never write or see code
- All code cells use `#@title` to collapse/hide them
- Students interact ONLY via ipywidgets and see ONLY plotly outputs
- Every interaction must teach a PM decision, not a technical skill

### Cell Structure
1. **Setup cell** (hidden): `!pip install` + imports + `output.enable_custom_widget_manager()`
2. **Context markdown**: Failure story, PM framing, "why this matters"
3. **Interactive demo cells** (hidden code): Widget inputs -> plotly outputs
4. **Discussion markdown**: "Turn to your neighbor and discuss..."
5. **Stakeholder framing markdown**: "Here's how you'd explain this to your VP..."

### Technical Requirements
- Pin ipywidgets: `!pip install "ipywidgets>=7,<8"` for Colab compatibility
- Use `%%capture` for install cells to suppress output
- Use `plotly.graph_objects` or `plotly.express` for all charts
- Use `ipywidgets.interact()` or `ipywidgets.interactive()` for widget binding
- Include `from google.colab import output; output.enable_custom_widget_manager()`
- Set random seeds for reproducibility

### Content Flow Per Demo
```
[Hidden code cell: setup widgets + plotly figure]
[Markdown: "Try adjusting the slider to see how X affects Y"]
[Hidden code cell: interactive widget -> plotly output]
[Markdown: "PM Insight: When X increases, you should expect..."]
[Markdown: "Discussion: How would this affect your project timeline?"]
```

### Text Formatting Rules

- **No em dashes** - use regular dashes `-` instead of `&mdash;` or em dash characters

## CRITICAL: Incremental Building

**NEVER ADD MORE THAN 5 CELLS WITHOUT APPROVAL**

1. Add maximum 5 cells
2. STOP IMMEDIATELY
3. Ask: "I've added cells X-Y. How does it look? Should I continue?"
4. DO NOT PROCEED until explicit approval
5. "Continue" means next 5 cells ONLY

### Implementation:

Use NotebookEdit tool to add cells incrementally:

```
First batch (cells 0-4):
- Cell 0: Title + learning objectives markdown
- Cell 1: Setup code (hidden with #@title)
- Cell 2: Failure story context markdown
- Cell 3: First demo code (hidden with #@title)
- Cell 4: PM insight + discussion markdown

STOP - Ask for approval
WAIT FOR APPROVAL

Second batch (cells 5-9):
- Continue with next demo...
```

### NotebookEdit Rules:
- First cell: `edit_mode="insert"` (no cell_id needed)
- All subsequent cells: MUST specify `cell_id` of the previous cell
- Track cell IDs from each NotebookEdit return value

## File Locations

- Create notebook at: `notebooks/section-N-name/section_N_name.ipynb`
- Create the directory first if it doesn't exist

## Checklist Before Marking Complete

- [ ] All code cells hidden with `#@title`
- [ ] Students never see code, only widgets and charts
- [ ] Opens with failure story
- [ ] Each demo teaches a PM decision
- [ ] ipywidgets for all student interaction
- [ ] Plotly for all visualizations
- [ ] Discussion prompts between demos
- [ ] Stakeholder framing at the end
- [ ] Runs top-to-bottom in Colab without errors
- [ ] Content follows: FAILURE STORY -> PM DECISION -> MINIMAL THEORY -> HANDS-ON -> STAKEHOLDER FRAMING

## AFTER COMPLETION

Run `/validate-section N` to check:

- Aesthetics compliance (AESTHETICS.md)
- Guidelines compliance (GUIDELINES.md)
- Continuity with previous sections
- Known issues from issues/ folder

## NOW BEGIN:

1. Read all context files
2. Show me the plan for section [NUMBER]
3. Wait for my approval
4. Start building incrementally (5 cells at a time)
5. After completion, run `/validate-section N`
