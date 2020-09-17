from faker import Faker
from herbie_core.constants import JsonSchemaPropertiesConstants


class SchemaConstGenerator:
    def __init__(self):
        self._faker = Faker()

    def generate_const(self, schema: dict):
        return schema[JsonSchemaPropertiesConstants.CONST_TYPE_PROPERTY]
