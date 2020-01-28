import unittest.mock as mock

from django.test import TestCase

from herbieapp.models import AbstractBusinessEntity
from herbieapp.services import MessagePublisher, EntityUpdateMessage, EntityDeleteMessage, KafkaPublisher
from herbieapp.tests.services.matcher import Matcher


class MessageTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


key = '123'
version = 'v1'
data = '{"field": "value"}'
topic = 'message_test_entity'
entity = MessageTestEntity(key=key, version=version, data=data)


class MessagePublisherTestCase(TestCase):

    def setUp(self):
        self._message_publisher = MessagePublisher()

    @mock.patch.object(KafkaPublisher, '_producer')
    def test_send_entity_update_message(self, mock_producer):
        self._message_publisher.send_entity_update_message(entity)

        mock_producer.send.assert_called_once_with(topic, key=key, value=Matcher(
            EntityUpdateMessage, {'action': 'update', 'type': topic, 'key': key, 'version': version, 'payload': data, 'tags': []}
        ))

    @mock.patch.object(KafkaPublisher, '_producer')
    def test_send_entity_delete_message(self, mock_producer):
        self._message_publisher.send_entity_delete_message(entity)

        mock_producer.send.assert_called_once_with(topic, key=key, value=Matcher(
            EntityDeleteMessage, {'action': 'delete', 'type': topic, 'key': key, 'version': version}
        ))
