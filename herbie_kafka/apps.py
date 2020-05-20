from django.apps import AppConfig
from herbie_core.services.message_publisher.registry import Registry
from herbie_kafka.publisher import KafkaPublisher


class HerbieKafkaConfig(AppConfig):
    name = 'herbie_kafka'
    verbose_name = 'HerbieKafka'

    def ready(self):
        Registry.add_publisher(KafkaPublisher())
