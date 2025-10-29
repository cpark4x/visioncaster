"""
Data Models for ProblemExplorer

Defines all data structures used throughout the 6-stage pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Citation:
    """Source citation with evidence."""

    url: str
    title: str
    relevant_excerpt: str
    fetch_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ResearchQuery:
    """A research query to be executed."""

    query: str
    purpose: str
    priority: int = 1


@dataclass
class ResearchResult:
    """Result from a single research query."""

    query: ResearchQuery
    citation: Citation | None = None
    error: str | None = None


@dataclass
class ProblemDimension:
    """A dimension/facet of the problem."""

    name: str
    description: str
    importance: str
    citations: list[Citation] = field(default_factory=list)


@dataclass
class ProblemStatement:
    """Complete problem statement with evidence."""

    title: str
    summary: str
    dimensions: list[ProblemDimension] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    all_citations: list[Citation] = field(default_factory=list)


@dataclass
class ValidationIssue:
    """Issue found during validation."""

    dimension: str
    issue_type: str  # "insufficient_evidence", "weak_claim", "unsupported"
    description: str
    severity: str  # "low", "medium", "high"


@dataclass
class QualityMetrics:
    """Quality assessment metrics."""

    evidence_strength: str  # "weak", "moderate", "strong"
    coverage_score: float  # 0-1
    citation_count: int
    dimension_count: int
    issues_found: int
    overall_quality: str  # "needs_work", "acceptable", "good", "excellent"
    recommendations: list[str] = field(default_factory=list)


@dataclass
class PipelineState:
    """Complete pipeline state for persistence."""

    # Pipeline tracking
    stage: str = "initialized"
    iteration: int = 0
    max_iterations: int = 3

    # Input
    initial_problem: str = ""

    # Stage outputs
    research_queries: list[ResearchQuery] = field(default_factory=list)
    research_results: list[ResearchResult] = field(default_factory=list)
    problem_statement: ProblemStatement | None = None
    validation_issues: list[ValidationIssue] = field(default_factory=list)
    quality_metrics: QualityMetrics | None = None

    # Search budget tracking
    searches_used: int = 0
    max_searches: int = 15

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Output
    output_path: str | None = None


def pipeline_state_to_dict(state: PipelineState) -> dict[str, Any]:
    """Convert PipelineState to dict for JSON serialization."""

    def citation_to_dict(c: Citation) -> dict:
        return {
            "url": c.url,
            "title": c.title,
            "relevant_excerpt": c.relevant_excerpt,
            "fetch_timestamp": c.fetch_timestamp,
        }

    def query_to_dict(q: ResearchQuery) -> dict:
        return {
            "query": q.query,
            "purpose": q.purpose,
            "priority": q.priority,
        }

    def result_to_dict(r: ResearchResult) -> dict:
        return {
            "query": query_to_dict(r.query),
            "citation": citation_to_dict(r.citation) if r.citation else None,
            "error": r.error,
        }

    def dimension_to_dict(d: ProblemDimension) -> dict:
        return {
            "name": d.name,
            "description": d.description,
            "importance": d.importance,
            "citations": [citation_to_dict(c) for c in d.citations],
        }

    def statement_to_dict(s: ProblemStatement | None) -> dict | None:
        if not s:
            return None
        return {
            "title": s.title,
            "summary": s.summary,
            "dimensions": [dimension_to_dict(d) for d in s.dimensions],
            "assumptions": s.assumptions,
            "all_citations": [citation_to_dict(c) for c in s.all_citations],
        }

    def issue_to_dict(i: ValidationIssue) -> dict:
        return {
            "dimension": i.dimension,
            "issue_type": i.issue_type,
            "description": i.description,
            "severity": i.severity,
        }

    def metrics_to_dict(m: QualityMetrics | None) -> dict | None:
        if not m:
            return None
        return {
            "evidence_strength": m.evidence_strength,
            "coverage_score": m.coverage_score,
            "citation_count": m.citation_count,
            "dimension_count": m.dimension_count,
            "issues_found": m.issues_found,
            "overall_quality": m.overall_quality,
            "recommendations": m.recommendations,
        }

    return {
        "stage": state.stage,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "initial_problem": state.initial_problem,
        "research_queries": [query_to_dict(q) for q in state.research_queries],
        "research_results": [result_to_dict(r) for r in state.research_results],
        "problem_statement": statement_to_dict(state.problem_statement),
        "validation_issues": [issue_to_dict(i) for i in state.validation_issues],
        "quality_metrics": metrics_to_dict(state.quality_metrics),
        "searches_used": state.searches_used,
        "max_searches": state.max_searches,
        "created_at": state.created_at,
        "updated_at": state.updated_at,
        "output_path": state.output_path,
    }


def pipeline_state_from_dict(data: dict[str, Any]) -> PipelineState:
    """Reconstruct PipelineState from dict."""

    def dict_to_citation(d: dict) -> Citation:
        return Citation(
            url=d["url"],
            title=d["title"],
            relevant_excerpt=d["relevant_excerpt"],
            fetch_timestamp=d.get("fetch_timestamp", datetime.now().isoformat()),
        )

    def dict_to_query(d: dict) -> ResearchQuery:
        return ResearchQuery(
            query=d["query"],
            purpose=d["purpose"],
            priority=d.get("priority", 1),
        )

    def dict_to_result(d: dict) -> ResearchResult:
        return ResearchResult(
            query=dict_to_query(d["query"]),
            citation=dict_to_citation(d["citation"]) if d.get("citation") else None,
            error=d.get("error"),
        )

    def dict_to_dimension(d: dict) -> ProblemDimension:
        return ProblemDimension(
            name=d["name"],
            description=d["description"],
            importance=d["importance"],
            citations=[dict_to_citation(c) for c in d.get("citations", [])],
        )

    def dict_to_statement(d: dict | None) -> ProblemStatement | None:
        if not d:
            return None
        return ProblemStatement(
            title=d["title"],
            summary=d["summary"],
            dimensions=[dict_to_dimension(dim) for dim in d.get("dimensions", [])],
            assumptions=d.get("assumptions", []),
            all_citations=[dict_to_citation(c) for c in d.get("all_citations", [])],
        )

    def dict_to_issue(d: dict) -> ValidationIssue:
        return ValidationIssue(
            dimension=d["dimension"],
            issue_type=d["issue_type"],
            description=d["description"],
            severity=d["severity"],
        )

    def dict_to_metrics(d: dict | None) -> QualityMetrics | None:
        if not d:
            return None
        return QualityMetrics(
            evidence_strength=d["evidence_strength"],
            coverage_score=d["coverage_score"],
            citation_count=d["citation_count"],
            dimension_count=d["dimension_count"],
            issues_found=d["issues_found"],
            overall_quality=d["overall_quality"],
            recommendations=d.get("recommendations", []),
        )

    return PipelineState(
        stage=data.get("stage", "initialized"),
        iteration=data.get("iteration", 0),
        max_iterations=data.get("max_iterations", 3),
        initial_problem=data.get("initial_problem", ""),
        research_queries=[dict_to_query(q) for q in data.get("research_queries", [])],
        research_results=[dict_to_result(r) for r in data.get("research_results", [])],
        problem_statement=dict_to_statement(data.get("problem_statement")),
        validation_issues=[dict_to_issue(i) for i in data.get("validation_issues", [])],
        quality_metrics=dict_to_metrics(data.get("quality_metrics")),
        searches_used=data.get("searches_used", 0),
        max_searches=data.get("max_searches", 15),
        created_at=data.get("created_at", datetime.now().isoformat()),
        updated_at=data.get("updated_at", datetime.now().isoformat()),
        output_path=data.get("output_path"),
    )
