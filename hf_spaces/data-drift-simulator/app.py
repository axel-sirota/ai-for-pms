"""
Data Drift Simulator — AI for Product Managers
Watch model performance degrade as data distribution changes over time.
"""

import gradio as gr
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score


def generate_base_data(n=500, seed=42):
    """Generate synthetic fraud detection dataset."""
    rng = np.random.RandomState(seed)
    amount = rng.exponential(200, n)
    hour = rng.randint(0, 24, n)
    distance = rng.exponential(50, n)
    txn_count = rng.poisson(5, n)
    is_online = rng.choice([0, 1], n, p=[0.6, 0.4])

    logits = (-4 + 0.003 * amount + 0.1 * (hour < 5).astype(float) +
              0.01 * distance + 0.15 * txn_count + 0.5 * is_online +
              rng.normal(0, 0.5, n))
    labels = (1 / (1 + np.exp(-logits)) > 0.5).astype(int)

    X = np.column_stack([amount, hour, distance, txn_count, is_online])
    return X, labels


def apply_drift(X_base, month, drift_type, intensity, rng):
    """Apply drift to data for a given month."""
    X = X_base.copy()
    t = intensity / 100.0

    if drift_type == "Gradual":
        # Features slowly shift
        shift = t * month / 24.0
        X[:, 0] *= (1 + shift * 0.5)  # amounts increase
        X[:, 2] *= (1 + shift * 0.3)  # distances increase
        X[:, 3] = np.clip(X[:, 3] + shift * 2, 0, 20)  # more transactions

    elif drift_type == "Sudden":
        # Sharp change at month 6
        if month >= 6:
            X[:, 0] *= (1 + t * 0.8)  # amounts jump
            X[:, 2] *= (1 + t * 0.6)
            X[:, 4] = rng.choice([0, 1], len(X), p=[0.3, 0.7])  # more online

    elif drift_type == "Seasonal":
        # Cyclical pattern (holiday fraud spikes)
        seasonal_factor = t * 0.5 * np.sin(2 * np.pi * month / 12)
        X[:, 0] *= (1 + seasonal_factor)
        X[:, 3] = np.clip(X[:, 3] * (1 + seasonal_factor * 0.5), 0, 20)

    return X


def simulate_drift(drift_type, intensity, months):
    months = int(months)
    rng = np.random.RandomState(42)

    # Train baseline model on month 0
    X_train, y_train = generate_base_data(500, seed=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    # Simulate months
    accuracies, f1_scores, month_labels = [], [], []
    drift_amounts = []

    for m in range(months + 1):
        X_test, y_test = generate_base_data(200, seed=100 + m)
        X_drifted = apply_drift(X_test, m, drift_type, intensity, rng)
        preds = model.predict(X_drifted)

        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds, zero_division=0)
        accuracies.append(acc)
        f1_scores.append(f1)
        month_labels.append(m)

        # Measure drift magnitude
        mean_diff = np.mean(np.abs(X_drifted - X_test)) / (np.mean(np.abs(X_test)) + 1e-6)
        drift_amounts.append(mean_diff)

    # Find degradation point (first month where F1 drops > 10%)
    baseline_f1 = f1_scores[0]
    degradation_month = None
    for i, f in enumerate(f1_scores):
        if f < baseline_f1 * 0.9:
            degradation_month = i
            break

    # Performance chart
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=("Model Performance Over Time", "Data Drift Magnitude"),
        vertical_spacing=0.15
    )

    fig.add_trace(go.Scatter(
        x=month_labels, y=accuracies, name="Accuracy",
        line=dict(color="#3b82f6", width=2), mode="lines+markers"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=month_labels, y=f1_scores, name="F1 Score",
        line=dict(color="#10b981", width=2), mode="lines+markers"
    ), row=1, col=1)

    # Threshold line
    fig.add_hline(y=baseline_f1 * 0.9, line_dash="dash", line_color="red",
                  annotation_text="10% degradation threshold", row=1, col=1)

    if degradation_month is not None:
        fig.add_vline(x=degradation_month, line_dash="dot", line_color="red", row=1, col=1)

    fig.add_trace(go.Bar(
        x=month_labels, y=drift_amounts, name="Drift Magnitude",
        marker_color="#f59e0b", opacity=0.7
    ), row=2, col=1)

    fig.update_layout(height=600, margin=dict(l=20, r=20, t=40, b=20))
    fig.update_yaxes(title_text="Score", range=[0, 1.05], row=1, col=1)
    fig.update_yaxes(title_text="Drift", row=2, col=1)
    fig.update_xaxes(title_text="Month", row=2, col=1)

    # Summary
    final_acc = accuracies[-1]
    final_f1 = f1_scores[-1]
    acc_drop = (accuracies[0] - final_acc) / accuracies[0] * 100

    summary = f"""## Drift Analysis

| Metric | Month 0 | Month {months} | Change |
|--------|---------|----------|--------|
| Accuracy | {accuracies[0]:.1%} | {final_acc:.1%} | {'-' if acc_drop > 0 else '+'}{abs(acc_drop):.1f}% |
| F1 Score | {f1_scores[0]:.1%} | {final_f1:.1%} | {'-' if f1_scores[0] > final_f1 else '+'}{abs(f1_scores[0] - final_f1)*100:.1f}pp |

"""

    if degradation_month is not None:
        summary += f"**Alert:** Performance degraded past 10% threshold at **month {degradation_month}**.\n\n"
    else:
        summary += "**Status:** No significant degradation detected in this timeframe.\n\n"

    # Recommendations by drift type
    if drift_type == "Gradual":
        rec_interval = max(3, degradation_month - 1) if degradation_month else 6
        summary += f"**Recommendation:** For gradual drift, retrain every **{rec_interval} months**. Set up automated performance monitoring with alerts at 5% degradation."
    elif drift_type == "Sudden":
        summary += "**Recommendation:** For sudden drift, you need **real-time monitoring** and the ability to retrain within days. Set up alerts for sharp accuracy drops and have a retraining pipeline ready."
    else:
        summary += "**Recommendation:** For seasonal drift, retrain **before each peak season** using recent data. Consider maintaining separate models for peak vs off-peak periods."

    return fig, summary


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Data Drift Simulator", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Data Drift Simulator\n\n"
        "**PM Decision:** ML models degrade over time as real-world data changes. Use this "
        "to understand why you must require monitoring in every ML project and budget for "
        "retraining. A model that's 95% accurate at launch might drop to 70% in 6 months.\n\n"
        "Watch a fraud detection model's performance degrade as data distribution changes. "
        "**ML models aren't like software — they don't stay accurate forever.**"
    )

    with gr.Row():
        drift_type = gr.Dropdown(
            choices=["Gradual", "Sudden", "Seasonal"],
            value="Gradual",
            label="Drift Type"
        )
        intensity = gr.Slider(10, 100, value=50, step=5, label="Drift Intensity (%)")
        months = gr.Slider(6, 24, value=18, step=1, label="Simulation Length (months)")

    run_btn = gr.Button("Simulate Drift", variant="primary")

    chart = gr.Plot(label="Performance Over Time")
    analysis = gr.Markdown()

    run_btn.click(simulate_drift, [drift_type, intensity, months], [chart, analysis])
    demo.load(simulate_drift, [drift_type, intensity, months], [chart, analysis])

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** Always ask: 'What happens when the data changes? How will we know, "
        "and how often will we retrain?' Budget for monitoring from day one.\n\n"
        "*AI for Product Managers*"
    )


if __name__ == "__main__":
    demo.launch()
