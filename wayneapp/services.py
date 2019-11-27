import importlib

from wayneapp.models.models import AbstractBusinessEntity


def get_business_entity_class(entity_name: str):
    models_module = importlib.import_module("wayneapp.models")
    return getattr(models_module, str(entity_name))


def update_or_create_business_entity(entity_name: str, key: str, version: int, data: str) -> (AbstractBusinessEntity, bool):
    business_entity_class = get_business_entity_class(entity_name)
    obj, created = business_entity_class.objects.update_or_create(
        key=key,
        version=version,
        defaults={
            'key': key,
            'version': version,
            'data': data
        }
    )
    return obj


def delete_business_entity(entity_name: str, key: str, version: int) -> None:
    business_entity_class = get_business_entity_class(entity_name)
    business_entity_class.objects.filter(key=key, version=version).delete()
