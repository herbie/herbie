import json

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from herbie_core.constants import ControllerConstants as Constants
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.services.schema_registry import SchemaRegistry
from herbie_core.views.utils import ViewUtils
from rest_framework.permissions import IsAuthenticated

from herbie_core.services.permission_manager import PermissionManager


class SaveBusinessEntityView(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._logger = logging.getLogger(__name__)
        self._validator = JsonSchemaValidator()
        self._schema_registry = SchemaRegistry()
        self._permission_classes = (IsAuthenticated,)
        self._permission_manager = PermissionManager()

    def post(self, request: Request, business_entity: str) -> Response:
        if not self._validator.business_entity_exist(business_entity):
            return ViewUtils.business_entity_not_exist_response(business_entity)
        if not self._permission_manager.has_save_permission(business_entity, request):
            return ViewUtils.unauthorized_response()

        body = ViewUtils.extract_body(request)

        if Constants.VERSION not in body:
            return ViewUtils.custom_response(Constants.VERSION_MISSING, status.HTTP_400_BAD_REQUEST)

        version = body[Constants.VERSION]

        if not self._validator.version_exist(version=version, business_entity=business_entity):
            return ViewUtils.business_entity_version_not_exist_response(version)

        key = body[Constants.KEY]
        payload = body[Constants.PAYLOAD]

        schema = self._get_json_schema(business_entity=business_entity, version=version)

        error_messages = self._validator.validate_schema(schema, payload)

        if error_messages:
            return ViewUtils.custom_response(error_messages, status.HTTP_400_BAD_REQUEST)

        created = self._entity_manager.update_or_create(business_entity, key, version, request.user, payload)

        return self._create_response(created, key, version)

    def _create_response(self, created, key, version):
        if created:
            return ViewUtils.custom_response(Constants.SAVE_MESSAGE.format(key, version), status.HTTP_201_CREATED)

        return ViewUtils.custom_response(Constants.UPDATE_MESSAGE.format(key, version), status.HTTP_200_OK)

    def _get_json_schema(self, business_entity, version) -> json:
        return self._schema_registry.find_schema(business_entity, version)
