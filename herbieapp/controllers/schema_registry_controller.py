from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from herbieapp.services import SchemaRegistry


class SchemaRegistryController(APIView):
    _schema_registry = None

    def __init__(self, _schema_registry: SchemaRegistry, **kwargs):
        self._schema_registry = _schema_registry
        super().__init__(**kwargs)

    def get(self, request: Request, business_entity: str, version: str) -> Response:
        if version == '':
            version = self._schema_registry.get_schema_latest_version(business_entity)

        json_data = self._schema_registry.find_schema(business_entity, version)

        return Response(json_data, status=status.HTTP_200_OK)
