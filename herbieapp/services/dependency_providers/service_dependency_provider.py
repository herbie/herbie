from herbieapp.services import BusinessEntityManager, SchemaRegistry, JsonSchemaValidator, SchemaPackage
from herbieapp.services import SchemaImporter
from herbieapp.services.permission_manager import PermissionManager
from herbieapp.services.message_publisher.message_publisher import MessagePublisher
from herbieapp.services.message_publisher.utils import MessagePublisherUtils


class ServiceDependencyProvider:
    publisher_provider = MessagePublisherUtils.get_messaging_provider_publisher_client()()
    messaging_provider = MessagePublisherUtils.get_messaging_provider()(publisher=publisher_provider)
    message_publisher_provider = MessagePublisher(messaging_provider=messaging_provider)
    entity_manager_provider = BusinessEntityManager(message_publisher=message_publisher_provider)
    schema_registry_provider = SchemaRegistry()
    schema_package_provider = SchemaPackage()
    schema_importer_provider = SchemaImporter(schema_package=schema_package_provider)
    validator_provider = JsonSchemaValidator(schema_registry=schema_registry_provider)
    permission_manager_provider = PermissionManager()
