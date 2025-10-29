# ProblemSpace

**Validate problem clarity before building solutions.**

ProblemSpace is an AI-powered tool that guides you through validating and documenting your problem before any solution is built. It ensures you have clear problem definition, evidence, success metrics, and stakeholder alignment.

## Why ProblemSpace?

Building the wrong thing is expensive. ProblemSpace helps you avoid this by:

- **Clarifying the real problem** - AI analysis identifies assumptions, gaps, and risks
- **Requiring evidence** - No guesswork, only validated problems worth solving
- **Defining success upfront** - Know how you'll measure if the solution works
- **Getting alignment** - Human review ensures stakeholder buy-in before building

## How It Works

ProblemSpace guides you through 6 stages:

1. **Capture** - Describe the problem in your own words
2. **Analyze** - AI identifies core problem, stakeholders, assumptions, and gaps
3. **Evidence** - Provide data, research, and validation
4. **Metrics** - Define measurable success criteria
5. **Review** - Human approval or request changes
6. **Output** - Generate final problem statement document

## Installation

ProblemSpace is part of the amplifier toolkit:

```bash
# If amplifier is symlinked in your project
cd your-project/
python -m scenarios.problemspace
```

## Usage

### Start New Session

```bash
python -m scenarios.problemspace
```

The tool will guide you through each stage interactively.

### Resume Session

If interrupted, resume where you left off:

```bash
python -m scenarios.problemspace --resume
```

### Start Fresh

Reset and start over:

```bash
python -m scenarios.problemspace --reset
```

### Verbose Logging

Enable detailed logging:

```bash
python -m scenarios.problemspace --verbose
```

## Session Management

ProblemSpace saves state after every operation to `.data/problemspace/<timestamp>/`:

```
.data/problemspace/20241028_143000/
├── state.json                           # Complete state
└── problem-statement-<slug>.md          # Final output (after approval)
```

You can safely interrupt (Ctrl+C) and resume later.

## Stage Details

### 1. Capture Stage

Interactive prompts collect:
- Problem description (required)
- Additional context (optional)
- Known constraints (optional)

**Input method:** Multi-line text (Ctrl+D to finish)

### 2. Analyze Stage

AI analyzes your problem and provides:
- Core problem statement (clarified)
- Identified stakeholders
- Hidden assumptions
- Potential risks
- Clarity score (0-10)
- Information gaps

**Gate:** Automatically passes to next stage

### 3. Evidence Stage

Interactive prompts for:
- User research findings
- Key data points
- Competitive analysis

**Gate:** Proceeds with or without evidence (tracks validation status)

### 4. Metrics Stage

Define success metrics across:
- Business metrics (revenue, cost, growth)
- User metrics (satisfaction, retention, completion)
- Technical metrics (performance, reliability, scale)

**Gate:** Requires at least one metric

### 5. Review Stage

Human review of complete problem statement:
- View full problem summary
- Approve or request changes
- Provide specific feedback

**Gate:** Must be approved to proceed

### 6. Output Stage

Generates final markdown document with:
- Complete problem statement
- All evidence and metrics
- Analysis and recommendations
- Approval status

## Output Format

Final problem statement includes:

```markdown
# Problem Statement

## Core Problem
[AI-clarified problem statement]

## Context
[Your provided context]

## Stakeholders
- [Identified stakeholders]

## Evidence
### User Research
### Key Data Points
### Competitive Analysis

## Success Metrics
### Business Metrics
### User Metrics
### Technical Metrics

## Analysis
- Clarity Score
- Assumptions
- Risks
- Identified Gaps

## Status
✅ APPROVED
```

## Integration with amplifier

ProblemSpace follows amplifier patterns:

- **State management** - Resumable sessions with JSON persistence
- **Stage-based pipeline** - Clear boundaries and gates
- **AI + Human** - AI for analysis, human for decisions
- **Defensive I/O** - Retry logic on file operations
- **Logging** - Uses amplifier logger

## Examples

### Example 1: Simple Problem

```bash
$ python -m scenarios.problemspace

Step 1: Describe the problem
What problem are you trying to solve?

Users are abandoning checkout after adding items to cart
^D

[AI Analysis shows 8.5/10 clarity score]
[Proceed through evidence and metrics]
[Review and approve]

✅ Problem statement saved: problem-statement-users-abandoning-checkout.md
```

### Example 2: Complex Problem with Iteration

```bash
$ python -m scenarios.problemspace

[Initial capture with vague problem]
[AI Analysis shows 3.2/10 clarity score - flags gaps]
[Add evidence and metrics]
[Review shows need for clarification]
[Save feedback and exit]

$ python -m scenarios.problemspace --resume

[Continue from review stage]
[Refine based on feedback]
[Re-submit for approval]
```

## Best Practices

1. **Be specific in capture** - The more context you provide, the better the AI analysis
2. **Provide real evidence** - Data beats opinions
3. **Define measurable metrics** - "Better UX" isn't measurable, "25% faster task completion" is
4. **Iterate based on gaps** - If AI flags gaps, gather that info before proceeding
5. **Get stakeholder input** - Use review stage to align with team

## When to Use ProblemSpace

✅ **Use ProblemSpace when:**
- Starting a new project or feature
- Problem feels unclear or debated
- Need stakeholder alignment
- Want to validate problem before building
- Defining product requirements

❌ **Don't use ProblemSpace when:**
- Problem is already well-documented and validated
- You're fixing a specific bug (scope too narrow)
- Building a prototype to discover the problem

## Architecture

ProblemSpace follows the "bricks and studs" pattern:

```
main.py              # Pipeline orchestrator (code for structure)
state.py             # State management (code for structure)
stages/              # Independent stage modules
├── capture.py       # Human input
├── analyze.py       # AI intelligence
├── evidence.py      # Human input
├── metrics.py       # Human input
├── review.py        # Human decision
└── output.py        # Code generation
```

Each stage:
- Has clear input/output contract
- Can be tested independently
- Saves state before proceeding
- Handles errors gracefully

## Troubleshooting

### AI Analysis Fails

If AI analysis fails, ProblemSpace uses a fallback analysis. The pipeline continues but with reduced clarity scoring. Consider:
- Checking network connection
- Verifying claude-code CLI is installed
- Running with --verbose for detailed logs

### Session Not Resuming

If `--resume` doesn't work:
- Check `.data/problemspace/` exists
- Verify state.json is valid JSON
- Use `--reset` to start fresh

### Low Clarity Scores

If AI gives low clarity scores (<5.0):
- Provide more specific problem description
- Add concrete examples
- Include context and constraints
- Consider the gaps AI identified

## Contributing

See `HOW_TO_CREATE_YOUR_OWN.md` for guidance on creating similar tools using the amplifier patterns.

## License

Part of the amplifier toolkit.
