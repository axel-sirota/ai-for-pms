"""
LLM Output Evaluator - Rate LLM outputs and compare with AI judge
Uses real OpenAI API for LLM-as-judge evaluation
"""

import gradio as gr
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Sample outputs for evaluation
SAMPLE_OUTPUTS = {
    "customer_service": {
        "prompt": "I ordered a laptop 2 weeks ago and it still hasn't arrived. What's going on?",
        "response": "I apologize for the delay with your laptop order. Let me look into this for you right away. Could you please provide your order number so I can check the shipping status? In the meantime, I want to assure you that we take delivery times seriously and will do everything we can to resolve this quickly."
    },
    "content_generation": {
        "prompt": "Write a product description for wireless earbuds.",
        "response": "Experience freedom with our premium wireless earbuds. Featuring crystal-clear audio, 8-hour battery life, and a comfortable ergonomic design, these earbuds are perfect for music lovers on the go. The intuitive touch controls let you manage calls and playlists effortlessly, while the IPX4 water resistance keeps you moving through any workout."
    },
    "technical_explanation": {
        "prompt": "Explain what an API is to a non-technical person.",
        "response": "Think of an API like a waiter at a restaurant. You (the customer) want food from the kitchen, but you can't just walk in there. The waiter takes your order, brings it to the kitchen, and returns with your food. An API does the same thing for software - it takes requests from one program, communicates with another system, and brings back the results. It's the messenger that lets different software talk to each other."
    },
    "analysis_task": {
        "prompt": "What are the main pros and cons of remote work?",
        "response": "Remote work offers flexibility and eliminates commuting, saving time and money. It can improve work-life balance and productivity for self-motivated individuals. However, it may lead to isolation, communication challenges, and difficulty separating work from personal life. Some people struggle with distractions at home, and team collaboration can suffer without in-person interaction."
    }
}

EVALUATION_CRITERIA = {
    "accuracy": "Is the information factually correct and verifiable?",
    "relevance": "Does the response directly address what was asked?",
    "helpfulness": "Would this response actually help the user accomplish their goal?",
    "clarity": "Is the response well-organized and easy to understand?",
    "tone": "Is the tone appropriate for the context?",
    "completeness": "Does the response cover all important aspects?"
}


def load_sample(sample_type):
    """Load a sample prompt and response for evaluation"""
    if sample_type not in SAMPLE_OUTPUTS:
        return "", ""
    sample = SAMPLE_OUTPUTS[sample_type]
    return sample["prompt"], sample["response"]


