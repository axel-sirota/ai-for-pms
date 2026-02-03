import gradio as gr

# Failure mode scenarios
FAILURE_MODES = {
    "Bad Chunking": {
        "description": "Important information is split across chunks, so retrieval returns incomplete data.",
        "document": """Our pricing structure is as follows:
The Basic plan costs $29 per month and includes up to 5 users with basic features.
The Pro plan costs $99 per month, which includes unlimited users, priority support, and advanced analytics.
The Enterprise plan is custom priced based on your needs.""",
        "bad_chunks": [
            "Our pricing structure is as follows: The Basic plan costs $29 per month and includes up to 5 users with basic features. The Pro plan costs $99 per",
            "month, which includes unlimited users, priority support, and advanced analytics. The Enterprise plan is custom priced based on your needs."
        ],
        "question": "How much does the Pro plan cost?",
        "retrieved": "Our pricing structure is as follows: The Basic plan costs $29 per month and includes up to 5 users with basic features. The Pro plan costs $99 per",
        "bad_answer": "The Pro plan costs $99. (Note: The 'per month' part was in the next chunk and not retrieved)",
        "good_answer": "The Pro plan costs $99 per month and includes unlimited users, priority support, and advanced analytics.",
        "fix": "Use sentence-aware chunking to avoid splitting mid-sentence, or increase chunk overlap to capture boundary content."
    },
    "Wrong Retrieval": {
        "description": "Semantic similarity matches keywords but retrieves contextually wrong information.",
        "document": """Software Licensing Policy:
All software licenses are non-transferable and tied to the original purchaser.

Hardware Return Policy:
Hardware items can be returned within 30 days for a full refund.

General Refund Processing:
All approved refunds are processed within 5-7 business days.

Software Refund Policy:
Software purchases can be refunded within 14 days if the product has not been activated or downloaded.""",
        "bad_chunks": [
            "Software Licensing Policy: All software licenses are non-transferable and tied to the original purchaser.",
            "Hardware Return Policy: Hardware items can be returned within 30 days for a full refund.",
            "General Refund Processing: All approved refunds are processed within 5-7 business days.",
            "Software Refund Policy: Software purchases can be refunded within 14 days if the product has not been activated or downloaded."
        ],
        "question": "What is the refund policy for software?",
        "retrieved": "Software Licensing Policy: All software licenses are non-transferable... | General Refund Processing: All approved refunds are processed within 5-7 business days.",
        "bad_answer": "Software licenses are non-transferable and refunds are processed within 5-7 business days. (Wrong! Retrieved 'software licensing' and 'refund processing' but missed the actual software refund policy)",
        "good_answer": "Software purchases can be refunded within 14 days if the product has not been activated or downloaded.",
        "fix": "Use hybrid search (keywords + embeddings), add metadata filtering, or improve chunk boundaries to keep related content together."
    },
    "Hallucination Despite Context": {
        "description": "The model ignores retrieved context and generates incorrect information.",
        "document": """Return Policy:
Customers may return items within 30 days of purchase for a full refund.
Items must be in original condition with all tags attached.
Electronics have a shorter 15-day return window.
Gift cards and final sale items are non-refundable.""",
        "bad_chunks": [
            "Return Policy: Customers may return items within 30 days of purchase for a full refund. Items must be in original condition with all tags attached.",
            "Electronics have a shorter 15-day return window. Gift cards and final sale items are non-refundable."
        ],
        "question": "How long do I have to return an item?",
        "retrieved": "Return Policy: Customers may return items within 30 days of purchase for a full refund. Items must be in original condition with all tags attached.",
        "bad_answer": "You have 60 days to return items for a full refund. (HALLUCINATION! The context clearly says 30 days but the model ignored it)",
        "good_answer": "You have 30 days to return items for a full refund. Items must be in original condition with all tags attached.",
        "fix": "Use stronger grounding prompts ('Only use information from the provided context'), better models, or add output validation that compares the answer to retrieved chunks."
    },
    "Outdated Info Conflict": {
        "description": "Your documents have current info, but the model's training data has outdated info it prefers.",
        "document": """Shipping Policy (Updated January 2024):
Free shipping on all orders over $50.
Standard shipping: 5-7 business days.
Express shipping: 2-3 business days ($9.99).
International shipping available to 50+ countries.""",
        "bad_chunks": [
            "Shipping Policy (Updated January 2024): Free shipping on all orders over $50. Standard shipping: 5-7 business days.",
            "Express shipping: 2-3 business days ($9.99). International shipping available to 50+ countries."
        ],
        "question": "What's the minimum order for free shipping?",
        "retrieved": "Shipping Policy (Updated January 2024): Free shipping on all orders over $50. Standard shipping: 5-7 business days.",
        "bad_answer": "Free shipping is available on orders over $35. (OUTDATED! The model 'remembered' an old policy from its training data instead of using the retrieved document showing $50)",
        "good_answer": "Free shipping is available on all orders over $50.",
        "fix": "Use explicit prompting to prioritize retrieved context over model knowledge, or use a model with less domain knowledge that will defer to the provided context."
    },
    "Missing Info Hallucination": {
        "description": "The question isn't covered in documents, but instead of saying 'I don't know', the model invents an answer.",
        "document": """Membership Benefits:
- 10% discount on all purchases
- Early access to sales
- Free birthday gift
- Exclusive member events

Membership Tiers:
- Silver: Spend $0-$499/year
- Gold: Spend $500-$999/year
- Platinum: Spend $1000+/year""",
        "bad_chunks": [
            "Membership Benefits: 10% discount on all purchases, Early access to sales, Free birthday gift, Exclusive member events",
            "Membership Tiers: Silver ($0-$499/year), Gold ($500-$999/year), Platinum ($1000+/year)"
        ],
        "question": "Do you offer student discounts?",
        "retrieved": "Membership Benefits: 10% discount on all purchases, Early access to sales, Free birthday gift, Exclusive member events",
        "bad_answer": "Yes! We offer a 15% student discount with a valid student ID. (HALLUCINATION! The documents say nothing about student discounts - the model made this up)",
        "good_answer": "I don't have information about student discounts in the provided documents. The membership program offers a 10% discount on all purchases.",
        "fix": "Train the model to say 'I don't know' when retrieval confidence is low, or implement a confidence threshold that triggers a human handoff."
    }
}


