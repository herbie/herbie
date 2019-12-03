from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.utils import json
import logging
from wayneapp.services import BusinessEntityManager, SchemaLoader
from wayneapp.validations.jsonSchemaValidator import JsonSchemaValidator


class BusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()

    def post(self, request: Request, type: str, key: str) -> Response:

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        version = body['version']
        payload = body['payload']

        error_messages = self._validator.validate_schema(payload, type, version)
        if error_messages:
            return self._custom_response(error_messages, status.HTTP_400_BAD_REQUEST)

        created = self._entity_manager.update_or_create(
            type, key, version, payload
        )
        return self.post_response(created)

    def post_response(self, created):
        if created:
            return self._custom_response("entity created", status.HTTP_201_CREATED)
        return self._custom_response("entity updated", status.HTTP_200_OK)

    def delete(self, request: Request, type: str, key: str) -> Response:
        self._entity_manager.delete_by_key(
            type, key
        )
        return self._custom_response("entity deleted", status.HTTP_200_OK)

    def _custom_response(self, message: str, status_code: status) -> Response:
        return Response(
            {
                "message": message
            },
            status=status_code
        )


class SchemaEntityController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request, type: str, version: str) -> Response:
        json_data = self._schema_loader.load(type, version)

        return Response(json.loads(json_data), status=status.HTTP_200_OK)
