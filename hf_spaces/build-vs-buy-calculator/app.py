"""Build vs Buy Calculator - 12-month TCO comparison with risk matrix.
No API keys needed - pure calculation logic.
"""
import gradio as gr

USE_CASES = [
    "Customer support chatbot",
    "Document processing / extraction",
    "Content generation",
    "Search / recommendation",
    "Fraud detection",
    "Demand forecasting",
    "Code assistant",
    "Data analysis / reporting",
    "Other"
]

SENSITIVITY_OPTIONS = ["Low (public data)", "Medium (internal business data)", "High (PII, PHI, financial)"]
SCALE_OPTIONS = ["Small (<1K queries/day)", "Medium (1K-50K/day)", "Large (50K-500K/day)", "Enterprise (500K+/day)"]


def calculate_tco(team_size, ml_expertise, timeline_pressure, use_case, sensitivity, scale,
                  need_explainability, need_on_prem, need_custom_training):

    # ---- Cost Estimates ----
    # API approach costs
    api_setup_cost = 5_000
    if scale == SCALE_OPTIONS[0]:
        api_monthly_compute = 500
    elif scale == SCALE_OPTIONS[1]:
        api_monthly_compute = 5_000
    elif scale == SCALE_OPTIONS[2]:
        api_monthly_compute = 25_000
    else:
        api_monthly_compute = 100_000

    api_monthly_eng = 15_000  # 1 engineer part-time
    api_12mo = api_setup_cost + (api_monthly_compute + api_monthly_eng) * 12

    # Fine-tune approach
    ft_setup_cost = 30_000 + (10_000 if need_custom_training else 0)
    ft_monthly_compute = api_monthly_compute * 0.7  # slightly cheaper per query after fine-tuning
    ft_monthly_eng = 25_000  # more engineering time
    ft_12mo = ft_setup_cost + (ft_monthly_compute + ft_monthly_eng) * 12

    # Build from scratch
    build_setup_cost = 150_000
    if need_on_prem:
        build_setup_cost += 100_000
    build_monthly_infra = api_monthly_compute * 0.4  # cheaper compute long term
    build_monthly_team = team_size * 12_000  # average cost per ML team member/month
    build_12mo = build_setup_cost + (build_monthly_infra + build_monthly_team) * 12

    # ---- Risk Scoring (1-5, lower is better) ----
    api_risk = 1.5
    ft_risk = 2.5
    build_risk = 4.0

    if sensitivity == SENSITIVITY_OPTIONS[2]:
        api_risk += 1.5  # data leaving your infra
        ft_risk += 1.0
        build_risk -= 0.5  # you control everything
    if need_on_prem:
        api_risk += 2.0  # can't do on-prem with most APIs
        ft_risk += 1.0
    if timeline_pressure >= 4:
        build_risk += 1.0  # building under time pressure = disaster
    if ml_expertise <= 2:
        build_risk += 1.5
        ft_risk += 0.5
    if need_explainability:
        api_risk += 0.5
        build_risk -= 0.5  # full control over explainability

    api_risk = min(5, max(1, api_risk))
    ft_risk = min(5, max(1, ft_risk))
    build_risk = min(5, max(1, build_risk))

    # ---- Time to Production ----
    api_time = "2-4 weeks"
    ft_time = "1-3 months"
    build_time = f"{max(4, 12 - ml_expertise)}-{max(8, 18 - ml_expertise)} months"

    # ---- Team Requirements ----
    api_team = "PM + 1 engineer"
    ft_team = "PM + 1-2 engineers + data scientist (part-time)"
    build_team = f"PM + {max(2, team_size)} engineers + {max(1, team_size // 2)} data scientists + MLOps"

    # ---- Recommendation ----
    scores = {
        "API (Buy)": (1 / max(api_12mo, 1)) * 1e6 * (6 - api_risk),
        "Fine-Tune": (1 / max(ft_12mo, 1)) * 1e6 * (6 - ft_risk),
        "Build": (1 / max(build_12mo, 1)) * 1e6 * (6 - build_risk)
    }

    # Override: if on-prem required, API is not viable
    if need_on_prem:
        scores["API (Buy)"] *= 0.1

    winner = max(scores, key=scores.get)
    rec_text = f"## Recommendation: **{winner}**\n\n"

    if winner == "API (Buy)":
        rec_text += "Start with an API. Fastest time to value, lowest risk. Only upgrade if measurable quality gaps exist."
    elif winner == "Fine-Tune":
        rec_text += "Fine-tune an existing model. Good balance of control and speed. Requires some ML expertise and training data."
    else:
        rec_text += "Building may be justified given your constraints. But prototype with an API first to validate the use case."

    # ---- Format TCO Table ----
    tco_text = f"""## 12-Month Total Cost of Ownership

| Factor | API (Buy) | Fine-Tune | Build |
|--------|-----------|-----------|-------|
| **Setup Cost** | ${api_setup_cost:,} | ${ft_setup_cost:,} | ${build_setup_cost:,} |
| **Monthly Compute** | ${api_monthly_compute:,} | ${ft_monthly_compute:,.0f} | ${build_monthly_infra:,.0f} |
| **Monthly Team** | ${api_monthly_eng:,} | ${ft_monthly_eng:,} | ${build_monthly_team:,} |
| **12-Month TCO** | **${api_12mo:,}** | **${ft_12mo:,.0f}** | **${build_12mo:,.0f}** |
| **Time to Production** | {api_time} | {ft_time} | {build_time} |
| **Team Needed** | {api_team} | {ft_team} | {build_team} |
"""

    # ---- Risk Matrix ----
    def risk_bar(score):
        filled = round(score)
        return ("🟥" * filled) + ("⬜" * (5 - filled)) + f" ({score:.1f}/5)"

    risk_text = f"""## Risk Assessment

| Risk Factor | API (Buy) | Fine-Tune | Build |
|-------------|-----------|-----------|-------|
| **Overall Risk** | {risk_bar(api_risk)} | {risk_bar(ft_risk)} | {risk_bar(build_risk)} |
| **Data Privacy** | {"🟥🟥🟥" if sensitivity == SENSITIVITY_OPTIONS[2] else "🟩"} | {"🟨" if sensitivity == SENSITIVITY_OPTIONS[2] else "🟩"} | 🟩 Full control |
| **Vendor Lock-in** | 🟨 Medium | 🟨 Medium | 🟩 None |
| **Maintenance** | 🟩 Provider handles | 🟨 Retraining needed | 🟥 Full responsibility |
| **Scaling** | 🟩 Automatic | 🟩 Automatic | 🟥 You manage |
"""

    return rec_text, tco_text, risk_text


