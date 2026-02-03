import gradio as gr


def analyze_approach(
    update_frequency,
    corpus_size,
    need_citations,
    training_examples,
    budget,
    timeline,
    volume
):
    """Analyze which approach is best based on inputs."""

    scores = {"RAG": 0, "Fine-tuning": 0, "Long Context": 0}
    reasons = {"RAG": [], "Fine-tuning": [], "Long Context": []}

    # Update frequency
    if update_frequency == "Daily/Weekly":
        scores["RAG"] += 3
        reasons["RAG"].append("Frequent updates - RAG handles without retraining")
        scores["Fine-tuning"] -= 2
        reasons["Fine-tuning"].append("Would need constant retraining")
    elif update_frequency == "Monthly":
        scores["RAG"] += 2
        reasons["RAG"].append("Monthly updates manageable with RAG")
        scores["Long Context"] += 1
    else:  # Rarely
        scores["Fine-tuning"] += 2
        reasons["Fine-tuning"].append("Stable content suits fine-tuning")
        scores["Long Context"] += 1

    # Corpus size
    if corpus_size == "Small (<50 pages)":
        scores["Long Context"] += 3
        reasons["Long Context"].append("Small corpus fits in context window")
        scores["RAG"] -= 1
        reasons["RAG"].append("RAG may be overkill for small corpus")
    elif corpus_size == "Medium (50-500 pages)":
        scores["RAG"] += 2
        reasons["RAG"].append("Medium corpus ideal for RAG")
    else:  # Large
        scores["RAG"] += 3
        reasons["RAG"].append("Large corpus requires RAG")
        scores["Long Context"] -= 3
        reasons["Long Context"].append("Too large for context window")

    # Citations
    if need_citations == "Required":
        scores["RAG"] += 3
        reasons["RAG"].append("RAG provides source citations")
        scores["Fine-tuning"] -= 2
        reasons["Fine-tuning"].append("Fine-tuning can't provide citations")
    elif need_citations == "Nice to have":
        scores["RAG"] += 1

    # Training examples
    if training_examples == "1000+":
        scores["Fine-tuning"] += 2
        reasons["Fine-tuning"].append("Sufficient training data available")
    elif training_examples == "100-1000":
        scores["Fine-tuning"] -= 1
        reasons["Fine-tuning"].append("Limited training data")
    else:  # <100
        scores["Fine-tuning"] -= 2
        reasons["Fine-tuning"].append("Insufficient data for fine-tuning")

    # Budget
    if budget == "Low (<$5K)":
        scores["Long Context"] += 2
        reasons["Long Context"].append("Lowest setup cost")
        scores["Fine-tuning"] -= 2
        reasons["Fine-tuning"].append("Fine-tuning typically costs $10K+")
    elif budget == "Medium ($5K-$50K)":
        scores["RAG"] += 2
        reasons["RAG"].append("Good budget for RAG setup")

    # Timeline
    if timeline == "Urgent (<2 weeks)":
        scores["Long Context"] += 2
        reasons["Long Context"].append("Fastest to implement")
        scores["Fine-tuning"] -= 2
        reasons["Fine-tuning"].append("Fine-tuning takes weeks-months")
    elif timeline == "Standard (1-2 months)":
        scores["RAG"] += 1

    # Volume
    if volume == "High (10K+ queries/day)":
        scores["Fine-tuning"] += 2
        reasons["Fine-tuning"].append("Fine-tuning has lower per-query cost at scale")
        scores["Long Context"] -= 2
        reasons["Long Context"].append("Long context expensive at high volume")

    # Determine winner
    sorted_approaches = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    winner = sorted_approaches[0][0]
    runner_up = sorted_approaches[1][0]

    # Build recommendation
    recommendation = f"## Recommendation: **{winner}**\n\n"

    if winner == "RAG":
        recommendation += """### Why RAG?
RAG (Retrieval-Augmented Generation) retrieves relevant documents at query time and uses them to generate grounded answers.

**Pros:**
- Updates without retraining
- Provides citations
- Handles large document sets
- Moderate setup cost

**Cons:**
- Retrieval quality depends on chunking
- Additional latency for retrieval step
- Requires vector database

"""
    elif winner == "Fine-tuning":
        recommendation += """### Why Fine-tuning?
Fine-tuning retrains the model on your specific data to learn domain knowledge, terminology, and desired output format.

**Pros:**
- Lower per-query cost at scale
- Consistent style/format
- No retrieval latency

**Cons:**
- High upfront cost ($10K-$200K)
- Slow to update (requires retraining)
- Can't provide citations
- Needs 1000+ training examples

"""
    else:
        recommendation += """### Why Long Context?
Long context simply includes all relevant documents directly in the prompt for each query.

**Pros:**
- Simplest to implement
- No infrastructure needed
- Easy to update

**Cons:**
- Limited corpus size
- High per-query cost
- Doesn't scale

"""

    # Add reasons
    recommendation += f"### Key Factors for Your Use Case\n\n"
    if reasons[winner]:
        recommendation += "**In favor of " + winner + ":**\n"
        for r in reasons[winner]:
            recommendation += f"- {r}\n"

    recommendation += f"\n**Runner-up: {runner_up}**\n"
    if reasons[runner_up]:
        for r in reasons[runner_up][:2]:
            recommendation += f"- {r}\n"

    # Comparison table
    comparison = """## Approach Comparison

| Factor | RAG | Fine-tuning | Long Context |
|--------|-----|-------------|--------------|
| **Setup Cost** | $1K-$10K | $10K-$200K | $0 |
| **Time to Update** | Minutes | Weeks | Immediate |
| **Citations** | ✅ Yes | ❌ No | ⚠️ Manual |
| **Max Corpus** | Unlimited | N/A | ~100K tokens |
| **Per-Query Cost** | Medium | Low | High |
| **Scalability** | High | High | Low |
"""

    return recommendation, comparison


