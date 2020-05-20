import logging

from herbie.services import AbstractPublisher
from herbie.models.message_models_and_serializers import Message


class LoggingPublisher(AbstractPublisher):

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_name(self) -> str:
        return 'logging'

    def send_message(self, message: Message):
        self._logger.info(message)
