# python-fastapi-foundation

**Production-ready cookiecutter for Python FastAPI microservices** — aligned with [python-services-rules](https://github.com/drivestream-lab/python-services-rules) and [Launchpad](https://github.com/drivestream-lab/launchpad) harness profiles.

Every generated service starts with settled patterns: layered `src/`, dependency injection, auth middleware, structured logging, optional Postgres/Redis/Kafka integrations, Makefile quality gates, spec-driven test layout, and harness pin placeholders.

| | |
|---|---|
| **License** | [MIT](LICENSE) |
| **Template engine** | [Cookiecutter](https://cookiecutter.readthedocs.io/) |
| **Harness profile** | `python-backend` |
| **Default remote** | `gh:drivestream-lab/python-fastapi-foundation` |
| **Pairs with** | [python-services-rules](https://github.com/drivestream-lab/python-services-rules) · [prayog-skills](https://github.com/drivestream-lab/prayog-skills) |

---

## Role in the stack

```text
python-fastapi-foundation (this repo)     python-services-rules
         │  cookiecutter once                      │  submodule forever
         ▼                                         ▼
    <service-repo>/                          .cursor/rules/*.mdc
         │
         └── launchpad sync-harness-app ──► prayog-skills + .harness-pin.yaml
```

**SSOT for scaffold code is this repository** — not individual app repos. Fix template bugs here; overlay into apps with `launchpad scaffold-app --apply --force`.

---

## Quick start

```bash
pip install cookiecutter

# From GitHub
cookiecutter gh:drivestream-lab/python-fastapi-foundation

# From a local clone
cookiecutter /path/to/python-fastapi-foundation
```

After generation:

```bash
cd <service-name>
cp .env.example .env
make setup          # venv, deps, pre-commit
make check          # should pass on day one
make test           # health unit test included
```

Wire harness (from tenant meta workspace):

```bash
launchpad sync-harness-app --repo <service-name> --apply
launchpad verify-harness-app --repo <service-name>
```

---

## Cookiecutter options

| Option | Choices | Description |
|--------|---------|-------------|
| `service_name` | string | Kebab-case name (e.g. `notifications-api`) |
| `service_description` | string | One-line description |
| `default_port` | number | Uvicorn default port |
| `auth_mode` | `jwt` / `allowlist` / `mtls` / `none` | Inbound auth strategy |
| `has_postgres` | `yes` / `no` | SQLAlchemy async + Alembic |
| `has_redis` | `yes` / `no` | Redis connection manager |
| `has_kafka` | `no` / `yes` | Kafka consumer (aiokafka) |
| `has_s3` | `no` / `yes` | S3 / CloudFront (boto3) |
| `has_cratedb` | `no` / `yes` | CrateDB client |
| `has_emqx` | `no` / `yes` | EMQX REST publish |
| `has_telemetry` | `yes` / `no` | OpenTelemetry → OTLP |
| `has_internal_api` | `no` / `yes` | Network-trusted `/internal` router |
| `parichay_client` | `yes` / `no` | Optional HTTP client stub (rename for your platform) |
| `abhilekh_client` | `no` / `yes` | Optional registry client stub |
| `kavach_client` | `no` / `yes` | Optional policy client stub |

`hooks/post_gen_project.py` removes unselected integration modules automatically.

---

## Generated structure (all options enabled)

```text
<service-name>/
├── src/
│   ├── main.py / app.py           # factory + lifespan
│   ├── api/health/, api/v1/, api/internal/
│   ├── business_services/
│   ├── infra_services/            # postgres, redis, kafka, …
│   ├── database/
│   ├── di/                        # injector modules
│   ├── configs/                   # PREFIX + get_instance() settings
│   ├── common/auth/
│   ├── logging/                   # loguru + correlation
│   └── utils/
├── tests/unit/                    # pytest
├── tests/verify/                  # live scripts (not CI)
├── postgres_migrations/           # when has_postgres=yes
├── docker/docker-compose.yml
├── Makefile                       # check = black + ruff + pyright + import-linter
├── Dockerfile
├── AGENTS.md
├── .harness-pin.yaml
└── .gitmodules                    # → drivestream-lab/python-services-rules
```

---

## Settled patterns

| Concern | Implementation |
|---------|----------------|
| **Logging** | `from src.logging import get_logger` · loguru JSON/text · `log_scope` |
| **Config** | `class FooSettings(BaseSettings): PREFIX = "FOO"` → `get_instance()` |
| **DI** | `injector` · `configure_container()` / `initialize_all_services()` |
| **Layers** | import-linter: `api → business_services → repository` |
| **Auth** | JWT Bearer → `AuthContext` on `request.state.auth` |
| **Errors** | `BaseAppException` → structured JSON + correlation id |
| **Tests** | `tests/unit/` (mocked) · `tests/verify/` (live, manual) |
| **Quality** | `make check` read-only before merge |
| **Harness** | Rules submodule + prayog-skills via pin file |

Details: [python-services-rules](https://github.com/drivestream-lab/python-services-rules).

---

## Extending a generated service

| Task | Where |
|------|--------|
| Business logic | `src/business_services/<domain>_service.py` + DI module |
| Persistence | `src/database/postgres/repository/` + repository module |
| HTTP API | `src/api/v1/<domain>_routes.py` |
| External client | `src/infra_services/<name>_client.py` + infra module |

Update `docs/specification/as-built/implementation-status.md` in the **same PR** as behavior changes.

---

## Launchpad overlay workflow

Use a **canary app repo** to validate template changes before tagging a foundation release:

```bash
# 1. Fix template in python-fastapi-foundation (PR → develop → main)

# 2. Overlay into existing app checkout
cd <tenant-meta>
launchpad scaffold-app --repo <service> --apply --force

# 3. Day-one gate in app repo
cd ../<service>
make setup && make check && make test

# 4. Harness envelope
cd ../<tenant-meta>
launchpad sync-harness-app --repo <service> --apply
launchpad verify-harness-app --repo <service>
```

Do **not** patch scaffold-only fixes in app repos — they are lost on the next overlay.

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `LAUNCHPAD_PYTHON_FOUNDATION` | Override local template path for `launchpad scaffold-app` |

Default: `gh:drivestream-lab/python-fastapi-foundation`

---

## Related repositories

| Repo | Role |
|------|------|
| [python-services-rules](https://github.com/drivestream-lab/python-services-rules) | Coding constitution (`.mdc`) |
| [prayog-skills](https://github.com/drivestream-lab/prayog-skills) | SDD agent skills |
| [launchpad](https://github.com/drivestream-lab/launchpad) | Scaffold, harness sync, playbook |
| [tenant-meta-foundation](https://github.com/drivestream-lab/tenant-meta-foundation) | Tenant meta layout |

Harness pins: [playbook/harness-pins.md](https://github.com/drivestream-lab/launchpad/blob/main/playbook/harness-pins.md)

---

## License

MIT — see [LICENSE](LICENSE).
