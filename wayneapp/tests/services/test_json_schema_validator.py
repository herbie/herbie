from django.test import TestCase
from wayneapp.services import settings
from wayneapp.services import JsonSchemaValidator


class JsonSchemaValidatorTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(JsonSchemaValidatorTestCase, cls).setUpClass()
        settings.SCHEMA_REGISTRY_PACKAGE = 'wayneapp.tests.test_schema'
        cls._schema_validator = JsonSchemaValidator()
        cls._business_entity = 'test_entity'
        cls._version_1 = 'v1'

    def test_validate_success(self):
        json_data = {
            "testId": 12,
            "name": "testName"
        }

        validation_messages = self._schema_validator.validate_schema(json_data, self._business_entity, self._version_1)

        self.assertEqual({}, validation_messages)

    def test_validate_additional_property_error(self):
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

    def test_validate_required_error(self):
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

    def test_validate_type_error(self):
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
