import re
import importlib
from django.conf import settings
from herbie_core.models.models import AbstractBusinessEntity


class BusinessEntityUtils:
    @staticmethod
    def snake_to_camel(word: str) -> str:
        return "".join(x.capitalize() or "" for x in word.split("_"))

    @staticmethod
    def camel_to_snake(word: str) -> str:
        # explanation: https://stackoverflow.com/a/1176023
        interim = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", word)

        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", interim).lower()

    @staticmethod
    def get_entity_type_name(entity: AbstractBusinessEntity) -> str:
        return BusinessEntityUtils.camel_to_snake(type(entity).__name__)

    @staticmethod
    def get_entity_class(entity_type_name: str):
        model_module = importlib.import_module(settings.APP_LABEL + ".models")

        return getattr(model_module, BusinessEntityUtils.snake_to_camel(entity_type_name))
