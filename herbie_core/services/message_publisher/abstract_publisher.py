from abc import abstractmethod
from herbie_core.models.message_models_and_serializers import Message


class AbstractPublisher:
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def send_message(self, message: Message):
        pass
