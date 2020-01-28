import logging
from herbie import settings
from herbieapp.models import AbstractBusinessEntity
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher
from herbieapp.services.message_publisher.kafka_publisher import KafkaPublisher
from herbieapp.models.message_models_serializers import EntityUpdateMessage, EntityDeleteMessage
from herbieapp.services.utils import BusinessEntityUtils


class MessagePublisher:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        if settings.MESSAGING_PROVIDER == 'kafka':
            self.messaging_provider = KafkaPublisher()
        self.messaging_provider = GooglePubSubPublisher()

    def send_entity_update_message(self, entity: AbstractBusinessEntity, tags=None):
        if tags is None:
            tags = []
        self.messaging_provider.send_message(EntityUpdateMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version,
            entity.data,
            entity.created,
            entity.modified,
            tags
        ))

    def send_entity_delete_message(self, entity: AbstractBusinessEntity):
        self.messaging_provider.send_message(EntityDeleteMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version
        ))
