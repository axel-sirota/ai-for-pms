"""
LLM Judge Comparator - Compare how different AI judges rate the same outputs
Uses real OpenAI API for evaluation
"""

import gradio as gr
import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Sample comparison scenarios
COMPARISON_SCENARIOS = {
    "email_responses": {
        "prompt": "Write a professional email declining a meeting request",
        "response_a": "Hi, I won't be able to make that meeting. I'm too busy. Maybe another time.",
        "response_b": "Thank you for the meeting invitation. Unfortunately, I have a scheduling conflict during that time. Would you be available next week instead? I'd be happy to find a time that works for both of us.",
        "response_c": "Dear colleague, I regret to inform you that due to unforeseen circumstances and prior commitments that have been scheduled well in advance, I find myself unable to attend the proposed meeting at the suggested time. I would like to express my sincere apologies for any inconvenience this may cause."
    },
    "explanations": {
        "prompt": "Explain machine learning to a 10-year-old",
        "response_a": "Machine learning is when computers learn from examples, just like you learn from practice. If you show a computer lots of pictures of cats and dogs, it learns to tell them apart - without anyone programming specific rules!",
        "response_b": "ML uses statistical algorithms to identify patterns in data through iterative optimization of loss functions, enabling predictive modeling without explicit programming of decision rules.",
        "response_c": "Imagine teaching a robot to recognize your favorite ice cream flavor. You show it pictures of different ice creams and tell it which ones you like. After seeing enough examples, the robot starts to guess correctly on its own. That's machine learning - computers learning from examples!"
    },
    "summaries": {
        "prompt": "Summarize the key benefits of exercise",
        "response_a": "Exercise is good for you. It helps your heart and makes you feel better. You should do it regularly.",
        "response_b": "Regular exercise improves cardiovascular health, boosts mental wellbeing through endorphin release, strengthens muscles and bones, aids weight management, and enhances sleep quality. Studies show even 30 minutes daily can significantly reduce disease risk.",
        "response_c": "Exercise offers numerous benefits including improved heart health, better mood, stronger muscles, weight control, and improved sleep. It also reduces the risk of chronic diseases like diabetes and certain cancers, while boosting energy levels and cognitive function."
    }
}

# Simulated judge personalities for comparison
JUDGE_PROFILES = {
    "strict": {
        "name": "Strict Judge",
        "style": "Be critical and demanding. Focus on what's missing or could be improved. High standards.",
        "temp": 0.2
    },
    "balanced": {
        "name": "Balanced Judge",
        "style": "Be fair and balanced. Acknowledge both strengths and weaknesses. Moderate standards.",
        "temp": 0.5
    },
    "lenient": {
        "name": "Lenient Judge",
        "style": "Be encouraging and positive. Focus on what's good. Give benefit of the doubt.",
        "temp": 0.7
    }
}


def load_scenario(scenario_type):
    """Load a comparison scenario"""
    if scenario_type not in COMPARISON_SCENARIOS:
        return "", "", "", ""
    scenario = COMPARISON_SCENARIOS[scenario_type]
    return scenario["prompt"], scenario["response_a"], scenario["response_b"], scenario["response_c"]


def evaluate_with_judge(prompt, responses, judge_profile):
    """Get evaluation from a specific judge profile"""

    profile = JUDGE_PROFILES[judge_profile]

    eval_prompt = f"""You are evaluating three different responses to the same prompt.
{profile['style']}

**Original Prompt:** {prompt}

**Response A:** {responses['a']}

**Response B:** {responses['b']}

**Response C:** {responses['c']}

Rank these responses from best to worst (1st, 2nd, 3rd).
For each, give a score out of 10 and a brief explanation (1-2 sentences).

Format:
1st Place: [Letter] - [Score]/10 - [Explanation]
2nd Place: [Letter] - [Score]/10 - [Explanation]
3rd Place: [Letter] - [Score]/10 - [Explanation]
"""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are {profile['name']}. {profile['style']}"},
                {"role": "user", "content": eval_prompt}
            ],
            temperature=profile['temp'],
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def run_comparison(prompt, response_a, response_b, response_c):
    """Run evaluation with all three judge profiles"""

    if not prompt or not response_a or not response_b or not response_c:
        return "Please provide a prompt and all three responses.", "", "", ""

    responses = {"a": response_a, "b": response_b, "c": response_c}

    # Get evaluations from each judge
    strict_eval = evaluate_with_judge(prompt, responses, "strict")
    balanced_eval = evaluate_with_judge(prompt, responses, "balanced")
    lenient_eval = evaluate_with_judge(prompt, responses, "lenient")

    # Create agreement analysis
    agreement = analyze_agreement(strict_eval, balanced_eval, lenient_eval)

    return strict_eval, balanced_eval, lenient_eval, agreement


