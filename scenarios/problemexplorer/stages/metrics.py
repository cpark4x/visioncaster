"""
Stage 5: Quality Metrics

Assesses overall quality and provides recommendations.
"""

from amplifier.utils.logger import get_logger

from ..models import PipelineState, QualityMetrics

logger = get_logger(__name__)


async def assess_quality(state: PipelineState) -> QualityMetrics:
    """Stage 5: Assess quality and generate metrics.

    Args:
        state: Current pipeline state with problem_statement and validation_issues

    Returns:
        Quality metrics with recommendations
    """
    logger.info("\n📈 Stage 5: Assessing quality metrics...")

    if not state.problem_statement:
        raise ValueError("No problem statement to assess")

    statement = state.problem_statement
    issues = state.validation_issues

    citation_count = len(statement.all_citations)
    dimension_count = len(statement.dimensions)

    avg_citations_per_dim = citation_count / dimension_count if dimension_count > 0 else 0

    evidence_strength = _calculate_evidence_strength(
        citation_count,
        dimension_count,
        issues,
    )

    coverage_score = _calculate_coverage_score(
        dimension_count,
        avg_citations_per_dim,
    )

    overall_quality = _determine_overall_quality(
        evidence_strength,
        coverage_score,
        len(issues),
    )

    recommendations = _generate_recommendations(
        issues,
        citation_count,
        dimension_count,
        avg_citations_per_dim,
    )

    metrics = QualityMetrics(
        evidence_strength=evidence_strength,
        coverage_score=coverage_score,
        citation_count=citation_count,
        dimension_count=dimension_count,
        issues_found=len(issues),
        overall_quality=overall_quality,
        recommendations=recommendations,
    )

    logger.info(f"\nQuality Assessment:")
    logger.info(f"  Overall Quality: {metrics.overall_quality}")
    logger.info(f"  Evidence Strength: {metrics.evidence_strength}")
    logger.info(f"  Coverage Score: {metrics.coverage_score:.2f}")
    logger.info(f"  Citations: {metrics.citation_count}")
    logger.info(f"  Dimensions: {metrics.dimension_count}")
    logger.info(f"  Issues: {metrics.issues_found}")

    if recommendations:
        logger.info(f"\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            logger.info(f"  {i}. {rec}")

    return metrics


def _calculate_evidence_strength(
    citation_count: int,
    dimension_count: int,
    issues: list,
) -> str:
    """Calculate evidence strength rating.

    Args:
        citation_count: Total number of citations
        dimension_count: Number of dimensions
        issues: List of validation issues

    Returns:
        Rating: "weak", "moderate", "strong"
    """
    high_severity_issues = sum(1 for i in issues if i.severity == "high")

    if high_severity_issues > 0:
        return "weak"

    avg_citations = citation_count / dimension_count if dimension_count > 0 else 0

    if avg_citations >= 3:
        return "strong"
    elif avg_citations >= 2:
        return "moderate"
    else:
        return "weak"


def _calculate_coverage_score(
    dimension_count: int,
    avg_citations_per_dim: float,
) -> float:
    """Calculate coverage score (0-1).

    Args:
        dimension_count: Number of dimensions
        avg_citations_per_dim: Average citations per dimension

    Returns:
        Score between 0 and 1
    """
    dimension_score = min(dimension_count / 5.0, 1.0)

    citation_score = min(avg_citations_per_dim / 3.0, 1.0)

    return (dimension_score + citation_score) / 2.0


def _determine_overall_quality(
    evidence_strength: str,
    coverage_score: float,
    issue_count: int,
) -> str:
    """Determine overall quality rating.

    Args:
        evidence_strength: Evidence strength rating
        coverage_score: Coverage score (0-1)
        issue_count: Number of validation issues

    Returns:
        Rating: "needs_work", "acceptable", "good", "excellent"
    """
    if evidence_strength == "weak" or coverage_score < 0.4:
        return "needs_work"

    if issue_count > 5:
        return "needs_work"
    elif issue_count > 2:
        return "acceptable"

    if evidence_strength == "strong" and coverage_score >= 0.8:
        return "excellent"
    elif evidence_strength == "strong" or coverage_score >= 0.7:
        return "good"
    else:
        return "acceptable"


def _generate_recommendations(
    issues: list,
    citation_count: int,
    dimension_count: int,
    avg_citations_per_dim: float,
) -> list[str]:
    """Generate recommendations for improvement.

    Args:
        issues: List of validation issues
        citation_count: Total citations
        dimension_count: Number of dimensions
        avg_citations_per_dim: Average citations per dimension

    Returns:
        List of recommendation strings
    """
    recommendations = []

    if avg_citations_per_dim < 2:
        recommendations.append(
            f"Add more evidence: currently averaging {avg_citations_per_dim:.1f} citations per dimension (target: 2+)"
        )

    if dimension_count < 3:
        recommendations.append(
            f"Consider exploring more dimensions: found {dimension_count} (target: 3-5)"
        )

    high_issues = [i for i in issues if i.severity == "high"]
    if high_issues:
        for issue in high_issues:
            recommendations.append(
                f"Address high-severity issue in '{issue.dimension}': {issue.description}"
            )

    if not recommendations:
        recommendations.append("Problem statement is well-supported and comprehensive!")

    return recommendations
