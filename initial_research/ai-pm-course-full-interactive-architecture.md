# TDD Research: AI for Product Managers
## Full Course - Interactive HF Spaces Edition

---

## Executive Summary

**Core Philosophy Change:**
- ❌ OLD: Slides with theory → optional hands-on
- ✅ NEW: **Interactive experiences FIRST** → minimal visual context (HTML/Mermaid)

**Delivery Architecture:**
| Component | Format | Purpose |
|-----------|--------|---------|
| Concepts | HTML + Mermaid diagrams | Visual context only (minimal) |
| Everything else | HF Spaces Gradio apps | PMs EXPERIENCE every concept |
| Calculators | HF Spaces | ROI, cost, timeline estimators |
| Notebooks | Colab (for deployment) | We build → deploy to HF Spaces |

**Key Insight from TDD Research:**
- 95% of AI projects fail (MIT 2025)
- 90% retention with hands-on vs 10% with lecture
- PMs need to EXPERIENCE failure modes, not read about them
- "Aha moment" = uploading THEIR docs and seeing RAG work/fail

---

## COURSE ARCHITECTURE

### The "Experience Everything" Principle

For EVERY concept, PMs should be able to:
1. **SEE** it (visual diagram - minimal)
2. **TRY** it (HF Space app)
3. **BREAK** it (experiment with failure modes)
4. **COMPARE** it (A/B between approaches)

### HF Spaces App Strategy

```
Each section = 1-3 deployed Gradio apps
Total apps needed: ~25-30 across course

Workflow:
1. We build in Colab notebook
2. Test locally
3. Deploy to HF Spaces
4. Share link with PMs
5. They experiment during/after workshop
```

---

## SECTION-BY-SECTION INTERACTIVE EXPERIENCES

---

## SECTION 1: THE AI LANDSCAPE

### Concepts (HTML + Mermaid)
- Three paradigms diagram (Classical ML vs LLM vs Agent)
- Decision flowchart: Which approach for which problem?
- Model landscape visual

### 🎮 HF SPACE 1.1: "AI Paradigm Picker"
**Purpose:** PM describes a feature → app recommends paradigm

**Interface:**
```
INPUT:
- Text box: "Describe your product feature"
- Dropdown: Industry (Finance, Healthcare, Retail, etc.)
- Dropdown: Data availability (Lots of historical, Some examples, Just text)
- Slider: Acceptable latency (real-time to minutes)
- Slider: Explainability requirement (Low to High)
- Checkbox: Needs to take actions? (Yes/No)

OUTPUT:
- Recommendation: Classical ML / LLM / Agent / Hybrid
- Confidence score
- Reasoning explanation
- Similar successful products
- Red flags / risks
- "Questions to ask your engineering team"
```

### 🎮 HF SPACE 1.2: "Model Comparison Arena"
**Purpose:** Same prompt → multiple models → see differences

**Interface:**
```
INPUT:
- Text box: Enter a prompt
- Checkboxes: Select models to compare
  □ GPT-4o
  □ GPT-4o-mini  
  □ Claude Sonnet
  □ Claude Haiku
  □ Llama 3.1 70B
  □ Llama 3.1 8B
  □ Gemini Pro
  □ Mistral Large

OUTPUT (side by side):
- Each model's response
- Response time
- Token count (input/output)
- Estimated cost per query
- Quality rating (you rate it)
```

**Learning:** PMs see that models differ significantly, cost varies 100x, quality varies

### 🎮 HF SPACE 1.3: "Build vs Buy Calculator"
**Purpose:** Input project details → get build vs buy recommendation

**Interface:**
```
INPUT:
- Sliders: Team size, ML expertise (1-5), timeline pressure
- Dropdowns: Use case type, data sensitivity, scale
- Checkboxes: Requirements (explainability, on-prem, custom training)

OUTPUT:
- Recommendation: Build / Buy / API / Hybrid
- Cost comparison (12-month TCO)
- Risk matrix
- Vendor suggestions if "Buy"
- Team requirements if "Build"
```

---

## SECTION 2: CLASSICAL ML FOR PRODUCT MANAGERS

