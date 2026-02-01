"""Model Comparison Arena - Compare LLM responses side by side.
Uses OpenAI + Anthropic APIs when available, falls back to pre-cached responses.
"""
import gradio as gr
import os
import time
import json

# ---- Pre-cached responses for demo/fallback mode ----
CACHED_RESPONSES = {
    "Write a professional email declining a meeting": {
        "GPT-4o": {
            "response": "Subject: Unable to Attend - [Meeting Name]\n\nHi [Name],\n\nThank you for the invitation to [meeting]. Unfortunately, I have a prior commitment at that time and won't be able to attend.\n\nIf there are any materials or action items I should review afterward, please share them and I'll follow up. Alternatively, I'm available [suggest 2-3 alternative times] if rescheduling works for the group.\n\nBest regards,\n[Your Name]",
            "time_ms": 1240, "input_tokens": 12, "output_tokens": 89,
            "cost_per_query": 0.00067
        },
        "GPT-4o-mini": {
            "response": "Subject: Regrets - [Meeting Name]\n\nHi [Name],\n\nThanks for including me. Unfortunately, I won't be able to make it due to a scheduling conflict.\n\nPlease send me the notes afterward so I can stay in the loop. Happy to connect separately if needed.\n\nBest,\n[Your Name]",
            "time_ms": 680, "input_tokens": 12, "output_tokens": 62,
            "cost_per_query": 0.000012
        },
        "Claude 3.5 Sonnet": {
            "response": "Subject: Unable to Attend [Meeting Name] on [Date]\n\nHi [Name],\n\nI appreciate you thinking of me for this meeting. Unfortunately, I have a conflicting obligation at that time and won't be able to join.\n\nA few thoughts:\n- If there's a specific topic you'd like my input on, I'm happy to share my perspective beforehand\n- I'd welcome reviewing any notes or decisions that come out of the meeting\n- If it would be helpful, I'm free on [alternative dates] for a quick catch-up\n\nThanks for understanding.\n\nWarm regards,\n[Your Name]",
            "time_ms": 1450, "input_tokens": 12, "output_tokens": 112,
            "cost_per_query": 0.00045
        },
        "Claude Haiku": {
            "response": "Subject: Can't Make [Meeting]\n\nHi [Name],\n\nThanks for the invite - unfortunately I can't attend due to a conflict. Could you share the notes after? I'll review and follow up on anything relevant.\n\nBest,\n[Your Name]",
            "time_ms": 320, "input_tokens": 12, "output_tokens": 48,
            "cost_per_query": 0.000008
        },
        "Llama 3.1 70B": {
            "response": "Subject: Meeting Decline\n\nHello [Name],\n\nI wanted to let you know that I won't be able to attend the upcoming meeting. I have another commitment that conflicts with the scheduled time.\n\nPlease feel free to share any meeting notes or follow-up items with me, and I'll make sure to address them promptly.\n\nThank you for your understanding.\n\nBest regards,\n[Your Name]",
            "time_ms": 890, "input_tokens": 12, "output_tokens": 76,
            "cost_per_query": 0.00018
        }
    },
    "Summarize the key risks of deploying AI in customer service": {
        "GPT-4o": {
            "response": "**Key Risks of AI in Customer Service:**\n\n1. **Hallucination** — AI confidently provides incorrect information (e.g., Air Canada chatbot promising non-existent fares, costing $800K+)\n\n2. **Brand Damage** — Inappropriate responses go viral instantly (DPD chatbot swearing at customers)\n\n3. **Escalation Failures** — AI doesn't know when to hand off to humans, frustrating customers on complex issues\n\n4. **Data Privacy** — Customer conversations may contain PII; improper handling creates regulatory liability\n\n5. **Over-automation** — Customers feel dehumanized; satisfaction drops for emotional or complex issues\n\n6. **Bias** — AI may treat customer segments differently based on training data patterns\n\n7. **Dependency Risk** — Over-reliance on AI vendor creates single point of failure\n\n**Mitigation:** Human-in-the-loop for high-stakes decisions, robust guardrails, continuous monitoring, and clear escalation paths.",
            "time_ms": 2100, "input_tokens": 15, "output_tokens": 178,
            "cost_per_query": 0.0013
        },
        "GPT-4o-mini": {
            "response": "Key risks of deploying AI in customer service:\n\n1. **Hallucinations** - AI may give incorrect information confidently\n2. **Brand risk** - Bad AI interactions can go viral on social media\n3. **Privacy concerns** - Customer data handling must comply with regulations\n4. **Over-reliance** - Reducing human staff too quickly can hurt service quality\n5. **Escalation gaps** - AI may fail to recognize when human help is needed\n6. **Bias in responses** - AI may not serve all customer segments equally\n\nRecommend starting with AI-assisted (not AI-only) approach with human oversight.",
            "time_ms": 950, "input_tokens": 15, "output_tokens": 118,
            "cost_per_query": 0.00002
        },
        "Claude 3.5 Sonnet": {
            "response": "Here are the critical risks to consider:\n\n**Immediate Risks:**\n- **Hallucination liability** — AI states incorrect policies, prices, or commitments as fact. Legal precedent exists (Air Canada, 2024: $800K+ for chatbot promising non-existent bereavement fares)\n- **Prompt injection** — Malicious users manipulate AI into bypassing guidelines (DPD chatbot was tricked into swearing)\n- **PII exposure** — AI accidentally surfaces or stores sensitive customer information\n\n**Operational Risks:**\n- **Silent failures** — AI gives plausible but wrong answers with no escalation trigger\n- **Coverage gaps** — Edge cases and novel scenarios not in training data\n- **Measurement blind spots** — Automated CSAT scores may not capture frustrated customers who gave up\n\n**Strategic Risks:**\n- **Customer trust erosion** — Customers who receive bad AI responses may not return\n- **Regulatory exposure** — EU AI Act, CCPA, industry-specific regulations apply\n- **Vendor dependency** — API price increases or outages directly impact service\n\n**Recommendation:** Deploy with human-in-the-loop, measure everything, and start with low-stakes interactions (FAQs, status checks) before handling complaints or transactions.",
            "time_ms": 2400, "input_tokens": 15, "output_tokens": 215,
            "cost_per_query": 0.00073
        },
        "Claude Haiku": {
            "response": "Main risks of AI in customer service:\n\n1. Hallucinations - providing wrong information as facts\n2. Brand damage from viral bad interactions\n3. Privacy/data concerns with customer conversations\n4. Failed escalations - not recognizing when humans are needed\n5. Over-automation reducing service quality\n6. Regulatory compliance issues\n\nStart with AI-assisted rather than AI-only, with clear human escalation paths.",
            "time_ms": 450, "input_tokens": 15, "output_tokens": 82,
            "cost_per_query": 0.00001
        },
        "Llama 3.1 70B": {
            "response": "**Risks of AI in Customer Service:**\n\n1. **Accuracy Issues** - AI can provide incorrect information, leading to customer frustration and potential legal issues\n2. **Lack of Empathy** - AI struggles with emotional intelligence in sensitive situations\n3. **Privacy Concerns** - Handling of customer data must meet regulatory requirements\n4. **Integration Complexity** - Connecting AI to existing systems can be challenging\n5. **Customer Resistance** - Some customers prefer human interaction\n6. **Maintenance Burden** - Knowledge base needs constant updating\n\nBest practice: Start with simple, high-volume queries and gradually expand scope with continuous monitoring.",
            "time_ms": 1200, "input_tokens": 15, "output_tokens": 132,
            "cost_per_query": 0.00030
        }
    },
    "Explain machine learning to a 10-year-old": {
        "GPT-4o": {
            "response": "Imagine you have a robot friend who wants to learn how to sort your Halloween candy. 🍬\n\nAt first, the robot doesn't know anything about candy. So you show it examples:\n- \"This is chocolate\" 🍫\n- \"This is gummy\" 🐻\n- \"This is sour\" 🍋\n\nAfter seeing hundreds of examples, the robot starts to notice patterns — chocolate is usually brown and wrapped in foil, gummies are colorful and squishy.\n\nNow when you dump a new pile of candy, the robot can sort most of it correctly! But sometimes it makes mistakes — like thinking a brown gummy bear is chocolate. That's okay! You correct it, and it gets better over time.\n\n**That's machine learning:** teaching computers by showing them lots of examples instead of writing specific rules for everything. The more examples, the better it gets!",
            "time_ms": 1800, "input_tokens": 10, "output_tokens": 165,
            "cost_per_query": 0.0012
        },
        "GPT-4o-mini": {
            "response": "Machine learning is like teaching a computer to learn from examples, just like how you learn!\n\nImagine you're learning to tell dogs from cats. At first, you look at lots of pictures. After a while, you notice dogs usually have longer noses and cats have pointy ears.\n\nA computer does the same thing! You show it thousands of pictures, and it figures out the patterns on its own. Then it can look at a new picture and say \"that's a dog!\" or \"that's a cat!\"\n\nThe cool part? The more pictures it sees, the better it gets — just like you get better at things with practice! 🎯",
            "time_ms": 750, "input_tokens": 10, "output_tokens": 120,
            "cost_per_query": 0.000018
        },
        "Claude 3.5 Sonnet": {
            "response": "You know how you learned to catch a ball? Nobody gave you a math equation for it — you just tried a bunch of times, missed some, caught some, and your brain figured out the pattern.\n\nMachine learning works the same way, but for computers.\n\nLet's say you want a computer to recognize photos of dogs:\n1. You show it 10,000 photos labeled \"dog\" and \"not dog\"\n2. At first, it guesses randomly — maybe 50% right\n3. Each time it's wrong, it adjusts a tiny bit\n4. After millions of adjustments, it gets really good — maybe 95% right!\n\nThe computer doesn't actually \"understand\" what a dog is. It found patterns in the pixels — like floppy ears, fur, and four legs tend to appear together in photos labeled \"dog.\"\n\nThat's the secret: machine learning is really just pattern-finding at a scale humans can't do. And it's everywhere — your YouTube recommendations, Spotify playlists, and the face unlock on phones all use it!",
            "time_ms": 2100, "input_tokens": 10, "output_tokens": 195,
            "cost_per_query": 0.00062
        },
        "Claude Haiku": {
            "response": "Machine learning is when computers learn from examples, like you do!\n\nImagine teaching a computer to spot cats in photos. You show it thousands of cat pictures and not-cat pictures. Over time, it figures out that cats have pointy ears, whiskers, and fur.\n\nNow it can look at a new photo and say \"that's a cat!\" — even if it's never seen that exact cat before.\n\nThe more examples it sees, the smarter it gets. That's machine learning!",
            "time_ms": 380, "input_tokens": 10, "output_tokens": 90,
            "cost_per_query": 0.000012
        },
        "Llama 3.1 70B": {
            "response": "Think of machine learning like training a pet!\n\nWhen you teach a dog to sit, you show it what to do, give it treats when it's right, and gently correct it when it's wrong. After enough practice, the dog learns!\n\nMachine learning is the same idea, but with computers. Instead of treats, the computer uses math to know when it's getting closer to the right answer.\n\nFor example, if you want a computer to recognize your handwriting, you show it thousands of examples of letters. It practices over and over until it can read new handwriting it's never seen before.\n\nPretty cool, right? It's how Netflix knows what movies you'll like and how your phone recognizes your face!",
            "time_ms": 950, "input_tokens": 10, "output_tokens": 140,
            "cost_per_query": 0.00025
        }
    }
}

