from herbieapp.services.dependency_containers import ServiceDependencyContainer
from herbieapp.controllers.dependency_containers import ControllerDependencyContainer


class ControllerDependencyContainerView(ControllerDependencyContainer):
    save_business_entity_controller_as_view = \
        ControllerDependencyContainer.save_business_entity_controller_provider().as_view(
            _entity_manager=ServiceDependencyContainer.entity_manager_provider(),
            _validator=ServiceDependencyContainer.validator_provider(),
            _schema_registry=ServiceDependencyContainer.schema_registry_provider(),
            _permission_classes=ControllerDependencyContainer.permission_classes_provider,
            _permission_manager=ServiceDependencyContainer.permission_manager_provider()
        )

    delete_business_entity_controller_as_view = \
        ControllerDependencyContainer.delete_business_entity_controller_provider().as_view(
            _entity_manager=ServiceDependencyContainer.entity_manager_provider(),
            _validator=ServiceDependencyContainer.validator_provider(),
            _permission_classes=ControllerDependencyContainer.permission_classes_provider,
            _permission_manager=ServiceDependencyContainer.permission_manager_provider()
        )

    schema_registry_controller_as_view = \
        ControllerDependencyContainer.schema_registry_controller_provider().as_view(
            _schema_registry=ServiceDependencyContainer.schema_registry_provider()
        )
