import logging
from herbie.models import AbstractBusinessEntity
from herbie.models.message_models_and_serializers import EntityUpdateMessage, EntityDeleteMessage
from herbie.services.message_publisher.utils import MessagePublisherUtils
from herbie.services.utils import BusinessEntityUtils


class MessagePublisher:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._messaging_provider = MessagePublisherUtils.get_messaging_provider()

    def send_entity_update_message(self, entity: AbstractBusinessEntity, tags=None):
        if tags is None:
            tags = []
        self._messaging_provider.send_message(EntityUpdateMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version,
            entity.data,
            entity.created,
            entity.modified,
            tags
        ))

    def send_entity_delete_message(self, entity: AbstractBusinessEntity):
        self._messaging_provider.send_message(EntityDeleteMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version
        ))
