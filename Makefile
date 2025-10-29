# VisionCaster Makefile

.PHONY: help problemexplorer problemexplorer-resume problemexplorer-reset test

help: ## Show this help message
	@echo "VisionCaster - AI-First Problem Discovery"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'

problemexplorer: ## Discover and validate problems with AI research
	@if [ -z "$(PROBLEM)" ]; then \
		echo "Usage: make problemexplorer PROBLEM='your problem description'"; \
		echo "Example: make problemexplorer PROBLEM='Managing AI-first teams is difficult'"; \
		exit 1; \
	fi
	@PYTHONPATH=$$PYTHONPATH:./amplifier python3 -m scenarios.problemexplorer --problem "$(PROBLEM)"

problemexplorer-resume: ## Resume previous ProblemExplorer session
	@PYTHONPATH=$$PYTHONPATH:./amplifier python3 -m scenarios.problemexplorer --resume

problemexplorer-reset: ## Reset and start fresh
	@PYTHONPATH=$$PYTHONPATH:./amplifier python3 -m scenarios.problemexplorer --reset

test: ## Run all tests
	@echo "Running tests..."
	@cd scenarios/problemexplorer && python3 -m pytest tests/
