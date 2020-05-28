from herbieapp.services.dependency_providers import ServiceDependencyProvider
from herbieapp.initializers.permisson_initializer import PermissionInitializer
from herbieapp.initializers.schema_initializer import SchemaInitializer


class InitializerDependencyProvider:
    permission_initializer = PermissionInitializer(
        permission_manager=ServiceDependencyProvider.permission_manager_provider
    )
    schema_initializer = SchemaInitializer(
        schema_importer=ServiceDependencyProvider.schema_importer_provider
    )

