from django.apps import AppConfig
from django.conf import settings
from herbie import default_settings

settings.configure(default_settings=default_settings)


class HerbieConfig(AppConfig):
    name = 'herbie'
    verbose_name = 'Herbie'

