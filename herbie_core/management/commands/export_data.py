import logging

from django.conf import settings
from django.core.management import BaseCommand
from herbie_core.constants import CommandsConstants as Constants
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.message_publisher.message_publisher import MessagePublisher


class Command(BaseCommand):

    help = "publish all data from a business entity to the business entity channel/topic"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._chunk_size = settings.DEFAULT_CHUNK_SIZE
        self._message_service = MessagePublisher()

    def add_arguments(self, parser):
        parser.add_argument(Constants.BUSINESS_ENTITY, type=str)
        parser.add_argument(Constants.CHUNK_SIZE, type=int, nargs="?", default=settings.DEFAULT_CHUNK_SIZE)

    def handle(self, *args, **kwargs):
        self._chunk_size = kwargs[Constants.CHUNK_SIZE]
        business_entity = kwargs[Constants.BUSINESS_ENTITY]
        queryset = self._entity_manager.find_all(business_entity)
        tags = [Constants.FULL_EXPORT]

        for business_entity in queryset.iterator(chunk_size=self._chunk_size):
            self._message_service.send_entity_update_message(business_entity, tags)

        self._message_service.shutdown()
