import logging

from django.core.management import BaseCommand

from herbie_core.services import SchemaPackage
from google_pubsub_adapter.publisher.google_pubsub_publisher import GooglePubsubPublisher


class Command(BaseCommand):
    help = 'initialize pubsub topics'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._publisher = GooglePubsubPublisher()
        self._schema_package = SchemaPackage()

    def handle(self, *args, **kwargs):
        names = self._schema_package.get_all_schema_names()
        print(names)
        for name in names:
            self._publisher.create_topic(name)

