"""
Basic tests for ProblemExplorer components.
"""

import pytest
from pathlib import Path

from ..models import (
    Citation,
    PipelineState,
    ProblemDimension,
    ProblemStatement,
    ResearchQuery,
    pipeline_state_to_dict,
    pipeline_state_from_dict,
)
from ..session_manager import SessionManager


class TestModels:
    """Test data models and serialization."""

    def test_citation_creation(self):
        """Test creating a citation."""
        citation = Citation(
            url="https://example.com",
            title="Test Article",
            relevant_excerpt="This is a test excerpt",
        )

        assert citation.url == "https://example.com"
        assert citation.title == "Test Article"
        assert citation.relevant_excerpt == "This is a test excerpt"
        assert citation.fetch_timestamp is not None

    def test_research_query_creation(self):
        """Test creating a research query."""
        query = ResearchQuery(
            query="test query",
            purpose="testing",
            priority=1,
        )

        assert query.query == "test query"
        assert query.purpose == "testing"
        assert query.priority == 1

    def test_pipeline_state_serialization(self):
        """Test state serialization and deserialization."""
        state = PipelineState(
            stage="research_complete",
            iteration=1,
            initial_problem="Test problem",
        )

        state.research_queries = [
            ResearchQuery(
                query="test query",
                purpose="testing",
                priority=1,
            )
        ]

        state_dict = pipeline_state_to_dict(state)
        restored_state = pipeline_state_from_dict(state_dict)

        assert restored_state.stage == state.stage
        assert restored_state.iteration == state.iteration
        assert restored_state.initial_problem == state.initial_problem
        assert len(restored_state.research_queries) == 1
        assert restored_state.research_queries[0].query == "test query"

    def test_problem_statement_with_dimensions(self):
        """Test problem statement with dimensions."""
        citation = Citation(
            url="https://example.com",
            title="Test",
            relevant_excerpt="Test excerpt",
        )

        dimension = ProblemDimension(
            name="Test Dimension",
            description="A test dimension",
            importance="Very important",
            citations=[citation],
        )

        statement = ProblemStatement(
            title="Test Problem",
            summary="A test problem summary",
            dimensions=[dimension],
            all_citations=[citation],
        )

        assert statement.title == "Test Problem"
        assert len(statement.dimensions) == 1
        assert statement.dimensions[0].name == "Test Dimension"
        assert len(statement.all_citations) == 1


class TestSessionManager:
    """Test session management."""

    def test_session_creation(self, tmp_path):
        """Test creating a new session."""
        session = SessionManager(tmp_path)

        assert session.session_dir == tmp_path
        assert session.state_file == tmp_path / "state.json"
        assert session.state.stage == "initialized"
        assert session.state.iteration == 0

    def test_state_persistence(self, tmp_path):
        """Test saving and loading state."""
        session = SessionManager(tmp_path)

        session.state.initial_problem = "Test problem"
        session.state.stage = "research_complete"
        session.save()

        session2 = SessionManager(tmp_path)

        assert session2.state.initial_problem == "Test problem"
        assert session2.state.stage == "research_complete"

    def test_stage_updates(self, tmp_path):
        """Test stage updates."""
        session = SessionManager(tmp_path)

        session.update_stage("capturing_problem")
        assert session.state.stage == "capturing_problem"

        session.update_stage("problem_captured")
        assert session.state.stage == "problem_captured"

    def test_iteration_increment(self, tmp_path):
        """Test iteration increment."""
        session = SessionManager(tmp_path)
        session.state.max_iterations = 3

        assert session.increment_iteration()
        assert session.state.iteration == 1

        assert session.increment_iteration()
        assert session.state.iteration == 2

        assert session.increment_iteration()
        assert session.state.iteration == 3

        assert not session.increment_iteration()
        assert session.state.iteration == 4

    def test_search_budget(self, tmp_path):
        """Test search budget tracking."""
        session = SessionManager(tmp_path)
        session.state.max_searches = 5

        for i in range(5):
            assert session.increment_searches()
            assert session.state.searches_used == i + 1

        assert not session.increment_searches()
        assert session.state.searches_used == 6


class TestOutputGeneration:
    """Test output generation."""

    def test_slugify(self):
        """Test slug generation."""
        from ..stages.output import slugify

        assert slugify("Test Problem") == "test-problem"
        assert slugify("Users Struggle with X") == "users-struggle-with-x"
        assert slugify("Problem: A & B") == "problem-a-b"
        assert slugify("  Spaces  Everywhere  ") == "spaces-everywhere"


@pytest.fixture
def tmp_path(tmp_path_factory):
    """Create temporary directory for tests."""
    return tmp_path_factory.mktemp("problemexplorer_test")
