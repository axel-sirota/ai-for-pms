# A/B Test Simulator

Interactive tool for planning and analyzing A/B tests for AI features.

## Features

- **Sample Size Calculator**: Determine how many users you need based on baseline rate, expected lift, and statistical power
- **Test Simulation**: Run Monte Carlo simulations to see how tests behave
- **Significance Checker**: Analyze existing test results for statistical significance
- **Visual Explanations**: Understand p-values and effect sizes through interactive charts

## For Product Managers

This tool helps you:
- Plan A/B tests properly (avoid calling tests too early)
- Understand statistical power and sample sizes
- Interpret test results correctly
- Communicate findings to stakeholders

## Key Concepts

- **Baseline Rate**: Your current conversion/success rate
- **Minimum Detectable Effect (MDE)**: Smallest improvement worth detecting
- **Statistical Power**: Probability of detecting a real effect (typically 80%)
- **Confidence Level**: How sure you want to be (typically 95%)

## Rules of Thumb

| Expected Lift | Typical Sample Size | Notes |
|--------------|---------------------|-------|
| 5% | 3,000+ per group | Very hard to detect |
| 10% | ~800 per group | Standard test |
| 20% | ~200 per group | Easy to detect |

## Common Mistakes to Avoid

1. **Peeking**: Checking results too early inflates false positives
2. **Ignoring practical significance**: A statistically significant but tiny lift may not matter
3. **Testing on biased samples**: Results won't generalize
4. **Day-of-week effects**: Run tests for full weeks

## Part of AI for PMs Course - Section 6: Evaluation
