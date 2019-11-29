import json
import os
import re

from jsonschema import validators
from jsonschema import ValidationError
from jsonschema import exceptions
from jsonschema import FormatError
from jsonschema import ErrorTree
from jsonschema import Draft7Validator


class JsonSchemaValidator():

    def validate_schema(self, jsonData: json) -> json:
        schema = self.get_json_schema()
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

    def get_json_schema(self) -> json:
        # projectDir = os.path.dirname(__file__)
        # jsonValidatorPath = os.path.join(projectDir, "json/customer.json")

        # with open(jsonValidatorPath, 'r') as f:
        #    schema_data = f.read()
        # schema = json.loads(schema_data)

        schema = {"$schema": "http://json-schema.org/draft-07/schema#",
                  "$id": "customer", "title": "Customer", "description": "Customer info",
                  "type": "object", "properties": {
                "customerId": {"description": "The unique identifier for a customer", "type": "string"},
                "cNumber": {"type": "number"}, "firstName": {"type": "string"}, "lastName": {"type": "string"}},
                  "required": ["firstName", "lastName", "cNumber"]}

        return schema
