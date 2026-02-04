"""
Tool Use Sandbox - Watch an agent use tools to solve multi-step problems
Helps PMs understand how agents select and use tools
"""

import gradio as gr
import time
import json

# Available tools with descriptions
AVAILABLE_TOOLS = {
    "web_search": {
        "description": "Search the web for information",
        "parameters": ["query"],
        "example": "web_search(query='best practices for AI agents')"
    },
    "calculator": {
        "description": "Perform mathematical calculations",
        "parameters": ["expression"],
        "example": "calculator(expression='1500 * 0.15')"
    },
    "calendar_lookup": {
        "description": "Check calendar for availability",
        "parameters": ["date", "person"],
        "example": "calendar_lookup(date='2024-01-20', person='John')"
    },
    "send_email_draft": {
        "description": "Create an email draft (does not send)",
        "parameters": ["to", "subject", "body"],
        "example": "send_email_draft(to='john@example.com', subject='Meeting', body='...')"
    },
    "database_query": {
        "description": "Query the sample database",
        "parameters": ["table", "filter"],
        "example": "database_query(table='customers', filter='status=active')"
    },
    "file_reader": {
        "description": "Read contents of a file",
        "parameters": ["filename"],
        "example": "file_reader(filename='project_data.csv')"
    }
}

# Pre-defined task scenarios with simulated execution
TASK_SCENARIOS = {
    "meeting_scheduler": {
        "task": "Schedule a project kickoff meeting with John and Sarah next week. Calculate the project budget at 15% of the $50,000 total, and draft an invite email.",
        "tools_needed": ["calendar_lookup", "calculator", "send_email_draft"],
        "execution": [
            {
                "step": 1,
                "reasoning": "I need to find when John is available next week. Let me check the calendar.",
                "tool": "calendar_lookup",
                "call": "calendar_lookup(date='2024-01-22', person='John')",
                "result": "John is available: Mon 10am-12pm, Tue 2pm-4pm, Thu 9am-11am"
            },
            {
                "step": 2,
                "reasoning": "Now I need to check Sarah's availability to find overlap.",
                "tool": "calendar_lookup",
                "call": "calendar_lookup(date='2024-01-22', person='Sarah')",
                "result": "Sarah is available: Mon 11am-1pm, Tue 2pm-5pm, Wed all day"
            },
            {
                "step": 3,
                "reasoning": "Both are available Tuesday 2pm-4pm. Now I need to calculate the budget.",
                "tool": "calculator",
                "call": "calculator(expression='50000 * 0.15')",
                "result": "7500.0"
            },
            {
                "step": 4,
                "reasoning": "Budget is $7,500. Now I'll draft the meeting invite.",
                "tool": "send_email_draft",
                "call": "send_email_draft(to='john@example.com, sarah@example.com', subject='Project Kickoff - Tuesday 2pm', body='Hi team, let\\'s meet Tuesday 2-4pm to kick off the project. Budget allocation: $7,500.')",
                "result": "Email draft created. Ready for review."
            },
            {
                "step": 5,
                "reasoning": "Task complete. Summarizing results.",
                "tool": None,
                "call": None,
                "result": "COMPLETE: Meeting scheduled for Tuesday 2-4pm. Budget: $7,500. Email draft ready for your review."
            }
        ]
    },
    "research_report": {
        "task": "Research the latest trends in AI agents, find relevant data from our customer database, and summarize findings.",
        "tools_needed": ["web_search", "database_query", "file_reader"],
        "execution": [
            {
                "step": 1,
                "reasoning": "I need to search for the latest AI agent trends.",
                "tool": "web_search",
                "call": "web_search(query='AI agents trends 2024 enterprise')",
                "result": "Found 15 articles. Key trends: 1) Agentic workflows up 300%, 2) Human-in-the-loop critical, 3) Tool use becoming standard."
            },
            {
                "step": 2,
                "reasoning": "Let me find more specific data about enterprise adoption.",
                "tool": "web_search",
                "call": "web_search(query='enterprise AI agent adoption statistics')",
                "result": "Gartner: 45% of enterprises piloting agents by 2025. McKinsey: $2.6T potential value from agentic AI."
            },
            {
                "step": 3,
                "reasoning": "Now I should check our internal customer data for relevant insights.",
                "tool": "database_query",
                "call": "database_query(table='customers', filter='ai_features=enabled')",
                "result": "127 customers have AI features enabled. Average usage: 450 queries/day. Top use case: customer support (62%)."
            },
            {
                "step": 4,
                "reasoning": "Let me also check if there's any previous research we've done.",
                "tool": "file_reader",
                "call": "file_reader(filename='previous_ai_research.md')",
                "result": "Previous research (Q3 2023): Identified 5 key barriers - trust, accuracy, cost, integration, compliance."
            },
            {
                "step": 5,
                "reasoning": "I have enough information. Compiling the summary.",
                "tool": None,
                "call": None,
                "result": "COMPLETE: Research compiled. Key findings: 45% enterprise adoption expected, $2.6T market potential, our customers using AI primarily for support (62%). Previous barriers still relevant. Recommend focusing on trust-building features."
            }
        ]
    },
    "expense_analysis": {
        "task": "Analyze Q4 expenses from the finance file, calculate the total and average, and draft a summary email to the CFO.",
        "tools_needed": ["file_reader", "calculator", "send_email_draft"],
        "execution": [
            {
                "step": 1,
                "reasoning": "First, I need to read the expense file.",
                "tool": "file_reader",
                "call": "file_reader(filename='q4_expenses.csv')",
                "result": "Read 47 expense entries. Categories: Travel ($45,230), Software ($32,100), Marketing ($28,500), Equipment ($15,200), Other ($8,970)"
            },
            {
                "step": 2,
                "reasoning": "Now I'll calculate the total expenses.",
                "tool": "calculator",
                "call": "calculator(expression='45230 + 32100 + 28500 + 15200 + 8970')",
                "result": "130000.0"
            },
            {
                "step": 3,
                "reasoning": "Let me calculate the average per category.",
                "tool": "calculator",
                "call": "calculator(expression='130000 / 5')",
                "result": "26000.0"
            },
            {
                "step": 4,
                "reasoning": "Now I'll calculate percent change from Q3 (which was $115,000).",
                "tool": "calculator",
                "call": "calculator(expression='((130000 - 115000) / 115000) * 100')",
                "result": "13.04"
            },
            {
                "step": 5,
                "reasoning": "I have all the data. Drafting the summary email.",
                "tool": "send_email_draft",
                "call": "send_email_draft(to='cfo@company.com', subject='Q4 Expense Summary', body='Q4 Total: $130,000 (+13% vs Q3). Top category: Travel ($45,230). Average per category: $26,000.')",
                "result": "Email draft created for CFO review."
            },
            {
                "step": 6,
                "reasoning": "Task complete.",
                "tool": None,
                "call": None,
                "result": "COMPLETE: Q4 expenses analyzed. Total: $130,000 (13% increase from Q3). Email draft ready for review."
            }
        ]
    }
}


