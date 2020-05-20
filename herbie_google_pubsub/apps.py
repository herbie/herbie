from django.apps import AppConfig
from herbie.services.message_publisher.registry import Registry
from herbie_google_pubsub.publisher import GooglePubsubPublisher


class HerbieGooglePubsubConfig(AppConfig):
    name = 'herbie_google_pubsub'
    verbose_name = 'HerbieGooglePubsub'

    def ready(self):
        Registry.add_publisher(GooglePubsubPublisher())
