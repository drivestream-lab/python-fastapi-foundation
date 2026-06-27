#!/usr/bin/env bash
set -euo pipefail
echo "Setting up {{cookiecutter.service_name}} development environment..."
[ ! -d ".venv" ] && python3 -m venv .venv
.venv/bin/pip install --upgrade pip poetry
.venv/bin/poetry install --with dev
.venv/bin/pre-commit install
echo "✓ Setup complete. Run: make check && make test"
