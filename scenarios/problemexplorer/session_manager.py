"""
Session Manager for ProblemExplorer

Handles state persistence with incremental saves after each operation.
Supports resume capability.
"""

import json
from datetime import datetime
from pathlib import Path

from amplifier.utils.logger import get_logger

from .models import (
    PipelineState,
    pipeline_state_from_dict,
    pipeline_state_to_dict,
)

logger = get_logger(__name__)


class SessionManager:
    """Manages pipeline state with automatic persistence."""

    def __init__(self, session_dir: Path | None = None):
        """Initialize session manager.

        Args:
            session_dir: Path to session directory (default: .data/problemexplorer/<timestamp>/)
        """
        if session_dir is None:
            base_dir = Path(".data/problemexplorer")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_dir = base_dir / timestamp

        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.session_dir / "state.json"
        self.state = self._load_state()

    def _load_state(self) -> PipelineState:
        """Load state from file or create new."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    data = json.load(f)
                logger.info(f"Resumed state from: {self.state_file}")
                logger.info(f"  Stage: {data.get('stage', 'unknown')}")
                logger.info(f"  Iteration: {data.get('iteration', 0)}")
                logger.info(f"  Searches used: {data.get('searches_used', 0)}/{data.get('max_searches', 15)}")
                return pipeline_state_from_dict(data)
            except Exception as e:
                logger.warning(f"Could not load state: {e}")
                logger.info("Starting fresh pipeline")

        return PipelineState()

    def save(self) -> None:
        """Save current state to file."""
        self.state.updated_at = datetime.now().isoformat()

        try:
            state_dict = pipeline_state_to_dict(self.state)
            with open(self.state_file, "w") as f:
                json.dump(state_dict, f, indent=2)
            logger.debug(f"State saved to: {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def update_stage(self, stage: str) -> None:
        """Update pipeline stage and save."""
        old_stage = self.state.stage
        self.state.stage = stage
        logger.info(f"Pipeline stage: {old_stage} → {stage}")
        self.save()

    def increment_iteration(self) -> bool:
        """Increment iteration counter.

        Returns:
            True if within max iterations, False if exceeded
        """
        self.state.iteration += 1
        logger.info(f"Iteration {self.state.iteration}/{self.state.max_iterations}")

        if self.state.iteration > self.state.max_iterations:
            logger.warning(f"Exceeded max iterations ({self.state.max_iterations})")
            return False

        self.save()
        return True

    def increment_searches(self) -> bool:
        """Increment search budget counter.

        Returns:
            True if within budget, False if exceeded
        """
        self.state.searches_used += 1
        logger.info(f"Searches used: {self.state.searches_used}/{self.state.max_searches}")

        if self.state.searches_used > self.state.max_searches:
            logger.warning(f"Exceeded search budget ({self.state.max_searches})")
            return False

        self.save()
        return True

    def is_complete(self) -> bool:
        """Check if pipeline is complete."""
        return self.state.stage == "complete"

    def mark_complete(self) -> None:
        """Mark pipeline as complete."""
        self.update_stage("complete")
        logger.info("✅ Pipeline complete!")

    def reset(self) -> None:
        """Reset state for fresh run."""
        self.state = PipelineState()
        self.save()
        logger.info("State reset for fresh pipeline run")
