# {{cookiecutter.service_name}} — Agent Constitution

## Rules (read before writing any code)
- `.cursor/rules/` — python-services-rules submodule (alwaysApply — enforced by CI)

## Skills (dev bundle — prayog-skills)
Exposed as `.claude/commands/` slash commands:
- `/spec-feasibility-review` — on spec handoff PR branch
- `/spec-implementation-plan` — after spec merged
- `/pre-implement` — before each wave
- `/verify` — after each wave

## Product spec
- `docs/specification/product/` — what to build
- `docs/specification/as-built/implementation-status.md` — what is live

## Run commands
```bash
make setup     # first-time setup
make check     # format + lint + types + layers (all must pass before PR)
make test      # pytest tests/unit/
make run       # start service on port {{cookiecutter.default_port}}
make verify    # live verify (requires running infra — see docker/docker-compose.yml)
```

## Service identity
- Port: {{cookiecutter.default_port}}
- Auth: {{cookiecutter.auth_mode}}
- Description: {{cookiecutter.service_description}}

## Wave discipline
- One wave = one board issue = one branch = one PR
- Branch: `feature/<INITIATIVE>-w{N}-{slug}`
- `make check && make test` must be green before opening any PR
- Update `docs/specification/as-built/implementation-status.md` in same commit as code
