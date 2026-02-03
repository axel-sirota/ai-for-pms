"""
Prompt Engineering Lab — AI for Product Managers
4 tabs showing how prompt patterns change output quality.
All responses pre-cached for demo mode.
"""

import gradio as gr
import os

# ── Tab 1: Zero-Shot vs Few-Shot ─────────────────────────────────────────────

ZERO_VS_FEW = {
    "Classify this customer email: 'I've been waiting 3 weeks for my order and nobody will help me!'": {
        "zero_shot": {
            "prompt": "Classify this customer email: 'I've been waiting 3 weeks for my order and nobody will help me!'",
            "response": "This is a complaint email.",
            "quality": "Vague — no category, no severity, no actionable classification."
        },
        "few_shot": {
            "prompt": """Classify customer emails into exactly one category and severity level.

Examples:
Email: "Thanks for the quick delivery!" → Category: Praise | Severity: None
Email: "My item arrived broken" → Category: Product Issue | Severity: High
Email: "How do I change my password?" → Category: Account Support | Severity: Low
Email: "I want to cancel everything, this is the worst service ever" → Category: Cancellation Risk | Severity: Critical

Now classify:
Email: "I've been waiting 3 weeks for my order and nobody will help me!\"""",
            "response": "Category: Shipping Issue | Severity: Critical\n\nReasoning: The customer mentions a 3-week wait (significantly delayed) and has already tried to get help without success, indicating high frustration and potential churn risk.",
            "quality": "Structured, actionable, includes severity. The few-shot examples taught the model the exact format and level of detail you want."
        }
    },
    "Summarize this product review: 'The battery life is amazing but the screen is too dim outdoors. Camera is decent for the price.'": {
        "zero_shot": {
            "prompt": "Summarize this product review: 'The battery life is amazing but the screen is too dim outdoors. Camera is decent for the price.'",
            "response": "The reviewer likes the battery life but finds the screen dim outdoors and thinks the camera is okay for the price.",
            "quality": "Just a paraphrase — not structured, not actionable for product decisions."
        },
        "few_shot": {
            "prompt": """Extract structured feedback from product reviews.

Examples:
Review: "Love the design, hate the charging speed" →
- Positive: Design (aesthetics)
- Negative: Charging speed (performance)
- Sentiment: Mixed

Review: "Everything works perfectly, best purchase this year" →
- Positive: Overall quality, reliability
- Negative: None
- Sentiment: Positive

Now extract:
Review: "The battery life is amazing but the screen is too dim outdoors. Camera is decent for the price.\"""",
            "response": "- Positive: Battery life (performance)\n- Negative: Screen brightness outdoors (display)\n- Neutral: Camera quality (value for money)\n- Sentiment: Mixed-positive\n- Product team signal: Display brightness is a prioritizable improvement",
            "quality": "Structured, categorized, actionable. The PM can immediately route this to the display team."
        }
    },
}

# ── Tab 2: System Prompt Impact ───────────────────────────────────────────────

