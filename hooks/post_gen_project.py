#!/usr/bin/env python3
"""Post-generation hook: format Python sources for day-one-green make check."""

import shutil
import subprocess

SERVICE_NAME = "{{cookiecutter.service_name}}"


def format_python() -> None:
    black = shutil.which("black")
    if not black:
        print("Note: black not on PATH — run `make format` before `make check`.")
        return
    subprocess.run([black, "--line-length", "100", "src", "tests"], check=False)


format_python()

print(f"""
✓ {SERVICE_NAME} scaffold generated successfully.

Next steps:
  cd {SERVICE_NAME}
  cp .env.example .env
  make setup
  docker compose -f docker/docker-compose.yml up -d
  make check && make test
  make run

Live verify: tests/verify/01-health-detailed.md
""")