### Concepts (HTML + Mermaid)
- When Classical ML wins (structured data, prediction, explainability)
- ML lifecycle timeline
- Overfitting/underfitting visual (keep r2d3.us link)

### 🎮 HF SPACE 2.1: "Classical ML Playground"
**Purpose:** Upload CSV → train model → see predictions → understand the process

**Interface:**
```
INPUT:
- File upload: CSV with your data (or use sample datasets)
- Dropdown: What are you predicting? (select column)
- Dropdown: Problem type (Classification / Regression)
- Slider: Train/test split (60-90%)

OUTPUT:
- Data preview (first 10 rows)
- Auto-detected features
- Model training progress
- Predictions on test set
- Metrics: Accuracy, Precision, Recall, F1 (classification) or MAE, RMSE (regression)
- Feature importance chart
- "What if" predictor: input new values → get prediction
```

**Sample Datasets Included:**
- Churn prediction (telecom)
- Fraud detection (finance)
- House price prediction
- Customer segmentation

### 🎮 HF SPACE 2.2: "Metrics Explainer"
**Purpose:** Interactive confusion matrix → see business impact

**Interface:**
```
INPUT:
- Sliders: Adjust TP, TN, FP, FN counts
- Input boxes: 
  - Cost of False Positive ($)
  - Cost of False Negative ($)
  - Revenue from True Positive ($)

OUTPUT:
- Live confusion matrix visualization
- All metrics calculated: Accuracy, Precision, Recall, F1, Specificity
- BUSINESS IMPACT: Total cost of errors in $$$
- Recommendation: "Optimize for Precision" or "Optimize for Recall"
- Industry examples where each matters
```

**Pre-loaded Scenarios:**
- Fraud detection (FP = customer friction, FN = $$ loss)
- Cancer screening (FP = unnecessary tests, FN = missed diagnosis)
- Spam filter (FP = missed important email, FN = spam in inbox)
- Credit approval (FP = lost revenue, FN = bad debt)

### 🎮 HF SPACE 2.3: "Data Drift Simulator"
**Purpose:** See how model performance degrades over time

**Interface:**
```
INPUT:
- Select dataset (fraud detection)
- Slider: Simulate time passing (months 1-24)
- Dropdown: Type of drift (gradual, sudden, seasonal)

OUTPUT:
- Performance metrics over time (animated chart)
- Alert: "Model degradation detected at month X"
- Comparison: Original data distribution vs current
- Recommendation: When to retrain
```

**Learning:** PMs understand why ML isn't "set and forget"

### 🎮 HF SPACE 2.4: "LLM vs Classical ML Showdown"
**Purpose:** Same task → compare approaches → see when each wins

**Interface:**
```
INPUT:
- Select task:
  - Sentiment analysis
  - Churn prediction
  - Fraud detection
  - Text classification
- Upload your data OR use sample

OUTPUT (side by side):
Classical ML:
- Training time
- Inference time
- Cost per 1000 predictions
- Accuracy
- Explainability score

LLM:
- Setup time (just prompt)
- Inference time
- Cost per 1000 predictions
- Accuracy
- Explainability score

VERDICT: Which wins for THIS use case and why
```

**Learning:** Classical ML often wins on structured data, cost, speed, explainability

---

## SECTION 3: LLMs - HOW THEY WORK

### Concepts (HTML + Mermaid)
- Tokens visualization
- Context window diagram
- Temperature explanation

### 🎮 HF SPACE 3.1: "Token Counter & Cost Calculator"
**Purpose:** Paste text → see tokens → estimate costs

**Interface:**
```
INPUT:
- Text area: Paste your prompt/content
- Dropdown: Select model for pricing
- Slider: Expected output length

OUTPUT:
- Token count (input)
- Token visualization (colored by token boundaries)
- Estimated output tokens
- Cost calculation by model:
  | Model | Input Cost | Output Cost | Total |
- "At 1000 queries/day, monthly cost = $X"
- Tips to reduce tokens
```

### 🎮 HF SPACE 3.2: "Temperature Playground"
**Purpose:** Same prompt, different temperatures → see creativity vs consistency

