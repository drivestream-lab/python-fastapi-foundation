"""Alembic env.py for {{cookiecutter.service_name}}."""

import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

import dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"), override=True)

from src.configs.postgres_settings import PostgresSettings
settings = PostgresSettings.get_instance()
config.set_main_option("sqlalchemy.url", settings.alembic_database_uri)

target_metadata = None  # replace with your Base.metadata after W0


def run_migrations_offline() -> None:
    context.configure(url=config.get_main_option("sqlalchemy.url"),
                      target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section),
                                     prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
