"""
Token Counter & Cost Calculator — AI for Product Managers
Paste text → see tokens → estimate costs by model.
"""

import gradio as gr
import tiktoken

# ── Model Pricing (per 1M tokens, as of late 2024) ───────────────────────────

MODEL_PRICING = {
    "GPT-4o": {"input": 2.50, "output": 10.00, "ratio": 1.0},
    "GPT-4o-mini": {"input": 0.15, "output": 0.60, "ratio": 1.0},
    "GPT-4 Turbo": {"input": 10.00, "output": 30.00, "ratio": 1.0},
    "Claude 3.5 Sonnet": {"input": 3.00, "output": 15.00, "ratio": 1.05},
    "Claude 3.5 Haiku": {"input": 0.80, "output": 4.00, "ratio": 1.05},
    "Gemini 1.5 Pro": {"input": 1.25, "output": 5.00, "ratio": 0.95},
    "Gemini 1.5 Flash": {"input": 0.075, "output": 0.30, "ratio": 0.95},
    "Llama 3.1 70B (hosted)": {"input": 0.59, "output": 0.79, "ratio": 1.1},
}

SAMPLE_TEXTS = {
    "Short email": "Hi team,\n\nJust a quick update on the Q4 product roadmap. We've decided to prioritize the customer dashboard redesign and push the API v2 launch to Q1. The design team will share mockups by Friday.\n\nLet me know if you have questions.\n\nBest,\nSarah",
    "Customer support query": "I ordered a pair of running shoes (Order #45892) three weeks ago and they still haven't arrived. The tracking shows it's been stuck in transit for 10 days. I've already contacted the shipping company and they said to talk to you. I need these for a marathon next weekend. Can you either expedite a replacement or give me a full refund? This is really frustrating as a long-time customer.",
    "Product description": "Introducing the CloudSync Pro — our most advanced wireless earbuds yet. Featuring adaptive noise cancellation powered by AI, 40-hour battery life with the charging case, and seamless switching between up to 3 devices. The custom-tuned 11mm drivers deliver rich bass and crystal-clear mids, while the ergonomic design ensures all-day comfort. IPX5 water resistance means they can handle your toughest workouts. Available in Midnight Black, Arctic White, and Ocean Blue. Compatible with iOS 16+, Android 12+, and Windows 11.",
    "JSON API response": '{"user":{"id":12345,"name":"Alex Johnson","email":"alex@example.com","plan":"enterprise","usage":{"api_calls_today":1247,"api_calls_limit":10000,"tokens_used":523891,"tokens_limit":1000000},"billing":{"current_period":"2024-01-01 to 2024-01-31","amount_due":299.99,"payment_method":"visa_4242","next_invoice":"2024-02-01"}}}',
}


def count_tokens_and_cost(text, output_length, queries_per_day):
    if not text or not text.strip():
        return "Please enter some text to analyze.", None

    # Count tokens using tiktoken (cl100k_base = GPT-4/4o encoding)
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    input_token_count = len(tokens)

    # Token visualization: show first 50 tokens with boundaries
    token_strings = [enc.decode([t]) for t in tokens[:60]]
    viz_parts = []
    colors = ["#dbeafe", "#fef3c7", "#d1fae5", "#ede9fe", "#fee2e2", "#fce7f3"]
    for i, ts in enumerate(token_strings):
        color = colors[i % len(colors)]
        display_text = ts.replace(" ", "·").replace("\n", "↵")
        viz_parts.append(f'<span style="background:{color}; padding:2px 4px; border-radius:3px; margin:1px; display:inline-block; font-family:monospace; font-size:0.85rem;">{display_text}</span>')

    if len(tokens) > 60:
        viz_parts.append(f'<span style="color:#6b7280;">... and {len(tokens) - 60} more tokens</span>')

    viz_html = " ".join(viz_parts)

    # Build results
    output_tokens = int(output_length)

    md = f"""## Token Analysis

**Input tokens:** {input_token_count:,}
**Expected output tokens:** {output_tokens:,}
**Total tokens per query:** {input_token_count + output_tokens:,}

### Token Visualization (first 60 tokens)

{viz_html}

---

### Cost by Model

| Model | Input Cost | Output Cost | **Total/Query** | Monthly ({queries_per_day:,}/day) |
|-------|-----------|-------------|----------------|--------------------------------|
"""

    for model, pricing in MODEL_PRICING.items():
        # Adjust token count for non-OpenAI models
        adj_input = int(input_token_count * pricing["ratio"])
        adj_output = int(output_tokens * pricing["ratio"])

        input_cost = adj_input * pricing["input"] / 1_000_000
        output_cost = adj_output * pricing["output"] / 1_000_000
        total = input_cost + output_cost
        monthly = total * queries_per_day * 30

        md += f"| {model} | ${input_cost:.6f} | ${output_cost:.6f} | **${total:.5f}** | **${monthly:,.2f}** |\n"

    # Tips
    md += f"""
---

### Tips to Reduce Costs

"""
    if input_token_count > 500:
        md += "- **Shorten your prompt** — your input is {0} tokens. Can you convey the same meaning in fewer words?\n".format(input_token_count)
    if output_tokens > 300:
        md += f"- **Limit output length** — set `max_tokens={output_tokens}` to cap responses. Output tokens cost 2-4x more than input.\n"

    md += "- **Use a smaller model** — GPT-4o-mini is 17x cheaper than GPT-4o. Test if quality is sufficient.\n"
    md += "- **Cache common queries** — if users ask similar questions, cache responses to avoid repeated API calls.\n"
    md += "- **Route by complexity** — use cheap models for simple tasks, expensive ones for complex tasks.\n"

    return md, None


def load_sample(sample_name):
    return SAMPLE_TEXTS.get(sample_name, "")


# ── Gradio UI ─────────────────────────────────────────────────────────────────

with gr.Blocks(title="Token Counter & Cost Calculator", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown(
        "# Token Counter & Cost Calculator\n"
        "Paste text → see exact token counts → estimate API costs by model.\n"
        "**Every token costs money. Know what you're spending.**"
    )

    gr.Markdown(
        "> **PM Decision:** Token counts directly impact API costs and response latency. "
        "Use this to estimate costs before committing to a model - a 10x difference in token count "
        "means a 10x difference in your monthly bill."
    )

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Your Text",
                placeholder="Paste your prompt, document, or any text here...",
                lines=8
            )
            sample_dd = gr.Dropdown(
                choices=list(SAMPLE_TEXTS.keys()),
                label="Or load a sample",
                value=None
            )
        with gr.Column(scale=1):
            output_length = gr.Slider(
                50, 2000, value=300, step=50,
                label="Expected Output Tokens"
            )
            queries_per_day = gr.Slider(
                10, 100000, value=1000, step=10,
                label="Queries per Day"
            )

    sample_dd.change(load_sample, [sample_dd], [text_input])

    count_btn = gr.Button("Count Tokens & Calculate Cost", variant="primary")

    results = gr.Markdown()
    hidden = gr.State()

    count_btn.click(
        count_tokens_and_cost,
        [text_input, output_length, queries_per_day],
        [results, hidden]
    )

    gr.Markdown("---\n*AI for Product Managers*")


if __name__ == "__main__":
    demo.launch()
