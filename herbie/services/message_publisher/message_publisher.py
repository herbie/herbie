import logging
from herbie.models import AbstractBusinessEntity
from herbie.models.message_models_and_serializers import EntityUpdateMessage
from herbie.models.message_models_and_serializers import EntityDeleteMessage
from herbie.models.message_models_and_serializers import Message
from herbie.services.message_publisher.registry import Registry
from herbie.services.utils import BusinessEntityUtils


class MessagePublisher:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._publisher_list = Registry.get_publisher_list()

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
            tags
        )

        self._send_message(update_message)

    def send_entity_delete_message(self, entity: AbstractBusinessEntity):
        delete_message = EntityDeleteMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version
        )

        self._send_message(delete_message)

    def _send_message(self, message: Message):
        for publisher in self._publisher_list:
            publisher.send_message(message)
