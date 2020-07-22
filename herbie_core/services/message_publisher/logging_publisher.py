import logging

from herbie_core.models.message_models_and_serializers import Message
from herbie_core.services.message_publisher.abstract_publisher import AbstractPublisher


class LoggingPublisher(AbstractPublisher):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_name(self) -> str:
        return "logging"

    def send_message(self, message: Message):
        self._logger.info(message)
