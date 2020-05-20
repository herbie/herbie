import logging
from herbieapp.services.dependency_providers import ServiceDependencyProvider
from herbieapp.controllers import SaveBusinessEntityController
from herbieapp.controllers import DeleteBusinessEntityController
from herbieapp.controllers import SchemaRegistryController
from rest_framework.permissions import IsAuthenticated

from dependency_injector import containers, providers


class ControllerDependencyProvider(containers.DeclarativeContainer):
    permission_classes_provider = providers.Singleton(IsAuthenticated)
    logger = providers.Singleton(logging.Logger, name='herbie')

    save_business_entity_controller_provider = providers.Factory(
        SaveBusinessEntityController,
        _entity_manager=ServiceDependencyProvider.entity_manager_provider(),
        _validator=ServiceDependencyProvider.validator_provider(),
        _schema_registry=ServiceDependencyProvider.schema_registry_provider(),
        _permission_classes=permission_classes_provider(),
        _permission_manager=ServiceDependencyProvider.permission_manager_provider()
    )

    delete_business_entity_controller_provider = providers.Factory(
        DeleteBusinessEntityController,
        _entity_manager=ServiceDependencyProvider.entity_manager_provider(),
        _validator=ServiceDependencyProvider.validator_provider(),
        _permission_classes=permission_classes_provider(),
        _permission_manager=ServiceDependencyProvider.permission_manager_provider()
    )

    schema_registry_controller_provider = providers.Singleton(
        SchemaRegistryController, _schema_registry=ServiceDependencyProvider.schema_registry_provider()
    )
