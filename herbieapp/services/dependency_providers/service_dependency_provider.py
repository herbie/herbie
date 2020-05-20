from herbieapp.services import BusinessEntityManager, SchemaRegistry, JsonSchemaValidator, SchemaPackage
from herbieapp.services.permission_manager import PermissionManager
from herbieapp.services.message_publisher.message_publisher import MessagePublisher
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher
from dependency_injector import providers
from herbieapp.services.message_publisher.utils import MessagePublisherUtils


class ServiceDependencyProvider:
    publisher_provider = providers.Factory(MessagePublisherUtils.get_messaging_provider_publisher_client())
    messaging_provider = providers.Factory(MessagePublisherUtils.get_messaging_provider(),
                                           publisher=publisher_provider)
    message_publisher_provider = providers.Factory(MessagePublisher, messaging_provider=messaging_provider)
    entity_manager_provider = providers.Factory(BusinessEntityManager, message_publisher=message_publisher_provider())
    schema_registry_provider = providers.Factory(SchemaRegistry)
    schema_package_provider = providers.Factory(SchemaPackage)
    validator_provider = providers.Factory(JsonSchemaValidator, schema_registry=schema_registry_provider())
    permission_manager_provider = providers.Factory(PermissionManager)
    pubsub_publisher_provider = providers.Factory(GooglePubSubPublisher, _publisher=publisher_provider())
