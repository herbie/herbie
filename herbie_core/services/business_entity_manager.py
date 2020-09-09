from typing import Optional

from django.contrib.auth.models import User
from django.db.models import QuerySet
from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.message_publisher.message_publisher import MessagePublisher
from herbie_core.services.utils import BusinessEntityUtils


class BusinessEntityManager:

    _message_publisher = MessagePublisher()

    def update_or_create(
        self, entity_name: str, key: str, version: str, user: User, data: str
    ) -> (AbstractBusinessEntity, bool):
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        business_entity, created = business_entity_class.objects.update_or_create(
            key=key, version=version, defaults={"key": key, "version": version, "publisher": user, "data": data}
        )

        if created:
            self._message_publisher.send_entity_create_message(business_entity)
        else:
            self._message_publisher.send_entity_update_message(business_entity)

        return created

    def find_all(self, entity_name: str) -> QuerySet:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return business_entity_class.objects.all()

    def find_by_key_and_version(self, entity_name: str, key: str, version: str) -> Optional[AbstractBusinessEntity]:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)

        try:
            business_entity = business_entity_class.objects.get(key=key, version=version)
        except business_entity_class.DoesNotExist:
            business_entity = None

        return business_entity

    def delete(self, entity_name: str, key: str, version: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key, version=version))

    def delete_by_key(self, entity_name: str, key: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key))

    def delete_by_queryset(self, queryset: QuerySet) -> int:
        for entity in queryset.all():
            self._message_publisher.send_entity_delete_message(entity)
        # return only the number of deleted objects
        return queryset.delete()[0]

    def delete_by_instance(self, entity: AbstractBusinessEntity) -> int:
        self._message_publisher.send_entity_delete_message(entity)
        return entity.delete()[0]