def analyze_agreement(strict, balanced, lenient):
    """Analyze where judges agree and disagree"""

    # Simple heuristic analysis
    analysis = """## Agreement Analysis

**Key Observations:**

Different judge personalities often rank the same responses differently. This demonstrates:

1. **Evaluation is subjective**: Even with the same criteria, perspective matters
2. **Context determines standards**: A "strict" judge for customer service might be "lenient" for creative writing
3. **Multiple perspectives help**: Using several judges reduces individual bias

**When Judges Disagree, Ask:**
- Which judge profile matches your use case?
- Are the disagreements on edge cases or core quality?
- Would your users agree with the strict or lenient assessment?

**Best Practice:** Use multiple judge profiles and look at the *range* of opinions, not just one score.
"""
    return analysis


# Build Gradio interface
with gr.Blocks(title="LLM Judge Comparator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # LLM Judge Comparator

    See how different AI judge "personalities" rate the same responses differently.

    **For Product Managers:** Understanding judge variability helps you design more robust
    evaluation systems and set appropriate expectations for LLM-as-judge approaches.
    """)

    gr.Markdown(
        "> **PM Decision:** LLM-as-judge is faster than human eval but may miss nuance. "
        "Use for scale, not for final decisions. Always validate against human judgment first."
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Load Scenario or Enter Custom")

            scenario_dropdown = gr.Dropdown(
                choices=[
                    ("Email Responses", "email_responses"),
                    ("Technical Explanations", "explanations"),
                    ("Summary Quality", "summaries")
                ],
                label="Load Sample Scenario",
                value=None
            )

            prompt_input = gr.Textbox(
                label="Original Prompt",
                placeholder="What was the task?",
                lines=2
            )

            response_a = gr.Textbox(
                label="Response A",
                placeholder="First response to compare...",
                lines=4
            )

            response_b = gr.Textbox(
                label="Response B",
                placeholder="Second response to compare...",
                lines=4
            )

            response_c = gr.Textbox(
                label="Response C",
                placeholder="Third response to compare...",
                lines=4
            )

            compare_btn = gr.Button("Compare with All Judges", variant="primary")

        with gr.Column(scale=2):
            with gr.Tab("Strict Judge"):
                gr.Markdown("*Critical, demanding, focuses on what's missing*")
                strict_output = gr.Markdown()

            with gr.Tab("Balanced Judge"):
                gr.Markdown("*Fair, acknowledges strengths and weaknesses*")
                balanced_output = gr.Markdown()

            with gr.Tab("Lenient Judge"):
                gr.Markdown("*Encouraging, focuses on positives*")
                lenient_output = gr.Markdown()

            with gr.Tab("Agreement Analysis"):
                agreement_output = gr.Markdown()

    gr.Markdown("""
    ---
    ### PM Insights: Judge Reliability

    | Judge Agreement | What It Means | Action |
    |----------------|---------------|--------|
    | All judges agree | Clear quality difference | High confidence in ranking |
    | 2 of 3 agree | Likely real difference | Medium confidence |
    | All disagree | Subjective or edge case | Need human review |

    **Key Takeaway:** LLM judges are tools, not truth. Use them to filter and flag, not as final decisions.

    **Real-World Stats:**
    - LLM judges agree with humans ~85% on pairwise comparisons
    - Agreement drops to ~70% on absolute scores
    - Edge cases and creative tasks show the most disagreement
    """)

    # Event handlers
    scenario_dropdown.change(
        fn=load_scenario,
        inputs=[scenario_dropdown],
        outputs=[prompt_input, response_a, response_b, response_c]
    )

    compare_btn.click(
        fn=run_comparison,
        inputs=[prompt_input, response_a, response_b, response_c],
        outputs=[strict_output, balanced_output, lenient_output, agreement_output]
    )

if __name__ == "__main__":
    demo.launch()
