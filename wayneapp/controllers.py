import pkgutil
from _ast import Dict

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.utils import json
from wayneapp.services import BusinessEntityManager, SchemaLoader
from wayneapp.validations.validator import JsonSchemaValidator

class BusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()

    def post(self, request: Request, type: str, key: str) -> Response:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # TODO Validation Part
        # TODO validate(body[object],type)
        validator = JsonSchemaValidator()
        #response_validation = validator.validate_schema(body[object], type, version)

        version = self._get_version(body)
        try:
            self._entity_manager.update_or_create(
                type, key, body['payload']['version'], body['payload']
            )
        except Exception:
            # TODO log exception?
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({}, status=status.HTTP_200_OK)

    def get(self, test: str):
        # TODO delete, only for testing
        validator = JsonSchemaValidator()

        jsonData = {"cNumber": 'ff', "customerId": 22, "firstNameb": 11, "lastNamef": "testFirstName"}
        response_validation = validator.validate_schema(jsonData, 'customer', 'v1')

        return Response({'test': 'yes', 'responseV': response_validation}, status=status.HTTP_200_OK)

class SchemaEntityController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request, type: str, version: str) -> Response:
        json_data = self._schema_loader.load(type, version)

        return Response(json.loads(json_data), status=status.HTTP_200_OK)
