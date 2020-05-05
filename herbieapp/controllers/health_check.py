from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connections


class HealthCheckController(APIView):

    def get(self, request: Request) -> Response:
        connection = connections['default']
        connection.cursor()

        return Response({'connections': 'success'}, status=status.HTTP_200_OK)