SYSTEM_PROMPT_DEMOS = {
    "What are the risks of our new AI chatbot?": {
        "No system prompt": {
            "system": "(none)",
            "response": "AI chatbots carry several risks including hallucination (generating false information), bias in responses, privacy concerns with user data, potential for misuse, and lack of accountability. They may also provide incorrect advice in high-stakes domains like healthcare or finance.",
            "analysis": "Generic, academic answer. Not tailored to any specific context or audience."
        },
        "PM Persona": {
            "system": "You are a senior product manager at a SaaS company. Frame all answers in terms of business impact, user experience, and stakeholder communication. Be specific and actionable.",
            "response": "Key risks to present to stakeholders:\n\n1. **Hallucination risk** — The bot may confidently state incorrect policies (see: Air Canada, $800K). Mitigation: implement fact-checking layer against your knowledge base.\n\n2. **Brand damage** — One viral screenshot of a bad response costs more than the entire project (see: DPD chatbot). Mitigation: output filtering + human escalation for sensitive topics.\n\n3. **Scope creep** — Users will ask questions outside the bot's domain. Without boundaries, it'll answer anyway, badly. Mitigation: clear system prompt constraints + 'I don't know' fallback.\n\n4. **Cost overrun** — Token costs scale linearly with usage. A viral feature could 10x your API bill overnight. Mitigation: rate limiting + cost alerts.\n\n**Recommendation:** Soft-launch to 5% of traffic with human-in-the-loop review before full rollout.",
            "analysis": "Specific, actionable, business-framed. References real cases. Includes mitigations. This is what your VP wants to hear."
        },
        "Security Auditor Persona": {
            "system": "You are a cybersecurity auditor reviewing AI systems. Focus on attack vectors, compliance risks, and security controls. Reference industry frameworks (OWASP, NIST) where applicable.",
            "response": "**Security Risk Assessment: AI Chatbot**\n\n1. **Prompt Injection (OWASP LLM01)** — Users can override system instructions. Severity: HIGH. Control: Input sanitization + instruction hierarchy.\n\n2. **Sensitive Information Disclosure (OWASP LLM06)** — Model may leak training data, system prompts, or PII from context. Severity: HIGH. Control: Output filtering + PII detection.\n\n3. **Data Poisoning** — If the model learns from user interactions, adversarial inputs can degrade quality. Severity: MEDIUM. Control: Input validation + human review of training data.\n\n4. **Compliance** — GDPR Art. 22 requires disclosure of automated decision-making. If the chatbot makes decisions affecting users, you need transparency. Severity: HIGH.\n\n**Required before launch:** Penetration testing, privacy impact assessment, incident response plan.",
            "analysis": "Completely different framing — same question, but now focused on attack vectors and compliance. The system prompt transformed the response."
        }
    },
}

# ── Tab 3: Chain-of-Thought ───────────────────────────────────────────────────

COT_DEMOS = {
    "A customer bought 3 items at $50, $30, and $20. They have a 20% discount code and a $10 store credit. What's the final total?": {
        "without_cot": {
            "prompt": "A customer bought 3 items at $50, $30, and $20. They have a 20% discount code and a $10 store credit. What's the final total?",
            "response": "$62",
            "correct": False,
            "analysis": "Wrong answer, no reasoning shown. The model likely applied the discount incorrectly. Without step-by-step thinking, errors go undetected."
        },
        "with_cot": {
            "prompt": "A customer bought 3 items at $50, $30, and $20. They have a 20% discount code and a $10 store credit. What's the final total? Think step by step.",
            "response": "Let me work through this step by step:\n\n1. **Subtotal:** $50 + $30 + $20 = $100\n2. **Apply 20% discount:** $100 × 0.20 = $20 discount → $100 - $20 = $80\n3. **Apply $10 store credit:** $80 - $10 = $70\n\n**Final total: $70**",
            "correct": True,
            "analysis": "Correct answer with full reasoning. Each step is verifiable. If there's an error, you can see exactly where it happened. This is why CoT matters for any feature involving calculations."
        }
    },
    "Should we build a recommendation engine in-house or buy a third-party solution? Our team has 3 ML engineers, 6-month timeline, and 10M users.": {
        "without_cot": {
            "prompt": "Should we build or buy a recommendation engine? Team: 3 ML engineers, 6-month timeline, 10M users.",
            "response": "You should probably buy a third-party solution given your timeline constraints.",
            "correct": None,
            "analysis": "Unsupported opinion. No reasoning, no tradeoff analysis. A PM can't present this to stakeholders."
        },
        "with_cot": {
            "prompt": "Should we build or buy a recommendation engine? Team: 3 ML engineers, 6-month timeline, 10M users. Think step by step, considering cost, timeline, quality, and maintenance.",
            "response": "Let me analyze this systematically:\n\n**1. Build Assessment:**\n- 3 ML engineers × 6 months = 18 person-months\n- At $15K/month fully loaded = ~$270K development cost\n- Risk: 6 months is tight for production-quality recsys at 10M scale\n- Ongoing: Need to maintain, retrain, scale — permanent headcount\n\n**2. Buy Assessment:**\n- Solutions like Algolia Recommend, Amazon Personalize: $5K-20K/month\n- Time to integrate: 2-4 weeks\n- 12-month cost: $60K-240K\n- Ongoing: vendor manages scaling, updates, ML pipeline\n\n**3. Key Factors:**\n- Timeline: Buy wins (weeks vs months)\n- Cost (year 1): Similar range\n- Cost (year 2+): Build gets cheaper IF no major changes needed\n- Customization: Build wins for unique requirements\n- Team focus: Buy frees engineers for core product\n\n**Recommendation:** Buy for v1, instrument heavily, evaluate build for v2 after you understand what customization you actually need.\n\n**Present to stakeholders:** 'We can be live in 3 weeks with a vendor solution vs. 6 months to build. Let's validate demand first, then build custom if our needs diverge from what the vendor offers.'",
            "correct": True,
            "analysis": "Structured analysis with numbers, tradeoffs, and a stakeholder-ready recommendation. Chain-of-thought turned a vague opinion into a PM decision framework."
        }
    },
}

