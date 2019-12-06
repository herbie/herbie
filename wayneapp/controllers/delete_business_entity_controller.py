from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from wayneapp.constants import ControllerConstants as Constants
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
        key = body[Constants.KEY]
        if not self._validator.business_entity_exist(business_entity):
            return ControllerUtils.business_entity_not_exist_response(business_entity)
        if Constants.VERSION not in body:
            return self._delete_all_versions(business_entity, key)

        return self._delete_from_version(body, business_entity, key)

    def _delete_all_versions(self, business_entity, key) -> Response:
        self._entity_manager.delete_by_key(
            business_entity, key
        )

        return ControllerUtils.custom_response(
            Constants.DELETE_ALL_VERSIONS_MESSAGE.format(key),
            status.HTTP_200_OK
        )

    def _delete_from_version(self, body, business_entity, key) -> Response:
        version = body[Constants.VERSION]
        if not self._validator.version_exist(version, business_entity):
            return ControllerUtils.custom_response(
                Constants.VERSION_NOT_EXIST.format(version),
                status.HTTP_400_BAD_REQUEST
            )
        self._entity_manager.delete(business_entity, key, version)

        return ControllerUtils.custom_response(
            Constants.DELETE_FROM_VERSION_MESSAGE.format(key, version),
            status.HTTP_200_OK
        )



