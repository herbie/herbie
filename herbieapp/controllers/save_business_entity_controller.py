import logging

from django.contrib.auth.models import Permission, AnonymousUser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from herbieapp.constants import ControllerConstants as Constants
from herbieapp.controllers.utils import ControllerUtils
from herbieapp.services import SchemaRegistry, JsonSchemaValidator
from herbieapp.services.business_entity_handler import BusinessEntityHandler

from herbieapp.services.permission_manager import PermissionManager


class SaveBusinessEntityController(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_handler = BusinessEntityHandler()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()
        self._schema_registry = SchemaRegistry()
        self._permission_classes = (IsAuthenticated,)
        self._permission_manager = PermissionManager()

    def post(self, request: Request, business_entity: str) -> Response:
        if not self._validator.business_entity_exist(business_entity):
            return ControllerUtils.business_entity_not_exist_response(business_entity)
        if not self._permission_manager.has_save_permission(business_entity, request):
            return ControllerUtils.unauthorized_response()

        body = ControllerUtils.extract_body(request)

        if Constants.VERSION not in body:
            return ControllerUtils.custom_response(
                Constants.VERSION_MISSING,
                status.HTTP_400_BAD_REQUEST
            )

        version = body[Constants.VERSION]
        key = body[Constants.KEY]
        payload = body[Constants.PAYLOAD]
        error_messages = self._validator.validate_schema(payload, business_entity, version)

        if error_messages:
            return ControllerUtils.custom_response(error_messages, status.HTTP_400_BAD_REQUEST)

        created = self._entity_handler.save(
            business_entity, key, version, request.user, payload
        )

        return self._create_response(created, key, version)

    def _create_response(self, created, key, version):
        if created:
            return ControllerUtils.custom_response(
                Constants.SAVE_MESSAGE.format(key, version),
                status.HTTP_201_CREATED
            )

        return ControllerUtils.custom_response(
            Constants.UPDATE_MESSAGE.format(key, version),
            status.HTTP_200_OK
        )


