from herbie import settings
from herbieapp.exceptions import InvalidMessagingProvider
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher
from herbieapp.services.message_publisher.kafka_publisher import KafkaPublisher
from google.cloud.pubsub_v1 import PublisherClient


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'kafka':
            return KafkaPublisher
        elif settings.MESSAGING_PROVIDER == 'google_pub_sub':
            return GooglePubSubPublisher

        raise InvalidMessagingProvider('invalid messaging provider')

    @staticmethod
    def get_messaging_provider_publisher_client():
        if settings.MESSAGING_PROVIDER == 'kafka':
            return None
        elif settings.MESSAGING_PROVIDER == 'google_pub_sub':
            return PublisherClient

        raise InvalidMessagingProvider('invalid messaging provider')