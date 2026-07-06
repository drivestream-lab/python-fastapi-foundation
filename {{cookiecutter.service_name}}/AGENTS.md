# {{cookiecutter.service_name}} — Agent guide

## Constitution

Read **`.cursor/rules/*.mdc`** (python-services-rules submodule) before writing code.

## Harness (run from tenant meta after clone)

```bash
launchpad sync-harness-app --repo {{cookiecutter.service_name}} --apply
```

That writes this file, `.harness-pin.yaml`, the rules submodule @ pinned ref, and prayog dev skills under `.agents/skills/`. **Do not** hand-maintain skill lists here before sync.

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
