"""
Agent Workflow Builder - Visual agent workflow designer
Helps PMs understand how agents work by designing and simulating workflows
"""

import gradio as gr
import json
import time

# Simulated workflow execution traces
WORKFLOW_TEMPLATES = {
    "travel_booking": {
        "name": "Travel Booking Agent",
        "description": "Book flights based on user preferences",
        "tools": ["search_flights", "compare_prices", "book_flight", "send_confirmation"],
        "steps": [
            {"phase": "REASON", "content": "User wants a flight from NYC to LA under $500. I need to search for available flights."},
            {"phase": "ACT", "content": "search_flights(from='NYC', to='LA', max_price=500)", "tool": "search_flights"},
            {"phase": "OBSERVE", "content": "Found 3 flights: Delta $450, United $380, JetBlue $420"},
            {"phase": "REASON", "content": "United is the cheapest at $380. I should present options to the user for confirmation."},
            {"phase": "ACT", "content": "present_options([Delta $450, United $380, JetBlue $420])", "tool": "compare_prices"},
            {"phase": "OBSERVE", "content": "User selected United $380"},
            {"phase": "CHECKPOINT", "content": "HUMAN APPROVAL REQUIRED: Book United flight for $380?", "requires_approval": True},
            {"phase": "REASON", "content": "User approved. Proceeding with booking."},
            {"phase": "ACT", "content": "book_flight(airline='United', price=380)", "tool": "book_flight"},
            {"phase": "OBSERVE", "content": "Booking confirmed. Confirmation #UA12345"},
            {"phase": "ACT", "content": "send_confirmation(email='user@example.com', confirmation='UA12345')", "tool": "send_confirmation"},
            {"phase": "COMPLETE", "content": "Flight booked successfully. Confirmation sent to user."}
        ]
    },
    "expense_processing": {
        "name": "Expense Report Agent",
        "description": "Process and approve expense reports",
        "tools": ["extract_receipt", "categorize_expense", "check_policy", "submit_approval", "process_payment"],
        "steps": [
            {"phase": "REASON", "content": "New expense submitted. Need to extract data from the receipt image."},
            {"phase": "ACT", "content": "extract_receipt(image='receipt_001.jpg')", "tool": "extract_receipt"},
            {"phase": "OBSERVE", "content": "Extracted: Amount=$247.50, Vendor='Marriott', Date='2024-01-15'"},
            {"phase": "REASON", "content": "Receipt data extracted. Now categorize the expense."},
            {"phase": "ACT", "content": "categorize_expense(vendor='Marriott', amount=247.50)", "tool": "categorize_expense"},
            {"phase": "OBSERVE", "content": "Category: Travel - Lodging"},
            {"phase": "REASON", "content": "Expense categorized. Need to check against company policy."},
            {"phase": "ACT", "content": "check_policy(category='Travel - Lodging', amount=247.50)", "tool": "check_policy"},
            {"phase": "OBSERVE", "content": "Policy check: COMPLIANT. Hotel limit is $300/night."},
            {"phase": "REASON", "content": "Expense is compliant. Amount is $247.50 which is between $100-$500, requires manager approval."},
            {"phase": "CHECKPOINT", "content": "MANAGER APPROVAL REQUIRED: Approve $247.50 for Marriott lodging?", "requires_approval": True},
            {"phase": "ACT", "content": "process_payment(amount=247.50, employee_id='EMP001')", "tool": "process_payment"},
            {"phase": "COMPLETE", "content": "Expense approved and payment processed."}
        ]
    },
    "customer_service": {
        "name": "Customer Service Agent",
        "description": "Handle customer inquiries and resolve issues",
        "tools": ["lookup_customer", "search_knowledge_base", "create_ticket", "send_response", "escalate_to_human"],
        "steps": [
            {"phase": "REASON", "content": "Customer asking about order status. Need to look up their information."},
            {"phase": "ACT", "content": "lookup_customer(email='customer@example.com')", "tool": "lookup_customer"},
            {"phase": "OBSERVE", "content": "Customer found: John Doe, Order #12345, Status: Shipped"},
            {"phase": "REASON", "content": "Order is shipped. Let me get tracking information from knowledge base."},
            {"phase": "ACT", "content": "search_knowledge_base(query='tracking order 12345')", "tool": "search_knowledge_base"},
            {"phase": "OBSERVE", "content": "Tracking: UPS 1Z999AA10123456784, Expected delivery: Jan 20"},
            {"phase": "REASON", "content": "Have all information. This is a routine inquiry, can respond directly at Level 2."},
            {"phase": "ACT", "content": "send_response(message='Your order #12345 shipped via UPS...')", "tool": "send_response"},
            {"phase": "COMPLETE", "content": "Response sent to customer with tracking information."}
        ]
    },
    "research_assistant": {
        "name": "Research Assistant Agent",
        "description": "Research topics and compile reports",
        "tools": ["web_search", "summarize_article", "compile_report", "send_report"],
        "steps": [
            {"phase": "REASON", "content": "User wants a competitive analysis of AI chatbot providers. Starting web research."},
            {"phase": "ACT", "content": "web_search(query='enterprise AI chatbot providers 2024')", "tool": "web_search"},
            {"phase": "OBSERVE", "content": "Found 15 relevant articles from Gartner, Forrester, and tech news."},
            {"phase": "REASON", "content": "Good sources found. Need to summarize key findings."},
            {"phase": "ACT", "content": "summarize_article(url='gartner.com/chatbot-mq-2024')", "tool": "summarize_article"},
            {"phase": "OBSERVE", "content": "Summary: Top providers are Intercom, Zendesk, Drift. Key differentiators..."},
            {"phase": "ACT", "content": "summarize_article(url='forrester.com/conversational-ai')", "tool": "summarize_article"},
            {"phase": "OBSERVE", "content": "Summary: Enterprise focus on Salesforce Einstein, Microsoft Copilot..."},
            {"phase": "REASON", "content": "Have enough information. Compiling report."},
            {"phase": "ACT", "content": "compile_report(topic='AI Chatbot Competitive Analysis')", "tool": "compile_report"},
            {"phase": "OBSERVE", "content": "Report compiled: 5 pages, 3 comparison tables, executive summary"},
            {"phase": "CHECKPOINT", "content": "HUMAN REVIEW REQUIRED: Review report before sending?", "requires_approval": True},
            {"phase": "ACT", "content": "send_report(recipient='stakeholder@company.com')", "tool": "send_report"},
            {"phase": "COMPLETE", "content": "Research report compiled and sent."}
        ]
    }
}


