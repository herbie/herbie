import json
import logging

from kafka import KafkaProducer
from django.core.serializers.json import DjangoJSONEncoder

from wayne import settings
from wayneapp.models import AbstractBusinessEntity


class EntityUpdateMessage:
    def __init__(self, _type, key, version, payload, created, modified):
        self.action = 'update'
        self.type = _type
        self.key = key
        self.version = version
        self.payload = payload
        self.created = created
        self.modified = modified


class EntityDeleteMessage:
    def __init__(self, _type, key, version):
        self.action = 'delete'
        self.type = _type
        self.key = key
        self.version = version


class MessageService:

    _producer = KafkaProducer(bootstrap_servers=settings.KAFKA.get('SERVERS'),
                              request_timeout_ms=settings.KAFKA.get('TIMEOUT'),
                              key_serializer=str.encode,
                              value_serializer=lambda v: json.dumps(v.__dict__, cls=DjangoJSONEncoder).encode('utf-8'))
    _logger = logging.getLogger(__name__)

    def send_entity_update_message(self, entity: AbstractBusinessEntity):
        self._send_message(EntityUpdateMessage(
            type(entity).__name__,
            entity.key,
            entity.version,
            entity.data,
            entity.created,
            entity.modified
        ))

    def send_entity_delete_message(self, entity_name: str, key: str, version: str):
        self._send_message(EntityDeleteMessage(
            entity_name,
            key,
            version
        ))

    def _send_message(self, message):
        self._producer.send(message.type, value=message, key=message.key)\
            .add_callback(self._on_send_success)\
            .add_errback(self._on_send_error)

    def _on_send_success(self, record_metadata):
        self._logger.debug('Message delivered to {} [{}]'.format(record_metadata.topic, record_metadata.partition))

    def _on_send_error(self, excp):
        self._logger.error('Message delivery failed: {}'.format(excp), exc_info=excp)
