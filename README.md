# python-fastapi-foundation

**Cookiecutter chassis for Python FastAPI microservices** — production-grade shape aligned with existing services (abhilekh, parichay, kavach, pravah, airforge).

| | |
|---|---|
| **Template engine** | Cookiecutter |
| **Version** | see [`VERSION`](VERSION) (currently **0.3.1**) · [CHANGELOG](CHANGELOG.md) |
| **Stack** | FastAPI · SQLAlchemy async · Postgres · Redis · OTEL · JWT · Injector DI |

## What the chassis guarantees

1. **Shape** — layered `src/`, DI modules, API layout (`health`, `internal/v1`, `v1`)
2. **Real infra** — wired Postgres, Redis, and OpenTelemetry services (not stubs)
3. **Hello world** — `/health` simple + `?detailed=true` with real postgres/redis checks
4. **Day-one-green CI** — `make check` / `make test` pass immediately

## Options

| Option | Meaning |
|--------|---------|
| `service_name` | Package identity, db name, redis prefix, OTEL service name |
| `service_description` | Description |
| `default_port` | Dev server port |

Always included (no toggles): Postgres, Redis, OTEL, JWT auth middleware, Alembic, Docker entrypoint.

## Usage

```bash
pip install cookiecutter
cookiecutter /path/to/python-fastapi-foundation
```

After generation:

```bash
cd <service-name>
cp .env.example .env
make setup
docker compose -f docker/docker-compose.yml up -d
make check && make test
make run
```

Live verify: `tests/verify/01-health-detailed.md`
