from _ast import Dict

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from wayneapp.services import BusinessEntityManager
from rest_framework.utils import json

class BusinessEntityController(APIView):
    _entity_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._entity_manager = BusinessEntityManager()

    def post(self, request: Request, type: str, key: str) -> Response:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # TODO Validation Part
        # TODO validate(body[object],type)
        version = self._get_version(body)
        try:
            generic_object, created = self._entity_manager.update_or_create(
                type, key, version, body['object']
            )
        except Exception:
            # TODO log exception?
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #TODO should we return the saved object?
        return Response({}, status=status.HTTP_200_OK)

    def _get_version(self, body: Dict):
        if 'version' not in body.keys():
            return 1
        return body['version']
