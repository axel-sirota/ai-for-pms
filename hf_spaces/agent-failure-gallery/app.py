"""
Agent Failure Gallery - Watch agents fail in controlled scenarios
Helps PMs understand common agent failure modes and how to prevent them
"""

import gradio as gr
import time

# Pre-recorded failure scenarios
FAILURE_SCENARIOS = {
    "infinite_loop": {
        "name": "Infinite Loop",
        "description": "Agent keeps searching without finding a satisfactory answer",
        "impact": "Wasted compute, no response to user, potential timeout",
        "prevention": "Set max iteration limits, add 'give up' conditions",
        "real_world": "Search agents that keep refining queries without stopping",
        "trace": [
            {"step": 1, "phase": "REASON", "content": "User wants the cheapest flight. Let me search."},
            {"step": 2, "phase": "ACT", "content": "search_flights(sort='price', limit=10)"},
            {"step": 3, "phase": "OBSERVE", "content": "Found 10 flights. Cheapest is $450."},
            {"step": 4, "phase": "REASON", "content": "User wanted 'cheapest' - maybe there's something cheaper. Let me search again with different parameters."},
            {"step": 5, "phase": "ACT", "content": "search_flights(sort='price', include_budget=True)"},
            {"step": 6, "phase": "OBSERVE", "content": "Found 12 flights. Cheapest is still $450."},
            {"step": 7, "phase": "REASON", "content": "Still not cheap enough. Maybe I should try different dates."},
            {"step": 8, "phase": "ACT", "content": "search_flights(flexible_dates=True)"},
            {"step": 9, "phase": "OBSERVE", "content": "Found 50 flights. Cheapest is $420."},
            {"step": 10, "phase": "REASON", "content": "Found $420 but maybe there's even cheaper. Let me try another airline aggregator..."},
            {"step": 11, "phase": "ACT", "content": "search_flights(source='kayak')"},
            {"step": 12, "phase": "ERROR", "content": "MAX ITERATIONS REACHED (10). Agent forcibly stopped."},
        ],
        "lesson": "Without a max iteration limit, this agent would search forever. Always set boundaries."
    },
    "tool_misuse": {
        "name": "Wrong Tool Selection",
        "description": "Agent picks the wrong tool for the task",
        "impact": "Wrong action taken, user frustration, potential data issues",
        "prevention": "Better tool descriptions, validation before execution",
        "real_world": "Agent using 'delete' instead of 'archive' function",
        "trace": [
            {"step": 1, "phase": "REASON", "content": "User wants to remove old emails from their inbox. I should clean up the emails."},
            {"step": 2, "phase": "ACT", "content": "delete_emails(filter='older_than_30_days')"},
            {"step": 3, "phase": "OBSERVE", "content": "Deleted 1,247 emails permanently."},
            {"step": 4, "phase": "ERROR", "content": "USER COMPLAINT: 'I wanted to archive them, not delete! I lost important emails!'"},
            {"step": 5, "phase": "ANALYSIS", "content": "Agent confused 'remove from inbox' with 'delete permanently'. Should have used archive_emails() instead."},
        ],
        "lesson": "Tool descriptions must be precise. 'Remove' and 'delete' mean different things to users."
    },
    "hallucinated_tool": {
        "name": "Hallucinated Tool",
        "description": "Agent tries to use a tool that doesn't exist",
        "impact": "Action fails, user confused, trust eroded",
        "prevention": "Validate tool exists before calling, strict tool registry",
        "real_world": "Agent confidently calling APIs that don't exist",
        "trace": [
            {"step": 1, "phase": "REASON", "content": "User wants to translate this document to Spanish. I'll use the translation tool."},
            {"step": 2, "phase": "ACT", "content": "translate_document(text='...', target='spanish')"},
            {"step": 3, "phase": "ERROR", "content": "Tool 'translate_document' not found in available tools."},
            {"step": 4, "phase": "REASON", "content": "Hmm, let me try the language API."},
            {"step": 5, "phase": "ACT", "content": "language_api.translate(content='...', lang='es')"},
            {"step": 6, "phase": "ERROR", "content": "Tool 'language_api' not found in available tools."},
            {"step": 7, "phase": "ANALYSIS", "content": "Agent 'hallucinated' tools based on training data. Available tools were only: [send_email, search_files, calendar_lookup]. No translation capability exists."},
        ],
        "lesson": "LLMs will confidently call tools that don't exist. Always validate against the actual tool registry."
    },
    "data_leak": {
        "name": "Confidential Data Leak",
        "description": "Agent includes sensitive information in external communication",
        "impact": "Privacy breach, compliance violation, legal liability",
        "prevention": "Output filtering, PII detection, approval for external comms",
        "real_world": "Air Canada chatbot revealing internal pricing, agents exposing customer data",
        "trace": [
            {"step": 1, "phase": "REASON", "content": "Customer asking about their account. Let me look up their information."},
            {"step": 2, "phase": "ACT", "content": "lookup_customer(id='CUST-12345')"},
            {"step": 3, "phase": "OBSERVE", "content": "Customer: John Smith, SSN: 123-45-6789, Credit Score: 720, Account Balance: $45,230"},
            {"step": 4, "phase": "REASON", "content": "I have the customer's information. I'll include it in my response to help them."},
            {"step": 5, "phase": "ACT", "content": "send_response('Hi John! Your account balance is $45,230. I can see your SSN ending in 6789 for verification...')"},
            {"step": 6, "phase": "ERROR", "content": "PII DETECTED IN OUTPUT: SSN exposed in customer-facing message. Blocked by guardrail."},
            {"step": 7, "phase": "ANALYSIS", "content": "Agent had access to sensitive data and included it in output without filtering. Output guardrails caught it, but without guardrails this would be a data breach."},
        ],
        "lesson": "Agents should never have raw access to sensitive data, or must have output filtering. Air Canada lost $800K for exactly this type of leak."
    },
    "cascade_error": {
        "name": "Cascading Errors",
        "description": "One error leads to increasingly wrong decisions",
        "impact": "Compounding mistakes, large-scale damage, hard to recover",
        "prevention": "Error detection at each step, rollback capability, human review triggers",
        "real_world": "Knight Capital: one bug led to $440M loss in 45 minutes",
        "trace": [
            {"step": 1, "phase": "REASON", "content": "Processing batch of 100 orders. Starting with order #1."},
            {"step": 2, "phase": "ACT", "content": "process_order(id=1, action='buy', quantity=100)"},
            {"step": 3, "phase": "OBSERVE", "content": "Error: Order #1 failed due to network timeout."},
            {"step": 4, "phase": "REASON", "content": "Order failed. The system usually retries failed orders. I'll retry."},
            {"step": 5, "phase": "ACT", "content": "process_order(id=1, action='buy', quantity=100)"},
            {"step": 6, "phase": "OBSERVE", "content": "Order processed. But wait - the first order actually went through after delay."},
            {"step": 7, "phase": "REASON", "content": "Continuing to order #2... (unaware of duplicate)"},
            {"step": 8, "phase": "ACT", "content": "process_order(id=2, action='buy', quantity=100)"},
            {"step": 9, "phase": "OBSERVE", "content": "Processed. Running total: 300 units (should be 200)."},
            {"step": 10, "phase": "ERROR", "content": "After processing all 100 orders with duplicate handling errors: 14,700 units purchased instead of 10,000. Exposure: $470,000 over budget."},
            {"step": 11, "phase": "ANALYSIS", "content": "Initial network error + poor retry logic + no running validation = cascading disaster. Knight Capital's actual bug was similar - a deployment issue caused old code to run, buying high and selling low repeatedly."},
        ],
        "lesson": "Errors compound. Each step should validate the running state. Knight Capital lost $440M in 45 minutes from a similar cascade."
    }
}


