import logging

from django.core.management import BaseCommand

from herbieapp.services import SchemaPackage, GooglePubSubPublisher


class Command(BaseCommand):
    help = 'initialize pubsub topics'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._publisher = GooglePubSubPublisher()
        self._schema_package = SchemaPackage()

    def handle(self, *args, **kwargs):
        names = self._schema_package.get_all_schema_names()
        print(names)
        for name in names:
            self._publisher.create_topic(name)
            self._publisher.create_subscription(name, 'subscription_'+name)

