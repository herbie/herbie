import pkgutil
from unittest import mock
import json

from django.conf import settings
from django.test import TestCase
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.services.schema_registry import SchemaRegistry


class JsonSchemaValidatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(JsonSchemaValidatorTestCase, cls).setUpClass()
        settings.SCHEMA_REGISTRY_PACKAGE = "tests.test_schema"
        cls._schema_validator = JsonSchemaValidator()
        cls._business_entity = "test_entity"
        cls._version_1 = "v1"

    @mock.patch.object(SchemaRegistry, "get_all_versions")
    def test_validate_success(self, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        schema_json = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {"testId": 12, "name": "testName", "created_at": "2020-07-10T15:03:23+02:00"}

        validation_messages = self._schema_validator.validate_schema(schema_json, json_data)

        self.assertEqual({}, validation_messages)

    @mock.patch.object(SchemaRegistry, "get_all_versions")
    def test_validate_additional_property_error(self, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        schema_json = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {"testId": 12, "name": "testName", "someAdditionalProperty": "testSome"}

        validation_messages = self._schema_validator.validate_schema(schema_json, json_data)
        message_response_expected = {
            "additionalProperties": {
                "error_message": "Additional properties are not "
                "allowed ('someAdditionalProperty' "
                "was unexpected)",
                "validation_error": "additionalProperties",
            }
        }

        self.assertEqual(message_response_expected, validation_messages)

    @mock.patch.object(SchemaRegistry, "get_all_versions")
    def test_validate_required_error(self, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        schema_json = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "name": "testName",
        }

        validation_messages = self._schema_validator.validate_schema(schema_json, json_data)
        message_response_expected = {
            "testId": {"error_message": "'testId' is a required property", "validation_error": "required"}
        }

        self.assertEqual(message_response_expected, validation_messages)

    @mock.patch.object(SchemaRegistry, "get_all_versions")
    def test_validate_type_error(self, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        schema_json = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "testId": "wrongType",
            "name": "testName",
        }

        validation_messages = self._schema_validator.validate_schema(schema_json, json_data)
        message_response_expected = {
            "testId": {"error_message": "'wrongType' is not of type 'integer'", "validation_error": "integer"}
        }

        self.assertEqual(message_response_expected, validation_messages)

    @mock.patch.object(SchemaRegistry, "get_all_versions")
    def test_validate_string_date_time_format(self, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        schema_json = self._load_test_schema(self._business_entity, self._version_1)

        invalid_date_time = "2020/10/07 16:00:00"

        json_data = {
            "testId": 123,
            "name": "testName",
            "created_at": invalid_date_time,
        }

        validation_messages = self._schema_validator.validate_schema(schema_json, json_data)

        message_response_expected = {
            "created_at": {
                "error_message": f"'{invalid_date_time}' is not a 'date-time'",
                "validation_error": "date-time",
            }
        }

        self.assertEqual(message_response_expected, validation_messages)

    def _load_test_schema(self, business_entity, version):
        return json.loads(
            pkgutil.get_data("tests.test_schema", business_entity + "/" + business_entity + "_" + version + ".json")
        )
