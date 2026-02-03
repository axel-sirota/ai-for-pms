---
description: Build an HTML concept module for a course section (project)
---

Build HTML module: $ARGUMENTS

(Format: section.submodule, e.g., "4.1" or "4.2")

## Pre-Work: MANDATORY Reading

**READ THESE FILES BEFORE DOING ANYTHING:**

1. **CLAUDE.md** - Content philosophy, delivery architecture
2. **GUIDELINES.md** - HTML module specs, content checklist, failure stories
3. **initial_research/ai-pm-course-full-interactive-architecture.md** - **DEFINITIVE SPEC** (read first, this wins when in doubt)
4. **initial_research/ai-pm-course-curriculum-design.md** - Background context/reference
5. **shared/css/course.css** - Shared stylesheet (if it exists)
6. **The section folder** in sections/section-N-name/ (existing modules)

## Plan the Module

**IN CHAT, SHOW ME YOUR PLAN:**

1. Module number and title (e.g., "4.1 The Problem RAG Solves")
2. Opening failure story (which one, what cost, what went wrong)
3. PM decision point ("As a PM, you would have needed to decide...")
4. Minimal theory content (bullet points only, no paragraphs of explanation)
5. Mermaid diagrams to include (describe each one)
6. Links to HF Spaces apps (which apps, how embedded)
7. Interactive JS elements (quizzes, calculators, decision trees)
8. Stakeholder framing ("Here's how you'd present this to your VP...")

**DO NOT PROCEED until I approve this plan.**

## HTML Module Structure

Every module follows this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>N.X - Module Title</title>
    <link rel="stylesheet" href="../../shared/css/course.css">
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
    </script>
</head>
<body>
    <!-- 1. FAILURE STORY -->
    <section class="failure-story">...</section>

    <!-- 2. PM DECISION POINT -->
    <section class="decision-point">...</section>

    <!-- 3. MINIMAL THEORY (with Mermaid diagrams) -->
    <section class="theory">
        <pre class="mermaid">
            graph TD
            A[Start] --> B{Decision}
        </pre>
    </section>

    <!-- 4. HANDS-ON LINK (to HF Space) -->
    <section class="hands-on">
        <iframe src="https://huggingface.co/spaces/..." ...></iframe>
    </section>

    <!-- 5. STAKEHOLDER FRAMING -->
    <section class="stakeholder-framing">...</section>

    <!-- 6. NAVIGATION -->
    <nav class="module-nav">
        <a href="N.X-1.html">Previous</a>
        <a href="N.X+1.html">Next</a>
    </nav>
</body>
</html>
```

## Content Rules

- **No code** shown to students, ever
- **No math formulas** - translate everything to business language
- **No algorithm taxonomies** - focus on "when to use what"
- **No em dashes** - use regular dashes `-` instead of `&mdash;` or em dash characters
- **Mermaid diagrams** for all flowcharts and decision trees
- **Mobile-friendly** - works on tablets for workshop use
- **Each `<pre class="mermaid">` tag** gets its own diagram; never combine multiple
- **Interactive JS elements** for quizzes use simple event listeners, no frameworks
- **Failure stories** must include: company name, what happened, business cost, PM lesson

## Mermaid Diagram Guidelines

- Use `graph TD` (top-down) for decision trees
- Use `graph LR` (left-right) for pipelines/workflows
- Use `sequenceDiagram` for interaction flows
- Keep diagrams simple (max 10-12 nodes)
- Use clear, PM-friendly labels (not technical jargon)
- Each diagram in its own `<pre class="mermaid">` tag

## File Location

Save to: `sections/section-N-name/N.X-module-title.html`

Example: `sections/section-4-rag/4.1-problem-rag-solves.html`

## Checklist Before Complete

- [ ] Opens with failure story (company, cost, lesson)
- [ ] PM decision point clearly stated
- [ ] Theory is minimal (20% of content max)
- [ ] Mermaid diagrams render correctly
- [ ] Links to relevant HF Spaces apps
- [ ] Stakeholder framing section present
- [ ] Mobile-friendly (test with narrow viewport)
- [ ] Navigation to previous/next module
- [ ] No code, no math, no algorithm taxonomies
- [ ] Uses shared CSS from shared/css/course.css
