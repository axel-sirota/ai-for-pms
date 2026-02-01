# AI for Product Managers - Course Review & Restructuring Project

## Context

Axel (Data Trainers LLC) is preparing to deliver a **3-day "AI for Product Managers" course**. Previous versions received feedback that some parts were "not actionable" and some were "too deep" - need to find the right balance for a PM audience.

---

## The New Course Outline (Target State)

### Course Overview
- **Duration:** 3 days
- **Audience:** Product Managers
- **Goal:** Functional understanding of AI across classical ML, LLMs, and agentic systems
- **Prerequisite:** Google Colab account (free version)

### What the Course DOES Include:
- Clear understanding of when to use classical ML vs LLMs vs agents
- Practical skills: designing AI evaluations, estimating costs, managing AI projects
- Real-world applications: text generation, document understanding, forecasting, customer analysis
- Key concepts: RAG, prompt engineering, embeddings, agents, guardrails
- Ethical AI: hallucination mitigation, bias detection, compliance
- Stakeholder communication strategies

### What the Course Does NOT Include:
- In-depth coding or technical implementation
- Algorithm mathematics or neural network architecture internals
- Vendor-specific training (AWS SageMaker, Google Vertex AI)
- DevOps, CI/CD, Kubernetes details

### Course Sections (from outline):

**1. The AI Landscape**
- Three paradigms: Classical ML, LLMs, Agents
- Decision framework for product features
- Key players: OpenAI, Anthropic, Google, Meta, open-source
- Model landscape: GPT-4, Claude, Llama, Gemini
- Build vs Buy vs API decisions
- Hands-on: Map a product feature to appropriate AI paradigm

**2. Classical ML for Product Managers**
- When Classical ML wins: structured data, prediction, explainability
- Use cases: propensity models, fraud detection, forecasting, churn
- Data requirements: quality, quantity, labeling costs
- ML lifecycle and timelines
- Why models fail: overfitting, underfitting, data drift (conceptual only)
- Metrics: Precision, Recall, F1, RMSE, MAE
- Cost of errors in business terms
- Hands-on: Design success metrics for a prediction model

**3. LLMs: How They Work (Enough to Lead)**
- Tokens, context windows, cost/capability implications
- Temperature: creativity vs consistency
- Foundation vs fine-tuned vs prompted (PM decision tree)
- Prompt engineering: system vs user prompts, patterns (persona, few-shot, chain-of-thought)
- Prompt injection risks and defenses
- Embeddings and semantic understanding
- Hands-on: Design prompts for customer-facing text generation

**4. RAG: Building Knowledge-Grounded AI**
- Hallucination problem and how retrieval addresses it
- RAG vs fine-tuning vs prompting decision framework
- Use cases: form autofill, personalized responses, document Q&A
- Pipeline: Ingest → Chunk → Embed → Retrieve → Generate
- PM decisions: chunk size, retrieval depth, source prioritization, freshness
- Vector databases overview
- RAG failure modes: retrieval failures, generation failures
- Hands-on: Design RAG system for customer support

**5. AI Agents and Intelligent Automation**
- Copilots vs Agents distinction
- When to use each: risk tolerance, complexity, user trust
- ReAct pattern: Reason → Act → Observe → Repeat
- Tool use: API calls, database queries, form filling, search
- Multi-step workflows and error handling
- Human-in-the-loop design
- Building trust progressively
- UX patterns for AI transparency
- Hands-on: Design agent workflow with human checkpoints

**6. Evaluating AI Features**
- Why evaluation is the PM's job
- Classical ML evaluation: confusion matrix, A/B testing, drift detection
- LLM evaluation: task success, factuality, quality, compliance
- LLM-as-judge approach
- Feedback loops: explicit (thumbs up/down) and implicit (edit rate, send rate)
- When to use human annotation
- Hands-on: Design evaluation framework for text generation

**7. Guardrails, Safety, and Compliance**
- Financial services context: regulatory requirements, brand risk
- Cost of AI failures: legal, reputation, trust
- Input guardrails: prompt injection, PII detection, topic restrictions
- Output guardrails: hallucination detection, toxicity filtering, compliance checks
- Production guardrails: latency vs safety tradeoffs, logging, audit trails
- Incident response
- Hands-on: Design guardrails for customer-facing AI feature

