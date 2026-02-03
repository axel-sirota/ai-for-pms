import gradio as gr

# Pricing data
EMBEDDING_PRICING = {
    "OpenAI text-embedding-3-small": 0.02,  # per 1M tokens
    "OpenAI text-embedding-3-large": 0.13,
    "OpenAI ada-002": 0.10,
    "Cohere embed-v3": 0.10,
    "Self-hosted (GPU cost)": 0.01,  # Estimated
}

VECTOR_DB_PRICING = {
    "Pinecone (Starter)": {"storage": 0.00, "queries": 0.0000, "note": "Free tier: 1 index, 100K vectors"},
    "Pinecone (Standard)": {"storage": 0.096, "queries": 0.0001, "note": "Per GB-hour storage + per query"},
    "Weaviate Cloud": {"storage": 0.08, "queries": 0.00008, "note": "Per GB-month + per query"},
    "Qdrant Cloud": {"storage": 0.05, "queries": 0.00005, "note": "Per GB-month + per query"},
    "Supabase pgvector": {"storage": 0.125, "queries": 0.00001, "note": "Database pricing + minimal query cost"},
    "Self-hosted": {"storage": 0.02, "queries": 0.00001, "note": "Server costs only"},
}

LLM_PRICING = {
    "GPT-4o": {"input": 2.50, "output": 10.00},
    "GPT-4o-mini": {"input": 0.15, "output": 0.60},
    "Claude 3.5 Sonnet": {"input": 3.00, "output": 15.00},
    "Claude 3.5 Haiku": {"input": 0.80, "output": 4.00},
    "Llama 3.1 70B (hosted)": {"input": 0.90, "output": 0.90},
    "Llama 3.1 8B (hosted)": {"input": 0.10, "output": 0.10},
}


def calculate_costs(
    num_docs,
    avg_doc_tokens,
    queries_per_day,
    chunks_per_query,
    embedding_model,
    vector_db,
    llm_model
):
    """Calculate monthly RAG costs."""

    # Document stats
    total_doc_tokens = num_docs * avg_doc_tokens
    tokens_per_chunk = 500  # Assumption
    chunks_per_doc = avg_doc_tokens / tokens_per_chunk
    total_chunks = int(num_docs * chunks_per_doc)

    # Embedding dimensions (affects storage)
    embedding_dims = 1536 if "OpenAI" in embedding_model else 1024

    # === One-time costs ===
    embed_cost_docs = (total_doc_tokens / 1_000_000) * EMBEDDING_PRICING[embedding_model]

    # === Monthly costs ===

    # Query embeddings
    query_tokens_month = queries_per_day * 30 * 100  # ~100 tokens per query
    embed_cost_queries = (query_tokens_month / 1_000_000) * EMBEDDING_PRICING[embedding_model]

    # Vector storage (bytes = dims * 4 bytes per float32)
    storage_gb = (total_chunks * embedding_dims * 4) / (1024**3)
    vdb = VECTOR_DB_PRICING[vector_db]
    storage_cost = storage_gb * vdb["storage"] * 30  # Monthly

    # Vector queries
    query_cost = queries_per_day * 30 * vdb["queries"]

    # LLM generation
    llm = LLM_PRICING[llm_model]
    context_tokens = chunks_per_query * tokens_per_chunk
    input_tokens_month = queries_per_day * 30 * (100 + context_tokens)  # query + context
    output_tokens_month = queries_per_day * 30 * 300  # ~300 token response

    llm_input_cost = (input_tokens_month / 1_000_000) * llm["input"]
    llm_output_cost = (output_tokens_month / 1_000_000) * llm["output"]
    llm_cost = llm_input_cost + llm_output_cost

    # Total monthly
    monthly_total = embed_cost_queries + storage_cost + query_cost + llm_cost

    # Cost per query
    cost_per_query = monthly_total / (queries_per_day * 30) if queries_per_day > 0 else 0

    # Build results
    breakdown = f"""## Monthly Cost Breakdown

| Component | Cost |
|-----------|------|
| Embedding (queries) | ${embed_cost_queries:.2f} |
| Vector DB Storage | ${storage_cost:.2f} |
| Vector DB Queries | ${query_cost:.2f} |
| LLM Generation | ${llm_cost:.2f} |
| **MONTHLY TOTAL** | **${monthly_total:.2f}** |

**Cost per query:** ${cost_per_query:.4f}

---

### One-Time Setup Cost
- Document embedding: **${embed_cost_docs:.2f}** ({total_doc_tokens:,} tokens)

### System Stats
- Total chunks: {total_chunks:,}
- Storage: {storage_gb:.2f} GB
- Monthly queries: {queries_per_day * 30:,}
"""

    # Insights
    insights = "## Insights\n\n"

    llm_pct = (llm_cost / monthly_total * 100) if monthly_total > 0 else 0
    if llm_pct > 80:
        insights += f"⚠️ **LLM costs are {llm_pct:.0f}% of total.** The vector DB is cheap - optimize the LLM first (model selection, caching, prompt efficiency).\n\n"

    if monthly_total > 1000:
        insights += "⚠️ **Monthly cost exceeds $1,000.** Consider:\n"
        insights += "- Caching common queries\n"
        insights += "- Using smaller models for simple queries\n"
        insights += "- Reducing chunks retrieved per query\n\n"

    if cost_per_query > 0.10:
        insights += f"⚠️ **Cost per query (${cost_per_query:.4f}) is high.** Compare to support ticket cost ($15-$25) to justify.\n\n"

    if llm_pct <= 80 and monthly_total <= 1000:
        insights += "✅ **Costs look reasonable.** Monitor actual usage after launch.\n\n"

    # Scaling projection
    scaling = f"""## Scaling Projection

| Scale | Queries/Day | Monthly Cost | Cost/Query |
|-------|-------------|--------------|------------|
| Current | {queries_per_day:,} | ${monthly_total:.2f} | ${cost_per_query:.4f} |
| 5x | {queries_per_day * 5:,} | ${monthly_total * 5:.2f} | ${cost_per_query:.4f} |
| 10x | {queries_per_day * 10:,} | ${monthly_total * 10:.2f} | ${cost_per_query:.4f} |
| 100x | {queries_per_day * 100:,} | ${monthly_total * 100:.2f} | ${cost_per_query:.4f} |

*Note: Per-query cost stays constant, but consider volume discounts and caching at scale.*
"""

    return breakdown, insights, scaling


