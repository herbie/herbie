from django.apps import AppConfig


class HerbieCoreConfig(AppConfig):
    name = "herbie_core"
    verbose_name = "HerbieCore"

    def ready(self):
        from herbie_core.services.message_publisher.message_publisher import Registry
        from herbie_core.services.message_publisher.logging_publisher import LoggingPublisher

        Registry.add_publisher(LoggingPublisher())
