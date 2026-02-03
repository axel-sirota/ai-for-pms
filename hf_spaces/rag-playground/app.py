import gradio as gr
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import hashlib
import re

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB
chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))

# Sample documents
SAMPLE_DOCS = {
    "Support FAQ": """
Q: What is your return policy?
A: You can return most items within 30 days of purchase for a full refund. Items must be in original condition with tags attached. Electronics have a 15-day return window.

Q: How long does shipping take?
A: Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. Free shipping on orders over $50.

Q: How do I track my order?
A: Once your order ships, you'll receive an email with a tracking number. You can also log into your account to view order status.

Q: What payment methods do you accept?
A: We accept Visa, Mastercard, American Express, PayPal, and Apple Pay. All transactions are encrypted and secure.

Q: How do I contact customer support?
A: You can reach us via email at support@example.com, phone at 1-800-EXAMPLE, or live chat on our website. Support hours are 9am-6pm EST.
""",
    "Product Manual": """
Product: Smart Home Hub X1

Setup Instructions:
1. Unbox the device and connect the power adapter
2. Download the SmartHome app from your app store
3. Create an account or sign in
4. Press the pairing button on the hub for 5 seconds until the light blinks blue
5. Follow the in-app instructions to complete setup

Troubleshooting:
- If the hub won't connect: Ensure your WiFi is 2.4GHz (not 5GHz). The hub doesn't support 5GHz networks.
- If lights are unresponsive: Check that the hub firmware is updated in the app settings.
- If voice commands fail: Verify that your voice assistant is linked in the Integrations menu.

Specifications:
- Dimensions: 4" x 4" x 1.5"
- Weight: 8 oz
- Connectivity: WiFi 2.4GHz, Bluetooth 5.0, Zigbee
- Power: 5V DC, 2A adapter included
- Compatible with: Alexa, Google Home, Apple HomeKit

Warranty: 2-year limited warranty. Register at example.com/warranty within 30 days of purchase.
""",
    "Company Policy": """
Remote Work Policy - Effective January 2024

Eligibility:
All full-time employees who have completed their 90-day probation period are eligible for remote work. Certain roles requiring physical presence (e.g., facilities, reception) are exempt.

Guidelines:
- Core hours: All remote employees must be available 10am-3pm in their local timezone for meetings and collaboration.
- Equipment: The company provides a laptop and monitor. Employees are responsible for reliable internet (minimum 25 Mbps).
- Workspace: Employees must have a dedicated workspace that allows for video calls without disruption.

Expectations:
- Respond to messages within 2 hours during core hours
- Attend all scheduled meetings with camera on
- Complete weekly status updates in the project management tool
- Be available for occasional in-office days (minimum 2 per month)

Expenses:
- Home office stipend: $500 one-time for setup
- Internet reimbursement: Up to $50/month
- Coworking space: Pre-approved expenses reimbursed

Violations of this policy may result in revocation of remote work privileges.
"""
}


def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - overlap
    return [c for c in chunks if c]


def process_documents(doc_text, chunk_size, overlap_pct):
    """Process documents into chunks and store in ChromaDB."""
    overlap = int(chunk_size * overlap_pct / 100)
    chunks = chunk_text(doc_text, chunk_size, overlap)

    # Create unique collection name
    collection_name = f"docs_{hashlib.md5(doc_text.encode()).hexdigest()[:8]}"

    # Delete if exists
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

    collection = chroma_client.create_collection(name=collection_name)

    # Generate embeddings and store
    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=ids
    )

    return collection, chunks


def query_rag(question, doc_text, chunk_size, overlap_pct, top_k, use_openai):
    """Query the RAG system."""
    if not doc_text.strip():
        return "Please provide documents first.", "", ""

    # Process documents
    collection, chunks = process_documents(doc_text, chunk_size, overlap_pct)

    # Embed query
    query_embedding = model.encode([question]).tolist()

    # Retrieve
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, len(chunks))
    )

    retrieved_chunks = results['documents'][0]
    distances = results['distances'][0]

    # Format retrieved context
    context_display = ""
    for i, (chunk, dist) in enumerate(zip(retrieved_chunks, distances)):
        similarity = 1 - dist  # Convert distance to similarity
        context_display += f"**Chunk {i+1}** (similarity: {similarity:.2f})\n"
        context_display += f"```\n{chunk}\n```\n\n"

    # Generate answer
    context = "\n\n".join(retrieved_chunks)

    if use_openai and os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()

            prompt = f"""Based on the following context, answer the question. Only use information from the context. If the answer is not in the context, say "I don't have information about that in the provided documents."

Context:
{context}

Question: {question}

Answer:"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"OpenAI API error: {str(e)}. Using fallback response."
            answer += f"\n\nBased on the retrieved context, the relevant information is:\n{context[:500]}..."
    else:
        # Fallback: simple extractive response
        answer = f"**[Demo Mode - No API Key]**\n\nBased on semantic search, the most relevant information for your question is:\n\n{retrieved_chunks[0]}"
        if len(retrieved_chunks) > 1:
            answer += f"\n\nAdditional relevant context:\n{retrieved_chunks[1][:200]}..."

    # Groundedness analysis
    groundedness = f"Retrieved {len(retrieved_chunks)} chunks. Top similarity: {1-distances[0]:.2f}"

    return answer, context_display, groundedness


def load_sample(sample_name):
    """Load a sample document."""
    return SAMPLE_DOCS.get(sample_name, "")


# Build Gradio interface
with gr.Blocks(title="RAG Playground", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# RAG Playground\n\n"
        "**PM Decision:** Should your team build RAG? Use this to understand what they're "
        "proposing, see where it fails, and estimate costs before committing.\n\n"
        "Upload YOUR documents, ask questions, see how RAG retrieves and generates answers."
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Documents")
            sample_dropdown = gr.Dropdown(
                choices=list(SAMPLE_DOCS.keys()),
                label="Load Sample Document",
                value="Support FAQ"
            )
            doc_input = gr.Textbox(
                label="Document Text",
                placeholder="Paste your document here or select a sample above...",
                lines=10,
                value=SAMPLE_DOCS["Support FAQ"]
            )

            gr.Markdown("### 2. RAG Configuration")
            chunk_size = gr.Slider(100, 1000, value=500, step=50, label="Chunk Size (characters)")
            overlap = gr.Slider(0, 50, value=20, step=5, label="Overlap (%)")
            top_k = gr.Slider(1, 10, value=3, step=1, label="Chunks to Retrieve")
            use_openai = gr.Checkbox(label="Use OpenAI for generation (requires API key)", value=True)

        with gr.Column(scale=1):
            gr.Markdown("### 3. Ask a Question")
            question_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is the return policy?",
                lines=2
            )
            query_btn = gr.Button("Ask RAG", variant="primary")

            gr.Markdown("### 4. Results")
            answer_output = gr.Markdown(label="Generated Answer")

            with gr.Accordion("Retrieved Chunks", open=False):
                chunks_output = gr.Markdown()

            groundedness_output = gr.Textbox(label="Retrieval Stats", interactive=False)

    # Event handlers
    sample_dropdown.change(load_sample, sample_dropdown, doc_input)

    query_btn.click(
        query_rag,
        inputs=[question_input, doc_input, chunk_size, overlap, top_k, use_openai],
        outputs=[answer_output, chunks_output, groundedness_output]
    )

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** RAG quality depends on chunking and retrieval - ask your team "
        "how they're handling documents that don't fit neatly into chunks.\n\n"
        "*AI for Product Managers*"
    )

if __name__ == "__main__":
    demo.launch()
