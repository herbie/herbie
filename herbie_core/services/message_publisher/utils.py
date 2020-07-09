from django.conf import settings
from herbie_core.exceptions import InvalidMessagingProvider
from herbie_google_pubsub.publisher.google_pubsub_publisher import GooglePubsubPublisher


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'google_pubsub':
            return GooglePubsubPublisher()

        raise InvalidMessagingProvider('invalid messaging provider')
