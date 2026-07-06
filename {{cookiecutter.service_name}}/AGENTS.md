# {{cookiecutter.service_name}} — Agent Constitution

## Rules (read before writing any code)
- `.cursor/rules/` — python-services-rules submodule (alwaysApply — enforced by CI)

## Skills (dev bundle — prayog-skills)
Installed under `.agents/skills/` via harness sync (replaced by `launchpad sync-harness-app`):
- `/spec-draft` — PRD → spec slice for this repo
- `/initiative-feasibility` — on spec handoff PR branch
- `/spec-technical-review` — PE decisions + ADRs
- `/spec-implementation-plan` — wave plan + board seed YAML
- `/pre-implement` — before each wave
- `/loop-spec` — implement → verify → fix per task
- `/ground-spec` — wave complete; FR validation
- `/verify` — live CLI/API verification

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
