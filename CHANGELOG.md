# Changelog

All notable changes to `python-fastapi-foundation` are documented here.

---

## v0.3.2

### Summary

Fail fast when conda is active during `make setup` — prevents Poetry installing into the wrong environment.

### Changes

- **`scripts/setup_dev.sh`** — exit with clear message if `CONDA_DEFAULT_ENV` / `CONDA_PREFIX` is set; unset `VIRTUAL_ENV` before Poetry; verify Poetry resolves to project `.venv` after install

### Migration guide

- Regenerate from v0.3.2+ or copy updated `setup_dev.sh` into existing scaffolds
- No runtime API changes

---

## v0.3.1

### Summary

Harden day-one toolchain setup — require Python 3.12, verify dev tools after install, commit `poetry.lock`.

### Changes

- **`scripts/setup_dev.sh`** — fail fast without `python3.12`; verify `black`, `ruff`, `pyright`, `pytest` exist after `poetry install`
- **`poetry.lock`** — committed in template for reproducible `poetry install` on first `make setup`

### Migration guide

- Regenerate services from v0.3.1+ template, or copy `setup_dev.sh` + `poetry.lock` into existing scaffolds
- No runtime API changes

---

## v0.3.0

### Summary

Enterprise baseline — real Postgres/Redis/OTEL, simplified cookiecutter (3 options), harness files removed from scaffold.

See git history and release notes for v0.3.0 merge.
