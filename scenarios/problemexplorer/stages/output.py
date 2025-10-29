"""
Stage 6: Output Generation

Generates final markdown problem statement document.
"""

import re
from pathlib import Path

from amplifier.utils.logger import get_logger

from ..models import PipelineState

logger = get_logger(__name__)


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified string
    """
    slug = text.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


async def generate_output(state: PipelineState, output_dir: Path) -> Path:
    """Stage 6: Generate final markdown output.

    Args:
        state: Current pipeline state with complete problem_statement
        output_dir: Directory to write output file

    Returns:
        Path to generated output file
    """
    logger.info("\n📄 Stage 6: Generating output document...")

    if not state.problem_statement:
        raise ValueError("No problem statement to output")

    statement = state.problem_statement
    metrics = state.quality_metrics

    slug = slugify(statement.title)
    output_path = output_dir / f"problem-statement-{slug}.md"

    content = _generate_markdown(statement, metrics, state)

    output_path.write_text(content)

    logger.info(f"\n✅ Output generated: {output_path}")
    logger.info(f"   Title: {statement.title}")
    logger.info(f"   Dimensions: {len(statement.dimensions)}")
    logger.info(f"   Citations: {len(statement.all_citations)}")

    return output_path


def _generate_markdown(statement, metrics, state) -> str:
    """Generate markdown content for problem statement.

    Args:
        statement: ProblemStatement object
        metrics: QualityMetrics object
        state: PipelineState object

    Returns:
        Markdown formatted string
    """
    lines = []

    lines.append(f"# {statement.title}")
    lines.append("")
    lines.append(f"**Generated**: {state.updated_at[:10]}")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(statement.summary)
    lines.append("")

    lines.append("## Problem Dimensions")
    lines.append("")

    for i, dim in enumerate(statement.dimensions, 1):
        lines.append(f"### {i}. {dim.name}")
        lines.append("")
        lines.append(f"**Description**: {dim.description}")
        lines.append("")
        lines.append(f"**Importance**: {dim.importance}")
        lines.append("")

        if dim.citations:
            lines.append("**Evidence**:")
            lines.append("")
            for j, citation in enumerate(dim.citations, 1):
                lines.append(f"{j}. *{citation.title}*")
                lines.append(f"   - Source: [{citation.url}]({citation.url})")
                lines.append(f"   - Key finding: \"{citation.relevant_excerpt}\"")
                lines.append("")

    if statement.assumptions:
        lines.append("## Key Assumptions")
        lines.append("")
        for assumption in statement.assumptions:
            lines.append(f"- {assumption}")
        lines.append("")

    lines.append("## Quality Assessment")
    lines.append("")

    if metrics:
        lines.append(f"- **Overall Quality**: {metrics.overall_quality}")
        lines.append(f"- **Evidence Strength**: {metrics.evidence_strength}")
        lines.append(f"- **Coverage Score**: {metrics.coverage_score:.2f}")
        lines.append(f"- **Total Citations**: {metrics.citation_count}")
        lines.append(f"- **Dimensions Explored**: {metrics.dimension_count}")
        lines.append(f"- **Issues Found**: {metrics.issues_found}")
        lines.append("")

        if metrics.recommendations:
            lines.append("### Recommendations")
            lines.append("")
            for rec in metrics.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

    if state.validation_issues:
        lines.append("## Validation Issues")
        lines.append("")

        high_issues = [i for i in state.validation_issues if i.severity == "high"]
        medium_issues = [i for i in state.validation_issues if i.severity == "medium"]
        low_issues = [i for i in state.validation_issues if i.severity == "low"]

        if high_issues:
            lines.append("### High Severity")
            lines.append("")
            for issue in high_issues:
                lines.append(f"- **{issue.dimension}**: {issue.description}")
            lines.append("")

        if medium_issues:
            lines.append("### Medium Severity")
            lines.append("")
            for issue in medium_issues:
                lines.append(f"- **{issue.dimension}**: {issue.description}")
            lines.append("")

        if low_issues:
            lines.append("### Low Severity")
            lines.append("")
            for issue in low_issues:
                lines.append(f"- **{issue.dimension}**: {issue.description}")
            lines.append("")

    lines.append("## All Citations")
    lines.append("")

    for i, citation in enumerate(statement.all_citations, 1):
        lines.append(f"{i}. **{citation.title}**")
        lines.append(f"   - URL: [{citation.url}]({citation.url})")
        lines.append(f"   - Retrieved: {citation.fetch_timestamp[:10]}")
        lines.append(f"   - Excerpt: \"{citation.relevant_excerpt}\"")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"*Generated by ProblemExplorer - AI-Research-First Problem Statement Tool*")
    lines.append(f"*Search Budget: {state.searches_used}/{state.max_searches} searches used*")

    return "\n".join(lines)
