import json
import re

from wayneapp.services import SchemaLoader
from jsonschema import Draft7Validator


class JsonSchemaValidator():

    def validate_schema(self, jsonData: json, type: str, version: str) -> json:
        schema = self.__get_json_schema(type, version)
        response = {'status': 'ok'}

        data_validated = Draft7Validator(schema)
        iterator = 0

        sorted_errors = sorted(data_validated.iter_errors(jsonData), key=lambda e: e.path)
        for error in sorted_errors:
            if error.validator == 'required':
                error_property = re.search("'(.+?)'", error.message)
                if error_property:
                    response[error_property.group(1)] = {'error_message': error.message, 'validate': error.validator}
            else:
                for error_property in error.path:
                    response[error_property] = {'error_message': error.message, 'validate': error.validator_value}
            iterator += 1

        if iterator > 0:
            response['status'] = 'error'

        return {'response': response}

    def __get_json_schema(self, type, version) -> json:
        schema_loader = SchemaLoader()
        schema = json.loads(schema_loader.load(type, version))

        return schema
