"""
Metrics Stage

Defines success metrics for measuring solution effectiveness.
"""

from pathlib import Path
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import SuccessMetrics, ProblemAnalysis

logger = get_logger(__name__)


def define_metrics(analysis: ProblemAnalysis) -> SuccessMetrics:
    """Define success metrics for the solution.

    Args:
        analysis: Problem analysis data

    Returns:
        SuccessMetrics data
    """
    logger.info("\n📊 Success Metrics Stage")
    logger.info("=" * 60)

    print("\nHow will we measure success?\n")

    print("Business metrics:")
    print("(e.g., revenue, cost reduction, user growth)")
    print("Enter one per line (Enter on empty line to finish):\n")

    business_metrics = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            # Filter out uncertain responses
            if line.lower() not in ["not sure", "don't know", "unsure", "idk"]:
                business_metrics.append(line)
    except EOFError:
        pass

    print("\n\nUser metrics:")
    print("(e.g., satisfaction, task completion, retention)")
    print("Enter one per line (Enter on empty line to finish):\n")

    user_metrics = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            # Filter out uncertain responses
            if line.lower() not in ["not sure", "don't know", "unsure", "idk"]:
                user_metrics.append(line)
    except EOFError:
        pass

    print("\n\nTechnical metrics:")
    print("(e.g., performance, reliability, scalability)")
    print("Enter one per line (Enter on empty line to finish):\n")

    technical_metrics = []
    try:
        while True:
            line = input().strip()
            if not line:
                break
            # Filter out uncertain responses
            if line.lower() not in ["not sure", "don't know", "unsure", "idk"]:
                technical_metrics.append(line)
    except EOFError:
        pass

    # Ensure at least one metric is defined
    all_metrics = business_metrics + user_metrics + technical_metrics
    if not all_metrics:
        logger.warning("⚠️  No metrics provided. Adding default measurement.")
        business_metrics.append("Problem validation completed")

    metrics = SuccessMetrics(
        business_metrics=business_metrics,
        user_metrics=user_metrics,
        technical_metrics=technical_metrics,
    )

    total_metrics = len(business_metrics) + len(user_metrics) + len(technical_metrics)
    logger.info(f"✅ Success metrics defined ({total_metrics} total)")
    return metrics