def run_workflow_simulation(workflow_type, include_checkpoints, max_steps, step_delay):
    """Simulate running a workflow with step-by-step execution"""

    if workflow_type not in WORKFLOW_TEMPLATES:
        yield "Please select a workflow template."
        return

    workflow = WORKFLOW_TEMPLATES[workflow_type]
    steps = workflow["steps"]

    output_lines = []
    output_lines.append(f"# {workflow['name']}\n")
    output_lines.append(f"**Description:** {workflow['description']}\n")
    output_lines.append(f"**Available Tools:** {', '.join(workflow['tools'])}\n")
    output_lines.append("---\n")

    yield "\n".join(output_lines)

    step_count = 0
    for i, step in enumerate(steps):
        if step_count >= max_steps:
            output_lines.append(f"\n**MAX STEPS REACHED ({max_steps})**")
            output_lines.append("Agent stopped to prevent infinite loops.")
            yield "\n".join(output_lines)
            break

        # Skip checkpoints if disabled
        if step["phase"] == "CHECKPOINT" and not include_checkpoints:
            continue

        step_count += 1
        time.sleep(step_delay)

        # Format based on phase
        phase = step["phase"]
        content = step["content"]

        if phase == "REASON":
            output_lines.append(f"\n**Step {step_count} - REASON**")
            output_lines.append(f"> {content}\n")
        elif phase == "ACT":
            tool = step.get("tool", "unknown")
            output_lines.append(f"\n**Step {step_count} - ACT** (using `{tool}`)")
            output_lines.append(f"```\n{content}\n```\n")
        elif phase == "OBSERVE":
            output_lines.append(f"\n**Step {step_count} - OBSERVE**")
            output_lines.append(f"Result: {content}\n")
        elif phase == "CHECKPOINT":
            output_lines.append(f"\n**Step {step_count} - CHECKPOINT**")
            output_lines.append(f"**{content}**")
            output_lines.append("*[Simulating human approval...]*\n")
        elif phase == "COMPLETE":
            output_lines.append(f"\n---\n**WORKFLOW COMPLETE**")
            output_lines.append(f"{content}")

        yield "\n".join(output_lines)

    # Summary
    output_lines.append(f"\n\n---\n**Execution Summary:**")
    output_lines.append(f"- Total steps: {step_count}")
    output_lines.append(f"- Human checkpoints: {sum(1 for s in steps[:step_count] if s['phase'] == 'CHECKPOINT')}")
    output_lines.append(f"- Tools used: {len(set(s.get('tool', '') for s in steps if s.get('tool')))}")

    yield "\n".join(output_lines)


