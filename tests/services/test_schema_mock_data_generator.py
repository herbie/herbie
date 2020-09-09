import glob
import json
import os
import pkgutil

import pytest
from herbie_core.services.schema_mock_data.schema_mock_data_generator import SchemaMockDataGenerator
from jsonschema import validate, Draft7Validator, SchemaError


class TestSchemaMockDataGenerator:
    os.chdir("tests/test_schema/mock_data_generation")
    mock_data_json_schemas = glob.glob("*.json")

    @pytest.mark.parametrize("filename", mock_data_json_schemas)
    def test_mock_generation(self, filename):
        schema = json.loads(pkgutil.get_data("tests.test_schema", "mock_data_generation/" + filename))

        try:
            Draft7Validator.check_schema(schema)
        except SchemaError as e:
            pytest.fail(f"Schema is not a valid DRAFT 7 JSOn Schema, please fix it! {repr(e)}")

        generator = SchemaMockDataGenerator()
        mock_data_for_json_schema = generator.mock_data_from_schema(schema)

        validate(mock_data_for_json_schema, schema)
