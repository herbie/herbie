from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils import json
from herbie_core.constants import ControllerConstants


class ViewUtils:
    @staticmethod
    def unauthorized_response() -> Response:
        return ViewUtils.custom_response(ControllerConstants.UNAUTHORIZED, status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def business_entity_not_exist_response(business_entity: str) -> Response:
        return ViewUtils.custom_response(
            ControllerConstants.BUSINESS_ENTITY_NOT_EXIST.format(business_entity), status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def business_entity_version_not_exist_response(version: str) -> Response:
        return ViewUtils.custom_response(
            ControllerConstants.VERSION_NOT_EXIST.format(version), status.HTTP_400_BAD_REQUEST
        )

    @staticmethod
    def custom_response(message: str, status_code: status) -> Response:
        return Response({"message": message}, status=status_code)

    @staticmethod
    def extract_body(request: Request) -> dict:
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)

        return body
