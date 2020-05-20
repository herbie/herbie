from django.apps import AppConfig


class HerbieConfig(AppConfig):
    name = 'herbie'
    verbose_name = 'Herbie'

    def ready(self):
        from herbie.services.message_publisher import Registry
        from herbie.services.message_publisher.logging_publisher import LoggingPublisher

        Registry.add_publisher(LoggingPublisher())
