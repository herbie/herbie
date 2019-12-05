from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from wayneapp.services import SchemaLoader


class SchemaEntityController(APIView):
    _schema_loader = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._schema_loader = SchemaLoader()

    def get(self, request: Request, business_entity: str, version: str) -> Response:
        json_data = self._schema_loader.load(business_entity, version)

        return Response(json.loads(json_data), status=status.HTTP_200_OK)
