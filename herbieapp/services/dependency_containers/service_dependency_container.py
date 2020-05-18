from herbieapp.services import BusinessEntityManager, SchemaRegistry, JsonSchemaValidator
from herbieapp.services.permission_manager import PermissionManager
from dependency_injector import containers, providers


class ServiceDependencyContainer(containers.DeclarativeContainer):
    entity_manager = providers.Factory(BusinessEntityManager)
    validator = providers.Factory(JsonSchemaValidator)
    schema_registry = providers.Factory(SchemaRegistry)
    permission_manager = providers.Factory(PermissionManager)