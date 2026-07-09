#!/usr/bin/env bash
set -euo pipefail

echo "Setting up {{ cookiecutter.service_name }} development environment..."

if ! command -v python3.12 >/dev/null 2>&1; then
  echo "[ERROR] python3.12 is required. Install Python 3.12 and retry."
  echo "        Check: python3.12 --version"
  exit 1
fi

PYTHON=python3.12
PY_VERSION="$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ "$PY_VERSION" != "3.12" ]]; then
  echo "[ERROR] Expected Python 3.12, got $PY_VERSION from $PYTHON"
  exit 1
fi

echo "[INFO] Using Python: $($PYTHON --version)"

if [ ! -x ".venv/bin/pip" ]; then
  rm -rf .venv
  "$PYTHON" -m venv .venv
fi

echo "[INFO] .venv Python: $(.venv/bin/python --version)"

.venv/bin/pip install --upgrade pip poetry
POETRY_VIRTUALENVS_IN_PROJECT=1 .venv/bin/poetry env use .venv/bin/python
.venv/bin/poetry install --with dev

for tool in black ruff pyright pytest; do
  if [ ! -x ".venv/bin/$tool" ]; then
    echo "[ERROR] Toolchain incomplete: .venv/bin/$tool is missing after poetry install"
    exit 1
  fi
done

if git rev-parse --git-dir >/dev/null 2>&1; then
  .venv/bin/pre-commit install
else
  echo "Note: skipped pre-commit install (not a git repository yet)"
fi

echo "✓ Setup complete. Run: make check && make test"