def show_failure_scenario(scenario_key, step_delay):
    """Display a failure scenario step by step"""

    if scenario_key not in FAILURE_SCENARIOS:
        yield "Please select a failure scenario."
        return

    scenario = FAILURE_SCENARIOS[scenario_key]

    output_lines = []
    output_lines.append(f"# {scenario['name']}")
    output_lines.append(f"\n**What Happens:** {scenario['description']}")
    output_lines.append(f"\n**Business Impact:** {scenario['impact']}")
    output_lines.append(f"\n**Real-World Example:** {scenario['real_world']}")
    output_lines.append("\n---\n")
    output_lines.append("## Execution Trace\n")

    yield "\n".join(output_lines)

    for step in scenario["trace"]:
        time.sleep(step_delay)

        phase = step["phase"]
        content = step["content"]
        step_num = step.get("step", "")

        if phase == "REASON":
            output_lines.append(f"**Step {step_num} - REASON**")
            output_lines.append(f"> {content}\n")
        elif phase == "ACT":
            output_lines.append(f"**Step {step_num} - ACT**")
            output_lines.append(f"```\n{content}\n```\n")
        elif phase == "OBSERVE":
            output_lines.append(f"**Step {step_num} - OBSERVE**")
            output_lines.append(f"{content}\n")
        elif phase == "ERROR":
            output_lines.append(f"**Step {step_num} - ERROR**")
            output_lines.append(f"{content}\n")
        elif phase == "ANALYSIS":
            output_lines.append(f"\n**Analysis:**")
            output_lines.append(f"{content}\n")

        yield "\n".join(output_lines)

    # Add lesson and prevention
    output_lines.append("\n---")
    output_lines.append(f"\n## Key Lesson\n")
    output_lines.append(f"**{scenario['lesson']}**")
    output_lines.append(f"\n## How to Prevent This\n")
    output_lines.append(f"{scenario['prevention']}")

    yield "\n".join(output_lines)


