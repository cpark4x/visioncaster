#!/bin/bash
# Run ProblemSpace with proper PYTHONPATH

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AMPLIFIER_PATH="$SCRIPT_DIR/../../amplifier"

PYTHONPATH="$AMPLIFIER_PATH:$PYTHONPATH" python3 -m scenarios.problemspace "$@"
