import gradio as gr
import re

SAMPLE_DOCS = {
    "FAQ Document": """Q: What is your return policy?
A: You can return most items within 30 days of purchase for a full refund. Items must be in original condition with tags attached.

Q: How long does shipping take?
A: Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days.

Q: Do you offer international shipping?
A: Yes, we ship to over 50 countries. International shipping typically takes 10-14 business days.

Q: How do I track my order?
A: Once your order ships, you'll receive an email with tracking information. You can also check order status in your account.

Q: What payment methods do you accept?
A: We accept Visa, Mastercard, American Express, PayPal, and Apple Pay.""",

    "Product Documentation": """Smart Thermostat Pro - User Guide

Installation:
Turn off power at the circuit breaker before beginning installation. Remove your old thermostat and take a photo of the wiring. The Smart Thermostat Pro is compatible with most 24V heating and cooling systems.

Setup:
Download the SmartHome app and create an account. The thermostat will automatically enter pairing mode when powered on. Follow the in-app instructions to connect to your WiFi network.

Daily Use:
The touchscreen displays current temperature and humidity. Swipe left or right to adjust target temperature. Tap the calendar icon to view and edit your schedule.

Energy Saving Features:
Auto-Away detects when you leave and adjusts temperature to save energy. The monthly energy report shows your usage patterns and savings. Eco mode reduces heating/cooling by 2 degrees to save up to 15% on energy bills.

Troubleshooting:
If the display is blank, check that power is connected at the circuit breaker. If WiFi won't connect, ensure your network is 2.4GHz (5GHz is not supported). For heating/cooling issues, verify the system wires match the terminal labels.""",

    "Policy Document": """Employee Remote Work Policy

1. Eligibility
All full-time employees who have completed their probationary period are eligible for remote work. Certain roles requiring physical presence are exempt from this policy.

2. Core Hours
Remote employees must be available from 10am to 3pm in their local timezone. This ensures overlap for team collaboration and meetings.

3. Equipment
The company provides a laptop and external monitor. Employees are responsible for maintaining reliable internet connectivity with minimum 25 Mbps speed.

4. Communication
Employees must respond to messages within 2 hours during core hours. All meetings should be attended with camera on unless otherwise specified.

5. Performance
Remote work privileges are contingent on meeting performance expectations. Managers will review remote work arrangements quarterly.

6. Expenses
Home office setup stipend: $500 one-time. Monthly internet reimbursement: up to $50. Coworking space usage requires pre-approval."""
}


def chunk_fixed_size(text, size, overlap_pct):
    """Fixed-size chunking."""
    overlap = int(size * overlap_pct / 100)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        start = end - overlap if overlap > 0 else end
    return chunks


def chunk_sentence(text, sentences_per_chunk):
    """Sentence-based chunking."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i + sentences_per_chunk])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks


def chunk_paragraph(text):
    """Paragraph-based chunking."""
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


def chunk_qa_pairs(text):
    """Q&A pair chunking (for FAQ documents)."""
    pattern = r'(Q:.*?A:.*?)(?=Q:|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches if m.strip()]


def visualize_chunks(text, strategy, chunk_size, overlap_pct, sentences_per_chunk):
    """Generate chunk visualization."""
    if not text.strip():
        return "Please provide text to chunk.", "", ""

    # Apply chunking strategy
    if strategy == "Fixed Size":
        chunks = chunk_fixed_size(text, chunk_size, overlap_pct)
    elif strategy == "Sentence-Based":
        chunks = chunk_sentence(text, sentences_per_chunk)
    elif strategy == "Paragraph-Based":
        chunks = chunk_paragraph(text)
    elif strategy == "Q&A Pairs":
        chunks = chunk_qa_pairs(text)
    else:
        chunks = [text]

    if not chunks:
        return "No chunks generated. Try a different strategy.", "", ""

    # Calculate stats
    total_chars = sum(len(c) for c in chunks)
    avg_size = total_chars / len(chunks)
    min_size = min(len(c) for c in chunks)
    max_size = max(len(c) for c in chunks)

    # Check for problems
    problems = []
    split_sentences = 0
    for i, chunk in enumerate(chunks):
        if not chunk.rstrip().endswith(('.', '!', '?', '"')) and i < len(chunks) - 1:
            split_sentences += 1

    if split_sentences > 0:
        problems.append(f"⚠️ {split_sentences} chunks end mid-sentence")
    if min_size < 50:
        problems.append(f"⚠️ Some chunks are very small ({min_size} chars)")
    if max_size > 2000:
        problems.append(f"⚠️ Some chunks are very large ({max_size} chars)")

    # Stats display
    stats = f"""### Chunking Statistics