def show_failure_mode(mode):
    """Display a specific failure mode scenario."""
    scenario = FAILURE_MODES[mode]

    doc_display = f"**Original Document:**\n```\n{scenario['document']}\n```"
    chunks_display = "**How it was chunked:**\n" + "\n".join([f"- Chunk {i+1}: `{c[:80]}...`" for i, c in enumerate(scenario['bad_chunks'])])
    question_display = f"**User Question:** {scenario['question']}"
    retrieved_display = f"**Retrieved Context:**\n```\n{scenario['retrieved']}\n```"
    bad_answer_display = f"**❌ Bad RAG Answer:**\n{scenario['bad_answer']}"
    good_answer_display = f"**✅ What it should have said:**\n{scenario['good_answer']}"
    fix_display = f"**🔧 How to Fix:**\n{scenario['fix']}"

    return (
        scenario['description'],
        doc_display,
        chunks_display,
        question_display,
        retrieved_display,
        bad_answer_display,
        good_answer_display,
        fix_display
    )


# Build interface
with gr.Blocks(title="RAG Failure Simulator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# RAG Failure Simulator\n\n"
        "**PM Decision:** Before launching a RAG system, you need to understand how it can fail. "
        "This simulator shows you the 5 most common failure modes so you can ask the right questions "
        "during development and diagnose issues when they occur.\n\n"
        "Select a failure mode to see a realistic example."
    )

    mode_dropdown = gr.Dropdown(
        choices=list(FAILURE_MODES.keys()),
        label="Select Failure Mode",
        value="Bad Chunking"
    )

    description_output = gr.Markdown(label="What Happens")

    with gr.Row():
        with gr.Column():
            doc_output = gr.Markdown(label="Document")
            chunks_output = gr.Markdown(label="Chunking")

        with gr.Column():
            question_output = gr.Markdown(label="Question")
            retrieved_output = gr.Markdown(label="Retrieved")

    with gr.Row():
        with gr.Column():
            bad_output = gr.Markdown(label="Bad Answer")

        with gr.Column():
            good_output = gr.Markdown(label="Good Answer")

    fix_output = gr.Markdown(label="Fix")

    # Load initial
    demo.load(
        show_failure_mode,
        inputs=[mode_dropdown],
        outputs=[description_output, doc_output, chunks_output, question_output, retrieved_output, bad_output, good_output, fix_output]
    )

    mode_dropdown.change(
        show_failure_mode,
        inputs=[mode_dropdown],
        outputs=[description_output, doc_output, chunks_output, question_output, retrieved_output, bad_output, good_output, fix_output]
    )

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** When RAG gives wrong answers, don't just say 'fix it.' Diagnose which of these "
        "5 failure modes occurred - each needs a different solution.\n\n"
        "*AI for Product Managers*"
    )

if __name__ == "__main__":
    demo.launch()
