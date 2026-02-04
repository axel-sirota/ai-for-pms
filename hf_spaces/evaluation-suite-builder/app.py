"""
Evaluation Suite Builder - Design custom evaluation frameworks for AI features
Helps PMs create evaluation rubrics, test cases, and judge prompts
"""

import gradio as gr
import json

# Use case templates with recommended evaluation approaches
USE_CASE_TEMPLATES = {
    "customer_service": {
        "name": "Customer Service Bot",
        "description": "AI that responds to customer inquiries and resolves issues",
        "priority_dimensions": ["helpfulness", "accuracy", "tone", "resolution"],
        "recommended_metrics": [
            "Task completion rate",
            "Customer satisfaction (CSAT)",
            "First-response resolution rate",
            "Escalation rate",
            "Response relevance score"
        ],
        "test_case_categories": [
            "Simple FAQ questions",
            "Order status inquiries",
            "Complaint handling",
            "Refund requests",
            "Technical troubleshooting",
            "Edge cases (angry customers, unusual requests)"
        ],
        "judge_focus": "Focus on whether the response would actually resolve the customer's issue. Tone should be professional and empathetic. Accuracy of information is critical."
    },
    "content_generation": {
        "name": "Content Generation",
        "description": "AI that creates marketing copy, blog posts, or social media content",
        "priority_dimensions": ["creativity", "brand_voice", "engagement", "accuracy"],
        "recommended_metrics": [
            "Brand voice consistency score",
            "Engagement prediction",
            "Factual accuracy",
            "Readability score",
            "Human edit rate"
        ],
        "test_case_categories": [
            "Product descriptions",
            "Social media posts",
            "Email subject lines",
            "Blog introductions",
            "Ad copy variations",
            "Edge cases (sensitive topics, competitor mentions)"
        ],
        "judge_focus": "Evaluate creativity and engagement potential while maintaining brand voice. Check for factual claims that could be problematic."
    },
    "code_assistant": {
        "name": "Code Assistant",
        "description": "AI that helps developers write, debug, and explain code",
        "priority_dimensions": ["correctness", "efficiency", "clarity", "security"],
        "recommended_metrics": [
            "Code execution success rate",
            "Bug introduction rate",
            "Code review pass rate",
            "Explanation clarity score",
            "Security vulnerability detection"
        ],
        "test_case_categories": [
            "Simple function implementation",
            "Bug fixing",
            "Code explanation",
            "Refactoring suggestions",
            "Security-sensitive code",
            "Edge cases (ambiguous requirements, legacy code)"
        ],
        "judge_focus": "Code must be correct and runnable. Security issues are critical failures. Explanations should be clear to developers of varying skill levels."
    },
    "analysis_assistant": {
        "name": "Analysis Assistant",
        "description": "AI that analyzes data, documents, or situations and provides insights",
        "priority_dimensions": ["accuracy", "completeness", "clarity", "actionability"],
        "recommended_metrics": [
            "Factual accuracy rate",
            "Key insight coverage",
            "Actionable recommendation rate",
            "Source citation accuracy",
            "Logical consistency score"
        ],
        "test_case_categories": [
            "Data summarization",
            "Trend identification",
            "Comparison analysis",
            "Risk assessment",
            "Recommendation generation",
            "Edge cases (insufficient data, conflicting information)"
        ],
        "judge_focus": "Analysis must be logically sound and factually accurate. Conclusions should be supported by the data. Recommendations should be specific and actionable."
    }
}

# Evaluation dimension definitions
DIMENSION_DEFINITIONS = {
    "accuracy": {
        "name": "Accuracy",
        "description": "Is the information factually correct and verifiable?",
        "rubric_1": "Contains significant factual errors",
        "rubric_3": "Mostly accurate with minor errors",
        "rubric_5": "Completely accurate and verifiable"
    },
    "relevance": {
        "name": "Relevance",
        "description": "Does the response address what was actually asked?",
        "rubric_1": "Completely off-topic",
        "rubric_3": "Partially addresses the question",
        "rubric_5": "Directly and fully addresses the question"
    },
    "helpfulness": {
        "name": "Helpfulness",
        "description": "Would this actually help the user accomplish their goal?",
        "rubric_1": "Not helpful at all",
        "rubric_3": "Somewhat helpful but incomplete",
        "rubric_5": "Extremely helpful and actionable"
    },
    "clarity": {
        "name": "Clarity",
        "description": "Is the response well-organized and easy to understand?",
        "rubric_1": "Confusing and poorly structured",
        "rubric_3": "Understandable with some effort",
        "rubric_5": "Crystal clear and well-organized"
    },
    "tone": {
        "name": "Tone",
        "description": "Is the tone appropriate for the context?",
        "rubric_1": "Inappropriate tone",
        "rubric_3": "Acceptable but could be better",
        "rubric_5": "Perfect tone for the situation"
    },
    "completeness": {
        "name": "Completeness",
        "description": "Does the response cover all important aspects?",
        "rubric_1": "Missing critical information",
        "rubric_3": "Covers main points but missing some details",
        "rubric_5": "Comprehensive and thorough"
    },
    "creativity": {
        "name": "Creativity",
        "description": "Is the response original and engaging?",
        "rubric_1": "Generic and uninspired",
        "rubric_3": "Shows some creativity",
        "rubric_5": "Highly creative and engaging"
    },
    "safety": {
        "name": "Safety",
        "description": "Is the response free from harmful or inappropriate content?",
        "rubric_1": "Contains harmful content",
        "rubric_3": "Some potentially concerning elements",
        "rubric_5": "Completely safe and appropriate"
    }
}