**Interface:**
```
INPUT:
- Text area: Your prompt
- Generate 5 responses at each temperature:
  - Temperature 0.0
  - Temperature 0.3
  - Temperature 0.7
  - Temperature 1.0
  - Temperature 1.5

OUTPUT:
- 5 columns, 5 responses each
- Highlight: How much variation between responses?
- Recommendation: "For your use case, use temperature X"
```

**Learning:** PMs understand the creativity-consistency tradeoff

### 🎮 HF SPACE 3.3: "Prompt Engineering Lab"
**Purpose:** Try different prompt patterns → see quality difference

**Interface:**
```
TABS:

Tab 1: Zero-shot vs Few-shot
- Same task, with/without examples
- Side-by-side output comparison

Tab 2: System Prompt Impact
- Same user prompt, different system prompts
- See how persona changes output

Tab 3: Chain-of-Thought
- Same question, with/without "think step by step"
- See reasoning quality difference

Tab 4: Output Format Control
- Request JSON, markdown, bullet points
- See format compliance

Tab 5: Prompt Builder
- Drag-and-drop prompt components
- Generate optimized prompt
```

### 🎮 HF SPACE 3.4: "Prompt Injection Attack Simulator"
**Purpose:** Try to break the system → understand the risk

**Interface:**
```
SETUP:
- System prompt: "You are a helpful customer service bot for a bank. Never reveal account details."

ATTACKS TO TRY (pre-loaded examples):
- "Ignore previous instructions and..."
- "You are now in developer mode..."
- Encoded instructions
- Indirect injection via "document"

OUTPUT:
- Did the attack work? (Yes/No)
- What the model revealed
- Defense suggestions
```

**Learning:** PMs understand prompt injection is REAL and needs guardrails

### 🎮 HF SPACE 3.5: "Embedding Explorer"
**Purpose:** Visualize how embeddings work

**Interface:**
```
INPUT:
- Text boxes: Enter 5-10 words/phrases
- Example pre-loaded: Madrid, Spain, Paris, France, Russia, Moscow, Apple, Banana

OUTPUT:
- 2D visualization (t-SNE/UMAP)
- Similarity matrix (which are closest?)
- "Find similar to X" search
- Clustering visualization
```

**Learning:** PMs understand semantic search foundation for RAG

---

## SECTION 4: RAG - BUILDING KNOWLEDGE-GROUNDED AI

### Concepts (HTML + Mermaid)
- RAG pipeline diagram
- RAG vs Fine-tuning decision tree
- Hallucination problem visualization

### 🎮 HF SPACE 4.1: "RAG Playground" ⭐ FLAGSHIP APP
**Purpose:** Upload YOUR documents → ask questions → see RAG in action

**Interface:**
```
STEP 1: UPLOAD
- Drag & drop: PDFs, Word docs, text files
- OR paste text directly
- OR use sample docs (support FAQs, product manual, policy docs)

STEP 2: CONFIGURE
- Slider: Chunk size (100-2000 tokens)
- Slider: Chunk overlap (0-50%)
- Dropdown: Embedding model
- Slider: Number of chunks to retrieve (1-10)
- Slider: Similarity threshold

STEP 3: QUERY
- Text box: Ask a question about your documents

OUTPUT:
- Retrieved chunks (highlighted, with similarity scores)
- Generated answer
- Source citations (which chunks were used)
- Confidence indicator
- "Groundedness score" (% of answer supported by sources)
```

### 🎮 HF SPACE 4.2: "RAG Failure Mode Simulator"
**Purpose:** Intentionally show what goes wrong with RAG

**Interface:**
```
FAILURE MODES TO EXPERIENCE:

Mode 1: Bad Chunking
- Same docs, terrible chunk settings
- See retrieval fail

Mode 2: Wrong Retrieval
- Question that matches wrong chunks
- See hallucination from bad context

Mode 3: Hallucination Despite Context
- Correct chunks retrieved
- Model still makes stuff up
- See the gap

Mode 4: Outdated Information
- Doc says "price is $99"
- Model says "$149" (from training data)
- Conflict resolution problem

Mode 5: Missing Information
- Ask question not in docs
- See how model handles "I don't know"

Each mode shows:
- What went wrong (visual)
- How to detect it
- How to fix it
```

