import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet

from herbieapp.services import BusinessEntityManager, AbstractBusinessEntity, BusinessEntityUtils, MessagePublisher, \
    JsonSchemaValidator
from herbieapp.services.business_entity_compositor import BusinessEntityCompositor


class BusinessEntityHandler:
    """ orchestrates all logic for business entities """

    _business_entity_manager = BusinessEntityManager()
    _business_entity_compositor = BusinessEntityCompositor()
    _message_publisher = MessagePublisher()
    _validator = JsonSchemaValidator()
    _logger = logging.getLogger(__name__)

    def save(self, entity_name: str, key: str, version: str, user: User, data: str) -> bool:
        entity, created = self._business_entity_manager.update_or_create(entity_name, key, version, user, data)
        self._message_publisher.send_entity_update_message(entity)

        composite_entities = self._business_entity_compositor.on_entity_saved(entity, user)
        for composite_entity in composite_entities:
            self._business_entity_manager.save(composite_entity)

            composite_entity_name = BusinessEntityUtils.get_entity_type_name(composite_entity)
            errors = self._validator.validate_schema(composite_entity.data, composite_entity_name,
                                                     composite_entity.version)
            if errors:
                self._logger.debug(f"{composite_entity_name} is not valid (yet): {errors}")
            else:
                self._message_publisher.send_entity_update_message(composite_entity)

        return created

    def delete(self, entity_name: str, key: str, version: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key, version=version))

    def delete_by_key(self, entity_name: str, key: str) -> int:
        business_entity_class = BusinessEntityUtils.get_entity_class(entity_name)
        return self.delete_by_queryset(business_entity_class.objects.filter(key=key))

    def delete_by_queryset(self, queryset: QuerySet) -> int:
        for entity in queryset.all():
            self._message_publisher.send_entity_delete_message(entity)
            self._handle_composite_delete(entity)
        return self._business_entity_manager.delete_by_queryset(queryset)

    def delete_by_instance(self, entity: AbstractBusinessEntity) -> int:
        self._message_publisher.send_entity_delete_message(entity)
        self._handle_composite_delete(entity)
        return self._business_entity_manager.delete_by_instance(entity)

    def _handle_composite_delete(self, entity: AbstractBusinessEntity):
        composite_entities = self._business_entity_compositor.on_entity_deleted(entity)
        for composite_entity in composite_entities:
            self._message_publisher.send_entity_delete_message(composite_entity)
            self._business_entity_manager.delete_by_instance(composite_entity)
