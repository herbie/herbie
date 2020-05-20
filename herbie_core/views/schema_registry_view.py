from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from herbie_core.services import SchemaRegistry


class SchemaRegistryView(APIView):
    _schema_registry = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_registry = SchemaRegistry()

    def get(self, request: Request, business_entity: str, version: str) -> Response:
        if version == '':
            version = self._schema_registry.get_schema_latest_version(business_entity)

        json_data = self._schema_registry.find_schema(business_entity, version)

        return Response(json.loads(json_data), status=status.HTTP_200_OK)
