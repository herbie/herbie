import logging

from django.db.models import QuerySet
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.services.business_entity_manager import BusinessEntityManager


class SchemaVersionCompatibility:
    def __init__(self):
        self._business_entity_manager = BusinessEntityManager()
        self._schema_validator = JsonSchemaValidator()
        self._logger = logging.getLogger(__name__)

    def is_backwards_compatible(self, new_schema: str, business_entity: str, version: str):
        saved_entities = self._business_entity_manager.find_by_version(entity_name=business_entity, version=version)

        if not saved_entities:
            return True

        return self._validate_entity_data(
            saved_entities=saved_entities, schema=new_schema, business_entity=business_entity, version=version
        )

    def _validate_entity_data(self, saved_entities: QuerySet, schema: str, business_entity: str, version: str):
        for entity in saved_entities:
            errors = self._schema_validator.validate_schema(schema, entity.data, business_entity, version)

            if errors:
                self._logger.info(f"Key#{entity.key} is not valid with new Schema: {errors}")
                return False

        return True
