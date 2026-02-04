"""
Human-in-the-Loop Designer - Configure approval workflows for agent systems
Helps PMs design appropriate checkpoints and see tradeoffs
"""

import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Action types and their default risk profiles
ACTION_PROFILES = {
    "send_email": {"base_risk": 30, "reversible": False, "category": "Communication"},
    "schedule_meeting": {"base_risk": 20, "reversible": True, "category": "Calendar"},
    "make_purchase": {"base_risk": 80, "reversible": False, "category": "Financial"},
    "delete_data": {"base_risk": 95, "reversible": False, "category": "Data"},
    "update_record": {"base_risk": 40, "reversible": True, "category": "Data"},
    "create_ticket": {"base_risk": 15, "reversible": True, "category": "Support"},
    "send_notification": {"base_risk": 25, "reversible": False, "category": "Communication"},
    "process_refund": {"base_risk": 70, "reversible": False, "category": "Financial"},
    "escalate_to_human": {"base_risk": 5, "reversible": True, "category": "Support"},
    "archive_file": {"base_risk": 35, "reversible": True, "category": "Data"},
}


def calculate_checkpoint_recommendations(
    actions_requiring_approval,
    dollar_threshold,
    confidence_threshold,
    risk_tolerance
):
    """Calculate which actions need checkpoints based on configuration"""

    results = []

    for action, profile in ACTION_PROFILES.items():
        base_risk = profile["base_risk"]
        reversible = profile["reversible"]
        category = profile["category"]

        # Calculate adjusted risk
        adjusted_risk = base_risk

        # If explicitly requiring approval, set checkpoint
        requires_approval = action in actions_requiring_approval

        # Determine checkpoint type
        if requires_approval or adjusted_risk > (100 - risk_tolerance):
            checkpoint = "Pre-Approval Required"
            friction = "High"
        elif reversible and adjusted_risk < 30:
            checkpoint = "Auto-Approve + Log"
            friction = "Low"
        elif reversible:
            checkpoint = "Auto-Approve + Undo Option"
            friction = "Low"
        elif adjusted_risk > 50:
            checkpoint = "Confidence-Based"
            friction = "Medium"
        else:
            checkpoint = "Post-Action Review"
            friction = "Medium"

        results.append({
            "Action": action.replace("_", " ").title(),
            "Category": category,
            "Base Risk": base_risk,
            "Reversible": "Yes" if reversible else "No",
            "Checkpoint": checkpoint,
            "Friction": friction
        })

    return pd.DataFrame(results)


def create_friction_risk_chart(df):
    """Create a scatter plot showing friction vs risk tradeoff"""

    friction_map = {"Low": 1, "Medium": 2, "High": 3}
    df["Friction_Numeric"] = df["Friction"].map(friction_map)

    fig = go.Figure()

    # Color by checkpoint type
    colors = {
        "Pre-Approval Required": "#dc2626",
        "Confidence-Based": "#f59e0b",
        "Post-Action Review": "#40B8A6",
        "Auto-Approve + Undo Option": "#059669",
        "Auto-Approve + Log": "#22c55e"
    }

    for checkpoint_type in df["Checkpoint"].unique():
        subset = df[df["Checkpoint"] == checkpoint_type]
        fig.add_trace(go.Scatter(
            x=subset["Base Risk"],
            y=subset["Friction_Numeric"],
            mode="markers+text",
            name=checkpoint_type,
            text=subset["Action"],
            textposition="top center",
            marker=dict(
                size=12,
                color=colors.get(checkpoint_type, "#666")
            ),
            hovertemplate="<b>%{text}</b><br>Risk: %{x}<br>Friction: %{y}<extra></extra>"
        ))

    fig.update_layout(
        title="Friction vs Risk Tradeoff by Action",
        xaxis_title="Risk Score (0-100)",
        yaxis_title="User Friction",
        yaxis=dict(
            tickmode="array",
            tickvals=[1, 2, 3],
            ticktext=["Low", "Medium", "High"]
        ),
        legend_title="Checkpoint Type",
        height=500,
        template="plotly_white"
    )

    # Add quadrant annotations
    fig.add_annotation(x=25, y=1.2, text="Sweet Spot", showarrow=False, font=dict(color="green"))
    fig.add_annotation(x=75, y=2.8, text="Necessary Friction", showarrow=False, font=dict(color="red"))

    return fig


def create_workflow_summary(df, dollar_threshold, confidence_threshold):
    """Create a summary of the workflow configuration"""

    auto_approve = len(df[df["Checkpoint"].str.contains("Auto")])
    needs_review = len(df[~df["Checkpoint"].str.contains("Auto")])
    high_risk = len(df[df["Base Risk"] > 70])

    summary = f"""
## Workflow Configuration Summary

### Approval Distribution
- **Auto-Approved Actions:** {auto_approve}
- **Actions Requiring Review:** {needs_review}
- **High-Risk Actions (>70):** {high_risk}

### Thresholds
- **Dollar Threshold:** ${dollar_threshold:,} (purchases above this require approval)
- **Confidence Threshold:** {confidence_threshold}% (below this, ask human)

### Estimated Impact
- **Speed:** {"Fast" if auto_approve > needs_review else "Moderate" if auto_approve > 3 else "Slow"}
- **Safety:** {"High" if needs_review > auto_approve else "Moderate"}
- **User Experience:** {"Smooth" if auto_approve > 5 else "Some interruptions"}

### Recommendations
"""

    if high_risk > 0 and auto_approve > high_risk:
        summary += "- Consider tightening controls on high-risk actions\n"
    if needs_review > 7:
        summary += "- High friction may cause user fatigue - consider confidence-based approvals\n"
    if auto_approve > 8:
        summary += "- Very permissive - ensure logging and monitoring are robust\n"

    return summary


