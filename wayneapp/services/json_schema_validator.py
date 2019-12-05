import json
import re

from wayneapp.services import SchemaLoader
from jsonschema import Draft7Validator
from wayneapp.constants import ResponseConstants


class JsonSchemaValidator:
    def __init__(self):
        self._schema_loader = SchemaLoader()

    def validate_schema(self, json_data: json, business_entity: str, version: str) -> json:
        if not self.version_exist(version, business_entity):
            return 'version does not exist'
        schema = self._get_json_schema(business_entity, version)
        data_validated = Draft7Validator(schema)
        sorted_errors = sorted(data_validated.iter_errors(json_data), key=lambda e: e.path)
        errors = {}

        for error in sorted_errors:
            if error.validator == ResponseConstants.REQUIRED_KEY:
                error_property = re.search("'(.+?)'", error.message)
                if error_property:
                    errors[error_property.group(1)] = {
                        ResponseConstants.ERROR_MESSAGE: error.message,
                        ResponseConstants.VALIDATE_KEY: error.validator
                    }
            else:
                for error_property in error.path:
                    errors[error_property] = {
                        ResponseConstants.ERROR_MESSAGE: error.message,
                        ResponseConstants.VALIDATE_KEY: error.validator_value
                    }

        return errors

    def _get_json_schema(self, business_entity, version) -> json:
        file = self._schema_loader.load(business_entity, version)
        schema = json.loads(file)

        return schema

    def schema_entity_exist(self, business_entity: str) -> bool:
        business_entity_names = self._schema_loader.get_all_business_entity_names()

        return business_entity in business_entity_names

    def version_exist(self, version: str, business_entity: str) -> bool:
        versions = self._schema_loader.get_all_versions(business_entity)

        return version in versions
