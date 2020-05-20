import inject
from herbieapp.services.dependency_providers import ServiceDependencyProvider
from herbieapp.services import BusinessEntityManager
from herbieapp.services import SchemaRegistry
from herbieapp.services import JsonSchemaValidator
from herbieapp.services import SchemaPackage
from herbieapp.services.permission_manager import PermissionManager
from herbieapp.services.message_publisher.utils import MessagePublisherUtils


class ServiceInjectConfig:

    def inject_config(binder):
        binder.bind(MessagePublisherUtils.get_messaging_provider(),
                    ServiceDependencyProvider.messaging_provider())
        binder.bind(BusinessEntityManager,
                    BusinessEntityManager(ServiceDependencyProvider.message_publisher_provider()))
        binder.bind(SchemaRegistry, ServiceDependencyProvider.schema_registry_provider())
        binder.bind(PermissionManager, ServiceDependencyProvider.permission_manager_provider())
        binder.bind(SchemaPackage, ServiceDependencyProvider.schema_package_provider())
        binder.bind(JsonSchemaValidator, ServiceDependencyProvider.validator_provider())
