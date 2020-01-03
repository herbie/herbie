from django.apps import AppConfig
from herbie import settings


class HerbieappConfig(AppConfig):
    name = settings.APP_LABEL
