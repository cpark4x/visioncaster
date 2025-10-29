#!/usr/bin/env python3
"""
ProblemSpace - Main Orchestrator and CLI

Coordinates the problem validation pipeline with state management.
"""

import sys
from pathlib import Path

import click

try:
    from amplifier.utils.logger import get_logger
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "amplifier"))
    from amplifier.utils.logger import get_logger

from .state import StateManager
from .stages import (
    capture_problem,
    analyze_problem,
    validate_evidence,
    define_metrics,
    human_review,
    generate_output,
)

logger = get_logger(__name__)


class ProblemSpacePipeline:
    """Orchestrates the problem validation pipeline."""

    def __init__(self, state_manager: StateManager):
        """Initialize pipeline with state management.

        Args:
            state_manager: State manager instance
        """
        self.state = state_manager

    def run(self) -> bool:
        """Run the complete pipeline.

        Returns:
            True if successful and approved, False otherwise
        """
        stage = self.state.state.stage
        logger.info(f"Starting from stage: {stage}")

        try:
            if stage == "initialized":
                self._run_capture()
                stage = self.state.state.stage

            if stage == "captured":
                self._run_analyze()
                stage = self.state.state.stage

            if stage == "analyzed":
                self._run_evidence()
                stage = self.state.state.stage

            if stage == "evidence_collected":
                self._run_metrics()
                stage = self.state.state.stage

            if stage == "metrics_defined":
                self._run_review()
                stage = self.state.state.stage

            if stage == "reviewed":
                if self.state.state.review.approved:
                    self._run_output()
                    self.state.mark_complete()
                    return True
                else:
                    logger.warning("Problem statement not approved")
                    logger.info("Run again with --resume to iterate")
                    return False

            if stage == "approved":
                logger.info("Pipeline already complete!")
                return True

            return False

        except KeyboardInterrupt:
            logger.info("\n\n⚠️ Pipeline interrupted")
            logger.info("Progress saved. Run with --resume to continue.")
            return False
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            logger.info(f"\n⚠️ Last successful stage: {self.state.state.stage}")
            logger.info(f"   Session saved to: {self.state.session_dir}")
            logger.info("\n💡 You can resume with: make problemspace-resume")
            return False

    def _run_capture(self) -> None:
        """Run problem capture stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 1: CAPTURE")
        logger.info("=" * 60)

        capture = capture_problem()
        self.state.state.capture = capture
        self.state.update_stage("captured")
        self.state.add_history({"stage": "capture", "status": "complete"})

    def _run_analyze(self) -> None:
        """Run AI analysis stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 2: ANALYZE")
        logger.info("=" * 60)

        analysis = analyze_problem(self.state.state.capture)
        self.state.state.analysis = analysis
        self.state.update_stage("analyzed")
        self.state.add_history({"stage": "analyze", "clarity_score": analysis.clarity_score})

        if analysis.clarity_score < 5.0:
            logger.warning(f"⚠️ Low clarity score: {analysis.clarity_score}/10")
            logger.warning("Consider refining the problem statement")

    def _run_evidence(self) -> None:
        """Run evidence validation stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 3: EVIDENCE")
        logger.info("=" * 60)

        evidence = validate_evidence(self.state.state.analysis)
        self.state.state.evidence = evidence
        self.state.update_stage("evidence_collected")
        self.state.add_history({"stage": "evidence", "status": evidence.validation_status})

    def _run_metrics(self) -> None:
        """Run metrics definition stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 4: METRICS")
        logger.info("=" * 60)

        metrics = define_metrics(self.state.state.analysis)
        self.state.state.metrics = metrics
        self.state.update_stage("metrics_defined")
        self.state.add_history({"stage": "metrics", "status": "complete"})

    def _run_review(self) -> None:
        """Run human review stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 5: REVIEW")
        logger.info("=" * 60)

        review = human_review(self.state.state)
        self.state.state.review = review
        self.state.update_stage("reviewed")
        self.state.add_history({
            "stage": "review",
            "approved": review.approved,
            "changes_requested": len(review.requested_changes),
        })

    def _run_output(self) -> None:
        """Run output generation stage."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 6: OUTPUT")
        logger.info("=" * 60)

        output_path = generate_output(self.state.state, self.state.session_dir)
        self.state.add_history({"stage": "output", "file": str(output_path)})


@click.command()
@click.option(
    "--resume",
    is_flag=True,
    help="Resume from saved state",
)
@click.option(
    "--reset",
    is_flag=True,
    help="Reset state and start fresh",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
def main(resume: bool, reset: bool, verbose: bool):
    """ProblemSpace - Validate problem clarity before building.

    This tool guides you through validating and documenting your problem
    before any solution is built. It ensures you have:

    - Clear problem definition
    - Evidence the problem exists
    - Success metrics defined
    - Stakeholder alignment

    Example:
        python -m scenarios.problemspace

        # Resume interrupted session
        python -m scenarios.problemspace --resume

        # Start fresh
        python -m scenarios.problemspace --reset
    """
    if verbose:
        logger.logger.setLevel("DEBUG")

    session_dir = None
    if resume:
        base_dir = Path(".data/problemspace")
        if base_dir.exists():
            sessions = sorted([d for d in base_dir.iterdir() if d.is_dir()], reverse=True)
            if sessions:
                session_dir = sessions[0]
                logger.info(f"Resuming session: {session_dir.name}")

    state_manager = StateManager(session_dir)

    if reset:
        state_manager.reset()
        logger.info("State reset - starting fresh")

    if resume and state_manager.state_file.exists() and not reset:
        logger.info("Resuming from saved state")

    pipeline = ProblemSpacePipeline(state_manager)

    logger.info("\n🚀 Starting ProblemSpace Pipeline")
    logger.info(f"  Session: {state_manager.session_dir}")

    success = pipeline.run()

    if success:
        logger.info("\n✨ Problem validation complete!")
        logger.info("✅ Problem statement approved and ready to build from!")
        return 0

    logger.info("\n⚠️ Problem validation incomplete")
    return 1


if __name__ == "__main__":
    sys.exit(main())
