# How to Create Your Own Tool Like This

**You don't need to be a programmer. You just need to describe what you want.**

This document shows you how ProblemExplorer was created with minimal input, so you can create your own tools the same way.

## What the Creator Did

The person who "created" this tool described their goal and thinking process to Amplifier. Here's what they actually did:

### Step 1: Described What They Wanted

They started by describing the problem and desired workflow:

> *I want a tool that takes a rough problem statement and turns it into an evidence-backed problem statement with citations.*
>
> *The key difference from traditional approaches: AI should do the research, not the human.*
>
> *The workflow should be:*
> 1. *Human provides a problem hunch (e.g., "users struggle with X")*
> 2. *AI decomposes this into 5-10 research queries*
> 3. *AI executes web searches for each query*
> 4. *AI extracts relevant evidence and citations*
> 5. *AI synthesizes findings into structured problem dimensions*
> 6. *AI validates that claims are supported by evidence*
> 7. *AI assesses overall quality and provides recommendations*
> 8. *Tool outputs formatted problem statement with full citations*
>
> *The tool should save state after each search so I can Ctrl+C anytime and resume later.*

That's it. **No code. No architecture diagrams. No technical specifications.**

### Step 2: Described the Thinking Process

Notice what they described:
1. "Decompose problem into research angles"
2. "Execute searches and collect evidence"
3. "Synthesize findings into dimensions"
4. "Validate evidence quality"
5. "Assess rigor and provide feedback"
6. "Generate final output"

This is what we call a **metacognitive recipe** - the "how should this tool think about the problem?"

They also specified:
- **Search budget**: Limit to 15 searches to prevent runaway costs
- **Iteration limit**: Allow 3 refinement cycles
- **Quality gates**: Don't proceed if evidence is insufficient
- **Incremental saves**: State persists after every search

### Step 3: Let Amplifier Build It

Amplifier:
- Used specialized agents (zen-architect, amplifier-cli-architect)
- Designed a 6-stage pipeline
- Implemented state management with resume capability
- Integrated web search via WebFetch
- Added validation and quality assessment
- Built the CLI interface
- Created documentation

**The creator didn't need to know:**
- How to make async API calls
- How to manage state persistence
- How to integrate web search tools
- How to structure a multi-stage pipeline
- How to implement quality gates
- Which Python libraries to use

### Step 4: Iterated to Refine

After testing, they provided feedback:
- "Searches are returning too generic results"
- "Need better extraction of relevant excerpts"
- "Quality metrics should be more strict"

Amplifier refined the implementation. Total time: one conversation session.

## How You Can Create Your Own Tool

### 1. Find a Need

Ask yourself:
- What repetitive research task takes too much time?
- What process would benefit from AI doing the heavy lifting?
- What workflow would be more effective if AI handled discovery?

**Examples:**
- "I need to research competitors for market analysis"
- "I need to validate technical assumptions with evidence"
- "I need to explore solution spaces for design problems"

### 2. Describe the Thinking Process

Not the code, the **thinking**. How should the tool approach the problem?

**Good example:**
> "First, decompose the design problem into key questions. Then, research each question by searching for case studies and best practices. Extract relevant design patterns. Synthesize into a decision framework with pros/cons. Validate that recommendations match evidence."

**Bad example:**
> "Use Python requests library to hit the Google API and parse JSON responses into a pandas DataFrame"

### 3. Start the Conversation

In your Amplifier environment:

```bash
claude
```

Then describe your goal:

```
I want to create a tool that [describes your goal and thinking process].

The workflow should be:
1. [First step - what the AI should do]
2. [Second step - how it builds on the first]
3. [Third step - quality checks or validation]
4. [Output - what format and what it contains]

It should save state incrementally so I can resume if interrupted.
```

### 4. Provide Feedback as Needed

When you try the tool, you'll likely find issues:
- "The research queries are too broad"
- "Citations aren't formatted well"
- "Need to filter out low-quality sources"

Just describe what's wrong in natural language. Amplifier will fix it.

### 5. Share It Back (Optional)

