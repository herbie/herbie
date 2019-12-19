from django.apps import AppConfig
from wayne import settings


class WayneappConfig(AppConfig):
    name = settings.APP_LABEL

