#!/usr/bin/env python3
"""
ProblemExplorer - Main Orchestrator and CLI

AI-research-first problem statement tool where AI discovers evidence
and humans validate.
"""

import asyncio
import sys
from pathlib import Path

import click

from amplifier.utils.logger import get_logger

from .session_manager import SessionManager
from .stages import (
    assess_quality,
    capture_problem,
    execute_research,
    generate_output,
    synthesize_statement,
    validate_statement,
)

logger = get_logger(__name__)


class ProblemExplorerPipeline:
    """Orchestrates the 6-stage ProblemExplorer pipeline."""

    def __init__(self, session: SessionManager):
        """Initialize pipeline with session management.

        Args:
            session: Session manager instance
        """
        self.session = session

    async def run(self, problem: str) -> bool:
        """Run the complete 6-stage pipeline.

        Args:
            problem: Initial problem statement

        Returns:
            True if successful, False otherwise
        """
        self.session.state.initial_problem = problem
        self.session.save()

        stage = self.session.state.stage
        logger.info(f"Starting from stage: {stage}")

        try:
            if stage == "initialized":
                await self._stage_1_capture()
                stage = self.session.state.stage

            if stage == "problem_captured":
                await self._stage_2_research()
                stage = self.session.state.stage

            if stage == "research_complete":
                await self._stage_3_synthesize()
                stage = self.session.state.stage

            if stage == "synthesized":
                await self._stage_4_validate()
                stage = self.session.state.stage

            if stage == "validated":
                needs_refinement = await self._check_quality_gate()

                if needs_refinement and self.session.state.iteration < self.session.state.max_iterations:
                    logger.info("\n🔄 Quality gate not met - refining...")
                    if not self.session.increment_iteration():
                        logger.warning("Max iterations reached")
                    else:
                        await self._refine_and_retry()
                        return await self.run(problem)

            if stage == "validated":
                await self._stage_5_metrics()
                stage = self.session.state.stage

            if stage == "assessed":
                await self._stage_6_output()

            self.session.mark_complete()
            return True

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def _stage_1_capture(self) -> None:
        """Stage 1: Capture problem and generate research queries."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 1: PROBLEM CAPTURE")
        logger.info("="*60)

        self.session.update_stage("capturing_problem")

        queries = await capture_problem(self.session.state)
        self.session.state.research_queries = queries
        self.session.update_stage("problem_captured")

    async def _stage_2_research(self) -> None:
        """Stage 2: Execute research and collect evidence."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 2: RESEARCH EXECUTION")
        logger.info("="*60)

        self.session.update_stage("researching")

        results = await execute_research(self.session.state, self.session)
        self.session.state.research_results = results
        self.session.update_stage("research_complete")

    async def _stage_3_synthesize(self) -> None:
        """Stage 3: Synthesize problem statement."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 3: SYNTHESIS")
        logger.info("="*60)

        self.session.update_stage("synthesizing")

        statement = await synthesize_statement(self.session.state)
        self.session.state.problem_statement = statement
        self.session.save()
        self.session.update_stage("synthesized")

    async def _stage_4_validate(self) -> None:
        """Stage 4: Validate problem statement."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 4: VALIDATION")
        logger.info("="*60)

        self.session.update_stage("validating")

        issues = await validate_statement(self.session.state)
        self.session.state.validation_issues = issues
        self.session.save()
        self.session.update_stage("validated")

    async def _stage_5_metrics(self) -> None:
        """Stage 5: Assess quality metrics."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 5: QUALITY METRICS")
        logger.info("="*60)

        self.session.update_stage("assessing")

        metrics = await assess_quality(self.session.state)
        self.session.state.quality_metrics = metrics
        self.session.save()
        self.session.update_stage("assessed")

    async def _stage_6_output(self) -> None:
        """Stage 6: Generate output document."""
        logger.info("\n" + "="*60)
        logger.info("STAGE 6: OUTPUT GENERATION")
        logger.info("="*60)

        self.session.update_stage("generating_output")

        output_path = await generate_output(
            self.session.state,
            self.session.session_dir,
        )
        self.session.state.output_path = str(output_path)
        self.session.save()

    async def _check_quality_gate(self) -> bool:
        """Check if quality gate is met.

        Returns:
            True if needs refinement, False if quality is acceptable
        """
        issues = self.session.state.validation_issues

        high_issues = [i for i in issues if i.severity == "high"]

        if high_issues:
            logger.warning(f"\n⚠️  Quality gate: {len(high_issues)} high-severity issues found")
            return True

        logger.info("\n✅ Quality gate passed")
        return False

    async def _refine_and_retry(self) -> None:
        """Refine problem statement based on validation issues."""
        logger.info("\n🔄 Refining based on validation feedback...")

        self.session.update_stage("problem_captured")


@click.command()
@click.option(
    "--problem",
    type=str,
    required=False,
    help="Initial problem statement (or provide via --problem-file)",
)
@click.option(
    "--problem-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to file containing problem statement",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Resume from most recent session",
)
@click.option(
    "--reset",
    is_flag=True,
    help="Reset state and start fresh",
)
@click.option(
    "--max-iterations",
    type=int,
    default=3,
    help="Maximum refinement iterations (default: 3)",
)
@click.option(
    "--max-searches",
    type=int,
    default=15,
    help="Maximum web searches (default: 15)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
def main(
    problem: str | None,
    problem_file: Path | None,
    resume: bool,
    reset: bool,
    max_iterations: int,
    max_searches: int,
    verbose: bool,
):
    """ProblemExplorer - AI-research-first problem statement tool.

    AI discovers evidence through web research, then synthesizes it into
    a structured problem statement with citations.

    Example:
        python -m scenarios.problemexplorer --problem "Users struggle with X"

    Or from file:
        python -m scenarios.problemexplorer --problem-file problem.txt
    """
    if verbose:
        logger.logger.setLevel("DEBUG")

    session_dir = None
    if resume:
        base_dir = Path(".data/problemexplorer")
        if base_dir.exists():
            sessions = sorted([d for d in base_dir.iterdir() if d.is_dir()], reverse=True)
            if sessions:
                session_dir = sessions[0]
                logger.info(f"Resuming session: {session_dir.name}")

    session = SessionManager(session_dir)

    if reset:
        session.reset()
        logger.info("State reset - starting fresh")

    session.state.max_iterations = max_iterations
    session.state.max_searches = max_searches
    session.save()

    if resume and session.state.initial_problem:
        problem_text = session.state.initial_problem
        logger.info("Using problem from saved state")
    elif problem_file:
        problem_text = problem_file.read_text().strip()
        logger.info(f"Loaded problem from: {problem_file}")
    elif problem:
        problem_text = problem.strip()
    else:
        logger.error("Must provide --problem or --problem-file")
        return 1

    pipeline = ProblemExplorerPipeline(session)

    logger.info("\n🚀 Starting ProblemExplorer Pipeline")
    logger.info(f"  Session: {session.session_dir}")
    logger.info(f"  Max iterations: {max_iterations}")
    logger.info(f"  Max searches: {max_searches}")
    logger.info(f"\n  Problem: {problem_text[:100]}...")

    success = asyncio.run(pipeline.run(problem_text))

    if success:
        logger.info("\n✨ ProblemExplorer complete!")
        if session.state.output_path:
            logger.info(f"📄 Output: {session.state.output_path}")
        return 0

    logger.error("\n❌ ProblemExplorer failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