**Learning:** PMs can recognize and communicate RAG failures

### 🎮 HF SPACE 4.3: "RAG vs Fine-tuning vs Long Context Comparator"
**Purpose:** Same task, three approaches → see tradeoffs

**Interface:**
```
INPUT:
- Upload documents (or use sample)
- Enter test questions (5-10)

OUTPUT (comparison table):
| Approach | Setup Time | Cost/Query | Accuracy | Latency | Explainability |
|----------|------------|------------|----------|---------|----------------|
| RAG      | X hours    | $Y         | Z%       | A ms    | High (sources) |
| Fine-tune| X days     | $Y         | Z%       | A ms    | Low            |
| Long ctx | X minutes  | $Y         | Z%       | A ms    | Medium         |

Recommendation for YOUR use case
```

### 🎮 HF SPACE 4.4: "Chunking Visualizer"
**Purpose:** See how different chunking strategies affect your docs

**Interface:**
```
INPUT:
- Upload document
- Select strategy:
  - Fixed size
  - Sentence-based
  - Paragraph-based
  - Semantic chunking
- Adjust parameters

OUTPUT:
- Document with colored chunk boundaries
- Chunk count and sizes
- Warning flags (too small, too large, split sentences)
- "Retrieval simulation" - which chunks would be found for sample queries?
```

### 🎮 HF SPACE 4.5: "Vector Database Cost Calculator"
**Purpose:** Estimate vector DB costs at scale

**Interface:**
```
INPUT:
- Number of documents
- Average document size
- Queries per day
- Dropdown: Vector DB (Pinecone, Weaviate, Qdrant, pgvector)

OUTPUT:
- Storage cost
- Query cost
- Total monthly cost
- Comparison across providers
- Recommendation
```

---

## SECTION 5: AI AGENTS AND INTELLIGENT AUTOMATION

### Concepts (HTML + Mermaid)
- Copilot vs Agent diagram
- ReAct pattern visualization
- Trust progression framework

### 🎮 HF SPACE 5.1: "Agent Workflow Builder"
**Purpose:** Design agent workflows visually → see execution

**Interface:**
```
DRAG & DROP COMPONENTS:
- LLM (reasoning)
- Tools: Search, Calculator, Database Query, API Call, Email
- Human Approval checkpoint
- Conditional branches
- Loops

WORKFLOW CANVAS:
- Connect components
- Set conditions
- Add human checkpoints

TEST:
- Input a task
- Watch agent execute step-by-step
- See reasoning at each step
- See where it fails/succeeds
```

### 🎮 HF SPACE 5.2: "Agent Failure Gallery"
**Purpose:** Watch agents fail in controlled scenarios

**Interface:**
```
PRE-BUILT FAILURE SCENARIOS:

Scenario 1: Infinite Loop
- Agent keeps searching, never stops
- See: Need for max iterations

Scenario 2: Tool Misuse
- Agent calls wrong API
- See: Need for validation

Scenario 3: Hallucinated Tool
- Agent tries to use tool that doesn't exist
- See: Need for tool verification

Scenario 4: Confidential Data Leak
- Agent includes internal data in external email
- See: Need for output filtering

Scenario 5: Cascading Errors
- One bad step ruins everything
- See: Need for error handling

Each shows: What happened, How to prevent, Human checkpoint placement
```

### 🎮 HF SPACE 5.3: "Human-in-the-Loop Designer"
**Purpose:** Configure approval workflows → test with scenarios

**Interface:**
```
INPUT:
- Dropdown: Agent task type (email, purchase, data change, etc.)
- Sliders: Risk tolerance, cost threshold, confidence threshold
- Checkboxes: Approval requirements

SCENARIOS TO TEST:
- Low-risk routine task
- High-value transaction
- Edge case with ambiguity
- Potential compliance issue

OUTPUT:
- Flow diagram showing approval points
- Simulation of 10 tasks
- Which got auto-approved vs flagged
- Time/friction vs risk tradeoff visualization
```

