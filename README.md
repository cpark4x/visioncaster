# VisionCaster

**AI-powered tools for product vision and problem validation**

## Project Overview

This repository contains amplifier-based CLI tools for helping teams establish clear product vision and validate problems before building solutions.

### Tools Included

1. **ProblemExplorer** (MVP Complete) - AI-research-first problem statement generator
2. **ProblemSpace v1** (Archived) - Learning artifact showing what not to build

## Quick Start

### Prerequisites

1. Python 3.9+
2. Amplifier toolkit (symlinked from `~/dev/toolkits/amplifier`)

### Installation

```bash
# Clone the repository
git clone [repository-url]
cd visioncaster

# Install amplifier dependencies (if not already installed)
cd amplifier
pip install -e .
cd ..
```

### Try ProblemExplorer

```bash
make problemexplorer PROBLEM="Your problem statement here"
```

Example:
```bash
make problemexplorer PROBLEM="Managing AI-first teams is challenging"
```

## What's Inside

### ProblemExplorer (`scenarios/problemexplorer/`)

**Status**: ✅ MVP Complete - Works end-to-end with mock data

An AI-research-first tool that:
- Takes a problem statement from the user
- Generates research queries automatically
- Executes searches (mock data in MVP)
- Synthesizes findings into structured dimensions
- Validates evidence quality
- Generates formatted problem statement documents

**Use cases**:
- Validating product ideas before building
- Research-backed problem statements for RFCs
- Exploring problem spaces systematically
- Documenting evidence for business cases

**Current state**: Fully functional MVP with mock data. Production requires:
- Real web search integration (SerpAPI or similar)
- Claude API for intelligent synthesis
- See [ProblemExplorer README](scenarios/problemexplorer/README.md) for details

### ProblemSpace v1 (`_archive/problemspace/`)

**Status**: ⚠️ Archived - Solved wrong problem

A validation tool where users provide evidence and AI formats it.

**Why archived**: User testing revealed fundamental flaw - it asked humans to do research they haven't done yet. The insight "people are lazy - AI should do the work" led to building ProblemExplorer v2 instead.

**Learning value**: Demonstrates that well-architected tools are useless if they solve the wrong problem. Preserved as learning artifact.

## Project Structure

```
visioncaster/
├── README.md                   # This file
├── STATUS.md                   # Detailed status and learnings
├── Makefile                    # Common commands
├── .gitignore                  # Git ignore rules
├── amplifier/                  # Symlink to ~/dev/toolkits/amplifier
├── _archive/                   # Archived/deprecated tools
│   └── problemspace/          # v1 - learning artifact
└── scenarios/                  # Active tools
    └── problemexplorer/       # v2 - MVP complete
        ├── README.md          # Tool documentation
        ├── main.py            # Entry point
        ├── models.py          # Data models
        ├── session_manager.py # State persistence
        └── stages/            # Pipeline stages
            ├── problem_capture.py
            ├── research.py
            ├── synthesis.py
            ├── validation.py
            ├── metrics.py
            └── output.py
```

## Documentation

- **[STATUS.md](STATUS.md)** - Current state, test results, and next steps
- **[ProblemExplorer README](scenarios/problemexplorer/README.md)** - Tool usage and architecture
- **[Archive README](_archive/README.md)** - Why v1 was archived

## Key Learnings

1. **MVP = Working End-to-End** - Mock data is fine; complete workflow matters
2. **User Testing Reveals Truth** - v1 looked great but wasn't useful
3. **User Insight Drives Pivots** - "People are lazy - AI should do the work"
4. **Test Before User Tests** - Fixed all issues before second round of testing
5. **Heuristics Work for MVP** - Don't need perfect AI to demonstrate value

## Development Philosophy

This project follows the **Amplifier CLI toolkit pattern**:

**Code for structure, AI for intelligence**

- **Code handles**: Pipeline orchestration, state management, data persistence, quality gates
- **AI handles**: Research decomposition, evidence extraction, synthesis, validation

This separation ensures tools are both reliable (code manages workflow) and intelligent (AI does reasoning).

See [Amplifier documentation](amplifier/README.md) for more on this philosophy.

## Make Commands

```bash
make help              # Show all available commands
make problemexplorer   # Run ProblemExplorer (requires PROBLEM="...")
make test             # Run tests (when implemented)
```

## Next Steps

### To Make ProblemExplorer Production-Ready

1. **Add real web search** (Critical)
   - Option A: SerpAPI (paid but reliable)
   - Option B: Browser automation (Selenium/Playwright)
   - Option C: MCP web search server

2. **Integrate Claude API** (Critical)
   - Replace heuristic query generation
   - Intelligent evidence synthesis
   - Nuanced quality validation

3. **Enhance output** (Nice to have)
   - Multiple export formats (JSON, PDF)
   - Citation deduplication
   - Visual dimension graphs

### To Build New Tools

Follow the ProblemExplorer pattern:
1. Clear problem statement
2. Multi-stage pipeline with state persistence
3. Code for structure, AI for intelligence
4. Test with mock data first
5. Add real integrations for production

## Contributing

This is a personal learning project demonstrating amplifier CLI tool patterns.

Contributions welcome for:
- Bug fixes
- Documentation improvements
- Production integrations (web search, Claude API)
- New tool scenarios

## License

[Add license here]

## Built With

- **[Amplifier](https://github.com/anthropics/amplifier)** - CLI tool framework
- Python 3.9+
- Click for CLI interfaces
- Pydantic for data validation

---

**Status**: MVP Complete | **Last Updated**: 2025-10-29

See [STATUS.md](STATUS.md) for detailed progress and learnings.