AVAILABLE_MODELS = ["GPT-4o", "GPT-4o-mini", "Claude 3.5 Sonnet", "Claude Haiku", "Llama 3.1 70B"]

# Cost per 1K tokens (approximate, 2025 pricing)
MODEL_PRICING = {
    "GPT-4o": {"input": 0.0025, "output": 0.01},
    "GPT-4o-mini": {"input": 0.00015, "output": 0.0006},
    "Claude 3.5 Sonnet": {"input": 0.003, "output": 0.015},
    "Claude Haiku": {"input": 0.00025, "output": 0.00125},
    "Llama 3.1 70B": {"input": 0.0009, "output": 0.0009},
}


def try_live_api(prompt, model_name):
    """Try calling live APIs. Returns None if unavailable."""
    try:
        if model_name in ["GPT-4o", "GPT-4o-mini"]:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                return None
            import openai
            client = openai.OpenAI(api_key=api_key)
            model_id = "gpt-4o" if model_name == "GPT-4o" else "gpt-4o-mini"
            start = time.time()
            resp = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            elapsed = (time.time() - start) * 1000
            text = resp.choices[0].message.content
            usage = resp.usage
            cost = (usage.prompt_tokens / 1000 * MODEL_PRICING[model_name]["input"] +
                    usage.completion_tokens / 1000 * MODEL_PRICING[model_name]["output"])
            return {
                "response": text, "time_ms": int(elapsed),
                "input_tokens": usage.prompt_tokens, "output_tokens": usage.completion_tokens,
                "cost_per_query": cost
            }
        elif model_name in ["Claude 3.5 Sonnet", "Claude Haiku"]:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                return None
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            model_id = "claude-sonnet-4-20250514" if "Sonnet" in model_name else "claude-haiku-4-20250414"
            start = time.time()
            resp = client.messages.create(
                model=model_id,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            elapsed = (time.time() - start) * 1000
            text = resp.content[0].text
            cost = (resp.usage.input_tokens / 1000 * MODEL_PRICING[model_name]["input"] +
                    resp.usage.output_tokens / 1000 * MODEL_PRICING[model_name]["output"])
            return {
                "response": text, "time_ms": int(elapsed),
                "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
                "cost_per_query": cost
            }
    except Exception:
        return None
    return None


def compare_models(prompt, selected_models):
    if not prompt.strip():
        return "Please enter a prompt.", ""
    if not selected_models:
        return "Please select at least one model.", ""

    results = []
    mode = "demo"

    for model in selected_models:
        if model not in AVAILABLE_MODELS:
            continue

        # Try live API first
        live = try_live_api(prompt, model)
        if live:
            mode = "live"
            results.append((model, live))
        else:
            # Fallback to cached
            cached = CACHED_RESPONSES.get(prompt, {}).get(model)
            if cached:
                results.append((model, cached))
            else:
                # Generate a placeholder for unknown prompts
                results.append((model, {
                    "response": f"*[Demo mode - no cached response for this prompt. Deploy with API keys for live responses.]*",
                    "time_ms": 0, "input_tokens": 0, "output_tokens": 0, "cost_per_query": 0
                }))

    if not results:
        return "No results generated.", ""

    mode_note = "**Live API responses**" if mode == "live" else "**Demo mode** (pre-cached responses — deploy with API keys for live comparisons)"

    # Build comparison markdown
    md = f"## Model Comparison\n{mode_note}\n\n"

    for model_name, data in results:
        cost_str = f"${data['cost_per_query']:.6f}" if data['cost_per_query'] > 0 else "N/A"
        md += f"---\n### {model_name}\n"
        md += f"**Time:** {data['time_ms']}ms | "
        md += f"**Tokens:** {data['input_tokens']} in / {data['output_tokens']} out | "
        md += f"**Cost:** {cost_str}\n\n"
        md += f"{data['response']}\n\n"

    # Cost comparison summary
    if len(results) > 1:
        md += "---\n## Cost at Scale\n\n"
        md += "| Model | Cost/Query | 1K queries/day | 50K queries/day | 500K queries/day |\n"
        md += "|-------|-----------|----------------|-----------------|------------------|\n"
        for model_name, data in results:
            cpq = data['cost_per_query']
            if cpq > 0:
                md += f"| {model_name} | ${cpq:.6f} | ${cpq * 1000:.2f}/day | ${cpq * 50000:.2f}/day | ${cpq * 500000:,.2f}/day |\n"

    # Key insight
    insight = "\n\n---\n## PM Takeaway\n"
    if len(results) >= 2:
        costs = [(m, d['cost_per_query']) for m, d in results if d['cost_per_query'] > 0]
        if len(costs) >= 2:
            costs.sort(key=lambda x: x[1])
            cheapest, most_expensive = costs[0], costs[-1]
            if most_expensive[1] > 0:
                ratio = most_expensive[1] / max(cheapest[1], 0.000001)
                insight += f"**{most_expensive[0]}** costs **{ratio:.0f}x more** than **{cheapest[0]}** per query. "
                insight += f"At 50K queries/day, that's **${most_expensive[1] * 50000 - cheapest[1] * 50000:,.2f}/day** in savings by using the cheaper model. "
                insight += "Always test if the cheaper model meets your quality bar before defaulting to the expensive one."

    return md, insight


with gr.Blocks(
    title="Model Comparison Arena",
    theme=gr.themes.Soft(primary_hue="blue")
) as demo:
    gr.Markdown(
        "# Model Comparison Arena\n"
        "Send the same prompt to multiple models and compare quality, speed, and cost side by side.\n\n"
        "*Runs with pre-cached responses in demo mode. Deploy with API keys for live comparisons.*"
    )

    with gr.Row():
        with gr.Column(scale=2):
            prompt_input = gr.Textbox(
                label="Your Prompt",
                placeholder="Enter a prompt to send to all selected models...",
                lines=3
            )
        with gr.Column(scale=1):
            model_select = gr.CheckboxGroup(
                choices=AVAILABLE_MODELS,
                value=["GPT-4o", "Claude 3.5 Sonnet", "GPT-4o-mini"],
                label="Select Models to Compare"
            )

    submit_btn = gr.Button("Compare Models", variant="primary")

    comparison_output = gr.Markdown(label="Comparison Results")
    insight_output = gr.Markdown(label="PM Takeaway")

    submit_btn.click(
        fn=compare_models,
        inputs=[prompt_input, model_select],
        outputs=[comparison_output, insight_output]
    )

    gr.Examples(
        examples=[
            ["Write a professional email declining a meeting", ["GPT-4o", "GPT-4o-mini", "Claude 3.5 Sonnet", "Claude Haiku", "Llama 3.1 70B"]],
            ["Summarize the key risks of deploying AI in customer service", ["GPT-4o", "Claude 3.5 Sonnet", "Llama 3.1 70B"]],
            ["Explain machine learning to a 10-year-old", ["GPT-4o", "Claude 3.5 Sonnet", "Claude Haiku"]],
        ],
        inputs=[prompt_input, model_select],
    )

if __name__ == "__main__":
    demo.launch()
