.PHONY: setup check format-check lint-check format lint types layers test run

# First-time setup: creates .venv, installs deps, installs pre-commit hooks.
# Run once after cloning: make setup
setup:
	@bash scripts/setup_dev.sh

# Read-only quality gate — safe for CI and pre-commit.
# All checks report errors; none auto-fix. Run `make format` and `make lint` to fix locally.
check: format-check lint-check types layers

format-check:
	.venv/bin/black --check --line-length 100 src/ tests/

lint-check:
	.venv/bin/ruff check src/ tests/

# Mutating targets — run locally to fix formatting/lint issues before committing.
format:
	.venv/bin/black --line-length 100 src/ tests/

lint:
	.venv/bin/ruff check --fix src/ tests/

types:
	.venv/bin/pyright

layers:
	.venv/bin/lint-imports

test:
	.venv/bin/pytest tests/unit/ -v

run:
	.venv/bin/python -m src.main
