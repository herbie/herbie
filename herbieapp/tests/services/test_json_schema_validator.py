import pkgutil
from unittest import mock
import json

from django.test import TestCase
from herbieapp.services import settings
from herbieapp.services import JsonSchemaValidator, SchemaRegistry


class JsonSchemaValidatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(JsonSchemaValidatorTestCase, cls).setUpClass()
        settings.SCHEMA_REGISTRY_PACKAGE = 'herbieapp.tests.test_schema'
        cls._schema_validator = JsonSchemaValidator()
        cls._business_entity = 'test_entity'
        cls._version_1 = 'v1'

    @mock.patch.object(SchemaRegistry, 'get_all_versions')
    @mock.patch.object(SchemaRegistry, 'find_schema')
    def test_validate_success(self, mock_find_schema, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        mock_find_schema.return_value = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "testId": 12,
            "name": "testName"
        }

        validation_messages = self._schema_validator.validate_schema(json_data, self._business_entity, self._version_1)

        self.assertEqual({}, validation_messages)

    @mock.patch.object(SchemaRegistry, 'get_all_versions')
    @mock.patch.object(SchemaRegistry, 'find_schema')
    def test_validate_additional_property_error(self, mock_find_schema, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        mock_find_schema.return_value = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "testId": 12,
            "name": "testName",
            "someAdditionalProperty": "testSome"
        }

        validation_messages = self._schema_validator.validate_schema(json_data, self._business_entity, self._version_1)
        message_response_expected = {'additionalProperties':
                                         {'error_message': 'Additional properties are not '
                                                           "allowed ('someAdditionalProperty' "'was unexpected)',
                                          'validation_error': 'additionalProperties'}
                                     }

        self.assertEqual(message_response_expected, validation_messages)

    @mock.patch.object(SchemaRegistry, 'get_all_versions')
    @mock.patch.object(SchemaRegistry, 'find_schema')
    def test_validate_required_error(self, mock_find_schema, mock_get_all_versions):
        mock_get_all_versions.return_value = [self._version_1]
        mock_find_schema.return_value = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "name": "testName",
        }

        validation_messages = self._schema_validator.validate_schema(json_data, self._business_entity, self._version_1)
        message_response_expected = {'testId':
            {
                'error_message': "'testId' is a required property",
                'validation_error': 'required'
            }
        }

        self.assertEqual(message_response_expected, validation_messages)

    @mock.patch.object(SchemaRegistry, 'find_schema')
    @mock.patch.object(SchemaRegistry, 'get_all_versions')
    def test_validate_type_error(self, mock_get_all_versions, mock_find_schema):
        mock_get_all_versions.return_value = [self._version_1]
        mock_find_schema.return_value = self._load_test_schema(self._business_entity, self._version_1)

        json_data = {
            "testId": "wrongType",
            "name": "testName",
        }

        validation_messages = self._schema_validator.validate_schema(json_data, self._business_entity, self._version_1)
        message_response_expected = {'testId':
            {
                'error_message': "'wrongType' is not of type 'integer'",
                'validation_error': 'integer'
            }
        }

        self.assertEqual(message_response_expected, validation_messages)

    def test_validate_entity_in_version_missing(self):
        json_data = {
            "testId": "wrongType",
            "name": "testName",
        }

        validation_messages = self._schema_validator.validate_schema(json_data, 'wrong', self._version_1)
        message_response_expected = "version " + self._version_1 + " does not exist"

        self.assertEqual(message_response_expected, validation_messages)

    def _load_test_schema(self, business_entity, version):
        return json.loads(pkgutil.get_data('herbieapp.tests.test_schema',
                                business_entity + '/' + business_entity + '_' + version +  '.json'))