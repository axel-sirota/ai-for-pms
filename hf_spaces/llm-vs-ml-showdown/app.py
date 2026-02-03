"""
LLM vs Classical ML Showdown — AI for Product Managers
Pre-computed comparison of ML vs LLM across different task types.
"""

import gradio as gr
import plotly.graph_objects as go

# ── Pre-computed Task Results ─────────────────────────────────────────────────

TASKS = {
    "Customer Churn Prediction": {
        "description": "Predict which customers will cancel their subscription based on usage data, tenure, and billing info.",
        "data_type": "Structured (rows & columns)",
        "ml": {
            "accuracy": 0.91, "training_time": "2 hours", "inference_ms": 5,
            "cost_per_1k": 0.001, "explainability": 0.95,
            "setup_days": 14, "model": "Random Forest",
            "notes": "Feature importance shows top churn drivers. Runs in real-time. Scales to millions."
        },
        "llm": {
            "accuracy": 0.72, "training_time": "N/A (prompt only)", "inference_ms": 2000,
            "cost_per_1k": 5.00, "explainability": 0.40,
            "setup_days": 1, "model": "GPT-4",
            "notes": "Struggles with tabular patterns. Each prediction costs tokens. Not designed for this."
        },
        "winner": "Classical ML",
        "verdict": "Classical ML wins decisively. Structured data prediction is exactly what ML was built for — faster, cheaper, more accurate, and explainable. An LLM reading spreadsheet rows is like using a translator to do math."
    },
    "Fraud Detection": {
        "description": "Flag fraudulent transactions in real-time based on amount, location, time, and spending patterns.",
        "data_type": "Structured (transaction logs)",
        "ml": {
            "accuracy": 0.94, "training_time": "3 hours", "inference_ms": 3,
            "cost_per_1k": 0.001, "explainability": 0.90,
            "setup_days": 21, "model": "XGBoost",
            "notes": "Sub-10ms latency critical for real-time blocking. Feature importance for compliance."
        },
        "llm": {
            "accuracy": 0.68, "training_time": "N/A", "inference_ms": 3000,
            "cost_per_1k": 8.00, "explainability": 0.30,
            "setup_days": 1, "model": "Claude 3.5",
            "notes": "3-second latency is unacceptable for real-time fraud. Can't process millions of transactions affordably."
        },
        "winner": "Classical ML",
        "verdict": "Classical ML wins overwhelmingly. Fraud detection needs millisecond latency, explainability for regulators, and the ability to process millions of transactions cheaply. LLMs fail on all three."
    },
    "Customer Review Sentiment": {
        "description": "Classify customer reviews as positive, negative, or neutral to track product satisfaction.",
        "data_type": "Unstructured (free text)",
        "ml": {
            "accuracy": 0.78, "training_time": "4 hours", "inference_ms": 10,
            "cost_per_1k": 0.01, "explainability": 0.50,
            "setup_days": 30, "model": "TF-IDF + SVM",
            "notes": "Needs labeled training data. Misses sarcasm and nuance. Fast but limited understanding."
        },
        "llm": {
            "accuracy": 0.93, "training_time": "N/A (zero-shot)", "inference_ms": 800,
            "cost_per_1k": 2.00, "explainability": 0.70,
            "setup_days": 1, "model": "GPT-4o-mini",
            "notes": "Understands sarcasm, context, nuance. No training data needed. Can explain its reasoning."
        },
        "winner": "LLM",
        "verdict": "LLM wins. Text understanding is what language models were built for. The accuracy gap is significant, setup is instant, and the LLM catches nuances that keyword-based ML misses entirely."
    },
    "Support Ticket Routing": {
        "description": "Automatically route support tickets to the right team (billing, technical, account, etc.) based on ticket content.",
        "data_type": "Unstructured (text + categories)",
        "ml": {
            "accuracy": 0.82, "training_time": "6 hours", "inference_ms": 8,
            "cost_per_1k": 0.01, "explainability": 0.60,
            "setup_days": 45, "model": "BERT fine-tuned",
            "notes": "Needs 5,000+ labeled tickets for training. Struggles with new categories. Good for stable, well-defined routing."
        },
        "llm": {
            "accuracy": 0.89, "training_time": "N/A", "inference_ms": 1200,
            "cost_per_1k": 3.00, "explainability": 0.75,
            "setup_days": 2, "model": "Claude 3.5 Haiku",
            "notes": "Handles new categories instantly. Understands context and urgency. Can explain routing decisions to agents."
        },
        "winner": "LLM",
        "verdict": "LLM wins for most teams. Support categories change often, and LLMs adapt without retraining. The cost per ticket ($0.003) is negligible compared to the cost of misrouting. ML only wins if you have extremely high volume (1M+ tickets/month) and stable categories."
    },
}