**8. Cost, Timeline, and Project Management**
- Token pricing: input vs output, model tiers, volume discounts
- Cost drivers: context length, generation length, call frequency
- Cost optimization: caching, model routing, prompt efficiency
- Timeline reality for Classical ML, LLM features, and Agents
- Roles: Data Scientist, ML Engineer, Prompt Engineer
- Sprint planning for AI with uncertainty
- Go/no-go decisions
- Common pitfalls: underestimating evaluation, overpromising on demos, ignoring edge cases
- Hands-on: Create project plan and cost estimate

**9. Strategy and Stakeholder Communication**
- Decision tree: Rule-based → Classical ML → LLM → Agent
- When NOT to use AI
- Build vs buy vs partner
- ROI framework: time saved, accuracy improved, new capabilities
- Cost factors: development, compute, maintenance, risk mitigation
- Learning from failed AI projects
- Translating technical concepts to business language
- Managing expectations
- Communicating uncertainty honestly
- Hands-on: Prepare stakeholder presentation

---

## Current Materials Reviewed (Need More to Upload)

### Deck 1: Data Science Workflow (16 slides)
**Content:**
- Data science lifecycle diagram (Business Understanding → Data Acquisition → Modeling → Deployment)
- "What data scientists spend time doing" pie chart (60% cleaning, 19% collecting, etc.) - Source: CrowdFlower 2016
- Data Scientist vs ML Engineer distinction
- Team roles: DS, MLE, Product Developer, Data Analytics, PM/TPM, Policy
- Go/No-go meeting checklist
- Timeline visualization showing months for data work, weeks for ML/production
- Lab: Real estate price prediction scenario (Ames housing dataset)
- Data acquisition questions to ask
- Data cleansing cycle diagram

**Issues Identified:**
- Too process-heavy for PMs - teaches how to DO data science, not how to LEAD it
- Missing: What questions should PMs ask? What decisions do PMs make?
- Team roles slide is useful but needs PM-specific actions
- CrowdFlower 2016 source is outdated
- Lab is good concept but framing is for practitioners, not PMs

---

### Deck 2: Modelling (17 slides)
**Content:**
- Massive ML algorithm taxonomy tree (Bayesian, Decision Trees, Neural Networks, Clustering, etc.)
- Supervised vs Unsupervised visual comparison
- Data enriching examples (adding Sex column to Name/Age/Location data)
- Lab: Feature enriching for Ames dataset
- Overfitting/Underfitting visual progression (raw data → good fit → overfit → underfit)
- External link to r2d3.us visualization
- Train/test split diagram
- K-fold cross validation diagram
- Gradient descent visualization (cost function curve)
- 3D loss landscape visualization
- SF vs NY classification decision tree example

**Issues Identified:**
- Algorithm taxonomy is WAY too deep for PMs - they don't pick algorithms
- Gradient descent and loss landscapes are engineer-level detail
- K-fold cross validation is implementation detail PMs don't need
- Missing entirely: LLMs, agents, the three paradigms
- Good: Overfitting/underfitting concept (keep but simplify)
- Good: r2d3.us link is excellent for visual learners

---

### Deck 3: Applications (22 slides)
**Content:**
- Same ML algorithm taxonomy repeated
- For each algorithm family, shows:
  - Bayesian Methods: spam filtering, medical diagnosis, financial modeling
  - Decision Trees: credit scoring, customer segmentation, disease diagnosis
  - PCA: image compression, finance/risk, genomics
  - Instance-Based/k-NN: recommendations, medical diagnosis, pattern recognition
  - Clustering: market segmentation, medical imaging, document clustering
  - Regression: real estate pricing, demand forecasting, health risk
  - Rule-based systems: expert systems, fraud detection
  - Regularization: finance, healthcare, computer vision
  - Neural Networks: image/speech recognition, NLP, healthcare predictive analytics
  - Ensembles: weather forecasting, financial risk, biomedical research

**Issues Identified:**
- This is an algorithm catalog, not PM decision-making content
- PMs don't choose between Bayesian vs k-NN - they choose between approaches
- Missing: The PM decision framework (when would I use ML vs LLM vs agent for this feature?)
- Could be restructured around USE CASES instead of algorithms
- Finance examples are good given likely Bread Financial audience