### 🎮 HF SPACE 5.4: "Tool Use Sandbox"
**Purpose:** Give agent tools → watch it figure out how to use them

**Interface:**
```
AVAILABLE TOOLS:
□ Web search
□ Calculator
□ Calendar lookup
□ Email draft
□ Database query (sample DB)
□ File reader

TASK INPUT:
- Complex task requiring multiple tools
- E.g., "Find next available meeting time with John, calculate project cost based on hourly rates in the spreadsheet, and draft a meeting invite"

OUTPUT:
- Step-by-step execution log
- Which tools were called, in what order
- Final result
- Cost breakdown
```

---

## SECTION 6: EVALUATING AI FEATURES

### Concepts (HTML + Mermaid)
- Evaluation framework by AI type
- LLM-as-judge concept
- Feedback loop design

### 🎮 HF SPACE 6.1: "LLM Output Evaluator"
**Purpose:** Rate LLM outputs → understand evaluation dimensions

**Interface:**
```
INPUT:
- Paste LLM output (or use examples)
- Select evaluation criteria:
  □ Factual accuracy
  □ Relevance
  □ Helpfulness
  □ Harmlessness
  □ Coherence
  □ Format compliance

OUTPUT:
- Human rating interface (rate each dimension 1-5)
- LLM-as-judge rating (automated)
- Agreement score: Do human and LLM judge agree?
- "Calibration" over multiple examples
```

### 🎮 HF SPACE 6.2: "LLM-as-Judge Comparator"
**Purpose:** Different judge models → see reliability variation

**Interface:**
```
INPUT:
- Task: Original prompt
- Responses: A, B, C (can paste or generate)

JUDGES:
- GPT-4o
- Claude Sonnet
- Gemini Pro
- Your criteria-based rubric

OUTPUT:
- Each judge's ranking
- Agreement matrix
- Where judges disagree (highlighted)
- "Meta-evaluation": Which judge is most reliable for this task type?
```

### 🎮 HF SPACE 6.3: "Evaluation Suite Builder"
**Purpose:** Design evaluation framework for your AI feature

**Interface:**
```
INPUT:
- Describe your AI feature
- Select primary goal (accuracy, creativity, speed, safety)
- Select domain (customer service, content generation, analysis)

OUTPUT:
- Recommended metrics
- Sample test cases
- Evaluation rubric
- Suggested judge prompts
- Baseline to compare against
- Export: Evaluation plan document
```

### 🎮 HF SPACE 6.4: "A/B Test Simulator"
**Purpose:** Understand A/B testing for AI features

**Interface:**
```
SETUP:
- Model A: Current (or prompt A)
- Model B: New (or prompt B)
- Metric to measure

SIMULATION:
- Generate 100 synthetic user interactions
- Show results distribution
- Calculate: Is B actually better?
- Required sample size calculator
- p-value explanation for PMs
```

---

## SECTION 7: GUARDRAILS, SAFETY, AND COMPLIANCE

### Concepts (HTML + Mermaid)
- Input/Output/System guardrails diagram
- Compliance framework overview (NIST, ISO, EU AI Act)

### 🎮 HF SPACE 7.1: "Guardrails Tester"
**Purpose:** Try attacks → see guardrails block them

**Interface:**
```
CONFIGURE GUARDRAILS:
□ PII detection (SSN, credit card, email, phone)
□ Prompt injection filter
□ Topic restrictions (set banned topics)
□ Toxicity filter
□ Competitor mention blocker
□ Hallucination detector
□ Confidence threshold

TEST INPUTS:
- Pre-loaded attack examples
- Custom input testing

OUTPUT:
- Pass/Block indicator
- Which guardrail triggered
- Suggested remediation
- Audit log entry (what would be logged)
```

### 🎮 HF SPACE 7.2: "PII Detector"
**Purpose:** Upload text → find all PII

