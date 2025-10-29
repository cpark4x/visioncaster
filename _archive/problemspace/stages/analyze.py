"""
Analyze Stage

AI-powered analysis of the problem to identify gaps and assumptions.
"""

import subprocess
import json
from pathlib import Path
import sys

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from ..state import ProblemCapture, ProblemAnalysis

logger = get_logger(__name__)


def analyze_problem(capture: ProblemCapture) -> ProblemAnalysis:
    """Analyze the captured problem using AI.

    Args:
        capture: Problem capture data

    Returns:
        ProblemAnalysis with AI insights
    """
    logger.info("\n🤖 AI Analysis Stage")
    logger.info("=" * 60)

    prompt = f"""Analyze this problem statement and identify:

Problem Description:
{capture.raw_input}

Context:
{capture.context}

Constraints:
{capture.constraints}

Please provide a structured analysis:

1. CORE PROBLEM (1-2 sentences): What is the fundamental problem?
2. STAKEHOLDERS: Who is affected by this problem?
3. ASSUMPTIONS: What assumptions are being made?
4. RISKS: What could go wrong?
5. CLARITY SCORE (0-10): How clear and well-defined is this problem?
6. GAPS: What information is missing to fully understand this problem?

Return your analysis as JSON with these keys:
- core_problem (string)
- stakeholders (array of strings)
- assumptions (array of strings)
- risks (array of strings)
- clarity_score (number 0-10)
- gaps (array of strings)
"""

    temp_file = Path("/tmp/problemspace_analysis.txt")
    temp_file.write_text(prompt)

    logger.info("Analyzing problem with AI...")

    try:
        result = subprocess.run(
            ["claude-code", "--prompt-file", str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            logger.warning("AI analysis failed, using fallback")
            return _fallback_analysis(capture)

        response = result.stdout.strip()

        try:
            data = json.loads(response)
            analysis = ProblemAnalysis(
                core_problem=data.get("core_problem", ""),
                stakeholders=data.get("stakeholders", []),
                assumptions=data.get("assumptions", []),
                risks=data.get("risks", []),
                clarity_score=float(data.get("clarity_score", 0)),
                gaps=data.get("gaps", []),
            )
            logger.info(f"✅ Analysis complete (Clarity: {analysis.clarity_score}/10)")
            return analysis
        except json.JSONDecodeError:
            logger.warning("Could not parse AI response, using fallback")
            return _fallback_analysis(capture)

    except subprocess.TimeoutExpired:
        logger.warning("AI analysis timed out, using fallback")
        return _fallback_analysis(capture)
    except Exception as e:
        logger.warning(f"AI analysis error: {e}, using fallback")
        return _fallback_analysis(capture)


def _fallback_analysis(capture: ProblemCapture) -> ProblemAnalysis:
    """Simple fallback analysis without AI.

    Args:
        capture: Problem capture data

    Returns:
        Basic ProblemAnalysis
    """
    return ProblemAnalysis(
        core_problem=capture.raw_input[:200] + "..." if len(capture.raw_input) > 200 else capture.raw_input,
        stakeholders=["User"],
        assumptions=["Assuming problem is clearly defined"],
        risks=["Risk of building wrong solution"],
        clarity_score=5.0,
        gaps=["Evidence needed", "Metrics needed"],
    )
