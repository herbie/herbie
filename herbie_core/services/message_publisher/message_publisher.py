from herbie_core.models.message_models_and_serializers import EntityUpdateMessage, EntityCreateMessage
from herbie_core.models.message_models_and_serializers import EntityDeleteMessage
from herbie_core.models.message_models_and_serializers import Message
from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.message_publisher.registry import Registry
from herbie_core.services.utils import BusinessEntityUtils


class MessagePublisher:
    def __init__(self):
        self._publisher_list = Registry.get_publisher_list()

    def send_entity_create_message(self, entity: AbstractBusinessEntity, tags=None):
        if tags is None:
            tags = []
        self._send_message(
            EntityCreateMessage(
                BusinessEntityUtils.get_entity_type_name(entity),
                entity.key,
                entity.version,
                entity.data,
                entity.created,
                tags,
            )
        )

    def send_entity_update_message(self, entity: AbstractBusinessEntity, tags=None):
        if tags is None:
            tags = []

        update_message = EntityUpdateMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version,
            entity.data,
            entity.created,
            entity.modified,
            tags,
        )

        self._send_message(update_message)

    def send_entity_delete_message(self, entity: AbstractBusinessEntity):
        delete_message = EntityDeleteMessage(
            BusinessEntityUtils.get_entity_type_name(entity), entity.key, entity.version
        )

        self._send_message(delete_message)

    def _send_message(self, message: Message):
        for publisher in self._publisher_list.values():
            publisher.send_message(message)
