from django.db.models import QuerySet

from wayneapp.services import MessagePublisher, BusinessEntityUtils
import importlib
from django.db.models import QuerySet
from wayneapp.services import MessagePublisher
from wayneapp.models.models import AbstractBusinessEntity


class BusinessEntityManager:

    _message_service = MessagePublisher()

    def update_or_create(
            self,
            entity_name: str,
            key: str,
            version: str,
            data: str
    ) -> (AbstractBusinessEntity, bool):
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
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

    def find_all(self, entity_name: str) -> QuerySet:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return business_entity_class.objects.all()

    def delete(self, entity_name: str, key: str, version: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key, version=version))

    def delete_by_key(self, entity_name: str, key: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key))

    def delete_by_queryset(self, queryset: QuerySet) -> int:
        for entity in queryset.all():
            self._message_service.send_entity_delete_message(entity)
        # return only the number of deleted objects
        return queryset.delete()[0]

    def delete_by_instance(self, entity: AbstractBusinessEntity) -> int:
        self._message_service.send_entity_delete_message(entity)
        return entity.delete()[0]
