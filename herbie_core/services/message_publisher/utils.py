from django.conf import settings
from herbie_core.exceptions import InvalidMessagingProvider
from google_pubsub_adapter.publisher.google_pubsub_publisher import GooglePubsubPublisher


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'google_pubsub':
            return GooglePubsubPublisher()

        raise InvalidMessagingProvider('invalid messaging provider')