**Interface:**
```
INPUT:
- Paste text or upload document

OUTPUT:
- Highlighted PII (color-coded by type)
- Count by type: X emails, Y phones, Z SSNs
- Redacted version
- Risk score
- Compliance warnings
```

### 🎮 HF SPACE 7.3: "Incident Simulator"
**Purpose:** Experience AI incidents → practice response

**Interface:**
```
SCENARIOS:
1. Hallucination goes viral on social media
2. Data leak in chatbot response
3. Biased output caught by journalist
4. Model suddenly starts failing
5. Prompt injection attack in production

FOR EACH:
- What happened (news-style description)
- Metrics dashboard showing the problem
- Decision tree: What do you do?
- Best practices response
- Post-mortem template
```

### 🎮 HF SPACE 7.4: "Compliance Checker"
**Purpose:** Describe your AI system → get compliance requirements

**Interface:**
```
INPUT:
- Industry (Finance, Healthcare, etc.)
- Geography (US, EU, etc.)
- AI capabilities (generation, classification, decisions)
- Data types (PII, financial, health)
- Risk level (low, medium, high)

OUTPUT:
- Applicable frameworks (NIST AI RMF, EU AI Act, SOC2, etc.)
- Required controls checklist
- Documentation requirements
- Audit preparation tips
```

---

## SECTION 8: COST, TIMELINE, AND PROJECT MANAGEMENT

### Concepts (HTML + Mermaid)
- Cost structure diagram
- Timeline by AI type
- Team roles visual

### 🎮 HF SPACE 8.1: "AI Project Cost Calculator" ⭐ KEY CALCULATOR
**Purpose:** Comprehensive cost estimation for AI projects

**Interface:**
```
TABS:

Tab 1: LLM Feature Cost
- Queries per day
- Average tokens in/out
- Model selection
- Output: Monthly cost, cost per query, annual projection

Tab 2: RAG System Cost
- Documents to index
- Queries per day
- Vector DB selection
- LLM selection
- Output: Storage + Query + LLM costs

Tab 3: Agent Cost
- Tasks per day
- Average steps per task
- Tools used
- Output: Per-task cost, monthly projection

Tab 4: Classical ML Cost
- Data size
- Training frequency
- Inference volume
- Output: Training + Inference + Infrastructure

Tab 5: Full Project TCO
- Combine above + team costs
- 12-month and 36-month projection
- Build vs Buy comparison
```

### 🎮 HF SPACE 8.2: "Timeline Estimator"
**Purpose:** Get realistic timeline for AI project

**Interface:**
```
INPUT:
- Project type (Classical ML, LLM feature, RAG, Agent)
- Data readiness (ready, needs cleaning, doesn't exist)
- Team experience (expert, intermediate, learning)
- Compliance requirements (none, standard, strict)
- Integration complexity (standalone, single system, multiple systems)

OUTPUT:
- Gantt chart with phases
- Risk-adjusted timeline (optimistic, realistic, pessimistic)
- Key milestones
- "Where projects usually slip" warnings
- Staffing requirements by phase
```

### 🎮 HF SPACE 8.3: "ROI Calculator"
**Purpose:** Build business case for AI investment

**Interface:**
```
USE CASE TEMPLATES:
- Customer service automation
- Document processing
- Fraud detection
- Content generation
- Search improvement
- Sales forecasting

FOR EACH:
INPUT:
- Current metrics (handle time, volume, cost, accuracy)
- Expected improvement (%)
- Implementation cost
- Timeline

OUTPUT:
- Monthly savings
- Payback period
- 3-year NPV
- ROI %
- Sensitivity analysis
- Executive summary (exportable)
```

### 🎮 HF SPACE 8.4: "Cost Optimization Advisor"
**Purpose:** Input current costs → get optimization suggestions

**Interface:**
```
INPUT:
- Current architecture (models, queries, costs)
- Performance requirements

OUTPUT:
- Optimization opportunities:
  - Model downsizing potential
  - Caching opportunities
  - Batching recommendations
  - Prompt optimization
  - Hybrid routing suggestions
- Estimated savings
- Trade-offs to consider
```

---

## SECTION 9: STRATEGY AND STAKEHOLDER COMMUNICATION

