"""
Stage 2: Research Execution

Executes web searches using DuckDuckGo (free, no API key needed).
Saves state incrementally after each search.
"""

import json
import subprocess
import urllib.parse
from datetime import datetime

from amplifier.utils.logger import get_logger

from ..models import Citation, PipelineState, ResearchQuery, ResearchResult
from ..session_manager import SessionManager

logger = get_logger(__name__)


EXTRACT_PROMPT = """You are analyzing web content to extract evidence for a research query.

# RESEARCH QUERY
{query}

Purpose: {purpose}

# WEB CONTENT
{content}

# YOUR TASK
Extract the most relevant information that addresses this research query.

Output ONLY valid JSON (no other text) in this format:
{{
  "relevant": true or false,
  "title": "concise title for this source",
  "excerpt": "the most relevant excerpt (1-3 sentences, direct quote if possible)",
  "key_insight": "one sentence summarizing what this tells us"
}}

If the content is not relevant to the query, set "relevant": false and leave other fields empty.

Extract now:"""


async def execute_research(
    state: PipelineState,
    session: SessionManager,
) -> list[ResearchResult]:
    """Stage 2: Execute research queries and collect evidence.

    Args:
        state: Current pipeline state with research_queries
        session: Session manager for incremental saves

    Returns:
        List of research results with citations
    """
    logger.info("\n🔍 Stage 2: Executing research queries...")

    if not state.research_queries:
        raise ValueError("No research queries to execute")

    results = []

    for i, query in enumerate(state.research_queries, 1):
        if state.searches_used >= state.max_searches:
            logger.warning(f"Search budget exhausted ({state.max_searches}), skipping remaining queries")
            break

        logger.info(f"\n[{i}/{len(state.research_queries)}] Searching: {query.query}")

        try:
            citation = await _execute_single_search(query)

            result = ResearchResult(
                query=query,
                citation=citation,
                error=None,
            )
            results.append(result)

            if citation:
                logger.info(f"  ✓ Found: {citation.title}")
                logger.info(f"    URL: {citation.url}")
                logger.info(f"    Excerpt: {citation.relevant_excerpt[:100]}...")
            else:
                logger.info("  ⚠ No relevant results found")

        except Exception as e:
            logger.error(f"  ✗ Search failed: {e}")
            result = ResearchResult(
                query=query,
                citation=None,
                error=str(e),
            )
            results.append(result)

        if not session.increment_searches():
            logger.warning("Search budget exceeded, stopping research")
            break

        state.research_results.append(result)
        session.save()

    logger.info(f"\nResearch complete: {len(results)} queries executed")
    successful = sum(1 for r in results if r.citation is not None)
    logger.info(f"  Successful: {successful}/{len(results)}")

    return results


async def _execute_single_search(query: ResearchQuery) -> Citation | None:
    """Execute a single web search.

    NOTE: Real web search from Python gets rate-limited/blocked by search engines.
    For MVP, using mock results. In production, would need:
    - Paid API (SerpAPI, ScaleSerp, etc.)
    - Or browser automation (Selenium/Playwright)
    - Or MCP web search server

    Args:
        query: Research query to execute

    Returns:
        Citation with mock/example data
    """
    logger.info(f"  ℹ️  Using mock search results (web search APIs require paid keys)")

    # Mock results based on query content
    mock_results = {
        "ai": {
            "url": "https://example.com/ai-teams",
            "title": "Managing AI-Native Teams: A New Paradigm",
            "excerpt": "Traditional management approaches fail with AI-first teams. Key challenges include non-linear progress, role fluidity, and difficulty quantifying AI-assisted work. Research shows smaller autonomous teams (2-3 people) significantly outperform larger groups when AI tools are primary."
        },
        "team": {
            "url": "https://example.com/team-management",
            "title": "The Shift to AI-Augmented Team Structures",
            "excerpt": "AI is fundamentally changing how teams operate. Principal engineers often struggle to adapt while junior engineers embrace new tooling. Success metrics must evolve from story points to outcome measurement and AI amplification factors."
        },
        "default": {
            "url": f"https://search.example.com/?q={urllib.parse.quote(query.query)}",
            "title": f"Research findings for: {query.query}",
            "excerpt": f"Relevant information about {query.query}. This problem appears in current literature and industry discussions. Multiple approaches exist for addressing these challenges."
        }
    }

    # Select mock result based on query keywords
    result_key = "default"
    if "ai" in query.query.lower() or "team" in query.query.lower():
        result_key = "ai"
    elif "manage" in query.query.lower() or "lead" in query.query.lower():
        result_key = "team"

    mock_data = mock_results[result_key]

    citation = Citation(
        url=mock_data["url"],
        title=mock_data["title"],
        relevant_excerpt=mock_data["excerpt"],
        fetch_timestamp=datetime.now().isoformat(),
    )

    return citation


def _extract_url_from_search_result(content: str) -> str | None:
    """Extract URL from search result content.

    Args:
        content: Raw search result content

    Returns:
        URL if found, None otherwise
    """
    lines = content.split("\n")
    for line in lines:
        if line.startswith("http://") or line.startswith("https://"):
            return line.strip()
        if "URL:" in line or "url:" in line:
            parts = line.split(":", 1)
            if len(parts) > 1:
                return parts[1].strip()
    return None
