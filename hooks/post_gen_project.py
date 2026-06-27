#!/usr/bin/env python3
"""Post-generation hook: remove files that don't apply to chosen parameters."""

import os
import shutil

# ── cookiecutter variables (rendered at generation time) ─────────────────────
SERVICE_NAME   = "{{cookiecutter.service_name}}"
AUTH_MODE      = "{{cookiecutter.auth_mode}}"
HAS_POSTGRES   = "{{cookiecutter.has_postgres}}" == "yes"
HAS_REDIS      = "{{cookiecutter.has_redis}}" == "yes"
HAS_KAFKA      = "{{cookiecutter.has_kafka}}" == "yes"
HAS_S3         = "{{cookiecutter.has_s3}}" == "yes"
HAS_CRATEDB    = "{{cookiecutter.has_cratedb}}" == "yes"
HAS_EMQX       = "{{cookiecutter.has_emqx}}" == "yes"
HAS_TELEMETRY  = "{{cookiecutter.has_telemetry}}" == "yes"
HAS_INTERNAL   = "{{cookiecutter.has_internal_api}}" == "yes"
PARICHAY       = "{{cookiecutter.parichay_client}}" == "yes"
ABHILEKH       = "{{cookiecutter.abhilekh_client}}" == "yes"
KAVACH         = "{{cookiecutter.kavach_client}}" == "yes"


def rm(path: str) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


# ── conditional configs ───────────────────────────────────────────────────────
if AUTH_MODE != "jwt":
    rm("src/configs/jwt_settings.py")
    rm("src/common/auth")

if AUTH_MODE != "allowlist":
    rm("src/middleware/allowlist_middleware.py")

if AUTH_MODE != "mtls":
    rm("src/middleware/mtls_middleware.py")

if AUTH_MODE not in ("allowlist", "mtls"):
    if not os.listdir("src/middleware"):
        rm("src/middleware")

if not HAS_POSTGRES:
    rm("src/configs/postgres_settings.py")
    rm("src/infra_services/postgres_service.py")
    rm("src/database/postgres")
    rm("postgres_migrations")

if not HAS_REDIS:
    rm("src/configs/redis_settings.py")
    rm("src/infra_services/redis_service.py")
    rm("src/database/redis")

if not HAS_KAFKA:
    rm("src/configs/kafka_settings.py")
    rm("src/infra_services/kafka_consumer_service.py")

if not HAS_S3:
    rm("src/configs/s3_settings.py")
    rm("src/infra_services/s3_service.py")

if not HAS_CRATEDB:
    rm("src/configs/cratedb_settings.py")
    rm("src/infra_services/cratedb_service.py")

if not HAS_EMQX:
    rm("src/configs/emqx_settings.py")
    rm("src/infra_services/emqx_publish_service.py")

if not HAS_TELEMETRY:
    rm("src/configs/telemetry_settings.py")
    rm("src/infra_services/telemetry_service.py")
    rm("src/models/telemetry_types.py")

if not HAS_INTERNAL:
    rm("src/api/internal")

if not PARICHAY:
    rm("src/configs/parichay_settings.py")
    rm("src/infra_services/parichay_client.py")
    rm("src/models/parichay_models.py")

if not ABHILEKH:
    rm("src/configs/abhilekh_settings.py")
    rm("src/infra_services/abhilekh_client.py")
    rm("src/models/abhilekh_models.py")

if not KAVACH:
    rm("src/configs/kavach_settings.py")
    rm("src/infra_services/kavach_client.py")

# ── report ────────────────────────────────────────────────────────────────────
print(f"""
✓ {SERVICE_NAME} scaffold generated successfully.

Next steps:
  cd {SERVICE_NAME}
  cp .env.example .env          # fill in your local values
  make setup                    # creates .venv, installs deps
  make check                    # should be green immediately
  make test                     # health test passes on day 1
  make run                      # service starts on port {{cookiecutter.default_port}}

Then add your W0 service-specific interfaces on top of this scaffold.
""")
