"""
Capture Stage

Collects initial problem description from the user.
"""

from pathlib import Path
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import ProblemCapture

logger = get_logger(__name__)


def capture_problem() -> ProblemCapture:
    """Capture initial problem description from user.

    Returns:
        ProblemCapture with user's input
    """
    logger.info("\n📝 Problem Capture Stage")
    logger.info("=" * 60)

    print("\nWelcome to ProblemSpace!")
    print("Let's capture your problem clearly before building anything.\n")

    print("Step 1: Describe the problem")
    print("-" * 40)
    print("What problem are you trying to solve?")
    print("(Enter your description, then press Ctrl+D when done)\n")

    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    raw_input = "\n".join(lines).strip()

    print("\n\nStep 2: Additional context (optional)")
    print("-" * 40)
    print("Any additional context? (Press Enter to skip, or Ctrl+D when done)\n")

    context_lines = []
    try:
        while True:
            line = input()
            if not line and not context_lines:
                break
            context_lines.append(line)
    except EOFError:
        pass

    context = "\n".join(context_lines).strip()

    print("\n\nStep 3: Constraints (optional)")
    print("-" * 40)
    print("Any known constraints? (Press Enter to skip, or Ctrl+D when done)\n")

    constraint_lines = []
    try:
        while True:
            line = input()
            if not line and not constraint_lines:
                break
            constraint_lines.append(line)
    except EOFError:
        pass

    constraints = "\n".join(constraint_lines).strip()

    capture = ProblemCapture(
        raw_input=raw_input,
        context=context,
        constraints=constraints,
    )

    logger.info("✅ Problem captured")
    return capture