def get_tools_list():
    """Format available tools for display"""
    tools_md = "## Available Tools\n\n"
    for name, info in AVAILABLE_TOOLS.items():
        tools_md += f"### `{name}`\n"
        tools_md += f"{info['description']}\n\n"
        tools_md += f"**Parameters:** {', '.join(info['parameters'])}\n\n"
        tools_md += f"**Example:** `{info['example']}`\n\n"
    return tools_md


def run_task(task_key, show_reasoning, step_delay):
    """Execute a task and show the agent's tool usage"""

    if task_key not in TASK_SCENARIOS:
        yield "Please select a task scenario."
        return

    scenario = TASK_SCENARIOS[task_key]

    output_lines = []
    output_lines.append(f"# Task Execution\n")
    output_lines.append(f"**Task:** {scenario['task']}\n")
    output_lines.append(f"**Tools Available:** {', '.join(f'`{t}`' for t in scenario['tools_needed'])}\n")
    output_lines.append("\n---\n")

    yield "\n".join(output_lines)

    tool_calls = []

    for step in scenario["execution"]:
        time.sleep(step_delay)

        step_num = step["step"]
        reasoning = step["reasoning"]
        tool = step["tool"]
        call = step["call"]
        result = step["result"]

        output_lines.append(f"## Step {step_num}\n")

        if show_reasoning:
            output_lines.append(f"**Reasoning:** {reasoning}\n")

        if tool:
            output_lines.append(f"**Tool:** `{tool}`\n")
            output_lines.append(f"```\n{call}\n```\n")
            tool_calls.append(tool)

        output_lines.append(f"**Result:** {result}\n")
        output_lines.append("\n---\n")

        yield "\n".join(output_lines)

    # Summary
    output_lines.append("\n## Execution Summary\n")
    output_lines.append(f"- **Total Steps:** {len(scenario['execution'])}")
    output_lines.append(f"- **Tools Used:** {len(tool_calls)}")
    output_lines.append(f"- **Unique Tools:** {len(set(tool_calls))}")
    output_lines.append(f"\n**Tool Call Sequence:** {' → '.join(tool_calls) if tool_calls else 'None'}")

    yield "\n".join(output_lines)


