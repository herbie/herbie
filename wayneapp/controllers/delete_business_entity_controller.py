from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from wayneapp.controllers.utils import ControllerUtils
from wayneapp.services import BusinessEntityManager, JsonSchemaValidator


class DeleteBusinessEntityController(APIView):

    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()

    def post(self, request: Request, business_entity: str) -> Response:
        body = ControllerUtils.extract_body(request)
        key = body['key']
        if not self._validator.schema_entity_exist(business_entity):
            return ControllerUtils.custom_response('schema files does not exist', status.HTTP_400_BAD_REQUEST)
        if 'version' not in body:
            return self._delete_all_versions(business_entity, key)

        return self._delete_by_version(body, business_entity, key)

    def _delete_all_versions(self, business_entity, key) -> Response:
        self._entity_manager.delete_by_key(
            business_entity, key
        )

        return ControllerUtils.custom_response('entity deleted from all versions', status.HTTP_200_OK)

    def _delete_by_version(self, body, business_entity, key) -> Response:
        version = body['version']
        if not self._validator.version_exist(version, business_entity):
            return ControllerUtils.custom_response('version does not exist', status.HTTP_400_BAD_REQUEST)
        self._entity_manager.delete(business_entity, key, version)

        return ControllerUtils.custom_response('entity deleted from version ' + version, status.HTTP_200_OK)



