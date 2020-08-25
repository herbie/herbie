from django.core.management import BaseCommand
from herbie_core.services.schema_data_generator import SchemaDataGenerator


class Command(BaseCommand):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_data_generator = SchemaDataGenerator()

    def handle(self, *args, **kwargs):
        self._schema_data_generator.mock_data_from_schema()