| Metric | Value |
|--------|-------|
| Total Chunks | {len(chunks)} |
| Average Size | {avg_size:.0f} characters |
| Min Size | {min_size} characters |
| Max Size | {max_size} characters |
| Total Characters | {total_chars} |

"""
    if problems:
        stats += "### ⚠️ Potential Issues\n" + "\n".join(problems)
    else:
        stats += "### ✅ No obvious issues detected"

    # Chunk display with color coding
    colors = ['#E6F7F5', '#D4F0EC', '#C2E9E3', '#B0E2DA', '#9EDBD1', '#8CD4C8', '#7ACDBF']
    chunk_display = "### Chunk Preview\n\n"

    for i, chunk in enumerate(chunks[:10]):  # Show first 10
        color = colors[i % len(colors)]
        ends_mid_sentence = not chunk.rstrip().endswith(('.', '!', '?', '"')) and i < len(chunks) - 1
        border = "2px solid #dc2626" if ends_mid_sentence else "1px solid #40B8A6"
        warning = " ⚠️ *ends mid-sentence*" if ends_mid_sentence else ""

        preview = chunk[:200] + "..." if len(chunk) > 200 else chunk
        chunk_display += f"**Chunk {i+1}** ({len(chunk)} chars){warning}\n```\n{preview}\n```\n\n"

    if len(chunks) > 10:
        chunk_display += f"*... and {len(chunks) - 10} more chunks*"

    return stats, chunk_display, f"Strategy: {strategy} | Chunks: {len(chunks)}"


def load_sample(sample_name):
    return SAMPLE_DOCS.get(sample_name, "")


# Build interface
with gr.Blocks(title="Chunking Visualizer", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# Chunking Visualizer\n\n"
        "**PM Decision:** Your engineering team says they'll 'chunk the documents.' "
        "This tool shows you exactly what that means and helps you spot potential problems "
        "before they affect retrieval quality.\n\n"
        "Try different strategies and see how they split your documents."
    )

    with gr.Row():
        with gr.Column(scale=1):
            sample_dropdown = gr.Dropdown(
                choices=list(SAMPLE_DOCS.keys()),
                label="Load Sample Document",
                value="FAQ Document"
            )
            text_input = gr.Textbox(
                label="Document Text",
                placeholder="Paste your document here...",
                lines=12,
                value=SAMPLE_DOCS["FAQ Document"]
            )

            strategy = gr.Radio(
                choices=["Fixed Size", "Sentence-Based", "Paragraph-Based", "Q&A Pairs"],
                label="Chunking Strategy",
                value="Fixed Size"
            )

            with gr.Row():
                chunk_size = gr.Slider(100, 1000, value=300, step=50, label="Chunk Size (chars)")
                overlap = gr.Slider(0, 50, value=10, step=5, label="Overlap (%)")

            sentences = gr.Slider(1, 10, value=3, step=1, label="Sentences per Chunk")

            visualize_btn = gr.Button("Visualize Chunks", variant="primary")

        with gr.Column(scale=1):
            summary_output = gr.Textbox(label="Summary", interactive=False)
            stats_output = gr.Markdown(label="Statistics")
            chunks_output = gr.Markdown(label="Chunks")

    # Events
    sample_dropdown.change(load_sample, sample_dropdown, text_input)

    visualize_btn.click(
        visualize_chunks,
        inputs=[text_input, strategy, chunk_size, overlap, sentences],
        outputs=[stats_output, chunks_output, summary_output]
    )

    # Auto-update on strategy change
    strategy.change(
        visualize_chunks,
        inputs=[text_input, strategy, chunk_size, overlap, sentences],
        outputs=[stats_output, chunks_output, summary_output]
    )

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** The right chunking strategy depends on your document type. "
        "FAQs work best with Q&A pair chunking. Product docs work with paragraph or sentence-based. "
        "Always test with real queries to verify retrieval quality.\n\n"
        "*AI for Product Managers*"
    )

if __name__ == "__main__":
    demo.launch()
