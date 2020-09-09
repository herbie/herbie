from faker import Faker
from herbie_core.constants import JsonSchemaPropertiesConstants
from herbie_core.services.schema_mock_data.schema_data_type_mapper import SchemaDataTypeMapper


class SchemaMockDataGenerator:
    def __init__(self):
        self._mapper = SchemaDataTypeMapper()
        self._faker = Faker()

    def mock_data_from_schema(self, schema: dict):
        schema_type = schema.get(JsonSchemaPropertiesConstants.PROPERTY_TYPE, None)

        if isinstance(schema_type, list):
            schema_type = self._faker.random_element(elements=schema_type)

        return self._mapper.generate_from_data_type(schema_type, schema)
