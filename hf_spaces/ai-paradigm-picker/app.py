"""AI Paradigm Picker - Recommends Classical ML vs LLM vs Agent
No API keys needed - uses rule-based decision logic.
"""
import gradio as gr

INDUSTRIES = [
    "Finance", "Healthcare", "Retail / E-commerce", "SaaS / Technology",
    "Media / Content", "Manufacturing", "Education", "Government",
    "Logistics / Supply Chain", "Other"
]

DATA_OPTIONS = [
    "Lots of structured historical data (spreadsheets, databases)",
    "Some examples but not a large dataset",
    "Mostly text / unstructured data",
    "Very little data available"
]


def pick_paradigm(feature_desc, industry, data_avail, latency, explainability, needs_actions):
    if not feature_desc.strip():
        return "Please describe your product feature to get a recommendation.", "", "", "", ""

    # Scoring system
    ml_score = 0
    llm_score = 0
    agent_score = 0
    reasoning = []
    red_flags = []
    questions = []

    # Data availability
    if data_avail == DATA_OPTIONS[0]:
        ml_score += 3
        reasoning.append("Strong structured data available - Classical ML thrives here")
    elif data_avail == DATA_OPTIONS[1]:
        ml_score += 1
        llm_score += 2
        reasoning.append("Limited data favors LLMs (they need examples in prompt, not training data)")
    elif data_avail == DATA_OPTIONS[2]:
        llm_score += 3
        reasoning.append("Text/unstructured data is LLM territory")
    else:
        llm_score += 2
        reasoning.append("Very little data means LLMs with careful prompting are your best bet")
        red_flags.append("Low data availability increases risk - start with a very narrow use case")

    # Latency
    if latency <= 2:
        ml_score += 2
        reasoning.append("Real-time latency requirement favors Classical ML (ms inference) or cached LLM responses")
        if needs_actions:
            red_flags.append("Real-time + autonomous actions is a high-risk combination")
    elif latency <= 4:
        llm_score += 1
    else:
        agent_score += 1
        reasoning.append("Relaxed latency tolerance allows for multi-step agent workflows")

    # Explainability
    if explainability >= 4:
        ml_score += 2
        reasoning.append("High explainability requirement strongly favors Classical ML (feature importance, decision trees)")
        if industry in ["Finance", "Healthcare", "Government"]:
            red_flags.append(f"Regulated industry ({industry}) + high explainability = Classical ML is likely required for compliance")
    elif explainability >= 3:
        ml_score += 1
        llm_score += 0.5

    # Actions
    if needs_actions:
        agent_score += 3
        reasoning.append("Autonomous actions require an Agent architecture (tool use + decision loops)")
        questions.append("What actions will the system take? What's the blast radius if it acts incorrectly?")
        questions.append("What approval workflows are needed before actions execute?")
    else:
        llm_score += 1

    # Text-related keywords boost LLM
    text_keywords = ["summarize", "generate", "write", "draft", "translate", "classify text",
                     "chatbot", "customer support", "content", "email", "respond", "answer questions"]
    desc_lower = feature_desc.lower()
    for kw in text_keywords:
        if kw in desc_lower:
            llm_score += 1.5
            reasoning.append(f"Text-oriented task ('{kw}') aligns with LLM capabilities")
            break

    # Prediction keywords boost ML
    pred_keywords = ["predict", "forecast", "churn", "fraud", "score", "rank",
                     "recommend", "segment", "classify", "detect anomal"]
    for kw in pred_keywords:
        if kw in desc_lower:
            ml_score += 1.5
            reasoning.append(f"Prediction task ('{kw}') aligns with Classical ML")
            break

    # Multi-step keywords boost Agent
    agent_keywords = ["automate", "workflow", "multi-step", "research", "book",
                      "process", "end-to-end", "coordinate", "orchestrate"]
    for kw in agent_keywords:
        if kw in desc_lower:
            agent_score += 1.5
            reasoning.append(f"Multi-step task ('{kw}') aligns with Agent architecture")
            break

    # Determine winner
    scores = {"Classical ML": ml_score, "LLM": llm_score, "Agent": agent_score}
    winner = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    confidence = scores[winner] / total

    # Check for hybrid
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_scores[0][1] - sorted_scores[1][1] < 1.5:
        recommendation = f"**Hybrid: {sorted_scores[0][0]} + {sorted_scores[1][0]}**"
        reasoning.append(f"Scores are close - consider combining {sorted_scores[0][0]} and {sorted_scores[1][0]}")
    else:
        recommendation = f"**{winner}**"

    # Confidence label
    if confidence > 0.6:
        conf_label = "High"
    elif confidence > 0.4:
        conf_label = "Medium"
    else:
        conf_label = "Low - consider hybrid approach"

    # Standard questions
    questions.extend([
        "What does 'success' look like? Define metrics before building.",
        "What's the timeline expectation? (Realistic: ML=3-6mo, LLM=weeks, Agent=months)",
        "What happens when the AI is wrong? What's the fallback?",
        "Do we have the data this approach needs?",
        "What's the budget for ongoing compute costs?"
    ])

    # Add industry-specific flags
    if industry in ["Finance", "Healthcare"]:
        red_flags.append(f"{industry}: Regulatory compliance will add 2-4 months to timeline")
        questions.append("Has legal/compliance reviewed the AI use case?")
    if industry == "Government":
        red_flags.append("Government: On-premise requirements may limit model choices")

    # Format outputs
    rec_text = f"## Recommendation: {recommendation}\n\n**Confidence:** {conf_label}\n\n"
    rec_text += f"**Scores:** Classical ML: {ml_score:.1f} | LLM: {llm_score:.1f} | Agent: {agent_score:.1f}"

    reasoning_text = "\n".join(f"- {r}" for r in reasoning)
    flags_text = "\n".join(f"- {r}" for r in red_flags) if red_flags else "No major red flags identified."
    questions_text = "\n".join(f"- {q}" for q in questions)

    # Similar products
    similar = {
        "Classical ML": "Stripe Radar (fraud), Netflix recommendations, Spotify Discover Weekly, Amazon demand forecasting",
        "LLM": "ChatGPT, GitHub Copilot, Notion AI, Grammarly, Intercom Fin",
        "Agent": "Klarna AI assistant, Cursor IDE, Devin (coding agent), Harvey (legal AI)"
    }
    similar_text = f"**Products using {winner}:** {similar.get(winner, 'Various')}"

    return rec_text, reasoning_text, similar_text, flags_text, questions_text


