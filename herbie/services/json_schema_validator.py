import json
import re

from herbie.services import SchemaRegistry
from jsonschema import Draft7Validator
from herbie.constants import ValidatorResponseConstants, ControllerConstants


class JsonSchemaValidator:
    def __init__(self):
        self._schema_registry = SchemaRegistry()

    def validate_schema(self, json_data: json, business_entity: str, version: str) -> json:
        if not self.version_exist(version, business_entity):
            return ControllerConstants.VERSION_NOT_EXIST.format(version)
        schema = self._get_json_schema(business_entity, version)
        data_validated = Draft7Validator(schema)
        sorted_errors = sorted(data_validated.iter_errors(json_data), key=lambda e: e.path)
        errors = {}

        for error in sorted_errors:
            if error.validator == ValidatorResponseConstants.REQUIRED_KEY:
                error_property = re.search("'(.+?)'", error.message)
                if error_property:
                    errors[error_property.group(1)] = {
                        ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                        ValidatorResponseConstants.VALIDATE_KEY: error.validator
                    }
            elif error.validator == ValidatorResponseConstants.ADDITIONAL_PROPERTIES:
                errors[error.validator] = {
                    ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                    ValidatorResponseConstants.VALIDATE_KEY: error.validator
                }
            else:
                for error_property in error.path:
                    errors[error_property] = {
                        ValidatorResponseConstants.ERROR_MESSAGE: error.message,
                        ValidatorResponseConstants.VALIDATE_KEY: error.validator_value
                    }

        return errors

    def _get_json_schema(self, business_entity, version) -> json:
        schema = self._schema_registry.find_schema(business_entity, version)

        return schema

    def business_entity_exist(self, business_entity: str) -> bool:
        business_entity_names = self._schema_registry.get_all_schema_names()

        return business_entity in business_entity_names

    def version_exist(self, version: str, business_entity: str) -> bool:
        versions = self._schema_registry.get_all_versions(business_entity)

        return version in versions
