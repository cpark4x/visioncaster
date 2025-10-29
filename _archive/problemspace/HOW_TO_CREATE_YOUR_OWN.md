# How to Create Your Own Scenario Tool

This guide shows you how to create scenario tools like ProblemSpace using amplifier patterns.

## Overview

Scenario tools are multi-stage pipelines that combine:
- **Code for structure** - State management, flow control, gates
- **AI for intelligence** - Analysis, generation, recommendations
- **Human for decisions** - Approval, feedback, direction

## The Pattern

Every scenario tool follows this structure:

```
scenarios/
└── your_tool/
    ├── __init__.py
    ├── __main__.py
    ├── README.md
    ├── main.py              # Pipeline orchestrator
    ├── state.py             # State management
    ├── stages/
    │   ├── __init__.py
    │   ├── stage1.py
    │   ├── stage2.py
    │   └── stageN.py
    ├── templates/
    │   └── output_template.md
    └── tests/
        └── test_tool.py
```

## Step-by-Step Guide

### 1. Define Your Pipeline

Before coding, map out:

**What problem does this solve?**
- ProblemSpace: Validates problems before building
- BlogWriter: Transforms ideas into polished posts
- Your tool: ___?

**What are the stages?**
- Each stage should have one clear purpose
- Identify which need AI vs human input
- Define gates (what must pass to proceed?)

**What's the final output?**
- Document, code, report, etc.

### 2. Create State Schema

Define your state in `state.py`:

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class YourStage1Data:
    """Data from stage 1."""
    field1: str = ""
    field2: list[str] = field(default_factory=list)

@dataclass
class YourStage2Data:
    """Data from stage 2."""
    analysis: str = ""
    score: float = 0.0

@dataclass
class YourToolState:
    """Complete pipeline state."""

    stage: str = "initialized"

    stage1: YourStage1Data = field(default_factory=YourStage1Data)
    stage2: YourStage2Data = field(default_factory=YourStage2Data)

    history: list[dict[str, Any]] = field(default_factory=list)

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
```

### 3. Create StateManager

Use the amplifier pattern:

```python
from pathlib import Path
from amplifier.ccsdk_toolkit.defensive.file_io import read_json_with_retry, write_json_with_retry
from amplifier.utils.logger import get_logger

logger = get_logger(__name__)

class StateManager:
    """Manages pipeline state with automatic persistence."""

    def __init__(self, session_dir: Path | None = None):
        if session_dir is None:
            base_dir = Path(".data/your_tool")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_dir = base_dir / timestamp

        self.session_dir = session_dir
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.session_dir / "state.json"
        self.state = self._load_state()

    def _load_state(self) -> YourToolState:
        """Load state from file or create new."""
        if self.state_file.exists():
            try:
                data = read_json_with_retry(self.state_file)
                # Reconstruct state from JSON
                return YourToolState(**data)
            except Exception as e:
                logger.warning(f"Could not load state: {e}")

        return YourToolState()

    def save(self) -> None:
        """Save current state to file."""
        self.state.updated_at = datetime.now().isoformat()
        state_dict = asdict(self.state)
        write_json_with_retry(state_dict, self.state_file)

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
```

### 4. Create Stage Modules

Each stage is an independent module in `stages/`:

```python
# stages/your_stage.py

from amplifier.utils.logger import get_logger
from ..state import YourStageData

logger = get_logger(__name__)

def run_your_stage(input_data: PreviousStageData) -> YourStageData:
    """Execute this stage.

    Args:
        input_data: Output from previous stage

    Returns:
        YourStageData: Results for this stage
    """
    logger.info("\n🎯 Your Stage Name")
    logger.info("=" * 60)

    # Stage logic here
    # - Human input via input()
    # - AI calls via subprocess
    # - Validation and gates

    result = YourStageData(...)

    logger.info("✅ Stage complete")
    return result
```

**Stage Design Tips:**
- One stage = one responsibility
- Clear input/output contracts
- No side effects (return data, don't modify external state)
- Use logger for progress updates
- Handle errors gracefully

### 5. Create Pipeline Orchestrator

In `main.py`:

```python
from amplifier.utils.logger import get_logger
from .state import StateManager
from .stages import stage1, stage2, stage3

