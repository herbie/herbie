import json
import logging

from herbie_core.models.schema import Schema
from herbie_core.services.schema_package import SchemaPackage
from herbie_core.services.schema_registry import SchemaRegistry
from herbie_core.services.schema_version_compatibility import SchemaVersionCompatibility


class SchemaImporter:
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._schema_package = SchemaPackage()
        self._schema_compatibility = SchemaVersionCompatibility()

    def import_schemas(self):
        schema_list = self._schema_package.get_all_json_schemas()

        if len(schema_list) == 0:
            self._logger.error("No schemas defined!")
            return 0

        self._logger.info("Schema import started!!")

        for schema in schema_list:
            schema_data = json.loads(schema)
            self._logger.info(f"Processing schema {schema_data['business_entity']}_{schema_data['version']}!!")
            self._save_json_schema(schema_data["business_entity"], schema_data["version"], schema_data["data"])

        self._logger.info("Schemas import ended!!")

        return 0

    def _save_json_schema(self, business_entity: str, version: str, data: str):
        schema = Schema.objects.filter(name=business_entity, version=version)

        reg = SchemaRegistry()
        reg.find_schema(business_entity, version)

        schema_data = json.loads(data) if data != "" else {}

        if not schema.exists():
            self._create_json_schema(business_entity=business_entity, version=version, data=schema_data)
        else:
            self._update_json_schema(schema=schema, business_entity=business_entity, version=version, data=schema_data)

    def _create_json_schema(self, business_entity: str, version: str, data: str):
        json_schema = Schema()
        json_schema.name = business_entity
        json_schema.version = version
        json_schema.content = data
        json_schema.save()

        self._logger.info(f"Schema for Entity: {business_entity} / Version: {version} created!!")

    def _update_json_schema(self, schema: Schema, business_entity: str, version: str, data: str):

        is_new_schema_backwards_compatible = self._schema_compatibility.is_backwards_compatible(
            new_schema=data, business_entity=business_entity, version=version
        )

        if is_new_schema_backwards_compatible is False:
            self._logger.error("Cannot import schema: Introduces Backwards-Compatibility Break!")
            return

        schema.update(name=business_entity, version=version, content=data)

        self._logger.info(f"Schema for Entity: {business_entity} / Version: {version} updated!!")