# Build interface
with gr.Blocks(title="RAG vs Fine-tuning", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# RAG vs Fine-tuning Comparison\n\n"
        "**PM Decision:** Your engineering team proposes grounding AI in company knowledge. "
        "But which approach? RAG, fine-tuning, or just long context?\n\n"
        "Answer these questions to get a recommendation based on your specific requirements."
    )

    with gr.Row():
        with gr.Column():
            update_freq = gr.Radio(
                choices=["Daily/Weekly", "Monthly", "Rarely"],
                label="How often do your documents change?",
                value="Monthly"
            )
            corpus_size = gr.Radio(
                choices=["Small (<50 pages)", "Medium (50-500 pages)", "Large (500+ pages)"],
                label="How large is your document corpus?",
                value="Medium (50-500 pages)"
            )
            citations = gr.Radio(
                choices=["Required", "Nice to have", "Not needed"],
                label="Do you need to cite source documents?",
                value="Nice to have"
            )
            training_data = gr.Radio(
                choices=["<100 examples", "100-1000 examples", "1000+ examples"],
                label="How many training examples do you have?",
                value="100-1000 examples"
            )

        with gr.Column():
            budget = gr.Radio(
                choices=["Low (<$5K)", "Medium ($5K-$50K)", "High ($50K+)"],
                label="What's your budget for setup?",
                value="Medium ($5K-$50K)"
            )
            timeline = gr.Radio(
                choices=["Urgent (<2 weeks)", "Standard (1-2 months)", "Flexible (3+ months)"],
                label="What's your timeline?",
                value="Standard (1-2 months)"
            )
            volume = gr.Radio(
                choices=["Low (<1K queries/day)", "Medium (1K-10K)", "High (10K+ queries/day)"],
                label="Expected query volume?",
                value="Medium (1K-10K)"
            )

            analyze_btn = gr.Button("Get Recommendation", variant="primary")

    recommendation_output = gr.Markdown(label="Recommendation")
    comparison_output = gr.Markdown(label="Comparison")

    analyze_btn.click(
        analyze_approach,
        inputs=[update_freq, corpus_size, citations, training_data, budget, timeline, volume],
        outputs=[recommendation_output, comparison_output]
    )

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** RAG is usually the safest choice - it's easier to update, provides citations, "
        "and has moderate costs. Only consider fine-tuning if you have stable content, 1000+ examples, "
        "and don't need citations.\n\n"
        "*AI for Product Managers*"
    )

if __name__ == "__main__":
    demo.launch()