with gr.Blocks(
    title="Build vs Buy Calculator",
    theme=gr.themes.Soft(primary_hue="blue")
) as demo:
    gr.Markdown(
        "# Build vs Buy vs API Calculator\n"
        "Input your project details to get a recommendation with 12-month TCO comparison and risk analysis.\n\n"
        "*Success rates: API/Buy = 67% | Build = 33% (MIT 2025)*"
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Team & Context")
            team_size = gr.Slider(1, 10, value=3, step=1, label="Available Team Size")
            ml_expertise = gr.Slider(1, 5, value=2, step=1,
                                     label="Team ML Expertise (1=none, 5=expert)")
            timeline_pressure = gr.Slider(1, 5, value=3, step=1,
                                          label="Timeline Pressure (1=relaxed, 5=ASAP)")

        with gr.Column(scale=1):
            gr.Markdown("### Project Details")
            use_case = gr.Dropdown(choices=USE_CASES, value=USE_CASES[0], label="Use Case Type")
            sensitivity = gr.Dropdown(choices=SENSITIVITY_OPTIONS, value=SENSITIVITY_OPTIONS[1],
                                      label="Data Sensitivity")
            scale = gr.Dropdown(choices=SCALE_OPTIONS, value=SCALE_OPTIONS[1], label="Expected Scale")

    with gr.Row():
        need_explain = gr.Checkbox(label="Explainability required (regulated industry)")
        need_onprem = gr.Checkbox(label="Must run on-premise (data can't leave infra)")
        need_custom = gr.Checkbox(label="Need custom training on proprietary data")

    submit_btn = gr.Button("Calculate TCO & Get Recommendation", variant="primary")

    rec_output = gr.Markdown(label="Recommendation")
    tco_output = gr.Markdown(label="TCO Comparison")
    risk_output = gr.Markdown(label="Risk Matrix")

    submit_btn.click(
        fn=calculate_tco,
        inputs=[team_size, ml_expertise, timeline_pressure, use_case, sensitivity, scale,
                need_explain, need_onprem, need_custom],
        outputs=[rec_output, tco_output, risk_output]
    )

    gr.Examples(
        examples=[
            [2, 1, 5, "Customer support chatbot", SENSITIVITY_OPTIONS[0], SCALE_OPTIONS[1], False, False, False],
            [5, 4, 2, "Fraud detection", SENSITIVITY_OPTIONS[2], SCALE_OPTIONS[3], True, True, True],
            [3, 2, 3, "Content generation", SENSITIVITY_OPTIONS[1], SCALE_OPTIONS[1], False, False, False],
        ],
        inputs=[team_size, ml_expertise, timeline_pressure, use_case, sensitivity, scale,
                need_explain, need_onprem, need_custom],
    )

if __name__ == "__main__":
    demo.launch()