with gr.Blocks(
    title="AI Paradigm Picker",
    theme=gr.themes.Soft(primary_hue="blue")
) as demo:
    gr.Markdown(
        "# AI Paradigm Picker\n"
        "Describe your product feature and get a recommendation: **Classical ML**, **LLM**, or **Agent**.\n\n"
        "*No AI APIs needed - this uses rule-based decision logic to teach the framework.*"
    )

    with gr.Row():
        with gr.Column(scale=1):
            feature_input = gr.Textbox(
                label="Describe your product feature",
                placeholder="e.g., 'Predict which customers will churn next month based on usage patterns'",
                lines=3
            )
            industry_input = gr.Dropdown(
                choices=INDUSTRIES, label="Industry", value="SaaS / Technology"
            )
            data_input = gr.Dropdown(
                choices=DATA_OPTIONS, label="Data Availability", value=DATA_OPTIONS[0]
            )
            latency_input = gr.Slider(
                minimum=1, maximum=5, step=1, value=3,
                label="Acceptable Latency (1=real-time, 5=minutes OK)"
            )
            explain_input = gr.Slider(
                minimum=1, maximum=5, step=1, value=2,
                label="Explainability Requirement (1=low, 5=must explain every decision)"
            )
            actions_input = gr.Checkbox(label="Needs to take autonomous actions? (send emails, make purchases, etc.)")
            submit_btn = gr.Button("Get Recommendation", variant="primary")

        with gr.Column(scale=1):
            rec_output = gr.Markdown(label="Recommendation")
            reasoning_output = gr.Markdown(label="Reasoning")
            similar_output = gr.Markdown(label="Similar Products")

    with gr.Accordion("Red Flags & Risks", open=False):
        flags_output = gr.Markdown()

    with gr.Accordion("Questions to Ask Your Engineering Team", open=False):
        questions_output = gr.Markdown()

    submit_btn.click(
        fn=pick_paradigm,
        inputs=[feature_input, industry_input, data_input, latency_input, explain_input, actions_input],
        outputs=[rec_output, reasoning_output, similar_output, flags_output, questions_output]
    )

    # Pre-loaded examples
    gr.Examples(
        examples=[
            ["Predict which customers will churn next month based on usage data", "SaaS / Technology",
             DATA_OPTIONS[0], 3, 3, False],
            ["Generate personalized email responses to customer complaints", "Retail / E-commerce",
             DATA_OPTIONS[2], 3, 1, False],
            ["Automatically research competitors and compile a weekly report", "SaaS / Technology",
             DATA_OPTIONS[3], 5, 1, True],
            ["Detect fraudulent transactions in real-time", "Finance",
             DATA_OPTIONS[0], 1, 5, False],
            ["AI chatbot that books appointments and sends confirmations", "Healthcare",
             DATA_OPTIONS[1], 3, 2, True],
        ],
        inputs=[feature_input, industry_input, data_input, latency_input, explain_input, actions_input],
    )

if __name__ == "__main__":
    demo.launch()