def get_workflow_info(workflow_type):
    """Get information about a workflow template"""
    if workflow_type not in WORKFLOW_TEMPLATES:
        return "Select a workflow to see details."

    workflow = WORKFLOW_TEMPLATES[workflow_type]

    info = f"""## {workflow['name']}

**Description:** {workflow['description']}

**Available Tools:**
{chr(10).join(f'- `{tool}`' for tool in workflow['tools'])}

**Total Steps:** {len(workflow['steps'])}

**Human Checkpoints:** {sum(1 for s in workflow['steps'] if s['phase'] == 'CHECKPOINT')}
"""
    return info


# Build the Gradio interface
with gr.Blocks(title="Agent Workflow Builder", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Agent Workflow Builder

    Design and simulate agent workflows to understand how AI agents reason, act, and observe.

    **For Product Managers:** This tool helps you understand the ReAct pattern and design
    appropriate human checkpoints for your agent systems.
    """)

    gr.Markdown(
        "> **PM Decision:** Agent workflows determine failure modes and cost. "
        "More steps = more points of failure but potentially higher capability. "
        "Design your workflows to match task complexity and acceptable risk."
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Configuration")

            workflow_dropdown = gr.Dropdown(
                choices=[
                    ("Travel Booking Agent", "travel_booking"),
                    ("Expense Processing Agent", "expense_processing"),
                    ("Customer Service Agent", "customer_service"),
                    ("Research Assistant Agent", "research_assistant")
                ],
                value="travel_booking",
                label="Workflow Template"
            )

            workflow_info = gr.Markdown(get_workflow_info("travel_booking"))

            include_checkpoints = gr.Checkbox(
                value=True,
                label="Include Human Checkpoints",
                info="Simulate human approval steps"
            )

            max_steps = gr.Slider(
                minimum=5,
                maximum=20,
                value=15,
                step=1,
                label="Max Steps",
                info="Prevent infinite loops"
            )

            step_delay = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=0.5,
                step=0.1,
                label="Step Delay (seconds)",
                info="Animation speed"
            )

            run_btn = gr.Button("Run Workflow Simulation", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("### Workflow Execution")
            output = gr.Markdown("Select a workflow and click 'Run' to see the simulation.")

    gr.Markdown("""
    ---
    ### PM Insights

    **Key Observations:**
    - Each workflow follows the **ReAct pattern**: Reason → Act → Observe → Repeat
    - **Human checkpoints** are critical for irreversible actions (bookings, payments)
    - **Max steps** prevents infinite loops when agents get stuck
    - Tools define what the agent **can** do; you define what it **should** do

    **Questions to Ask Your Engineering Team:**
    1. What happens when a tool call fails?
    2. How do we handle partial workflow completion?
    3. What logging do we have for debugging?
    4. How do we A/B test different checkpoint placements?
    """)

    # Event handlers
    workflow_dropdown.change(
        fn=get_workflow_info,
        inputs=[workflow_dropdown],
        outputs=[workflow_info]
    )

    run_btn.click(
        fn=run_workflow_simulation,
        inputs=[workflow_dropdown, include_checkpoints, max_steps, step_delay],
        outputs=[output]
    )

if __name__ == "__main__":
    demo.launch()
