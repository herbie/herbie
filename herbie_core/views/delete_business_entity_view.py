from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from herbie_core.constants import ControllerConstants as Constants
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.views.utils import ViewUtils
from herbie_core.services.permission_manager import PermissionManager


class DeleteBusinessEntityView(APIView):

    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()
        self._permission_classes = (IsAuthenticated,)
        self._permission_manager = PermissionManager()

    def post(self, request: Request, business_entity: str) -> Response:
        if not self._permission_manager.has_delete_permission(business_entity, request):
            return ViewUtils.unauthorized_response()

        body = ViewUtils.extract_body(request)
        key = body[Constants.KEY]
        if not self._validator.business_entity_exist(business_entity):
            return ViewUtils.business_entity_not_exist_response(business_entity)
        if Constants.VERSION not in body:
            return self._delete_all_versions(business_entity, key)

        return self._delete_from_version(body, business_entity, key)

    def _delete_all_versions(self, business_entity, key) -> Response:
        number_of_deleted_objects = self._entity_manager.delete_by_key(business_entity, key)

        message = (
            Constants.DELETE_ALL_VERSIONS_MESSAGE
            if number_of_deleted_objects > 0
            else Constants.DELETE_ALL_VERSIONS_MESSAGE_NOT_FOUND
        )

        return ViewUtils.custom_response(message.format(key), status.HTTP_200_OK)

    def _delete_from_version(self, body, business_entity, key) -> Response:
        version = body[Constants.VERSION]
        if not self._validator.version_exist(version, business_entity):
            return ViewUtils.custom_response(Constants.VERSION_NOT_EXIST.format(version), status.HTTP_400_BAD_REQUEST)
        number_of_deleted_objects = self._entity_manager.delete(business_entity, key, version)

        message = (
            Constants.DELETE_FROM_VERSION_MESSAGE
            if number_of_deleted_objects > 0
            else Constants.DELETE_FROM_VERSION_MESSAGE_NOT_FOUND
        )

        return ViewUtils.custom_response(message.format(key, version), status.HTTP_200_OK)
