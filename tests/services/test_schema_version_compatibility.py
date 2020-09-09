import json
import pkgutil
from unittest import mock

from django.conf import settings
from django.test import TestCase

from herbie_core.services.schema_version_compatibility import SchemaVersionCompatibility


class TestSchemaVersionCompatibility(TestCase):
    def setUp(self):
        settings.SCHEMA_REGISTRY_PACKAGE = "tests.test_schema"
        self._saved_schema = self._load_test_schema("test_entity")

    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaRegistry")
    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaMockDataGenerator")
    @mock.patch("herbie_core.services.schema_version_compatibility.JsonSchemaValidator")
    def test_validation_succeeds_when_validation_has_no_errors(
        self, mock_json_schema_validator, mock_schema_mock_generator, mock_schema_registry
    ):
        mock_schema_registry().find_schema.return_value = {}
        mock_json_schema_validator().validate_schema.return_value = None
        mock_schema_mock_generator().mock_data_from_schema.return_value = {}

        version_compatibility = SchemaVersionCompatibility()

        self.assertTrue(version_compatibility.is_backwards_compatible({}, "entity", "v1"))

    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaRegistry")
    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaMockDataGenerator")
    @mock.patch("herbie_core.services.schema_version_compatibility.JsonSchemaValidator")
    def test_validation_fails_when_validation_has_some_error(
        self, mock_json_schema_validator, mock_schema_mock_generator, mock_schema_registry
    ):
        mock_schema_registry().find_schema.return_value = {}
        mock_schema_mock_generator().mock_data_from_schema.return_value = {}
        mock_json_schema_validator().validate_schema.return_value = ["error"]

        version_compatibility = SchemaVersionCompatibility()

        self.assertFalse(version_compatibility.is_backwards_compatible("schema", "entity", "v1"))

    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaRegistry")
    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaMockDataGenerator")
    def test_validation_succeds_with_compatible_new_schema(self, mock_schema_mock_generator, mock_schema_registry):
        mock_schema_mock_generator().mock_data_from_schema.return_value = {"firstName": "first"}
        mock_schema_registry().find_schema.return_value = self._load_test_schema("test_entity_new")

        version_compatibility = SchemaVersionCompatibility()

        self.assertTrue(
            version_compatibility.is_backwards_compatible(new_schema={}, business_entity="entity", version="v1")
        )

    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaRegistry")
    @mock.patch("herbie_core.services.schema_version_compatibility.SchemaMockDataGenerator")
    def test_validation_fails_with_breaking_new_schema(self, mock_schema_mock_generator, mock_schema_registry):
        mock_schema_mock_generator().mock_data_from_schema.return_value = {"firstName": "first"}
        mock_schema_registry().find_schema.return_value = self._load_test_schema("test_entity_not_bc")

        version_compatibility = SchemaVersionCompatibility()

        self.assertFalse(
            version_compatibility.is_backwards_compatible(new_schema={}, business_entity="entity", version="v1")
        )

    def _load_test_schema(self, schema_filename):
        return json.loads(
            pkgutil.get_data("tests.test_schema", "backwards_compatibility" + "/" + schema_filename + "_v1.json")
        )
