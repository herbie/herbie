import json
import re

from wayneapp.services import SchemaLoader
from jsonschema import Draft7Validator
from wayneapp.constants import StatusConstants, ResponseConstants


class JsonSchemaValidator():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def validate_schema(self, jsonData: json, type: str, version: str) -> json:
        schema = self._get_json_schema(type, version)
        response = {StatusConstants.STATUS: StatusConstants.STATUS_OK}

        data_validated = Draft7Validator(schema)
        iterator = 0

        sorted_errors = sorted(data_validated.iter_errors(jsonData), key=lambda e: e.path)

        for error in sorted_errors:
            if error.validator == ResponseConstants.REQUIRED_KEY:
                error_property = re.search("'(.+?)'", error.message)
                if error_property:
                    response[error_property.group(1)] = {
                        ResponseConstants.ERROR_MESSAGE: error.message,
                        ResponseConstants.VALIDATE_KEY: error.validator
                    }
            else:
                for error_property in error.path:
                    response[error_property] = {
                        ResponseConstants.ERROR_MESSAGE: error.message,
                        ResponseConstants.VALIDATE_KEY: error.validator_value
                    }
            iterator += 1

        if iterator > 0:
            response[StatusConstants.STATUS] = StatusConstants.STATUS_ERROR

        return {ResponseConstants.RESPONSE_KEY: response}

    def _get_json_schema(self, type, version) -> json:
        schema = json.loads(self._schema_loader.load(type, version))

        return schema
