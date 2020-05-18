from herbie import settings
from herbieapp.exceptions import InvalidMessagingProvider
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher
from herbieapp.services.message_publisher.kafka_publisher import KafkaPublisher


class MessagePublisherUtils:

    @staticmethod
    def get_messaging_provider():
        if settings.MESSAGING_PROVIDER == 'kafka':
            return KafkaPublisher()
        elif settings.MESSAGING_PROVIDER == 'google_pub_sub':
            return GooglePubSubPublisher()

        raise InvalidMessagingProvider('invalid messaging provider')