def evaluate_with_llm(prompt, response, criteria_weights):
    """Use OpenAI to evaluate the response"""

    if not prompt or not response:
        return "Please provide both a prompt and response to evaluate."

    # Build criteria list based on weights
    active_criteria = [c for c, w in criteria_weights.items() if w > 0]

    if not active_criteria:
        return "Please select at least one evaluation criterion."

    criteria_text = "\n".join([f"- {c.title()}: {EVALUATION_CRITERIA[c]}" for c in active_criteria])

    eval_prompt = f"""You are an expert evaluator. Rate the following AI response on a scale of 1-10 for each criterion.

**Original Prompt:** {prompt}

**Response to Evaluate:** {response}

**Evaluation Criteria:**
{criteria_text}

For each criterion, provide:
1. A score from 1-10
2. A brief explanation (1-2 sentences)

Format your response as:
[Criterion]: [Score]/10 - [Explanation]

End with an overall assessment (2-3 sentences).
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI evaluation expert. Be fair, specific, and constructive in your assessments."},
                {"role": "user", "content": eval_prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}\n\nMake sure OPENAI_API_KEY is set in HF Spaces secrets."


def calculate_weighted_score(human_scores, criteria_weights):
    """Calculate weighted average of human scores"""
    total_weight = sum(criteria_weights.values())
    if total_weight == 0:
        return 0

    weighted_sum = sum(
        human_scores.get(c, 0) * w
        for c, w in criteria_weights.items()
    )
    return weighted_sum / total_weight


def run_evaluation(
    prompt, response,
    accuracy_weight, relevance_weight, helpfulness_weight,
    clarity_weight, tone_weight, completeness_weight,
    human_accuracy, human_relevance, human_helpfulness,
    human_clarity, human_tone, human_completeness
):
    """Run both human and AI evaluation"""

    criteria_weights = {
        "accuracy": accuracy_weight,
        "relevance": relevance_weight,
        "helpfulness": helpfulness_weight,
        "clarity": clarity_weight,
        "tone": tone_weight,
        "completeness": completeness_weight
    }

    human_scores = {
        "accuracy": human_accuracy,
        "relevance": human_relevance,
        "helpfulness": human_helpfulness,
        "clarity": human_clarity,
        "tone": human_tone,
        "completeness": human_completeness
    }

    # Calculate human weighted score
    human_weighted = calculate_weighted_score(human_scores, criteria_weights)

    # Get AI evaluation
    ai_evaluation = evaluate_with_llm(prompt, response, criteria_weights)

    # Build human score summary
    human_summary = "## Your Ratings\n\n"
    for criterion, score in human_scores.items():
        weight = criteria_weights[criterion]
        if weight > 0:
            human_summary += f"- **{criterion.title()}**: {score}/10 (weight: {weight})\n"
    human_summary += f"\n**Weighted Average: {human_weighted:.1f}/10**"

    return human_summary, ai_evaluation


# Build Gradio interface
with gr.Blocks(title="LLM Output Evaluator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # LLM Output Evaluator

    Rate LLM outputs across multiple dimensions and compare your ratings with an AI judge.

    **For Product Managers:** This tool helps you understand evaluation dimensions and
    how AI judges compare to human assessment.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Select or Enter Content")

            sample_dropdown = gr.Dropdown(
                choices=[
                    ("Customer Service Response", "customer_service"),
                    ("Content Generation", "content_generation"),
                    ("Technical Explanation", "technical_explanation"),
                    ("Analysis Task", "analysis_task")
                ],
                label="Load Sample",
                value=None
            )

            prompt_input = gr.Textbox(
                label="Original Prompt",
                placeholder="What was the user asking for?",
                lines=3
            )

            response_input = gr.Textbox(
                label="Response to Evaluate",
                placeholder="Paste the LLM response here...",
                lines=6
            )

            gr.Markdown("### 2. Set Criteria Weights")
            gr.Markdown("*Set to 0 to disable a criterion*")

            accuracy_weight = gr.Slider(0, 10, value=8, step=1, label="Accuracy Weight")
            relevance_weight = gr.Slider(0, 10, value=9, step=1, label="Relevance Weight")
            helpfulness_weight = gr.Slider(0, 10, value=10, step=1, label="Helpfulness Weight")
            clarity_weight = gr.Slider(0, 10, value=7, step=1, label="Clarity Weight")
            tone_weight = gr.Slider(0, 10, value=5, step=1, label="Tone Weight")
            completeness_weight = gr.Slider(0, 10, value=6, step=1, label="Completeness Weight")

        with gr.Column(scale=1):
            gr.Markdown("### 3. Your Ratings (1-10)")

            human_accuracy = gr.Slider(1, 10, value=5, step=1, label="Accuracy")
            human_relevance = gr.Slider(1, 10, value=5, step=1, label="Relevance")
            human_helpfulness = gr.Slider(1, 10, value=5, step=1, label="Helpfulness")
            human_clarity = gr.Slider(1, 10, value=5, step=1, label="Clarity")
            human_tone = gr.Slider(1, 10, value=5, step=1, label="Tone")
            human_completeness = gr.Slider(1, 10, value=5, step=1, label="Completeness")

            evaluate_btn = gr.Button("Run Evaluation", variant="primary")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Your Assessment")
            human_output = gr.Markdown()
        with gr.Column():
            gr.Markdown("### AI Judge Assessment")
            ai_output = gr.Markdown()

    gr.Markdown("""
    ---
    ### PM Insights

    **Key Takeaways:**
    - Different criteria matter for different use cases (customer service = tone + helpfulness, technical = accuracy + clarity)
    - AI judges agree with humans ~85% of the time on relative comparisons, less on absolute scores
    - Weight criteria based on your product's priorities

    **Questions to Consider:**
    - Which dimensions are most important for YOUR AI feature?
    - Where do you and the AI judge disagree? Why might that be?
    - How would you scale this evaluation process?
    """)

    # Event handlers
    sample_dropdown.change(
        fn=load_sample,
        inputs=[sample_dropdown],
        outputs=[prompt_input, response_input]
    )

    evaluate_btn.click(
        fn=run_evaluation,
        inputs=[
            prompt_input, response_input,
            accuracy_weight, relevance_weight, helpfulness_weight,
            clarity_weight, tone_weight, completeness_weight,
            human_accuracy, human_relevance, human_helpfulness,
            human_clarity, human_tone, human_completeness
        ],
        outputs=[human_output, ai_output]
    )

if __name__ == "__main__":
    demo.launch()
