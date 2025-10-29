# ProblemExplorer: AI-Research-First Problem Statements

**Turn vague hunches into evidence-backed problem statements.**

## The Problem

You have an idea that something is a problem, but:
- **Research takes forever** - Validating hunches requires hours of searching and reading
- **Evidence is scattered** - Insights are buried across dozens of sources
- **Synthesis is painful** - Connecting dots and structuring findings is tedious
- **Quality is uncertain** - Hard to know if your evidence actually supports your claims

## The Solution

ProblemExplorer is an AI-research-first tool that:

1. **AI does the research** - Decomposes your problem into queries and searches the web
2. **Discovers evidence** - Collects citations and excerpts from real sources
3. **Synthesizes dimensions** - Structures findings into problem facets with evidence
4. **Validates quality** - Checks that claims are actually supported
5. **Assesses rigor** - Provides metrics and recommendations for improvement
6. **Generates output** - Creates a formatted problem statement with full citations

**The result**: An evidence-backed problem statement with citations, in a fraction of the time.

## Quick Start

**Prerequisites**: Complete the [Amplifier setup instructions](../../amplifier/README.md) first.

**⚠️ MVP STATUS**: Currently uses mock search data. Real web search requires paid APIs or MCP server integration. See "Limitations" section below.

### Basic Usage

```bash
make problemexplorer PROBLEM="Users struggle to understand their energy consumption patterns"
```

Or run directly:

```bash
PYTHONPATH=./amplifier python3 -m scenarios.problemexplorer \
  --problem "Users struggle to understand their energy consumption patterns"
```

Or from a file:

```bash
PYTHONPATH=./amplifier python3 -m scenarios.problemexplorer \
  --problem-file my-problem.txt
```

The tool will:
1. Decompose your problem into research queries
2. Execute mock web searches (up to 15 by default)
3. Synthesize findings into structured dimensions
4. Validate evidence quality
5. Generate a problem statement document

### Your First Problem Statement

1. **Identify your hunch** - What problem do you think exists?

```txt
Users struggle to understand their monthly energy consumption patterns,
making it difficult to identify opportunities for savings.
```

2. **Run ProblemExplorer**:

```bash
python -m scenarios.problemexplorer \
  --problem "Users struggle to understand their energy consumption patterns"
```

3. **Review the output** - The tool generates `problem-statement-<slug>.md` in `.data/problemexplorer/<session>/`

4. **Check quality metrics** - The output includes:
   - Evidence strength rating
   - Coverage score
   - Validation issues
   - Recommendations for improvement

## Usage Examples

### Basic: Simple Problem

```bash
python -m scenarios.problemexplorer \
  --problem "Remote workers feel isolated from their teams"
```

**What happens**:
- AI generates 5-10 research queries
- Executes web searches for evidence
- Synthesizes findings into 3-5 problem dimensions
- Validates quality and provides metrics
- Outputs formatted problem statement

### Advanced: Custom Budget

```bash
python -m scenarios.problemexplorer \
  --problem-file complex-problem.txt \
  --max-searches 25 \
  --max-iterations 5
```

**What happens**:
- Uses more searches for thorough research
- Allows more refinement iterations
- Same validation and quality gates

### Resume Interrupted Session

```bash
python -m scenarios.problemexplorer --resume
```

**What happens**:
- Loads most recent session
- Continues from exact stopping point
- All searches and state preserved

## How It Works

### The Pipeline

```
Your Problem Hunch
        ↓
   [1. Capture] → AI generates research queries
        ↓
   [2. Research] → AI executes web searches (incremental saves)
        ↓
   [3. Synthesis] → AI structures findings into dimensions
        ↓
   [4. Validation] → AI checks evidence quality
        ↓
   [5. Metrics] → Calculate coverage and strength
        ↓
   [6. Output] → Generate formatted markdown
        ↓
Problem Statement Document
```

### Key Components

- **Problem Capture**: AI decomposes problem into 5-10 targeted research queries
- **Research Executor**: Runs web searches and extracts relevant evidence
- **Synthesizer**: Structures findings into problem dimensions with citations
- **Validator**: Checks that claims are supported by evidence
- **Quality Assessor**: Provides metrics and recommendations
- **Output Generator**: Creates markdown with full citations

### Why It Works

