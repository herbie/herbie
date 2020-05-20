from django.apps import AppConfig
from herbie.services.message_publisher import Registry
from herbie.services.message_publisher.logging_publisher import LoggingPublisher


class HerbieConfig(AppConfig):
    name = 'herbie'
    verbose_name = 'Herbie'

    def ready(self):
        Registry.add_publisher(LoggingPublisher())
