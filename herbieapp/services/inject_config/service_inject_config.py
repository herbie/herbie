from herbieapp.services.dependency_providers import ServiceDependencyProvider
import inject
from herbieapp.services import BusinessEntityManager
from herbieapp.services import SchemaRegistry
from herbieapp.services import JsonSchemaValidator
from herbieapp.services import SchemaPackage
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher
from herbieapp.services.permission_manager import PermissionManager


class ServiceInjectConfig:

    def inject_config(binder):
        binder.bind(BusinessEntityManager,
                    BusinessEntityManager(ServiceDependencyProvider.message_publisher_provider()))
        binder.bind(SchemaRegistry, ServiceDependencyProvider.schema_registry_provider())
        binder.bind(PermissionManager, ServiceDependencyProvider.permission_manager_provider())
        binder.bind(SchemaPackage, ServiceDependencyProvider.schema_package_provider())
        binder.bind(JsonSchemaValidator, ServiceDependencyProvider.validator_provider())
        binder.bind(GooglePubSubPublisher, ServiceDependencyProvider.pubsub_publisher_provider())