**Code handles the structure**:
- Pipeline orchestration and flow control
- State management with incremental saves
- Web search execution and retry logic
- Citation tracking and persistence
- Quality gate enforcement

**AI handles the intelligence**:
- Decomposing problems into research angles
- Extracting relevant information from sources
- Synthesizing findings into coherent dimensions
- Validating evidence quality
- Assessing overall rigor

This separation means the tool is both reliable (code manages workflow) and intelligent (AI does research and synthesis).

## Configuration

### Command-Line Options

```bash
# Required (one of):
--problem TEXT              # Problem statement inline
--problem-file PATH         # Path to file with problem statement

# Optional:
--resume                    # Resume most recent session
--reset                     # Start fresh (discard saved state)
--max-iterations N          # Max refinement iterations (default: 3)
--max-searches N            # Max web searches (default: 15)
--verbose                   # Enable detailed logging
```

### Session Data

All working files saved to `.data/problemexplorer/<timestamp>/`:
- `state.json` - Complete pipeline state for resume
- `problem-statement-<slug>.md` - Final output document

## Output Format

The generated problem statement includes:

- **Summary**: Overview of the problem
- **Dimensions**: Distinct facets with descriptions, importance, and citations
- **Assumptions**: Key assumptions made
- **Quality Assessment**: Metrics and recommendations
- **Validation Issues**: Any evidence gaps or weak claims
- **All Citations**: Complete list of sources with excerpts

Example:
```markdown
# Users Struggle to Understand Energy Consumption

**Generated**: 2024-10-28

## Summary
Users lack visibility into their energy consumption patterns...

## Problem Dimensions

### 1. Lack of Granular Data
**Description**: Most utility bills provide only monthly totals...
**Importance**: Without granular data, users cannot identify...
**Evidence**:
1. *Study finds 73% of consumers want real-time data*
   - Source: [https://example.com/study]
   - Key finding: "73% of surveyed consumers..."

### 2. Complex Presentation
...

## Quality Assessment
- **Overall Quality**: good
- **Evidence Strength**: strong
- **Coverage Score**: 0.75
- **Total Citations**: 12
```

## Current Limitations (MVP)

This tool is currently an **MVP with mock data**. Real production use requires addressing these limitations:

### Web Search

**Current**: Uses mock search results with example data
**Production Need**: One of:
- Paid search API (SerpAPI, ScaleSerp, etc.)
- Browser automation (Selenium/Playwright with anti-detection)
- MCP web search server integration
- Custom search scraping service

**Why**: Free web scraping from Python gets blocked/rate-limited by search engines (returns 202 status or empty results)

### AI Synthesis

**Current**: Uses heuristic synthesis and validation (no external AI)
**Production Need**: Integration with Claude API or similar for:
- Intelligent query generation
- Evidence extraction and synthesis
- Quality validation with nuanced judgment

**Implementation**: See [blog_writer](../blog_writer) for example of Claude API integration patterns

## Troubleshooting

### "Using mock search results"

This is expected behavior in MVP mode. The tool will generate a problem statement but with placeholder/example data.

### "Search budget exhausted"

**Problem**: Hit the search limit before completing research.

**Solution**: Increase with `--max-searches 25`

### "Quality gate not met"

**Problem**: Validation found high-severity issues.

**Solution**: This is working as intended - the tool will attempt refinement automatically (up to `--max-iterations`). Check the output for what issues were found.

## Learn More

- **[HOW_TO_CREATE_YOUR_OWN.md](./HOW_TO_CREATE_YOUR_OWN.md)** - Create your own tool like this
- **[Amplifier](https://github.com/microsoft/amplifier)** - The framework that powers these tools
- **[Scenario Tools](../)** - More tools like this one

## What's Next?

This tool demonstrates what's possible with AI-research-first workflows:

1. **Use it** - Generate evidence-backed problem statements
2. **Learn from it** - See [HOW_TO_CREATE_YOUR_OWN.md](./HOW_TO_CREATE_YOUR_OWN.md)
3. **Build your own** - Adapt the pattern for your domain
4. **Share back** - Contribute improvements!

---

**Built with Amplifier** - Following the "code for structure, AI for intelligence" philosophy. See [HOW_TO_CREATE_YOUR_OWN.md](./HOW_TO_CREATE_YOUR_OWN.md) for how this was created.