---

### Deck 4: Metrics (8 slides)
**Content:**
- Lab: Fire detection model that always predicts "no fire" - is accuracy good?
- TP/TN/FP/FN definitions
- Lab: Categorize smoker/nonsmoker predictions
- Confusion matrix visual with emojis
- Precision/Recall/Accuracy/F1 formulas with visual
- Lab: What metrics for regression (predicting numbers)?
- Regression metrics: MAE, MSE, RMSE formulas

**Issues Identified:**
- Good foundation for classical ML metrics
- Fire detection example is excellent for teaching class imbalance
- Missing: LLM evaluation (hallucination detection, task success, LLM-as-judge)
- Missing: Business framing - what does a false positive cost in DOLLARS?
- Missing: Online metrics, A/B testing, drift detection
- Missing: Feedback loops (explicit and implicit)
- Formulas are fine but need business context

---

## Gap Analysis: Current Materials vs New Outline

### What to KEEP (with modifications):
1. **Team roles slide** - Add PM-specific actions and decisions
2. **Timeline visualization** - Update to include LLM and Agent timelines
3. **Overfitting/underfitting concept** - Simplify, focus on "what it means for your project"
4. **r2d3.us link** - Great visual resource
5. **Confusion matrix basics** - Add business cost framing
6. **Precision/Recall/F1** - Add "which matters for YOUR use case" framing
7. **Fire detection example** - Excellent, keep as-is
8. **Go/no-go checklist** - Expand for AI-specific considerations

### What to CUT:
1. ML algorithm taxonomy trees (appears 3x!)
2. Gradient descent / loss landscape visualizations
3. K-fold cross validation details
4. Algorithm-by-algorithm applications catalog
5. Data cleansing cycle details
6. Feature engineering specifics
7. Mathematical formulas without business context

### What to CREATE (New Content Needed):

**For Section 1 - AI Landscape:**
- Three paradigms comparison chart (Classical ML vs LLM vs Agent)
- Decision framework flowchart
- Model landscape overview (GPT-4, Claude, Llama, Gemini capabilities)
- Build vs Buy vs API decision matrix

**For Section 3 - LLMs:**
- Tokens and context windows explanation
- Temperature settings visual
- Prompt engineering patterns with examples
- System vs user prompt examples
- Prompt injection examples and defenses

**For Section 4 - RAG:**
- RAG pipeline diagram
- RAG vs fine-tuning vs prompting decision tree
- Failure modes examples
- Vector database conceptual overview

**For Section 5 - Agents:**
- Copilot vs Agent comparison
- ReAct pattern diagram
- Human-in-the-loop design patterns
- Trust progression framework

**For Section 6 - Evaluation:**
- LLM evaluation framework
- LLM-as-judge concept
- Feedback loop design
- Evaluation metrics by AI type (table)

**For Section 7 - Guardrails:**
- Input/Output/Production guardrails framework
- PII detection examples
- Compliance checklist for financial services
- Incident response playbook template

**For Section 8 - Cost & Timeline:**
- Token pricing calculator/example
- Cost optimization strategies
- Timeline templates by AI type
- Common pitfalls checklist

**For Section 9 - Strategy:**
- Full decision tree (Rule-based → ML → LLM → Agent)
- ROI calculation template
- Stakeholder communication templates
- "When NOT to use AI" checklist

---

## Key Reframing Needed

### From Data Scientist Perspective → To PM Perspective

| Current Framing | Needed Framing |
|----------------|----------------|
| "How to clean data" | "What questions to ask about data quality" |
| "Which algorithm to use" | "Which approach fits this product need" |
| "How to train a model" | "How long will this take and what could go wrong" |
| "Technical metrics (F1, RMSE)" | "Business impact of model errors in dollars" |
| "How ML works internally" | "What decisions do I need to make as PM" |
| "Algorithm taxonomy" | "Classical ML vs LLM vs Agent decision" |

---

## Additional Materials Reviewed

### Deck 5: Model Tour Part 1 (36 slides)

**Content:**
- **Linear Regression** with Bikeshare dataset
  - Equation of a line (y = mx + b)
  - Generalized formula with multiple variables and coefficients
  - Scatter plot: total_rentals vs temp_F with regression line
  - Seasonal factors warning (time series visualization)