def simulate_tasks(df, num_tasks):
    """Simulate a batch of tasks and show approval distribution"""

    np.random.seed(42)

    results = {
        "Auto-Approved": 0,
        "Confidence-Based": 0,
        "Human Approved": 0,
        "Blocked": 0
    }

    for _ in range(num_tasks):
        # Pick a random action
        action_row = df.sample(1).iloc[0]
        checkpoint = action_row["Checkpoint"]

        # Simulate confidence
        confidence = np.random.randint(60, 100)

        if "Auto" in checkpoint:
            results["Auto-Approved"] += 1
        elif "Confidence" in checkpoint:
            if confidence > 80:
                results["Auto-Approved"] += 1
            else:
                results["Human Approved"] += 1
        elif "Pre-Approval" in checkpoint:
            if np.random.random() > 0.1:  # 90% approval rate
                results["Human Approved"] += 1
            else:
                results["Blocked"] += 1
        else:
            results["Auto-Approved"] += 1

    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=list(results.keys()),
        values=list(results.values()),
        marker_colors=["#22c55e", "#f59e0b", "#40B8A6", "#dc2626"],
        hole=0.4
    )])

    fig.update_layout(
        title=f"Simulated Task Distribution ({num_tasks} tasks)",
        height=400
    )

    return fig


def update_all(actions, dollar_threshold, confidence_threshold, risk_tolerance, num_tasks):
    """Update all outputs based on configuration"""

    df = calculate_checkpoint_recommendations(
        actions, dollar_threshold, confidence_threshold, risk_tolerance
    )

    chart = create_friction_risk_chart(df)
    summary = create_workflow_summary(df, dollar_threshold, confidence_threshold)
    simulation = simulate_tasks(df, num_tasks)

    return df, chart, summary, simulation


# Build the Gradio interface
with gr.Blocks(title="Human-in-the-Loop Designer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Human-in-the-Loop Designer

    Configure approval workflows for your AI agent and see the tradeoffs between
    safety and user friction.

    **For Product Managers:** This tool helps you design checkpoints that balance
    risk management with user experience.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Configuration")

            actions_checkbox = gr.CheckboxGroup(
                choices=[
                    ("Send Email", "send_email"),
                    ("Schedule Meeting", "schedule_meeting"),
                    ("Make Purchase", "make_purchase"),
                    ("Delete Data", "delete_data"),
                    ("Update Record", "update_record"),
                    ("Create Ticket", "create_ticket"),
                    ("Process Refund", "process_refund"),
                ],
                value=["make_purchase", "delete_data", "process_refund"],
                label="Actions Requiring Manual Approval"
            )

            dollar_threshold = gr.Slider(
                minimum=0,
                maximum=10000,
                value=500,
                step=100,
                label="Auto-Approval Dollar Threshold",
                info="Purchases below this are auto-approved"
            )

            confidence_threshold = gr.Slider(
                minimum=50,
                maximum=100,
                value=80,
                step=5,
                label="Confidence Threshold (%)",
                info="Below this, ask for human review"
            )

            risk_tolerance = gr.Slider(
                minimum=10,
                maximum=90,
                value=50,
                step=10,
                label="Risk Tolerance",
                info="Higher = more permissive"
            )

            num_tasks = gr.Slider(
                minimum=10,
                maximum=100,
                value=50,
                step=10,
                label="Tasks to Simulate"
            )

            update_btn = gr.Button("Update Configuration", variant="primary")

        with gr.Column(scale=2):
            with gr.Tab("Checkpoint Matrix"):
                checkpoint_table = gr.DataFrame(
                    label="Action Checkpoint Configuration"
                )

            with gr.Tab("Risk vs Friction"):
                friction_chart = gr.Plot(label="Friction vs Risk Tradeoff")

            with gr.Tab("Task Simulation"):
                simulation_chart = gr.Plot(label="Simulated Task Distribution")

            with gr.Tab("Summary"):
                summary_md = gr.Markdown()

    gr.Markdown("""
    ---
    ### Key PM Decisions

    1. **Which actions absolutely require approval?** Start conservative, loosen based on performance.
    2. **What's your dollar threshold?** Common values: $100, $500, $1000
    3. **How confident must the AI be?** 80% is typical; regulated industries use 95%+
    4. **What's your risk tolerance?** Startups often higher, enterprises lower

    ### The Tradeoff
    - **More checkpoints** = Safer but slower, higher friction
    - **Fewer checkpoints** = Faster but riskier, requires better monitoring

    **Best Practice:** Start with more checkpoints (Level 0-1), reduce as system proves itself.
    """)

    # Initialize with defaults
    demo.load(
        fn=update_all,
        inputs=[actions_checkbox, dollar_threshold, confidence_threshold, risk_tolerance, num_tasks],
        outputs=[checkpoint_table, friction_chart, summary_md, simulation_chart]
    )

    # Update on button click
    update_btn.click(
        fn=update_all,
        inputs=[actions_checkbox, dollar_threshold, confidence_threshold, risk_tolerance, num_tasks],
        outputs=[checkpoint_table, friction_chart, summary_md, simulation_chart]
    )

if __name__ == "__main__":
    demo.launch()
