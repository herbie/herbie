import logging
from herbieapp.services.dependency_containers import ServiceDependencyContainer
from herbieapp.controllers import SaveBusinessEntityController
from herbieapp.controllers import SchemaRegistryController
from dependency_injector import containers, providers


class ControllerDependencyContainer(containers.DeclarativeContainer):
    logger = logging.getLogger(__name__)

    save_business_entity_controller = providers.Factory(
        SaveBusinessEntityController,
        _entity_manager=ServiceDependencyContainer.entity_manager(),
        _logger=logger,
        _validator=ServiceDependencyContainer.validator(),
        _schema_registry=ServiceDependencyContainer.schema_registry(),
        _permission_manager=ServiceDependencyContainer.permission_manager()
    )

    schema_registry_controller = providers.Singleton(
        SchemaRegistryController, _schema_registry=ServiceDependencyContainer.schema_registry()
    )

    # TODO move to providers ?
    save_business_entity_controller_as_view = save_business_entity_controller().as_view(
        _entity_manager=ServiceDependencyContainer.entity_manager(),
        _logger=logger,
        _validator=ServiceDependencyContainer.validator(),
        _schema_registry=ServiceDependencyContainer.schema_registry(),
        _permission_manager=ServiceDependencyContainer.permission_manager()
    )

    schema_registry_controller_as_view = schema_registry_controller().as_view(
        _schema_registry=ServiceDependencyContainer.schema_registry()
    )