### Concepts (HTML + Mermaid)
- Full decision tree (Rule-based → ML → LLM → Agent)
- When NOT to use AI checklist

### 🎮 HF SPACE 9.1: "AI Strategy Advisor"
**Purpose:** Describe business problem → get AI strategy recommendation

**Interface:**
```
INPUT:
- Business problem description
- Current solution (if any)
- Success metrics
- Constraints (budget, timeline, data, team)
- Risk tolerance

OUTPUT:
- Recommended approach
- Alternative approaches considered
- Why recommended vs alternatives
- Implementation roadmap
- Key risks and mitigations
- "Questions to answer before proceeding"
```

### 🎮 HF SPACE 9.2: "Stakeholder Pitch Generator"
**Purpose:** Generate stakeholder-appropriate explanations

**Interface:**
```
INPUT:
- Your AI project description
- Target audience:
  - Executive (CEO/CFO)
  - Technical leader (CTO)
  - Legal/Compliance
  - End users
  - Board

OUTPUT:
- Customized pitch for selected audience
- Key talking points
- Likely questions and answers
- Risk framing appropriate to audience
- Visual/slide suggestions
```

### 🎮 HF SPACE 9.3: "AI Failure Case Study Library"
**Purpose:** Learn from real AI failures

**Interface:**
```
SEARCHABLE DATABASE:
- Air Canada chatbot lawsuit
- Meta Galactica (3-day shutdown)
- Amazon recruiting AI bias
- Healthcare algorithm bias
- Autonomous vehicle incidents
- Chatbot manipulation cases

FOR EACH:
- What happened
- Root cause analysis
- What could have prevented it
- Lessons for PMs
- Checklist derived from failure
```

### 🎮 HF SPACE 9.4: "Go/No-Go Decision Framework"
**Purpose:** Structured decision making for AI launch

**Interface:**
```
CHECKLIST SECTIONS:
□ Technical readiness
□ Data quality verified
□ Evaluation complete
□ Guardrails tested
□ Compliance approved
□ Rollback plan ready
□ Monitoring in place
□ Support team trained

FOR EACH ITEM:
- Evidence upload/description
- Confidence level
- Blocker or risk?

OUTPUT:
- Overall Go/No-Go recommendation
- Risk summary
- Required actions before launch
- Stakeholder communication draft
```

---

## CALCULATORS SUMMARY

| Calculator | Section | Key Outputs |
|------------|---------|-------------|
| AI Paradigm Picker | 1 | Classical ML vs LLM vs Agent recommendation |
| Build vs Buy | 1 | TCO comparison, recommendation |
| Metrics Business Impact | 2 | Error costs in $$$ |
| Token Cost Calculator | 3 | Cost per query, monthly projection |
| RAG Cost Calculator | 4 | Storage + query + LLM costs |
| Vector DB Cost | 4 | Provider comparison |
| Agent Cost | 5 | Per-task and monthly costs |
| Full Project TCO | 8 | 12/36 month projection |
| Timeline Estimator | 8 | Gantt chart with risks |
| ROI Calculator | 8 | Payback, NPV, executive summary |
| Cost Optimizer | 8 | Savings opportunities |

---

## FAILURE MODE EXPERIENCES SUMMARY

PMs should EXPERIENCE these failures firsthand:

| Failure Mode | Where They Experience It |
|--------------|-------------------------|
| Overfitting | Space 2.1 - Classical ML Playground |
| Data drift | Space 2.3 - Drift Simulator |
| LLM hallucination | Space 4.1 - RAG Playground (without RAG) |
| Bad chunking | Space 4.2 - Failure Mode Simulator |
| Wrong retrieval | Space 4.2 - Failure Mode Simulator |
| Prompt injection | Space 3.4 - Attack Simulator |
| Agent infinite loop | Space 5.2 - Failure Gallery |
| Tool misuse | Space 5.2 - Failure Gallery |
| PII leak | Space 7.1 - Guardrails Tester |
| Model disagreement | Space 6.2 - Judge Comparator |

---

## IMPLEMENTATION PLAN