- **Logistic Regression** with Window dataset (glass classification)
  - Binary classification: household glass (0/1)
  - Why linear regression fails for classification (line goes outside 0-1)
  - Sigmoid curve showing probability output
  - Logit function formulas (log odds)
  - "Less prone to outlier errors since we take log"
- **Decision Trees** with Window dataset
  - Full tree visualization with gini, samples, value, class at each node
  - Depth concept illustrated
  - Lab: "Will the tree above have perfect accuracy?"
- **KNN (K-Nearest Neighbors)** with Iris dataset
  - Petal/sepal measurements table and flower image
  - Scatter plot showing class separation
  - KNN process: pick K, find nearest, use majority vote
  - Classification maps for K=1, K=5, K=15 showing decision boundaries
  - Bias vs Variance chart (error vs K value)
- **Random Forests**
  - Cartoon trees "voting" on solubility (fun visual)
  - Architecture diagram: Dataset → Multiple trees → Majority voting → Final result
- **K-Means Clustering** with Iris dataset
  - Centroid-based algorithm explanation
  - Process: choose K, select random centroids, assign points, recompute, repeat
  - Elbow method chart for choosing K
  - 2D and 3D cluster visualizations

**Issues Identified:**
- Heavy on mathematical formulas (logit function, log odds equations)
- Good visualizations but presented at practitioner level, not PM level
- Missing: "Why should a PM care about this?" framing
- Missing: Business use case connections
- Good: Bikeshare is intuitive example
- Good: KNN classification maps show how K affects decisions
- Good: Bias/Variance tradeoff chart is essential concept
- Good: Random forest voting visual is accessible

**What to Keep:**
- Bikeshare example (simplify, remove formulas)
- Sigmoid curve (explains confidence scores)
- Decision tree visual (for explainability discussion)
- KNN classification maps (intuitive)
- Bias vs Variance chart (critical concept)
- Random Forest voting diagram
- K-Means elbow method (if covering segmentation)

**What to Cut:**
- All formulas (y = β₀ + β₁x₁..., logit, log odds)
- Logistic regression mathematical derivation
- Gini coefficient details in decision trees

---

### Deck 6: Model Tour Part 2 (18 slides)

**Content:**
- **Embeddings / Word Representations**
  - Spain → [1, 1], Russia → [-1, -1] vector example
  - 2D plot showing Spain and Russia as vectors
  - "Madrid should be closer to Spain than Russia"
  - Word cloud showing clustered concepts (city, food, travel, feeling, relative)
  - "Neural networks are great to find good embeddings"
- **Neural Networks basics**
  - "You and only you" → one-hot encoding [1,0,0], [0,1,0], etc.
  - Weighted sum: Z2 = w1*"you" + w2*"and" + w3*"only" + w4*"you"
  - Multi-dimensional representation (4 output nodes)
  - Input Layer → Hidden Layer → Output Layer diagram
- **CBOW (Continuous Bag of Words)**
  - "Hope can set you free" example
  - Predict center word from context window
  - Weight matrices W and W'
  - "We used this trick with windows to train it in an unlabeled fashion"
- **Fine-tuning concept**
  - Brain scan image showing pretrained layers vs replaced layers
  - "Reuse pretrained model on first layers, train the rest"
  - "Makes it possible to do magic with little data"
- **Classification with Neural Networks**
  - TensorFlow Playground separability examples
  - XOR-like pattern that linear can't solve
  - "More neurons == nonlinearities" - solving spiral dataset
  - 3 hidden layers, 8-8-5 neurons solving complex boundaries
- **Softmax**
  - MNIST digit classification example
  - Weight matrices, bias, softmax formula
  - Probability distribution over classes
- **Binary Cross Entropy**
  - Loss curve visualization
  - LogLoss formula

**Issues Identified:**
- Embeddings section is EXCELLENT - directly relevant for RAG explanation
- CBOW architecture is too deep for PMs
- Fine-tuning concept is important PM decision (prompt vs fine-tune vs train)
- TensorFlow Playground is great interactive resource
- Softmax and loss functions are implementation details PMs don't need
- Missing: Connection to LLM context (these are the same embeddings!)

