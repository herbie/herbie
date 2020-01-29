from herbie import settings
from herbieapp.exceptions import InvalidMessagingProvider
from herbieapp.services import KafkaPublisher, GooglePubSubPublisher


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'kafka':
            return KafkaPublisher()
        elif settings.MESSAGING_PROVIDER == 'google_pub_sub':
            return GooglePubSubPublisher()

        raise InvalidMessagingProvider('invalid messaging provider')
