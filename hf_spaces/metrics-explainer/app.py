"""
Metrics Explainer — AI for Product Managers
Interactive confusion matrix with $ cost of errors.
"""

import gradio as gr
import plotly.graph_objects as go
import numpy as np

# ── Pre-loaded Scenarios ──────────────────────────────────────────────────────

SCENARIOS = {
    "Custom": {"tp": 100, "fp": 20, "fn": 10, "tn": 870, "fp_cost": 50, "fn_cost": 5000, "tp_revenue": 0},
    "Fraud Detection": {"tp": 950, "fp": 407, "fn": 50, "tn": 98593, "fp_cost": 50, "fn_cost": 5000, "tp_revenue": 5000},
    "Cancer Screening": {"tp": 90, "fp": 150, "fn": 10, "tn": 9750, "fp_cost": 500, "fn_cost": 100000, "tp_revenue": 0},
    "Spam Filter": {"tp": 800, "fp": 5, "fn": 200, "tn": 9000, "fp_cost": 1000, "fn_cost": 0.10, "tp_revenue": 0},
    "Credit Approval": {"tp": 450, "fp": 50, "fn": 30, "tn": 470, "fp_cost": 500, "fn_cost": 5000, "tp_revenue": 200},
}


def load_scenario(name):
    s = SCENARIOS.get(name, SCENARIOS["Custom"])
    return s["tp"], s["fp"], s["fn"], s["tn"], s["fp_cost"], s["fn_cost"], s["tp_revenue"]


def calculate_metrics(tp, fp, fn, tn, fp_cost, fn_cost, tp_revenue):
    tp, fp, fn, tn = int(tp), int(fp), int(fn), int(tn)
    total = tp + fp + fn + tn

    # Metrics
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    # Business impact
    total_fp_cost = fp * fp_cost
    total_fn_cost = fn * fn_cost
    total_saved = tp * tp_revenue
    total_error_cost = total_fp_cost + total_fn_cost
    net_impact = total_saved - total_error_cost

    # Confusion matrix heatmap
    cm = np.array([[tp, fp], [fn, tn]])
    labels = [
        [f"TP: {tp}<br>Correctly caught", f"FP: {fp}<br>False alarm"],
        [f"FN: {fn}<br>Missed!", f"TN: {tn}<br>Correctly cleared"]
    ]
    colors = [[0.7, 0.2], [0.3, 0.6]]  # green-ish for TP/TN, red-ish for FP/FN

    fig = go.Figure(data=go.Heatmap(
        z=colors,
        text=[[labels[0][0], labels[0][1]], [labels[1][0], labels[1][1]]],
        texttemplate="%{text}",
        textfont={"size": 14},
        colorscale=[[0, "#fecaca"], [0.4, "#fed7aa"], [0.6, "#bbf7d0"], [1, "#bbf7d0"]],
        showscale=False,
        xgap=3, ygap=3
    ))
    fig.update_layout(
        title="Confusion Matrix",
        xaxis=dict(tickvals=[0, 1], ticktext=["Predicted Positive", "Predicted Negative"], side="top"),
        yaxis=dict(tickvals=[0, 1], ticktext=["Actually Positive", "Actually Negative"]),
        height=350, width=450,
        margin=dict(l=20, r=20, t=80, b=20)
    )

    # Metrics bar chart
    metric_names = ["Accuracy", "Precision", "Recall", "F1", "Specificity"]
    metric_vals = [accuracy, precision, recall, f1, specificity]
    colors_bar = ["#6b7280", "#3b82f6", "#10b981", "#8b5cf6", "#f59e0b"]

    fig_metrics = go.Figure(go.Bar(
        x=metric_names, y=metric_vals,
        marker_color=colors_bar,
        text=[f"{v:.1%}" for v in metric_vals],
        textposition="outside"
    ))
    fig_metrics.update_layout(
        title="Model Metrics",
        yaxis=dict(range=[0, 1.15], tickformat=".0%"),
        height=350,
        margin=dict(l=20, r=20, t=50, b=30)
    )

    # Recommendation
    if fn_cost > fp_cost * 10:
        rec = "**Optimize for RECALL** — missed cases cost far more than false alarms."
        rec_color = "#10b981"
    elif fp_cost > fn_cost * 10:
        rec = "**Optimize for PRECISION** — false alarms are the bigger cost."
        rec_color = "#3b82f6"
    else:
        rec = "**Optimize for F1** — both error types have similar costs."
        rec_color = "#8b5cf6"

    # Summary text
    summary = f"""## Metrics Summary

| Metric | Value |
|--------|-------|
| Accuracy | {accuracy:.1%} |
| **Precision** | **{precision:.1%}** |
| **Recall** | **{recall:.1%}** |
| **F1 Score** | **{f1:.1%}** |
| Specificity | {specificity:.1%} |

## Business Impact

| Item | Amount |
|------|--------|
| False Positive Cost | {fp} x ${fp_cost:,.0f} = **${total_fp_cost:,.0f}** |
| False Negative Cost | {fn} x ${fn_cost:,.0f} = **${total_fn_cost:,.0f}** |
| Total Error Cost | **${total_error_cost:,.0f}** |
| Value Captured (TP) | {tp} x ${tp_revenue:,.0f} = **${total_saved:,.0f}** |
| **Net Impact** | **${net_impact:,.0f}** |

## Recommendation

{rec}
"""
    return fig, fig_metrics, summary


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Metrics Explainer", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Metrics Explainer\n"
        "Adjust the confusion matrix and costs to see how metrics and business impact change.\n"
        "**Every metric is a business decision.**"
    )

    scenario_dd = gr.Dropdown(
        choices=list(SCENARIOS.keys()),
        value="Fraud Detection",
        label="Load Scenario"
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Confusion Matrix Counts")
            tp = gr.Slider(0, 5000, value=950, step=1, label="True Positives (correctly caught)")
            fp = gr.Slider(0, 5000, value=407, step=1, label="False Positives (false alarms)")
            fn = gr.Slider(0, 5000, value=50, step=1, label="False Negatives (missed!)")
            tn = gr.Slider(0, 100000, value=98593, step=1, label="True Negatives (correctly cleared)")

        with gr.Column():
            gr.Markdown("### Business Costs ($)")
            fp_cost = gr.Number(value=50, label="Cost per False Positive ($)")
            fn_cost = gr.Number(value=5000, label="Cost per False Negative ($)")
            tp_revenue = gr.Number(value=5000, label="Revenue per True Positive ($)")

    calc_btn = gr.Button("Calculate", variant="primary")

    with gr.Row():
        cm_plot = gr.Plot(label="Confusion Matrix")
        metrics_plot = gr.Plot(label="Metrics")

    summary_md = gr.Markdown()

    # Wire events
    scenario_dd.change(load_scenario, [scenario_dd], [tp, fp, fn, tn, fp_cost, fn_cost, tp_revenue])

    inputs = [tp, fp, fn, tn, fp_cost, fn_cost, tp_revenue]
    outputs = [cm_plot, metrics_plot, summary_md]

    calc_btn.click(calculate_metrics, inputs, outputs)

    # Auto-calculate on load
    demo.load(calculate_metrics, inputs, outputs)

    gr.Markdown("---\n*AI for Product Managers*")


if __name__ == "__main__":
    demo.launch()