**What to Keep:**
- Spain/Russia/Madrid embedding example (GOLD for RAG section)
- Word cloud clustering visual
- Fine-tuning concept (simplify)
- TensorFlow Playground reference
- "Neural networks find patterns humans can't specify"

**What to Cut:**
- CBOW architecture details
- Weight matrix mathematics
- Softmax formula
- Binary cross entropy / loss functions
- One-hot encoding details

---

### Deck 7: LLM Prompt Patterns (19 slides)

**Content:**
- **Configuration Parameters Table**
  | Parameter | Consequence | Usage | Importance |
  |-----------|-------------|-------|------------|
  | max-tokens | Limit output length | Keep answers concise | HIGH |
  | top-p | Only choose from top P probability | Limit creativeness | LOW |
  | top-k | Only choose from top K tokens | Limit creativeness | MEDIUM |
  | temperature | Control "hotness" / creativity | Limit creativeness | HIGH |

- **Persona Pattern**
  - "Act as a researcher expert on immunology"
  - ChatGPT screenshot showing immunology Q&A
  - "Extremely useful to get a new view on the project!"
  - Lab: Use persona for OKR/SMART goals questions; meditation planning

- **Cognitive Verifier Pattern**
  - "When asked a question, generate additional questions that would help answer more accurately"
  - ChatGPT screenshot showing clarifying questions for GenAI learning path
  - Lab: Apply to project planning or presentation outline

- **Few-Shot Pattern**
  - Sentiment analysis example:
    - Input: "I hate this movie" → Output: Negative
    - Input: "This movie has Keanu Reeves" → Output: Positive
    - Input: "Gross revenue 200M" → Output: Neutral
  - Driving scenarios with thought process:
    - Scenario: "Elk 80 feet over road" → Thought: "Elk too big to drive around" → Action: "Stop car"
    - Scenario: "Flooded street" → Thought: "Engine will break" → Action: "U turn"
  - "Never use more than 4/5 examples"
  - Lab: Sentiment analysis, situational questions

- **Game Play Pattern**
  - "Create a game around prompt engineering to identify improvements"
  - "Create a game around NLP to identify code improvements"
  - ChatGPT screenshot: "Code Optimizer's Quest" game with tokenization challenge
  - Lab: Refine prompts through game, refine email through game

**Issues Identified:**
- This deck is SOLID - right level for PMs
- Good hands-on labs with clear instructions
- ChatGPT screenshots make it tangible
- Missing: Chain-of-Thought pattern (mentioned in course outline)
- Missing: System prompt vs User prompt distinction
- Missing: Prompt injection risks and defenses
- Could add: Real business examples beyond immunology

**What to Keep:**
- Configuration parameters table (essential)
- All four patterns with examples
- All labs
- ChatGPT screenshots

**What to Add:**
- Chain-of-Thought pattern
- System prompt vs User prompt
- Prompt injection awareness (1-2 slides)
- Business-relevant examples

---

## Complete Gap Analysis: All Materials vs Course Outline

### Section-by-Section Coverage

| Section | What Outline Needs | What We Have | Gap Status |
|---------|-------------------|--------------|------------|
| **1. AI Landscape** | Three paradigms, decision framework, model landscape, build/buy/API | Nothing | 🔴 CREATE ALL |
| **2. Classical ML** | When ML wins, use cases, data requirements, lifecycle, metrics, business cost | Model Tour 1 (algorithms), Metrics deck | 🟡 RESTRUCTURE: Remove math, add PM framing, add business cost |
| **3. LLMs** | Tokens, context, temperature, prompts, patterns, embeddings, injection | Prompt Patterns (good), Model Tour 2 (embeddings) | 🟡 ADD: Tokens/context, chain-of-thought, injection risks |
| **4. RAG** | Hallucination, RAG pipeline, PM decisions, vector DBs, failure modes | Embeddings only (Model Tour 2) | 🔴 CREATE MOST |
| **5. Agents** | Copilots vs Agents, ReAct, tool use, human-in-loop, trust | Nothing | 🔴 CREATE ALL |
| **6. Evaluation** | ML eval, LLM eval, LLM-as-judge, feedback loops | Metrics deck (ML only) | 🟡 ADD: LLM evaluation, feedback loops |
| **7. Guardrails** | Input/output/production guardrails, compliance, incident response | Nothing | 🔴 CREATE ALL |
| **8. Cost & Timeline** | Token pricing, cost optimization, timelines by AI type, team roles | Data Science Workflow (partial) | 🟡 ADD: Token economics, LLM/Agent timelines |
| **9. Strategy** | Decision tree, when NOT to use AI, ROI, stakeholder communication | Nothing | 🔴 CREATE ALL |