If your tool works well and others might benefit:
1. Document what it does (like this tool's README)
2. Document how you created it (like this file)
3. Contribute it back to the scenarios/ directory

## Real Examples of Tools You Could Create

### Research-First Tools

**Technical Feasibility Explorer**
- **What it does**: Takes a technical idea and researches feasibility
- **The recipe**: Decompose into technical questions → Search for implementations → Extract approaches → Assess feasibility → Identify risks
- **Why it's useful**: Validates ideas before investing engineering time

**Solution Space Mapper**
- **What it does**: Explores all possible approaches to a problem
- **The recipe**: Identify problem constraints → Search for existing solutions → Categorize approaches → Compare trade-offs → Recommend path
- **Why it's useful**: Prevents reinventing wheels or missing better approaches

**Competitive Intelligence Gatherer**
- **What it does**: Researches competitors' features and positioning
- **The recipe**: Identify competitors → Search for feature lists → Extract differentiators → Synthesize landscape → Identify opportunities
- **Why it's useful**: Automates competitive research

### Validation Tools

**Assumption Validator**
- **What it does**: Takes assumptions and finds evidence for/against
- **The recipe**: Parse assumptions → Generate search queries → Find evidence → Assess strength → Flag weak assumptions
- **Why it's useful**: Catches bad assumptions early

**Market Research Synthesizer**
- **What it does**: Gathers and synthesizes market data
- **The recipe**: Define market → Research size and trends → Find customer pain points → Identify opportunities → Generate report
- **Why it's useful**: Automates early market research

### Design Tools

**Design Pattern Explorer**
- **What it does**: Researches design patterns for specific problems
- **The recipe**: Understand problem → Search for patterns → Extract examples → Compare approaches → Recommend pattern
- **Why it's useful**: Accelerates design decisions with evidence

## The Key Principles

### 1. You Describe, Amplifier Builds

You don't need to know how to code. You need to know:
- What problem you're solving
- How to think through the problem (the metacognitive recipe)
- What good output looks like

### 2. AI-Research-First Is Powerful

Let AI do the discovery:
- Search for information
- Extract relevant bits
- Synthesize findings
- Validate quality

Human validates and guides, not executes.

### 3. Iteration Is Normal

Your first description won't be perfect. That's fine. Describe what's wrong, and Amplifier will fix it. This is **much faster** than trying to specify everything perfectly upfront.

### 4. Working Tools Beat Perfect Specs

The tools in this directory are experimental and ready to use, not production-perfect. They solve problems now. Improvements come later as needs emerge.

## Common Patterns for AI-Research Tools

### Pattern 1: Decompose → Research → Synthesize

```
Problem/Question
    ↓
[AI: Break into sub-questions]
    ↓
[AI: Research each question]
    ↓
[AI: Synthesize findings]
    ↓
Comprehensive Answer
```

### Pattern 2: Explore → Collect → Validate → Report

```
Topic/Domain
    ↓
[AI: Explore landscape]
    ↓
[AI: Collect evidence]
    ↓
[AI: Validate quality]
    ↓
Evidence-Backed Report
```

### Pattern 3: Hypothesis → Evidence → Assessment

```
Hypothesis/Assumption
    ↓
[AI: Search for evidence]
    ↓
[AI: Assess strength]
    ↓
Validation Result
```

## Getting Started

1. **Complete the [Amplifier setup](../../amplifier/README.md)**
2. **Think about what you need** - What research task takes too long?
3. **Describe your thinking process** - How should AI approach it?
4. **Start the conversation** - Describe your goal to Amplifier
5. **Iterate to refine** - Provide feedback as you use it
6. **Share it back** - Help others by contributing your tool

## Common Questions

**Q: Do I need to be a programmer?**
A: No. You need to understand the problem domain and be able to describe a thinking process. Amplifier handles all the implementation.

**Q: How long does it take?**
A: ProblemExplorer took one conversation session (a few hours including iteration). Your mileage may vary based on complexity.

**Q: What if I don't know how to describe the thinking process?**
A: Start with: "I want a tool that does X. It should first do A, then B, then C." Amplifier will help you refine from there.

**Q: Can I modify the code after Amplifier creates it?**
A: You can, but it's usually easier to describe what you want changed and let Amplifier update it. These tools follow the "describe and regenerate" pattern.

**Q: What if my tool idea is too complex?**
A: Break it into smaller pieces. Create a simple version first, then add features one at a time.

**Q: How do I handle API costs for web searches?**
A: Set a search budget (like ProblemExplorer's `--max-searches 15`). Monitor costs and adjust as needed.

## Next Steps

- **Try ProblemExplorer** to see what's possible
- **Brainstorm ideas** for your own research tools
- **Start a conversation** with Amplifier
- **Share what you create** so others can learn

---

**Remember**: The person who created this tool didn't write any code. They just described what they wanted and how it should think. You can do the same.

For more examples and guidance, see the [main scenarios README](../README.md).
