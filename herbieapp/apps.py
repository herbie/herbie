from django.apps import AppConfig
from herbie import settings


class HerbieappConfig(AppConfig):
    name = settings.APP_LABEL

    def ready(self):
        from herbieapp.inject_config import InjectConfig
        inject_initiate = InjectConfig()
