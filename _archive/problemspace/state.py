"""
State Management Module

Handles pipeline state persistence for resume capability.
Saves state after every operation to enable interruption recovery.
"""

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from amplifier.ccsdk_toolkit.defensive.file_io import read_json_with_retry, write_json_with_retry
    from amplifier.utils.logger import get_logger
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "amplifier"))
    from amplifier.ccsdk_toolkit.defensive.file_io import read_json_with_retry, write_json_with_retry
    from amplifier.utils.logger import get_logger

logger = get_logger(__name__)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified string (lowercase, dashes for spaces, no special chars)
    """
    slug = text.lower()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug


@dataclass
class ProblemCapture:
    """Initial problem capture from user."""

    raw_input: str = ""
    context: str = ""
    constraints: str = ""


@dataclass
class ProblemAnalysis:
    """AI analysis of the problem."""

    core_problem: str = ""
    stakeholders: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    clarity_score: float = 0.0
    gaps: list[str] = field(default_factory=list)


@dataclass
class Evidence:
    """Evidence supporting the problem."""

    user_research: str = ""
    data_points: list[str] = field(default_factory=list)
    competitive_analysis: str = ""
    validation_status: str = "pending"


@dataclass
class SuccessMetrics:
    """Metrics to measure solution success."""

    business_metrics: list[str] = field(default_factory=list)
    user_metrics: list[str] = field(default_factory=list)
    technical_metrics: list[str] = field(default_factory=list)


@dataclass
class HumanReview:
    """Human review and feedback."""

    approved: bool = False
    feedback: str = ""
    requested_changes: list[str] = field(default_factory=list)


@dataclass
class ProblemSpaceState:
    """Complete pipeline state for ProblemSpace."""

    stage: str = "initialized"

    capture: ProblemCapture = field(default_factory=ProblemCapture)
    analysis: ProblemAnalysis = field(default_factory=ProblemAnalysis)
    evidence: Evidence = field(default_factory=Evidence)
    metrics: SuccessMetrics = field(default_factory=SuccessMetrics)
    review: HumanReview = field(default_factory=HumanReview)

    history: list[dict[str, Any]] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class StateManager:
    """Manages pipeline state with automatic persistence."""

    def __init__(self, session_dir: Path | None = None):
        """Initialize state manager.

        Args:
            session_dir: Path to session directory (default: .data/problemspace/<timestamp>/)
        """
        if session_dir is None:
            base_dir = Path(".data/problemspace")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_dir = base_dir / timestamp

        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.session_dir / "state.json"
        self.state = self._load_state()

    def _load_state(self) -> ProblemSpaceState:
        """Load state from file or create new."""
        if self.state_file.exists():
            try:
                data = read_json_with_retry(self.state_file)

                capture = ProblemCapture(**data.get("capture", {}))
                analysis = ProblemAnalysis(**data.get("analysis", {}))
                evidence = Evidence(**data.get("evidence", {}))
                metrics = SuccessMetrics(**data.get("metrics", {}))
                review = HumanReview(**data.get("review", {}))

                state = ProblemSpaceState(
                    stage=data.get("stage", "initialized"),
                    capture=capture,
                    analysis=analysis,
                    evidence=evidence,
                    metrics=metrics,
                    review=review,
                    history=data.get("history", []),
                    created_at=data.get("created_at", datetime.now().isoformat()),
                    updated_at=data.get("updated_at", datetime.now().isoformat()),
                )

                logger.info(f"Resumed state from: {self.state_file}")
                logger.info(f"  Stage: {state.stage}")
                return state
            except Exception as e:
                logger.warning(f"Could not load state: {e}")
                logger.info("Starting fresh pipeline")

        return ProblemSpaceState()

    def save(self) -> None:
        """Save current state to file."""
        self.state.updated_at = datetime.now().isoformat()

        try:
            state_dict = asdict(self.state)
            write_json_with_retry(state_dict, self.state_file)
            logger.debug(f"State saved to: {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def update_stage(self, stage: str) -> None:
        """Update pipeline stage and save."""
        old_stage = self.state.stage
        self.state.stage = stage
        logger.info(f"Pipeline stage: {old_stage} → {stage}")
        self.save()

    def add_history(self, entry: dict[str, Any]) -> None:
        """Add entry to history for audit trail."""
        entry["timestamp"] = datetime.now().isoformat()
        self.state.history.append(entry)
        self.save()

    def mark_complete(self) -> None:
        """Mark pipeline as complete."""
        self.update_stage("approved")
        logger.info("✅ ProblemSpace complete!")

    def reset(self) -> None:
        """Reset state for fresh run."""
        self.state = ProblemSpaceState()
        self.save()
        logger.info("State reset for fresh pipeline run")