# ── Tab 4: Output Format Control ──────────────────────────────────────────────

FORMAT_DEMOS = {
    "List the top 5 risks of launching an AI chatbot for customer service.": {
        "No format instruction": {
            "prompt": "List the top 5 risks of launching an AI chatbot for customer service.",
            "response": "The main risks of launching an AI chatbot include hallucination where the bot gives wrong information, prompt injection attacks, high costs at scale, brand damage from bad responses, and compliance issues with data privacy regulations. Each of these needs careful planning before launch.",
            "analysis": "Paragraph format — hard to scan, can't copy into a slide deck."
        },
        "Markdown bullets": {
            "prompt": "List the top 5 risks of launching an AI chatbot for customer service. Use markdown bullet points with bold risk names.",
            "response": "- **Hallucination** — Bot confidently states incorrect policies or facts\n- **Prompt Injection** — Users override system instructions to misuse the bot\n- **Cost Overrun** — Token costs scale linearly; viral usage = massive bill\n- **Brand Damage** — One bad response screenshot goes viral on social media\n- **Compliance** — GDPR/CCPA requirements for AI-based decision making",
            "analysis": "Scannable, copy-paste ready for docs or Slack."
        },
        "JSON": {
            "prompt": "List the top 5 risks of launching an AI chatbot. Return as JSON array with fields: risk_name, severity (high/medium/low), mitigation.",
            "response": "```json\n[\n  {\"risk_name\": \"Hallucination\", \"severity\": \"high\", \"mitigation\": \"RAG with verified knowledge base + output validation\"},\n  {\"risk_name\": \"Prompt Injection\", \"severity\": \"high\", \"mitigation\": \"Input sanitization + instruction hierarchy + output filtering\"},\n  {\"risk_name\": \"Cost Overrun\", \"severity\": \"medium\", \"mitigation\": \"Rate limiting + cost alerts + model routing\"},\n  {\"risk_name\": \"Brand Damage\", \"severity\": \"high\", \"mitigation\": \"Output filtering + human-in-loop for sensitive topics\"},\n  {\"risk_name\": \"Compliance\", \"severity\": \"medium\", \"mitigation\": \"Privacy impact assessment + transparency disclosures\"}\n]\n```",
            "analysis": "Machine-readable. Can be directly ingested by dashboards, risk trackers, or APIs."
        },
    },
}


def tab1_compare(scenario):
    data = ZERO_VS_FEW.get(scenario)
    if not data:
        return "Select a scenario.", ""
    zs = data["zero_shot"]
    fs = data["few_shot"]

    left = f"### Zero-Shot Prompt\n\n```\n{zs['prompt']}\n```\n\n### Response\n\n{zs['response']}\n\n### Quality Assessment\n\n⚠️ {zs['quality']}"
    right = f"### Few-Shot Prompt\n\n```\n{fs['prompt']}\n```\n\n### Response\n\n{fs['response']}\n\n### Quality Assessment\n\n✅ {fs['quality']}"
    return left, right


