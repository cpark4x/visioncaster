"""
Stage 4: Validation

Validates problem statement quality and identifies issues.
"""

from amplifier.utils.logger import get_logger

from ..models import PipelineState, ValidationIssue

logger = get_logger(__name__)


VALIDATION_PROMPT = """You are a quality validation expert. Your task is to critically review a problem statement for evidence quality.

# PROBLEM STATEMENT
Title: {title}
Summary: {summary}

# DIMENSIONS
{dimensions}

# YOUR TASK
Critically evaluate each dimension for evidence quality. Identify specific issues.

Output ONLY valid JSON (no other text) in this format:
{{
  "issues": [
    {{
      "dimension": "dimension name",
      "issue_type": "insufficient_evidence" | "weak_claim" | "unsupported",
      "description": "specific issue description",
      "severity": "low" | "medium" | "high"
    }}
  ],
  "overall_assessment": "brief assessment of the problem statement quality"
}}

Issue types:
- insufficient_evidence: Not enough citations or evidence
- weak_claim: Claims not strongly supported by evidence
- unsupported: Assertions made without any evidence

Be rigorous. A high-quality problem statement should have:
- At least 2 citations per dimension
- Clear connection between evidence and claims
- No unsupported assertions

Validate now:"""


async def validate_statement(state: PipelineState) -> list[ValidationIssue]:
    """Stage 4: Validate problem statement quality.

    Args:
        state: Current pipeline state with problem_statement

    Returns:
        List of validation issues found
    """
    logger.info("\n🔍 Stage 4: Validating problem statement...")

    if not state.problem_statement:
        raise ValueError("No problem statement to validate")

    statement = state.problem_statement

    dimensions_text = _format_dimensions(statement.dimensions)

    prompt = VALIDATION_PROMPT.format(
        title=statement.title,
        summary=statement.summary,
        dimensions=dimensions_text,
    )

    # MVP: Use heuristic validation instead of AI
    logger.info("Using heuristic validation (MVP mode)")

    issues = []

    # Check each dimension for quality issues
    for dim in statement.dimensions:
        citation_count = len(dim.citations)

        # Check for insufficient evidence
        if citation_count < 2:
            issues.append(
                ValidationIssue(
                    dimension=dim.name,
                    issue_type="insufficient_evidence",
                    description=f"Only {citation_count} citation(s) provided. Recommend at least 2 for robustness.",
                    severity="medium" if citation_count == 1 else "high",
                )
            )

        # Check for weak claims (short descriptions)
        if len(dim.description) < 100:
            issues.append(
                ValidationIssue(
                    dimension=dim.name,
                    issue_type="weak_claim",
                    description="Description is quite brief. Consider expanding with more specific details.",
                    severity="low",
                )
            )

    logger.info(f"\nValidation complete:")
    logger.info(f"  Issues found: {len(issues)}")

    if issues:
        high = sum(1 for i in issues if i.severity == "high")
        medium = sum(1 for i in issues if i.severity == "medium")
        low = sum(1 for i in issues if i.severity == "low")
        logger.info(f"    High: {high}, Medium: {medium}, Low: {low}")

        for issue in issues:
            logger.info(f"  [{issue.severity.upper()}] {issue.dimension}")
            logger.info(f"    {issue.issue_type}: {issue.description}")
    else:
        logger.info("  ✅ No issues found - statement is well-supported!")

    return issues


def _format_dimensions(dimensions: list) -> str:
    """Format dimensions for validation prompt.

    Args:
        dimensions: List of ProblemDimension objects

    Returns:
        Formatted dimensions text
    """
    text = []

    for i, dim in enumerate(dimensions, 1):
        text.append(f"""
## {i}. {dim.name}
Description: {dim.description}
Importance: {dim.importance}
Citations: {len(dim.citations)}

Evidence:
{_format_citations(dim.citations)}
""")

    return "\n".join(text)


def _format_citations(citations: list) -> str:
    """Format citations for display.

    Args:
        citations: List of Citation objects

    Returns:
        Formatted citations text
    """
    if not citations:
        return "  (No citations provided)"

    text = []
    for i, citation in enumerate(citations, 1):
        text.append(f"  [{i}] {citation.title}")
        text.append(f"      {citation.url}")
        text.append(f"      \"{citation.relevant_excerpt}\"")

    return "\n".join(text)
