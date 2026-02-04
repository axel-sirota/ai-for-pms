"""
A/B Test Simulator - Understand statistical significance for AI experiments
Helps PMs calculate sample sizes and interpret A/B test results
"""

import gradio as gr
import numpy as np
import plotly.graph_objects as go
from scipy import stats

np.random.seed(42)


def calculate_sample_size(baseline_rate, expected_lift, confidence_level, power):
    """Calculate required sample size for A/B test"""

    # Convert percentages to proportions
    p1 = baseline_rate / 100
    p2 = p1 * (1 + expected_lift / 100)

    # Z-scores for confidence and power
    alpha = 1 - confidence_level / 100
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power / 100)

    # Pooled proportion
    p_pooled = (p1 + p2) / 2

    # Sample size formula
    numerator = (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) +
                 z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    if denominator == 0:
        return float('inf')

    n = numerator / denominator
    return int(np.ceil(n))


def simulate_ab_test(baseline_rate, actual_lift, sample_size_per_group, num_simulations=1000):
    """Simulate A/B test results"""

    p_control = baseline_rate / 100
    p_treatment = p_control * (1 + actual_lift / 100)

    significant_count = 0
    p_values = []
    observed_lifts = []

    for _ in range(num_simulations):
        # Simulate outcomes
        control_successes = np.random.binomial(sample_size_per_group, p_control)
        treatment_successes = np.random.binomial(sample_size_per_group, p_treatment)

        # Calculate observed rates
        control_rate = control_successes / sample_size_per_group
        treatment_rate = treatment_successes / sample_size_per_group

        # Calculate observed lift
        if control_rate > 0:
            observed_lift = (treatment_rate - control_rate) / control_rate * 100
        else:
            observed_lift = 0
        observed_lifts.append(observed_lift)

        # Perform chi-square test
        contingency = [[control_successes, sample_size_per_group - control_successes],
                       [treatment_successes, sample_size_per_group - treatment_successes]]
        _, p_value, _, _ = stats.chi2_contingency(contingency)
        p_values.append(p_value)

        if p_value < 0.05:
            significant_count += 1

    return significant_count / num_simulations, p_values, observed_lifts


def run_analysis(baseline_rate, expected_lift, confidence_level, power, daily_traffic):
    """Run full A/B test analysis"""

    # Calculate required sample size
    sample_size = calculate_sample_size(baseline_rate, expected_lift, confidence_level, power)

    # Calculate days needed
    samples_per_day = daily_traffic / 2  # Split between A and B
    days_needed = int(np.ceil(sample_size / samples_per_day)) if samples_per_day > 0 else float('inf')

    # Create sample size vs lift chart
    lifts = [2, 5, 10, 15, 20, 25, 30]
    sample_sizes = [calculate_sample_size(baseline_rate, lift, confidence_level, power) for lift in lifts]

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=[f"{l}%" for l in lifts],
        y=sample_sizes,
        marker_color=['#dc2626' if s > 10000 else '#f59e0b' if s > 2000 else '#22c55e' for s in sample_sizes]
    ))
    fig1.add_hline(y=sample_size, line_dash="dash", line_color="#40B8A6",
                   annotation_text=f"Your target: {sample_size:,}")
    fig1.update_layout(
        title="Sample Size Required by Expected Lift",
        xaxis_title="Expected Lift",
        yaxis_title="Sample Size per Group",
        height=350
    )

    # Simulate what happens if we run the test
    power_achieved, p_values, observed_lifts = simulate_ab_test(
        baseline_rate, expected_lift, sample_size, num_simulations=500
    )

    # P-value distribution
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(
        x=p_values,
        nbinsx=30,
        marker_color='#40B8A6'
    ))
    fig2.add_vline(x=0.05, line_dash="dash", line_color="#dc2626",
                   annotation_text="p=0.05 threshold")
    fig2.update_layout(
        title="Distribution of P-Values (500 Simulations)",
        xaxis_title="P-Value",
        yaxis_title="Count",
        height=300
    )

    # Observed lift distribution
    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=observed_lifts,
        nbinsx=30,
        marker_color='#40B8A6'
    ))
    fig3.add_vline(x=expected_lift, line_dash="dash", line_color="#22c55e",
                   annotation_text=f"True lift: {expected_lift}%")
    fig3.update_layout(
        title="Distribution of Observed Lifts",
        xaxis_title="Observed Lift (%)",
        yaxis_title="Count",
        height=300
    )

    # Summary
    summary = f"""## A/B Test Analysis

### Required Sample Size
**{sample_size:,} samples per group** ({sample_size * 2:,} total)

### Time Estimate
At {daily_traffic:,} users/day: **~{days_needed} days**

### Configuration
- Baseline Rate: {baseline_rate}%
- Expected Lift: {expected_lift}%
- Confidence Level: {confidence_level}%
- Statistical Power: {power}%

### Simulation Results (500 runs)
- **Power Achieved:** {power_achieved*100:.1f}% of tests detected the effect
- Median Observed Lift: {np.median(observed_lifts):.1f}%
- Lift Range (95%): {np.percentile(observed_lifts, 2.5):.1f}% to {np.percentile(observed_lifts, 97.5):.1f}%

### Interpretation
{"The test is well-powered and should reliably detect this effect size." if power_achieved > 0.75 else "Warning: The test may be underpowered. Consider running longer or targeting a larger effect size."}
"""

    return summary, fig1, fig2, fig3


