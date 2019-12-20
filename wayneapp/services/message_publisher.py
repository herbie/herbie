import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import cached_property
from kafka import KafkaProducer
from wayne import settings
from wayneapp.models import AbstractBusinessEntity
from wayneapp.services.utils import BusinessEntityUtils


class EntityUpdateMessage:
    def __init__(self, _type, key, version, payload, created, modified, tags):
        self.tags = tags
        self.action = 'update'
        self.type = _type
        self.key = key
        self.version = version
        self.payload = payload
        self.created = created
        self.modified = modified


class EntityDeleteMessage:
    def __init__(self, _type, key, version=None):
        self.action = 'delete'
        self.type = _type
        self.key = key
        self.version = version


class MessagePublisher:

    _logger = logging.getLogger(__name__)

    def send_entity_update_message(self, entity: AbstractBusinessEntity, tags=None):
        if tags is None:
            tags = []
        self._send_message(EntityUpdateMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version,
            entity.data,
            entity.created,
            entity.modified,
            tags
        ))

    def send_entity_delete_message(self, entity: AbstractBusinessEntity):
        self._send_message(EntityDeleteMessage(
            BusinessEntityUtils.get_entity_type_name(entity),
            entity.key,
            entity.version
        ))

    def _send_message(self, message):
        self._producer.send(message.type, value=message, key=message.key)\
            .add_callback(self._on_send_success)\
            .add_errback(self._on_send_error)

    @cached_property
    def _producer(self) -> KafkaProducer:
        self._logger.info('initializing kafka address: {} timeout: {} '
                          .format(settings.KAFKA.get('SERVERS'), settings.KAFKA.get('TIMEOUT')))
        # lazy init of the kafka producer, because kafka may not be available yet when starting the app with docker
        return KafkaProducer(bootstrap_servers=settings.KAFKA.get('SERVERS'),
                             request_timeout_ms=settings.KAFKA.get('TIMEOUT'),
                             key_serializer=str.encode,
                             value_serializer=lambda v: json.dumps(v.__dict__, cls=DjangoJSONEncoder).encode('utf-8'))

    def _on_send_success(self, record_metadata):
        self._logger.debug('Message delivered to {} [{}]'.format(record_metadata.topic, record_metadata.partition))

    def _on_send_error(self, excp):
        self._logger.error('Message delivery failed: {}'.format(excp), exc_info=excp)

    def shutdown(self):
        self._logger.info('flushing kafka producer')
        self._producer.flush()
