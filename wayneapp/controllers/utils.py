from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json


class ControllerUtils:

    @staticmethod
    def custom_response(message: str, status_code: status) -> Response:
        return Response(
            {
                "message": message
            },
            status=status_code
        )
    
    @staticmethod
    def extract_body(request: Request) -> dict:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        return body
