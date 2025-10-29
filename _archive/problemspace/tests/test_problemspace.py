"""
Tests for ProblemSpace

Basic smoke tests for state management and pipeline.
"""

import pytest
from pathlib import Path
from scenarios.problemspace.state import (
    StateManager,
    ProblemSpaceState,
    ProblemCapture,
    ProblemAnalysis,
    slugify,
)


def test_slugify():
    """Test slug generation from text."""
    assert slugify("Test Problem") == "test-problem"
    assert slugify("Complex Problem With Spaces") == "complex-problem-with-spaces"
    assert slugify("Problem-With-Dashes") == "problem-with-dashes"
    assert slugify("Problem_With_Underscores") == "problem-with-underscores"
    assert slugify("Problem!@#$%Special&*()Chars") == "problemspecialchars"
    assert slugify("Multiple   Spaces") == "multiple-spaces"


def test_state_creation():
    """Test state manager creates initial state."""
    manager = StateManager()

    assert manager.state.stage == "initialized"
    assert manager.session_dir.exists()
    assert isinstance(manager.state, ProblemSpaceState)

    manager.save()
    assert manager.state_file.exists()


def test_state_persistence(tmp_path):
    """Test state saves and loads correctly."""
    session_dir = tmp_path / "test_session"

    manager = StateManager(session_dir)
    manager.state.stage = "captured"
    manager.state.capture = ProblemCapture(
        raw_input="Test problem",
        context="Test context",
        constraints="Test constraints",
    )
    manager.save()

    manager2 = StateManager(session_dir)
    assert manager2.state.stage == "captured"
    assert manager2.state.capture.raw_input == "Test problem"
    assert manager2.state.capture.context == "Test context"
    assert manager2.state.capture.constraints == "Test constraints"


def test_stage_progression(tmp_path):
    """Test stage updates work correctly."""
    manager = StateManager(tmp_path)

    assert manager.state.stage == "initialized"

    manager.update_stage("captured")
    assert manager.state.stage == "captured"

    manager.update_stage("analyzed")
    assert manager.state.stage == "analyzed"

    manager.update_stage("evidence_collected")
    assert manager.state.stage == "evidence_collected"


def test_history_tracking(tmp_path):
    """Test history entries are tracked."""
    manager = StateManager(tmp_path)

    assert len(manager.state.history) == 0

    manager.add_history({"stage": "capture", "status": "complete"})
    assert len(manager.state.history) == 1
    assert manager.state.history[0]["stage"] == "capture"
    assert "timestamp" in manager.state.history[0]

    manager.add_history({"stage": "analyze", "clarity_score": 8.5})
    assert len(manager.state.history) == 2


def test_state_reset(tmp_path):
    """Test state reset works correctly."""
    manager = StateManager(tmp_path)

    manager.state.stage = "analyzed"
    manager.state.capture = ProblemCapture(raw_input="Test")
    manager.add_history({"test": "data"})
    manager.save()

    manager.reset()

    assert manager.state.stage == "initialized"
    assert manager.state.capture.raw_input == ""
    assert len(manager.state.history) == 0


def test_dataclass_defaults():
    """Test dataclass default values."""
    capture = ProblemCapture()
    assert capture.raw_input == ""
    assert capture.context == ""
    assert capture.constraints == ""

    analysis = ProblemAnalysis()
    assert analysis.core_problem == ""
    assert analysis.stakeholders == []
    assert analysis.assumptions == []
    assert analysis.risks == []
    assert analysis.clarity_score == 0.0
    assert analysis.gaps == []


def test_complete_state_structure(tmp_path):
    """Test complete state with all fields populated."""
    manager = StateManager(tmp_path)

    manager.state.capture = ProblemCapture(
        raw_input="Users are leaving",
        context="E-commerce site",
        constraints="Limited budget",
    )

    manager.state.analysis = ProblemAnalysis(
        core_problem="Cart abandonment issue",
        stakeholders=["Users", "Business"],
        assumptions=["Users want to complete purchase"],
        risks=["May not be technical issue"],
        clarity_score=7.5,
        gaps=["Need user research"],
    )

    manager.state.stage = "analyzed"
    manager.save()

    manager2 = StateManager(tmp_path)

    assert manager2.state.capture.raw_input == "Users are leaving"
    assert manager2.state.analysis.core_problem == "Cart abandonment issue"
    assert manager2.state.analysis.clarity_score == 7.5
    assert len(manager2.state.analysis.stakeholders) == 2
