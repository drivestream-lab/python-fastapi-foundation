# python-fastapi-foundation

Canonical cookiecutter template for DriveStream Python FastAPI microservices.

Every service generated from this template starts with the full settled foundation:
layered architecture, DI, auth, structured logging, OTel, Postgres/Redis/Kafka/EMQX
options, Makefile quality gates, Dockerfile, harness pins, and spec-driven test layout.

---

## Usage

### Generate a new service

```bash
# One-time: install cookiecutter
pip install cookiecutter

# Generate (prompts for options)
cookiecutter gh:drivestream-lab/python-fastapi-foundation

# Or from a local clone
cookiecutter /path/to/python-fastapi-foundation
```

### After generation

```bash
cd <service-name>
cp .env.example .env          # fill in secrets + service config
make setup                    # creates .venv, installs deps, pre-commit hooks
make check                    # should be green immediately
make test                     # health unit test passes on day 1
```

Then wire the new repo into the platform:

```bash
launchpad sync-harness --repo <service-name> --apply
```

---

## Cookiecutter options

| Option | Choices | Description |
|--------|---------|-------------|
| `service_name` | string | Kebab-case service name (e.g. `suchana`) |
| `service_description` | string | One-line description |
| `default_port` | number | Uvicorn default port |
| `auth_mode` | `jwt` / `allowlist` / `mtls` / `none` | Inbound auth strategy |
| `has_postgres` | `yes` / `no` | PostgreSQL via SQLAlchemy async + Alembic |
| `has_redis` | `yes` / `no` | Redis connection manager |
| `has_kafka` | `no` / `yes` | Kafka consumer (aiokafka) |
| `has_s3` | `no` / `yes` | S3/CloudFront (boto3) |
| `has_cratedb` | `no` / `yes` | CrateDB client |
| `has_emqx` | `no` / `yes` | EMQX REST publish service |
| `has_telemetry` | `yes` / `no` | OpenTelemetry (OTLP HTTP → Alloy) |
| `has_internal_api` | `no` / `yes` | Network-trusted `/internal` router |
| `parichay_client` | `yes` / `no` | HTTP client for Parichay (auth/JWT) |
| `abhilekh_client` | `no` / `yes` | HTTP client for Abhilekh (device registry) |
| `kavach_client` | `no` / `yes` | HTTP client for Kavach |

The post-generation hook (`hooks/post_gen_project.py`) automatically removes all
infra service files, settings modules, and models that were not selected.

---

## What you get

### Folder structure (all options enabled)

```
<service-name>/
├── src/
│   ├── main.py                     # uvicorn entry point (factory pattern)
│   ├── app.py                      # FastAPI lifespan + DI + middleware
│   ├── api/
│   │   ├── health/health_router.py # GET /health
│   │   ├── internal/               # network-trust /internal (optional)
│   │   └── v1/                     # JWT-authenticated /api/v1 routes
│   ├── business_services/
│   │   └── base_business_service.py
│   ├── infra_services/
│   │   ├── base_infra_service.py
│   │   ├── postgres_service.py
│   │   ├── redis_service.py
│   │   ├── telemetry_service.py
│   │   ├── kafka_consumer_service.py
│   │   ├── emqx_publish_service.py
│   │   ├── cratedb_service.py
│   │   ├── s3_service.py
│   │   ├── parichay_client.py
│   │   ├── abhilekh_client.py
│   │   └── kavach_client.py
│   ├── database/
│   │   ├── postgres/{connection_manager,schema/,repository/}
│   │   └── redis/connection.py
│   ├── di/
│   │   ├── dependency_container.py
│   │   └── modules/{infra,business_services}_module.py
│   ├── configs/
│   │   ├── base_settings.py        # PREFIX + get_instance() singleton pattern
│   │   ├── app_settings.py
│   │   └── *_settings.py           # one per integration
│   ├── common/auth/
│   │   ├── config.py
│   │   └── middleware.py           # JWT Bearer → AuthContext
│   ├── middleware/
│   │   ├── allowlist_middleware.py
│   │   └── mtls_middleware.py
│   ├── logging/
│   │   ├── logging_setup.py        # Loguru JSON/text, service name
│   │   └── logging_context.py      # log_scope + CorrelationId
│   ├── exceptions/app_exceptions.py
│   ├── models/
│   │   ├── base_models.py          # BaseUUIDModel, BaseTimestampModel
│   │   ├── health_models.py
│   │   ├── parichay_models.py
│   │   └── abhilekh_models.py
│   └── utils/
│       ├── correlation_id.py       # CorrelationIdMiddleware
│       └── api_helpers.py
├── tests/
│   ├── unit/api/test_health.py     # Day-1 health test
│   ├── verify/                     # live E2E scripts (not pytest)
│   └── _helpers/verify_preflight.py
├── postgres_migrations/            # Alembic (when has_postgres=yes)
├── docker/
│   └── docker-compose.yml          # local dev infra (Postgres, Redis, etc.)
├── scripts/
│   ├── setup_dev.sh
│   ├── create_postgres_migration.sh
│   └── run_postgres_migration.sh
├── Makefile
├── Dockerfile
├── pyproject.toml
├── AGENTS.md
├── .harness-pin.yaml
└── .gitmodules                     # rules submodule placeholder
```

