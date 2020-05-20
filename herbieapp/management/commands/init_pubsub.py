import logging
import inject
from django.core.management import BaseCommand
from herbieapp.services import SchemaPackage
from herbieapp.services.message_publisher.google_pub_sub_publisher import GooglePubSubPublisher


class Command(BaseCommand):
    help = 'initialize pubsub topics'

    @inject.autoparams()
    def __init__(
            self,
            publisher: GooglePubSubPublisher,
            schema_package: SchemaPackage,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._publisher = publisher
        self._schema_package = schema_package

    def handle(self, *args, **kwargs):
        names = self._schema_package.get_all_schema_names()
        print(names)
        for name in names:
            self._publisher.create_topic(name)

