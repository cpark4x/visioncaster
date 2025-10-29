# ProblemSpace Usage Guide

Quick reference for using ProblemSpace.

## Installation

ProblemSpace is part of visioncaster which symlinks to amplifier toolkit.

## Running ProblemSpace

### Option 1: Using the run script (recommended)

```bash
cd scenarios/problemspace
./run.sh
```

### Option 2: Using Python module directly

```bash
# From visioncaster root
PYTHONPATH=amplifier:$PYTHONPATH python3 -m scenarios.problemspace
```

### Option 3: Resume session

```bash
./run.sh --resume
```

### Option 4: Reset and start fresh

```bash
./run.sh --reset
```

### Option 5: Verbose logging

```bash
./run.sh --verbose
```

## Running Tests

```bash
cd scenarios/problemspace
./run_tests.sh
```

Or with specific pytest options:

```bash
./run_tests.sh -v --tb=short
./run_tests.sh -k test_state_creation
```

## Session Data

Sessions are saved in `.data/problemspace/<timestamp>/`:

```
.data/problemspace/20241028_143000/
├── state.json                          # Complete state
└── problem-statement-<slug>.md         # Final output (after approval)
```

## Example Workflow

```bash
# Start new problem validation
./run.sh

# Follow interactive prompts:
# 1. Describe problem
# 2. AI analysis
# 3. Provide evidence
# 4. Define metrics
# 5. Review and approve

# If interrupted, resume:
./run.sh --resume

# Output saved to:
# .data/problemspace/<timestamp>/problem-statement-<slug>.md
```

## Tips

1. **Be specific** - More context = better AI analysis
2. **Have evidence ready** - Data, research, competitive info
3. **Think about metrics** - How will you measure success?
4. **Review carefully** - Final approval gates the build
5. **Use --resume** - Safe to interrupt and continue later

## Troubleshooting

**Import errors:**
- Ensure amplifier symlink exists: `ls -la ../../amplifier`
- Use run.sh which sets PYTHONPATH automatically

**Can't resume:**
- Check `.data/problemspace/` exists
- Verify state.json is valid JSON
- Use `--reset` to start fresh

**AI analysis fails:**
- Check network connection
- Verify claude-code CLI installed
- Pipeline continues with fallback analysis

## Integration with amplifier

ProblemSpace uses:
- `amplifier.ccsdk_toolkit.defensive.file_io` - Safe file operations
- `amplifier.utils.logger` - Consistent logging
- `amplifier` patterns - State management, stages, gates

See `HOW_TO_CREATE_YOUR_OWN.md` for creating similar tools.
