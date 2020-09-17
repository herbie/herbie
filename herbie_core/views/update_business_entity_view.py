import json

from herbie_core.services.schema_registry import SchemaRegistry
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from herbie_core.constants import ControllerConstants as Constants
from herbie_core.services.json_schema_validator import JsonSchemaValidator
from herbie_core.models.models import AbstractBusinessEntity
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.permission_manager import PermissionManager
from herbie_core.views.utils import ViewUtils


class UpdateBusinessEntityView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._entity_manager = BusinessEntityManager()
        self._permission_classes = (IsAuthenticated,)
        self._permission_manager = PermissionManager()
        self._validator = JsonSchemaValidator()
        self._schema_registry = SchemaRegistry()

    def patch(self, request: Request, business_entity: str, key: str, version: str):
        entity = self._entity_manager.find_by_key_and_version(business_entity, key, version)

        if entity is None:
            return ViewUtils.custom_response(
                f"Entity {business_entity} not found for Key: {key} / Version: {version}",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        body = ViewUtils.extract_body(request)
        entity_dict = self._update_fields(entity, body)

        schema = self._get_json_schema(business_entity=business_entity, version=version)

        error_messages = self._validator.validate_schema(schema, entity_dict)

        if error_messages:
            return ViewUtils.custom_response(error_messages, status.HTTP_400_BAD_REQUEST)

        self._entity_manager.update_or_create(business_entity, key, version, request.user, entity_dict)

        return ViewUtils.custom_response(Constants.UPDATE_MESSAGE.format(key, version), status.HTTP_200_OK)

    def _update_fields(self, entity: AbstractBusinessEntity, payload_data: dict):
        return {**entity.data, **payload_data}

    def _get_json_schema(self, business_entity, version) -> json:
        return self._schema_registry.find_schema(business_entity, version)
