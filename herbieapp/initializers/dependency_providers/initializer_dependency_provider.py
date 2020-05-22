from herbieapp.services.dependency_providers import ServiceDependencyProvider
from herbieapp.initializers.permisson_initializer import PermissionInitializer
from herbieapp.initializers.schema_initializer import SchemaInitializer
#from dependency_injector import containers, providers


class InitializerDependencyProvider: #(containers.DeclarativeContainer):
    permission_initializer = PermissionInitializer(
        permission_manager=ServiceDependencyProvider.permission_manager_provider
    )
    schema_initializer = SchemaInitializer(
        schema_importer=ServiceDependencyProvider.schema_importer_provider
    )

    # Using library dependency-injector
    # permission_initializer = providers.Factory(
    #     PermissionInitializer,
    #     permission_manager=ServiceDependencyProvider.permission_manager_provider()
    # )
    # schema_initializer = providers.Factory(
    #     SchemaInitializer,
    #     schema_importer=ServiceDependencyProvider.schema_importer_provider()
    # )