def load_template(use_case):
    """Load a use case template"""
    if use_case not in USE_CASE_TEMPLATES:
        return "", "", [], "", ""

    template = USE_CASE_TEMPLATES[use_case]

    return (
        template["name"],
        template["description"],
        template["priority_dimensions"],
        "\n".join(f"- {m}" for m in template["recommended_metrics"]),
        template["judge_focus"]
    )


def generate_evaluation_suite(
    feature_name, feature_description, selected_dimensions,
    sample_size, evaluator_type, include_test_cases
):
    """Generate a complete evaluation suite"""

    if not feature_name or not selected_dimensions:
        return "Please provide a feature name and select at least one evaluation dimension."

    # Build the evaluation suite
    suite = f"# Evaluation Suite: {feature_name}\n\n"
    suite += f"**Feature Description:** {feature_description}\n\n"

    # Evaluation dimensions section
    suite += "## Evaluation Dimensions\n\n"
    for dim in selected_dimensions:
        if dim in DIMENSION_DEFINITIONS:
            d = DIMENSION_DEFINITIONS[dim]
            suite += f"### {d['name']}\n"
            suite += f"{d['description']}\n\n"
            suite += "**Rubric:**\n"
            suite += f"- 1-2: {d['rubric_1']}\n"
            suite += f"- 3-4: {d['rubric_3']}\n"
            suite += f"- 5: {d['rubric_5']}\n\n"

    # Sample size and evaluator recommendations
    suite += "## Evaluation Setup\n\n"
    suite += f"**Recommended Sample Size:** {sample_size} examples\n"
    suite += f"**Evaluator Type:** {evaluator_type}\n\n"

    if evaluator_type == "Human Only":
        suite += "**Evaluator Requirements:**\n"
        suite += "- 2-3 evaluators per sample for inter-rater reliability\n"
        suite += "- Calibration session before evaluation begins\n"
        suite += "- 10-20% overlap for reliability measurement\n"
        suite += "- Target Fleiss' Kappa > 0.4\n\n"
    elif evaluator_type == "LLM-as-Judge Only":
        suite += "**LLM Judge Setup:**\n"
        suite += "- Use GPT-4 or Claude as judge model\n"
        suite += "- Validate against human ratings on 50+ samples first\n"
        suite += "- Monitor for position and length bias\n"
        suite += "- Re-calibrate monthly\n\n"
    else:
        suite += "**Hybrid Approach:**\n"
        suite += "- LLM judge for initial screening (100% of samples)\n"
        suite += "- Human review for flagged samples and random 5-10%\n"
        suite += "- Calibrate LLM judge quarterly against human ratings\n\n"

    # Test cases section
    if include_test_cases:
        suite += "## Test Case Categories\n\n"
        suite += "Create test cases for each category:\n\n"
        suite += "1. **Happy Path** - Standard, expected inputs\n"
        suite += "2. **Edge Cases** - Unusual but valid inputs\n"
        suite += "3. **Adversarial** - Attempts to break or manipulate\n"
        suite += "4. **Domain-Specific** - Industry or use-case specific scenarios\n"
        suite += "5. **Failure Recovery** - How does it handle errors?\n\n"

    # Judge prompt section
    suite += "## LLM Judge Prompt Template\n\n"
    suite += "```\n"
    suite += f"You are evaluating an AI response for a {feature_name}.\n\n"
    suite += "**Evaluation Criteria:**\n"
    for dim in selected_dimensions:
        if dim in DIMENSION_DEFINITIONS:
            d = DIMENSION_DEFINITIONS[dim]
            suite += f"- {d['name']}: {d['description']}\n"
    suite += "\n"
    suite += "**Scoring:**\n"
    suite += "Rate each criterion from 1-5 with a brief explanation.\n"
    suite += "```\n"

    return suite