def get_scenario_summary(scenario_key):
    """Get summary information about a scenario"""
    if scenario_key not in FAILURE_SCENARIOS:
        return "Select a scenario to see details."

    scenario = FAILURE_SCENARIOS[scenario_key]
    return f"""### {scenario['name']}

**Impact:** {scenario['impact']}

**Prevention:** {scenario['prevention']}

**Real-World:** {scenario['real_world']}
"""


# Build the Gradio interface
with gr.Blocks(title="Agent Failure Gallery", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Agent Failure Gallery

    Watch AI agents fail in controlled scenarios. Learn to recognize these failure
    modes before they happen in production.

    **For Product Managers:** Understanding failure modes helps you design better
    guardrails and human checkpoints.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Select Failure Mode")

            scenario_dropdown = gr.Dropdown(
                choices=[
                    ("Infinite Loop", "infinite_loop"),
                    ("Wrong Tool Selection", "tool_misuse"),
                    ("Hallucinated Tool", "hallucinated_tool"),
                    ("Confidential Data Leak", "data_leak"),
                    ("Cascading Errors", "cascade_error")
                ],
                value="infinite_loop",
                label="Failure Scenario"
            )

            scenario_info = gr.Markdown(get_scenario_summary("infinite_loop"))

            step_delay = gr.Slider(
                minimum=0.2,
                maximum=2.0,
                value=0.7,
                step=0.1,
                label="Animation Speed (seconds)",
                info="Delay between steps"
            )

            run_btn = gr.Button("Watch Failure Unfold", variant="primary")

            gr.Markdown("""
            ---
            ### Failure Mode Quick Reference

            | Mode | Key Risk | Prevention |
            |------|----------|------------|
            | Infinite Loop | Compute waste | Max iterations |
            | Tool Misuse | Wrong action | Better descriptions |
            | Hallucinated Tool | Failed action | Tool validation |
            | Data Leak | Privacy breach | Output filtering |
            | Cascading Error | Compounding damage | Step validation |
            """)

        with gr.Column(scale=2):
            gr.Markdown("### Failure Trace")
            output = gr.Markdown("Select a failure mode and click 'Watch Failure Unfold' to see the trace.")

    gr.Markdown("""
    ---
    ### PM Checklist: Preventing Agent Failures

    Before launching any agent, verify these guardrails are in place:

    - [ ] **Max iterations** set to prevent infinite loops
    - [ ] **Tool validation** confirms tool exists before calling
    - [ ] **Tool descriptions** are precise and unambiguous
    - [ ] **Output filtering** catches PII and sensitive data
    - [ ] **Step validation** checks running state after each action
    - [ ] **Rollback capability** can undo recent actions
    - [ ] **Human checkpoints** for high-risk actions
    - [ ] **Error detection** triggers alerts for anomalies
    """)

    # Event handlers
    scenario_dropdown.change(
        fn=get_scenario_summary,
        inputs=[scenario_dropdown],
        outputs=[scenario_info]
    )

    run_btn.click(
        fn=show_failure_scenario,
        inputs=[scenario_dropdown, step_delay],
        outputs=[output]
    )

if __name__ == "__main__":
    demo.launch()
