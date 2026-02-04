"""
Prompt Engineering Lab - AI for Product Managers
Live LLM interaction to experiment with 7 prompt patterns.
Students bring their own API key (OpenAI or Anthropic).
"""

import gradio as gr
import os

# Try to import API clients
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def get_completion(api_key: str, provider: str, prompt: str, system_prompt: str = None) -> str:
    """Get completion from OpenAI or Anthropic."""
    # Use provided key, or fall back to HF Secrets
    if provider == "OpenAI":
        key = api_key or os.getenv("OPENAI_API_KEY")
    else:
        key = api_key or os.getenv("ANTHROPIC_API_KEY")

    if not key:
        return "No API key found. Either enter one above, or ask your instructor for access."

    try:
        if provider == "OpenAI" and OPENAI_AVAILABLE:
            client = OpenAI(api_key=key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content

        elif provider == "Anthropic" and ANTHROPIC_AVAILABLE:
            client = Anthropic(api_key=key)

            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1000,
                system=system_prompt or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        else:
            return f"Provider {provider} not available. Install: pip install openai anthropic"

    except Exception as e:
        return f"Error: {str(e)}"


# ── Tab 1: Few-Shot Pattern ──────────────────────────────────────────────────

def tab1_run(api_key, provider, scenario, use_few_shot):
    """Compare zero-shot vs few-shot."""

    if scenario == "Customer Email Classification":
        user_input = "I've been waiting 3 weeks for my order and nobody will help me!"

        if use_few_shot:
            prompt = """Classify customer emails into exactly one category and severity level.

Examples:
Email: "Thanks for the quick delivery!" → Category: Praise | Severity: None
Email: "My item arrived broken" → Category: Product Issue | Severity: High
Email: "How do I change my password?" → Category: Account Support | Severity: Low
Email: "I want to cancel everything, this is the worst service ever" → Category: Cancellation Risk | Severity: Critical

Now classify:
Email: "{input}"
""".format(input=user_input)
        else:
            prompt = f"Classify this customer email: '{user_input}'"

    elif scenario == "Product Review Analysis":
        user_input = "The battery life is amazing but the screen is too dim outdoors. Camera is decent for the price."

        if use_few_shot:
            prompt = """Extract structured feedback from product reviews.

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
Review: "{input}"
""".format(input=user_input)
        else:
            prompt = f"Summarize this product review: '{user_input}'"

    else:
        return "Select a scenario."

    response = get_completion(api_key, provider, prompt)

    pattern_used = "Few-Shot (with examples)" if use_few_shot else "Zero-Shot (no examples)"
    return f"**Pattern:** {pattern_used}\n\n**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n\n{response}"


# ── Tab 2: Chain-of-Thought Pattern ──────────────────────────────────────────

def tab2_run(api_key, provider, scenario, use_cot):
    """Compare with/without chain-of-thought."""

    if scenario == "Pricing Calculation":
        base_prompt = "A customer bought 3 items at $50, $30, and $20. They have a 20% discount code and a $10 store credit. What's the final total?"
    elif scenario == "Build vs Buy Decision":
        base_prompt = "Should we build or buy a recommendation engine? Team: 3 ML engineers, 6-month timeline, 10M users."
    else:
        return "Select a scenario."

    if use_cot:
        prompt = base_prompt + " Think step by step."
    else:
        prompt = base_prompt

    response = get_completion(api_key, provider, prompt)

    pattern_used = "Chain-of-Thought ('Think step by step')" if use_cot else "Direct (no reasoning)"
    return f"**Pattern:** {pattern_used}\n\n**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n\n{response}"


# ── Tab 3: Persona Pattern ───────────────────────────────────────────────────

def tab3_run(api_key, provider, question, persona):
    """Compare different personas on same question."""

    personas = {
        "No persona": None,
        "Senior PM": "You are a senior product manager at a SaaS company. Frame all answers in terms of business impact, user experience, and stakeholder communication. Be specific and actionable.",
        "Security Auditor": "You are a cybersecurity auditor reviewing AI systems. Focus on attack vectors, compliance risks, and security controls. Reference industry frameworks (OWASP, NIST) where applicable.",
        "CFO": "You are a CFO evaluating technology investments. Focus on ROI, cost structure, risk mitigation, and financial impact. Be quantitative where possible.",
    }

    system_prompt = personas.get(persona)
    response = get_completion(api_key, provider, question, system_prompt)

    return f"**Persona:** {persona}\n\n**System Prompt:**\n```\n{system_prompt or '(none)'}\n```\n\n**Question:** {question}\n\n**Response:**\n\n{response}"


# ── Tab 4: Template Pattern ──────────────────────────────────────────────────

def tab4_run(api_key, provider, input_text, output_format):
    """Force structured output formats."""

    formats = {
        "No format": f"List the top 5 risks of launching an AI chatbot for customer service.",
        "Markdown bullets": f"List the top 5 risks of launching an AI chatbot for customer service. Use markdown bullet points with bold risk names.",
        "JSON": f"List the top 5 risks of launching an AI chatbot. Return as JSON array with fields: risk_name, severity (high/medium/low), mitigation.",
        "Table": f"List the top 5 risks of launching an AI chatbot. Format as a markdown table with columns: Risk | Severity | Mitigation | Owner.",
    }

    prompt = formats.get(output_format, formats["No format"])
    response = get_completion(api_key, provider, prompt)

    return f"**Format:** {output_format}\n\n**Prompt:**\n```\n{prompt}\n```\n\n**Response:**\n\n{response}"


# ── Tab 5: Flipped Interaction Pattern ───────────────────────────────────────

def tab5_run(api_key, provider, goal):
    """Make the AI ask questions first."""

    system_prompt = f"""You are a helpful assistant. Before providing any recommendations or solutions, you MUST ask clarifying questions first.

Your goal is to help the user: {goal}

Start by asking 3-5 relevant questions to understand their specific situation. Do NOT provide recommendations until you have gathered enough information."""

    user_prompt = f"I need help with: {goal}"

    response = get_completion(api_key, provider, user_prompt, system_prompt)

    return f"**Pattern:** Flipped Interaction\n\n**Goal:** {goal}\n\n**System Prompt:**\n```\n{system_prompt}\n```\n\n**Response:**\n\n{response}\n\n---\n**Why this matters:** The AI asks before assuming. Essential for chatbots - prevents hallucinated recommendations based on incomplete info."


# ── Tab 6: Reflection Pattern ────────────────────────────────────────────────

def tab6_run(api_key, provider, question, use_reflection):
    """Make the AI self-check its response."""

    if use_reflection:
        system_prompt = """You are a helpful assistant. After providing your response, you MUST include a self-review section.

Format:
1. [Your main response]

2. **Self-Review:**
   - Potential issues with this response:
   - Claims that should be verified:
   - What I might be missing:
   - Confidence level (low/medium/high):"""
    else:
        system_prompt = "You are a helpful assistant."

    response = get_completion(api_key, provider, question, system_prompt)

    pattern_used = "Reflection (self-check)" if use_reflection else "Standard (no reflection)"
    return f"**Pattern:** {pattern_used}\n\n**Question:** {question}\n\n**Response:**\n\n{response}"


# ── Tab 7: Fact Check List Pattern ───────────────────────────────────────────

def tab7_run(api_key, provider, topic):
    """Make the AI list verifiable claims."""

    system_prompt = """You are a helpful assistant that prioritizes accuracy. After providing information, you MUST include a fact-check list.

Format:
1. [Your main response]

2. **Fact Check List:**
   For each factual claim you made, list:
   - Claim: [the specific claim]
   - Verifiable: Yes/No
   - Suggested verification: [how to verify]
   - Confidence: High/Medium/Low"""

    prompt = f"Tell me about: {topic}"

    response = get_completion(api_key, provider, prompt, system_prompt)

    return f"**Pattern:** Fact Check List\n\n**Topic:** {topic}\n\n**Response:**\n\n{response}\n\n---\n**Why this matters:** This is your #1 defense against hallucination in customer-facing AI. The model flags its own claims that need verification."


# ── Gradio UI ────────────────────────────────────────────────────────────────

with gr.Blocks(title="Prompt Engineering Lab", theme=gr.themes.Soft(primary_hue="teal")) as demo:
    gr.Markdown(
        "# Prompt Engineering Lab\n"
        "**Experiment with 7 prompt patterns using live LLM calls.**\n\n"
        "API key may already be configured. If not, enter yours below."
    )

    gr.Markdown(
        "> **PM Decision:** Well-structured prompts reduce hallucinations and improve output quality - "
        "without changing models or increasing costs. Prompt engineering is your cheapest lever for quality improvement."
    )

    with gr.Row():
        api_key = gr.Textbox(
            label="API Key",
            placeholder="sk-... or sk-ant-...",
            type="password",
            scale=3
        )
        provider = gr.Dropdown(
            choices=["OpenAI", "Anthropic"],
            value="OpenAI",
            label="Provider",
            scale=1
        )

    gr.Markdown("---")

    # Tab 1: Few-Shot
    with gr.Tab("1. Few-Shot"):
        gr.Markdown("### Does giving examples help? Compare zero-shot vs few-shot.")
        t1_scenario = gr.Dropdown(
            choices=["Customer Email Classification", "Product Review Analysis"],
            value="Customer Email Classification",
            label="Scenario"
        )
        t1_fewshot = gr.Checkbox(label="Use Few-Shot (with examples)", value=False)
        t1_btn = gr.Button("Run", variant="primary")
        t1_out = gr.Markdown()
        t1_btn.click(tab1_run, [api_key, provider, t1_scenario, t1_fewshot], t1_out)

    # Tab 2: Chain-of-Thought
    with gr.Tab("2. Chain-of-Thought"):
        gr.Markdown("### Does 'think step by step' improve reasoning?")
        t2_scenario = gr.Dropdown(
            choices=["Pricing Calculation", "Build vs Buy Decision"],
            value="Pricing Calculation",
            label="Scenario"
        )
        t2_cot = gr.Checkbox(label="Use Chain-of-Thought", value=False)
        t2_btn = gr.Button("Run", variant="primary")
        t2_out = gr.Markdown()
        t2_btn.click(tab2_run, [api_key, provider, t2_scenario, t2_cot], t2_out)

    # Tab 3: Persona
    with gr.Tab("3. Persona"):
        gr.Markdown("### Same question, different personas. Watch the response transform.")
        t3_question = gr.Textbox(
            label="Your Question",
            value="What are the risks of launching an AI chatbot for customer service?",
            lines=2
        )
        t3_persona = gr.Dropdown(
            choices=["No persona", "Senior PM", "Security Auditor", "CFO"],
            value="No persona",
            label="Persona"
        )
        t3_btn = gr.Button("Run", variant="primary")
        t3_out = gr.Markdown()
        t3_btn.click(tab3_run, [api_key, provider, t3_question, t3_persona], t3_out)

    # Tab 4: Template
    with gr.Tab("4. Template"):
        gr.Markdown("### Control output format - text, bullets, JSON, tables.")
        t4_format = gr.Dropdown(
            choices=["No format", "Markdown bullets", "JSON", "Table"],
            value="No format",
            label="Output Format"
        )
        t4_btn = gr.Button("Run", variant="primary")
        t4_out = gr.Markdown()
        t4_btn.click(tab4_run, [api_key, provider, gr.State(""), t4_format], t4_out)

    # Tab 5: Flipped Interaction
    with gr.Tab("5. Flipped Interaction"):
        gr.Markdown("### Make the AI ask questions FIRST before recommending.")
        t5_goal = gr.Textbox(
            label="What do you need help with?",
            value="Planning a vacation",
            placeholder="e.g., Planning a vacation, Writing a PRD, Choosing a tech stack"
        )
        t5_btn = gr.Button("Run", variant="primary")
        t5_out = gr.Markdown()
        t5_btn.click(tab5_run, [api_key, provider, t5_goal], t5_out)

    # Tab 6: Reflection
    with gr.Tab("6. Reflection"):
        gr.Markdown("### Make the AI critique its own answer before responding.")
        t6_question = gr.Textbox(
            label="Ask a question",
            value="What's the best way to reduce customer churn?",
            lines=2
        )
        t6_reflection = gr.Checkbox(label="Use Reflection Pattern", value=False)
        t6_btn = gr.Button("Run", variant="primary")
        t6_out = gr.Markdown()
        t6_btn.click(tab6_run, [api_key, provider, t6_question, t6_reflection], t6_out)

    # Tab 7: Fact Check List
    with gr.Tab("7. Fact Check List"):
        gr.Markdown("### Make the AI list claims that need verification - hallucination defense.")
        t7_topic = gr.Textbox(
            label="Topic to ask about",
            value="The Air Canada chatbot lawsuit",
            placeholder="e.g., GDPR requirements for AI, OpenAI pricing, etc."
        )
        t7_btn = gr.Button("Run", variant="primary")
        t7_out = gr.Markdown()
        t7_btn.click(tab7_run, [api_key, provider, t7_topic], t7_out)

    gr.Markdown(
        "---\n"
        "*AI for Product Managers* | "
        "Patterns from [Jules White et al.](https://arxiv.org/abs/2302.11382)"
    )

if __name__ == "__main__":
    demo.launch()
