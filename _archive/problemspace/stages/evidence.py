"""
Evidence Stage

Validates the problem with evidence and data.
"""

from pathlib import Path
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import Evidence, ProblemAnalysis

logger = get_logger(__name__)


def validate_evidence(analysis: ProblemAnalysis) -> Evidence:
    """Collect evidence supporting the problem.

    Args:
        analysis: Problem analysis data

    Returns:
        Evidence data
    """
    logger.info("\n🔍 Evidence Validation Stage")
    logger.info("=" * 60)

    print("\nLet's validate this problem with evidence.\n")

    print("What evidence supports this problem exists?")
    print("(e.g., user research, data, competitive analysis)")
    print("Enter details below (Ctrl+D when done):\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    user_research = "\n".join(lines).strip()

    # Handle requests for AI research
    if "research" in user_research.lower() and "own" in user_research.lower():
        print("\n💡 Note: This tool helps YOU validate evidence you already have.")
        print("   Consider: What have you observed? What feedback have you heard?")
        print("   What metrics suggest this problem exists?\n")
        print("   For now, let's continue with the information you provided.\n")

    print("\n\nKey data points (optional):")
    print("Enter data points one per line (Enter on empty line to finish):\n")

    data_points = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            data_points.append(line)
    except EOFError:
        pass

    print("\n\nCompetitive analysis (optional):")
    print("What are competitors doing? (Ctrl+D when done, Enter to skip):\n")

    comp_lines = []
    try:
        while True:
            line = input()
            if not line and not comp_lines:
                break
            comp_lines.append(line)
    except EOFError:
        pass

    competitive_analysis = "\n".join(comp_lines).strip()

    validation_status = "validated" if user_research or data_points else "needs_validation"

    evidence = Evidence(
        user_research=user_research,
        data_points=data_points,
        competitive_analysis=competitive_analysis,
        validation_status=validation_status,
    )

    logger.info(f"✅ Evidence collected (Status: {validation_status})")
    return evidence
