import json
from django.core.management import BaseCommand
from wayneapp.services import SchemaRegistry, logging
from wayneapp.models import BusinessSchema


class Command(BaseCommand):
    help = 'import all json schemas to db'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaRegistry()
        self._logger = logging.getLogger(__name__)

    def handle(self, *args, **kwargs):
        schema_list = self._schema_loader.get_all_json_schemas()

        if len(schema_list) is 0:
            self._logger.error('No schemas defined!')
            return 0

        self._logger.info('Schema import started!')

        for schema in schema_list:
            schema_data = json.loads(schema)
            self._create_update_json_schema(schema_data['business_entity'], schema_data['version'], schema_data['data'])

        self._logger.info('Schemas imported successfully!')

        return 0

    def _create_update_json_schema(self, business_entity: str, version: str, data: str):
        schema = BusinessSchema.objects.filter(business_entity=business_entity, version=version)

        schema_data = json.loads(data) if data != '' else {}

        if schema.exists() is False:
            json_schema = BusinessSchema()
            json_schema.version = version
            json_schema.business_entity = business_entity
            json_schema.schema = schema_data
            json_schema.save()
        else:
            schema.update(business_entity=business_entity, version=version, schema=schema_data)
