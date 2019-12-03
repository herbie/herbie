import json
import re

from wayneapp.services import SchemaLoader
from jsonschema import Draft7Validator
from wayneapp.constants import StatusConstants, ResponseConstants


class JsonSchemaValidator:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def validate_schema(self, json_data: json, type: str, version: str) -> json:
        if not self._type_exist(type):
            return 'schema files does not exist'
        if not self._version_exist(version, type):
            return 'version does not exist'
        schema = self._get_json_schema(type, version)
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

    def _get_json_schema(self, type, version) -> json:
        file = self._schema_loader.load(type, version)
        schema = json.loads(file)
        return schema

    def _type_exist(self, type: str) -> bool:
        business_entity_names = self._schema_loader.get_all_business_entity_names()
        return type in business_entity_names

    def _version_exist(self, version: str, type: str) -> bool:
        versions = self._schema_loader.get_all_versions(type)
        return version in versions
