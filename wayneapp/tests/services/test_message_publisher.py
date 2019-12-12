import unittest.mock as mock

from callee import Attrs
from django.test import TestCase

from wayneapp.models import AbstractBusinessEntity
from wayneapp.services import MessagePublisher


class TestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False


class MessagePublisherTestCase(TestCase):

    def setUp(self):
        self._message_publisher = MessagePublisher()

    @mock.patch.object(MessagePublisher, '_producer')
    def test_send_entity_update_message(self, mock_producer):
        key = '123'
        version = 'v1'
        data = '{"field": "value"}'
        topic = 'test_entity'

        self._message_publisher.send_entity_update_message(TestEntity(key=key, version=version, data=data))

        mock_producer.send.assert_called_once_with(topic, key=key, value=Attrs(
            action='update', type=topic, key=key, version=version, payload=data
        ))

    @mock.patch.object(MessagePublisher, '_producer')
    def test_send_entity_delete_message(self, mock_producer):
        key = '123'
        version = 'v1'
        data = '{"field": "value"}'
        topic = 'test_entity'

        self._message_publisher.send_entity_delete_message(TestEntity(key=key, version=version, data=data))

        mock_producer.send.assert_called_once_with(topic, key=key, value=Attrs(
            action='delete', type=topic, key=key, version=version
        ))
