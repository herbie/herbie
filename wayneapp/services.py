import importlib

from wayneapp.models.models import GenericModel


def get_model_class(type_name: str):
    """
    :param type_name: name of the generic model type
    :return: the class of the model
    """
    models_module = importlib.import_module("wayneapp.models")
    return getattr(models_module, str(type_name))


def update_or_create_generic_model(type_name: str, key: str, version: int, data: str) -> (GenericModel, bool):
    """
    :param type_name: name of the generic model type
    :param key: unique id of the data object
    :param version: version of the data object
    :param data: json data of the object
    :return: new or updated instance of the model
    """
    generic_model_class = get_model_class(type_name)
    obj, created = generic_model_class.objects.update_or_create(
        key=key,
        version=version,
        defaults={
            'key': key,
            'version': version,
            'data': data
        }
    )
    return obj


def delete_generic_model(type_name: str, key: str, version: int) -> None:
    """
    :param type_name: name of the generic model type
    :param key: unique id of the data object
    :param version: version of the data object
    """
    generic_model_class = get_model_class(type_name)
    generic_model_class.filter(key=key, version=version).delete()
