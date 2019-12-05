from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from wayneapp.controllers.utils import ControllerUtils
from wayneapp.services import BusinessEntityManager, SchemaLoader, JsonSchemaValidator


class SaveBusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()
        self._schema_loader = SchemaLoader()

    def post(self, request: Request, business_entity: str) -> Response:
        if not self._validator.schema_entity_exist(business_entity):
            return ControllerUtils.custom_response('schema files does not exist', status.HTTP_400_BAD_REQUEST)
        body = ControllerUtils.extract_body(request)

        if 'version' not in body:
            return ControllerUtils.custom_response('Version is missing.', status.HTTP_400_BAD_REQUEST)

        version = body['version']
        key = body['key']
        payload = body['payload']
        error_messages = self._validator.validate_schema(payload, business_entity, version)
        if error_messages:
            return ControllerUtils.custom_response(error_messages, status.HTTP_400_BAD_REQUEST)
        created = self._entity_manager.update_or_create(
            business_entity, key, version, payload
        )

        return self._create_response(created, version)

    def _create_response(self, created, version):
        if created:
            return ControllerUtils.custom_response('entity created in version ' + version, status.HTTP_201_CREATED)

        return ControllerUtils.custom_response('entity updated in version ' + version, status.HTTP_200_OK)