### Material Usability Summary

| Material | Total Slides | Usable As-Is | Usable with Mods | Cut | Notes |
|----------|--------------|--------------|------------------|-----|-------|
| Data Science Workflow | 16 | 2 | 5 | 9 | Keep roles, timeline; cut process details |
| Modelling | 17 | 1 | 3 | 13 | Keep overfit/underfit, r2d3 link |
| Applications | 22 | 0 | 3 | 19 | Restructure around use cases, not algorithms |
| Metrics | 8 | 3 | 4 | 1 | Add business framing, LLM eval |
| Model Tour Part 1 | 36 | 4 | 10 | 22 | Keep visuals, cut all formulas |
| Model Tour Part 2 | 18 | 2 | 4 | 12 | Keep embeddings, cut CBOW/loss |
| LLM Prompt Patterns | 19 | 15 | 4 | 0 | Add CoT, system prompts, injection |
| **TOTAL** | **136** | **27 (20%)** | **33 (24%)** | **76 (56%)** | |

### Content Creation Required

**Must Create (No existing content):**
1. Section 1: AI Landscape (~15-20 slides)
   - Three paradigms comparison
   - Decision framework flowchart
   - Model landscape (GPT-4, Claude, Llama, Gemini)
   - Build vs Buy vs API matrix
   
2. Section 4: RAG (~15-20 slides)
   - Why RAG (hallucination problem)
   - RAG vs fine-tuning vs prompting decision
   - Pipeline diagram with PM decision points
   - Vector databases (conceptual)
   - Failure modes and detection
   
3. Section 5: Agents (~15-20 slides)
   - Copilot vs Agent distinction
   - ReAct pattern
   - Tool use examples
   - Human-in-the-loop patterns
   - Trust progression
   
4. Section 7: Guardrails (~12-15 slides)
   - Input guardrails (injection, PII, topic)
   - Output guardrails (hallucination, toxicity, compliance)
   - Production guardrails (latency, logging, audit)
   - Incident response
   
5. Section 9: Strategy (~10-12 slides)
   - Full decision tree
   - ROI framework
   - Stakeholder communication templates
   - When NOT to use AI

**Must Add to Existing:**
1. Section 3: Add to Prompt Patterns
   - Tokens and context windows (~3-4 slides)
   - Chain-of-thought pattern (~2 slides)
   - System vs User prompts (~2 slides)
   - Prompt injection risks (~2-3 slides)
   
2. Section 6: Add to Metrics
   - LLM evaluation framework (~4-5 slides)
   - LLM-as-judge (~2 slides)
   - Feedback loops (~2-3 slides)
   
3. Section 8: Add to Data Science Workflow
   - Token pricing and cost calculation (~3-4 slides)
   - LLM and Agent timelines (~2-3 slides)

---

## Hands-On Activities Inventory

### Existing Labs (from materials):
1. Persona Pattern: OKR/SMART goals, meditation planning
2. Cognitive Verifier: Project planning, presentation outline
3. Few-Shot: Sentiment analysis, situational questions
4. Game Play: Prompt refinement, email refinement
5. Model Tour 1: "How to tackle seasonal factors?" (regression)
6. Model Tour 1: "Will tree have perfect accuracy?" (decision trees)
7. Metrics: Fire detection accuracy analysis
8. Metrics: Smoker/nonsmoker categorization

### Labs Needed (from outline):
1. Section 1: Map product feature to AI paradigm
2. Section 2: Design success metrics for prediction model
3. Section 3: Design prompts for customer-facing text generation
4. Section 4: Design RAG system for customer support
5. Section 5: Design agent workflow with human checkpoints
6. Section 6: Design evaluation framework for text generation
7. Section 7: Design guardrails for customer-facing AI
8. Section 8: Create project plan and cost estimate
9. Section 9: Prepare stakeholder presentation

