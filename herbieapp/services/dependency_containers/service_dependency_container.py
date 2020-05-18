from herbieapp.services import BusinessEntityManager, SchemaRegistry, JsonSchemaValidator
from herbieapp.services.permission_manager import PermissionManager
from herbieapp.services.message_publisher.message_publisher import MessagePublisher
from dependency_injector import containers, providers
from herbieapp.services.message_publisher.utils import MessagePublisherUtils


class ServiceDependencyContainer(containers.DeclarativeContainer):

    publisher_provider = providers.Factory(MessagePublisherUtils.get_messaging_provider_publisher_client())
    messaging_provider = providers.Factory(MessagePublisherUtils.get_messaging_provider(), _publisher=publisher_provider)
    message_publisher_provider = providers.Factory(MessagePublisher, _messaging_provider=messaging_provider)
    entity_manager_provider = providers.Factory(BusinessEntityManager, _message_publisher=message_publisher_provider())
    schema_registry_provider = providers.Factory(SchemaRegistry)
    validator_provider = providers.Factory(JsonSchemaValidator, _schema_registry=schema_registry_provider())
    permission_manager_provider = providers.Factory(PermissionManager)