from herbie_core.initializers.abstract_initializer import AbstractInitializer
from herbie_core.services.schema_importer import SchemaImporter


class SchemaInitializer(AbstractInitializer):
    def get_name(self) -> str:
        return "schemas"

    def init(self):
        schema_importer = SchemaImporter()
        schema_importer.import_schemas()
