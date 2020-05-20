from django.conf import settings
from herbie.exceptions import InvalidMessagingProvider
from herbie_google_pubsub.publisher.google_pub_sub_publisher import GooglePubSubPublisher
from herbie.services.message_publisher.kafka_publisher import KafkaPublisher


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'kafka':
            return KafkaPublisher()
        elif settings.MESSAGING_PROVIDER == 'google_pub_sub':
            return GooglePubSubPublisher()

        raise InvalidMessagingProvider('invalid messaging provider')
