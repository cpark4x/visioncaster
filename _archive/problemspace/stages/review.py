"""
Review Stage

Human review and approval of the problem statement.
"""

from pathlib import Path
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import HumanReview, ProblemSpaceState

logger = get_logger(__name__)


def human_review(state: ProblemSpaceState) -> HumanReview:
    """Get human review and approval.

    Args:
        state: Complete problem space state

    Returns:
        HumanReview with approval decision
    """
    logger.info("\n👤 Human Review Stage")
    logger.info("=" * 60)

    print("\n\n=== PROBLEM STATEMENT REVIEW ===\n")

    print("PROBLEM:")
    print(state.analysis.core_problem)
    print()

    print("STAKEHOLDERS:")
    for s in state.analysis.stakeholders:
        print(f"  - {s}")
    print()

    print("EVIDENCE:")
    if state.evidence.user_research:
        print(f"  User Research: {state.evidence.user_research[:100]}...")
    print(f"  Data Points: {len(state.evidence.data_points)}")
    print(f"  Status: {state.evidence.validation_status}")
    print()

    print("SUCCESS METRICS:")
    total_metrics = (
        len(state.metrics.business_metrics)
        + len(state.metrics.user_metrics)
        + len(state.metrics.technical_metrics)
    )
    print(f"  Total: {total_metrics} metrics defined")
    print()

    print("CLARITY SCORE: {:.1f}/10".format(state.analysis.clarity_score))
    print()

    if state.analysis.gaps:
        print("IDENTIFIED GAPS:")
        for gap in state.analysis.gaps:
            print(f"  - {gap}")
        print()

    print("\n" + "=" * 60)
    print("Do you approve this problem statement?")
    response = input("(yes/no): ").strip().lower()

    approved = response in ["yes", "y"]

    feedback = ""
    requested_changes = []

    if not approved:
        print("\nWhat changes are needed?")
        print("(Enter feedback, Ctrl+D when done):\n")

        feedback_lines = []
        try:
            while True:
                line = input()
                feedback_lines.append(line)
        except EOFError:
            pass

        feedback = "\n".join(feedback_lines).strip()

        print("\n\nSpecific changes requested:")
        print("(Enter one per line, Enter on empty line to finish):\n")

        while True:
            change = input().strip()
            if not change:
                break
            requested_changes.append(change)

    review = HumanReview(
        approved=approved,
        feedback=feedback,
        requested_changes=requested_changes,
    )

    if approved:
        logger.info("✅ Problem statement approved!")
    else:
        logger.info(f"⚠️ Changes requested ({len(requested_changes)} items)")

    return review