### Settled patterns

| Pattern | Implementation |
|---------|---------------|
| **Logging** | `from src.logging import get_logger` · Loguru JSON/text · `log_scope` context manager |
| **Config** | `class FooSettings(BaseSettings): PREFIX = "FOO"` → `FooSettings.get_instance()` |
| **DI** | `injector` modules · `configure_container()` / `initialize_all_services()` / `close_all_services()` |
| **Layers** | import-linter: `api → business_services → repository` (no upward imports) |
| **Auth** | `AuthMiddleware` (JWT Bearer) + `AuthContext` on `request.state.auth` |
| **Errors** | `BaseAppException` → `{status, error, metadata: {correlation_id}}` |
| **Correlation** | `CorrelationIdMiddleware` sets `X-Correlation-ID` on every request |
| **Tests** | `tests/unit/` (pytest, mocked) · `tests/verify/` (live, not in CI) |
| **Quality gate** | `make check` = read-only (black --check + ruff + pyright + lint-imports) |
| **Harness** | `python-services-rules` submodule + `prayog-skills` via `.harness-pin.yaml` |

---

## Development guidelines

Follow the codebase patterns established across parichay, abhilekh, and airforge:

- **Add a business service:** create `src/business_services/<domain>_service.py` extending `BaseBusinessService`; register in `di/modules/business_services_module.py`
- **Add a repository:** create `src/database/postgres/repository/<domain>_repository.py` extending `BasePostgresRepository`; register in `di/modules/repository_module.py`  
- **Add an API route:** create `src/api/v1/<domain>_routes.py`; register in `src/api/v1/__init__.py`
- **Add an infra client:** create `src/infra_services/<name>_client.py` extending `BaseInfraService`; register in `di/modules/infra_module.py`

Every PR should update `docs/specification/as-built/implementation-status.md` together with the code.

---

## Verify the template (fix scaffold first, then launchpad)

**SSOT for foundation code is this repo** — not individual app repos. Suchana (or the next greenfield module) is the **canary** to prove the template works end-to-end.

```text
python-fastapi-foundation   ← fix bugs here (pyproject, auth __init__, logging, …)
         │
         ▼
launchpad scaffold --repo suchana --apply --force   ← overlay into git clone (preserves .git)
         │
         ▼
make setup && make format && make check && make test
launchpad sync-harness --repo suchana --apply
         │
         ▼
green on canary → publish foundation / merge scaffold PR
```

**Do not** patch Suchana-only fixes that belong in the template — they will be lost on the next overlay and will break tarang/setu/etc.

**Recommended canary loop:**

```bash
# 1. Edit python-fastapi-foundation (commit on foundation repo)

# 2. Overlay into existing suchana checkout (develop or chore branch)
cd drivestream-meta
launchpad scaffold --repo suchana --apply --force

# 3. Day-1 gate
cd ../suchana
make setup && make format && make check && make test

# 4. Harness envelope (separate commit on app repo)
cd ../drivestream-meta
launchpad sync-harness --repo suchana --apply
launchpad verify-harness --repo suchana
```

App-specific code (W0 adapters, iac-local, domain routes) stays **only in the app repo** — never in the foundation template.

---

## Harness sync (after repo creation)

```bash
# From drivestream-meta
launchpad sync-harness --repo <service-name> --apply
launchpad verify-harness --repo <service-name>
```

See [playbook/harness-pins.md](https://github.com/drivestream-lab/launchpad/blob/main/playbook/harness-pins.md).

---

## License

MIT