def tab2_compare(scenario):
    data = SYSTEM_PROMPT_DEMOS.get(scenario)
    if not data:
        return ""
    md = f"## User Prompt: *\"{scenario}\"*\n\n"
    for persona, info in data.items():
        md += f"### {persona}\n\n"
        if info["system"] != "(none)":
            md += f"**System prompt:** *{info['system']}*\n\n"
        md += f"{info['response']}\n\n"
        md += f"**Analysis:** {info['analysis']}\n\n---\n\n"
    return md


def tab3_compare(scenario):
    data = COT_DEMOS.get(scenario)
    if not data:
        return "", ""
    wo = data["without_cot"]
    wi = data["with_cot"]

    icon_wo = "❌" if wo["correct"] is False else ("✅" if wo["correct"] else "⚠️")
    icon_wi = "✅" if wi["correct"] else "❌"

    left = f"### Without Chain-of-Thought\n\n```\n{wo['prompt']}\n```\n\n### Response\n\n{wo['response']}\n\n{icon_wo} **{wo['analysis']}**"
    right = f"### With Chain-of-Thought\n\n```\n{wi['prompt']}\n```\n\n### Response\n\n{wi['response']}\n\n{icon_wi} **{wi['analysis']}**"
    return left, right


def tab4_compare(scenario):
    data = FORMAT_DEMOS.get(scenario)
    if not data:
        return ""
    md = f"## Prompt: *\"{scenario}\"*\n\n"
    for fmt, info in data.items():
        md += f"### Format: {fmt}\n\n"
        md += f"**Prompt:** `{info['prompt']}`\n\n"
        md += f"**Response:**\n\n{info['response']}\n\n"
        md += f"**Assessment:** {info['analysis']}\n\n---\n\n"
    return md


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Prompt Engineering Lab", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Prompt Engineering Lab\n"
        "See how different prompt techniques change output quality.\n"
        "**Better prompts beat better models — and they're free.**"
    )

    with gr.Tab("Zero-Shot vs Few-Shot"):
        gr.Markdown("### Does giving examples actually help? See for yourself.")
        t1_dd = gr.Dropdown(choices=list(ZERO_VS_FEW.keys()), value=list(ZERO_VS_FEW.keys())[0], label="Scenario")
        t1_btn = gr.Button("Compare", variant="primary")
        with gr.Row():
            t1_left = gr.Markdown()
            t1_right = gr.Markdown()
        t1_btn.click(tab1_compare, [t1_dd], [t1_left, t1_right])
        demo.load(tab1_compare, [t1_dd], [t1_left, t1_right])

    with gr.Tab("System Prompt Impact"):
        gr.Markdown("### Same question, different personas. Watch the response transform.")
        t2_dd = gr.Dropdown(choices=list(SYSTEM_PROMPT_DEMOS.keys()), value=list(SYSTEM_PROMPT_DEMOS.keys())[0], label="Question")
        t2_btn = gr.Button("Compare", variant="primary")
        t2_out = gr.Markdown()
        t2_btn.click(tab2_compare, [t2_dd], [t2_out])
        demo.load(tab2_compare, [t2_dd], [t2_out])

    with gr.Tab("Chain-of-Thought"):
        gr.Markdown("### Does 'think step by step' actually improve reasoning?")
        t3_dd = gr.Dropdown(choices=list(COT_DEMOS.keys()), value=list(COT_DEMOS.keys())[0], label="Problem")
        t3_btn = gr.Button("Compare", variant="primary")
        with gr.Row():
            t3_left = gr.Markdown()
            t3_right = gr.Markdown()
        t3_btn.click(tab3_compare, [t3_dd], [t3_left, t3_right])
        demo.load(tab3_compare, [t3_dd], [t3_left, t3_right])

    with gr.Tab("Output Format Control"):
        gr.Markdown("### Same content, different formats. Control what you get back.")
        t4_dd = gr.Dropdown(choices=list(FORMAT_DEMOS.keys()), value=list(FORMAT_DEMOS.keys())[0], label="Request")
        t4_btn = gr.Button("Compare", variant="primary")
        t4_out = gr.Markdown()
        t4_btn.click(tab4_compare, [t4_dd], [t4_out])
        demo.load(tab4_compare, [t4_dd], [t4_out])

    gr.Markdown("---\n*AI for Product Managers*")

if __name__ == "__main__":
    demo.launch()
