import logging

from herbie_core.services.schema_registry import SchemaRegistry
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.services.schema_mock_data.schema_mock_data_generator import SchemaMockDataGenerator


class SchemaVersionCompatibility:
    def __init__(self):
        self._schema_validator = JsonSchemaValidator()
        self._logger = logging.getLogger(__name__)
        self._mock_data_generator = SchemaMockDataGenerator()
        self._schema_registry = SchemaRegistry()

    def is_backwards_compatible(self, new_schema: dict, business_entity: str, version: str):
        new_schema_mock_data = self._mock_data_generator.mock_data_from_schema(new_schema)
        current_schema_version = self._schema_registry.find_schema(business_entity=business_entity, version=version)

        errors = self._schema_validator.validate_schema(schema=current_schema_version, json_data=new_schema_mock_data)

        if errors:
            self._logger.info(f"Error validating new Schema: {errors}")
            return False

        return True