def export_as_json(
    feature_name, feature_description, selected_dimensions,
    sample_size, evaluator_type
):
    """Export evaluation config as JSON"""

    config = {
        "feature_name": feature_name,
        "feature_description": feature_description,
        "dimensions": selected_dimensions,
        "sample_size": sample_size,
        "evaluator_type": evaluator_type,
        "dimension_rubrics": {
            dim: DIMENSION_DEFINITIONS[dim]
            for dim in selected_dimensions
            if dim in DIMENSION_DEFINITIONS
        }
    }

    return json.dumps(config, indent=2)


# Build Gradio interface
with gr.Blocks(title="Evaluation Suite Builder", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Evaluation Suite Builder

    Design custom evaluation frameworks for your AI features. Get rubrics, sample sizes,
    evaluator recommendations, and judge prompts.

    **For Product Managers:** Use this to create evaluation plans before launching AI features.
    """)

    gr.Markdown(
        "> **PM Decision:** Your evaluation suite defines what 'good' means for your AI. "
        "Build it before you build the system - changing success criteria mid-project is expensive."
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Feature Details")

            template_dropdown = gr.Dropdown(
                choices=[
                    ("Customer Service Bot", "customer_service"),
                    ("Content Generation", "content_generation"),
                    ("Code Assistant", "code_assistant"),
                    ("Analysis Assistant", "analysis_assistant")
                ],
                label="Load Template (Optional)",
                value=None
            )

            feature_name = gr.Textbox(
                label="Feature Name",
                placeholder="e.g., Customer Support Chatbot"
            )

            feature_description = gr.Textbox(
                label="Feature Description",
                placeholder="What does this AI feature do?",
                lines=3
            )

            gr.Markdown("### 2. Evaluation Dimensions")

            dimensions = gr.CheckboxGroup(
                choices=[
                    ("Accuracy", "accuracy"),
                    ("Relevance", "relevance"),
                    ("Helpfulness", "helpfulness"),
                    ("Clarity", "clarity"),
                    ("Tone", "tone"),
                    ("Completeness", "completeness"),
                    ("Creativity", "creativity"),
                    ("Safety", "safety")
                ],
                value=["accuracy", "relevance", "helpfulness"],
                label="Select Dimensions to Evaluate"
            )

            gr.Markdown("### 3. Evaluation Setup")

            sample_size = gr.Radio(
                choices=["50 (Quick pilot)", "100 (Standard)", "250 (Thorough)", "500+ (Comprehensive)"],
                value="100 (Standard)",
                label="Sample Size"
            )

            evaluator_type = gr.Radio(
                choices=["Human Only", "LLM-as-Judge Only", "Hybrid (Recommended)"],
                value="Hybrid (Recommended)",
                label="Evaluator Type"
            )

            include_test_cases = gr.Checkbox(
                value=True,
                label="Include Test Case Categories"
            )

            generate_btn = gr.Button("Generate Evaluation Suite", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("### Your Evaluation Suite")
            output = gr.Markdown()

            with gr.Accordion("Export as JSON", open=False):
                json_output = gr.Code(language="json")
                export_btn = gr.Button("Export Config")

    gr.Markdown("""
    ---
    ### PM Checklist: Before Launching AI

    - [ ] Evaluation dimensions defined and prioritized
    - [ ] Rubric created with clear scoring criteria
    - [ ] Test cases covering happy path, edge cases, and adversarial inputs
    - [ ] Evaluator setup (human, LLM, or hybrid)
    - [ ] Baseline established from current solution or competitor
    - [ ] Success criteria defined (what score = launch-ready?)
    - [ ] Monitoring plan for post-launch evaluation
    """)

    # Event handlers
    template_dropdown.change(
        fn=load_template,
        inputs=[template_dropdown],
        outputs=[feature_name, feature_description, dimensions, gr.Textbox(visible=False), gr.Textbox(visible=False)]
    )

    generate_btn.click(
        fn=generate_evaluation_suite,
        inputs=[feature_name, feature_description, dimensions, sample_size, evaluator_type, include_test_cases],
        outputs=[output]
    )

    export_btn.click(
        fn=export_as_json,
        inputs=[feature_name, feature_description, dimensions, sample_size, evaluator_type],
        outputs=[json_output]
    )

if __name__ == "__main__":
    demo.launch()
