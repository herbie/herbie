from django.conf import settings
from django.test import TestCase

from unittest.mock import Mock

from herbie_core.models.message_models_and_serializers import EntityUpdateMessage, EntityDeleteMessage
from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.message_publisher.message_publisher import MessagePublisher
from tests.services.matcher import Matcher


class MessageTestEntity(AbstractBusinessEntity):
    class Meta:
        managed = False
        app_label = "herbie_core"


key = "123"
version = "v1"
data = '{"field": "value"}'
topic = "message_test_entity"
entity = MessageTestEntity(key=key, version=version, data=data)


class MessagePublisherTestCase(TestCase):
    def setUp(self):
        settings.MESSAGING_PROVIDER = "kafka"
        self._message_publisher = MessagePublisher()

    def test_send_entity_update_message(self):
        mock_producer = Mock(name="send_message")

        self._message_publisher._publisher_list = {"logging": mock_producer}
        self._message_publisher.send_entity_update_message(entity)

        mock_producer.send_message.assert_called_once_with(
            Matcher(
                EntityUpdateMessage,
                {"action": "update", "type": topic, "key": key, "version": version, "payload": data, "tags": []},
            )
        )

    def test_send_entity_delete_message(self):
        mock_producer = Mock(name="send_message")

        self._message_publisher._publisher_list = {"logging": mock_producer}
        self._message_publisher.send_entity_delete_message(entity)

        mock_producer.send_message.assert_called_once_with(
            Matcher(EntityDeleteMessage, {"action": "delete", "type": topic, "key": key, "version": version})
        )