logger = get_logger(__name__)

class YourToolPipeline:
    """Orchestrates the pipeline."""

    def __init__(self, state_manager: StateManager):
        self.state = state_manager

    def run(self) -> bool:
        """Run the complete pipeline."""
        stage = self.state.state.stage
        logger.info(f"Starting from stage: {stage}")

        try:
            # Execute stages in order
            if stage == "initialized":
                self._run_stage1()
                stage = self.state.state.stage

            if stage == "stage1_complete":
                self._run_stage2()
                stage = self.state.state.stage

            if stage == "stage2_complete":
                self._run_stage3()
                self.state.mark_complete()
                return True

            return stage == "complete"

        except KeyboardInterrupt:
            logger.info("\n⚠️ Pipeline interrupted")
            logger.info("Progress saved. Run with --resume to continue.")
            return False
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return False

    def _run_stage1(self) -> None:
        """Run stage 1."""
        logger.info("\n" + "=" * 60)
        logger.info("STAGE 1: DESCRIPTION")
        logger.info("=" * 60)

        result = stage1()
        self.state.state.stage1 = result
        self.state.update_stage("stage1_complete")
        self.state.add_history({"stage": "stage1", "status": "complete"})
```

### 6. Add CLI Interface

Use click for CLI:

```python
import click
from pathlib import Path

@click.command()
@click.option("--resume", is_flag=True, help="Resume from saved state")
@click.option("--reset", is_flag=True, help="Reset state and start fresh")
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
def main(resume: bool, reset: bool, verbose: bool):
    """Your Tool - Description.

    Example:
        python -m scenarios.your_tool
        python -m scenarios.your_tool --resume
    """
    if verbose:
        logger.logger.setLevel("DEBUG")

    # Session management
    session_dir = None
    if resume:
        base_dir = Path(".data/your_tool")
        if base_dir.exists():
            sessions = sorted([d for d in base_dir.iterdir() if d.is_dir()], reverse=True)
            if sessions:
                session_dir = sessions[0]

    state_manager = StateManager(session_dir)

    if reset:
        state_manager.reset()
        logger.info("State reset - starting fresh")

    # Run pipeline
    pipeline = YourToolPipeline(state_manager)
    success = pipeline.run()

    if success:
        logger.info("\n✨ Complete!")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 7. Create Module Exports

`__init__.py`:
```python
"""
Your Tool

Description of what it does.
"""

from .state import StateManager, YourToolState
from .main import YourToolPipeline

__all__ = [
    "StateManager",
    "YourToolState",
    "YourToolPipeline",
]
```

`__main__.py`:
```python
"""CLI Entry Point"""

from .main import main

if __name__ == "__main__":
    main()
```

### 8. Add AI Integration

For AI-powered stages, use subprocess to call claude-code:

```python
import subprocess
import json
from pathlib import Path

def call_ai(prompt: str) -> dict:
    """Call AI with prompt, return structured response.

    Args:
        prompt: The prompt text

    Returns:
        Parsed JSON response
    """
    temp_file = Path("/tmp/your_tool_prompt.txt")
    temp_file.write_text(prompt)

    try:
        result = subprocess.run(
            ["claude-code", "--prompt-file", str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            raise Exception(f"AI call failed: {result.stderr}")

    except Exception as e:
        logger.warning(f"AI error: {e}")
        return {}  # Fallback
```

### 9. Write Tests

Basic test structure:

```python
import pytest
from pathlib import Path
from scenarios.your_tool.state import StateManager, YourToolState

def test_state_creation():
    """Test state manager creates state."""
    manager = StateManager()
    assert manager.state.stage == "initialized"
    assert manager.session_dir.exists()

def test_state_persistence(tmp_path):
    """Test state saves and loads."""
    manager = StateManager(tmp_path)
    manager.state.stage = "stage1_complete"
    manager.save()

    # Reload
    manager2 = StateManager(tmp_path)
    assert manager2.state.stage == "stage1_complete"
```

