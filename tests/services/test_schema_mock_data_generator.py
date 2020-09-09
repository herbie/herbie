import json
import pkgutil
from django.test import TestCase
from herbie_core.services.schema_mock_data.schema_mock_data_generator import SchemaMockDataGenerator
from jsonschema import validate, Draft7Validator, SchemaError


class TestSchemaMockDataGenerator(TestCase):
    def test_mock_generation(self):
        schema = self._load_test_schema()

        try:
            Draft7Validator.check_schema(schema)
        except SchemaError as e:
            self.fail(f"Schema is not a valid DRAFT 7 JSOn Schema, please fix it! {repr(e)}")

        generator = SchemaMockDataGenerator()
        mock_data_for_json_schema = generator.mock_data_from_schema(schema)

        validate(mock_data_for_json_schema, schema)

    def _load_test_schema(self):
        return json.loads(pkgutil.get_data("tests.test_schema", "test_entity/test_entity_v1.json"))