def get_task_info(task_key):
    """Get information about a task"""
    if task_key not in TASK_SCENARIOS:
        return "Select a task to see details."

    scenario = TASK_SCENARIOS[task_key]
    return f"""### Task Preview

**Task:** {scenario['task']}

**Tools Needed:** {', '.join(f'`{t}`' for t in scenario['tools_needed'])}

**Expected Steps:** {len(scenario['execution'])}
"""


# Build the Gradio interface
with gr.Blocks(title="Tool Use Sandbox", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Tool Use Sandbox

    Watch an AI agent select and use tools to solve multi-step problems.

    **For Product Managers:** This tool helps you understand how agents decide
    which tools to use and in what order.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Task Configuration")

            task_dropdown = gr.Dropdown(
                choices=[
                    ("Meeting Scheduler", "meeting_scheduler"),
                    ("Research Report", "research_report"),
                    ("Expense Analysis", "expense_analysis")
                ],
                value="meeting_scheduler",
                label="Task Scenario"
            )

            task_info = gr.Markdown(get_task_info("meeting_scheduler"))

            show_reasoning = gr.Checkbox(
                value=True,
                label="Show Agent Reasoning",
                info="Display the agent's thought process"
            )

            step_delay = gr.Slider(
                minimum=0.3,
                maximum=2.0,
                value=0.8,
                step=0.1,
                label="Step Delay (seconds)"
            )

            run_btn = gr.Button("Run Task", variant="primary")

            with gr.Accordion("Available Tools Reference", open=False):
                gr.Markdown(get_tools_list())

        with gr.Column(scale=2):
            gr.Markdown("### Execution Log")
            output = gr.Markdown("Select a task and click 'Run Task' to see the agent in action.")

    gr.Markdown("""
    ---
    ### PM Insights: Tool Use Design

    **Key Questions When Designing Tool Access:**

    1. **What tools does the agent need?** Start minimal, add tools as needed.
    2. **What are the limits on each tool?** Max queries, dollar amounts, etc.
    3. **Which tool combinations are dangerous?** (e.g., database_query + send_email = potential data leak)
    4. **What happens if a tool fails?** Retry? Escalate? Give up?

    **Best Practices:**

    - **Least privilege:** Only give tools the agent actually needs
    - **Explicit descriptions:** Tool descriptions should be unambiguous
    - **Validation:** Check tool parameters before execution
    - **Logging:** Record every tool call for debugging
    - **Rate limits:** Prevent runaway tool usage

    **Warning Signs:**
    - Agent calling the same tool repeatedly → potential loop
    - Agent trying tools not in the list → hallucination
    - Unusual tool combinations → potential security issue
    """)

    # Event handlers
    task_dropdown.change(
        fn=get_task_info,
        inputs=[task_dropdown],
        outputs=[task_info]
    )

    run_btn.click(
        fn=run_task,
        inputs=[task_dropdown, show_reasoning, step_delay],
        outputs=[output]
    )

if __name__ == "__main__":
    demo.launch()
