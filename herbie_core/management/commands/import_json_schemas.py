from django.core.management import BaseCommand
from herbie_core.services.schema_importer import SchemaImporter


class Command(BaseCommand):
    help = "import all json schemas to db"

    def handle(self, *args, **kwargs):
        schema_importer = SchemaImporter()
        schema_importer.import_schemas()