### Lab Gap Analysis:
- Section 3 labs exist (Prompt Patterns deck) ✅
- All other section labs need to be designed 🔴

---

## Recommended Restructure

### Day 1: Foundations

**Morning (3 hours):**
- Section 1: AI Landscape [CREATE NEW]
  - 45 min lecture + 30 min hands-on
  
**Afternoon (3 hours):**
- Section 2: Classical ML [RESTRUCTURE]
  - Use: Bikeshare visual (no formula), KNN maps, Bias/Variance chart
  - Add: Business cost framing
  - 60 min lecture + 30 min hands-on
  
- Section 3 Part 1: LLM Foundations [CREATE + EXISTING]
  - Create: Tokens, context windows
  - Use: Temperature/config table from Prompt Patterns
  - Use: Embeddings from Model Tour 2
  - 45 min lecture + 15 min discussion

### Day 2: Building AI Features

**Morning (3 hours):**
- Section 3 Part 2: Prompt Engineering [EXISTING + ADD]
  - Use: All Prompt Patterns content
  - Add: Chain-of-thought, system prompts, injection
  - 60 min lecture + 45 min hands-on (existing labs work)
  
**Afternoon (3 hours):**
- Section 4: RAG [CREATE NEW]
  - 60 min lecture + 30 min hands-on
  
- Section 5: Agents [CREATE NEW]
  - 60 min lecture + 30 min hands-on

### Day 3: Production & Strategy

**Morning (3 hours):**
- Section 6: Evaluation [RESTRUCTURE + ADD]
  - Use: Confusion matrix, precision/recall (with business framing)
  - Add: LLM evaluation, feedback loops
  - 60 min lecture + 30 min hands-on
  
- Section 7: Guardrails [CREATE NEW]
  - 45 min lecture + 30 min hands-on

**Afternoon (3 hours):**
- Section 8: Cost & Timeline [RESTRUCTURE + ADD]
  - Use: Team roles, timeline concepts
  - Add: Token economics, AI-specific timelines
  - 45 min lecture + 30 min hands-on
  
- Section 9: Strategy [CREATE NEW]
  - 45 min lecture + 30 min hands-on (stakeholder presentation)

---

## Priority Action List

### Immediate (Before Day 1):
1. Create Section 1: AI Landscape slides
2. Restructure Section 2: Remove formulas from Model Tour 1, add business framing
3. Create tokens/context windows content for Section 3
4. Add chain-of-thought to Prompt Patterns deck

### Before Day 2:
5. Create Section 4: RAG content
6. Create Section 5: Agents content
7. Add prompt injection slides to Section 3

### Before Day 3:
8. Add LLM evaluation to Section 6
9. Create Section 7: Guardrails
10. Add token economics to Section 8
11. Create Section 9: Strategy

### Labs to Design:
- Section 1 lab: Feature-to-paradigm mapping exercise
- Section 4 lab: RAG system design exercise
- Section 5 lab: Agent workflow design exercise
- Section 7 lab: Guardrails design exercise
- Section 8 lab: Project plan template
- Section 9 lab: Stakeholder presentation template

---

## Content Reuse Map

### Move This Content:
| From | To | Content |
|------|-----|---------|
| Model Tour Part 2 | Section 3 (LLMs) | Embeddings (Spain/Madrid example) |
| Model Tour Part 2 | Section 3 (LLMs) | Fine-tuning concept |
| Model Tour Part 1 | Section 2 (Classical ML) | Bikeshare visual (no formula) |
| Model Tour Part 1 | Section 2 (Classical ML) | KNN classification maps |
| Model Tour Part 1 | Section 2 (Classical ML) | Bias vs Variance chart |
| Model Tour Part 1 | Section 2 (Classical ML) | Random Forest voting diagram |
| Modelling deck | Section 2 (Classical ML) | Overfitting/underfitting visual |
| Data Science Workflow | Section 8 (Cost & Timeline) | Team roles slide |
| Data Science Workflow | Section 8 (Cost & Timeline) | Timeline visualization |

### Keep in Place:
- Prompt Patterns deck → Section 3 (mostly intact, add to it)
- Metrics deck → Section 6 (add business framing + LLM eval)

---

*Document updated: January 31, 2026*
*Status: Complete gap analysis with all materials reviewed*