## Key Principles

### 1. Ruthless Simplicity

- Start with MVP
- Add complexity only when needed
- Simple subprocess calls > complex SDK integration
- Plain data structures > complex abstractions

### 2. Bricks and Studs

- Each stage is independent
- Clear input/output contracts
- Can be replaced/regenerated
- Testable in isolation

### 3. Code for Structure, AI for Intelligence

**Use code for:**
- State management
- Flow control
- Gates and validation
- File I/O
- Error handling

**Use AI for:**
- Analysis
- Generation
- Recommendations
- Insight extraction

### 4. Resumable

- Save state after every operation
- Handle Ctrl+C gracefully
- Resume from any stage
- Audit trail in history

## Common Patterns

### Pattern: Human Input Stage

```python
def capture_user_input() -> UserData:
    """Get input from user."""
    print("\nEnter your data:")
    print("(Ctrl+D when done)\n")

    lines = []
    try:
        while True:
            lines.append(input())
    except EOFError:
        pass

    return UserData(content="\n".join(lines))
```

### Pattern: AI Analysis Stage

```python
def analyze_with_ai(input_data: str) -> Analysis:
    """Analyze data with AI."""
    prompt = f"""Analyze this data and return JSON:

    {input_data}

    Return: {{"score": 0-10, "insights": ["..."]}}
    """

    response = call_ai(prompt)
    return Analysis(
        score=response.get("score", 0),
        insights=response.get("insights", [])
    )
```

### Pattern: Gate Logic

```python
def check_gate(data: StageData) -> bool:
    """Check if stage can proceed."""
    if data.score < 5.0:
        logger.warning("⚠️ Low score - consider revising")
        return False

    if not data.required_field:
        logger.error("❌ Missing required field")
        return False

    logger.info("✅ Gate passed")
    return True
```

### Pattern: Output Generation

```python
def generate_output(state: YourToolState, session_dir: Path) -> Path:
    """Generate final output document."""
    output_path = session_dir / "output.md"

    content = _generate_markdown(state)
    output_path.write_text(content)

    logger.info(f"✅ Output saved: {output_path}")
    return output_path
```

## Examples from amplifier

Study these existing scenario tools:

### blog_writer

- Multi-stage with iteration loop
- Style extraction from examples
- Review and revision cycle
- User feedback integration

### problemspace (this tool)

- Linear 6-stage pipeline
- AI analysis with fallback
- Human gates and approval
- Evidence-based validation

## Checklist

Before releasing your tool:

- [ ] State persists correctly
- [ ] Resume works from any stage
- [ ] Handles Ctrl+C gracefully
- [ ] Clear stage progression
- [ ] Helpful logging output
- [ ] README with examples
- [ ] Basic tests pass
- [ ] Error messages are actionable
- [ ] CLI options documented
- [ ] Output is useful

## Next Steps

1. **Start simple** - MVP with 3 stages
2. **Test early** - Run through pipeline manually
3. **Iterate** - Add stages and features incrementally
4. **Document** - README and examples
5. **Share** - Add to amplifier scenarios/

## Resources

- `scenarios/blog_writer/` - Reference implementation
- `scenarios/problemspace/` - This tool
- `amplifier/ccsdk_toolkit/` - Defensive utilities
- `amplifier/utils/logger.py` - Logging

## Questions?

Common questions:

**Q: Should I use async?**
A: Only if you need true parallelism. Most scenario tools are sequential and don't benefit from async.

**Q: How do I handle long AI calls?**
A: Use subprocess with timeout. Show progress indicators. Have fallbacks.

**Q: What if a stage fails?**
A: Log the error, save state, exit gracefully. User can fix and resume.

**Q: How many stages?**
A: 3-7 is typical. Too few = not enough validation. Too many = tedious.

**Q: Should stages be interactive or batch?**
A: Depends on use case. Interactive = better UX. Batch = better for automation.

## Contributing

Share your scenario tools! Add to `amplifier/scenarios/` and submit PR.

Make amplifier better for everyone.
