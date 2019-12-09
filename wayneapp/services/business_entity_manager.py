
import importlib
from wayneapp.services import MessagePublisher
from wayneapp.models.models import AbstractBusinessEntity


class BusinessEntityManager:

    _message_service = MessagePublisher()

    def get_class(self, entity_name: str):
        models_module = importlib.import_module('wayneapp.models')

        return getattr(models_module, str(entity_name).capitalize())

    def update_or_create(
            self,
            entity_name: str,
            key: str,
            version: str,
            data: str
    ) -> (AbstractBusinessEntity, bool):
        business_entity_class = self.get_class(entity_name)
        business_entity, created = business_entity_class.objects.update_or_create(
            key=key,
            version=version,
            defaults={
                'key': key,
                'version': version,
                'data': data
            }
        )

        self._message_service.send_entity_update_message(business_entity)

        return created

    def delete(self, entity_name: str, key: str, version: str) -> None:
        business_entity_class = self.get_class(entity_name)
        business_entity_class.objects.filter(key=key, version=version).delete()

        self._message_service.send_entity_delete_message(entity_name, key, version)

    def delete_by_key(self, entity_name: str, key: str) -> None:
        business_entity_class = self.get_class(entity_name)
        business_entity_class.objects.filter(key=key).delete()

        self._message_service.send_entity_delete_message(entity_name, key)
