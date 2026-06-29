"""Infra DI module for {{cookiecutter.service_name}} — register infra services here."""

from injector import Module, Binder


class InfraModule(Module):
    def configure(self, binder: Binder) -> None:
        # Example (uncomment and add imports as you implement each W0 service):
        # from src.infra_services.postgres_service import PostgresService
        # binder.bind(PostgresService, scope=singleton)
        pass