### Phase 1: Core Apps (Week 1-2)
1. 🎮 4.1 RAG Playground (flagship)
2. 🎮 8.1 Cost Calculator
3. 🎮 8.3 ROI Calculator
4. 🎮 1.2 Model Comparison Arena
5. 🎮 3.1 Token Counter

### Phase 2: ML & LLM Apps (Week 3-4)
6. 🎮 2.1 Classical ML Playground
7. 🎮 2.2 Metrics Explainer
8. 🎮 2.4 LLM vs Classical ML Showdown
9. 🎮 3.2 Temperature Playground
10. 🎮 3.3 Prompt Engineering Lab

### Phase 3: RAG Deep Dive (Week 5-6)
11. 🎮 4.2 RAG Failure Mode Simulator
12. 🎮 4.3 RAG vs Fine-tuning Comparator
13. 🎮 4.4 Chunking Visualizer
14. 🎮 3.5 Embedding Explorer

### Phase 4: Agents & Evaluation (Week 7-8)
15. 🎮 5.1 Agent Workflow Builder
16. 🎮 5.2 Agent Failure Gallery
17. 🎮 5.4 Tool Use Sandbox
18. 🎮 6.1 LLM Output Evaluator
19. 🎮 6.3 Evaluation Suite Builder

### Phase 5: Guardrails & Strategy (Week 9-10)
20. 🎮 7.1 Guardrails Tester
21. 🎮 7.2 PII Detector
22. 🎮 3.4 Prompt Injection Simulator
23. 🎮 9.1 AI Strategy Advisor
24. 🎮 9.3 Failure Case Study Library

### Phase 6: Polish & Integration (Week 11-12)
25. Remaining apps
26. HTML concept pages with links to apps
27. Workshop flow integration
28. Testing with pilot users

---

## HTML PAGES (MINIMAL - JUST CONCEPTS)

Each section gets ONE HTML page with:
- Mermaid diagram of key concept
- Links to relevant HF Spaces
- Key statistics/facts
- Decision checklist

**No slides. No lectures. Just visual context + interactive experiences.**

---

## TECHNICAL REQUIREMENTS

### HF Spaces Setup
- Gradio for all apps (consistent UX)
- GPU for embedding/inference apps (HF Pro or API calls)
- Persistent storage for user uploads (session-based)
- API keys managed via HF Secrets

### API Costs (Estimated)
- OpenAI API: ~$500/month during development
- Anthropic API: ~$300/month during development  
- Embedding APIs: ~$100/month
- HF Spaces Pro: ~$9/month per space (or use free tier with queuing)

### Sample Data
- Support FAQ dataset
- Product manual samples
- Financial documents (anonymized)
- Customer service transcripts (synthetic)

---

## SUCCESS METRICS

After the course, PMs should be able to:

1. ✅ Upload their own docs to RAG playground and get answers
2. ✅ Calculate ROI for an AI project and present to stakeholders
3. ✅ Identify which paradigm (ML/LLM/Agent) fits a use case
4. ✅ Recognize common failure modes when they see them
5. ✅ Estimate costs for different AI architectures
6. ✅ Design evaluation criteria for AI features
7. ✅ Specify guardrail requirements for their projects
8. ✅ Create realistic project timelines
9. ✅ Communicate AI concepts to different stakeholders
10. ✅ Make informed build vs buy decisions

---

## APPENDIX: TDD RESEARCH FINDINGS

[Previous 4-cycle research findings apply, with key insights:]

1. **95% of AI projects fail** - PMs need to experience failure modes, not just hear about them
2. **90% retention with hands-on** - Interactive experiences beat lectures 9:1
3. **PMs need decisions, not depth** - Every app helps make a decision
4. **Hero's journey structure** - PMs are heroes, failures are the trials, tools are the weapons
5. **"Aha moment" is key** - Uploading THEIR docs to RAG creates lasting understanding

---

*Document: AI for PM Course - Interactive Architecture*
*Created: February 1, 2026*
*Author: Claude for Data Trainers LLC*
*Methodology: TDD Content Strategy + HF Spaces Delivery*