def quick_check(control_rate, treatment_rate, control_n, treatment_n):
    """Quick significance check for existing results"""

    control_successes = int(control_rate / 100 * control_n)
    treatment_successes = int(treatment_rate / 100 * treatment_n)

    contingency = [[control_successes, control_n - control_successes],
                   [treatment_successes, treatment_n - treatment_successes]]

    _, p_value, _, _ = stats.chi2_contingency(contingency)

    observed_lift = (treatment_rate - control_rate) / control_rate * 100 if control_rate > 0 else 0

    if p_value < 0.01:
        result = "**Highly Significant** (p < 0.01)"
        color = "#22c55e"
    elif p_value < 0.05:
        result = "**Statistically Significant** (p < 0.05)"
        color = "#40B8A6"
    elif p_value < 0.1:
        result = "**Marginally Significant** (p < 0.1)"
        color = "#f59e0b"
    else:
        result = "**Not Statistically Significant** (p >= 0.1)"
        color = "#dc2626"

    summary = f"""## Results

**P-Value:** {p_value:.4f}
**Observed Lift:** {observed_lift:+.1f}%

### Conclusion
{result}

### What This Means
- There is a {"less than " + str(int(p_value*100)) + "%" if p_value < 0.05 else str(int(p_value*100)) + "%"} chance this result occurred by random chance
- {"You can be confident Treatment is better than Control" if p_value < 0.05 else "You cannot confidently conclude Treatment is better - the difference might be noise"}

### Recommendation
{"Consider rolling out Treatment" if p_value < 0.05 and observed_lift > 0 else "Keep Control or run a longer test" if p_value >= 0.05 else "Treatment appears worse than Control"}
"""

    return summary


# Build Gradio interface
with gr.Blocks(title="A/B Test Simulator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # A/B Test Simulator

    Calculate sample sizes, simulate A/B tests, and check statistical significance.

    **For Product Managers:** Understand when you have enough data to make a decision,
    and avoid the trap of calling tests too early.
    """)

    with gr.Tab("Plan a Test"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Test Parameters")

                baseline = gr.Slider(
                    minimum=1, maximum=50, value=10, step=1,
                    label="Baseline Success Rate (%)",
                    info="Current conversion/success rate"
                )

                lift = gr.Slider(
                    minimum=1, maximum=50, value=10, step=1,
                    label="Minimum Lift to Detect (%)",
                    info="Smallest improvement worth detecting"
                )

                confidence = gr.Slider(
                    minimum=80, maximum=99, value=95, step=1,
                    label="Confidence Level (%)",
                    info="95% is standard"
                )

                power = gr.Slider(
                    minimum=60, maximum=95, value=80, step=5,
                    label="Statistical Power (%)",
                    info="80% is standard"
                )

                traffic = gr.Slider(
                    minimum=100, maximum=100000, value=5000, step=100,
                    label="Daily Traffic",
                    info="Users per day in the test"
                )

                plan_btn = gr.Button("Calculate & Simulate", variant="primary")

            with gr.Column(scale=2):
                plan_summary = gr.Markdown()
                sample_chart = gr.Plot()
                pvalue_chart = gr.Plot()
                lift_chart = gr.Plot()

    with gr.Tab("Check Existing Results"):
        gr.Markdown("### Enter Your Test Results")

        with gr.Row():
            with gr.Column():
                control_rate_input = gr.Number(
                    value=10, label="Control Success Rate (%)"
                )
                control_n_input = gr.Number(
                    value=1000, label="Control Sample Size"
                )
            with gr.Column():
                treatment_rate_input = gr.Number(
                    value=12, label="Treatment Success Rate (%)"
                )
                treatment_n_input = gr.Number(
                    value=1000, label="Treatment Sample Size"
                )

        check_btn = gr.Button("Check Significance", variant="primary")
        check_result = gr.Markdown()

    gr.Markdown("""
    ---
    ### PM Guide to A/B Testing AI

    **Why AI A/B Testing is Different:**
    - AI outputs are **stochastic** (same input can give different outputs)
    - Quality is **subjective** (harder to measure than click rates)
    - **Harmful outputs** can hurt users, not just convert poorly

    **Rules of Thumb:**
    | Expected Lift | Typical Sample Size | Notes |
    |--------------|---------------------|-------|
    | 5% | 3,000+ per group | Very hard to detect |
    | 10% | ~800 per group | Standard test |
    | 20% | ~200 per group | Easy to detect |

    **Common Mistakes:**
    1. Calling the test too early (peeking)
    2. Not accounting for day-of-week effects
    3. Testing on a biased subset of users
    4. Ignoring practical significance (statistically significant but tiny lift)
    """)

    # Event handlers
    plan_btn.click(
        fn=run_analysis,
        inputs=[baseline, lift, confidence, power, traffic],
        outputs=[plan_summary, sample_chart, pvalue_chart, lift_chart]
    )

    check_btn.click(
        fn=quick_check,
        inputs=[control_rate_input, treatment_rate_input, control_n_input, treatment_n_input],
        outputs=[check_result]
    )

if __name__ == "__main__":
    demo.launch()
