import json
import re

from jsonschema import Draft7Validator, draft7_format_checker
from herbie_core.constants import ValidatorResponseConstants
from herbie_core.services.schema_registry import SchemaRegistry


class JsonSchemaValidator:
    def __init__(self):
        self._schema_registry = SchemaRegistry()

    def validate_schema(self, schema: str, json_data: json) -> json:
        data_validated = Draft7Validator(schema, format_checker=draft7_format_checker)
        sorted_errors = sorted(data_validated.iter_errors(json_data), key=lambda e: e.path)

        errors = {}

        for error in sorted_errors:
            if error.validator == ValidatorResponseConstants.REQUIRED_KEY:
                error_property = re.search("'(.+?)'", error.message)
                if error_property:
                    errors[error_property.group(1)] = {
                        ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                        ValidatorResponseConstants.VALIDATE_KEY: error.validator,
                    }
            elif error.validator == ValidatorResponseConstants.ADDITIONAL_PROPERTIES:
                errors[error.validator] = {
                    ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                    ValidatorResponseConstants.VALIDATE_KEY: error.validator,
                }
            else:
                for error_property in error.path:
                    errors[error_property] = {
                        ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                        ValidatorResponseConstants.VALIDATE_KEY: error.validator_value,
                    }

        return errors

    def business_entity_exist(self, business_entity: str) -> bool:
        business_entity_names = self._schema_registry.get_all_schema_names()

        return business_entity in business_entity_names

    def version_exist(self, version: str, business_entity: str) -> bool:
        versions = self._schema_registry.get_all_versions(business_entity)

        return version in versions
