from django.core.management import BaseCommand

from wayneapp.initializers.abstract_initializer import AbstractInitializer
from wayneapp.initializers.permisson_initializer import PermissionInitializer
from wayneapp.initializers.schema_initializer import SchemaInitializer
from wayneapp.services import logging


class Command(BaseCommand):
    help = 'initialize database'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._initializers = (
            PermissionInitializer(),
            SchemaInitializer()
        )

    def handle(self, *args, **kwargs):
        for initializer in self._initializers:
            if not isinstance(initializer, AbstractInitializer):
                raise TypeError

            self._logger.info('Start initializing ' + initializer.get_name())
            initializer.init()
            self._logger.info('Initialization done.')