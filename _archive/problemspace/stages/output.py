"""
Output Stage

Generates final problem statement document.
"""

from pathlib import Path
from datetime import datetime
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import ProblemSpaceState, slugify

logger = get_logger(__name__)


def generate_output(state: ProblemSpaceState, session_dir: Path) -> Path:
    """Generate final problem statement document.

    Args:
        state: Complete problem space state
        session_dir: Session directory for output

    Returns:
        Path to generated document
    """
    logger.info("\n📄 Output Generation Stage")
    logger.info("=" * 60)

    slug = slugify(state.analysis.core_problem[:50])
    output_file = session_dir / f"problem-statement-{slug}.md"

    content = _generate_markdown(state)

    output_file.write_text(content)

    logger.info(f"✅ Problem statement saved: {output_file}")
    return output_file


def _generate_markdown(state: ProblemSpaceState) -> str:
    """Generate markdown content for problem statement.

    Args:
        state: Complete problem space state

    Returns:
        Markdown content
    """
    lines = []

    lines.append("# Problem Statement")
    lines.append("")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    lines.append("")
    lines.append("---")
    lines.append("")

    lines.append("## Core Problem")
    lines.append("")
    lines.append(state.analysis.core_problem)
    lines.append("")

    lines.append("## Context")
    lines.append("")
    if state.capture.context:
        lines.append(state.capture.context)
    else:
        lines.append("*No additional context provided*")
    lines.append("")

    if state.capture.constraints:
        lines.append("## Constraints")
        lines.append("")
        lines.append(state.capture.constraints)
        lines.append("")

    lines.append("## Stakeholders")
    lines.append("")
    for stakeholder in state.analysis.stakeholders:
        lines.append(f"- {stakeholder}")
    lines.append("")

    lines.append("## Evidence")
    lines.append("")

    if state.evidence.user_research:
        lines.append("### User Research")
        lines.append("")
        lines.append(state.evidence.user_research)
        lines.append("")

    if state.evidence.data_points:
        lines.append("### Key Data Points")
        lines.append("")
        for point in state.evidence.data_points:
            lines.append(f"- {point}")
        lines.append("")

    if state.evidence.competitive_analysis:
        lines.append("### Competitive Analysis")
        lines.append("")
        lines.append(state.evidence.competitive_analysis)
        lines.append("")

    lines.append(f"**Validation Status:** {state.evidence.validation_status}")
    lines.append("")

    lines.append("## Success Metrics")
    lines.append("")

    if state.metrics.business_metrics:
        lines.append("### Business Metrics")
        lines.append("")
        for metric in state.metrics.business_metrics:
            lines.append(f"- {metric}")
        lines.append("")

    if state.metrics.user_metrics:
        lines.append("### User Metrics")
        lines.append("")
        for metric in state.metrics.user_metrics:
            lines.append(f"- {metric}")
        lines.append("")

    if state.metrics.technical_metrics:
        lines.append("### Technical Metrics")
        lines.append("")
        for metric in state.metrics.technical_metrics:
            lines.append(f"- {metric}")
        lines.append("")

    lines.append("## Analysis")
    lines.append("")
    lines.append(f"**Clarity Score:** {state.analysis.clarity_score}/10")
    lines.append("")

    if state.analysis.assumptions:
        lines.append("### Assumptions")
        lines.append("")
        for assumption in state.analysis.assumptions:
            lines.append(f"- {assumption}")
        lines.append("")

    if state.analysis.risks:
        lines.append("### Risks")
        lines.append("")
        for risk in state.analysis.risks:
            lines.append(f"- {risk}")
        lines.append("")

    if state.analysis.gaps:
        lines.append("### Identified Gaps")
        lines.append("")
        for gap in state.analysis.gaps:
            lines.append(f"- {gap}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    if state.review.approved:
        lines.append("✅ **APPROVED**")
    else:
        lines.append("⚠️ **NEEDS REVISION**")

        if state.review.feedback:
            lines.append("")
            lines.append("### Review Feedback")
            lines.append("")
            lines.append(state.review.feedback)

        if state.review.requested_changes:
            lines.append("")
            lines.append("### Requested Changes")
            lines.append("")
            for change in state.review.requested_changes:
                lines.append(f"- [ ] {change}")

    lines.append("")

    return "\n".join(lines)
