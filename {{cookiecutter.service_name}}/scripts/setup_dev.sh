#!/usr/bin/env bash
set -euo pipefail

echo "Setting up {{ cookiecutter.service_name }} development environment..."

if command -v python3.12 >/dev/null 2>&1; then
  PYTHON=python3.12
else
  PYTHON=python3
fi

echo "[INFO] Using Python: $($PYTHON --version)"

if [ ! -x ".venv/bin/pip" ]; then
  rm -rf .venv
  "$PYTHON" -m venv .venv
fi

.venv/bin/pip install --upgrade pip poetry
POETRY_VIRTUALENVS_IN_PROJECT=1 .venv/bin/poetry env use .venv/bin/python
.venv/bin/poetry install --with dev
if git rev-parse --git-dir >/dev/null 2>&1; then
  .venv/bin/pre-commit install
else
  echo "Note: skipped pre-commit install (not a git repository yet)"
fi

echo "✓ Setup complete. Run: make check && make test"
