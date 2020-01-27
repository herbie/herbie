import logging

from django.contrib.auth.models import User

from herbieapp.models import AbstractBusinessEntity, Schema
from herbieapp.services import BusinessEntityUtils, SchemaRegistry, BusinessEntityManager


class BusinessEntityCompositor:
    """ combines multiple business entities into a new business entity, based on the JSON definition """

    _logger = logging.getLogger(__name__)
    _business_entity_manager = BusinessEntityManager()
    _schema_registry = SchemaRegistry()

    def on_entity_saved(self, entity: AbstractBusinessEntity, user: User) -> [AbstractBusinessEntity]:
        composite_entities = []
        entity_type_name = BusinessEntityUtils.get_entity_type_name(entity)
        composition_schemas = self._schema_registry.find_composite_schemas(entity_type_name)
        for composition_schema in composition_schemas:
            composite_entity = self._combine(entity_type_name, entity, composition_schema, user)
            if composite_entity:
                composite_entities.append(composite_entity)
        return composite_entities

    def on_entity_deleted(self, entity: AbstractBusinessEntity) -> [AbstractBusinessEntity]:
        composite_entities = []
        entity_type_name = BusinessEntityUtils.get_entity_type_name(entity)
        composition_schemas = self._schema_registry.find_composite_schemas(entity_type_name)
        for composition_schema in composition_schemas:
            composite_version = composition_schema.version
            composition_definition = next(definition for definition in composition_schema.content['composition']
                                          if definition['businessEntity'] == entity_type_name)
            key = entity.data.get(composition_definition['joinField'])
            entity = self._business_entity_manager.get_entity(composition_schema.name, key, composite_version)
            if entity:
                composite_entities.append(entity)
        return composite_entities

    def _combine(self, entity_type_name: str, entity: AbstractBusinessEntity, composition_schema: Schema,
                 user: User) -> AbstractBusinessEntity:
        composite_entity_name = composition_schema.name
        composite_version = composition_schema.version
        composite_class = BusinessEntityUtils.get_entity_class(composite_entity_name)

        composition_definition = next(definition for definition in composition_schema.content['composition']
                                      if definition['businessEntity'] == entity_type_name)
        if not composition_definition:
            self._logger.error(f"no composition_definition for entity {entity_type_name} found in "
                               f"composition_schema {composition_schema.__dict__}")
        if composition_definition['version'] != entity.version:
            return

        key = entity.data.get(composition_definition['joinField'])
        if not key:
            self._logger.error(f"can't combine {entity_type_name} with {composite_entity_name}, "
                               f"because the join key value {composition_definition['joinField']} is empty!")
            return

        composite_entity = self._business_entity_manager.get_entity(composite_entity_name, key, composite_version)
        if not composite_entity:
            composite_entity = composite_class(key=key, version=composite_version, publisher=user, data={})

        self._logger.debug(f"combining {entity_type_name} with {composite_entity_name} {composite_version}, "
                           f"using join key: {key}")

        for field in composition_definition['fields']:
            value = entity.data.get(field, None)
            if value:
                composite_entity.data[field] = value

        return composite_entity
