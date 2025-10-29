"""
Stage 1: Problem Capture

Captures initial problem statement and generates research queries using AI.
"""

import json
import subprocess
from pathlib import Path

from amplifier.utils.logger import get_logger

from ..models import PipelineState, ResearchQuery

logger = get_logger(__name__)


DECOMPOSE_PROMPT = """You are a research planning expert. Your task is to decompose a problem statement into targeted research queries.

# PROBLEM STATEMENT
{problem}

# YOUR TASK
Generate 5-10 specific, targeted research queries that will help gather evidence about this problem.

Each query should:
- Be specific and searchable (imagine typing it into Google)
- Target a different dimension of the problem
- Have a clear purpose (what aspect are you investigating?)
- Be prioritized (1=critical, 2=important, 3=nice-to-have)

# OUTPUT FORMAT
Return ONLY valid JSON (no other text) in this structure:
{{
  "queries": [
    {{
      "query": "specific search query text",
      "purpose": "what aspect this investigates",
      "priority": 1
    }}
  ]
}}

Think about:
- What evidence would validate this problem exists?
- What are the different dimensions/facets of this problem?
- Who is affected and how?
- What are current solutions and their limitations?
- What are the underlying causes?

Generate the research queries now:"""


async def capture_problem(state: PipelineState) -> list[ResearchQuery]:
    """Stage 1: Capture problem and decompose into research queries.

    Args:
        state: Current pipeline state with initial_problem set

    Returns:
        List of research queries
    """
    logger.info("\n📋 Stage 1: Capturing problem and generating research queries...")

    if not state.initial_problem.strip():
        raise ValueError("No initial problem statement provided")

    prompt = DECOMPOSE_PROMPT.format(problem=state.initial_problem)
    prompt_file = Path(".data/problemexplorer/.tmp_prompt.txt")
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(prompt)

    # MVP: Use simple heuristic query generation
    # In production, this would call AI via proper SDK
    logger.info("Using heuristic query generation (MVP mode)")

    problem = state.initial_problem
    queries = [
        ResearchQuery(
            query=f"{problem}",
            purpose="Direct problem search",
            priority=1
        ),
        ResearchQuery(
            query=f"research on {problem}",
            purpose="Academic/research perspective",
            priority=1
        ),
        ResearchQuery(
            query=f"how to solve {problem}",
            purpose="Solution approaches",
            priority=2
        ),
        ResearchQuery(
            query=f"challenges with {problem}",
            purpose="Problem validation and scope",
            priority=1
        ),
        ResearchQuery(
            query=f"metrics for measuring {problem}",
            purpose="Success metrics discovery",
            priority=2
        ),
    ]

    logger.info(f"Generated {len(queries)} research queries")
    for i, q in enumerate(queries, 1):
        logger.info(f"  {i}. [P{q.priority}] {q.query}")
        logger.info(f"     → {q.purpose}")

    return queries[:state.max_searches]  # Respect search limit
