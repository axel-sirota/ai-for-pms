---
description: Create a TDD-style plan through iterative hypothesis refinement (3 cycles) (project)
---

Create a comprehensive TDD-style plan for: $ARGUMENTS

**CRITICAL: All process and cycles must be visible IN CHAT. Do not skip steps or summarize - show full reasoning.**

## Process Overview

You will iterate through 3 complete cycles of hypothesis formation, research, refutation, and refinement. Each cycle must be fully documented in the chat.

## Cycle Structure (Repeat 3 Times)

### Cycle 1, 2, 3: [Title the cycle]

#### Step 1: Scan Relevant Context & Form Initial Hypothesis

**DO THIS IN CHAT:**
1. Identify all relevant files and code sections to read
2. Read the relevant code and understand current implementation
3. Review related documentation (CLAUDE.md, initial_research/, etc.)
4. Understand the problem/feature request
5. **Formulate your initial hypothesis** - Write out:
   - What you think needs to be done
   - How you plan to approach it
   - What assumptions you're making
   - What the expected outcome should be

**Files to always check first:**
- CLAUDE.md
- **initial_research/ai-pm-course-full-interactive-architecture.md** (DEFINITIVE SPEC - read first, this wins when in doubt)
- Other initial_research/*.md files (background context/reference)
- Relevant sections/ content (if it exists)
- shared/ templates (if they exist)
- hf_spaces/ apps (if related)

#### Step 2: Research Potential Shortcomings (Optional but Recommended)

**DO THIS IN CHAT:**
- If the approach has potential risks or unknowns, perform web searches
- Search for:
  - Best practices for similar patterns (Gradio apps, PM training, interactive learning)
  - Known pitfalls or issues
  - Performance considerations
  - Accessibility concerns
  - HF Spaces deployment patterns
- Document findings in chat

**If research is not needed, explicitly state why:**
- "Research not needed because: [reason]"

#### Step 3: Refute Initial Hypothesis

**DO THIS IN CHAT:**
- Critically analyze your initial hypothesis based on:
  - Code review findings
  - Research results (if performed)
  - Content philosophy (FAILURE STORY → PM DECISION POINT → MINIMAL THEORY → HANDS-ON → STAKEHOLDER FRAMING)
  - Target audience constraints (non-technical PMs, zero coding)
  - Edge cases and error scenarios
- List all potential issues:
  - What could go wrong?
  - What assumptions might be wrong?
  - Does this align with 20% theory / 50% hands-on / 30% discussion?
  - What violates existing patterns?
  - What accessibility issues exist?

#### Step 4: Refine Thinking & Create New Plan

**DO THIS IN CHAT:**
- Based on the refutation, create a refined plan:
  - Address the issues identified
  - Adjust the approach
  - Add missing considerations
  - Update assumptions
- Document the refined hypothesis

---

## After All 3 Cycles

### Final Plan Synthesis

Create the final comprehensive plan that incorporates learnings from all 3 cycles:

1. **Problem Statement**
   - Clear description of what needs to be implemented
   - Context and constraints

2. **Architecture/Design Decisions**
   - Final approach after 3 iterations
   - Rationale for decisions
   - Alternatives considered

3. **Implementation Steps**
   - Specific files to create/modify
   - HTML modules, Gradio apps, notebooks as applicable
   - Content outline for each deliverable

4. **Validation Strategy**
   - How to verify the content works
   - HF Spaces testing approach
   - Notebook execution validation

5. **Files to Modify/Create**
   - Specific file paths
   - What changes in each file

6. **Success Criteria**
   - How to verify the implementation works
   - What manual verification is needed
   - Does it follow the content philosophy?

7. **Potential Risks & Mitigations**
   - Risks identified through iterations
   - How to mitigate them

---

## Important Notes

- **DO NOT** skip showing the process - all cycles must be visible
- **DO NOT** summarize cycles - show full reasoning each time
- **DO NOT** rush to the final plan - the iterative process is the value
- **DO** be thorough in refutation - challenge your own assumptions
- **DO** incorporate learnings from previous cycles into the next
- **DO** read actual files, not just summaries
- **DO** consider the content philosophy from CLAUDE.md
