from django.apps import AppConfig


class HerbieGooglePubsubConfig(AppConfig):
    name = 'herbie_google_pubsub'
    verbose_name = 'HerbieGooglePubsub'

    def ready(self):
        from herbie_core.services.message_publisher.registry import Registry
        from herbie_google_pubsub.publisher import GooglePubsubPublisher

        Registry.add_publisher(GooglePubsubPublisher())
