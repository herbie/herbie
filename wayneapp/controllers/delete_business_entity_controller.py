from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
        self._permission_classes = (IsAuthenticated,)

    def post(self, request: Request, business_entity: str) -> Response:
        if not self.has_delete_permission(business_entity, request):
            return ControllerUtils.unauthorized_response()
        body = ControllerUtils.extract_body(request)
        key = body[Constants.KEY]
        if not self._validator.business_entity_exist(business_entity):
            return ControllerUtils.business_entity_not_exist_response(business_entity)
        if Constants.VERSION not in body:
            return self._delete_all_versions(business_entity, key)

        return self._delete_from_version(body, business_entity, key)

    def _delete_all_versions(self, business_entity, key) -> Response:
        number_of_deleted_objects = self._entity_manager.delete_by_key(
            business_entity, key
        )

        message = Constants.DELETE_ALL_VERSIONS_MESSAGE if number_of_deleted_objects > 0 \
            else Constants.DELETE_ALL_VERSIONS_MESSAGE_NOT_FOUND
        return ControllerUtils.custom_response(
            message.format(key),
            status.HTTP_200_OK
        )

    def _delete_from_version(self, body, business_entity, key) -> Response:
        version = body[Constants.VERSION]
        if not self._validator.version_exist(version, business_entity):
            return ControllerUtils.custom_response(
                Constants.VERSION_NOT_EXIST.format(version),
                status.HTTP_400_BAD_REQUEST
            )
        number_of_deleted_objects = self._entity_manager.delete(business_entity, key, version)

        message = Constants.DELETE_FROM_VERSION_MESSAGE if number_of_deleted_objects > 0 \
            else Constants.DELETE_FROM_VERSION_MESSAGE_NOT_FOUND
        return ControllerUtils.custom_response(
            message.format(key, version),
            status.HTTP_200_OK
        )

    def has_delete_permission(self, business_entity: str, request: Request) -> bool:
        delete_permission = ControllerUtils.get_permission_string(Constants.DELETE, business_entity)

        return Permission.objects\
            .filter(user=request.user)\
            .filter(codename=delete_permission)\
            .exists()
