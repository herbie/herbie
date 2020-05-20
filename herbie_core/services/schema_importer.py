import json
from herbie_core.services import logging, SchemaRegistry, SchemaPackage
from herbie_core.models import Schema


class SchemaImporter:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._schema_package = SchemaPackage()

    def import_schemas(self):
        schema_list = self._schema_package.get_all_json_schemas()

        if len(schema_list) == 0:
            self._logger.error('No schemas defined!')
            return 0

        self._logger.info('Schema import started!')

        for schema in schema_list:
            schema_data = json.loads(schema)
            self._create_update_json_schema(schema_data['business_entity'], schema_data['version'], schema_data['data'])

        self._logger.info('Schemas imported successfully!')

        return 0

    def _create_update_json_schema(self, business_entity: str, version: str, data: str):
        schema = Schema.objects.filter(name=business_entity, version=version)

        reg = SchemaRegistry()
        reg.find_schema(business_entity, version)

        schema_data = json.loads(data) if data != '' else {}

        if not schema.exists():
            json_schema = Schema()
            json_schema.name = business_entity
            json_schema.version = version
            json_schema.content = schema_data
            json_schema.save()
        else:
            schema.update(name=business_entity, version=version, content=schema_data)
