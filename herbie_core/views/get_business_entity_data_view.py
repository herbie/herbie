from typing import Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from herbie_core.serializers.business_entity_serializer import BusinessEntitySerializer
from herbie_core.services.business_entity_manager import BusinessEntityManager
from herbie_core.services.schema_registry import SchemaRegistry
from herbie_core.views.utils import ViewUtils


class GetBusinessEntityDataView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()
        self._schema_registry = SchemaRegistry()

    def get(self, request: Request, business_entity: str, key: str, version: str = None) -> Response:
        version = self._get_latest_version_when_none(business_entity, version)

        if version is None:
            return ViewUtils.custom_response(
                f"Schema {business_entity} not found", status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        business_entity_data = self._entity_manager.find_by_key_and_version(business_entity, key, version)

        if business_entity_data is None:
            return ViewUtils.custom_response(
                f"Entity {business_entity} not found for Key: {key} / Version: {version}",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = BusinessEntitySerializer(business_entity_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def _get_latest_version_when_none(self, business_entity: str, version: str = None) -> Optional[str]:
        if version is not None:
            return version

        return self._schema_registry.get_schema_latest_version(business_entity)