# Dimensions for radar chart (normalized 0-1, higher = better)
def get_radar_scores(task_data):
    ml = task_data["ml"]
    llm = task_data["llm"]

    # Normalize: accuracy direct, speed inverse, cost inverse, explainability direct, setup inverse
    max_inference = max(ml["inference_ms"], llm["inference_ms"])
    max_cost = max(ml["cost_per_1k"], llm["cost_per_1k"])
    max_setup = max(ml["setup_days"], llm["setup_days"])

    ml_scores = [
        ml["accuracy"],
        1 - ml["inference_ms"] / (max_inference + 1),
        1 - ml["cost_per_1k"] / (max_cost + 0.01),
        ml["explainability"],
        1 - ml["setup_days"] / (max_setup + 1),
    ]
    llm_scores = [
        llm["accuracy"],
        1 - llm["inference_ms"] / (max_inference + 1),
        1 - llm["cost_per_1k"] / (max_cost + 0.01),
        llm["explainability"],
        1 - llm["setup_days"] / (max_setup + 1),
    ]
    return ml_scores, llm_scores


def compare(task_name):
    task = TASKS[task_name]
    ml = task["ml"]
    llm = task["llm"]

    # Comparison table
    table = f"""## {task_name}

**{task['description']}**
Data type: {task['data_type']}

| Dimension | Classical ML ({ml['model']}) | LLM ({llm['model']}) |
|-----------|---------------------------|---------------------|
| **Accuracy** | {ml['accuracy']:.0%} | {llm['accuracy']:.0%} |
| **Training Time** | {ml['training_time']} | {llm['training_time']} |
| **Inference Speed** | {ml['inference_ms']}ms | {llm['inference_ms']}ms |
| **Cost per 1,000** | ${ml['cost_per_1k']:.3f} | ${llm['cost_per_1k']:.2f} |
| **Explainability** | {ml['explainability']:.0%} | {llm['explainability']:.0%} |
| **Setup Time** | {ml['setup_days']} days | {llm['setup_days']} days |

**ML Notes:** {ml['notes']}

**LLM Notes:** {llm['notes']}
"""

    # Verdict
    winner_color = "#10b981" if task["winner"] == "Classical ML" else "#8b5cf6"
    verdict = f"""## Winner: {task['winner']}

{task['verdict']}
"""

    # Radar chart
    categories = ["Accuracy", "Speed", "Cost Efficiency", "Explainability", "Setup Speed"]
    ml_scores, llm_scores = get_radar_scores(task)

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=ml_scores + [ml_scores[0]],
        theta=categories + [categories[0]],
        fill="toself", name=f"ML ({ml['model']})",
        line_color="#3b82f6", fillcolor="rgba(59,130,246,0.15)"
    ))
    fig.add_trace(go.Scatterpolar(
        r=llm_scores + [llm_scores[0]],
        theta=categories + [categories[0]],
        fill="toself", name=f"LLM ({llm['model']})",
        line_color="#8b5cf6", fillcolor="rgba(139,92,246,0.15)"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=450, margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(x=0.5, y=-0.1, xanchor="center", orientation="h")
    )

    # Cost at scale
    scale_md = f"""## Cost at Scale (Monthly)

| Volume | ML Cost | LLM Cost | Savings with ML |
|--------|---------|----------|-----------------|
| 10,000 | ${ml['cost_per_1k'] * 10:,.2f} | ${llm['cost_per_1k'] * 10:,.2f} | ${(llm['cost_per_1k'] - ml['cost_per_1k']) * 10:,.2f} |
| 100,000 | ${ml['cost_per_1k'] * 100:,.2f} | ${llm['cost_per_1k'] * 100:,.2f} | ${(llm['cost_per_1k'] - ml['cost_per_1k']) * 100:,.2f} |
| 1,000,000 | ${ml['cost_per_1k'] * 1000:,.2f} | ${llm['cost_per_1k'] * 1000:,.2f} | ${(llm['cost_per_1k'] - ml['cost_per_1k']) * 1000:,.2f} |
"""

    return table, fig, verdict, scale_md


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="LLM vs ML Showdown", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# LLM vs Classical ML Showdown\n"
        "Same task, two approaches. See which tool wins on accuracy, speed, cost, and explainability.\n"
        "**Use the right tool for the job.**"
    )

    task_dd = gr.Dropdown(
        choices=list(TASKS.keys()),
        value="Customer Churn Prediction",
        label="Select Task"
    )

    comparison_md = gr.Markdown()
    radar = gr.Plot(label="Comparison")
    verdict_md = gr.Markdown()
    scale_md = gr.Markdown()

    task_dd.change(compare, [task_dd], [comparison_md, radar, verdict_md, scale_md])
    demo.load(compare, [task_dd], [comparison_md, radar, verdict_md, scale_md])

    gr.Markdown("---\n*AI for Product Managers*")


if __name__ == "__main__":
    demo.launch()
