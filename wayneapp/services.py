import importlib

from wayneapp.models import GenericModel


def update_or_create_generic_model(type_name: str, key: str, version: int, data: str) -> (GenericModel, bool):
    models_module = importlib.import_module("wayneapp.models")
    generic_class = getattr(models_module, str(type_name))

    return generic_class.objects.update_or_create(
        key=key,
        version=version,
        defaults={
            'key': key,
            'version': version,
            'data': data
        }
    )