# Build interface
with gr.Blocks(title="Vector DB Cost Calculator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# Vector DB Cost Calculator\n\n"
        "**PM Decision:** Before approving a RAG project, you need to understand the costs. "
        "This calculator helps you estimate monthly costs and identify where to optimize.\n\n"
        "Adjust the parameters to match your expected deployment."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Document Corpus")
            num_docs = gr.Slider(100, 100000, value=10000, step=100, label="Number of Documents")
            avg_tokens = gr.Slider(500, 10000, value=2000, step=500, label="Avg Tokens per Document")

            gr.Markdown("### Query Volume")
            queries = gr.Slider(100, 100000, value=1000, step=100, label="Queries per Day")
            chunks = gr.Slider(1, 20, value=5, step=1, label="Chunks Retrieved per Query")

        with gr.Column():
            gr.Markdown("### Technology Stack")
            embed_model = gr.Dropdown(
                choices=list(EMBEDDING_PRICING.keys()),
                value="OpenAI text-embedding-3-small",
                label="Embedding Model"
            )
            vdb = gr.Dropdown(
                choices=list(VECTOR_DB_PRICING.keys()),
                value="Pinecone (Standard)",
                label="Vector Database"
            )
            llm = gr.Dropdown(
                choices=list(LLM_PRICING.keys()),
                value="GPT-4o-mini",
                label="LLM for Generation"
            )

            calc_btn = gr.Button("Calculate Costs", variant="primary")

    with gr.Row():
        breakdown_output = gr.Markdown(label="Breakdown")

    with gr.Row():
        insights_output = gr.Markdown(label="Insights")

    with gr.Row():
        scaling_output = gr.Markdown(label="Scaling")

    calc_btn.click(
        calculate_costs,
        inputs=[num_docs, avg_tokens, queries, chunks, embed_model, vdb, llm],
        outputs=[breakdown_output, insights_output, scaling_output]
    )

    gr.Markdown(
        "---\n"
        "**PM Takeaway:** Vector databases are cheap - typically less than 20% of total cost. "
        "LLM generation is where the money goes. When optimizing costs, focus on: "
        "(1) caching, (2) model selection, (3) prompt length, (4) retrieval count.\n\n"
        "*AI for Product Managers*"
    )

if __name__ == "__main__":
    demo.launch()
