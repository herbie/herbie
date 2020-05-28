from django.core.management import BaseCommand
from herbieapp.services.schema_importer import SchemaImporter
import inject


class Command(BaseCommand):
    help = 'import all json schemas to db'
    _schema_importer = None

    @inject.autoparams()
    def __init__(
            self,
            schema_importer: SchemaImporter,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._schema_importer = schema_importer

    def handle(self, *args, **kwargs):
        self._schema_importer.import_schemas()
