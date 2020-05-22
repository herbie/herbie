from herbieapp.initializers.abstract_initializer import AbstractInitializer
from herbieapp.services.schema_importer import SchemaImporter


class SchemaInitializer(AbstractInitializer):
    _schema_importer = None

    def __init__(
            self,
            schema_importer: SchemaImporter,
            **kwargs
    ):
        self._schema_importer = schema_importer

    def get_name(self) -> str:
        return 'schemas'

    def init(self):
        self._schema_importer.import_schemas()
