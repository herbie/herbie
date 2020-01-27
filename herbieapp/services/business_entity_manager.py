from django.contrib.auth.models import User
from django.db.models import QuerySet

from herbieapp.models.models import AbstractBusinessEntity
from herbieapp.services import BusinessEntityUtils


class BusinessEntityManager:
    """ encapsulates database access for business entities """

    def get_entity(self, entity_name: str, key: str, version: str) -> AbstractBusinessEntity:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return business_entity_class.objects.filter(key=key, version=version).first()

    def update_or_create(self, entity_name: str, key: str, version: str, user: User, data: str
                         ) -> (AbstractBusinessEntity, bool):
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return business_entity_class.objects.update_or_create(
            key=key,
            version=version,
            defaults={
                'key': key,
                'version': version,
                'publisher': user,
                'data': data
            }
        )

    def save(self, entity: AbstractBusinessEntity):
        entity.save()

    def find_all(self, entity_name: str) -> QuerySet:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return business_entity_class.objects.all()

    def delete_by_queryset(self, queryset: QuerySet) -> int:
        return queryset.delete()[0]

    def delete_by_instance(self, entity: AbstractBusinessEntity) -> int:
        return entity.delete()[0]
