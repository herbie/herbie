from herbieapp.services import SchemaRegistry
from herbieapp.controllers import SchemaRegistryController
from dependency_injector import containers, providers


class SchemaRegistryDependencyContainer(containers.DeclarativeContainer):
    schema_registry = providers.Singleton(SchemaRegistry)
    schema_registry_controller = providers.Singleton(SchemaRegistryController, _schema_registry=schema_registry())
