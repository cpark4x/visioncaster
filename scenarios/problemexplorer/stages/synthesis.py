"""
Stage 3: Synthesis

Synthesizes research findings into a structured problem statement with dimensions.
"""

from amplifier.utils.logger import get_logger

from ..models import Citation, PipelineState, ProblemDimension, ProblemStatement

logger = get_logger(__name__)


SYNTHESIS_PROMPT = """You are a research synthesis expert. Your task is to synthesize research findings into a structured problem statement.

# ORIGINAL PROBLEM STATEMENT
{problem}

# RESEARCH FINDINGS
{findings}

# YOUR TASK
Synthesize these findings into a comprehensive problem statement with clear dimensions.

Each dimension should:
- Represent a distinct facet/aspect of the problem
- Be supported by specific citations from the research
- Explain why this dimension matters

Output ONLY valid JSON (no other text) in this format:
{{
  "title": "concise problem title",
  "summary": "2-3 sentence overview of the problem",
  "dimensions": [
    {{
      "name": "Dimension name",
      "description": "What this dimension is about (2-3 sentences)",
      "importance": "Why this matters (1-2 sentences)",
      "citation_indices": [0, 2]
    }}
  ],
  "assumptions": ["key assumption 1", "key assumption 2"]
}}

The citation_indices should reference the findings by their index number (0-based).

Think about:
- What are the core facets of this problem?
- What does the evidence actually show?
- What assumptions are we making?
- What is well-supported vs speculative?

Synthesize now:"""


async def synthesize_statement(state: PipelineState) -> ProblemStatement:
    """Stage 3: Synthesize research into problem statement.

    Args:
        state: Current pipeline state with research_results

    Returns:
        Structured problem statement with dimensions
    """
    logger.info("\n📊 Stage 3: Synthesizing problem statement...")

    if not state.research_results:
        raise ValueError("No research results to synthesize")

    valid_results = [r for r in state.research_results if r.citation is not None]

    if not valid_results:
        raise ValueError("No valid research findings to synthesize")

    findings_text = _format_findings(valid_results)

    prompt = SYNTHESIS_PROMPT.format(
        problem=state.initial_problem,
        findings=findings_text,
    )

    # MVP: Use heuristic synthesis instead of AI
    logger.info("Using heuristic synthesis (MVP mode)")

    all_citations = [r.citation for r in valid_results if r.citation]

    # Create dimensions from research findings
    dimensions = []

    # Group findings by query purpose
    purpose_groups = {}
    for i, result in enumerate(valid_results):
        purpose = result.query.purpose
        if purpose not in purpose_groups:
            purpose_groups[purpose] = []
        purpose_groups[purpose].append((i, result))

    # Create a dimension for each purpose group
    for purpose, results in purpose_groups.items():
        dim_citations = [r.citation for _, r in results if r.citation]
        citation_indices = [i for i, _ in results]

        # Extract key themes from excerpts
        excerpts = [r.citation.relevant_excerpt for _, r in results if r.citation]
        combined_excerpt = " ".join(excerpts[:2])  # Use first 2 excerpts

        dimension = ProblemDimension(
            name=purpose,
            description=combined_excerpt[:300] + ("..." if len(combined_excerpt) > 300 else ""),
            importance=f"This dimension addresses: {purpose.lower()}",
            citations=dim_citations,
        )
        dimensions.append(dimension)

    # Create problem statement
    statement = ProblemStatement(
        title=f"Problem: {state.initial_problem[:80]}",
        summary=f"Research reveals multiple dimensions of this problem. {len(dimensions)} key aspects identified from {len(all_citations)} sources.",
        dimensions=dimensions,
        assumptions=[
            "Research findings are based on mock data (MVP mode)",
            "Real validation would require actual web search and AI synthesis",
        ],
        all_citations=all_citations,
    )

    logger.info(f"\nSynthesized problem statement:")
    logger.info(f"  Title: {statement.title}")
    logger.info(f"  Dimensions: {len(statement.dimensions)}")
    for i, dim in enumerate(statement.dimensions, 1):
        logger.info(f"    {i}. {dim.name} ({len(dim.citations)} citations)")

    return statement


def _format_findings(results: list) -> str:
    """Format research results for synthesis prompt.

    Args:
        results: List of ResearchResult objects with citations

    Returns:
        Formatted findings text
    """
    findings = []

    for i, result in enumerate(results):
        if result.citation:
            findings.append(f"""
[{i}] Query: {result.query.query}
    Purpose: {result.query.purpose}
    Source: {result.citation.title}
    URL: {result.citation.url}
    Evidence: {result.citation.relevant_excerpt}
""")

    return "\n".join(findings)
